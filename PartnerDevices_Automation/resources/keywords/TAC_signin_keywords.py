import common
import time
from initiate_driver import config
from Libraries.Selectors import load_json_file
from selenium import webdriver

web_signin_dict = load_json_file("resources/Page_objects/Web_signin.json")
tac_dict = load_json_file("resources/Page_objects/TAC.json")


def perform_TAC_web_sign(device):
    username = config["tenant_admin"]["username"]
    password = config["tenant_admin"]["password"]
    chrome_driver = webdriver.Chrome(config["chrome_driver_path"])
    chrome_driver.get("https://admin.teams.microsoft.com")
    time.sleep(5)
    chrome_driver.maximize_window()
    chrome_driver.find_element_by_id(web_signin_dict["web_username_field"]["id"]).send_keys(username)
    chrome_driver.find_element_by_id(web_signin_dict["web_next_btn"]["id"]).click()
    time.sleep(3)
    chrome_driver.find_element_by_id(web_signin_dict["web_pswd_field"]["id"]).send_keys(password)
    time.sleep(3)
    chrome_driver.find_element_by_id(web_signin_dict["web_next_btn"]["id"]).click()
    time.sleep(3)
    chrome_driver.find_element_by_id(web_signin_dict["web_next_btn"]["id"]).click()
    time.sleep(5)
    common.sleep_with_msg(device, 5, "Allow app to settle")
    # VERIFY USERNAME SIGNED IN TAC
    chrome_driver.find_element_by_id(tac_dict["web_profile_pic"]["id"]).click()
    print("clicked profile pic")
    time.sleep(5)
    admin_name = chrome_driver.find_element_by_xpath(tac_dict["web_display_txt"]["xpath"])
    admin_user_name = admin_name.text
    if admin_user_name != username:
        raise AssertionError(f"TAC username is not matching: {admin_user_name} ")
    chrome_driver.find_element_by_id(tac_dict["web_profile_pic"]["id"]).click()

    # Navigate to panels in Teams device
    chrome_driver.find_element_by_xpath(tac_dict["teams_device_option"]["xpath"]).click()
    time.sleep(3)
    chrome_driver.find_element_by_xpath(tac_dict["panels_option"]["xpath"]).click()
    time.sleep(3)
    panels_header = chrome_driver.find_element_by_xpath(tac_dict["tac_panels_header"]["xpath"]).text
    if panels_header != "Panels":
        raise AssertionError(f"Teams device option is not Panels as per expected : {panels_header}")
    print("opened panels page in TAC")
