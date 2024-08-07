from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import InvalidElementStateException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import SignInOut
import call_views_keywords
import device_control
from Selectors import load_json_file
from initiate_driver import obj_dev as obj
from initiate_driver import config
import settings_keywords
import calendar_keywords
import call_keywords
import re
import common
import subprocess
import pytz
from datetime import datetime
import time
import SignInOut
import tr_calendar_keywords

display_time = 2
action_time = 3
action_times = 10

calls_dict = load_json_file("resources/Page_objects/Calls.json")
sign_dict = load_json_file("resources/Page_objects/Signin.json")
navigation_dict = load_json_file("resources/Page_objects/Navigation.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")
device_settings_dict = load_json_file("resources/Page_objects/Device_settings.json")
timezone_dict = load_json_file("timezone_list.json")
tr_device_settings_dict = load_json_file("resources/Page_objects/tr_device_settings.json")
tr_settings_dict = load_json_file("resources/Page_objects/tr_settings.json")
panels_device_settings_dict = load_json_file("resources/Page_objects/panels_device_settings.json")
tr_console_home_screen_dict = load_json_file("resources/Page_objects/rooms_console_home_screen.json")
calendar_dict = load_json_file("resources/Page_objects/Calendar.json")
tr_console_settings_dict = load_json_file("resources/Page_objects/rooms_console_settings.json")


