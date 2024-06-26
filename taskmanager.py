import psutil
import platform
import os
import time
import speedtest
import socket
import uuid
import wmi
import GPUtil
import threading
import ctypes
from ctypes import wintypes

def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def display_system_info():
    clear_screen()
    uname = platform.uname()
    print("="*40, "System Information", "="*40)
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}")
    print(f"HWID: {get_hwid()}")
    input("\nPress Enter to return to the menu...")

def get_hwid():
    c = wmi.WMI()
    for disk in c.Win32_DiskDrive():
        return disk.SerialNumber.strip()

def display_cpu_info():
    clear_screen()
    print("="*40, "CPU Info", "="*40)
    c = wmi.WMI()
    for processor in c.Win32_Processor():
        print(f"Name: {processor.Name}")
        print(f"Processor ID: {processor.ProcessorId}")
        print(f"Revision: {processor.Revision}")
        print(f"DataWidth: {processor.DataWidth}")
        print(f"Status: {processor.Status}")
        print(f"ID: {processor.DeviceID}")
        print(f"Level: {processor.Level}")
        print(f"Availability: {processor.Availability}")
    input("\nPress Enter to return to the menu...")

def display_memory_info():
    clear_screen()
    print("="*40, "Memory Information", "="*40)
    svmem = psutil.virtual_memory()
    print(f"Total: {get_size(svmem.total)}")
    print(f"Available: {get_size(svmem.available)}")
    print(f"Used: {get_size(svmem.used)}")
    print(f"Percentage: {svmem.percent}%")
    input("\nPress Enter to return to the menu...")

def display_disk_info():
    clear_screen()
    print("="*40, "Disk Information", "="*40)
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"=== Device: {partition.device} ===")
        print(f"  Mountpoint: {partition.mountpoint}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        print(f"  Total Size: {get_size(partition_usage.total)}")
        print(f"  Used: {get_size(partition_usage.used)}")
        print(f"  Free: {get_size(partition_usage.free)}")
        print(f"  Percentage: {partition_usage.percent}%")
    input("\nPress Enter to return to the menu...")

def display_network_info():
    clear_screen()
    print("="*40, "Network Information", "="*40)
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            print(f"=== Interface: {interface_name} ===")
            if str(address.family) == 'AddressFamily.AF_INET':
                print(f"  IP Address (IPv4): {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast IP: {address.broadcast}")
            elif str(address.family) == 'AddressFamily.AF_INET6':
                print(f"  IP Address (IPv6): {address.address}")
    print("\n=== Additional Network Information ===")
    try:
        public_ip = socket.gethostbyname(socket.gethostname())
        print(f"Public IP Address: {public_ip}")
    except:
        print("Failed to retrieve Public IP Address")

    try:
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                               for elements in range(0, 2 * 6, 2)][::-1])
        print(f"MAC Address: {mac_address}")
    except:
        print("Failed to retrieve MAC Address")
    
    input("\nPress Enter to return to the menu...")

def display_gpu_info():
    clear_screen()
    print("="*40, "GPU Information", "="*40)
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        print(f"GPU Name: {gpu.name}")
        print(f"GPU ID: {gpu.id}")
        print(f"Load: {gpu.load*100}%")
        print(f"Free Memory: {gpu.memoryFree}MB")
        print(f"Used Memory: {gpu.memoryUsed}MB")
        print(f"Total Memory: {gpu.memoryTotal}MB")
        print(f"Temperature: {gpu.temperature} °C")
    input("\nPress Enter to return to the menu...")

def start_real_time_monitoring():
    clear_screen()
    print("="*40, "Real-Time System Monitoring", "="*40)
    stop_thread = threading.Event()

    def monitor():
        while not stop_thread.is_set():
            cpu_percent = psutil.cpu_percent(interval=1)
            mem_info = psutil.virtual_memory()
            mem_percent = mem_info.percent
            disk_info = psutil.disk_usage('/')
            disk_percent = disk_info.percent

            clear_screen()
            print("="*40, "Real-Time System Monitoring", "="*40)
            print(f"CPU Usage: {cpu_percent}%")
            print(f"Memory Usage: {mem_percent}%")
            print(f"Disk Usage: {disk_percent}%")
            time.sleep(1)

    thread = threading.Thread(target=monitor)
    thread.start()

    input("Monitoring started. Press Enter to stop...")
    stop_thread.set()
    thread.join()
    clear_screen()
    print("Monitoring stopped.")

