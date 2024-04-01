import os 
import sys 
import psutil

def get_cpu_usage():
    cpu_usage = psutil.cpu_percent()

    return cpu_usage