def sign_out_oem(device):
    driver = obj.device_store.get(alias=device)
    if config["devices"][device]["model"].lower() == "gilbert":
        swipe_the_page_till_signout(device)
    time.sleep(display_time)
    if not common.click_if_present(device, settings_dict, "hotline_settings_btn"):
        common.wait_for_and_click(device, settings_dict, "Device_Settings")
    time.sleep(action_time)

    if config["devices"][device]["model"].lower() in ["albany"]:
        swipe_till_sign_out(device)
        # driver.swipe(100, 430, 100, 10)
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["sacramento_sign_out"]["xpath2"]))
            ).click()
            print("Clicked on sacramento_sign_out xpath2")
        except Exception as e:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["sacramento_sign_out"]["xpath"]))
            ).click()
            print("Clicked on sacramento_sign_out xpath")
        # xpath1 for landscape, xpath for portrait
        element1 = driver.find_element_by_xpath(settings_dict["admin_pass"]["xpath1"])
        admin_pwd = config["devices"][device]["admin_password"]
        print("admin_pwd : ", admin_pwd)
        element1.set_value(admin_pwd)
        time.sleep(action_time)
        element2 = driver.find_element_by_xpath(settings_dict["admin_enter"]["xpath"])
        element2.click()
        time.sleep(action_time)
        button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((MobileBy.XPATH, sign_dict["Sign_out_ok_button"]["xpath"]))
        )
        button.click()

    elif config["devices"][device]["model"].lower() in ["gilbert", "scottsdale"]:
        swipe_the_page_till_signout(device)
        swipe_the_page_till_signout(device)
        common.wait_for_and_click(device, settings_dict, "Device_administration")
        common.wait_for_and_click(device, settings_dict, "Device_login")
        common.wait_for_and_click(device, settings_dict, "admin_passwd", "xpath")
        common.wait_for_element(device, settings_dict, "admin_passwd", "xpath").set_value(
            config["devices"][device]["admin_password"]
        )
        common.wait_for_and_click(device, settings_dict, "Sign_out_ok")
        common.wait_for_and_click(device, settings_dict, "Account_Signout", "xpath")
        common.wait_for_and_click(device, settings_dict, "Sign_out_ok")

    elif config["devices"][device]["model"].lower() in ["seattle", "olympia", "tacoma", "kirkland"]:
        common.wait_for_and_click(device, settings_dict, "Admin_Only", "xpath")
        common.wait_for_and_click(device, settings_dict, "admin_passwd", "xpath")
        common.wait_for_element(device, settings_dict, "admin_passwd", "xpath").set_value(
            config["devices"][device]["admin_password"]
        )
        common.hide_keyboard(device)
        common.wait_for_and_click(device, settings_dict, "done")
        if not common.is_element_present(device, settings_dict, "Account_Signout"):
            swipe_till_sign_out(device)
            swipe_till_sign_out(device)
        common.wait_for_and_click(device, settings_dict, "Account_Signout", "xpath1")
        common.wait_for_and_click(device, sign_dict, "Sign_out_ok_button", "id")

    elif config["devices"][device]["model"].lower() == "redmond":
        common.wait_for_and_click(device, settings_dict, "Admin_Only")
        common.wait_for_element(device, settings_dict, "admin_passwd", "xpath").set_value(
            config["devices"][device]["admin_password"]
        )
        driver.execute_script("mobile: performEditorAction", {"action": "done"})
        settings_keywords.swipe_till_end(device)
        common.wait_for_and_click(device, settings_dict, "Account_Signout")
        common.wait_for_and_click(device, settings_dict, "Sign_out_ok")

    elif config["devices"][device]["model"].lower() == "miami":
        print("Device : miami ")
        time.sleep(action_time)
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((MobileBy.ID, settings_dict["Admin_Only"]["id"]))
            ).click()
        except Exception as e:
            swipe_the_page_till_signout(device)
            time.sleep(display_time)
            admin = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((MobileBy.XPATH, settings_dict["Admin_Only"]["xpath1"]))
            )
            admin.click()
        print("Clicked inside the Admin Settings Sign out")
        time.sleep(action_time)
        element1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.ID, settings_dict["admin_pass"]["id1"]))
        )
        print("Admin password is displayed ")
        if element1.is_displayed():
            element1.set_value(config["devices"][device]["admin_password"])
            print("Set admin password value")
            ele = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((MobileBy.ID, settings_dict["Sign_out_ok"]["id"]))
            )
            ele.click()
            print("Clicked on Input Admin OK button ")
            time.sleep(action_time)
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((MobileBy.XPATH, settings_dict["Sign_out_teams"]["xpath1"]))
                ).click()
                print("Sign_out option is behind Admin settings option : ", device)
                print("User Successfully Sign out ")
            except Exception as e:
                print("Sign_out option is not behind Admin settings option : ", device)
                raise AssertionError("Sign_out option is not behind Admin settings option")

    elif config["devices"][device]["model"].lower() in [
        "bakersfield",
        "santa cruz",
        "san jose",
        "san diego",
    ]:
        swipe_till_sign_out(device)
        swipe_till_sign_out(device)
        common.wait_for_and_click(device, device_settings_dict, "teams_admin_setting_01")
        common.wait_for_and_click(device, settings_dict, "admin_pass")
        common.wait_for_element(device, settings_dict, "admin_pswd_option").set_value(
            config["devices"][device]["admin_password"]
        )
        common.hide_keyboard(device)
        common.wait_for_and_click(device, device_settings_dict, "enter_button")
        common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings_01_btn")
        common.wait_for_and_click(device, settings_dict, "Sign_out", "id")
        common.wait_for_and_click(device, sign_dict, "Sign_out_ok_button")

    elif config["devices"][device]["model"].lower() in ["santa cruz_13", "bakersfield_13", "riverside_13"]:
        for i in range(3):
            if common.is_element_present(device, device_settings_dict, "teams_admin_settings", "text"):
                common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings", "text")
            else:
                swipe_till_sign_out(device)
        common.wait_for_element(device, panels_device_settings_dict, "pass_editbox").set_value(
            config["devices"][device]["admin_password"]
        )
        common.hide_keyboard(device)
        common.wait_for_and_click(device, device_settings_dict, "ok")
        common.wait_for_and_click(device, settings_dict, "Sign_out", "id")
        common.wait_for_and_click(device, sign_dict, "Sign_out_ok_button")

    elif config["devices"][device]["model"].lower() in ["riverside", "los angeles", "berkely"]:
        swipe_till_sign_out(device)
        common.wait_for_and_click(device, settings_dict, "device_admin_pswd")
        common.wait_for_element(device, settings_dict, "device_admin_pswd").set_value(
            config["devices"][device]["admin_password"]
        )
        driver.execute_script("mobile: performEditorAction", {"action": "done"})
        swipe_till_sign_out(device)
        swipe_till_sign_out(device)
        time.sleep(3)
        if not common.click_if_present(device, settings_dict, "sign_out_option"):
            common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings", "text")
            common.wait_for_and_click(device, settings_dict, "Sign_out", "id")
        common.wait_for_and_click(device, sign_dict, "Sign_out_ok_button")

    elif config["devices"][device]["model"].lower() == "manhattan":
        common.wait_for_and_click(device, settings_dict, "Admin_Settings")
        element1 = common.wait_for_element(device, settings_dict, "admin_passwd")
        element1.set_value(config["devices"][device]["admin_password"])
        driver.execute_script("mobile: performEditorAction", {"action": "done"})
        common.wait_for_and_click(device, settings_dict, "Login_btn")
        print(f"{device} Clicked on login button")
        common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings")
        common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings_btn")
        common.wait_for_and_click(device, settings_dict, "Sign_out")
        common.wait_for_and_click(device, settings_dict, "Sign_out_ok")

    elif config["devices"][device]["model"].lower() in ["queens", "long island"]:
        common.wait_for_and_click(device, device_settings_dict, "admin_settings")
        element1 = common.wait_for_element(device, settings_dict, "admin_passwd")
        element1.set_value(config["devices"][device]["admin_password"])
        driver.execute_script("mobile: performEditorAction", {"action": "done"})
        common.wait_for_and_click(device, settings_dict, "Login_btn")
        time.sleep(action_time)
        settings_keywords.swipe_till_end(device)
        time.sleep(display_time)
        if common.is_element_present(device, device_settings_dict, "teams_admin_settings"):
            common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings")
            common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings_btn")
            common.wait_for_and_click(device, settings_dict, "Sign_out")
            common.wait_for_and_click(device, settings_dict, "Sign_out_ok")
        else:
            common.wait_for_and_click(device, device_settings_dict, "user_sign_out")
            common.wait_for_and_click(device, device_settings_dict, "user_sign_out_btn")
            common.wait_for_and_click(device, device_settings_dict, "user_sign_out_yes")

    elif config["devices"][device]["model"].lower() == "malibu_13":
        for i in range(6):
            if common.is_element_present(device, device_settings_dict, "teams_admin_settings", "text"):
                common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings", "text")
            else:
                driver.swipe(280, 180, 280, 75)
        common.wait_for_element(device, panels_device_settings_dict, "pass_editbox").set_value(
            config["devices"][device]["admin_password"]
        )
        common.hide_keyboard(device)
        common.wait_for_and_click(device, device_settings_dict, "ok")
        common.wait_for_and_click(device, settings_dict, "Sign_out", "id")
        common.wait_for_and_click(device, sign_dict, "Sign_out_ok_button")

    elif common.is_norden(device):
        if config["devices"][device]["model"].lower() in ["oakland", "irvine", "eureka", "santamonica", "pasadena"]:
            common.sleep_with_msg(device, 5, "Waiting for loading the device settings page")
            if config["devices"][device]["model"].lower() in ["pasadena", "santamonica"]:
                for i in range(3):
                    if common.is_element_present(device, tr_device_settings_dict, "teams_admin_settings1"):
                        break
                    settings_keywords.swipe_till_end(device)
            else:
                swipe_right_side_screen_till_bottom(device)
                swipe_right_side_screen_till_bottom(device)
            common.wait_for_and_click(device, tr_device_settings_dict, "teams_admin_settings1")
            common.wait_for_element(device, settings_dict, "admin_pass", "xpath1").send_keys(
                config["devices"][device]["admin_password"]
            )
            print("Entered the admin password value")
            common.wait_for_and_click(device, settings_dict, "admin_enter")
            common.wait_for_and_click(device, settings_dict, "Sign_out")
            common.wait_for_and_click(device, sign_dict, "Sign_out_ok_button")

        elif config["devices"][device]["model"].lower() in ["sammamish", "spokane", "everett", "renton", "vancouver"]:
            # common.wait_for_element(device, tr_device_settings_dict, "admin_settings", "xpath")
            common.wait_for_and_click(device, tr_device_settings_dict, "admin_settings", "xpath")
            common.sleep_with_msg(device, 2, "Waiting for username and password edit box to appear")
            e1 = common.wait_for_element(
                device, tr_device_settings_dict, "edit_box_field", "xpath", cond=EC.visibility_of_all_elements_located
            )
            e1[0].send_keys(config["devices"][device]["admin_username"])
            print("Admin Username entered")
            time.sleep(action_time)
            e1[1].send_keys(config["devices"][device]["admin_password"])
            print("Admin password entered")
            common.wait_for_and_click(device, tr_device_settings_dict, "ok")
            time.sleep(action_time)
            if common.is_element_present(device, tr_device_settings_dict, "user_sign_out"):
                print("User sign out option is visible inside admin settings option")
                common.wait_for_and_click(device, tr_device_settings_dict, "user_sign_out")
                common.wait_for_and_click(device, tr_device_settings_dict, "ok")
                print(f"{device} : Sign out Successfully from the Admin settings option")
            else:
                raise AssertionError(f"{device} : User sign out option is not behind Admin settings option")

        elif config["devices"][device]["model"].lower() in ["atlanta"]:
            swipe_till_sign_out(device)
            swipe_till_sign_out(device)
            common.wait_for_and_click(device, settings_dict, "Sign_out")
            e1 = driver.find_element_by_xpath(settings_dict["admin_pass"]["xpath1"])
            e1.send_keys(config["devices"][device]["admin_password"])
            common.wait_for_and_click(device, settings_dict, "admin_enter_btn")
            common.wait_for_and_click(device, sign_dict, "Sign_out_ok_button")

        elif config["devices"][device]["model"].lower() in ["tucson"]:
            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (MobileBy.XPATH, tr_device_settings_dict["device_administration"]["xpath"])
                    )
                ).click()
                print("Clicked on the device_administration inside device admin settings")
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (MobileBy.XPATH, tr_device_settings_dict["device_administration_login"]["xpath"])
                    )
                ).click()
                print("Clicked on device_administration_login button")
                time.sleep(display_time)
                e1 = driver.find_element_by_id(settings_dict["admin_pass"]["id"])
                e1.send_keys(config["devices"][device]["admin_password"])
                print("Entered the admin password value")
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["ok"]["xpath"]))
                ).click()
                print("Clicked on OK button")
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, tr_device_settings_dict["account_signout"]["xpath"]))
                ).click()
                print("Clicked on account_signout button")
                print("Are you sure you want to signout from teams? text is visible")
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, sign_dict["Sign_out_ok_button"]["xpath"]))
                ).click()
                print("Sign out Successfully from the Admin settings option")
            except Exception as e:
                raise AssertionError("Sign out option is not behind Admin settings option", device)

        elif config["devices"][device]["model"].lower() in ["san francisco"]:
            settings_keywords.swipe_till_end(device)
            common.wait_for_and_click(device, tr_device_settings_dict, "teams_admin_settings1")
            e1 = common.wait_for_element(device, settings_dict, "admin_pass")
            e1.send_keys(config["devices"][device]["admin_password"])
            common.wait_for_and_click(device, tr_device_settings_dict, "admin_pass_enter")
            common.wait_for_and_click(device, tr_device_settings_dict, "teams_admin_settings2")
            common.wait_for_and_click(device, settings_dict, "admin_sign_out")
            common.wait_for_and_click(device, sign_dict, "Sign_out_ok_button", "xpath")

        elif config["devices"][device]["model"].lower() in ["houston", "austin", "sanantonio", "laredo"]:
            common.wait_for_and_click(device, tr_device_settings_dict, "admin_settings", "xpath1")
            common.wait_for_element(device, device_settings_dict, "edit_text_number_pin").send_keys(
                config["devices"][device]["admin_password"]
            )
            common.wait_for_and_click(device, device_settings_dict, "submit_button")
            common.wait_for_and_click(device, device_settings_dict, "system_settings")
            common.wait_for_and_click(device, tr_device_settings_dict, "service_provider")
            common.wait_for_and_click(device, tr_device_settings_dict, "teams_admin_settings1")
            common.wait_for_and_click(device, settings_dict, "Sign_out")
            common.wait_for_and_click(device, device_settings_dict, "ok")
            print("Sign out Sucessfully from admin settings page")

        elif config["devices"][device]["model"].lower() in ["detroit", "dearborn"]:
            common.wait_for_and_click(device, tr_device_settings_dict, "teams")
            common.wait_for_and_click(device, tr_device_settings_dict, "teams_admin_settings2", "xpath")
            ele = common.wait_for_element(
                device, tr_console_settings_dict, "admin_pass_field2", cond=EC.presence_of_all_elements_located
            )
            ele[-1].click()
            ele[-1].send_keys(config["devices"][device]["admin_password"])
            common.wait_for_and_click(device, sign_dict, "Sign_in")
            common.wait_for_and_click(device, tr_device_settings_dict, "teams_sign_out")
            common.wait_for_and_click(device, device_settings_dict, "ok")

        elif config["devices"][device]["model"].lower() in ["kodiak", "palmer"]:
            common.wait_for_and_click(device, tr_device_settings_dict, "login_to_admin")
            common.wait_for_and_click(device, tr_device_settings_dict, "admin_settings1")
            passcode = common.wait_for_element(device, tr_device_settings_dict, "admin_passcode")
            passcode.send_keys(config["devices"][device]["admin_password"])
            common.wait_for_and_click(device, tr_device_settings_dict, "login_button")
            driver.swipe(1280, 1728, 1280, 432)
            common.wait_for_and_click(device, tr_device_settings_dict, "teams_admin_setting")
            common.wait_for_and_click(device, tr_device_settings_dict, "teams_admin_setting1")
            common.wait_for_and_click(device, tr_device_settings_dict, "teams_sign_out")
            common.wait_for_and_click(device, device_settings_dict, "ok")

        elif config["devices"][device]["model"].lower() in ["vernon", "georgia", "manchester", "barre"]:
            enabling_the_teams_admin_settings(device)
            print("Clicked on teams admin settings")
            common.wait_for_and_click(device, settings_dict, "Sign_out")
            common.wait_for_and_click(device, device_settings_dict, "ok")

        elif config["devices"][device]["model"].lower() == "aurora":
            common.wait_for_and_click(device, tr_device_settings_dict, "admin")
            common.wait_for_element(device, tr_device_settings_dict, "username_filed").send_keys(
                config["devices"][device]["admin_username"]
            )
            common.wait_for_element(device, tr_device_settings_dict, "password_field").send_keys(
                config["devices"][device]["admin_password"]
            )
            common.wait_for_and_click(device, settings_dict, "Login_btn")
            common.wait_for_and_click(device, tr_device_settings_dict, "general")
            common.wait_for_and_click(device, tr_device_settings_dict, "service_provider")
            common.wait_for_and_click(device, tr_device_settings_dict, "access_settings")
            common.wait_for_and_click(device, settings_dict, "Sign_out")
            common.wait_for_and_click(device, device_settings_dict, "ok")

        elif config["devices"][device]["model"].lower() in ["page", "mesa"]:
            settings_keywords.swipe_till_end(device)
            common.wait_for_and_click(device, tr_device_settings_dict, "Device_administration")
            common.wait_for_and_click(device, tr_device_settings_dict, "device_administration_login")
            e1 = common.wait_for_element(device, settings_dict, "admin_pass")
            e1.send_keys(config["devices"][device]["admin_password"])
            common.wait_for_and_click(device, calendar_dict, "ok_button")
            settings_keywords.swipe_till_end(device)
            settings_keywords.swipe_till_end(device)
            common.wait_for_and_click(device, tr_device_settings_dict, "teams_admin_settings1")
            common.wait_for_and_click(device, tr_device_settings_dict, "teams_admin_settings_2")
            common.wait_for_and_click(device, settings_dict, "Sign_out")
            common.wait_for_and_click(device, device_settings_dict, "ok")

        elif config["devices"][device]["model"].lower() == "augusta":
            for i in range(5):
                if common.is_element_present(device, tr_device_settings_dict, "teams_admin_settings1"):
                    break
                settings_keywords.swipe_till_end(device)
            common.wait_for_and_click(device, tr_device_settings_dict, "teams_admin_settings1")
            e1 = common.wait_for_element(device, settings_dict, "admin_pass")
            e1.send_keys(config["devices"][device]["admin_password"])
            common.wait_for_and_click(device, tr_device_settings_dict, "admin_pass_enter")
            common.wait_for_and_click(device, settings_dict, "Sign_out")
            common.wait_for_and_click(device, device_settings_dict, "ok")

        elif config["devices"][device]["model"].lower() == "jackson":
            settings_keywords.swipe_till_end(device)
            if not common.is_element_present(device, tr_device_settings_dict, "pass_field"):
                common.wait_for_and_click(device, tr_device_settings_dict, "Teams")
                common.wait_for_and_click(device, tr_device_settings_dict, "teams_admin_settings1")
            e1 = common.wait_for_element(device, tr_device_settings_dict, "pass_field")
            e1.send_keys(config["devices"][device]["admin_password"])
            common.wait_for_and_click(device, tr_device_settings_dict, "Sign_in")
            common.wait_for_and_click(device, settings_dict, "Sign_out")
            common.wait_for_and_click(device, device_settings_dict, "ok")

    elif common.is_panel(device):
        if config["devices"][device]["model"].lower() in ["westchester", "brooklyn"]:
            common.wait_for_and_click(device, panels_device_settings_dict, "admin_settings")
            common.wait_for_element(device, panels_device_settings_dict, "admin_pswd_field").send_keys(
                config["devices"][device]["admin_password"]
            )
            common.wait_for_and_click(device, panels_device_settings_dict, "login_btn")
            time.sleep(5)
            swipe_till_sign_out(device)
            common.wait_for_and_click(device, panels_device_settings_dict, "account_sign_out")
            common.wait_for_and_click(device, panels_device_settings_dict, "sign_out_btn")
        elif config["devices"][device]["model"].lower() in ["beverly hills", "hollywood"]:
            # Find/click on the user sirn out option
            swipe_till_sign_out(device)
            swipe_till_sign_out(device)
            common.wait_for_and_click(device, panels_device_settings_dict, "device_settings_list_user_sign_out_option")

            # At this point, the device needs device admin credentials.
            #   If they have not already been entered previously, they will be requested:
            time.sleep(1)
            if common.click_if_present(device, panels_device_settings_dict, "admin_pswd_field"):
                _, admin_password = common.device_admin_credentials(device)

                common.wait_for_element(device, panels_device_settings_dict, "admin_pswd_field").set_value(
                    admin_password
                )
                common.wait_for_and_click(device, panels_device_settings_dict, "admin_login_btn")

            common.wait_for_and_click(device, panels_device_settings_dict, "california_device_settings_sign_out_btn")

            common.wait_for_and_click(device, device_settings_dict, "california_ok")

        elif config["devices"][device]["model"].lower() == "savannah":
            common.wait_for_and_click(device, panels_device_settings_dict, "admin_pswd_field")
            common.wait_for_element(device, panels_device_settings_dict, "admin_pswd_field").set_value(
                config["devices"][device]["admin_password"]
            )
            common.wait_for_and_click(device, panels_device_settings_dict, "admin_login_continue_btn")
            time.sleep(5)
            swipe_till_sign_out(device)
            time.sleep(5)
            swipe_till_sign_out(device)
            common.wait_for_and_click(device, settings_dict, "Sign_out", "xpath")
            common.wait_for_and_click(device, device_settings_dict, "ok")
        elif config["devices"][device]["model"].lower() == "flint":
            common.wait_for_and_click(device, device_settings_dict, "admin_settings")
            ele = common.wait_for_element(
                device, panels_device_settings_dict, "admin_pass_field", cond=EC.presence_of_all_elements_located
            )
            ele[-1].click()
            ele[-1].send_keys(config["devices"][device]["admin_password"])
            common.wait_for_and_click(device, calendar_dict, "ok_button")
            common.wait_for_element(device, device_settings_dict, "admin_settings")
            common.wait_for_and_click(device, tr_device_settings_dict, "teams_sign_out")
            common.wait_for_and_click(device, device_settings_dict, "ok")
        elif config["devices"][device]["model"].lower() == "arlington":
            common.wait_for_and_click(device, tr_device_settings_dict, "admin_settings", "xpath1")
            common.wait_for_element(device, device_settings_dict, "edit_text_number_pin").send_keys(
                config["devices"][device]["admin_password"]
            )
            common.wait_for_and_click(device, device_settings_dict, "submit_button")
            common.wait_for_and_click(device, device_settings_dict, "system_settings")
            common.wait_for_and_click(device, tr_device_settings_dict, "service_provider")
            common.wait_for_and_click(device, settings_dict, "Sign_out")
            common.wait_for_and_click(device, settings_dict, "Sign_out")
        if config["devices"][device]["model"].lower() == "richland":
            common.wait_for_and_click(device, tr_device_settings_dict, "admin_settings", "xpath")
            common.wait_for_element(device, device_settings_dict, "admin_username_box").send_keys(
                config["devices"][device]["admin_username"]
            )
            common.wait_for_element(device, settings_dict, "admin_passwd", "id1").set_value(
                config["devices"][device]["admin_password"]
            )
            common.wait_for_and_click(device, calendar_dict, "ok_button")
            common.wait_for_element(device, tr_device_settings_dict, "admin_settings")
            common.wait_for_and_click(device, device_settings_dict, "user_sign_out")
            common.wait_for_and_click(device, calendar_dict, "ok_button")
        if config["devices"][device]["model"].lower() == "surprise":
            common.wait_for_and_click(device, settings_dict, "Device_administration")
            if common.click_if_present(device, panels_device_settings_dict, "login_btn"):
                common.wait_for_element(device, settings_dict, "admin_passwd", "xpath").set_value(
                    config["devices"][device]["admin_password"]
                )
                common.wait_for_and_click(device, calendar_dict, "ok_button")
            common.wait_for_and_click(device, device_settings_dict, "user_sign_out")
            common.wait_for_and_click(device, calendar_dict, "ok_button")


