from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import calendar_keywords
import common
from Selectors import load_json_file
from initiate_driver import obj_dev as obj
from initiate_driver import config
import time
import settings_keywords
import app_bar_keywords

display_time = 5
action_time = 5
scroll_up_amount = 3
calendar_dict = load_json_file("resources/Page_objects/Calendar.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")
navigation_dict = load_json_file("resources/Page_objects/Navigation.json")
calls_dict = load_json_file("resources/Page_objects/Calls.json")
sign_dict = load_json_file("resources/Page_objects/Signin.json")
homescreen_dict = load_json_file("resources/Page_objects/Home_screen.json")
lcp_homescreen_dict = load_json_file("resources/Page_objects/lcp_homescreen.json")
tr_device_settings_dict = load_json_file("resources/Page_objects/tr_device_settings.json")


def verify_user_friendly_name_and_display_picture(device):
    device, account = common.decode_device_spec(device)
    if not common.click_if_present(device, navigation_dict, "Navigation"):
        if not (account == "meeting_user" and common.is_portrait_mode_cnf_device(device)):
            raise AssertionError(f"{device} couldn't open navigation menu")
    tmp_dict = common.get_dict_copy(
        navigation_dict, "user_name", "replace_xpath", config["devices"][device][account]["displayname"]
    )
    common.wait_for_element(device, tmp_dict, "user_name")
    if not (account == "meeting_user" and common.is_portrait_mode_cnf_device(device)):
        common.wait_for_element(device, navigation_dict, "user_image")
    common.click_if_present(device, navigation_dict, "Navigation")
    time.sleep(display_time)
    common.click_if_present(device, calls_dict, "Call_Back_Button")


def verify_user_contact_info(device):
    device, account = common.decode_device_spec(device)
    if not common.click_if_element_appears(device, navigation_dict, "Navigation"):
        if not (account == "meeting_user" and common.is_portrait_mode_cnf_device(device)):
            raise AssertionError(f"{device} couldn't open navigation menu")
        common.wait_for_element(device, homescreen_dict, "user_name")
        return
    tmp_dict = common.get_dict_copy(
        navigation_dict, "user_name", "replace_xpath", config["devices"][device][account]["displayname"]
    )
    common.wait_for_and_click(device, tmp_dict, "user_name")
    contact = common.wait_for_element(device, navigation_dict, "mailid")
    print(f"{device}: Mail-id: {contact}")


def report_a_problem(device):
    time.sleep(display_time)
    if common.is_lcp(device):
        common.wait_for_and_click(device, lcp_homescreen_dict, "homescreen_menu")
    elif not common.click_if_present(device, navigation_dict, "Navigation"):
        if not common.is_portrait_mode_cnf_device(device):
            raise AssertionError(f"{device} couldn't open navigation menu")
        common.wait_for_and_click(device, calendar_dict, "app_bar_more")
    if common.is_lcp(device):
        common.wait_for_and_click(device, lcp_homescreen_dict, "settings_icon")
        settings_keywords.swipe_till_end(device)
    else:
        common.wait_for_and_click(device, navigation_dict, "Settings_button")
    time.sleep(display_time)
    settings_keywords.swipe_till_end(device)
    common.sleep_with_msg(device, 5, "Wait for page refresh")
    if not common.is_element_present(device, settings_dict, "feedback_type_label"):
        common.wait_for_and_click(device, settings_dict, "send_feedback")
        common.wait_for_element(device, settings_dict, "summarize_your_feedback")
        common.wait_for_element(device, settings_dict, "feedback_text_section").send_keys(
            config["Report_feedback"]["bug_details"]
        )
        common.wait_for_and_click(device, settings_dict, "send_bug")
        common.wait_while_present(device, settings_dict, "send_bug")
        return
    common.wait_for_and_click(device, settings_dict, "Report_an_issue")
    common.wait_for_element(device, settings_dict, "issue_title").send_keys(config["Report_feedback"]["title"])
    time.sleep(5)
    if common.is_lcp(device):
        settings_keywords.swipe_till_end(device)
    common.wait_for_element(device, settings_dict, "bug_details").send_keys(config["Report_feedback"]["bug_details"])
    time.sleep(5)
    common.wait_for_and_click(device, settings_dict, "send_bug")


def verify_feedback_toast(device):
    print("Verifying feedback toast on device :", device)
    common.wait_for_element(device, settings_dict, "feedback_sent_toast")


