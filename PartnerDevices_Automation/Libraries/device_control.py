import platform
import time
import traceback
import subprocess
from subprocess import CalledProcessError, TimeoutExpired, PIPE


def ts_print(*args):
    # Prepend UTC timestamp to 'args' and output with flush after write:
    print(time.strftime("%Y-%m-%d %H:%M:%S UTC ", time.gmtime()), *args, flush=True)


def print_exception(context, device_name=None):
    if device_name is None:
        ts_print(f"{context}: {traceback.format_exc()}")
    else:
        ts_print(f"{device_name}: {context}: {traceback.format_exc()}")


def connect_device(device_name: str, config: dict):
    _udid = device_udid(device_name, config)
    ts_print(f"{device_name}: ADB connect_device, udid={_udid}...")

    cmd_connect = "adb connect " + str(_udid.split(":")[0])
    # ts_print(f"{device_name}: connect with: {cmd_connect}")
    _result = subprocess.run(
        cmd_connect,
        stdout=PIPE,
        stderr=PIPE,
        shell=True,
        text=True,
        check=True,
        timeout=float(1 * 60),
    )

    # This will also 'fail' if the device is connected but 'offline':
    #   Every time the adb server sends a command to the adbd daemon on a device it expects a
    #   response. If it does not get the response within allotted time limit (~3 seconds) ADB
    #   marks the device 'offline', but does not set a failed return code.
    #
    #   The timeouts can be caused by many different software and or hardware problems on the device and the host system itself.
    #
    # If so, command result contains "failed to connect to 10.31.78.54:5555"
    if "failed" in _result.stdout.lower():
        ts_print(f"FATAL: {device_name} ({_udid}) not responding - ADB: {_result}")
        raise AssertionError(f"{device_name} ({_udid}) failed")

    # Additional insurance - make sure the device is not 'offline'
    wait_for_device_online(device_name, config)

    # Optional - attempt to root the connection - allows storage info printing
    cmd_root = "adb -s " + str(_udid) + " root"
    cmd_timeout = float(1 * 60)
    # ts_print(f"{device_name}: root with: {cmd_root}")
    try:
        _results = subprocess.run(cmd_root, stdout=PIPE ,  check=True, shell=True,timeout=cmd_timeout)
        ts_print(f"{device_name}: 'root' result: '{_results}'")
    except CalledProcessError:
        print_exception("'root' failed result", device_name)
    except TimeoutExpired:
        ts_print(f"{device_name}: 'root' result: TimeoutExpired(after {cmd_timeout} secs).")

    # Again, make sure the 'root' did not knock the device 'offline'
    wait_for_device_online(device_name, config)


def disconnect_device(device_name: str, config: dict):
    _udid = device_udid(device_name, config)
    ts_print(f"{device_name}: disconnect_device, udid={_udid}")

    cmd_disconnect = "adb disconnect " + str(_udid)
    ts_print(f"{device_name}: disonnect with: {cmd_disconnect}")
    subprocess.run(cmd_disconnect, stdout=PIPE, check=True, shell=True)
    time.sleep(2)


def ping_device(device_name: str, config: dict, max_pings=10):
    udid = device_udid(device_name, config)
    if udid.count(".") != 3:
        ts_print(f"{device_name}: '{udid}' doesn't appear to be an IP address, ping skipped.")
        return
    just_ip = udid.split(":")[0]

    # Option for the number of packets as a function of OS
    param = "-n" if platform.system().lower() == "windows" else "-c"

    inter_ping_sleep = 3

    cmd_ping = f"ping {param} 1 {just_ip}"
    for attempt in range(1, max_pings + 1):
        try:
            response = subprocess.check_output(cmd_ping, text=True, stderr=PIPE)
            if f"Reply from {just_ip}" in response:
                break
        except CalledProcessError as pingFail:
            # Ignore, but report
            if "timed out" in pingFail.output:
                ts_print(f"{device_name}: ping_device {just_ip}: Request timed out.")
            else:
                ts_print(f"{device_name}: ping_device {just_ip}: {str(pingFail.output).strip()}")
        time.sleep(inter_ping_sleep)

    if attempt == max_pings:
        raise AssertionError(f"{device_name} (ping {just_ip}): did not respond after {str(attempt)} attempts.")

    ts_print(f"{device_name}: ping {just_ip} responded after {str(attempt)} of {str(max_pings)} attempts.")

    if attempt > 1:
        # Newly responding: Wait a bit more, a 'root' connect will be honored, even
        # if the device is not fully up:
        post_ping_sleep = 15
        ts_print(f"{device_name}: Newly responding to ping, sleeping an additional {str(post_ping_sleep)}.")
        time.sleep(post_ping_sleep)


