from appium.webdriver.common.mobileby import MobileBy
from initiate_driver import obj_dev as obj
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from initiate_driver import config
from Libraries.Selectors import load_json_file
import common
import time
import subprocess
import tr_call_keywords
import tr_settings_keywords


display_time = 2
action_time = 3

calls_dict = load_json_file("resources/Page_objects/Calls.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")
tr_settings_dict = load_json_file("resources/Page_objects/tr_settings.json")
tr_device_settings_dict = load_json_file("resources/Page_objects/tr_device_settings.json")
tr_console_settings_dict = load_json_file("resources/Page_objects/rooms_console_settings.json")
tr_console_signin_dict = load_json_file("resources/Page_objects/rooms_console_signin.json")
sign_dict = load_json_file("resources/Page_objects/Signin.json")
tr_calendar_dict = load_json_file("resources/Page_objects/tr_calendar.json")


def tap_on_settings_page(console):
    print("Console :", console)
    common.wait_for_and_click(console, tr_settings_dict, "settings_button")
    common.wait_for_element(console, settings_dict, "Device_Settings")


def click_on_close_button(console_list):
    consoles = console_list.split(",")
    for console in consoles:
        print("Console :", console)
        time.sleep(3)
        if not common.click_if_present(console, tr_console_settings_dict, "back_layout"):
            common.wait_for_and_click(console, tr_console_settings_dict, "back_button")


def click_on_back_layout_btn(console):
    consoles = console.split(",")
    for console in consoles:
        print("Console :", console)
        common.wait_for_and_click(console, tr_console_settings_dict, "back_layout")


def tap_on_device_center_point(console):
    consoles = console.split(",")
    for console in consoles:
        time.sleep(action_time)
        driver = obj.device_store.get(alias=console)
        window_size = driver.get_window_size()
        height = window_size["height"]
        width = window_size["width"]
        subprocess.call(
            "adb -s {} shell input tap {} {}".format(
                config["consoles"][console]["desired_caps"]["udid"].split(":")[0],
                width / 2,
                height / 2,
            ),
            shell=True,
        )
        time.sleep(display_time)
        print("Tapped co-ordinates : ", width / 2, height / 2)


def verify_options_inside_settings_page(console):
    print("device : ", console)
    account = "user"
    if ":" in console:
        user = console.split(":")[1]
        console = console.split(":")[0]
        print("User account : ", user)
        if user.lower() == "meeting_user":
            account = "meeting_user"
    print("Account :", account)
    if account == "meeting_user":
        # according to the new UI from report an issue is removed from the about page
        # common.wait_for_element(console, tr_settings_dict, "Report_an_issue")
        common.wait_for_element(console, tr_settings_dict, "about")
        # common.wait_for_element(console, tr_settings_dict, "device_health")
        common.wait_for_element(console, tr_device_settings_dict, "device_settings")
    else:
        common.wait_for_element(console, tr_settings_dict, "meetings_button")
        common.wait_for_element(console, tr_settings_dict, "calling_button")
        common.wait_for_element(console, tr_settings_dict, "wallpapers_button")
        common.wait_for_element(console, tr_settings_dict, "Report_an_issue")
        common.wait_for_element(console, tr_settings_dict, "about")
        common.wait_for_element(console, tr_settings_dict, "device_health")
        common.wait_for_element(console, settings_dict, "Sign_out")
        common.wait_for_element(console, tr_device_settings_dict, "device_settings")


