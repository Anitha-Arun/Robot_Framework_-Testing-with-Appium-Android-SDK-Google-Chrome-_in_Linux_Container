from selenium.webdriver.common.by import By
import common
import time
from initiate_driver import config
from Libraries.Selectors import load_json_file
from selenium import webdriver

sign_dict = load_json_file("resources/Page_objects/Signin.json")
calls_dict = load_json_file("resources/Page_objects/Calls.json")
web_signin_dict = load_json_file("resources/Page_objects/Web_signin.json")
lcp_homescreen_dict = load_json_file("resources/Page_objects/lcp_homescreen.json")


def signin_method_for_lcp(device, user=None):
    if user is None or user == "None":
        user = device
    elif "device" not in user:
        user = device + ":" + user
    username, password, user, account = common.get_credentials(user)
    common.sleep_with_msg(device, 10, "Allow app to settle")
    if common.is_element_present(device, sign_dict, "refresh_code_button"):
        common.wait_for_and_click(device, sign_dict, "refresh_code_button")
        common.sleep_with_msg(device, 5, "Allow refresh of DFC code")
    dfc_login_code = common.wait_for_element(device, sign_dict, "dcf_code").text
    perform_web_sign(dfc_login_code, username, password)
    # wait time work around for Bug 3633981:[SigninFriction][Phones][LCP][Automation]DUT is taking more time to get sign in, as no updates on fix
    common.sleep_with_msg(device, wait_seconds=90, why_message="waiting for web sign in to complete")
    common.wait_for_element(device, lcp_homescreen_dict, "user_profile_picture", wait_attempts=60)


def perform_web_sign(sign_in_code, username, pswd):
    chrome_driver = webdriver.Chrome()
    chrome_driver.get("https://login.microsoftonline.com/common/oauth2/deviceauth")
    time.sleep(5)
    chrome_driver.maximize_window()
    web_code = chrome_driver.find_element(by=By.NAME, value=web_signin_dict["web_code_field"]["name"])
    web_code.click()
    web_code.send_keys(sign_in_code)
    chrome_driver.find_element(By.ID, web_signin_dict["web_next_btn"]["id"]).click()
    time.sleep(3)
    chrome_driver.find_element(By.ID, web_signin_dict["web_username_field"]["id"]).send_keys(username)
    chrome_driver.find_element(By.ID, web_signin_dict["web_next_btn"]["id"]).click()
    time.sleep(3)
    chrome_driver.find_element(By.ID, web_signin_dict["web_pswd_field"]["id"]).send_keys(pswd)
    time.sleep(3)
    chrome_driver.find_element(By.ID, web_signin_dict["web_next_btn"]["id"]).click()
    time.sleep(3)
    chrome_driver.find_element(By.ID, web_signin_dict["web_next_btn"]["id"]).click()
    time.sleep(5)
    chrome_driver.close()


def verify_ui_post_signin(device, user_account=None):
    device, account = common.decode_device_spec(device)
    common.wait_for_element(device, lcp_homescreen_dict, "homescreen_menu")
    common.wait_for_element(device, lcp_homescreen_dict, "user_profile_picture")
    displayed_phone_number = common.wait_for_element(device, lcp_homescreen_dict, "phone_number").text
    if user_account == None:
        expected_phone_number = config["devices"][device][account]["pstndisplay"]
    else:
        expected_phone_number = config["devices"][user_account][account]["pstndisplay"]
    if displayed_phone_number != expected_phone_number:
        raise AssertionError(
            f"{device}: Displayed phone number: {displayed_phone_number} doesn't match the expected number: {expected_phone_number}"
        )
    common.wait_for_element(device, lcp_homescreen_dict, "calls_tab")
    common.wait_for_element(device, lcp_homescreen_dict, "people_tab")
    ##Work around for this bug : Bug 3812131: [Phones][LCP]"Display call forwarded on home screen" toggle is disabled by default in calling settings
    # common.wait_for_element(device, lcp_homescreen_dict, "forward_screen_menu")
    if account == "cap_search_enabled":
        """Cap Search Enabled account should not contains voicemail and lock options"""
        pass
    else:
        common.wait_for_element(device, lcp_homescreen_dict, "voicemail_tab")
        common.wait_for_element(device, lcp_homescreen_dict, "lock")


def verify_signin_ui_on_lcp(device):
    common.sleep_with_msg(device, 10, "Wait until signin page display")
    if common.is_element_present(device, sign_dict, "refresh_code_button"):
        common.wait_for_and_click(device, sign_dict, "refresh_code_button")
        common.sleep_with_msg(device, 5, "Allow refresh of DFC code")
    common.wait_for_element(device, sign_dict, "dcf_code")


def verify_sign_in_on_the_device_is_disabled(device):
    if common.is_element_present(device, sign_dict, "sign_in_on_the_device"):
        raise AssertionError(f"sign_in_on_the_device is present on {device}")
