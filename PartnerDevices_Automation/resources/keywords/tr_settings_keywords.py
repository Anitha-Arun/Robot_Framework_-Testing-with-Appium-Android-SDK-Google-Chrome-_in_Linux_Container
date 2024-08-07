from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Selectors import load_json_file
from initiate_driver import obj_dev as obj
from initiate_driver import config
import subprocess
import time
import common
import call_keywords
import tr_call_keywords
import tr_console_settings_keywords
import app_bar_keywords


display_time = 2
action_time = 3
display_action_time = 10

tr_settings_dict = load_json_file("resources/Page_objects/tr_settings.json")
tr_device_settings_dict = load_json_file("resources/Page_objects/tr_device_settings.json")
tr_home_screen_dict = load_json_file("resources/Page_objects/tr_home_screen.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")
tr_calendar_dict = load_json_file("resources/Page_objects/tr_calendar.json")
tr_calls_dict = load_json_file("resources/Page_objects/tr_calls.json")
common_dict = load_json_file("resources/Page_objects/Common.json")
ztp_dict = load_json_file("resources/Page_objects/ztp.json")


def click_on_settings_page(device):
    print("device :", device)
    common.wait_for_and_click(device, tr_settings_dict, "settings_button")


def verify_dark_theme(device):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((MobileBy.ID, tr_home_screen_dict["more_button"]["id"]))
    ).click()
    try:
        click_on_settings_page(device)
        print("Dark theme reflected on screen")
    except Exception as e:
        print("Dark theme toggle option is not available on setting page")


def verify_about_page(device):
    print("device :", device)
    common.wait_for_and_click(device, tr_settings_dict, "about")
    common.wait_for_element(device, tr_settings_dict, "version")
    tr_call_keywords.swipe_till_end_page(device)
    tr_call_keywords.swipe_till_end_page(device)
    common.wait_for_element(device, tr_settings_dict, "copy_right")
    swipe_screen_page(device)
    swipe_screen_page(device)
    common.wait_for_element(device, tr_settings_dict, "term_of_use")
    common.wait_for_element(device, tr_settings_dict, "third_party_information")
    common.wait_for_element(device, tr_settings_dict, "privacy_cookies")
    app_bar_keywords.swipe_page_up(device)


def swipe_screen_page(device):
    driver = obj.device_store.get(alias=device)
    window_size = driver.get_window_size()
    print("Window size: ", window_size)
    height = window_size["height"]
    print("Window Height :", height)
    width = window_size["width"]
    print("Window Width :", width)
    if height > width:
        print("Swiping co-ordinates : ", width / 2, 4 * (height / 5), width / 2, height / 5)
        driver.swipe(width / 2, 4 * (height / 5), width / 2, height / 5)
    else:
        print("Swiping co-ordinates : ", width / 2, 3 * (height / 8), width / 2, height / 4)
        driver.swipe(width / 2, 3 * (height / 8), width / 2, height / 4)
    pass


def select_proximity_join_button(device_list, state):
    devices = device_list.split(",")
    # toggle button ON/OFF
    print("Devices : ", devices)
    for device in devices:
        print("device : ", device)
        driver = obj.device_store.get(alias=device)
        time.sleep(display_time)
        if state.lower() == "on":
            try:
                e1 = driver.find_elements_by_id(tr_settings_dict["proximity_toggle"]["id"])
                toggle = e1[1]
                if toggle.is_displayed():
                    toggle.click()
                    print("Proximity toggle button is in 'ON' state")
                else:
                    raise Exception("Failed to display Proximity toggle button on the screen")
            except Exception as e:
                raise AssertionError("Proximity toggle button is 'OFF' state", e)
        elif state.lower() == "off":
            try:
                e2 = driver.find_elements_by_id(tr_settings_dict["proximity_toggle"]["id"])
                toggle = e2[1]
                if toggle.is_displayed():
                    toggle.click()
                    print("Proximity toggle button is in 'OFF' state")
                else:
                    raise Exception("Failed to display Proximity toggle button on the screen")
            except Exception as e:
                raise AssertionError("Proximity toggle button is 'ON' state", e)


def press_long_tap_on_screen(device):
    devices = device.split(",")
    for device in devices:
        time.sleep(action_time)
        driver = obj.device_store.get(alias=device)
        window_size = driver.get_window_size()
        height = window_size["height"]
        print("Window Height :", height)
        width = window_size["width"]
        print("Window Width :", width)
        subprocess.call(
            "adb -s {} shell input touchscreen swipe {} {} {} {} {}".format(
                config["devices"][device]["desired_caps"]["udid"].split(":")[0],
                width / 2,
                height / 2,
                width / 2,
                height / 2,
                1000,
            ),
            shell=True,
        )
        time.sleep(display_time)
        print("Long Tapped co-ordinates : ", width / 2, height / 2, width / 2, height / 2)


def verify_option_inside_settings_page(device):
    print("device :", device)
    account = "user"
    if ":" in device:
        user = device.split(":")[1]
        print("User account : ", user)
        if user.lower() == "meeting_user":
            account = "meeting_user"
    print("Account :", account)
    device = device.split(":")[0]
    if account == "meeting_user":
        # common.wait_for_element(device, tr_settings_dict, "Report_an_issue")
        common.wait_for_element(device, tr_settings_dict, "about")
        # common.wait_for_element(device, tr_settings_dict, "device_health")
        common.wait_for_element(device, tr_device_settings_dict, "device_settings")
    else:
        common.wait_for_element(device, tr_settings_dict, "meetings_button")
        common.wait_for_element(device, tr_settings_dict, "calling_button")
        common.wait_for_element(device, tr_settings_dict, "wallpapers_button")
        # common.wait_for_element(device, tr_settings_dict, "Report_an_issue")
        common.wait_for_element(device, tr_settings_dict, "about")
        # common.wait_for_element(device, tr_settings_dict, "device_health")
        common.wait_for_element(device, settings_dict, "Sign_out")
        common.wait_for_element(device, tr_device_settings_dict, "device_settings")


