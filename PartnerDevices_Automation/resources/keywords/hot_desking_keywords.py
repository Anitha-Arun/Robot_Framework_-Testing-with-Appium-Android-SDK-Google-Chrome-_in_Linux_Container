import call_keywords
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib3.exceptions import ProtocolError
import common
from Selectors import load_json_file
from initiate_driver import obj_dev as obj
from initiate_driver import config
import time
import settings_keywords
from subprocess import CalledProcessError
import subprocess
import device_settings_keywords
import panel_meetings_device_settings_keywords

display_time = 2
action_time = 3

device_settings_dict = load_json_file("resources/Page_objects/Device_settings.json")
navigation_dict = load_json_file("resources/Page_objects/Navigation.json")
sign_dict = load_json_file("resources/Page_objects/Signin.json")
hot_desk_dict = load_json_file("resources/Page_objects/Hot_desk.json")
calls_dict = load_json_file("resources/Page_objects/Calls.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")
home_screen_dict = load_json_file("resources/Page_objects/Home_screen.json")
calendar_dict = load_json_file("resources/Page_objects/Calendar.json")


def verify_settings_screen_from_hot_desk_page(device):
    common.wait_for_element(device, device_settings_dict, "fre_partner_settings")


def hot_desking_signin(device, hot_desk_account):
    max_attempts = 15
    for attempt in range(max_attempts):
        if common.click_if_present(device, navigation_dict, "Navigation") or common.click_if_present(
            device, calls_dict, "user_profile_picture"
        ):
            print(f"{device}: Opened hamburger menu")
            break
        if attempt == max_attempts - 1:
            raise AssertionError(f"{device} Couldn't open the hamburger menu")
    common.wait_for_and_click(device, hot_desk_dict, "hot_desk_btn")
    verify_settings_screen_from_hot_desk_page(device)
    username, password, hd_user, account = common.get_credentials(hot_desk_account)
    common.wait_for_element(device, sign_dict, "Username").send_keys(username)
    common.hide_keyboard(device)
    common.wait_for_and_click(device, sign_dict, "Sign_in_button")
    common.hide_keyboard(device)

    # Manually tapping on the password field on devices where password screen is not visible
    if config["devices"][device]["model"].lower() in [
        "olympia",
        "seattle",
        "tacoma",
        "redmond",
        "manhattan",
        "kirkland",
    ]:
        common.sleep_with_msg(device, 30, "Waiting for the password entry screen to appear")
        udid_ = config["devices"][device]["desired_caps"]["udid"]
        try:
            if config["devices"][device]["model"].lower() in ["olympia", "seattle", "kirkland"]:
                subprocess.run("adb -s " + udid_ + " shell input tap 100 320", stdout=subprocess.PIPE, shell=True)
            elif config["devices"][device]["model"].lower() == "redmond":
                subprocess.run("adb -s " + udid_ + " shell input tap 400 330", stdout=subprocess.PIPE, shell=True)
            elif config["devices"][device]["model"].lower() == "manhattan":
                subprocess.run("adb -s " + udid_ + " shell input tap 600 430", stdout=subprocess.PIPE, shell=True)
            common.sleep_with_msg(device, 7, f"Waiting to enter password on {device}")
            cmd = "adb -s " + udid_ + " shell input text " + password
            subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
            subprocess.run(
                "adb -s " + udid_ + " shell input keyevent KEYCODE_ENTER",
                stdout=subprocess.PIPE,
                shell=True,
            )
            print(f"{device}: Manually entered the user password")
        except CalledProcessError as failure:
            print(f"{device}: Failed ({failure.returncode}) manual input of the user password: {failure.output}")
            raise AssertionError("Manual password entry failed.")
    else:
        common.wait_for_element(device, sign_dict, "Password").send_keys(password)
        print(f"{device}: entered the user password")
        time.sleep(display_time)
        if not common.click_if_present(device, sign_dict, "Sign_in"):
            common.wait_for_and_click(device, sign_dict, "signin_button")

    # Handling the hot desk sign-in error (Commenting as work-around might be required in future)
    # try:
    #     if config["devices"][device]["model"].lower() in ["los angeles", "san diego", "sacramento"]:
    #         elem = WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
    #             (MobileBy.XPATH, hot_desk_dict["hot_desk_error_popup_ok"]["xpath"])))
    #         if elem.is_displayed():
    #             WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
    #                 (MobileBy.XPATH, hot_desk_dict["hot_desk_error_popup_ok"]["xpath"]))).click()
    #             WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    #                 (MobileBy.ID, hot_desk_dict["hot_desk_error_signin"]["id"]))).click()
    #             print("Handled the error during hotesk")
    #         else:
    #             pass
    #     try:
    #         search_input = WebDriverWait(driver, 60).until(
    #             EC.element_to_be_clickable((MobileBy.XPATH, sign_dict["Password"]["xpath"]))
    #         )
    #         if search_input.is_displayed():
    #             search_input.set_value(password)
    #             driver.hide_keyboard()
    #             WebDriverWait(driver, 60).until(
    #                 EC.element_to_be_clickable((MobileBy.XPATH, sign_dict["Sign_in"]["xpath"]))).click()
    #         else:
    #             pass
    #     except:
    #         print("No need to re-enter the password")
    #         pass
    # except:
    #     print("No need to handle hot desk sign-in failure")
    #     pass

    _max_loop = 10
    for attempt in range(_max_loop):
        common.sleep_with_msg(device, 10, "Waiting for sign-in to complete")
        common.click_if_present(device, sign_dict, "Gotit_button")
        if common.is_element_present(device, calls_dict, "calls_tab"):
            print(f"{device}: Calls tab is visible, sign-in successful on attempt {attempt} of {_max_loop - 1}")
            break
        if common.is_element_present(device, calls_dict, "user_profile_picture"):
            print(f"{device}: Home-screen is displayed, sign-in is successful on attempt {attempt} of {_max_loop-1}")
            break
        if attempt == _max_loop - 1:
            raise AssertionError(f"{device}: Hot desk user failed to sign-in")
    common.sleep_with_msg(device, 10, "Sign in complete, allow notifications arrival")

    # SignInOut.check_version_disable_home_app(device)
    common.wait_for_element(device, calls_dict, "calls_tab")
    common.click_if_present(device, home_screen_dict, "home_bar_icon")
    hd_displayname = config["devices"][hd_user][account]["displayname"]
    common.wait_for_and_click(device, navigation_dict, "Navigation")
    signed_in_user_name = common.wait_for_element(device, navigation_dict, "user_name").text
    if hd_displayname != signed_in_user_name:
        raise AssertionError(
            f"HD user name displayed: {signed_in_user_name} doesn't match the expected name: {hd_displayname}"
        )
    common.wait_for_and_click(device, settings_dict, "user_displayname")
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")
    time.sleep(action_time)


