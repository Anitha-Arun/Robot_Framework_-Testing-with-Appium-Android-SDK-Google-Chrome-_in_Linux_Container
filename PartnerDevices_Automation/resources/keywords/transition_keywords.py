from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Selectors import load_json_file
from initiate_driver import obj_dev as obj
import time
import call_keywords
import SignInOut
import common


display_time = 2
action_time = 3

calls_dict = load_json_file("resources/Page_objects/Calls.json")


def speed_dial_pretransition(device):
    print("device :", device)
    SignInOut.verify_and_enable_home_app(device)


def speed_dial_performtransition(device):
    print("device :", device)
    call_keywords.navigate_to_calls_favorites_page(device)
    common.wait_for_element(device, calls_dict, "speed_dial_header")


def dialpad_pretransition(device):
    print("device :", device)
    SignInOut.verify_and_enable_home_app(device)


def dialpad_performtransition(device):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, calls_dict["Make_a_call"]["id"]))
        ).click()
        time.sleep(10)
        print("verified call dial pad")

    except Exception:
        raise AssertionError("DialPad Transition Error")