def redirect_to_microsoft_help_page(device):
    driver = obj.device_store.get(alias=device)
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((MobileBy.XPATH, navigation_dict["Navigation"]["xpath"]))
    ).click()
    time.sleep(display_time)
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((MobileBy.XPATH, navigation_dict["Settings_button"]["xpath"]))
    ).click()
    time.sleep(display_time)
    settings_keywords.swipe_till_end(device)
    try:
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, settings_dict["Help_feedback"]["id"]))
        ).click()
        print("Clicked on Help & Feedback button")
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, settings_dict["help_btn"]["xpath"]))
        ).click()
        print("Clicked on Help button")
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, settings_dict["help_txt_view"]["xpath"]))
        )
        print("We are in Microsoft help page")
    except Exception as e:
        raise AssertionError("Help page Xpath not found")


def verify_third_party_software_notices(device):
    if not common.click_if_present(device, navigation_dict, "Navigation"):
        if common.is_portrait_mode_cnf_device(device):
            common.wait_for_and_click(device, calendar_dict, "app_bar_more")
        else:
            raise AssertionError(f"{device} couldn't open navigation menu")
    common.wait_for_and_click(device, navigation_dict, "Settings_button")
    common.wait_for_element(device, settings_dict, "Profile")
    settings_keywords.swipe_till_end(device)
    common.wait_for_and_click(device, settings_dict, "about_btn")
    common.wait_for_element(device, settings_dict, "about_txt_view")
    settings_keywords.swipe_till_end(device)
    common.wait_for_and_click(device, settings_dict, "third_party_notices")
    common.wait_for_element(device, settings_dict, "third_party_notices_page_text")


def open_and_verify_calling_option(device):
    common.wait_for_and_click(device, settings_dict, "Calling")
    common.wait_for_element(device, settings_dict, "call_forwarding")
    common.wait_for_element(device, settings_dict, "also_ring")
    common.wait_for_element(device, settings_dict, "if_unanswered")


def verify_company_portal_option(device):
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, settings_dict["company_Portal"]["id"]))
        ).click()
        time.sleep(display_time)
        print("Company Portal option visible")
    except Exception as e:
        raise AssertionError("Company Portal option not visible")


def block_calls_with_no_caller_id(device, block_user):
    settings_keywords.open_settings_page(device)
    common.wait_for_and_click(device, settings_dict, "Calling")
    time.sleep(display_time)
    for i in range(5):
        if common.is_element_present(device, settings_dict, "block_toggle_btn"):
            break
        calendar_keywords.scroll_only_once(device)
    common.change_toggle_button(device, settings_dict, "block_toggle_btn", "on")
    block_the_user(device, block_user)


def block_the_user(from_device, block_device):
    number = common.device_pstndisplay(block_device)
    common.wait_for_and_click(from_device, settings_dict, "blocked_numbers")
    if common.is_element_present(from_device, settings_dict, "remove_blocked_number"):
        common.wait_for_and_click(from_device, settings_dict, "remove_blocked_number")
        common.wait_for_and_click(from_device, settings_dict, "unblock_ok_button")
    common.wait_for_and_click(from_device, settings_dict, "add_number")
    common.wait_for_element(from_device, settings_dict, "add_number_to_blocked").send_keys(number)
    common.wait_for_and_click(from_device, settings_dict, "block")
    common.wait_for_element(from_device, settings_dict, "blocked_number_list")


def unblock_calls_with_no_caller_id(device):
    settings_keywords.open_settings_page(device)
    time.sleep(display_time)
    common.wait_for_and_click(device, settings_dict, "Calling")
    time.sleep(display_time)
    settings_keywords.swipe_till_end(device)
    print("Swiped till end")
    if common.is_lcp(device):
        calendar_keywords.scroll_only_once(device)
        calendar_keywords.scroll_only_once(device)
    common.change_toggle_button(device, settings_dict, "block_toggle_btn", "off")
    unblock_the_user(device)


def unblock_the_user(from_device):
    common.wait_for_and_click(from_device, settings_dict, "blocked_numbers")
    for i in range(2):
        if common.is_element_present(from_device, settings_dict, "remove_blocked_number"):
            common.wait_for_and_click(from_device, settings_dict, "remove_blocked_number")
            common.wait_for_and_click(from_device, settings_dict, "unblock_ok_button")
    common.wait_while_present(from_device, settings_dict, "remove_blocked_number")


