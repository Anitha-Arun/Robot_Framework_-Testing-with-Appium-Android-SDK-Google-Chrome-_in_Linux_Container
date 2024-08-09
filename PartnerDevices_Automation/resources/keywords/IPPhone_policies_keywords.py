from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Selectors import load_json_file
from initiate_driver import obj_dev as obj
import time
import common

display_time = 2
action_time = 3

calendar_dict = load_json_file("resources/Page_objects/Calendar.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")
navigation_dict = load_json_file("resources/Page_objects/Navigation.json")
calls_dict = load_json_file("resources/Page_objects/Calls.json")
people_dict = load_json_file("resources/Page_objects/People.json")


def verify_user_have_dial_pad_on_screen(device_list):
    devices = device_list.split(",")
    print("Devices : ", devices)
    for device in devices:
        print("device : ", device)
        driver = obj.device_store.get(alias=device)
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((MobileBy.ID, calls_dict["dial_pad"]["id"])))
            print("User have dial pad on the screen")
        except Exception as e:
            try:
                WebDriverWait(driver, 90).until(
                    EC.presence_of_element_located((MobileBy.ID, calls_dict["phone_number_with_backspace"]["id"]))
                )
                print("User have dial pad on the screen")
            except Exception as e:
                print("User don't have dial pad on the screen", e)
    pass


def verify_teams_app_have_global_search_option(device_list):
    devices = device_list.split(",")
    print("Devices : ", devices)
    for device in devices:
        common.click_if_present(device, people_dict, "people_tab")
        print("device : ", device)
        common.wait_for_element(device, calls_dict, "search")


def verify_teams_app_have_call_park_capability(device_list):
    devices = device_list.split(",")
    print("Devices : ", devices)
    for device in devices:
        print("device : ", device)
        common.wait_for_element(device, calls_dict, "call_park")


def verify_user_do_not_have_sign_out_option(device_list):
    devices = device_list.split(",")
    print("Devices : ", devices)
    for device in devices:
        print("device : ", device)
        driver = obj.device_store.get(alias=device)
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, navigation_dict["Navigation"]["xpath"]))
        ).click()
        time.sleep(action_time)
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, navigation_dict["Settings_button"]["xpath"]))
        ).click()
        time.sleep(action_time)
        driver.swipe(100, 430, 100, 10)
        try:
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, settings_dict["Sign_out"]["xpath"]))
            ).click()
        except Exception as e:
            print("User don't have sign out option", e)
    pass


def verify_that_teams_app_has_only_calendar_tab(device_list):
    devices = device_list.split(",")
    print("Devices : ", devices)
    for device in devices:
        print("device : ", device)
        driver = obj.device_store.get(alias=device)
        time.sleep(action_time)
        try:
            print("Meeting User")
            WebDriverWait(driver, 90).until(EC.presence_of_element_located((MobileBy.ID, calls_dict["search"]["id"])))
            print("Search option available")
            head_text = driver.find_element_by_id(calls_dict["Header"]["id"]).text
            print("head_text :", head_text)
            if head_text in ["Calendar", "Calls", "Voicemail", "People"]:
                raise AssertionError("Device contains teams Tab name")
            else:
                print("Device doesn't contain Calender name")
        except Exception as e:
            print("Not in Calender Tab : ", device)
            raise AssertionError("Not in Calender Tab : " + device)

    pass