def measure_speed():
    clear_screen()
    print("="*40, "Speed Test", "="*40)
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1024 / 1024  
    upload_speed = st.upload() / 1024 / 1024 
    print(f"Download Speed: {download_speed:.2f} Mbps")
    print(f"Upload Speed: {upload_speed:.2f} Mbps")
    input("\nPress Enter to return to the menu...")

def inject_dll(pid, dll_path):
    PROCESS_ALL_ACCESS = 0x1F0FFF
    dll_len = len(dll_path)

    h_process = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not h_process:
        print(f"Could not open process with PID {pid}.")
        return

    arg_address = ctypes.windll.kernel32.VirtualAllocEx(h_process, 0, dll_len, 0x3000, 0x40)
    if not arg_address:
        print("Could not allocate memory in the target process.")
        ctypes.windll.kernel32.CloseHandle(h_process)
        return

    written = ctypes.c_int(0)
    if not ctypes.windll.kernel32.WriteProcessMemory(h_process, arg_address, dll_path, dll_len, ctypes.byref(written)):
        print("Could not write DLL path to the target process memory.")
        ctypes.windll.kernel32.VirtualFreeEx(h_process, arg_address, 0, 0x8000)
        ctypes.windll.kernel32.CloseHandle(h_process)
        return

    h_kernel32 = ctypes.windll.kernel32.GetModuleHandleW("kernel32.dll")
    h_loadlib = ctypes.windll.kernel32.GetProcAddress(h_kernel32, b"LoadLibraryA")

    if not h_loadlib:
        print("Could not get address of LoadLibraryA.")
        ctypes.windll.kernel32.VirtualFreeEx(h_process, arg_address, 0, 0x8000)
        ctypes.windll.kernel32.CloseHandle(h_process)
        return

    thread_id = ctypes.c_ulong(0)
    if not ctypes.windll.kernel32.CreateRemoteThread(h_process, None, 0, h_loadlib, arg_address, 0, ctypes.byref(thread_id)):
        print("Could not create remote thread in the target process.")
        ctypes.windll.kernel32.VirtualFreeEx(h_process, arg_address, 0, 0x8000)
        ctypes.windll.kernel32.CloseHandle(h_process)
        return

    print(f"DLL injected successfully into process with PID {pid}.")