def verify_privacy_and_cookies(device):
    settings_keywords.open_settings_page(device)
    time.sleep(display_time)
    if not common.click_if_present(device, settings_dict, "about_btn"):
        settings_keywords.swipe_till_end(device)
        if common.is_lcp(device):
            settings_keywords.swipe_till_end(device)
            settings_keywords.swipe_till_end(device)
        common.wait_for_and_click(device, settings_dict, "about_btn")
    common.wait_for_element(device, settings_dict, "about_page_header")
    if config["devices"][device]["model"].lower() == "manhattan":
        common.wait_for_and_click(device, settings_dict, "privacy_cookies_btn")
        common.wait_for_element(device, settings_dict, "microsoft_privacy_link")
        common.wait_for_and_click(device, calls_dict, "Call_Back_Button")
        common.wait_for_element(device, settings_dict, "privacy_cookies_btn")
        return
    settings_keywords.swipe_till_end(device)
    if common.is_lcp(device):
        settings_keywords.swipe_till_end(device)
        settings_keywords.swipe_till_end(device)
    common.wait_for_and_click(device, settings_dict, "privacy_cookies_btn")
    if common.is_lcp(device):
        settings_keywords.swipe_till_end(device)
    common.wait_for_element(device, settings_dict, "microsoft_privacy_link")
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")
    common.wait_for_element(device, settings_dict, "privacy_cookies_btn")
    app_bar_keywords.swipe_page_up(device)
    app_bar_keywords.swipe_page_up(device)


def verify_terms_of_use(device):
    settings_keywords.open_settings_page(device)
    time.sleep(display_time)
    if not common.click_if_present(device, settings_dict, "about_btn"):
        settings_keywords.swipe_till_end(device)
        if common.is_lcp(device):
            settings_keywords.swipe_till_end(device)
            settings_keywords.swipe_till_end(device)
        common.wait_for_and_click(device, settings_dict, "about_btn")
    common.wait_for_element(device, settings_dict, "about_page_header")
    if config["devices"][device]["model"].lower() == "manhattan":
        common.wait_for_and_click(device, settings_dict, "terms_of_use")
        common.wait_for_element(device, settings_dict, "microsoft_license_link")
        common.wait_for_and_click(device, calls_dict, "Call_Back_Button")
        common.wait_for_element(device, settings_dict, "terms_of_use")
        return
    settings_keywords.swipe_till_end(device)
    if common.is_lcp(device):
        settings_keywords.swipe_till_end(device)
        settings_keywords.swipe_till_end(device)
        settings_keywords.swipe_till_end(device)
    common.wait_for_and_click(device, settings_dict, "terms_of_use")
    common.wait_for_element(device, settings_dict, "microsoft_license_link")
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")
    common.wait_for_element(device, settings_dict, "terms_of_use")
    app_bar_keywords.swipe_page_up(device)
    app_bar_keywords.swipe_page_up(device)


def view_user_profile(device):
    settings_keywords.open_settings_page(device)
    time.sleep(display_time)
    common.wait_for_and_click(device, settings_dict, "profile_btn")
    user_displayname = config["devices"][device]["user"]["displayname"]
    print("user_displayname : ", user_displayname)
    tmp_dict = common.get_dict_copy(calls_dict, "user_display_xpath", "username", user_displayname)
    common.wait_for_element(device, tmp_dict, "user_display_xpath")
    common.wait_for_element(device, settings_dict, "email_xpath")


def sign_out_cancel_btn_verify(device):
    settings_keywords.open_settings_page(device)
    time.sleep(action_time)
    settings_keywords.swipe_till_end(device)
    if common.is_lcp(device):
        settings_keywords.swipe_till_end(device)
    common.wait_for_and_click(device, settings_dict, "Sign_out")
    common.wait_for_and_click(device, sign_dict, "Sign_out_cancel_button")
    time.sleep(action_time)
    common.wait_for_element(device, settings_dict, "Sign_out")
    print("User able to cancel signout")
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")


def sign_out_ok_btn_verify(device):
    settings_keywords.open_settings_page(device)
    time.sleep(action_time)
    settings_keywords.swipe_till_end(device)
    common.wait_for_and_click(device, settings_dict, "Sign_out")
    common.wait_for_and_click(device, sign_dict, "Sign_out_ok_button")
    time.sleep(action_time)
    common.wait_for_element(device, sign_dict, "sign_in_on_the_device")
    print("sign_in_on_the_device Button visible")


def verify_and_disable_notification(device):
    common.wait_for_and_click(device, calls_dict, "user_profile_picture", wait_attempts=90)
    print("User profile picture is visible")
    common.wait_for_and_click(device, navigation_dict, "Settings_button")
    time.sleep(action_time)
    settings_keywords.swipe_till_end(device)
    settings_keywords.disable_notification(device)
    settings_keywords.verify_notification_status(device, "OFF")