def verify_hot_desking_mode(device):
    print("device :", device)
    time.sleep(5)
    common.click_if_present(device, home_screen_dict, "home_bar_icon")
    common.wait_for_and_click(device, navigation_dict, "Navigation")
    common.wait_for_element(device, hot_desk_dict, "stop_hot_desking")
    time.sleep(action_time)
    hd_timeout = common.wait_for_element(device, hot_desk_dict, "hot_desking_timeout").text
    print("Hot Desk timeout : ", hd_timeout)
    print("We are in Hot Desking Mode")
    # for audio phones and conferance landscape
    common.wait_for_and_click(device, settings_dict, "user_displayname")
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")
    time.sleep(action_time)
    # for cap user
    if not common.is_element_present(device, home_screen_dict, "call_tab"):
        close_the_hamburger_menu(device)


def close_the_hamburger_menu(device):
    if common.is_element_present(device, home_screen_dict, "hamburger_menu_container"):
        common.tap_outside_the_popup(
            device, common.wait_for_element(device, home_screen_dict, "hamburger_menu_container")
        )
    common.wait_while_present(device, home_screen_dict, "hamburger_menu_container")


def verify_hotdesking_automatic_timeout_warning(device):
    common.wait_for_and_click(device, hot_desk_dict, "continue_button")
    print("btn xpath")
    print("HD timeout pop-up displayed")
    print("HD timeout WARNING")


def end_hot_desk(device):
    print("device :", device)
    if config["devices"][device]["model"].lower() in ["tacoma", "berkely"]:
        return
    call_keywords.come_back_to_home_screen(device)
    common.click_if_present(device, hot_desk_dict, "continue_button")
    common.wait_for_and_click(device, navigation_dict, "Navigation")
    if common.click_if_element_appears(device, hot_desk_dict, "stop_hot_desking"):
        common.wait_for_and_click(device, hot_desk_dict, "end_button")
    else:
        common.wait_for_element(device, hot_desk_dict, "hot_desk_btn")
        common.wait_for_and_click(device, settings_dict, "user_displayname")
        common.wait_for_and_click(device, calls_dict, "Call_Back_Button")
    if common.is_conf(device):
        common.wait_for_element(device, home_screen_dict, "more_option")
        return
    common.click_if_element_appears(device, sign_dict, "Gotit_button", max_attempts=30)
    common.wait_for_element(device, navigation_dict, "Navigation")


