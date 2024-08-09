import call_keywords
from Libraries.Selectors import load_json_file
import common
import tr_console_call_keywords
from initiate_driver import config
import subprocess
import time
from initiate_driver import obj_dev as obj
import tr_console_settings_keywords

display_time = 2
action_time = 3

tr_console_home_screen_dict = load_json_file("resources/Page_objects/rooms_console_home_screen.json")
tr_home_screen_dict = load_json_file("resources/Page_objects/tr_home_screen.json")
tr_console_signin_dict = load_json_file("resources/Page_objects/rooms_console_signin.json")
tr_settings_dict = load_json_file("resources/Page_objects/tr_settings.json")
tr_console_settings_dict = load_json_file("resources/Page_objects/rooms_console_settings.json")
calls_dict = load_json_file("resources/Page_objects/Calls.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")
tr_calendar_dict = load_json_file("resources/Page_objects/tr_calendar.json")
common_dict = load_json_file("resources/Page_objects/common.json")
tr_calls_dict = load_json_file("resources/Page_objects/tr_calls.json")


def validate_user_details_along_with_home_screen_options(console):
    consoles = console.split(",")
    for console in consoles:
        print("Console: ", console)
        account = "user"
        if ":" in console:
            user = console.split(":")[1]
            print("User account : ", user)
            if user.lower() == "meeting_user":
                account = "meeting_user"
        print("account : ", account)
        console = console.split(":")[0]
        username = config["consoles"][console][account]["displayname"]
        phonenumber = config["consoles"][console][account]["pstndisplay"]
        print(" console : ", console)
        elem1 = common.wait_for_element(console, tr_console_home_screen_dict, "room_user_name").text
        if elem1 != username:
            raise AssertionError(f"user name {username} is not matched with {elem1} ")
        print("User name is visible on the home screen : ", elem1)
        elem2 = common.wait_for_element(console, tr_console_home_screen_dict, "phone_number").text
        if elem2 != phonenumber:
            raise AssertionError(f"user number  {phonenumber} is not matched with {elem2} ")
        print("Phone number is visible on the home screen : ", elem2)
        common.wait_for_element(console, tr_console_home_screen_dict, "meet_now_icon")
        common.wait_for_element(console, tr_console_home_screen_dict, "call_icon")
        common.wait_for_element(console, tr_console_home_screen_dict, "more_option")


def come_back_to_home_screen_page(console_list, device_list=None, disconnect=True):
    consoles = console_list.split(",")
    for console in consoles:
        print("consoles :", console)
        if disconnect:
            tr_console_call_keywords.check_the_call_state_and_disconnect(console)
        common.wait_for_element(console, tr_console_home_screen_dict, "more_option")
        common.wait_for_element(console, tr_console_home_screen_dict, "room_user_name")
    if device_list is not None:
        call_keywords.come_back_to_home_screen(device_list)


def verify_meet_now_present_on_home_screen(console):
    common.wait_for_element(console, tr_console_home_screen_dict, "meet_now_icon")


def verify_time_display_on_home_screen(console):
    common.wait_for_element(console, tr_home_screen_dict, "clock")


def verify_home_screen_options(console):
    common.wait_for_element(console, tr_console_home_screen_dict, "meet_now_icon")
    common.wait_for_element(console, tr_console_home_screen_dict, "call_icon")
    common.wait_for_element(console, tr_console_home_screen_dict, "more_option")


def verify_dpi_set_on_device(console):
    print("Check for dp set on :", console)
    udid_ = config["consoles"][console]["desired_caps"]["udid"]
    print(udid_)
    pd = subprocess.check_output("adb -s " + udid_ + " shell wm density", shell=True)
    out_put = pd.splitlines()[0].rsplit()[-1].strip()
    result = int(out_put.decode("utf-8"))
    print(result)
    exp_physical_density = config["console_physical_density"]
    if result != exp_physical_density:
        raise AssertionError(f"DPI value set on device {result}is not matched with {exp_physical_density}")