def swipe_till_sign_out(device):
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
        print("Swiping co-ordinates : ", width / 4, 4 * (height / 5), width / 4, height / 5)
        driver.swipe(width / 4, 4 * (height / 5), width / 4, height / 5)
    pass


def handle_system_time_zone_popup(device):
    if common.is_element_present(device, device_settings_dict, "time_zone_popup_title"):
        common.wait_for_and_click(device, device_settings_dict, "ok")
        print(f"Handled time zone pop-up on the device: {device}")
        return


def get_current_timezone(device):
    devices = device.split(",")
    for device in devices:
        driver = obj.device_store.get(alias=device)
        settings_keywords.open_settings_page(device)
        if config["devices"][device]["model"].lower() == "miami":
            driver.swipe(300, 700, 300, 200)
        else:
            pass
        settings_keywords.click_device_settings(device)
        if config["devices"][device]["model"].lower() in [
            "san diego",
            "los angeles",
            "albany",
            "sunnyvale",
            "berkely",
        ]:
            try:
                print("select device : ", config["devices"][device]["model"])
                xpath = driver.find_element_by_xpath(device_settings_dict["time_date"]["xpath"])
                if xpath.is_displayed():
                    xpath.click()
                    print("Clicked on time and date tab")
                time.sleep(display_time)
                timezone_xpath = driver.find_element_by_xpath(device_settings_dict["current_time_zone"]["xpath"])
                if timezone_xpath.is_displayed():
                    current_timezone = timezone_xpath.text
                    print("current_timezone : ", current_timezone)
            except Exception as e:
                raise AssertionError("Xpath not found")
            print("xpath : ", xpath)
            time.sleep(display_time)
            if config["devices"][device]["model"].lower() in ["los angeles", "sunnyvale", "berkely"]:
                settings_keywords.device_setting_back(device)
            else:
                pass
        elif config["devices"][device]["model"].lower() == "phoenix":
            try:
                print("select device : phoenix")
                time.sleep(display_time)
                xpath = driver.find_element_by_xpath(device_settings_dict["date_time"]["xpath1"])
                if xpath.is_displayed():
                    xpath.click()
                    print("Clicked on date and time tab")
                time.sleep(display_time)
                driver.swipe(300, 600, 300, 300)
                timezone_xpath = driver.find_element_by_xpath(device_settings_dict["current_time_zone"]["xpath1"])
                if timezone_xpath.is_displayed():
                    device_timezone = timezone_xpath.text
                string1 = device_timezone
                print("string1 : ", string1)
                tz_value = list(map(int, re.findall(r"\d+", string1)))
                x = re.findall("-", string1)
                y = re.findall("[+]", string1)
                strng = ""
                if x:
                    for n in x:
                        strng = n
                elif y:
                    for n in y:
                        strng = n
                if str(tz_value[1]) == "0":
                    current_timezone = str(strng) + str(tz_value[0])
                else:
                    current_timezone = str(strng) + str(tz_value[0]) + ":" + str(tz_value[1])
                print("new_tz_value : ", current_timezone)
                # subprocess.call("adb -s {} shell input keyevent 4".format(config['devices'][device]['desired_caps']['udid'].split(':')[0]), shell=True)
                settings_keywords.device_setting_back(device)
            except Exception as e:
                raise AssertionError("Xpath not found")

        elif config["devices"][device]["model"].lower() in ["seattle", "olympia", "redmond", "kirkland"]:
            try:
                print("select device : ", config["devices"][device]["model"])
                xpath = driver.find_element_by_xpath(device_settings_dict["date_time"]["xpath"])
                if xpath.is_displayed():
                    xpath.click()
                    print("Clicked on date and time tab")
                time.sleep(display_time)
                timezone_xpath = driver.find_element_by_xpath(device_settings_dict["current_time_zone"]["xpath1"])
                if timezone_xpath.is_displayed():
                    device_timezone = timezone_xpath.text
                string1 = device_timezone
                print("string1 : ", string1)
                tz_value = list(map(int, re.findall(r"\d+", string1)))
                x = re.findall("-", string1)
                y = re.findall("[+]", string1)
                strng = ""
                if x:
                    for n in x:
                        strng = n
                elif y:
                    for n in y:
                        strng = n
                if str(tz_value[1]) == "0":
                    current_timezone = str(strng) + str(tz_value[0])
                else:
                    current_timezone = str(strng) + str(tz_value[0]) + ":" + str(tz_value[1])
                print("new_tz_value : ", current_timezone)
                if config["devices"][device]["model"].lower() in ["seattle", "olympia", "kirkland"]:
                    settings_keywords.device_setting_back(device)
                else:
                    pass
            except Exception as e:
                raise AssertionError("Xpath not found")
        elif config["devices"][device]["model"].lower() == "miami":
            try:
                print("select device : ", config["devices"][device]["model"])
                xpath = driver.find_element_by_xpath(device_settings_dict["time_date"]["xpath1"])
                if xpath.is_displayed():
                    xpath.click()
                    print("Clicked on time and date tab")
                time.sleep(display_time)
                timezone_xpath = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["current_time_zone"]["xpath2"]))
                )
                if timezone_xpath.is_displayed():
                    device_timezone = timezone_xpath.text
                    print("device_timezone : ", device_timezone)
                string1 = device_timezone
                words = string1.split()
                letters = [word[0] for word in words]
                current_timezone = "".join(letters)
                print("new_tz_value : ", current_timezone)
            except Exception as e:
                raise AssertionError("Xpath not found")
        return current_timezone


def change_timezone(device, required_timezone):
    devices = device.split(",")
    for device in devices:
        driver = obj.device_store.get(alias=device)
        current_timezone = get_current_timezone(device)
        print("current_timezone : ", current_timezone)
        select_timezone = timezone_dict["Timezone"][required_timezone]["relative_GMT"]
        # select_timezone = select_timezone.replace("GMT","")
        print("select_timezone : ", select_timezone)
        if current_timezone == select_timezone:
            print("Already this timezone selected")
            pass
        elif current_timezone == required_timezone:
            print("Already this timezone selected")
            pass
        else:
            if config["devices"][device]["model"].lower() in [
                "san diego",
                "los angeles",
                "albany",
                "sunnyvale",
                "berkely",
            ]:
                try:
                    time.sleep(display_time)
                    if config["devices"][device]["model"].lower() in ["los angeles", "sunnyvale", "berkely"]:
                        xpath = driver.find_element_by_xpath(device_settings_dict["time_date"]["xpath"])
                        if xpath.is_displayed():
                            xpath.click()
                            print("Clicked on time and date tab")
                    else:
                        pass
                    timezone_xpath = driver.find_element_by_xpath(device_settings_dict["current_time_zone"]["xpath"])
                    if timezone_xpath.is_displayed():
                        timezone_xpath.click()
                        for i in range(5):
                            if config["devices"][device]["model"].lower() in ["los angeles", "sunnyvale", "berkely"]:
                                driver.swipe(100, 150, 100, 300)
                            else:
                                driver.swipe(400, 230, 400, 370)
                        for attempt in range(10):
                            try:
                                timezone_path = device_settings_dict["timezone_xpath"]["xpath"].replace(
                                    "timezone_replace", select_timezone
                                )
                                print("timezone_path : ", timezone_path)
                                elem = driver.find_element_by_xpath(timezone_path)
                                if elem.is_displayed():
                                    elem.click()
                                    time.sleep(display_time)
                                    break
                            except Exception as e:
                                if config["devices"][device]["model"].lower() in [
                                    "los angeles",
                                    "sunnyvale",
                                    "berkely",
                                ]:
                                    driver.swipe(100, 300, 100, 150)
                                else:
                                    driver.swipe(400, 370, 400, 230)
                except Exception as e:
                    raise AssertionError("Xpath not found")
                time.sleep(5)
                ok_btn = driver.find_element_by_xpath(device_settings_dict["ok"]["xpath"])
                ok_btn.click()
                time.sleep(display_time)
                ok_btn.click()
                if config["devices"][device]["model"].lower() in ["los angeles", "sunnyvale", "berkely"]:
                    settings_keywords.device_setting_back(device)
                else:
                    pass
            elif config["devices"][device]["model"].lower() == "phoenix":
                try:
                    print("select device : phoenix")
                    xpath = driver.find_element_by_xpath(device_settings_dict["date_time"]["xpath1"])
                    if xpath.is_displayed():
                        xpath.click()
                        print("Clicked on date and time tab")
                    time.sleep(display_time)
                    driver.swipe(300, 600, 300, 300)
                    time.sleep(display_time)
                    timezone_xpath = driver.find_element_by_xpath(device_settings_dict["current_time_zone"]["xpath1"])
                    if timezone_xpath.is_displayed():
                        timezone_xpath.click()
                    for i in range(15):
                        driver.swipe(300, 150, 300, 600)
                        time.sleep(display_time)
                    string1 = select_timezone
                    a = string1.split(":")
                    b = list(a[0])
                    if len(b) == 2:
                        c = "GMT" + b[0] + "0" + b[1]
                    else:
                        c = "GMT" + b[0] + b[1] + b[2]
                    try:
                        new_tz = c + ":" + a[1]
                    except IndexError:
                        new_tz = c + ":00"
                    print("new_tz : ", new_tz)
                    for attempt in range(20):
                        try:
                            timezone_path = device_settings_dict["timezone_xpath"]["xpath"].replace(
                                "timezone_replace", new_tz
                            )
                            print("timezone_path : ", timezone_path)
                            elem = driver.find_element_by_xpath(timezone_path)
                            if elem.is_displayed():
                                elem.click()
                                time.sleep(display_time)
                                break
                        except Exception as e:
                            driver.swipe(300, 600, 300, 150)
                            time.sleep(display_time)
                    # subprocess.call("adb -s {} shell input keyevent 4".format(config['devices'][device]['desired_caps']['udid'].split(':')[0]), shell=True)
                except Exception as e:
                    raise AssertionError("Xpath not found")
                settings_keywords.device_setting_back(device)
                settings_keywords.device_setting_back(device)
            elif config["devices"][device]["model"].lower() in ["seattle", "olympia", "redmond", "kirkland"]:
                try:
                    xpath = driver.find_element_by_xpath(device_settings_dict["date_time"]["xpath"])
                    if xpath.is_displayed():
                        xpath.click()
                        print("Clicked on date and time tab")
                    time.sleep(display_time)
                    timezone_xpath = driver.find_element_by_xpath(device_settings_dict["current_time_zone"]["xpath1"])
                    if timezone_xpath.is_displayed():
                        timezone_xpath.click()
                        time.sleep(display_time)
                        print("Clicked on Timezone")
                    for i in range(15):
                        if config["devices"][device]["model"].lower() in ["seattle", "olympia", "kirkland"]:
                            driver.swipe(300, 150, 300, 600)
                        else:
                            driver.swipe(600, 100, 600, 500)
                        time.sleep(action_time)
                    string1 = select_timezone
                    a = string1.split(":")
                    b = list(a[0])
                    if len(b) == 2:
                        c = "GMT" + b[0] + "0" + b[1]
                    else:
                        c = "GMT" + b[0] + b[1] + b[2]
                    try:
                        new_tz = c + ":" + a[1]
                    except IndexError:
                        new_tz = c + ":00"
                    print("new_tz : ", new_tz)
                    for attempt in range(20):
                        try:
                            timezone_path = device_settings_dict["timezone_xpath"]["xpath"].replace(
                                "timezone_replace", new_tz
                            )
                            print("timezone_path : ", timezone_path)
                            elem = driver.find_element_by_xpath(timezone_path)
                            if elem.is_displayed():
                                elem.click()
                                time.sleep(display_time)
                                break
                        except Exception as e:
                            if config["devices"][device]["model"].lower() in ["seattle", "olympia", "kirkland"]:
                                driver.swipe(300, 600, 300, 150)
                                time.sleep(display_time)
                            else:
                                driver.swipe(600, 500, 600, 100)
                                time.sleep(display_time)
                    settings_keywords.device_setting_back(device)
                except Exception as e:
                    raise AssertionError("Xpath not found")
            elif config["devices"][device]["model"].lower() == "miami":
                try:
                    print("select device : ", config["devices"][device]["model"])
                    xpath = driver.find_element_by_xpath(device_settings_dict["time_date"]["xpath1"])
                    if xpath.is_displayed():
                        xpath.click()
                        print("Clicked on time and date tab")
                    time.sleep(display_time)
                    timezone_xpath = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable(
                            (MobileBy.XPATH, device_settings_dict["current_time_zone"]["xpath2"])
                        )
                    )
                    if timezone_xpath.is_displayed():
                        timezone_xpath.click()
                    for i in range(15):
                        driver.swipe(950, 150, 950, 550)
                        time.sleep(display_time)
                    string1 = select_timezone  # +5:30
                    a = string1.split(":")
                    b = list(a[0])
                    if len(b) == 2:
                        c = "GMT" + b[0] + b[1]
                    else:
                        c = "GMT" + b[0] + b[1] + b[2]
                    try:
                        new_tz = c + ":" + a[1]
                    except IndexError:
                        new_tz = c + ":00"
                    print("new_tz : ", new_tz)
                    for attempt in range(20):
                        try:
                            timezone_path = device_settings_dict["timezone_xpath"]["xpath"].replace(
                                "timezone_replace", new_tz
                            )
                            print("timezone_path : ", timezone_path)
                            elem = driver.find_element_by_xpath(timezone_path)
                            if elem.is_displayed():
                                elem.click()
                                time.sleep(display_time)
                                break
                        except Exception as e:
                            driver.swipe(950, 550, 950, 150)
                            time.sleep(display_time)
                except Exception as e:
                    raise AssertionError("Xpath not found")