def validate_username_after_signed_out_from_hot_desking(device):
    displayname = common.device_displayname(device)
    if ":" in device:
        device = device.split(":")[0]
    print("displayname : ", displayname)
    common.sleep_with_msg(device, 5, "allow time to return back to host user")
    common.click_if_present(device, home_screen_dict, "home_bar_icon")
    common.wait_for_and_click(device, navigation_dict, "Navigation", wait_attempts=60)
    time.sleep(action_time)
    print("Clicked on Navigation button")
    signed_in_user_name = common.wait_for_element(device, navigation_dict, "user_name").text
    print("signed_in_user_name : ", signed_in_user_name)
    if displayname != signed_in_user_name:
        raise AssertionError(f"{device}: Unable to stop Hot Desking")
    common.wait_for_and_click(device, settings_dict, "user_displayname")
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")


def verify_settings_page_in_HD_mode(device):
    print("device :", device)
    settings_keywords.open_settings_page(device)
    common.wait_for_element(device, settings_dict, "manage_delegates")
    common.wait_for_element(device, settings_dict, "Profile")
    common.wait_for_element(device, settings_dict, "Calling")
    common.wait_for_element(device, calendar_dict, "meetings_button")
    settings_keywords.swipe_till_end(device)
    common.wait_for_element(device, settings_dict, "auto_restart")
    common.wait_for_element(device, navigation_dict, "what's_new")
    common.wait_for_element(device, settings_dict, "Help")
    common.wait_for_element(device, settings_dict, "about_btn")
    common.wait_for_element(device, settings_dict, "Sign_out")
    settings_keywords.swipe_till_end(device)
    common.wait_for_element(device, settings_dict, "Device_Settings")


def verify_device_settings_page_for_ztp_panel(device):
    print("device : ", device)
    panel_meetings_device_settings_keywords.verify_device_settings_option_in_panel(device)
    common.wait_for_element(device, settings_dict, "Device_Settings")
    print("We are in Device Settings page")
    settings_keywords.device_setting_back(device)


def validate_no_hot_desking_option_for_hd_user(device):
    print("device :", device)
    common.wait_for_and_click(device, navigation_dict, "Navigation")
    time.sleep(action_time)
    hd_timeout = common.wait_for_element(device, hot_desk_dict, "hot_desking_timeout").text
    print("Hot Desk timeout : ", hd_timeout)
    print("'Start Hot Desk' button not visible. 'Hot Desk timing visible'")


def verify_hd_user_details(device, hd_user):
    common.wait_for_and_click(device, navigation_dict, "Navigation")
    time.sleep(action_time)
    hd_user_displayname = config["devices"][hd_user]["user"]["displayname"]
    signed_in_user_name = common.wait_for_element(device, navigation_dict, "user_name").text
    print("signed_in_user_name : ", signed_in_user_name)
    time.sleep(display_time)
    if hd_user_displayname != signed_in_user_name:
        raise AssertionError("Unable to see Hot Desk User Details")
    common.wait_for_and_click(device, settings_dict, "user_displayname")
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")


def validate_hd_signin_with_invalid_user(device):
    print("device : ", device)
    common.wait_for_and_click(device, navigation_dict, "Navigation")
    common.wait_for_and_click(device, hot_desk_dict, "hot_desk_btn")
    invalid_username = config["hot_desk"]["invalid_username"]
    print("Invalid Username: ", invalid_username)
    common.hide_keyboard(device)
    search_input = common.wait_for_element(device, sign_dict, "Username")
    search_input.send_keys(invalid_username)
    common.hide_keyboard(device)
    time.sleep(display_time)
    common.wait_for_and_click(device, sign_dict, "Sign_in_button")
    time.sleep(2)
    common.hide_keyboard(device)
    common.wait_for_element(device, sign_dict, "sign_in_error")
    time.sleep(action_time)
    print("'Please enter a valid sign-in address' error visible")
    # settings_keywords.device_setting_back(device)