def reboot_device(device_name: str, config: dict):
    _udid = device_udid(device_name, config)
    ts_print(f"{device_name}: reboot_device, udid={_udid}")

    cmd_reboot = "adb -s " + str(_udid) + " reboot"
    # ts_print(f"{device_name}: reboot with: '{cmd_reboot}'")
    try:
        # Note short timeout - device connection sometimes hangs, and we want to begin
        # pinging it before it is ready to respond.
        subprocess.run(cmd_reboot,stdout=PIPE, text=True, check=True,shell=True, timeout=float(10))
        time.sleep(2)
    except TimeoutExpired:
        # Assuming this is ok - the socket does not always close even when the device is rebooting.
        ts_print(f"{device_name}: reboot - 'TimeoutExpired'")

        # these should not be necessary, the device should transition from 'offline' to 'device'
        # Extra effort because this is a Timeout condition...
        disconnect_device(device_name, config)
        ping_device(device_name, config, max_pings=40)
        connect_device(device_name, config)

    # Now wait for ADB to re-establish with this device:
    wait_for_device_online(device_name, config)


def wait_for_device_online(device_name: str, config: dict, max_attempts=180, newly_online_sleep=30):
    #
    # Wait for ADB to report the device as 'device' (online/connected).
    #   Typically ADB reports the device 'offline' when the device
    #   fails to report a heartbeat/response for 3 seconds.
    #
    ts_print(f"{device_name}: wait_for_device_online...")

    _udid = device_udid(device_name, config)
    cmd_devices = "adb devices -l"
    for attempt in range(1, max_attempts + 1):
        # print(f"Attempt {attempt}...")
        try:
            _result = subprocess.run(cmd_devices, stdout=PIPE, text=True, check=True, shell=True)
        except CalledProcessError:
            print_exception(f"'{cmd_devices}' result", device_name)
            raise
        _lines = _result.stdout.splitlines(keepends=False)
        for _line in _lines:
            _words = _line.split()
            if _udid in _words:
                if _words[1] == "device":
                    ts_print(f"{device_name}: online with '{_line.strip()}'")
                    ts_print(f"{device_name}: online after {attempt} of {max_attempts} checks")
                    if attempt > 1:
                        ts_print(f"{device_name}: newly online, sleeping an extra {newly_online_sleep} seconds.")
                        time.sleep(newly_online_sleep)
                    return
                if _words[1] != "offline":
                    ts_print(f"WARNING: {device_name}: Unexpected device state is '{_words[1]}', ignored.")
        time.sleep(1)
    raise AssertionError(f"{device_name}: NOT ONLINE after {max_attempts} attempts.")


def is_app_installed(device_name, config: dict, app_name):
    _udid = device_udid(device_name, config)

    # Note: the following gets all packages, we could limit to just *microsoft* packages with:
    # "shell pm list packages microsoft":
    cmd_get_installed_packages = "adb -s " + str(_udid) + " shell pm list packages"
    _installed_packages = subprocess.check_output(cmd_get_installed_packages, text=True, timeout=10, shell=True)
    return app_name in _installed_packages


def uninstall_app(device_name: str, config: dict, app_name: str):
    """
    Unconditionally attempt to uninstall the indicated app_name
    """
    _udid = device_udid(device_name, config)
    _max_uninstall_time = float(1 * 60)
    cmd_uninstall = f"adb -s {_udid} uninstall {app_name}"
    # ts_print(f"{device_name}: Uninstalling with: '{cmd_uninstall}'")
    try:
        _uninstall_result = subprocess.run(
            cmd_uninstall,
            text=True,
            stdout=subprocess.PIPE,
            check=True,
            timeout=_max_uninstall_time,
        )
        _result = _uninstall_result.stdout.strip()
        if "fail" in _result.lower():
            # Note - ignored: Uninstall result: Failure [DELETE_FAILED_DEVICE_POLICY_MANAGER]
            ts_print(f"{device_name}: WARN: Ignoring failure: Uninstall result: {_result}")
        else:
            ts_print(f"{device_name}: Uninstall result: {_result}")
        return True
    except TimeoutExpired:
        ts_print(f"{device_name}: WARN: Uninstall result: TimeoutExpired ignored (after {_max_uninstall_time} secs).")
        return True
    except:
        print_exception("ERROR: Uninstall failed", device_name)
    return False


