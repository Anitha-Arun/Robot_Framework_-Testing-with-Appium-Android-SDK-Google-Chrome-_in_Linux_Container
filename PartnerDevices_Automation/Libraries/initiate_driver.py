import os
import subprocess
import time
import json
from subprocess import DEVNULL, CalledProcessError
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from AccountSetup import AccountSetup
from device_control import connect_device, clear_app_caches, device_udid

obj_dev = AccountSetup.getInstance()

# Load configuration safely
def load_config(file_path="config.json"):
    try:
        with open(file_path, "r") as f:
            return json.load(f, object_pairs_hook=OrderedDict)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
        return {}

config = load_config()
appium_servers = []

def start_appium_servers():
    os.environ['PATH'] += ':/usr/bin'
    
    consoles = config.get("consoles", {})
    if consoles:
        print(" 'consoles' key is present in the config file")
    
    consoles_list = list(consoles.keys()) if consoles else []
    connected_devices = list(config.get("devices", {}).keys()) + consoles_list
    device_list = [device for device in connected_devices if device]

    devices_key_length = len(device_list)
    print("keys length ", devices_key_length)
    
    if devices_key_length == 1:
        print("WARNING : Only ONE device connected.")
    elif devices_key_length == 2:
        print("WARNING : Only TWO devices connected.")
    
    devices = config.get("devices", {})
    print("Devices ", devices)
    print("Consoles ", consoles)
    
    try:
        output = subprocess.check_output("netstat -tuln | grep ':82[0-9]' || true", shell=True)
        ports = [line.split()[3].split(':')[1] for line in output.decode("utf-8").splitlines()]
        print("Ports in use:", ports)
        for port in ports:
            subprocess.run(f"lsof -ti:{port} | xargs kill -9", shell=True)
        print("Cleared ports in range 8200-8299")
    except subprocess.CalledProcessError as e:
        print("Error checking or clearing ports:", e)

    # Safely get ports
    port_list = [
        devices[d].get("port", None) for d in devices
    ] + [
        consoles[c].get("port", None) for c in consoles_list
    ]
    port_list = [port for port in port_list if port]  # Remove None values
    print("Port List:", port_list)
    
    for port in port_list:
        try:
            port_output = subprocess.check_output(f"lsof -ti:{port} || true", shell=True)
            if port_output:
                port_pid = port_output.decode("utf-8").strip()
                subprocess.run(f"kill -9 {port_pid}", shell=True)
                print(f"Killed Appium server on port {port}")
        except subprocess.CalledProcessError as e:
            print(f"Error killing Appium server on port {port}: {e}")

    time.sleep(2)
    
    if len(port_list) != len(set(port_list)):
        raise AssertionError("Ports for different devices must be unique.")
    
    log_dir = os.path.join(BuiltIn().get_variable_value("${OUTPUT DIR}"), "appium_logs")
    os.makedirs(log_dir, exist_ok=True)

    for port in port_list:
        file_name = os.path.join(log_dir, f"appium_{port}.txt")
        appium_servers.append(
            subprocess.Popen(
                ["appium", "-p", str(port), "--log", file_name],
                stdout=DEVNULL,
                stdin=DEVNULL
            )
        )
        time.sleep(5)

    time.sleep(10)

def teardown_devices():
    """
    Process cleanup - WebDrivers and then Appium
    """
    for device in list(config.get("devices", {}).keys()):
        obj_dev.teardown_device_driver(device)

    for server_proc in appium_servers:
        try:
            cmd = f"kill -9 {server_proc.pid}"
            result = subprocess.run(cmd, shell=True, check=True)
            print(f"Successfully killed Appium server with PID: {server_proc.pid}")
        except CalledProcessError as e:
            print(f"Failed to kill Appium server with PID: {server_proc.pid} due to: {e}")

    appium_servers.clear()

def setup_devices():
    """
    Process startup - First Appium and then the WebDrivers
    """
    start_appium_servers()

    devices_config = config.get("devices", {})
    for device_name in list(devices_config.keys()):
        device_config = devices_config.get(device_name, {})
        desired_caps = device_config.get("desired_caps", None)
        if not desired_caps:
            print(f"ERROR: 'desired_caps' not found for device: {device_name}")
            continue  # Skip this device setup if 'desired_caps' is missing

        connect_device(device_name, config)

        # Clear caches to force consistent device state prior to launching automation.
        clear_app_caches(
            device_name, config, [config.get("companyPortal_Package", ""), config.get("common_desired_caps", {}).get("appPackage", "")]
        )

        # Launch automation
        obj_dev.setup_device_driver(device_name, config)
        print(f"{device_name}: Setup complete")

    if "consoles" in config:
        for console in list(config["consoles"].keys()):
            root_console(console, config)
            clear_app_caches(
                console, config, [config.get("companyPortal_Package", ""), config.get("common_desired_caps", {}).get("appPackage", "")]
            )
            obj_dev.setup_console_driver(console, config)

def read_config():
    """
    Read the main configuration file.
    (Logging the contents to aid debugging.)
    """
    with open("config.json") as file:
        tmp_config = json.load(file, object_pairs_hook=OrderedDict)
    print("Config loaded: ", tmp_config)  # Debugging line
    return tmp_config

def root_console(console: str, config: dict):
    _udid = device_udid(console, config)
    print(f"{console}: root_console, udid={_udid}")
    print("Inside Root")
    print("Type of device : ", type(console))
    cmd_root = "adb -s " + str(_udid) + " root"
    print("Root Command :", cmd_root)
    try:
        subprocess.check_call(cmd_root, stdout=subprocess.PIPE, shell=True)
        time.sleep(2)
        cp_version = subprocess.check_output(
            "adb -s " + _udid + " shell dumpsys package com.microsoft.windowsintune.companyportal | grep versionName",
            shell=True,
        )
        print("CP version : ", cp_version.decode("utf-8").strip())
    except subprocess.CalledProcessError as e:
        print("CP might not be found in debug build")

    try:
        teams_version = subprocess.check_output(
            "adb -s " + _udid + " shell dumpsys package com.microsoft.skype.teams.ipphone | grep versionName",
            shell=True,
        )
        print("Teams version : ", teams_version.decode("utf-8").strip())
    except subprocess.CalledProcessError as e:
        print("Teams package not found")

    try:
        firmware_ver = subprocess.check_output("adb -s " + _udid + " shell getprop build.firmware.version", shell=True)
        version = firmware_ver.decode("utf-8").strip()
        print("Firmware version is : {}".format(version))
    except subprocess.CalledProcessError as e:
        print("Firmware version retrieval failed")