def change_timeformat(device, required_timeformat):
    devices = device.split(",")
    for device in devices:
        driver = obj.device_store.get(alias=device)
        settings_keywords.open_settings_page(device)
        if config["devices"][device]["model"].lower() == "miami":
            driver.swipe(300, 700, 300, 200)
        else:
            pass
        settings_keywords.click_device_settings(device)
        if config["devices"][device]["model"].lower() in [
            "san diego",
            "los angeles",
            "albany",
            "sunnyvale",
            "berkely",
        ]:
            try:
                print("select device : ", config["devices"][device]["model"])
                xpath = driver.find_element_by_xpath(device_settings_dict["time_date"]["xpath"])
                if xpath.is_displayed():
                    xpath.click()
                    print("Clicked on time and date tab")
                time.sleep(display_time)
            except Exception as e:
                raise AssertionError("Xpath not found")
            if config["devices"][device]["model"].lower() in ["los angeles"]:
                driver.swipe(100, 400, 100, 200)
                time.sleep(display_time)
                subprocess.call(
                    "adb -s {} shell input tap 228 451".format(
                        config["devices"][device]["desired_caps"]["udid"].split(":")[0]
                    ),
                    shell=True,
                )
                time.sleep(display_time)
            elif config["devices"][device]["model"].lower() in ["sunnyvale", "berkely"]:
                driver.swipe(100, 400, 100, 200)
                time.sleep(display_time)
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["time_format"]["xpath"]))
                ).click()
                # subprocess.call("adb -s {} shell input tap 228 451".format(config['devices'][device]['desired_caps']['udid'].split(':')[0]), shell=True)
                time.sleep(display_time)
            else:
                driver.swipe(700, 500, 700, 350)
                time.sleep(display_time)
                subprocess.call(
                    "adb -s {} shell input tap 969 568".format(
                        config["devices"][device]["desired_caps"]["udid"].split(":")[0]
                    ),
                    shell=True,
                )
                time.sleep(display_time)

            try:
                time_format = str(required_timeformat) + " Hour"
                timeformat_path = device_settings_dict["timezone_xpath"]["xpath"].replace(
                    "timezone_replace", time_format
                )
                print("timeformat_path : ", timeformat_path)
                elem = driver.find_element_by_xpath(timeformat_path)
                if elem.is_displayed():
                    elem.click()
                    print(required_timeformat, " Hous Timeformat selected")
            except Exception as e:
                raise AssertionError("Xpath not found")
            time.sleep(display_time)
            ok_btn = driver.find_element_by_xpath(device_settings_dict["ok"]["xpath"])
            ok_btn.click()
            time.sleep(display_time)
            if config["devices"][device]["model"].lower() in ["los angeles", "sunnyvale", "berkely"]:
                settings_keywords.device_setting_back(device)
            else:
                pass
        elif config["devices"][device]["model"].lower() == "phoenix":
            try:
                print("select device : phoenix")
                xpath = driver.find_element_by_xpath(device_settings_dict["time_date"]["xpath"])
                if xpath.is_displayed():
                    xpath.click()
                    print("Clicked on date and time tab")
                time.sleep(display_time)
                timezone_toggle = driver.find_element_by_xpath(device_settings_dict["timeformat_toggle_btn"]["xpath"])
                timezone_toggle_txt = timezone_toggle.text
                if required_timeformat == "24":
                    if timezone_toggle_txt == "OFF":
                        timezone_toggle.click()
                elif required_timeformat == "12":
                    if timezone_toggle_txt == "ON":
                        timezone_toggle.click()
            except Exception as e:
                raise AssertionError("Xpath not found")
            subprocess.call(
                "adb -s {} shell input keyevent 4".format(
                    config["devices"][device]["desired_caps"]["udid"].split(":")[0]
                ),
                shell=True,
            )
        elif config["devices"][device]["model"].lower() in ["seattle", "olympia", "redmond", "kirkland"]:
            try:
                print("select device : ", config["devices"][device]["model"])
                xpath = driver.find_element_by_xpath(device_settings_dict["date_time"]["xpath"])
                if xpath.is_displayed():
                    xpath.click()
                    print("Clicked on date and time tab")
                time.sleep(display_time)
                if config["devices"][device]["model"].lower() == "redmond":
                    subprocess.call(
                        "adb -s {} shell input tap 477 567".format(
                            config["devices"][device]["desired_caps"]["udid"].replace(":5555", "")
                        ),
                        shell=True,
                    )
                else:
                    subprocess.call(
                        "adb -s {} shell input tap 96 1012".format(
                            config["devices"][device]["desired_caps"]["udid"].replace(":5555", "")
                        ),
                        shell=True,
                    )
                    # el = driver.find_element_by_xpath(device_settings_dict["timeformat_btn"]["xpath"])
                    # if el.is_displayed():
                    #     el.click()
                    #     print "Clicked on Time format tab"
                if config["devices"][device]["model"].lower() == ["olympia"]:
                    timezone_toggle = driver.find_element_by_xpath(
                        device_settings_dict["timeformat_toggle_btn"]["xpath1"]
                    )
                    timezone_toggle_txt = timezone_toggle.text
                    if required_timeformat == "24":
                        if timezone_toggle_txt == "OFF":
                            timezone_toggle.click()
                            print(required_timeformat, " Hous Timeformat selected")
                    elif required_timeformat == "12":
                        if timezone_toggle_txt == "ON":
                            timezone_toggle.click()
                            print(required_timeformat, " Hous Timeformat selected")
                else:
                    time.sleep(display_time)
                    time_format = str(required_timeformat) + " - Hour"
                    timeformat_path = device_settings_dict["timezone_xpath"]["xpath1"].replace(
                        "timezone_replace", time_format
                    )
                    print("timeformat_path : ", timeformat_path)
                    elem = driver.find_element_by_xpath(timeformat_path)
                    if elem.is_displayed():
                        elem.click()
                        print(required_timeformat, " Hous Timeformat selected")
                settings_keywords.device_setting_back(device)
                time.sleep(display_time)
                try:
                    xpath = driver.find_element_by_xpath(device_settings_dict["save_btn"]["xpath"])
                    if xpath.is_displayed():
                        xpath.click()
                        print("changes Saved")
                except Exception as e:
                    print("Didn't ask to Save")
                    pass
                time.sleep(display_time)

            except Exception as e:
                raise AssertionError("Xpath not found")
        elif config["devices"][device]["model"].lower() == "miami":
            try:
                print("select device : ", config["devices"][device]["model"])
                xpath = driver.find_element_by_xpath(device_settings_dict["time_date"]["xpath1"])
                if xpath.is_displayed():
                    xpath.click()
                    print("Clicked on date and time tab")
                time.sleep(display_time)
                # driver.swipe(300, 600, 300, 300)
                timezone_toggle = driver.find_element_by_xpath(device_settings_dict["timeformat_toggle_btn"]["xpath2"])
                timezone_toggle_txt = timezone_toggle.text
                if required_timeformat == "24":
                    if timezone_toggle_txt == "OFF":
                        timezone_toggle.click()
                elif required_timeformat == "12":
                    if timezone_toggle_txt == "ON":
                        timezone_toggle.click()
            except Exception as e:
                raise AssertionError("Xpath not found")


def convert_timezone(convert_time, from_tz, to_tz):
    from_tz_name = timezone_dict["Timezone"][from_tz]["TZ_name"]
    to_tz_name = timezone_dict["Timezone"][to_tz]["TZ_name"]

    tz1 = pytz.timezone(from_tz_name)
    tz2 = pytz.timezone(to_tz_name)
    print("Given time to Convert : ", convert_time)
    dt = datetime.strptime("2020-01-06 " + convert_time, "%Y-%m-%d %H:%M")
    dt = tz1.localize(dt)
    dt = dt.astimezone(tz2)
    dt = dt.strftime("%H:%M")
    print("timee : ", dt)

    return dt


def get_converted_meeting_tz(meeting_time, from_tz, to_tz):
    print("meeting_time : ", meeting_time)
    meeting_split_time = meeting_time.split("-")
    print("meeting_split_time : ", meeting_split_time)
    converted_time_list = []
    for times in meeting_split_time:
        times = times.strip()
        print("splited time : ", times)
        converted_tz = convert_timezone(times, from_tz, to_tz)
        print("converted_tz : ", converted_tz)
        converted_time_list.append(converted_tz)
    new_time = " - ".join(converted_time_list)
    print("new time : ", new_time)
    return new_time


def get_timezone_name(tz_gmt_value):
    timezone_list = timezone_dict["Timezone"]
    for key, value in list(timezone_list.items()):
        print("value : ", value)
        if tz_gmt_value == value["relative_GMT"]:
            print("key :", key)
            return key
        elif tz_gmt_value == key:
            return key

    return "key doesn't exist"


def enable_lock_device(device, pin="123456"):
    devices = device.split(",")
    for device in devices:
        driver = obj.device_store.get(alias=device)
        settings_keywords.open_settings_page(device)
        if config["devices"][device]["model"].lower() == "los angeles":
            driver.swipe(100, 300, 100, 150)
        elif config["devices"][device]["model"].lower() == "miami":
            driver.swipe(300, 700, 300, 200)
        else:
            pass
        settings_keywords.click_device_settings(device)
        if pin == "123456":
            device_pin = "123456"
        else:
            device_pin = pin
        if config["devices"][device]["model"].lower() in ["san diego", "los angeles", "albany"]:
            try:
                print("select device : ", config["devices"][device]["model"])
                xpath = driver.find_element_by_xpath(device_settings_dict["phone_lock"]["xpath"])
                if xpath.is_displayed():
                    xpath.click()
                    print("Clicked on phone lock tab")
                time.sleep(display_time)
                xpath = driver.find_element_by_xpath(device_settings_dict["lock_enable_toggle"]["xpath"])
                if xpath.is_displayed():
                    xpath.click()
                    print("Clicked on lock enable toggle button")
                time.sleep(display_time)

                xpath = driver.find_element_by_xpath(device_settings_dict["new_pin"]["xpath"])
                xpath1 = driver.find_element_by_xpath(device_settings_dict["confirm_pin"]["xpath"])
                print("device_pin : ", device_pin)
                if xpath.is_displayed():
                    xpath.send_keys(device_pin)
                    time.sleep(display_time)
                    xpath1.send_keys(device_pin)
                    time.sleep(display_time)
                    print("Entered phone pin : ", device_pin)

                xpath = driver.find_element_by_xpath(device_settings_dict["idle_time_set"]["xpath"])
                if xpath.is_displayed():
                    xpath.click()
                    time.sleep(display_time)
                print("Clicked on Idle time-out tab")

                if config["devices"][device]["model"].lower() == "los angeles":
                    driver.swipe(100, 150, 100, 300)
                    driver.swipe(100, 150, 100, 300)
                else:
                    driver.swipe(400, 230, 400, 370)
                    driver.swipe(400, 230, 400, 370)
                xpath = driver.find_element_by_xpath(device_settings_dict["30s_idle_time"]["xpath"])
                if xpath.is_displayed():
                    xpath.click()
                    time.sleep(display_time)
                    ok_xpath = driver.find_element_by_xpath(device_settings_dict["ok"]["xpath"])
                    ok_xpath.click()
                    print("Select 30s")

                xpath = driver.find_element_by_xpath(device_settings_dict["pin_save_btn"]["xpath"])
                if xpath.is_displayed():
                    xpath.click()
                    time.sleep(display_time)
                    print("Saved..")
                if config["devices"][device]["model"].lower() == "los angeles":
                    settings_keywords.device_setting_back(device)
                else:
                    pass

            except Exception as e:
                raise AssertionError("Xpath not found")
        elif config["devices"][device]["model"].lower() == "phoenix":
            for attempt in range(3):
                try:
                    print("attempt : ", attempt)
                    WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["security_btn"]["xpath"]))
                    ).click()
                    print("Clicked on Security button")
                    break
                except Exception as e:
                    driver.swipe(400, 580, 400, 200)
            time.sleep(display_time)
            try:
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["Screen_lock"]["xpath"]))
                ).click()
                print("Clicked on Screen lock option")
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["Password_option"]["xpath"]))
                ).click()
                if device_pin == "123456":
                    for attempt in range(2):
                        press_123456(device)
                        subprocess.call(
                            "adb -s {} shell input keyevent 66".format(
                                config["devices"][device]["desired_caps"]["udid"].split(":")[0]
                            ),
                            shell=True,
                        )
                else:
                    raise AssertionError("Default password is not matching.. check again")
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.ID, device_settings_dict["setting_btn"]["id"]))
                ).click()
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["Automatic_lock_option"]["xpath"]))
                ).click()
                driver.swipe(600, 180, 600, 500)
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["Immediately_option"]["xpath"]))
                ).click()
                settings_keywords.device_setting_back(device)
                settings_keywords.device_setting_back(device)
                driver.swipe(400, 200, 400, 580)
                driver.swipe(400, 200, 400, 580)
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["Display_btn"]["xpath"]))
                ).click()
                print("Clicked on Display button")
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["sleep_option"]["xpath"]))
                ).click()
                print("Clicked on Sleep option")
                driver.swipe(600, 180, 600, 500)
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["30s_sleep_time"]["xpath"]))
                ).click()
                print("Selected 30 second Sleep")
                settings_keywords.device_setting_back(device)
                settings_keywords.device_setting_back(device)
            except Exception as e:
                raise AssertionError("Xpath not found")
        elif config["devices"][device]["model"].lower() == "miami":
            try:
                print("select device : ", config["devices"][device]["model"])
                for attempt in range(3):
                    try:
                        print("attempt : ", attempt)
                        WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["phone_lock"]["xpath1"]))
                        ).click()
                        print("Clicked on phone lock tab")
                        # break
                    except Exception as e:
                        driver.swipe(100, 700, 100, 300)
                time.sleep(display_time)
                xpath = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["lock_enable_toggle"]["xpath"]))
                )
                if xpath.text == "OFF":
                    xpath.click()
                    print("Clicked on lock disable toggle button")
                else:
                    raise AssertionError("Passward is not but toggle button is still ON ... Bug verification")
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["phn_lock_timeout"]["xpath"]))
                ).click()
                print("Clicked on Phone lock timeout button")
                driver.swipe(600, 170, 600, 400)
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["1m_sleep_time"]["xpath"]))
                ).click()
                print("Select 1m sleep")
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["phn_lock_pin"]["xpath"]))
                ).click()
                print("Clicked on Phone lock pin button")
                print("device_pin : ", device_pin)
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["passward_text_field"]["xpath"]))
                ).send_keys(device_pin)
                time.sleep(display_time)
                print("Entered device_pin : ", device_pin)
                try:
                    driver.hide_keyboard()
                except Exception as e:
                    print("Cannot hide keyboard : ", e)
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["next_btn"]["xpath"]))
                ).click()
                print("Clicked on NEXT button")
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["passward_text_field"]["xpath"]))
                ).send_keys(device_pin)
                print("Entered device_pin : ", device_pin)
                time.sleep(display_time)
                try:
                    driver.hide_keyboard()
                except Exception as e:
                    print("Cannot hide keyboard : ", e)
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["ok"]["xpath"]))
                ).click()
                print("Clicked on OK button")
            except Exception as e:
                raise AssertionError("Xpath not found")
        elif config["devices"][device]["model"].lower() in ["seattle", "olympia", "redmond", "kirkland"]:
            print("select device : ", config["devices"][device]["model"])
            raise AssertionError(config["devices"][device]["model"], " device doesn't have Phone lock feature")