def device_setting_back_btn(console):
    print("console :", console)
    subprocess.call(
        "adb -s {} shell input keyevent 4".format(config["consoles"][console]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    pass


def tap_on_device_settings_page(console):
    print("console :", console)
    common.wait_for_and_click(console, tr_device_settings_dict, "device_settings")
    common.wait_for_element(console, settings_dict, "Device_Settings")


def tap_on_device_right_corner(console):
    consoles = console.split(",")
    for console in consoles:
        time.sleep(action_time)
        driver = obj.device_store.get(alias=console)
        window_size = driver.get_window_size()
        height = window_size["height"]
        width = window_size["width"]
        subprocess.call(
            "adb -s {} shell input tap {} {}".format(
                config["consoles"][console]["desired_caps"]["udid"].split(":")[0], width - 20, 20
            ),
            shell=True,
        )
        time.sleep(display_time)
        print("Tapped co-ordinates : ", width - 20, 20)


def user_checks_device_type(console):
    print("Check device type on :", console)
    udid_ = config["consoles"][console]["desired_caps"]["udid"]
    print(udid_)
    dev_type = subprocess.check_output("adb -s " + udid_ + " shell settings get secure teams_device_type", shell=True)
    output = dev_type.splitlines()[0].rsplit()[-1].strip().lower()
    actual_val = str(output, "utf-8")
    print("Device Type is {} ".format(actual_val))
    expected_val = (config["console_type"]).strip().lower()
    if actual_val != expected_val:
        raise AssertionError(
            f"{console}: Actual device type: {actual_val} doesn't match expected value: {expected_val}"
        )


def verify_user_signing_with_wrong_password(console):
    username = config["consoles"][console]["user"]["username"]
    wrong_password = config["user"]["invalid_password"]
    if not common.is_element_present(console, sign_dict, "dfc_login_code"):
        common.wait_for_element(console, sign_dict, "refresh_code_button")
    common.wait_for_and_click(console, sign_dict, "sign_in_on_the_device")
    search_input = common.wait_for_element(console, sign_dict, "Username", "xpath")
    search_input.send_keys(username)
    print("Entered username")
    common.wait_for_and_click(console, sign_dict, "Sign_in_button")
    common.wait_for_element(console, sign_dict, "Password").send_keys(wrong_password)
    print(f"{console}: entered the wrong password")
    if not common.click_if_present(console, sign_dict, "Sign_in"):
        common.wait_for_and_click(console, sign_dict, "signin_button")
    common.wait_for_element(console, sign_dict, "invalid_password_error")


def verify_options_inside_calling(console):
    common.wait_for_element(console, tr_device_settings_dict, "voicemail")
    tr_call_keywords.swipe_till_end_page(console)
    common.wait_for_element(console, tr_device_settings_dict, "ringtones")
    tr_call_keywords.swipe_till_end_page(console)
    common.wait_for_element(console, tr_device_settings_dict, "block_calls")
    tap_on_device_right_corner(console)


def verify_console_pairing_option(console):
    common.wait_for_and_click(console, tr_device_settings_dict, "console_pairing")
    common.wait_for_element(console, tr_device_settings_dict, "reset_pairing")
    common.wait_for_element(console, tr_device_settings_dict, "unpair_devices")


def verify_inside_general_option(console):
    common.wait_for_element(console, tr_device_settings_dict, "front_of_room_display")
    common.wait_for_element(console, tr_device_settings_dict, "enable_touchscreen_controls")
    common.wait_for_element(console, tr_device_settings_dict, "wallpaper")


def modify_touchscreen_control_toggle_state(console, state):
    if not state.lower() in ["enabled", "disabled"]:
        raise AssertionError(f"Unexpected state:{state}")
    state = "on" if state.lower() == "enabled" else "off" if state.lower() == "disabled" else state
    common.change_toggle_button(console, tr_device_settings_dict, "enable_touchscreen_controls_toggle_ON", state)


def verify_intents_for_touchscreen_control(device, state):
    if not state.lower() in ["enabled", "disabled"]:
        raise AssertionError(f"Unexpected state:{state}")
    driver = obj.device_store.get(alias=device)
    time.sleep(5)
    logs_current = driver.get_log("logcat")
    # print ("Current log cat : \n", logs_current)
    filter = "SETTINGS_ENABLE_TOUCHSCREEN_CONTROLS"
    if state.lower() == "enabled":
        filter_mode = "true"
    elif state.lower() == "disabled":
        filter_mode = "false"
    res = []
    for i in logs_current:
        if filter in i["message"] and filter_mode in i["message"]:
            print("Intent : ", i)
            res.append(i)
    if len(res) == 0:
        raise AssertionError("Intent not found")
    else:
        print("Intent {} found in logcat".format(res))


def verify_meeting_chat_under_admin_settings(console):
    common.wait_for_element(console, tr_device_settings_dict, "show_meeting_chat")
    common.wait_for_element(console, tr_calendar_dict, "chat_toggle_in_device_setting")


def verify_enable_touchscreen_controls_with_toggle(console):
    common.wait_for_element(console, tr_device_settings_dict, "front_of_room_display")
    common.wait_for_element(console, tr_device_settings_dict, "enable_touchscreen_controls")
    common.wait_for_element(console, tr_device_settings_dict, "enable_if_room_has_touchscreen_display")
    common.wait_for_element(console, tr_device_settings_dict, "enable_touchscreen_controls_toggle_off")