def validate_hd_signin_with_host_user(device):
    print("device : ", device)
    account = "user"
    if ":" in device:
        user = device.split(":")[1]
        print("User account : ", user)
        if user.lower() == "cap_search_enabled":
            account = "cap_search_enabled"
    print("Account :", account)
    device = device.split(":")[0]
    host_username = config["devices"][device][account]["username"]
    host_displayname = config["devices"][device][account]["displayname"]
    print("host_username : ", host_username)
    common.wait_for_and_click(device, navigation_dict, "Navigation")
    common.wait_for_and_click(device, hot_desk_dict, "hot_desk_btn")
    search_input = common.wait_for_element(device, sign_dict, "Username")
    search_input.send_keys(host_username)
    common.hide_keyboard(device)
    time.sleep(display_time)
    common.wait_for_and_click(device, sign_dict, "Sign_in_button")
    time.sleep(2)
    common.hide_keyboard(device)
    if account not in ["cap_search_enabled"]:
        common.wait_for_element(device, home_screen_dict, "calendar_tab")

    common.wait_for_and_click(device, navigation_dict, "Navigation")
    signed_in_user_name = common.wait_for_element(device, navigation_dict, "user_name").text
    print("signed_in_user_name : ", signed_in_user_name)
    time.sleep(display_time)
    if host_displayname == signed_in_user_name:
        print("Successfully Signed in with Host user again")
    else:
        raise AssertionError("Unable to signed in with Host user again")
    if not common.is_element_present(device, hot_desk_dict, "hot_desk_btn"):
        print("Hot Desk option not visible")
    print("Hot Desk option visible")
    # for audio phones and conferance landscape
    common.wait_for_and_click(device, settings_dict, "user_displayname")
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")
    time.sleep(action_time)
    # for cap user
    if not common.is_element_present(device, home_screen_dict, "call_tab"):
        close_the_hamburger_menu(device)


def validate_cancels_hot_desking_signin(device, hot_desk_account):
    print("device :", device)
    common.wait_for_and_click(device, navigation_dict, "Navigation")
    common.wait_for_and_click(device, hot_desk_dict, "hot_desk_btn")
    verify_settings_screen_from_hot_desk_page(device)
    account = "user"
    print("Account :", account)
    hd_user = hot_desk_account
    print("to_device : ", hd_user)
    username = config["devices"][hd_user][account]["username"]
    password = config["devices"][hd_user][account]["password"]
    print("HD username : ", username)
    print("HD password : ", password)
    common.hide_keyboard(device)
    search_input = common.wait_for_element(device, sign_dict, "Username")
    search_input.send_keys(username)
    common.hide_keyboard(device)
    time.sleep(display_time)
    common.wait_for_and_click(device, sign_dict, "Sign_in_button")
    time.sleep(2)
    common.hide_keyboard(device)
    common.wait_for_element(device, sign_dict, "Password")
    settings_keywords.device_setting_back(device)
    common.wait_for_and_click(device, sign_dict, "sign_in_back_button")
    if not common.is_element_present(device, calls_dict, "calls_tab"):
        if not common.is_element_present(device, calendar_dict, "calendar_tab"):
            common.wait_for_element(device, calls_dict, "call_park")


def end_hot_desk_without_disable_home_screen(device):
    print("device :", device)
    call_keywords.come_back_to_home_screen(device)
    common.click_if_present(device, hot_desk_dict, "continue_button")
    common.wait_for_and_click(device, navigation_dict, "Navigation")
    common.wait_for_and_click(device, hot_desk_dict, "stop_hot_desking")
    common.wait_for_and_click(device, hot_desk_dict, "end_button")
    common.wait_for_element(device, calls_dict, "user_profile_picture")


def verify_hd_signin_button_for_hd_policy_disable_user(device):
    print("device :", device)
    if not common.click_if_present(device, navigation_dict, "Navigation"):
        common.wait_for_and_click(device, calls_dict, "user_profile_picture")
    time.sleep(action_time)
    if common.is_element_present(device, hot_desk_dict, "hot_desk_btn"):
        raise AssertionError("Hot Desk button is visible for 'Hot Desk' disabled user")
    settings_keywords.swipe_left(device)
    print("Swiped left")


def verify_hd_user_access_to_advance_setting_page(device):
    verify_settings_page_in_HD_mode(device)
    common.wait_for_and_click(device, settings_dict, "Device_Settings")
    settings_keywords.swipe_till_end(device)
    time.sleep(display_time)
    device_settings_keywords.hd_user_checking_advance_setting_page(device)
    common.click_if_present(device, calls_dict, "Call_Back_Button")
    common.wait_for_element(device, calls_dict, "search")