def select_emergency_call_while_phone_lock(device):
    devices = device.split(",")
    for device in devices:
        driver = obj.device_store.get(alias=device)
        if config["devices"][device]["model"].lower() in ["san diego", "los angeles", "albany"]:
            try:
                print("select device : ", config["devices"][device]["model"])
                WebDriverWait(driver, 35).until(
                    EC.element_to_be_clickable((MobileBy.ID, device_settings_dict["phone_lock_icon"]["id"]))
                ).click()
                print("Clicked on phone un-lock")
                time.sleep(display_time)
                for attempt in range(3):
                    try:
                        print("attemp : ", attempt)
                        elem = driver.find_element_by_id(device_settings_dict["phone_unlock_emergency_call"]["id"])
                        if elem.is_displayed():
                            elem.click()
                            time.sleep(display_time)
                            print("Clicked on phone_unlock_emergency_call button")
                    except Exception as e:
                        break
                try:
                    xpath = driver.find_element_by_id(device_settings_dict["emergency_call_head"]["id"])
                    if xpath.is_displayed():
                        print("We are in lock emeergency call page")
                    time.sleep(display_time)
                except Exception as e:
                    raise AssertionError("We are not in Emergency call page")
            except Exception as e:
                raise AssertionError("Xpath not found")
        elif config["devices"][device]["model"].lower() == "phoenix":
            try:
                print("select device : ", config["devices"][device]["model"])
                time.sleep(35)
                subprocess.call(
                    "adb -s {} shell input keyevent 224".format(
                        config["devices"][device]["desired_caps"]["udid"].split(":")[0]
                    ),
                    shell=True,
                )
                xpath = WebDriverWait(driver, 35).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["swipe_up_to_unlock"]["xpath"]))
                )
                if xpath.is_displayed():
                    driver.swipe(640, 658, 640, 350)
                    print("swiped up to unlock")
                time.sleep(display_time)
                for attempt in range(3):
                    try:
                        print("attemp : ", attempt)
                        xpath = WebDriverWait(driver, 35).until(
                            EC.element_to_be_clickable(
                                (MobileBy.ID, device_settings_dict["phone_unlock_emergency_call"]["id1"])
                            )
                        )
                        if xpath.is_displayed():
                            xpath.click()
                            print("Clicked on phone_unlock_emergency_call button")
                            break
                    except Exception as e:
                        break
                try:
                    WebDriverWait(driver, 35).until(
                        EC.element_to_be_clickable((MobileBy.ID, device_settings_dict["emergency_call_head"]["id"]))
                    )
                    print("We are in lock emeergency call page")
                    time.sleep(display_time)
                except Exception as e:
                    print("Skipped the verification")
            except Exception as e:
                raise AssertionError("Xpath not found")

        elif config["devices"][device]["model"].lower() == "miami":
            try:
                print("select device : ", config["devices"][device]["model"])
                time.sleep(65)
                # wakeup keyevent
                subprocess.call(
                    "adb -s {} shell input keyevent 224".format(
                        config["devices"][device]["desired_caps"]["udid"].split(":")[0]
                    ),
                    shell=True,
                )
                driver.swipe(600, 700, 600, 200)
                print("swiped up to unlock")
                time.sleep(display_time)
                for attempt in range(3):
                    try:
                        print("attemp : ", attempt)
                        WebDriverWait(driver, 35).until(
                            EC.element_to_be_clickable(
                                (MobileBy.ID, device_settings_dict["phone_unlock_emergency_call"]["id1"])
                            )
                        ).click()
                        print("Clicked on phone_unlock_emergency_call button")
                        break
                    except Exception as e:
                        break
                try:
                    WebDriverWait(driver, 35).until(
                        EC.element_to_be_clickable((MobileBy.ID, device_settings_dict["emergency_call_head"]["id"]))
                    )
                    print("We are in lock emeergency call page")
                    time.sleep(display_time)
                except Exception as e:
                    print("Skipped the verification")
                    # raise AssertionError("We are not in Emergency call page")
            except Exception as e:
                print(e)
                raise AssertionError("Xpath not found")
        elif config["devices"][device]["model"].lower() in ["seattle", "olympia", "redmond", "kirkland"]:
            print("select device : ", config["devices"][device]["model"])
            raise AssertionError(config["devices"][device]["model"], " device doesn't have Phone lock feature")


def press_123456(device):
    subprocess.call(
        "adb -s {} shell input keyevent 8".format(config["devices"][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    subprocess.call(
        "adb -s {} shell input keyevent 9".format(config["devices"][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    subprocess.call(
        "adb -s {} shell input keyevent 10".format(config["devices"][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    subprocess.call(
        "adb -s {} shell input keyevent 11".format(config["devices"][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    subprocess.call(
        "adb -s {} shell input keyevent 12".format(config["devices"][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    subprocess.call(
        "adb -s {} shell input keyevent 13".format(config["devices"][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    time.sleep(display_time)


def unlock_phone(device, pin="123456"):
    devices = device.split(",")
    for device in devices:
        driver = obj.device_store.get(alias=device)
        if config["devices"][device]["model"].lower() in ["san diego", "los angeles", "albany"]:
            try:
                print("select device : ", config["devices"][device]["model"])
                xpath = driver.find_element_by_id(device_settings_dict["phone_lock_icon"]["id"])
                if xpath.is_displayed():
                    xpath.click()
                    print("Clicked on phone un-lock")
            except Exception as e:
                pass
        elif config["devices"][device]["model"].lower() == "phoenix":
            subprocess.call(
                "adb -s {} shell input keyevent 224".format(
                    config["devices"][device]["desired_caps"]["udid"].split(":")[0]
                ),
                shell=True,
            )
            xpath = WebDriverWait(driver, 35).until(
                EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["swipe_up_to_unlock"]["xpath"]))
            )
            if xpath.is_displayed():
                driver.swipe(640, 658, 640, 350)
                print("swiped up to unlock")
            time.sleep(display_time)
        elif config["devices"][device]["model"].lower() == "miami":
            print("select device : ", config["devices"][device]["model"])
            subprocess.call(
                "adb -s {} shell input keyevent 224".format(
                    config["devices"][device]["desired_caps"]["udid"].split(":")[0]
                ),
                shell=True,
            )
            xpath = WebDriverWait(driver, 35).until(
                EC.element_to_be_clickable((MobileBy.ID, device_settings_dict["lock_icon"]["id"]))
            )
            if xpath.is_displayed():
                driver.swipe(600, 700, 600, 200)
                print("swiped up to unlock")
        elif config["devices"][device]["model"].lower() in ["seattle", "olympia", "redmond", "kirkland"]:
            print("select device : ", config["devices"][device]["model"])
            raise AssertionError(config["devices"][device]["model"], " device doesn't have Phone lock feature")

        if pin == "123456":
            press_123456(device)
        else:
            raise AssertionError("Default password is not matching.. check again")

        if config["devices"][device]["model"].lower() in ["phoenix", "miami"]:
            subprocess.call(
                "adb -s {} shell input keyevent 66".format(
                    config["devices"][device]["desired_caps"]["udid"].split(":")[0]
                ),
                shell=True,
            )
            time.sleep(display_time)
        else:
            pass


def verify_device_is_unlocked(device):
    driver = obj.device_store.get(alias=device)
    try:
        time.sleep(display_time)
        xpath = WebDriverWait(driver, 35).until(
            EC.element_to_be_clickable((MobileBy.XPATH, navigation_dict["Navigation"]["xpath"]))
        )
        if xpath.is_displayed():
            time.sleep(action_time)
            print("Successfully we unlocked the device.")
    except Exception as e:
        raise AssertionError("Unable to unlocke the device")


def disable_lock_device(device, pin="123456"):
    devices = device.split(",")
    for device in devices:
        driver = obj.device_store.get(alias=device)
        time.sleep(display_time)
        settings_keywords.open_settings_page(device)
        if config["devices"][device]["model"].lower() == "los angeles":
            driver.swipe(100, 300, 100, 150)
        elif config["devices"][device]["model"].lower() == "miami":
            driver.swipe(300, 700, 300, 200)
        else:
            pass
        settings_keywords.click_device_settings(device)
        if pin == "123456":
            device_pin = "123456"
        else:
            device_pin = pin
        print("device_pin : ", device_pin)
        if config["devices"][device]["model"].lower() in ["san diego", "los angeles", "albany"]:
            try:
                print("select device : ", config["devices"][device]["model"])
                xpath = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["phone_lock"]["xpath"]))
                )
                if xpath.is_displayed():
                    xpath.click()
                    print("Clicked on phone lock tab")
                # time.sleep(display_time)
                try:
                    xpath = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((MobileBy.ID, device_settings_dict["phone_lock_icon"]["id"]))
                    )
                    if xpath.is_displayed():
                        unlock_phone(device)
                        print("Phone was locked")
                except Exception as e:
                    pass
                if config["devices"][device]["model"].lower() == "albany":
                    xpath = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable(
                            (MobileBy.XPATH, device_settings_dict["passward_text_field"]["xpath3"])
                        )
                    )
                    if xpath.is_displayed():
                        xpath.send_keys(device_pin)
                        print("Entered password to unlock")
                else:
                    xpath = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable(
                            (MobileBy.XPATH, device_settings_dict["passward_text_field"]["xpath1"])
                        )
                    )
                    if xpath.is_displayed():
                        xpath.send_keys(device_pin)
                        print("Entered password to unlock")
                try:
                    xpath = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((MobileBy.ID, device_settings_dict["phone_lock_icon"]["id"]))
                    )
                    if xpath.is_displayed():
                        unlock_phone(device)
                        print("Phone was locked")
                except Exception as e:
                    pass
                xpath = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["unlock_btn"]["xpath"]))
                )
                if xpath.is_displayed():
                    xpath.click()
                    print("Clicked on unlock button")
                xpath = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["lock_enable_toggle"]["xpath"]))
                )
                if xpath.is_displayed():
                    xpath.click()
                    print("Clicked on lock disable toggle button")
                time.sleep(display_time)
            except Exception as e:
                raise AssertionError("Xpath not found")
            if config["devices"][device]["model"].lower() == "los angeles":
                settings_keywords.device_setting_back(device)
            else:
                pass
        elif config["devices"][device]["model"].lower() == "phoenix":
            for attempt in range(3):
                try:
                    print("attempt : ", attempt)
                    WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["security_btn"]["xpath"]))
                    ).click()
                    print("Clicked on Security button")
                    break
                except Exception as e:
                    driver.swipe(400, 580, 400, 200)
            time.sleep(display_time)
            try:
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["Screen_lock"]["xpath"]))
                ).click()
                print("Clicked on Screen lock option")
                if device_pin == "123456":
                    press_123456(device)
                else:
                    raise AssertionError("Default password is not matching.. check again")
                subprocess.call(
                    "adb -s {} shell input keyevent 66".format(
                        config["devices"][device]["desired_caps"]["udid"].split(":")[0]
                    ),
                    shell=True,
                )
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["none_option"]["xpath"]))
                ).click()
                print("Clicked on None option")
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["yes_remove_btn"]["xpath"]))
                ).click()
                print("Clicked on YES REMOVE button")
                time.sleep(display_time)
                settings_keywords.device_setting_back(device)
                settings_keywords.device_setting_back(device)
                driver.swipe(400, 200, 400, 580)
                driver.swipe(400, 200, 400, 580)
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["Display_btn"]["xpath"]))
                ).click()
                print("Clicked on Display button")
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["sleep_option"]["xpath"]))
                ).click()
                print("Clicked on Sleep option")
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["10m_sleep_time"]["xpath"]))
                ).click()
                print("Selected 10 minute Sleep")
            except Exception as e:
                raise AssertionError("Xpath not found")
            settings_keywords.device_setting_back(device)
        elif config["devices"][device]["model"].lower() == "miami":
            for attempt in range(3):
                try:
                    print("attempt : ", attempt)
                    WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["phone_lock"]["xpath1"]))
                    ).click()
                    print("Clicked on phone lock tab")
                except Exception as e:
                    driver.swipe(100, 700, 100, 300)
            time.sleep(display_time)
            try:
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["lock_enable_toggle"]["xpath"]))
                ).click()
                print("Clicked on lock disable toggle button")
                if device_pin == "123456":
                    xpath = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable(
                            (MobileBy.XPATH, device_settings_dict["passward_text_field"]["xpath2"])
                        )
                    )
                    if xpath.is_displayed():
                        xpath.send_keys(device_pin)
                        print("Entered password to unlock")
                        WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["ok"]["xpath"]))
                        ).click()
                else:
                    raise AssertionError("Default password is not matching.. check again")
                time.sleep(display_time)
            except Exception as e:
                print(e)
                raise AssertionError("Xpath not found")
            settings_keywords.device_setting_back(device)
        elif config["devices"][device]["model"].lower() in ["seattle", "olympia", "redmond", "kirkland"]:
            print("select device : ", config["devices"][device]["model"])
            raise AssertionError(config["devices"][device]["model"], " device doesn't have Phone lock feature")


