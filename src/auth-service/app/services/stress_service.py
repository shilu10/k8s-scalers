import subprocess
from flask import current_app as app


def stress_ng_cpu(cores=1, duration=10, load=85):
    """
    Stress CPU with specified number of workers, duration, and load.

    :param cores: Number of CPU stressors
    :param duration: Duration in seconds
    :param load: CPU load percentage per stressor (0-100)
    """
    try:
        app.logger.info(f"Stressing {cores} cores for {duration}s at {load}% load each...")
        subprocess.run(
            ["stress-ng", "--cpu", str(cores), "--cpu-load", str(load), "--timeout", f"{duration}s"],
            check=True
        )

        return {"success": True}

    except FileNotFoundError:
        app.logger.warning("No installation of stress-ng found. Install with: sudo apt install stress-ng")
        return {"success": False, "err": "Install 'stress-ng' with: sudo apt install stress-ng"}
    except subprocess.CalledProcessError as e:
        app.logger.error(f"CPU stress failed: {e}")
        return {"success": False, "err": str(e)}


def stress_ng_mem(mem_bytes="256M", duration=10, vm_workers=1):
    """
    Stress memory with minimal CPU usage.

    :param mem_bytes: Amount of memory to stress (e.g., '256M', '1G')
    :param duration: Duration in seconds
    :param vm_workers: Number of memory stress workers
    """
    try:
        app.logger.info(f"Stressing memory (minimal CPU) with {vm_workers} workers, "
                        f"{mem_bytes} each for {duration}s...")
        subprocess.run(
            [
                "stress-ng",
                "--vm", str(vm_workers),
                "--vm-bytes", str(mem_bytes),
                "--vm-keep",
                "--timeout", f"{duration}s"
            ],
            check=True
        )
        return {"success": True}

    except FileNotFoundError:
        app.logger.warning("No installation of stress-ng found. Install with: sudo apt install stress-ng")
        return {"success": False, "err": "Install 'stress-ng' with: sudo apt install stress-ng"}
    except subprocess.CalledProcessError as e:
        app.logger.error(f"Memory stress failed: {e}")
        return {"success": False, "err": str(e)}


def stress_ng_cpu_mem(cpu_cores=4, mem_bytes='256M', vm_workers=1, duration=10, load=85):
    """
    Stress both CPU and memory using stress-ng.

    :param cpu_cores: Number of CPU stress workers
    :param mem_bytes: Memory to allocate per vm worker (e.g., '512M', '2G')
    :param vm_workers: Number of vm stress workers
    :param duration: Duration in seconds
    :param load: CPU load per core (0-100%)
    """
    try:
        app.logger.info(f"Stressing {cpu_cores} CPU cores at {load}% load and {vm_workers} memory workers "
                        f"with {mem_bytes} for {duration}s...")

        subprocess.run([
            "stress-ng",
            "--cpu", str(cpu_cores),
            "--cpu-load", str(load),
            "--vm", str(vm_workers),
            "--vm-bytes", str(mem_bytes),
            "--vm-keep",
            "--timeout", f"{duration}s"
        ], check=True)

        return {"success": True}

    except FileNotFoundError:
        app.logger.warning("No installation of stress-ng found. Install with: sudo apt install stress-ng")
        return {"success": False, "err": "Install 'stress-ng' with: sudo apt install stress-ng"}
    except subprocess.CalledProcessError as e:
        app.logger.error(f"CPU+MEM stress failed: {e}")
        return {"success": False, "err": str(e)}