def clear_app_cache(device_name: str, config: dict, app_name: str):
    """
    Clear device app cache for the specified app_name
    """
    _udid = device_udid(device_name, config)

    _max_clear_wait = float(15)
    cmd_clear = f"adb -s {_udid} shell pm clear {app_name}"
    # ts_print(f"{device_name}: Clearing cache for {app_name} with: '{cmd_clear}'")
    try:
        _clear_result = subprocess.run(
            cmd_clear,
            text=True,
            stdout=PIPE, 
            stderr=PIPE,
            check=True,
            shell=True,
            timeout=_max_clear_wait,
        )
        _result = _clear_result.stdout.strip()
        ts_print(f"{device_name}: Clear '{app_name}' result: {_result}")
    except TimeoutExpired:
        ts_print(
            f"{device_name}: WARN: Clear '{app_name}' result: TimeoutExpired ignored (after {_max_clear_wait} secs)."
        )


def storage_percent_in_use(device_name, config: dict):
    # Return the percentage of storage-in-use on the device (0-100).
    # Return None if not rooted or unparsible.
    _udid = device_udid(device_name, config)
    cmd_storage_request = "adb -s " + str(_udid) + " shell df /sdcard"
    storage_response = subprocess.check_output(cmd_storage_request, text=True)

    # Expecting:
    # 'Filesystem     1K-blocks   Used Available Use% Mounted on'
    # '/dev/fuse        3094448 562196   2532252  19% /storage/emulated'
    #
    if not "Mounted" in storage_response:
        ts_print(
            f"{device_name}: Cannot fetch storage information - root verification failed with '{storage_response.strip()}'."
        )
        return None

    _lines = storage_response.splitlines()
    if len(_lines) < 2:
        ts_print(f"{device_name}: Cannot fetch storage information - unknown format: {_lines}.")
        return None

    _fields = _lines[1].split()
    if len(_fields) < 5:
        ts_print(f"{device_name}: Cannot fetch storage information - insufficient fields: {_fields}.")
        return None

    # Just FYI: available blocks
    try:
        _available_blocks = int(_fields[3])
        ts_print(f"{device_name}: INFO: {_available_blocks} 1k-blocks available.")
    except:
        ts_print(f"{device_name}: Cannot fetch 'blocks available' - was reported as: {_fields[3]}.")

    try:
        _in_use = int(_fields[4][0:-1])
        ts_print(f"{device_name}: INFO: Storage {_in_use}% in-use ({100-_in_use}% available).")
        return _in_use
    except:
        ts_print(f"{device_name}: Cannot fetch 'percent in use' - was reported as: {_fields[4]}.")

    return None


def install_with_retry(
    device_name: str,
    config: dict,
    app_name: str,
    apk_file: str,
    replace_ok: bool = False,
    attempts: int = 3,
):
    _udid = device_udid(device_name, config)

    ts_print(f"{device_name}: Installing app '{app_name}' from APK file: {apk_file}")
    _max_install_time = float(10 * 60)

    _install_flags = "-r -d" if replace_ok else "-g -d"

    for attempt in range(attempts):
        ts_print(f"{device_name}: Install attempt: {attempt+1} of {attempts}")
        _ready_for_install = False

        if is_app_installed(device_name, config, app_name):
            ts_print(f"{device_name}: App is installed: {app_name}")
            if replace_ok:
                ts_print(f"{device_name}: App will be replaced.")
                _ready_for_install = True
            else:
                _ready_for_install = uninstall_app(device_name, config, app_name)
        else:
            ts_print(f"{device_name}: App not installed: {app_name}")
            _ready_for_install = True

        if _ready_for_install:
            cmd_install = f"adb -s {_udid} install {_install_flags} {apk_file}"
            ts_print(f"{device_name}: Installing with: '{cmd_install}'")
            try:
                _install_result = subprocess.run(
                    cmd_install,
                    text=True,
                    stdout=subprocess.PIPE,
                    check=True,
                    timeout=_max_install_time,
                )
                ts_print(f"{device_name}: Install result: {_install_result.stdout.strip()}")
                return True
            except TimeoutExpired:
                ts_print(f"{device_name}: ERROR: Install result: TimeoutExpired(after {_max_install_time} secs).")
            except:
                print_exception("ERROR: Install failed", device_name)
        if attempt == attempts - 1:
            # final failure, no more retries:
            break
        #
        # Issue: Here, the install failed - Have seen ADB report the device 'offline'
        #
        wait_for_device_online(device_name, config)

        if replace_ok:
            ts_print(f"{device_name}: Next attempt will force uninstall")
            replace_ok = False
        reboot_device(device_name, config)

    ts_print(f"{device_name}: FATAL: Install failed")
    return False