def access_device_settings_from_signin_page(device):
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((MobileBy.ID, device_settings_dict["fre_partner_settings"]["id"]))
        ).click()
        print("Clicked setting button on Sign-in page")
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["device_settings_text_view"]["xpath"]))
        )
        print("We are inside Device settings page from Sign-in page")
    except Exception as e:
        raise AssertionError("Signin page Xpath not found")
    settings_keywords.device_setting_back(device)


def verify_sign_in_to_make_an_emergency_call(device):
    common.wait_for_element(device, device_settings_dict, "sign_in_to_make_an_emergency_call")


def swipe_the_page_till_signout(device):
    driver = obj.device_store.get(alias=device)
    window_size = driver.get_window_size()
    print("Window size: ", window_size)
    height = window_size["height"]
    print("Window Height :", height)
    width = window_size["width"]
    print("Window Width :", width)
    if height > width:
        print("Swiping co-ordinates : ", width / 2, 4 * (height / 5), width / 2, 1 * (height / 5))
        driver.swipe(width / 2, 4 * (height / 5), width / 2, 1 * (height / 5))
    else:
        print("Swiping co-ordinates : ", width / 4, 4 * (height / 5), width / 4, height / 5)
        driver.swipe(width / 4, 4 * (height / 5), width / 4, height / 5)
    pass


def sign_out_console_oem(console):
    driver = obj.device_store.get(alias=console)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((MobileBy.ID, settings_dict["Device_Settings"]["id"]))
    ).click()
    print("Clicked on Device Settings Page")
    if config["consoles"][console]["model"].lower() in ["fresno"]:
        time.sleep(action_time)
        print("Inside device settings page")
        swipe_till_admin_sign_out(console)
        swipe_till_admin_sign_out(console)
        common.wait_for_and_click(console, tr_device_settings_dict, "teams_admin_settings1")
        common.wait_for_element(console, settings_dict, "admin_pass", "xpath1").send_keys(
            config["consoles"][console]["admin_password"]
        )
        print("Entered the admin password value")
        common.wait_for_and_click(console, settings_dict, "admin_enter")
        common.wait_for_and_click(console, settings_dict, "Sign_out")
        common.wait_for_and_click(console, sign_dict, "Sign_out_ok_button")

    elif config["consoles"][console]["model"].lower() in ["yakima", "sequim"]:
        common.wait_for_and_click(console, tr_device_settings_dict, "admin_settings", "xpath")
        time.sleep(display_time)
        e1 = driver.find_elements_by_xpath(tr_device_settings_dict["edit_box_field"]["xpath"])
        e1[0].send_keys(config["consoles"][console]["admin_username"])
        print("Admin Username entered")
        time.sleep(action_time)
        e1[1].send_keys(config["consoles"][console]["admin_password"])
        print("Admin password entered")
        common.wait_for_and_click(console, tr_device_settings_dict, "ok")
        time.sleep(display_time)
        swipe_till_admin_sign_out(console)
        common.wait_for_and_click(console, tr_device_settings_dict, "user_sign_out", "xpath")
        common.wait_for_and_click(console, tr_device_settings_dict, "ok")
        print("Sucessfully completed sign out from admin settings page")

    elif config["consoles"][console]["model"].lower() in ["dallas"]:
        common.wait_for_and_click(console, tr_device_settings_dict, "admin_settings", "xpath1")
        common.wait_for_element(console, device_settings_dict, "edit_text_number_pin").send_keys(
            config["consoles"][console]["admin_password"]
        )
        common.wait_for_and_click(console, device_settings_dict, "submit_button")
        common.wait_for_and_click(console, device_settings_dict, "system_settings")
        common.wait_for_and_click(console, tr_device_settings_dict, "service_provider")
        common.wait_for_and_click(console, tr_device_settings_dict, "teams_admin_settings1")
        common.wait_for_and_click(console, tr_device_settings_dict, "teams_sign_out")
        common.wait_for_and_click(console, device_settings_dict, "ok")
        print("Sign out Sucessfully from admin settings page")

    elif config["consoles"][console]["model"].lower() in ["lansing"]:
        swipe_till_admin_sign_out(console)
        common.wait_for_and_click(console, tr_device_settings_dict, "teams")
        common.wait_for_and_click(console, tr_device_settings_dict, "teams_admin_settings2", "xpath")
        ele = common.wait_for_element(
            console, tr_console_settings_dict, "admin_pass_field2", cond=EC.presence_of_all_elements_located
        )
        ele[-1].click()
        ele[-1].send_keys(config["consoles"][console]["admin_password"])
        common.wait_for_and_click(console, sign_dict, "Sign_in")
        common.wait_for_and_click(console, tr_device_settings_dict, "teams_sign_out")
        common.wait_for_and_click(console, device_settings_dict, "ok")

    elif config["consoles"][console]["model"].lower() == "pittsford":
        enabling_the_teams_admin_settings(console)
        print("Clicked on teams admin settings")
        common.wait_for_and_click(console, settings_dict, "Sign_out")
        common.wait_for_and_click(console, device_settings_dict, "ok")

    elif config["consoles"][console]["model"].lower() in ["denver"]:
        common.wait_for_and_click(console, tr_device_settings_dict, "admin")
        common.wait_for_element(console, tr_device_settings_dict, "username_filed").send_keys(
            config["consoles"][console]["admin_username"]
        )
        common.wait_for_element(console, tr_device_settings_dict, "password_field").send_keys(
            config["consoles"][console]["admin_password"]
        )
        common.wait_for_and_click(console, settings_dict, "Login_btn")
        common.wait_for_and_click(console, tr_device_settings_dict, "general")
        common.wait_for_and_click(console, tr_device_settings_dict, "service_provider")
        common.wait_for_and_click(console, tr_device_settings_dict, "access_settings")
        common.wait_for_and_click(console, settings_dict, "Sign_out")
        common.wait_for_and_click(console, device_settings_dict, "ok")

    elif config["consoles"][console]["model"].lower() == "athens":
        time.sleep(action_time)
        swipe_till_admin_sign_out(console)
        swipe_till_admin_sign_out(console)
        common.wait_for_and_click(console, tr_device_settings_dict, "teams_admin_settings1")
        e1 = common.wait_for_element(console, settings_dict, "admin_pass")
        e1.set_value(config["consoles"][console]["admin_password"])
        common.wait_for_and_click(console, tr_device_settings_dict, "admin_pass_enter")
        common.wait_for_and_click(console, settings_dict, "Sign_out")
        common.wait_for_and_click(console, device_settings_dict, "ok")

    elif config["consoles"][console]["model"].lower() == "tempe":
        common.wait_for_and_click(console, tr_device_settings_dict, "Device_administration")
        common.wait_for_and_click(console, tr_device_settings_dict, "device_administration_login")
        e1 = common.wait_for_element(console, settings_dict, "admin_pass")
        e1.set_value(config["consoles"][console]["admin_password"])
        common.wait_for_and_click(console, calendar_dict, "ok_button")
        swipe_till_admin_sign_out(console)
        swipe_till_admin_sign_out(console)
        common.wait_for_and_click(console, tr_device_settings_dict, "teams_admin_settings1")
        common.wait_for_and_click(console, tr_device_settings_dict, "teams_admin_settings_2")
        common.wait_for_and_click(console, settings_dict, "Sign_out")
        common.wait_for_and_click(console, device_settings_dict, "ok")

    elif config["consoles"][console]["model"].lower() == "wrangell":
        common.wait_for_and_click(console, tr_device_settings_dict, "login_to_admin")
        common.wait_for_and_click(console, tr_device_settings_dict, "admin_settings1")
        passcode = common.wait_for_element(console, tr_device_settings_dict, "admin_passcode")
        passcode.send_keys(config["consoles"][console]["admin_password"])
        common.wait_for_and_click(console, tr_device_settings_dict, "login_button")
        driver.swipe(606, 1176, 60, 176)
        common.wait_for_and_click(console, tr_device_settings_dict, "teams_admin_setting")
        common.wait_for_and_click(console, tr_device_settings_dict, "teams_admin_setting1")
        common.wait_for_and_click(console, tr_device_settings_dict, "teams_sign_out")
        common.wait_for_and_click(console, device_settings_dict, "ok")


def swipe_till_admin_sign_out(console):
    driver = obj.device_store.get(alias=console)
    window_size = driver.get_window_size()
    height = window_size["height"]
    width = window_size["width"]
    for i in range(0, 3):
        print(
            "Swiping co-ordinates : ",
            width / 4,
            4 * (height / 5),
            width / 4,
            height / 5,
        )
        driver.swipe(width / 4, 4 * (height / 5), width / 4, height / 5)
        time.sleep(action_time)
    pass


def check_device_capabilities(device):
    print(f"{device}: Check device capabilities")
    result_capabilities = firmware_validation_of_device(device, option="device_capabilities").split(",")
    print(f"{device}: Returned Teams capabilities: '{result_capabilities}'")

    expected_capabilities_list = (config["devices"][device]["teams_device_capabilities"]).lower()
    expected_capabilities = expected_capabilities_list.split(",")
    print(f"{device}: Expected Teams capabilities: '{expected_capabilities}'")

    if len(expected_capabilities) != len(result_capabilities):
        raise AssertionError(
            f"{device}: Length expected: '{len(expected_capabilities)}' is different from actual: '{len(result_capabilities)}'"
        )

    for arg in expected_capabilities:
        if arg not in result_capabilities:
            raise AssertionError(
                f"{device}: Capabilities: '{arg}' is not in actual capabilities: '{result_capabilities}'"
            )


def hd_user_checking_advance_setting_page(device):
    if config["devices"][device]["model"].lower() in ["queens", "long island"]:
        common.wait_for_and_click(device, device_settings_dict, "admin_settings")
        common.wait_for_element(device, settings_dict, "admin_passwd")
        subprocess.call(
            "adb -s {} shell input keyevent 67".format(config["devices"][device]["desired_caps"]["udid"].split(":")[0]),
            shell=True,
        )
        print("click close btn")
        settings_keywords.device_setting_back(device)
        common.click_if_present(device, calls_dict, "Call_Back_Button")

    elif config["devices"][device]["model"].lower() in ["riverside", "los angeles", "riverside_13"]:
        common.wait_for_element(device, settings_dict, "device_admin_pswd")
        settings_keywords.device_setting_back(device)
        common.click_if_present(device, calls_dict, "Call_Back_Button")