def verify_and_enable_notification(device):
    common.wait_for_and_click(device, calls_dict, "user_profile_picture", wait_attempts=90)
    print("User profile picture is visible")
    common.wait_for_and_click(device, navigation_dict, "Settings_button")
    time.sleep(action_time)
    settings_keywords.swipe_till_end(device)
    settings_keywords.enable_notification(device)
    settings_keywords.verify_notification_status(device, "ON")


def verify_options_inside_hamburger_menu_for_cnf_device(device):
    if common.is_portrait_mode_cnf_device(device):
        print(f"{device} doesn't support hamburger menu since it is  portrait mode")
        return
    common.wait_for_and_click(device, navigation_dict, "Navigation")
    common.wait_for_element(device, navigation_dict, "hot_desk_btn")
    common.wait_for_element(device, navigation_dict, "Settings_button")
    common.wait_for_element(device, navigation_dict, "what's_new")
    settings_keywords.click_device_center_point(device)


def verify_options_inside_about_page(device):
    settings_keywords.open_settings_page(device)
    time.sleep(action_time)
    settings_keywords.swipe_till_end(device)
    settings_keywords.swipe_till_end(device)
    common.wait_for_and_click(device, settings_dict, "about_btn")
    _max_attempts = 5
    for _attempt in range(_max_attempts):
        if common.is_element_present(device, settings_dict, "third_party_notices"):
            print(f"{device}: After scrolling {_attempt} third_party_notices found")
            break
        else:
            settings_keywords.swipe_till_end(device)
    common.wait_for_element(device, settings_dict, "terms_of_use")
    common.wait_for_element(device, settings_dict, "privacy_cookies_btn")


def navigate_to_privacy_and_cookies_from_about_page(device):
    common.wait_for_and_click(device, settings_dict, "privacy_cookies_btn")
    common.wait_for_element(device, settings_dict, "microsoft_privacy_link")


def navigate_to_third_party_software_notices_from_about_page(device):
    common.wait_for_and_click(device, settings_dict, "third_party_notices")
    common.wait_for_element(device, settings_dict, "third_party_notices_page_text")


def navigate_to_terms_of_use_from_about_page(device):
    common.wait_for_and_click(device, settings_dict, "terms_of_use")
    common.wait_for_element(device, settings_dict, "microsoft_license_link")


def navigate_to_home_screen_from_about_page(device):
    time.sleep(action_time)
    common.click_if_present(device, calls_dict, "Call_Back_Button")
    settings_keywords.device_setting_back(device)
    for i in range(2):
        common.click_if_present(device, calls_dict, "Call_Back_Button")


def navigate_to_whats_new_page_from_home_screen(device):
    settings_keywords.open_settings_page(device)
    for i in range(2):
        if common.is_element_present(device, navigation_dict, "what's_new"):
            common.wait_for_and_click(device, navigation_dict, "what's_new")
            break
        else:
            settings_keywords.swipe_till_end(device)


def verify_connected_experiences_does_not_present_in_about_page(device):
    common.wait_while_present(device, lcp_homescreen_dict, "Connected_Experiences", max_wait_attempts=3)


def verify_third_party_software_notices_for_lcp(device):
    common.wait_for_and_click(device, lcp_homescreen_dict, "homescreen_menu")
    common.wait_for_and_click(device, lcp_homescreen_dict, "settings_icon")
    common.wait_for_element(device, settings_dict, "Profile")
    settings_keywords.swipe_till_end(device)
    settings_keywords.swipe_till_end(device)
    common.wait_for_and_click(device, settings_dict, "about_btn")
    common.wait_for_element(device, settings_dict, "about_txt_view")
    _max_attempts = 5
    for _attempt in range(_max_attempts):
        if common.is_element_present(device, settings_dict, "third_party_notices"):
            print(f"{device}: After scrolling {_attempt} third_party_notices found")
            break
        else:
            settings_keywords.swipe_till_end(device)
    common.wait_for_and_click(device, settings_dict, "third_party_notices")
    common.wait_for_element(device, settings_dict, "third_party_notices_page_text")


def verify_meetings_btn_not_present_under_app_settings(device):
    settings_keywords.open_settings_page(device)
    for i in range(3):
        if common.is_element_present(device, calendar_dict, "meetings_button", "command"):
            raise AssertionError("Meeting button is present under app setting")
        calendar_keywords.scroll_only_once(device)