def clear_app_caches(device_name: str, config: dict, apps: list):
    for _app_name in apps:
        if is_app_installed(device_name, config, _app_name):
            try:
                clear_app_cache(device_name, config, _app_name)
            except Exception as e:
                ts_print(f"{device_name}: Clear '{_app_name}' cache FAILED: {type(e).__name__}: {e}")
                raise
        else:
            ts_print(f"{device_name}: Clear cache skipped, app is not installed: {_app_name}")
    _sleep_post_clear_caches = 30
    ts_print(f"{device_name}: Caches cleared, sleeping an additional : {_sleep_post_clear_caches}")
    time.sleep(_sleep_post_clear_caches)


def device_udid(device_name: str, config: dict):
    if "console" in device_name:
        devices = "consoles"
    else:
        devices = "devices"
    return config[devices][device_name]["desired_caps"]["udid"]


def get_device_property(device_name: str, config: dict, prop_name: str):
    _udid = device_udid(device_name, config)
    cmd_getprop = "adb -s " + str(_udid) + " shell getprop " + prop_name
    _result = subprocess.run(
        cmd_getprop,
        text=True,
        stdout=PIPE ,
        check=True,
        timeout=5.0,
    )
    return _result.stdout.strip()


def print_device_info(device_name: str, config: dict):
    # _device = get_device_property(device_name, "ro.product.device")
    _manufacturer = get_device_property(device_name, config, "ro.product.manufacturer")
    _model = get_device_property(device_name, config, "ro.product.model")
    _build = get_device_property(device_name, config, "ro.build.id")
    _version_firmware = get_device_property(device_name, config, "persist.product.version")
    _version_hardware = get_device_property(device_name, config, "hwversion")
    _mac = get_device_property(device_name, config, "persist.net.wifi.wlan_mac")
    if _mac == "":
        # device dependency, try model "riverside" location
        _mac = get_device_property(device_name, config, "persist.net.bt.mac")

    ts_print(f"{device_name}: INFO: device is {_manufacturer}, {_model}, Build Id: {_build}.")
    ts_print(f"{device_name}: INFO: Firmware version:'{_version_firmware}', Build Id: {_build}.")
    ts_print(f"{device_name}: INFO: Hardware version: '{_version_hardware}', MAC: {_mac}.")

    _config_oem = config["devices"][device_name]["oem"]
    _config_model = config["devices"][device_name]["model"]
    _config_port = config["devices"][device_name]["port"]
    ts_print(
        f"{device_name}: INFO: device is configured for port '{_config_port}' and as oem='{_config_oem}', model='{_config_model}'."
    )


####
#    Playground/standalone tests - go crazy...
####
if __name__ == "__main__":
    ############################################################
    # Adjust PYTHONPATH to allow imports relative to this file
    import os
    import sys

    ABS_DOT_DOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if ABS_DOT_DOT_DIR not in sys.path:
        sys.path.append(os.path.join(ABS_DOT_DOT_DIR))
    #
    ############################################################

    ############################################################
    # Load the configuration
    from configure_devices import load_json_file

    try:
        # Note: Using default/real configuration - "../config.json"
        cfg = load_json_file(ABS_DOT_DOT_DIR + "/config.json")
    except:
        print_exception("While loading config.json")
        exit(1)
    #
    ############################################################

    def some_test(a_config: dict):
        # Examples:
        #   print_device_info("device_1", a_config)
        #   wait_for_device_online("device_1", a_config)
        #   reboot_device("device_2", a_config)
        # And something harmless:
        ts_print("This is an example of a 'ts_print' timestamped message.")

    some_test(cfg)