def verify_admin_pwd_field(device):
    calendar_keywords.opens_partner_settings_page(device)
    time.sleep(3)
    if config["devices"][device]["model"].lower() in ["tacoma"]:
        common.wait_for_and_click(device, settings_dict, "Admin_Only")
    common.wait_for_element(device, settings_dict, "device_admin_pswd")


def advance_calling_option_oem(device):
    print(f"device : {device}")
    driver = obj.device_store.get(alias=device)
    if config["devices"][device]["model"].lower() in ["queens", "long island"]:
        settings_keywords.swipe_till_end(device)
        common.wait_for_and_click(device, device_settings_dict, "admin_settings")
        common.wait_for_element(device, settings_dict, "admin_passwd").set_value(
            config["devices"][device]["admin_password"]
        )
        driver.execute_script("mobile: performEditorAction", {"action": "done"})
        common.wait_for_and_click(device, settings_dict, "Login_btn")
        time.sleep(action_time)
        settings_keywords.swipe_till_end(device)
        common.wait_for_and_click(device, settings_dict, "Calling")
        time.sleep(display_time)
        common.wait_for_and_click(device, device_settings_dict, "calling_button")

    elif config["devices"][device]["model"].lower() == "los angeles":
        ele = common.wait_for_element(device, settings_dict, "device_admin_pswd")
        ele.click()
        ele.set_value(config["devices"][device]["admin_password"])
        driver.execute_script("mobile: performEditorAction", {"action": "done"})
        swipe_till_sign_out(device)
        common.wait_for_and_click(device, settings_dict, "Calling")

    elif config["devices"][device]["model"].lower() in ["bakersfield", "santa cruz"]:
        swipe_till_sign_out(device)
        swipe_till_sign_out(device)
        common.wait_for_and_click(device, device_settings_dict, "teams_admin_setting_01")
        common.wait_for_and_click(device, settings_dict, "admin_pass")
        common.wait_for_element(device, settings_dict, "admin_pswd_option").set_value(
            config["devices"][device]["admin_password"]
        )
        common.hide_keyboard(device)
        common.wait_for_and_click(device, device_settings_dict, "enter_button")
        common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings_01_btn")
        common.wait_for_and_click(device, settings_dict, "Calling")

    elif config["devices"][device]["model"].lower() in ["olympia", "tacoma", "bothell", "kirkland"]:
        _max_attempts = 4
        for _attempt in range(_max_attempts):
            if common.is_element_present(device, settings_dict, "Admin_Only", "xpath"):
                common.wait_for_and_click(device, settings_dict, "Admin_Only", "xpath")
                break
            else:
                settings_keywords.swipe_till_end(device)
        common.wait_for_and_click(device, settings_dict, "admin_passwd", "xpath")
        common.wait_for_element(device, settings_dict, "admin_passwd", "xpath").send_keys(
            config["devices"][device]["admin_password"]
        )
        driver.execute_script("mobile: performEditorAction", {"action": "done"})
        time.sleep(3)
        for _attempt in range(_max_attempts):
            if common.is_element_present(device, settings_dict, "Calling"):
                common.wait_for_and_click(device, settings_dict, "Calling")
                common.wait_for_element(device, settings_dict, "call_forwarding")
                return
            else:
                settings_keywords.swipe_till_end(device)
        verify_calling_option_inside_cap_device(device)
        common.wait_for_and_click(device, settings_dict, "Calling")

    elif config["devices"][device]["model"].lower() == "riverside":
        common.wait_for_and_click(device, settings_dict, "device_admin_pswd")
        common.wait_for_element(device, settings_dict, "device_admin_pswd").set_value(
            config["devices"][device]["admin_password"]
        )
        driver.execute_script("mobile: performEditorAction", {"action": "done"})
        swipe_till_sign_out(device)
        swipe_till_sign_out(device)
        time.sleep(5)
        if common.is_element_present(device, settings_dict, "Calling"):
            common.wait_for_and_click(device, settings_dict, "Calling")
        else:
            common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings", "text")
            common.wait_for_and_click(device, settings_dict, "Calling")

    elif config["devices"][device]["model"].lower() in ["santa cruz_13", "bakersfield_13", "riverside_13"]:
        for i in range(3):
            if common.is_element_present(device, device_settings_dict, "teams_admin_settings", "text"):
                common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings", "text")
            else:
                swipe_till_sign_out(device)
        common.wait_for_element(device, panels_device_settings_dict, "pass_editbox").set_value(
            config["devices"][device]["admin_password"]
        )
        common.hide_keyboard(device)
        common.wait_for_and_click(device, device_settings_dict, "ok")
        common.wait_for_and_click(device, settings_dict, "Calling")

    elif config["devices"][device]["model"].lower() == "manhattan":
        common.wait_for_and_click(device, device_settings_dict, "admin_settings")
        element1 = common.wait_for_element(device, settings_dict, "admin_passwd")
        element1.set_value(config["devices"][device]["admin_password"])
        common.hide_keyboard(device)
        common.wait_for_and_click(device, settings_dict, "Login_btn")
        common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings")
        common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings_btn")
        common.wait_for_and_click(device, settings_dict, "Calling")

    elif config["devices"][device]["model"].lower() == "berkely":
        common.wait_for_and_click(device, settings_dict, "device_admin_pswd")
        common.wait_for_element(device, settings_dict, "device_admin_pswd").set_value(
            config["devices"][device]["admin_password"]
        )
        driver.execute_script("mobile: performEditorAction", {"action": "done"})
        common.hide_keyboard(device)
        settings_keywords.swipe_till_end(device)
        time.sleep(3)
        if common.is_element_present(device, settings_dict, "Calling"):
            common.wait_for_and_click(device, settings_dict, "Calling")
        else:
            common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings", "text")
            common.wait_for_and_click(device, settings_dict, "Calling")

    elif config["devices"][device]["model"].lower() == "malibu":
        _max_attempts = 4
        for _attempt in range(_max_attempts):
            if common.is_element_present(device, settings_dict, "device_admin_pswd"):
                common.wait_for_and_click(device, settings_dict, "device_admin_pswd")
                break
            else:
                driver.swipe(280, 180, 280, 75)
        common.wait_for_element(device, settings_dict, "device_admin_pswd").set_value(
            config["devices"][device]["admin_password"]
        )
        driver.execute_script("mobile: performEditorAction", {"action": "done"})
        for _attempt in range(_max_attempts):
            if common.is_element_present(device, settings_dict, "Calling"):
                common.wait_for_and_click(device, settings_dict, "Calling")
                break
            else:
                driver.swipe(280, 180, 280, 75)

    elif config["devices"][device]["model"].lower() == "gilbert":
        swipe_the_page_till_signout(device)
        swipe_the_page_till_signout(device)
        common.wait_for_and_click(device, settings_dict, "Device_administration")
        common.wait_for_and_click(device, settings_dict, "Device_login")
        common.wait_for_and_click(device, settings_dict, "admin_passwd", "xpath")
        common.wait_for_element(device, settings_dict, "admin_passwd", "xpath").set_value(
            config["devices"][device]["admin_password"]
        )
        common.wait_for_and_click(device, settings_dict, "Sign_out_ok", "xpath")
        swipe_the_page_till_signout(device)
        common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings")
        common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings_btn", "xpath1")
        common.wait_for_and_click(device, settings_dict, "Calling")

    elif config["devices"][device]["model"].lower() == "scottsdale":
        swipe_the_page_till_signout(device)
        swipe_the_page_till_signout(device)
        common.wait_for_and_click(device, settings_dict, "Device_administration")
        common.wait_for_and_click(device, settings_dict, "Device_login")
        common.wait_for_and_click(device, settings_dict, "admin_passwd", "xpath")
        common.wait_for_element(device, settings_dict, "admin_passwd", "xpath").set_value(
            config["devices"][device]["admin_password"]
        )
        common.wait_for_and_click(device, settings_dict, "Sign_out_ok", "xpath")
        common.wait_for_and_click(device, tr_device_settings_dict, "back_button")
        swipe_the_page_till_signout(device)
        swipe_the_page_till_signout(device)
        common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings")
        common.wait_for_and_click(device, settings_dict, "Calling")

    elif config["devices"][device]["model"].lower() == "redmond":
        common.wait_for_and_click(device, settings_dict, "Admin_Only")
        common.wait_for_element(device, settings_dict, "admin_passwd", "xpath").set_value(
            config["devices"][device]["admin_password"]
        )
        driver.execute_script("mobile: performEditorAction", {"action": "done"})
        settings_keywords.swipe_till_end(device)
        common.wait_for_and_click(device, settings_dict, "Calling")

    elif config["devices"][device]["model"].lower() == "malibu_13":
        for i in range(6):
            if common.is_element_present(device, device_settings_dict, "teams_admin_settings", "text"):
                common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings", "text")
            else:
                driver.swipe(280, 180, 280, 75)
        common.wait_for_element(device, panels_device_settings_dict, "pass_editbox").set_value(
            config["devices"][device]["admin_password"]
        )
        common.hide_keyboard(device)
        common.wait_for_and_click(device, device_settings_dict, "ok")
        common.wait_for_and_click(device, settings_dict, "Calling")

    common.wait_for_element(device, settings_dict, "call_forwarding")


def navigate_to_calling_option_for_conf(device):
    driver = obj.device_store.get(alias=device)
    settings_keywords.open_settings_page(device)
    common.wait_for_and_click(device, settings_dict, "Device_Settings")
    if config["devices"][device]["model"].lower() == "manhattan":
        common.wait_for_and_click(device, device_settings_dict, "admin_settings")
        element1 = common.wait_for_element(device, settings_dict, "admin_passwd")
        element1.set_value(config["devices"][device]["admin_password"])
        common.hide_keyboard(device)
        common.wait_for_and_click(device, settings_dict, "Login_btn")
        common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings")
        common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings_btn")
        common.wait_for_and_click(device, settings_dict, "Calling")
        common.wait_for_element(device, settings_dict, "call_forwarding")

    elif config["devices"][device]["model"].lower() == "tacoma":
        common.wait_for_and_click(device, settings_dict, "Admin_Only")
        common.wait_for_element(device, settings_dict, "admin_passwd", "xpath").set_value(
            config["devices"][device]["admin_password"]
        )
        driver.execute_script("mobile: performEditorAction", {"action": "done"})
        common.wait_for_and_click(device, settings_dict, "Calling")
        common.wait_for_element(device, settings_dict, "call_forwarding")

    elif config["devices"][device]["model"].lower() in ["sunnyvale", "berkely"]:
        common.wait_for_and_click(device, settings_dict, "device_admin_pswd")
        common.wait_for_element(device, settings_dict, "device_admin_pswd").set_value(
            config["devices"][device]["admin_password"]
        )
        driver.execute_script("mobile: performEditorAction", {"action": "done"})
        common.hide_keyboard(device)
        settings_keywords.swipe_till_end(device)
        common.wait_for_and_click(device, settings_dict, "Calling")
        common.wait_for_element(device, settings_dict, "call_forwarding")


def navigate_to_user_survey_for_conf(device):
    print(f"device : {device}")
    navigate_to_calling_option_for_conf(device)
    time.sleep(action_times)
    calendar_keywords.scroll_only_once(device)
    common.wait_for_element(device, device_settings_dict, "dismiss_rate_my_call")


def verify_dismiss_rate_my_call_toggle_state(device, toggle):
    if toggle.lower() not in ["on", "off"]:
        raise AssertionError(f"Illegal value for 'toggle': '{toggle}'")
    calendar_keywords.scroll_only_once(device)
    if toggle.lower() == "on":
        common.wait_for_element(device, device_settings_dict, "dismiss_rate_toggle_on")
    elif toggle.lower() == "off":
        common.wait_for_element(device, device_settings_dict, "dismiss_rate_toggle_off")


def click_on_dismiss_rate_my_call_option_toggle(device):
    common.wait_for_and_click(device, device_settings_dict, "dismiss_rate_toggle_btn")


def enable_dismiss_rate_my_call_option(device):
    print(f"device : {device}")
    calendar_keywords.scroll_only_once(device)
    if not common.is_element_present(device, device_settings_dict, "dismiss_rate_toggle_on"):
        common.wait_for_and_click(device, device_settings_dict, "dismiss_rate_toggle_btn")


def come_back_to_home_screen_from_calling_settings_for_conf(device):
    if config["devices"][device]["model"].lower() == "manhattan":
        settings_keywords.device_setting_back(device)
        settings_keywords.device_setting_back(device)
        settings_keywords.device_setting_back(device)
    else:
        settings_keywords.device_setting_back(device)
    call_keywords.come_back_to_home_screen(device)


def swipe_right_side_screen_till_bottom(device):
    driver = obj.device_store.get(alias=device)
    window_size = driver.get_window_size()
    print("Window size: ", window_size)
    height = window_size["height"]
    print("Window Height :", height)
    width = window_size["width"]
    print("Window Width :", width)
    try:
        if height > width:
            print("Swiping co-ordinates : ", width / 2, 4 * (height / 5), width / 2, height / 5)
            driver.swipe(width / 2, 4 * (height / 5), width / 2, height / 5)
        else:
            print("Swiping co-ordinates : ", width / 4, 4 * (height / 5), width / 4, height / 5)
            driver.swipe(width / 5, 4 * (height / 5), width / 5, height / 5)
    except InvalidElementStateException:
        common.sleep_with_msg(device, 5, "Trapped InvalidElementStateException, retrying...")
        if height > width:
            driver.swipe(width / 2, 4 * (height / 5), width / 2, height / 5)
        else:
            driver.swipe(width / 5, 4 * (height / 5), width / 5, height / 5)
        print(f"{device}: Retry Success!")


