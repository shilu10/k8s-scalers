from kubernetes import client, config
import requests
from config import Config


def get_pods_ip_list():
    try: 
        # Use this inside any pod running in the cluster
        config.load_incluster_config()

        v1 = client.CoreV1Api()
        pod_list = v1.list_namespaced_pod(Config.ENDPOINT,
                                    label_selector=Config.LABEL_SELECTOR
                                    )

        ip_list = [pod.status.pod_ip for pod in pod_list.items if pod.status.phase == "Running"]

        return ip_list
    
    except Exception as err:
        return err 
    

def send_request(url, payload, headers):
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        return response 
    
    except Exception as err:
        return err 
    

def cpu_stress(ip_list, load, duration, workers):
    try:
        results = {}
        for ip_addr in ip_list:
            endpoint = Config.ENDPOINT
            port = Config.PORT
            url = f"http://{ip_addr}:{port}/{endpoint}/stress_cpu"
            headers = {"Content-Type": "application/json"}
            payload = {
                "load": load,
                "duration": duration,
                "worker": workers
            }
        
            response = send_request(url, payload, headers)

            if not isinstance(response, requests.Response):
                results[ip_addr] = {
                    "err": response
                }
            
            else:
                results[ip_addr] = {
                    "status": response.status_code,
                    "body": response.text
                }
        
        return results

    except Exception as err:
        return {
            "reason": err
        }
            
            
def mem_stress(ip_list, duration, mem_bytes):
    try:
        results = {}
        for ip_addr in ip_list:
            endpoint = Config.ENDPOINT
            port = Config.PORT
            url = f"http://{ip_addr}:{port}/{endpoint}/stress_cpu"
            headers = {"Content-Type": "application/json"}
            payload = {
                "duration": duration,
                "mem_bytes": mem_bytes
            }
        
            response = send_request(url, payload, headers)

            if not isinstance(response, requests.Response):
                results[ip_addr] = {
                    "err": response
                }
            
            else:
                results[ip_addr] = {
                    "status": response.status_code,
                    "body": response.text
                }
        
        return results

    except Exception as err:
        return {
            "reason": err
        }
            

def mem_and_cpu_stress(ip_list, duration, mem_bytes, load, workers):
    try:
        results = {}
        for ip_addr in ip_list:
            endpoint = Config.ENDPOINT
            port = Config.PORT
            url = f"http://{ip_addr}:{port}/{endpoint}/stress_cpu"
            headers = {"Content-Type": "application/json"}
            payload = {
                "duration": duration,
                "mem_bytes": mem_bytes,
                "load": load,
                "workers": workers
            }
        
            response = send_request(url, payload, headers)

            if not isinstance(response, requests.Response):
                results[ip_addr] = {
                    "err": response
                }
            
            else:
                results[ip_addr] = {
                    "status": response.status_code,
                    "body": response.text
                }
        
        return results

    except Exception as err:
        return {
            "reason": err
        }
    

def main():
    ip_list = get_pods_ip_list()

    if Config.STRESS_TYPE == "cpu":
        load = Config.LOAD
        duration = Config.DURATION
        workers = Config.WORKERS

        return cpu_stress(ip_list=ip_list, 
                          load=load, 
                          duration=duration, 
                          workers=workers
                        )
    
    if Config.STRESS_TYPE == "mem":
        duration = Config.DURATION
        mem_bytes = Config.MEM_BYTES

        return mem_stress(ip_list=ip_list, 
                          duration=duration, 
                          mem_bytes=mem_bytes
                        )
    
    if Config.STRESS_TYPE == "cpu_and_mem":
        duration = Config.DURATION
        mem_bytes = Config.MEM_BYTES
        load = Config.LOAD
        workers = Config.WORKERS

        return mem_and_cpu_stress(ip_list=ip_list, 
                                  duration=duration, 
                                  mem_bytes=mem_bytes, 
                                  load=load, workers=workers)
    

if __name__ == "__main__":
    print(main())