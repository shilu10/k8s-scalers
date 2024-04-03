import subprocess
import os 
import threading


def stress_ng_cpu(cores=0, duration=10, load=85):
    """
    Stress CPU with specified number of workers, duration, and load.

    :param cores: Number of CPU stressors
    :param duration: Duration in seconds
    :param load: CPU load percentage per stressor (0-100)
    """
    try:
        print(f"Stressing {cores} cores for {duration}s at {load}% load each...")
        subprocess.run(
            ["stress-ng", "--cpu", str(cores), "--cpu-load", str(load), "--timeout", f"{duration}s"],
            check=True
        )

        return {
            "success": True
        }

    except FileNotFoundError:
        return {
            "success": False,
            "err": "Install 'stress-ng' with: sudo apt install stress-ng"
        }


def stress_ng_mem(mem_bytes="256M", duration=10):
    """
    Stress CPU with specified number of workers, duration, and load.

    :param mem_byte: Amount of memory
    :param duration: Duration in seconds
    """
    try:
        print(f"Stressing {mem_bytes} bytes for {duration}s ...")
        subprocess.run(
            ["stress-ng", "--vm-bytes", str(mem_bytes), "--timeout", f"{duration}s"],
            check=True
        )

        return {
            "success": True
        }

    except FileNotFoundError:
        return {
            "success": False,
            "err": "Install 'stress-ng' with: sudo apt install stress-ng"
        }


def stress_ng_cpu_mem(cpu_cores=4, mem_bytes='256M', duration=10, load=85):
    """
    Stress CPU and memory using 'stress-ng'.

    :param cpu_cores: Number of CPU stress workers
    :param mem_workers: Number of memory stress workers
    :param mem_bytes: Total memory to use (not per worker) (e.g., '512M', '2G')
    :param duration: Duration in seconds
    :param load: CPU load per core (0-100%)
    """
    try:
        print(f"Stressing {cpu_cores} CPU cores at {load}% load and {mem_workers} memory workers "
              f"using total {mem_bytes} for {duration} seconds...")

        subprocess.run([
            "stress-ng",
            "--cpu", str(cpu_cores),
            "--cpu-load", str(load),
            "--vm-bytes", str(mem_bytes),
            "--timeout", f"{duration}s"
        ], check=True)

    except FileNotFoundError:
        return {
            "success": False,
            "err": "Install 'stress-ng' with: sudo apt install stress-ng"
        }