def swipe_till_admin_settings(console):
    driver = obj.device_store.get(alias=console)
    window_size = driver.get_window_size()
    height = window_size["height"]
    width = window_size["width"]
    print("Swiping co-ordinates : ", width / 4, 4 * (height / 5), width / 4, height / 5)
    driver.swipe(width / 4, 4 * (height / 5), width / 4, height / 5)


def enabling_the_teams_admin_settings(device):
    if "console" in device:
        udid_ = config["consoles"][device]["desired_caps"]["udid"]
    else:
        udid_ = config["devices"][device]["desired_caps"]["udid"]
    time.sleep(3)
    if not common.click_if_present(device, tr_device_settings_dict, "teams_admin_settings1"):
        if "console" not in device:
            call_keywords.device_right_corner_click(device)
        else:
            subprocess.run(
                "adb -s " + udid_ + " shell input keyevent KEYCODE_BACK",
                stdout=subprocess.PIPE,
                shell=True,
            )
        subprocess.run(
            "adb -s " + udid_ + " shell settings put secure show_hidden_menu 1", stdout=subprocess.PIPE, shell=True
        )
        common.wait_for_and_click(device, settings_dict, "Device_Settings")
        common.wait_for_and_click(device, tr_device_settings_dict, "teams_admin_settings1")


def verify_calling_option_inside_cap_device(device):
    driver = obj.device_store.get(alias=device)
    device_control.clear_app_caches(
        device, config, [config["companyPortal_Package"], config["common_desired_caps"]["appPackage"]]
    )
    settings_keywords.device_setting_back(device)
    SignInOut.sign_in_method(device, user="cap_search_enabled")
    settings_keywords.open_settings_page(device)
    settings_keywords.swipe_till_end(device)
    settings_keywords.swipe_till_end(device)
    common.wait_for_and_click(device, settings_dict, "Device_Settings")
    common.wait_for_and_click(device, settings_dict, "Admin_Only", "xpath")
    common.wait_for_element(device, settings_dict, "admin_passwd", "xpath").set_value(
        config["devices"][device]["admin_password"]
    )
    driver.execute_script("mobile: performEditorAction", {"action": "done"})
    common.wait_for_element(device, settings_dict, "Calling")


def navigate_to_calling_option_for_CAP_policy_user_for_audio_phones(device):
    settings_keywords.open_settings_page(device)
    swipe_the_page_till_signout(device)
    driver = obj.device_store.get(alias=device)
    common.wait_for_and_click(device, settings_dict, "Device_Settings")
    if config["devices"][device]["model"].lower() in ["queens", "long island", "manhattan"]:
        settings_keywords.swipe_till_end(device)
        common.wait_for_and_click(device, device_settings_dict, "admin_settings")
        common.wait_for_element(device, settings_dict, "admin_passwd").set_value(
            config["devices"][device]["admin_password"]
        )
        driver.execute_script("mobile: performEditorAction", {"action": "done"})
        common.wait_for_and_click(device, settings_dict, "Login_btn")
        settings_keywords.swipe_till_end(device)
        settings_keywords.swipe_till_end(device)
        common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings")
        common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings_btn")

    elif config["devices"][device]["model"].lower() in ["gilbert", "scottsdale"]:
        swipe_the_page_till_signout(device)
        swipe_the_page_till_signout(device)
        common.wait_for_and_click(device, settings_dict, "Device_administration")
        common.wait_for_and_click(device, settings_dict, "Device_login")
        common.wait_for_and_click(device, settings_dict, "admin_passwd", "xpath")
        common.wait_for_element(device, settings_dict, "admin_passwd", "xpath").set_value(
            config["devices"][device]["admin_password"]
        )
        common.hide_keyboard(device)
        common.wait_for_and_click(device, settings_dict, "Sign_out_ok", "xpath")
        calendar_keywords.scroll_only_once(device)
        common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings")
        common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings_btn", "xpath")

    elif config["devices"][device]["model"].lower() in ["seattle", "olympia", "tacoma", "kirkland"]:
        common.wait_for_and_click(device, settings_dict, "Admin_Only", "xpath")
        common.wait_for_and_click(device, settings_dict, "admin_passwd", "xpath")
        common.wait_for_element(device, settings_dict, "admin_passwd", "xpath").set_value(
            config["devices"][device]["admin_password"]
        )
        common.hide_keyboard(device)
        common.wait_for_and_click(device, settings_dict, "done")

    elif config["devices"][device]["model"].lower() in ["bakersfield", "santa cruz"]:
        swipe_the_page_till_signout(device)
        swipe_the_page_till_signout(device)
        common.wait_for_and_click(device, device_settings_dict, "sacramento_sign_out")
        common.wait_for_and_click(device, settings_dict, "admin_pswd_option")
        common.wait_for_element(device, settings_dict, "admin_pswd_option").set_value(
            config["devices"][device]["admin_password"]
        )
        common.wait_for_and_click(device, settings_dict, "admin_enter")

    elif config["devices"][device]["model"].lower() in ["santa cruz_13", "bakersfield_13", "riverside_13"]:
        for i in range(3):
            if common.is_element_present(device, device_settings_dict, "teams_admin_settings", "text"):
                common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings", "text")
            else:
                swipe_till_sign_out(device)
        common.wait_for_element(device, panels_device_settings_dict, "pass_editbox").set_value(
            config["devices"][device]["admin_password"]
        )
        common.hide_keyboard(device)
        common.wait_for_and_click(device, device_settings_dict, "ok")
        common.wait_for_and_click(device, settings_dict, "Sign_out", "id")
        common.wait_for_and_click(device, sign_dict, "Sign_out_ok_button")

    elif config["devices"][device]["model"].lower() == "riverside":
        common.wait_for_and_click(device, settings_dict, "device_admin_pswd")
        common.wait_for_element(device, settings_dict, "device_admin_pswd").set_value(
            config["devices"][device]["admin_password"]
        )
        driver.execute_script("mobile: performEditorAction", {"action": "done"})
        swipe_till_sign_out(device)
        swipe_till_sign_out(device)
        time.sleep(5)
        if common.is_element_present(device, settings_dict, "Calling"):
            common.wait_for_element(device, settings_dict, "Calling")
        else:
            common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings", "text")
            common.wait_for_element(device, settings_dict, "Calling")

    time.sleep(action_time)
    common.wait_for_and_click(device, settings_dict, "Calling")
    time.sleep(display_time)
    common.wait_for_element(device, calls_dict, "Header", "id")
    common.wait_for_element(device, settings_dict, "call_forwarding")


def enable_E2EE_option_inside_calling_option(device):
    common.run_parallel(device, enable_E2EE_toggle)


def enable_E2EE_toggle(device):
    if not common.is_element_present(device, device_settings_dict, "e2ee_calls"):
        navigate_to_E2EE_option_inside_calling_option(device)

    elem = common.wait_for_element(device, device_settings_dict, "e2ee_calls", "id1")
    temp = elem.get_attribute("checked")
    if temp == "false":
        common.wait_for_and_click(device, device_settings_dict, "e2ee_calls", "id1")
        elem1 = common.wait_for_element(device, device_settings_dict, "e2ee_calls", "id1")
        temp1 = elem1.get_attribute("checked")
        if temp1 != "true":
            raise AssertionError(f"{device}:E2EE toggle is not enabled")


def disable_E2EE_option_inside_calling_option(device):
    common.run_parallel(device, disable_E2EE_toggle)


def disable_E2EE_toggle(device):
    if not common.is_element_present(device, device_settings_dict, "e2ee_calls"):
        navigate_to_E2EE_option_inside_calling_option(device)

    elem = common.wait_for_element(device, device_settings_dict, "e2ee_calls", "id1")
    temp = elem.get_attribute("checked")
    if temp == "true":
        common.wait_for_and_click(device, device_settings_dict, "e2ee_calls", "id1")
        elem1 = common.wait_for_element(device, device_settings_dict, "e2ee_calls", "id1")
        temp1 = elem1.get_attribute("checked")
        if temp1 != "false":
            raise AssertionError(f"{device}:E2EE toggle is not disabled")


def verify_E2EE_option_inside_calling_option(device):
    devices = device.split(",")
    for device in devices:
        navigate_to_E2EE_option_inside_calling_option(device)


def navigate_to_learn_more_link_under_E2EE_calls(device):
    devices = device.split(",")
    for device in devices:
        navigate_to_E2EE_option_inside_calling_option(device)
        call_views_keywords.go_back_to_previous_page(device)


def navigate_to_E2EE_option_inside_calling_option(device):
    settings_keywords.open_settings_page(device)
    time.sleep(display_time)
    if not common.click_if_present(device, settings_dict, "Calling"):
        common.wait_for_and_click(device, settings_dict, "Device_Settings")
        advance_calling_option_oem(device)
    time.sleep(display_time)
    max_attempts = 5
    for _attempt in range(max_attempts):
        if common.is_element_present(device, device_settings_dict, "e2ee_link"):
            common.wait_for_element(device, device_settings_dict, "e2ee_calls")
            break
        else:
            settings_keywords.swipe_till_end(device)


def verify_status_of_device_firmware_for_production(device):
    print(f"{device}: Check status of Firmware for production")
    fw_build_status = firmware_validation_of_device(device, option="fw_production_status")
    print(f"{device}: Status of device firmware for production :{fw_build_status} ")
    expected_status = ["release-keys", "prod-keys", "test-keys", "dev-keys"]
    res = any(ele in fw_build_status for ele in expected_status)
    if not res:
        raise AssertionError(
            f"{device}: Actual status of firmware for production: {fw_build_status} is not matching as per expected status."
        )


def firmware_validation_of_device(device, option):
    if option == "firmware_version":
        if config["devices"][device]["oem"].lower() in ["texas"]:
            return common.get_adb_output(device, " shell getprop persist.logi.fwupd.manifest-current-collab-ver")
        else:
            return common.get_adb_output(device, " shell getprop build.firmware.version")
    elif option == "device_type":
        return common.get_adb_output(device, " shell settings get secure teams_device_type").lower()
    elif option == "apk_version":
        return common.get_adb_output(
            device, " shell dumpsys package com.microsoft.skype.teams.ipphone | findstr versionName"
        ).strip("\r\n")
    elif option == "fw_production_status":
        return common.get_adb_output(device, " shell getprop ro.build.fingerprint")
    elif option == "screen_resolution":
        return common.get_adb_output(device, " shell wm size")
    elif option == "device_capabilities":
        return common.get_adb_output(device, " shell settings get secure teams_device_capabilities")
    elif option == "partner_agent_version":
        return common.get_adb_output(
            device, " shell dumpsys package com.microsoft.teams.ipphone.partner.agent | findstr versionName"
        ).strip("\r\n")
    elif option == "company_portal_version":
        return common.get_adb_output(
            device, " shell dumpsys package com.microsoft.windowsintune.companyportal | findstr versionName"
        ).strip("\r\n")
    raise AssertionError(f"{device}: Illegal value for 'option': {option}")


def reboot_phones(device):
    settings_keywords.open_settings_page(device)
    settings_keywords.click_device_settings(device)
    _model = config["devices"][device]["model"].lower()

    if _model in ["olympia", "seattle", "redmond", "kirkland", "tacoma"]:
        common.wait_for_element(device, device_settings_dict, "phone_settings")
        common.wait_for_and_click(device, device_settings_dict, "reboot_phones")
        common.wait_for_and_click(device, sign_dict, "continue")
    elif _model == "scottsdale":
        common.wait_for_element(device, navigation_dict, "settings")
        settings_keywords.swipe_till_end(device)
        common.wait_for_and_click(device, device_settings_dict, "reboot_phones")
        common.wait_for_and_click(device, device_settings_dict, "reboot_v1")
        common.wait_for_and_click(device, device_settings_dict, "ok")
    elif _model in ["santa cruz", "bakersfield", "riverside", "berkely"]:
        common.wait_for_element(device, device_settings_dict, "device_settings_text_view")
        tr_calendar_keywords.swipe_the_middle_page_to_end(device)
        common.wait_for_and_click(device, device_settings_dict, "reboot_phones")
        common.wait_for_and_click(device, device_settings_dict, "reboot_phones")
        common.wait_for_and_click(device, device_settings_dict, "ok")
    elif _model == "gilbert":
        common.wait_for_element(device, navigation_dict, "settings")
        settings_keywords.swipe_till_end(device)
        common.wait_for_and_click(device, device_settings_dict, "reboot_phones")
        common.wait_for_and_click(device, device_settings_dict, "reboot_v1")
        common.wait_for_and_click(device, device_settings_dict, "ok")
    else:
        raise AssertionError(f"{device}: No validation specified for device model '{_model}'")
