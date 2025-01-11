import os
import csv
import time
import psutil
import asyncio
from ping3 import ping
from bleak import BleakScanner
from datetime import datetime


# Function to check Wi-Fi/Ethernet connectivity using ping
def check_connectivity(host="8.8.8.8"):
    response = ping(host)
    return response is not None


# Function to check Bluetooth device availability
async def check_bluetooth_devices():
    try:
        devices = await BleakScanner.discover()
        if not devices:
            return "No Bluetooth devices found"
        return [device.name or device.address for device in devices]
    except Exception as e:
        return f"Error scanning Bluetooth devices: {str(e)}"


# Function to monitor system resources (CPU, memory, disk)
def monitor_system_resources(disk_path="C:\\"):
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent

    try:
        disk = psutil.disk_usage(disk_path).percent
    except Exception as e:
        disk = f"Error: {e}"
    
    return cpu, memory, disk


# Function to write results to a log file
def write_to_log(log_message):
    with open("system_test.log", "a") as log_file:
        log_file.write(log_message + "\n")


# Function to generate a report in CSV format
def generate_report(test_results):
    fieldnames = ['Timestamp', 'Test', 'Status', 'Details']
    file_exists = os.path.exists('system_test_report.csv')

    with open('system_test_report.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:  # Write header only if the file doesn't exist
            writer.writeheader()
        writer.writerows(test_results)


# Main function to run tests
async def run_system_tests():
    test_results = []

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Test 1: Check network connectivity
    connectivity_status = check_connectivity()
    test_results.append({
        'Timestamp': timestamp,
        'Test': 'Network Connectivity',
        'Status': 'Pass' if connectivity_status else 'Fail',
        'Details': 'Internet Connectivity Test'
    })

    # Test 2: Check Bluetooth devices
    bluetooth_status = "Fail"
    bluetooth_devices = None
    try:
        bluetooth_devices = await check_bluetooth_devices()
        bluetooth_status = "Pass" if bluetooth_devices and isinstance(bluetooth_devices, list) else "Fail"
    except Exception as e:
        bluetooth_status = f"Error: {str(e)}"

    test_results.append({
        'Timestamp': timestamp,
        'Test': 'Bluetooth Device Discovery',
        'Status': bluetooth_status,
        'Details': bluetooth_devices if bluetooth_devices else "No devices found"
    })

    # Test 3: Monitor system resources
    cpu, memory, disk = monitor_system_resources()
    test_results.append({
        'Timestamp': timestamp,
        'Test': 'CPU Usage',
        'Status': 'Pass' if isinstance(cpu, float) and cpu < 90 else 'Fail',
        'Details': f'CPU Usage: {cpu}%'
    })
    test_results.append({
        'Timestamp': timestamp,
        'Test': 'Memory Usage',
        'Status': 'Pass' if isinstance(memory, float) and memory < 90 else 'Fail',
        'Details': f'Memory Usage: {memory}%'
    })
    test_results.append({
        'Timestamp': timestamp,
        'Test': 'Disk Usage',
        'Status': 'Pass' if isinstance(disk, float) and disk < 90 else 'Fail',
        'Details': f'Disk Usage: {disk}%'
    })

    # Generate report and log the results
    generate_report(test_results)
    for result in test_results:
        log_message = f"{result['Timestamp']} - {result['Test']} - {result['Status']} - {result['Details']}"
        write_to_log(log_message)


# Run the system tests
if __name__ == '__main__':
    asyncio.run(run_system_tests())
