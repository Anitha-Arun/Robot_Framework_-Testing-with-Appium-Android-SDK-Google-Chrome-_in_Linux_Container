import time
import common
import subprocess
from initiate_driver import config
from robot.libraries.BuiltIn import BuiltIn
import os
from io import open
from Libraries.Selectors import load_json_file
from initiate_driver import obj_dev as obj

calls_dict = load_json_file("resources/Page_objects/Calls.json")
signin_dict = load_json_file("resources/Page_objects/Signin.json")


def logcat_capture_for_perf_analysis(device, name, iteration=1):
    time.sleep(20)
    name = (
        name.replace(" ", "_")
        .replace(":", "-")
        .replace("/", "_")
        .replace('"', "")
        .replace(".", "")
        .replace("'", "")
        .replace(",", "")
    )
    newpath = BuiltIn().get_variable_value("${OUTPUT DIR}") + "\\logcat_logs_for_perf_analysis\\"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    _udid = config["devices"][device]["desired_caps"]["udid"]
    driver = obj.device_store.get(alias=device)
    logs = driver.get_log("logcat")
    log_messages = list(map(lambda log: log["message"], logs))
    # cmd = "adb -s " + _udid + " logcat -d"
    with open(newpath + name + "iteration" + str(iteration) + ".txt", "w", encoding="utf-8") as w1:
        # subprocess.run(cmd, stdout=w1, shell=True)
        for item in log_messages:
            item = item.encode().decode()
            w1.write("{}\n".format(item))
    time.sleep(20)


def reset_logs_capture(devices):
    device_list = devices.split(",")
    for device in device_list:
        # _udid = config["devices"][device]["desired_caps"]["udid"]
        # cmd = "adb -s " + _udid + " logcat -c"
        # subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
        driver = obj.device_store.get(alias=device)
        logs_previous = driver.get_log("logcat")
        time.sleep(10)


def pass_the_automation_flag(device):
    _udid = config["devices"][device]["desired_caps"]["udid"]
    if config["devices"][device]["model"].lower() in ["bakersfield", "riverside", "santa cruz"]:
        cmd = (
            "adb -s "
            + _udid
            + " shell am start com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.SplashActivity --esn automation"
        )
    else:
        cmd = (
            "adb -s "
            + _udid
            + " shell am start -n  com.microsoft.skype.teams.ipphone/com.microsoft.skype.teams.views.activities.SplashActivity --esn automation"
        )
    subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
    time.sleep(10)


def navigate_to_contact_search_tab(device):
    common.wait_for_and_click(device, calls_dict, "search")
    common.sleep_with_msg(device, 5, "Wait until search tab loads")
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")


def wait_and_click_refresh_code_button(device):
    common.wait_for_and_click(device, signin_dict, "refresh_code_button", wait_attempts=600)
    common.wait_for_element(device, signin_dict, "dfc_login_code")