def check_app_supported_UI(console):
    print("Check supported UI for :", console)
    udid_ = config["consoles"][console]["desired_caps"]["udid"]
    print(udid_)
    py_size = subprocess.check_output("adb -s " + udid_ + " shell wm size", shell=True)
    out_put = py_size.splitlines()[0].rsplit()[-1].strip()
    result = str(out_put, "utf-8")
    print(result)
    expected_val = config["console_physical_size"]
    if result != expected_val:
        raise AssertionError(f"Supported Physical UI size {expected_val} is not matched {result}")


def verify_available_options_in_more(console):
    common.wait_for_and_click(console, tr_console_home_screen_dict, "more_option")
    common.wait_for_element(console, tr_console_home_screen_dict, "meet_now_icon")
    common.wait_for_element(console, tr_console_home_screen_dict, "call_icon")
    common.wait_for_element(console, tr_console_home_screen_dict, "feedback_btn")
    common.wait_for_element(console, tr_settings_dict, "settings_button")


def verify_did_user_displayed_on_homescreen_and_on_dialpad(console):
    account = "user"
    if ":" in console:
        account = console.split(":")[1]
        console = console.split(":")[0]
    phone_number = common.wait_for_element(console, tr_console_home_screen_dict, "phone_number").text
    user_number = config["consoles"][console][account]["pstndisplay"]
    if phone_number != user_number:
        raise AssertionError(f"Phone number {phone_number}displayed is not as expected on homescreen: {user_number}")
    common.wait_for_and_click(console, tr_console_home_screen_dict, "call_icon")
    driver = obj.device_store.get(alias=console)
    driver.execute_script("mobile: performEditorAction", {"action": "done"})
    ph_no_dialpad = common.wait_for_element(console, tr_home_screen_dict, "user_phone_number").text
    expected_text = "Your number is: " + config["consoles"][console][account]["pstndisplay"]
    if ph_no_dialpad != expected_text:
        raise AssertionError(f"Phone number {ph_no_dialpad} displayed is not as expected on dialpad: {expected_text}")
    common.wait_for_and_click(console, tr_console_settings_dict, "back_layout")
    common.wait_for_element(console, tr_console_home_screen_dict, "call_icon")


def click_dialpad(console):
    common.wait_for_and_click(console, tr_console_home_screen_dict, "call_icon")
    common.hide_keyboard(console)
    common.wait_for_element(console, calls_dict, "dial_pad_field")


