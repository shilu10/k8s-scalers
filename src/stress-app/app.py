import logging
from kubernetes import client, config
import requests
from config import Config
from concurrent.futures import ThreadPoolExecutor, as_completed



# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def get_pods_ip_list():
    try:
        config.load_incluster_config()
        v1 = client.CoreV1Api()
        pod_list = v1.list_namespaced_pod(
            Config.NAMESPACE,
            label_selector=Config.LABEL_SELECTOR
        )

        ip_list = [pod.status.pod_ip for pod in pod_list.items if pod.status.phase == "Running"]

        if not ip_list:
            raise ValueError("No running pods found.")

        logging.debug(f"Pod IPs: {ip_list}")
        return ip_list

    except Exception as e:
        logging.error(f"Pod discovery failed: {e}")
        return []

def send_request(url, payload, headers):
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response
    except Exception as err:
        logging.error(f"Request failed to {url}: {err}")
        return err

def cpu_stress(ip_list, load, duration, workers):
    results = {}
    headers = {"Content-Type": "application/json"}
    payload = {"load": load, "duration": duration, "workers": workers}

    def send(ip):
        url = f"http://{ip}:{Config.PORT}/api/v1/stress_cpu"
        logging.debug(f"Sending request to {url} with payload {payload}")
        response = send_request(url, payload, headers)
        return ip, response

    with ThreadPoolExecutor(max_workers=len(ip_list)) as executor:
        futures = [executor.submit(send, ip) for ip in ip_list]

        for future in as_completed(futures):
            ip, response = future.result()
            if not isinstance(response, requests.Response):
                results[ip] = {"err": str(response)}
                logging.error(f"Request to {ip} failed: {response}")
            else:
                results[ip] = {
                    "status": response.status_code,
                    "body": response.text
                }
                logging.debug(f"Response from {ip}: {response.text}")

    return results

def mem_stress(ip_list, duration, mem_bytes, vm_workers):
    results = {}
    headers = {"Content-Type": "application/json"}
    mem_bytes = str(mem_bytes) + "M"
    payload = {"duration": duration, "mem_bytes": mem_bytes, "vm_workers": vm_workers}

    def send(ip):
        url = f"http://{ip}:{Config.PORT}/api/v1/stress_mem"
        logging.debug(f"Sending request to {url} with payload {payload}")
        response = send_request(url, payload, headers)
        return ip, response

    with ThreadPoolExecutor(max_workers=len(ip_list)) as executor:
        futures = [executor.submit(send, ip) for ip in ip_list]

        for future in as_completed(futures):
            ip, response = future.result()
            if not isinstance(response, requests.Response):
                results[ip] = {"err": str(response)}
                logging.error(f"Request to {ip} failed: {response}")
            else:
                results[ip] = {
                    "status": response.status_code,
                    "body": response.text
                }
                logging.debug(f"Response from {ip}: {response.text}")

    return results

def mem_and_cpu_stress(ip_list, duration, mem_bytes, load, workers, vm_workers):
    results = {}
    headers = {"Content-Type": "application/json"}
    mem_bytes = str(mem_bytes) + "M"
    payload = {"duration": duration, "mem_bytes": mem_bytes, "load": load, "workers": workers, "vm_workers": vm_workers}

    def send(ip):
        url = f"http://{ip}:{Config.PORT}/api/v1/stress_mem_cpu"
        logging.debug(f"Sending request to {url} with payload {payload}")
        response = send_request(url, payload, headers)
        return ip, response

    with ThreadPoolExecutor(max_workers=len(ip_list)) as executor:
        futures = [executor.submit(send, ip) for ip in ip_list]

        for future in as_completed(futures):
            ip, response = future.result()
            if not isinstance(response, requests.Response):
                results[ip] = {"err": str(response)}
                logging.error(f"Request to {ip} failed: {response}")
            else:
                results[ip] = {
                    "status": response.status_code,
                    "body": response.text
                }
                logging.debug(f"Response from {ip}: {response.text}")

    return results

def main():
    ip_list = get_pods_ip_list()
    if not ip_list:
        return {"error": "No running pods found or failed to fetch pod IPs."}

    if Config.STRESS_TYPE == "cpu":
        return cpu_stress(ip_list, Config.LOAD, Config.DURATION, Config.WORKERS)

    elif Config.STRESS_TYPE == "mem":
        return mem_stress(ip_list, Config.DURATION, Config.MEM_BYTES, Config.WORKERS)

    elif Config.STRESS_TYPE == "cpu_and_mem":
        return mem_and_cpu_stress(ip_list, Config.DURATION, Config.MEM_BYTES, Config.LOAD, Config.WORKERS, Config.VM_WORKERS)

    else:
        logging.error("Invalid STRESS_TYPE provided.")
        return {"error": "Invalid STRESS_TYPE"}


if __name__ == "__main__":
    result = main()
    logging.info(f"Final result: {result}")
