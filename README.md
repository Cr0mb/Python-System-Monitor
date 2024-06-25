![image](https://github.com/Cr0mb/Python-System-Information-and-Monitoring-Tool/assets/137664526/861ed2e5-35ea-44ae-8d0b-186c0420b1e6)


# System Information and Monitoring Tool
This Python script provides a comprehensive set of functionalities to gather and display system information, monitor real-time system metrics, perform speed tests, and display process details. It is useful for understanding various aspects of your system's performance.

## Features

> System Information: Display details about the operating system, node name, release, version, machine, processor, and hardware ID.

> CPU Information: View CPU details such as name, processor ID, revision, data width, status, and more.

> Memory Information: Show total, available, used memory, and percentage usage.

> Disk Information: Retrieve details about disk partitions, including total size, used space, free space, and percentage usage.

> Network Information: Display network interfaces, IP addresses (IPv4 and IPv6), broadcast IP, public IP address, and MAC address.

> GPU Information: Provide information about GPUs including name, load, free memory, used memory, total memory, and temperature.

> Real-Time System Monitoring: Monitor CPU usage, memory usage, and disk usage in real-time.

> Speed Test: Measure download and upload speeds using speedtest-cli.

> Process Information: List running processes along with their PID, name, and user.

## Requirements
- Python 3.x

```
pip install psutil speedtest-cli GPUtil wmi
```

- psutil: Cross-platform library for retrieving system utilization data.
- speedtest-cli: Command-line interface for testing internet bandwidth using speedtest.net.
- GPUtil: GPU utilization library.
- wmi: Windows Management Instrumentation interface for Python.