def auto_dial_emergency_num(console):
    click_dialpad(console)
    subprocess.call(
        "adb -s {} shell input keyevent 16".format(config["consoles"][console]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    subprocess.call(
        "adb -s {} shell input keyevent 10".format(config["consoles"][console]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    subprocess.call(
        "adb -s {} shell input keyevent 10".format(config["consoles"][console]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    time.sleep(display_time)
    if common.is_element_present(console, calls_dict, "emergency_call_icon"):
        raise AssertionError(f"user is able to auto dial the emergency number")
    common.wait_for_and_click(console, tr_console_settings_dict, "back_layout")


def check_dial_pad_on_landing_page(console):
    common.wait_for_element(console, tr_console_home_screen_dict, "call_icon")


def verify_date_and_time_with_user_details_on_home_screen(console):
    phonenumber = common.device_pstndisplay(console)
    username = common.device_displayname(console)
    console = console.split(":")[0] if ":" in console else console
    print(" console : ", console)
    print("Username and phone number : ", username, phonenumber)
    elem1 = common.wait_for_element(console, tr_console_home_screen_dict, "room_user_name").text
    if elem1 != username:
        raise AssertionError(f"user name {username} is not matched with {elem1} ")
    print("User name is visible on the home screen : ", elem1)
    elem2 = common.wait_for_element(console, tr_console_home_screen_dict, "phone_number").text
    if elem2 != phonenumber:
        raise AssertionError(f"user number  {phonenumber} is not matched with {elem2} ")
    print("Phone number is visible on the home screen : ", elem2)
    common.wait_for_element(console, tr_home_screen_dict, "day_month_date")
    common.wait_for_element(console, tr_home_screen_dict, "clock")
    common.wait_for_element(console, tr_home_screen_dict, "ring_indicator")
    common.wait_for_element(console, tr_home_screen_dict, "add_this_room_label")
    common.wait_for_element(console, settings_dict, "Help")


def verify_user_options_on_home_screen(console):
    common.wait_for_element(console, tr_console_home_screen_dict, "meet_now_icon")
    common.wait_for_element(console, tr_console_home_screen_dict, "call_icon")
    common.wait_for_element(console, tr_console_home_screen_dict, "more_option")
    common.wait_for_element(console, tr_home_screen_dict, "share_button")
    common.wait_for_element(console, tr_calls_dict, "Whiteboard")
    common.wait_for_element(console, tr_calendar_dict, "join_with_an_id")


def verify_the_help_button_functionality(device):
    common.wait_for_and_click(device, settings_dict, "Help")
    common.wait_for_element(device, tr_home_screen_dict, "give_feedback")
    common.wait_for_and_click(device, tr_home_screen_dict, "report_problem")
    common.wait_for_element(device, tr_home_screen_dict, "report_problem")
    common.wait_for_element(device, settings_dict, "send_bug")
    common.wait_for_and_click(device, common_dict, "back")


def verify_help_option_when_whiteboard_initiated_from_home_screen(console):
    common.wait_for_element(console, tr_console_home_screen_dict, "more_option")
    common.wait_for_and_click(console, tr_calls_dict, "Whiteboard")
    common.wait_for_element(console, tr_calendar_dict, "Microsoft_whiteboard_sharing")
    common.wait_for_element(console, tr_home_screen_dict, "whiteboard_meeting_btn")
    common.wait_for_element(console, settings_dict, "Help")
    common.wait_for_and_click(console, tr_calendar_dict, "stop_whiteboard_sharing")
    common.wait_for_and_click(console, tr_calendar_dict, "stop_whiteboard_sharing")
    common.wait_for_element(console, tr_console_home_screen_dict, "meet_now_icon")
    common.wait_for_element(console, tr_console_home_screen_dict, "more_option")


def verify_help_option_present_under_the_call_option(device):
    common.wait_for_element(device, tr_console_home_screen_dict, "more_option")
    time.sleep(3)
    if not common.click_if_present(device, tr_calls_dict, "dial_pad"):
        common.wait_for_and_click(device, tr_console_home_screen_dict, "call_icon")
    common.sleep_with_msg(device, 5, "wait until to load calling page")
    driver = obj.device_store.get(alias=device)
    driver.execute_script("mobile: performEditorAction", {"action": "done"})
    common.wait_for_and_click(device, settings_dict, "Help")
    common.wait_for_element(device, tr_home_screen_dict, "give_feedback")
    common.wait_for_element(device, tr_home_screen_dict, "report_problem")
    call_keywords.dismiss_the_popup_screen(device)
    common.wait_for_and_click(device, tr_console_settings_dict, "back_layout")
    time.sleep(5)
    if not common.is_element_present(device, tr_calls_dict, "dial_pad"):
        common.wait_for_element(device, tr_console_home_screen_dict, "call_icon")


def verify_dial_pad_on_homescreen(console):
    common.wait_for_and_click(console, tr_console_home_screen_dict, "call_icon")
    common.wait_for_element(console, calls_dict, "dial_pad_field")
    driver = obj.device_store.get(alias=console)
    driver.execute_script("mobile: performEditorAction", {"action": "done"})
    common.wait_for_element(console, tr_home_screen_dict, "user_phone_number")
    common.wait_for_and_click(console, tr_console_settings_dict, "back_layout")
    common.wait_for_element(console, tr_console_home_screen_dict, "call_icon")
