import os 
import sys 
import psutil

def get_memory_usage():
    memory_usage = psutil.virtual_memory()

    return memory_usage