import pynvml


def print_gpu_utilization():
    try:
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        print(f"GPU memory occupied: {info.used//1024**2} MB.")
    # if this is not a GPU nb bypass
    except pynvml.NVMLError_LibraryNotFound:
        print("GPU not enabled")
