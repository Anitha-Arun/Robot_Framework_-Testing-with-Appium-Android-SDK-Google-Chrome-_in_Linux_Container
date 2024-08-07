from initiate_driver import obj_dev as obj
from initiate_driver import config
import time
import json

display_time = 5
action_time = 5

# print os.popen('echo %cd%').read()
calendar_dict = json.loads(open("resources/Page_objects/Calendar.json").read())
settings_dict = json.loads(open("resources/Page_objects/Settings.json").read())
navigation_dict = json.loads(open("resources/Page_objects/Navigation.json").read())
calls_dict = json.loads(open("resources/Page_objects/Calls.json").read())


def reset_logcat_capture(count):
    devices = []
    if count == 1:
        devices = ["device_1"]
    elif count == 2:
        devices = ["device_1", "device_2"]
    elif count == 3:
        devices = ["device_1", "device_2", "device_3"]
    # devices = device.split(',')
    for device in devices:
        driver = obj.device_store.get(alias=device)
        logs_previous = driver.get_log("logcat")
        # print "Previous logs : ", logs_previous
    if "consoles" in config:
        for console in list(config["consoles"].keys())[0 : int(count)]:
            driver = obj.device_store.get(alias=console)
            logs = driver.get_log("logcat")
        pass


def verify_intents(device, intent, user):
    driver = obj.device_store.get(alias=device)
    time.sleep(5)
    logs_current = driver.get_log("logcat")
    # print "Current log cat : \n", logs_current
    filter = "com.microsoft.skype.teams.ipphone.APP_USER_STATE"
    if user == "user":
        filter_user = "IS_CAP 0"
    elif user in ["meeting_user", "cap_search_enabled", "cap_user"]:
        filter_user = "IS_CAP 1"
    if intent == "sign_in":
        filter_mode = "SIGNED_IN 1"
    elif intent == "sign_out":
        filter_mode = "SIGNED_IN 0"
        filter_user = "IS_CAP 0"
    res = []
    for i in logs_current:
        if filter in i["message"] and filter_mode in i["message"]:
            print("Intent : ", i)
            assert filter_user in i["message"], "Intent Not found"
            res.append(i)
    if len(res) == 0:
        raise AssertionError("Intent not found")
    else:
        print("Intent {} found in logcat".format(res))
    pass


def stop_logcat_capture(device):
    devices = device.split(",")
    for device in devices:
        driver = obj.device_store.get(alias=device)
        logs_post = driver.get_log("logcat")
        print("Previous logs : ", logs_post)
    pass


def Verify_presence_of_Intents(device, feature, state):
    if not state.lower() in ["present", "absent"]:
        raise AssertionError(f"Unexpected state:{state}")
    driver = obj.device_store.get(alias=device)
    time.sleep(5)
    logs_current = driver.get_log("logcat")
    # print ("Current log cat : \n", logs_current)
    if feature == "panel_app_settings":
        filter = "com.microsoft.skype.teams.ipphone.partner.LAUNCH_PANEL_SETTINGS"
    elif feature == "admin_pass_change":
        new_admin_pass = config["devices"][device]["admin_new_password"]
        filter = new_admin_pass
    elif feature == "keycode":
        filter = "keycode"
    res = []
    for i in logs_current:
        if filter in i["message"]:
            print("Intent : ", i)
            res.append(i)
    if state.lower() == "present":
        if len(res) == 0:
            raise AssertionError("Intent not found")
        else:
            print("Intent {} found in logcat".format(res))
    elif state.lower() == "absent":
        if len(res) == 0:
            print("Intent is absent as per expected")
        else:
            raise AssertionError("Intent {} found in logcat".format(res))