def display_process_info():
    clear_screen()
    print("="*40, "Process Information", "="*40)
    processes = []
    for proc in psutil.process_iter(attrs=['pid', 'name', 'username']):
        try:
            proc_info = proc.info
            processes.append(proc_info)
            print(f"PID: {proc_info['pid']} | Name: {proc_info['name']} | User: {proc_info['username']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    pid_to_kill = input("\nEnter the PID of the process to kill (or press Enter to skip): ").strip()
    if pid_to_kill:
        try:
            pid_to_kill = int(pid_to_kill)
            process = psutil.Process(pid_to_kill)
            process.terminate()
            process.wait()  # Wait for the process to be terminated
            print(f"Process {pid_to_kill} terminated successfully.")
        except (psutil.NoSuchProcess, ValueError):
            print(f"Process with PID {pid_to_kill} does not exist.")
        except psutil.AccessDenied:
            print(f"Access denied to terminate process with PID {pid_to_kill}.")
    
    input("\nPress Enter to return to the menu...")

def inject_dll_menu():
    clear_screen()
    print("="*40, "DLL Injection", "="*40)
    dll_path = input("Enter the full path of the DLL to inject: ").strip()
    if dll_path:
        pid_to_inject = input("Enter the PID of the process to inject the DLL into: ").strip()
        if pid_to_inject:
            try:
                pid_to_inject = int(pid_to_inject)
                inject_dll(pid_to_inject, dll_path.encode('utf-8'))
            except ValueError:
                print(f"Invalid PID: {pid_to_inject}")
    input("\nPress Enter to return to the menu...")

def output_system_info_to_file():
    uname = platform.uname()
    svmem = psutil.virtual_memory()
    partitions = psutil.disk_partitions()
    if_addrs = psutil.net_if_addrs()
    gpus = GPUtil.getGPUs()

    with open("system.txt", "w") as f:
        f.write("="*40 + " System Information " + "="*40 + "\n")
        f.write(f"System: {uname.system}\n")
        f.write(f"Node Name: {uname.node}\n")
        f.write(f"Release: {uname.release}\n")
        f.write(f"Version: {uname.version}\n")
        f.write(f"Machine: {uname.machine}\n")
        f.write(f"Processor: {uname.processor}\n")
        f.write(f"HWID: {get_hwid()}\n\n")

        f.write("="*40 + " Memory Information " + "="*40 + "\n")
        f.write(f"Total Memory: {get_size(svmem.total)}\n")
        f.write(f"Available Memory: {get_size(svmem.available)}\n")
        f.write(f"Used Memory: {get_size(svmem.used)}\n")
        f.write(f"Memory Percentage: {svmem.percent}%\n\n")

        f.write("="*40 + " Disk Information " + "="*40 + "\n")
        for partition in partitions:
            f.write(f"=== Device: {partition.device} ===\n")
            f.write(f"  Mountpoint: {partition.mountpoint}\n")
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                f.write(f"  Total Size: {get_size(partition_usage.total)}\n")
                f.write(f"  Used: {get_size(partition_usage.used)}\n")
                f.write(f"  Free: {get_size(partition_usage.free)}\n")
                f.write(f"  Percentage: {partition_usage.percent}%\n")
            except PermissionError:
                continue
            f.write("\n")

        f.write("="*40 + " Network Information " + "="*40 + "\n")
        for interface_name, interface_addresses in if_addrs.items():
            f.write(f"=== Interface: {interface_name} ===\n")
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    f.write(f"  IP Address (IPv4): {address.address}\n")
                    f.write(f"  Netmask: {address.netmask}\n")
                    f.write(f"  Broadcast IP: {address.broadcast}\n")
                elif str(address.family) == 'AddressFamily.AF_INET6':
                    f.write(f"  IP Address (IPv6): {address.address}\n")
            f.write("\n")

        f.write("="*40 + " GPU Information " + "="*40 + "\n")
        for gpu in gpus:
            f.write(f"GPU Name: {gpu.name}\n")
            f.write(f"GPU ID: {gpu.id}\n")
            f.write(f"Load: {gpu.load*100}%\n")
            f.write(f"Free Memory: {gpu.memoryFree}MB\n")
            f.write(f"Used Memory: {gpu.memoryUsed}MB\n")
            f.write(f"Total Memory: {gpu.memoryTotal}MB\n")
            f.write(f"Temperature: {gpu.temperature} °C\n")
            f.write("\n")

    print("System information exported to 'system.txt'.")
    input("\nPress Enter to return to the menu...")

def main():
    menu = {
        '1': ("System Information", display_system_info),
        '2': ("CPU Information", display_cpu_info),
        '3': ("Memory Information", display_memory_info),
        '4': ("Disk Information", display_disk_info),
        '5': ("Network Information", display_network_info),
        '6': ("GPU Information", display_gpu_info),
        '7': ("Start Real-Time Monitoring", start_real_time_monitoring),
        '8': ("Speed Test", measure_speed),
        '9': ("Process Information", display_process_info),
        '10': ("Inject DLL", inject_dll_menu),
        '11': ("Output System Information to 'system.txt'", output_system_info_to_file),
        '0': ("Exit", lambda: exit(0))
    }

    while True:
        clear_screen()
        print("="*40, "Task Manager Menu", "="*40)
        for key, value in menu.items():
            print(f"{key}: {value[0]}")

        choice = input("Enter your choice: ").strip()
        if choice in menu:
            menu[choice][1]()  
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == '__main__':
    main()