def tap_on_meetings_page_and_validate_options(device):
    print("device : ", device)
    common.wait_for_and_click(device, tr_settings_dict, "meetings_button")
    common.wait_for_element(device, tr_calendar_dict, "show_meeting_names_text")
    common.wait_for_element(device, tr_calendar_dict, "allow_bluetooth_beaconing")
    common.wait_for_element(device, tr_calendar_dict, "proximity_btn")
    common.wait_for_element(device, tr_calendar_dict, "allow_remote_control_of_room_system_btn")


def tap_on_manage_devices_option_and_validate(device):
    print("device : ", device)
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((MobileBy.XPATH, tr_settings_dict["manage_devices"]["xpath"]))
        ).click()
        print("Manage devices is visible")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.XPATH, tr_settings_dict["connect_device_text"]["xpath"]))
        )
        print("Connect device text is visible on the screen")
        time.sleep(action_time)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.ID, tr_settings_dict["find_device_btn"]["id"]))
        )
        print("'Find device btn' is visible on screen along with '+' icon")
    except Exception as e:
        raise AssertionError("Xpath not found", e)


def hide_or_unhide_meeting_names(device, state):
    common.wait_for_element(device, tr_calendar_dict, "show_meeting_names_text")
    common.change_toggle_button(device, tr_calendar_dict, "meeting_names_toggle", state)
    common.wait_for_and_click(device, settings_dict, "cancel_btn")
    # WARN : Should not use ADB device back button, should always use UI back buttons
    # settings_keywords.device_setting_back(device)


def verify_whats_new_in_privacy_cookies(device):
    common.wait_for_element(device, tr_device_settings_dict, "about")
    swipe_screen_page(device)
    swipe_screen_page(device)
    common.wait_for_and_click(device, tr_device_settings_dict, "privacy_cookies")
    common.wait_for_element(device, tr_device_settings_dict, "Microsoft_Privacy_Statement")
    common.wait_for_and_click(device, tr_device_settings_dict, "whats_new?")
    common.wait_for_element(device, tr_device_settings_dict, "change_history")


def verify_that_unable_to_open_external_links_privacy_cookies(device):
    common.wait_for_element(device, tr_device_settings_dict, "change_history")
    common.click_if_present(device, tr_device_settings_dict, "privacy_dropdown")
    common.wait_for_and_click(device, tr_device_settings_dict, "privacy_dashboard")
    common.wait_for_element(device, tr_device_settings_dict, "unable_to_open_links")
    common.wait_for_and_click(device, tr_device_settings_dict, "ok")


def verify_terms_of_use_option(device):
    common.wait_for_element(device, tr_device_settings_dict, "about")
    tr_call_keywords.swipe_till_end_page(device)
    tr_call_keywords.swipe_till_end_page(device)
    common.wait_for_and_click(device, tr_device_settings_dict, "terms_of_use")
    common.wait_for_element(device, tr_device_settings_dict, "microsoft")


def verify_that_unable_to_open_external_links_in_terms_of_use(device):
    time.sleep(3)
    swipe_screen_page(device)
    common.wait_for_and_click(device, tr_settings_dict, "facebook")
    common.wait_for_element(device, tr_device_settings_dict, "unable_to_open_links")
    common.wait_for_and_click(device, tr_device_settings_dict, "ok")
    if not common.click_if_present(device, tr_calls_dict, "close_roaster_button"):
        common.wait_for_and_click(device, common_dict, "back")


def verify_about_page_and_connected_experiences_is_not_present_in_about_page(device):
    tr_call_keywords.swipe_till_end_page(device)
    tr_call_keywords.swipe_till_end_page(device)
    time.sleep(action_time)
    if common.is_element_present(device, tr_device_settings_dict, "Connected_Experiences"):
        raise AssertionError(f"{device}:  Connect Experience is present in about page")
    swipe_screen_page(device)
    common.wait_for_element(device, tr_device_settings_dict, "privacy_cookies")
    common.wait_for_element(device, tr_device_settings_dict, "terms_of_use")
    common.wait_for_element(device, tr_device_settings_dict, "third_party_software_notices_and_information")
    if "console" in device:
        tr_console_settings_keywords.tap_on_device_right_corner(device)
    else:
        call_keywords.device_right_corner_click(device)


def third_party_software_and_information_in_about_page(device):
    common.wait_for_element(device, tr_device_settings_dict, "about")
    swipe_screen_page(device)
    swipe_screen_page(device)
    tr_call_keywords.swipe_till_end_page(device)
    common.wait_for_and_click(device, tr_device_settings_dict, "third_party_software_notices_and_information")
    common.wait_for_element(device, tr_device_settings_dict, "third_party_software_notices_and_information2")


def verify_wallpaper_page_in_teams_admin_setting(device):
    common.wait_for_and_click(device, tr_device_settings_dict, "general")
    common.wait_for_and_click(device, tr_device_settings_dict, "wallpaper")
    common.wait_for_element(device, tr_device_settings_dict, "background_wallpaper_text")


def verify_report_an_issue(device):
    common.wait_for_and_click(device, settings_dict, "Report_an_issue")
    common.wait_for_element(device, settings_dict, "send_bug")
    common.wait_for_and_click(device, ztp_dict, "Back_button")
