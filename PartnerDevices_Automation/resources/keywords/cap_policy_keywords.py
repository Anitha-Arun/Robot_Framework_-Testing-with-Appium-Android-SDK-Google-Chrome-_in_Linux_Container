from appium.webdriver.common.mobileby import MobileBy
from device_settings_keywords import swipe_the_page_till_signout
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Selectors import load_json_file
from initiate_driver import obj_dev as obj
from initiate_driver import config
import common
import time
import call_keywords
import settings_keywords
import home_screen_keywords
import calendar_keywords
import device_settings_keywords

display_time = 2
action_time = 5

sign_dict = load_json_file("resources/Page_objects/Signin.json")
calendar_dict = load_json_file("resources/Page_objects/Calendar.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")
navigation_dict = load_json_file("resources/Page_objects/Navigation.json")
device_settings_dict = load_json_file("resources/Page_objects/Device_settings.json")
calls_dict = load_json_file("resources/Page_objects/Calls.json")
people_dict = load_json_file("resources/Page_objects/People.json")
call_view_dict = load_json_file("resources/Page_objects/Call_views.json")
home_screen_dict = load_json_file("resources/Page_objects/Home_screen.json")


def verify_search_option_is_disabled(device):
    if common.is_element_present(device, calls_dict, "search"):
        raise AssertionError("Search option is present")
    else:
        print("Search option is disabled for CAP user")


def verify_phonelock_option_is_not_present(device):
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["phone_lock"]["xpath"]))
        ).click()
    except Exception as e:
        print("Phone Lock option is not present for CAP user", e)
    else:
        raise AssertionError("Phone Lock option is present")
    pass


def search_for_tdc_user(from_device, to_device):
    time.sleep(display_time)
    time.sleep(action_time)
    home_screen_keywords.navigate_to_people_tab_from_home_screen_for_cap(from_device)
    common.wait_for_and_click(from_device, calls_dict, "search")
    displayname = common.device_displayname(to_device)
    print("displayname : ", displayname)
    element = common.wait_for_element(from_device, calls_dict, "search_text")
    element.send_keys(displayname)
    common.hide_keyboard(from_device)
    time.sleep(display_time)
    tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", displayname)
    common.wait_for_and_click(from_device, tmp_dict, "search_result_item_container", "xpath")
    time.sleep(display_time)
    print("Teams app user is able to search for the TDC user")


def verify_signout_option_should_be_in_device_settings(device_list):
    devices = device_list.split(",")
    print("Devices : ", devices)
    for device in devices:
        print("device : ", device)
        driver = obj.device_store.get(alias=device_list)
        common.wait_for_and_click(device, settings_dict, "Device_Settings")
        if config["devices"][device]["model"].lower() == "manhattan":
            common.wait_for_and_click(device, settings_dict, "Admin_Settings")
            element1 = common.wait_for_element(device, settings_dict, "admin_passwd")
            element1.set_value(config["devices"][device]["admin_password"])
            driver.execute_script("mobile: performEditorAction", {"action": "done"})
            common.wait_for_and_click(device, settings_dict, "Login_btn")
            print(f"{device} Clicked on login button")
            common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings")
            common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings_btn")
            common.wait_for_element(device, settings_dict, "Sign_out")
        elif config["devices"][device]["model"].lower() in ["tacoma", "olympia"]:
            common.wait_for_and_click(device, settings_dict, "Admin_Only")
            common.wait_for_and_click(device, settings_dict, "admin_passwd", "xpath")
            common.wait_for_element(device, settings_dict, "admin_passwd", "xpath").set_value(
                config["devices"][device]["admin_password"]
            )
            driver.execute_script("mobile: performEditorAction", {"action": "done"})
            swipe_the_page_till_signout(device)
            common.wait_for_element(device, settings_dict, "Account_Signout", "xpath1")
    call_keywords.come_back_to_home_screen(device_list)
    pass


def verify_contact_page_details(device):
    print("device:", device)
    common.wait_for_element(device, people_dict, "user_profile_picture")
    common.wait_for_element(device, people_dict, "user_name")
    if common.is_element_present(device, calls_dict, "user_designation_title"):
        print("User Designation is available : ")
    else:
        print("Designation is not available for this user")
    common.wait_for_element(device, people_dict, "make_an_audio_call")
    common.wait_for_element(device, people_dict, "email")
    time.sleep(display_time)
    settings_keywords.click_back(device)


def verify_call_views_option_under_calling_settings_for_CAP_policy_user_for_audio_phones(device):
    device_settings_keywords.navigate_to_calling_option_for_CAP_policy_user_for_audio_phones(device)
    calendar_keywords.scroll_only_once(device)
    if common.is_element_present(device, call_view_dict, "call_view") or common.is_element_present(
        device, call_view_dict, "default_view"
    ):
        raise AssertionError(f"{device} : is Having Default view under calling settings for CAP Policy User")


def verify_missed_call_notification_for_cap_user(device):
    # Check missed call pill anywhere on screen
    common.wait_while_present(device, calls_dict, "missed_calls_count", max_wait_attempts=3)
    # check missed call notification banner on screen
    common.wait_while_present(device, home_screen_dict, "miss_call_notification")
