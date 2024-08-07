import common
from initiate_driver import config
import tr_settings_keywords
import settings_keywords
from Selectors import load_json_file
import time
import panel_meetings_device_settings_keywords
import calendar_keywords
import device_settings_keywords
from selenium.webdriver.support import expected_conditions as EC
import call_keywords

action_time = 3

panels_device_settings_dict = load_json_file("resources/Page_objects/panels_device_settings.json")
panels_home_screen_dict = load_json_file("resources/Page_objects/panels_homescreen.json")
panels_meeting_resrv_dict = load_json_file("resources/Page_objects/panels_meeting_reservation.json")
navigation_dict = load_json_file("resources/Page_objects/Navigation.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")
tr_settings_dict = load_json_file("resources/Page_objects/tr_settings.json")
tr_device_settings_dict = load_json_file("resources/Page_objects/tr_device_settings.json")
device_settings_dict = load_json_file("resources/Page_objects/Device_settings.json")
calendar_dict = load_json_file("resources/Page_objects/Calendar.json")
people_dict = load_json_file("resources/Page_objects/People.json")
tr_calendar_dict = load_json_file("resources/Page_objects/tr_calendar.json")
tr_console_signin_dict = load_json_file("resources/Page_objects/rooms_console_signin.json")


def navigation_to_settings_page_in_panel(device):
    common.wait_for_and_click(device, panels_home_screen_dict, "settings_icon")
    common.wait_for_element(device, settings_dict, "About")


def verify_all_options_in_panel_settings(device):
    common.wait_for_element(device, settings_dict, "Report_an_issue")
    common.wait_for_element(device, settings_dict, "About")
    common.wait_for_element(device, settings_dict, "Device_Settings")


def verify_report_an_issue_in_panel(device):
    common.wait_for_and_click(device, settings_dict, "Report_an_issue")
    element1 = common.wait_for_element(device, settings_dict, "issue_title", "id")
    element1.send_keys(config["Report_feedback"]["title"])
    element2 = common.wait_for_element(device, settings_dict, "bug_details", "id")
    element2.send_keys(config["Report_feedback"]["bug_details"])
    common.wait_for_and_click(device, settings_dict, "send_bug", "id")
    # feedback_sent_toast is not focusable
    # common.wait_for_element(device, settings_dict, "feedback_sent_toast")


def verify_about_option_in_panel(device):
    common.wait_for_and_click(device, tr_settings_dict, "about", "id")
    e1 = common.wait_for_element(device, tr_settings_dict, "version", "id")
    print("Teams client version is visible", e1.text)
    common.wait_for_element(device, tr_settings_dict, "copy_right", "id")
    tr_settings_keywords.swipe_screen_page(device)
    tr_settings_keywords.swipe_screen_page(device)
    common.wait_for_element(device, tr_settings_dict, "term_of_use", "id")
    tr_settings_keywords.swipe_screen_page(device)
    tr_settings_keywords.swipe_screen_page(device)
    common.wait_for_element(device, tr_settings_dict, "third_party_information", "id")


def verify_about_page_in_panel(device):
    common.wait_for_element(device, tr_settings_dict, "version", "id")
    common.wait_for_element(device, tr_settings_dict, "copy_right", "id")


def go_back_to_homescreen_from_admin_settings_options(device):
    for attempt in range(4):
        if not (
            common.click_if_present(device, tr_device_settings_dict, "back_button")
            or common.click_if_present(device, panels_device_settings_dict, "close_button")
            or common.click_if_present(device, panels_device_settings_dict, "admin_back_button")
            or common.click_if_present(device, tr_console_signin_dict, "back_layout")
        ):
            break
    if config["devices"][device]["model"].lower() in ["westchester", "brooklyn"]:
        common.wait_for_and_click(device, device_settings_dict, "admin_settings_yes")
        for attempt in range(3):
            common.click_if_present(device, tr_device_settings_dict, "back_button")
    common.wait_for_element(device, panels_home_screen_dict, "wallpaper")
    if common.is_element_present(device, tr_device_settings_dict, "back_button"):
        raise AssertionError(f"{device}: 'back_button' still present after {attempt + 1} clicks")


def verify_third_party_notices_and_information_option_in_panel(device):
    common.wait_for_and_click(device, tr_settings_dict, "about", "id")
    time.sleep(action_time)
    settings_keywords.swipe_till_end(device)
    common.wait_for_and_click(device, settings_dict, "third_party_notices")
    common.wait_for_element(device, settings_dict, "third_party_notices_page_text")


def verify_privacy_and_cookies_option_in_panel(device):
    common.wait_for_and_click(device, settings_dict, "about_btn")
    common.wait_for_element(device, settings_dict, "about_page_header")
    settings_keywords.swipe_till_end(device)
    common.wait_for_and_click(device, settings_dict, "privacy_cookies_btn")
    common.wait_for_element(device, tr_device_settings_dict, "Microsoft_Privacy_Statement")


def verify_terms_of_use_option_in_panel(device):
    common.wait_for_and_click(device, settings_dict, "about_btn")
    common.wait_for_element(device, settings_dict, "about_page_header")
    settings_keywords.swipe_till_end(device)
    common.wait_for_and_click(device, settings_dict, "terms_of_use")
    common.wait_for_element(device, settings_dict, "microsoft_license_link")


def verifying_all_options_in_panel_admin_app_settings(device):
    common.wait_for_element(device, panels_device_settings_dict, "LED_settings_in_panel")
    common.wait_for_element(device, panels_device_settings_dict, "meetings_in_panel")
    common.wait_for_element(device, panels_device_settings_dict, "device_pairing_in_panel")
    common.wait_for_element(device, tr_settings_dict, "background_button")
    common.wait_for_element(device, panels_device_settings_dict, "device_restart_option")


def navigate_to_background_tab_in_panel(device):
    panel_meetings_device_settings_keywords.go_to_meetings_tab_in_panel(device)
    common.wait_for_and_click(device, panels_device_settings_dict, "background_button")


def verify_service_provider_is_absent(device):
    if common.is_element_present(device, panels_device_settings_dict, "service_provider_txt"):
        raise AssertionError(f"{device}: service_provider_txt is present ")


def Navigate_and_change_time_and_date_in_admin_settings_for_panel(device, time_format):
    if time_format.lower() not in ["24hr", "12hr"]:
        raise AssertionError(f"{device}: Unexpected value for time_format: {time_format}")
    print("time_format sanity check")
    if time_format.lower() == "12hr":
        toggle_status = "off"
        time_format_select = "12 Hour"
    elif time_format.lower() == "24hr":
        toggle_status = "on"
        time_format_select = "24 Hour"
    print("values assigned")
    if config["devices"][device]["model"].lower() not in ["savannah", "beverly hills", "hollywood"]:
        panel_meetings_device_settings_keywords.navigate_inside_admin_setting_in_panel(device)
    if config["devices"][device]["model"].lower() in ["westchester", "savannah"]:
        common.wait_for_and_click(device, panels_device_settings_dict, "date_time")
        common.click_if_present(device, device_settings_dict, "timeformat_btn")
        if time_format.lower() == "12hr":
            print("12 hr test")
            radio_btn_12hr = common.wait_for_element(device, panels_device_settings_dict, "12_hr_time_format")
            radio_btn_12hr_status = radio_btn_12hr.get_attribute("checked").lower()
            if radio_btn_12hr_status != "true":
                common.wait_for_and_click(device, panels_device_settings_dict, "12_hr_time_format")
        elif time_format.lower() == "24hr":
            print("24 hr test")
            radio_btn_24hr = common.wait_for_element(device, panels_device_settings_dict, "24_hr_time_format")
            radio_btn_24hr_status = radio_btn_24hr.get_attribute("checked").lower()
            if radio_btn_24hr_status != "true":
                print("changed to 24")
                common.wait_for_and_click(device, panels_device_settings_dict, "24_hr_time_format")
        if config["devices"][device]["model"].lower() == "savannah":
            common.wait_for_and_click(device, calendar_dict, "ok_button", "id")
    if config["devices"][device]["model"].lower() == "arlington":
        common.wait_for_and_click(device, device_settings_dict, "system_settings")
        common.wait_for_and_click(device, panels_device_settings_dict, "regional_settings_button")
        common.change_toggle_button(device, panels_device_settings_dict, "time_format_option", toggle_status)
    if config["devices"][device]["model"].lower() == "surprise":
        common.wait_for_and_click(device, panels_device_settings_dict, "date_time")
        common.change_toggle_button(device, panels_device_settings_dict, "time_format_option", toggle_status)
    if config["devices"][device]["model"].lower() in ["beverly hills", "hollywood"]:
        common.hide_keyboard(device)
        if not common.click_if_present(device, tr_device_settings_dict, "general"):
            calendar_keywords.scroll_down_device_setting_tab(device)
            calendar_keywords.scroll_down_device_setting_tab(device)
            common.wait_for_and_click(device, tr_device_settings_dict, "general")
        panel_meetings_device_settings_keywords.navigate_inside_admin_setting_in_panel(device)
        common.wait_for_and_click(device, panels_device_settings_dict, "date_time")
        common.wait_for_and_click(device, device_settings_dict, "timeformat_btn")
        # if time_format_select.lower() != time_format_selected.lower():
        if time_format.lower() == "12hr":
            if not common.is_element_present(device, panels_device_settings_dict, "12_hr_time_format_selected"):
                common.wait_for_and_click(device, panels_device_settings_dict, "12_hr_time_format")
                common.wait_for_element(device, panels_device_settings_dict, "12_hr_time_format_selected")
        elif time_format.lower() == "24hr":
            if not common.is_element_present(device, panels_device_settings_dict, "24_hr_time_format_selected"):
                common.wait_for_and_click(device, panels_device_settings_dict, "24_hr_time_format")
                common.wait_for_element(device, panels_device_settings_dict, "24_hr_time_format_selected")
        common.wait_for_and_click(device, people_dict, "action_submit", "xpath")
    if config["devices"][device]["model"].lower() == "richland":
        common.wait_for_and_click(device, device_settings_dict, "system_settings")
        common.wait_for_and_click(device, panels_device_settings_dict, "date_time")
        time_format_selected = common.wait_for_element(
            device, panels_device_settings_dict, "time_format_selected_option"
        ).text
        print(f"time_format_selected: {time_format_selected}")
        print(f"time_format_select: {time_format_select}")
        if time_format_select.lower() != time_format_selected.lower():
            common.wait_for_and_click(device, panels_device_settings_dict, "time_format_dropdown")
            if time_format.lower() == "12hr":
                common.wait_for_and_click(device, panels_device_settings_dict, "12_hr_time_format")
            elif time_format.lower() == "24hr":
                common.wait_for_and_click(device, panels_device_settings_dict, "24_hr_time_format")
            time_format_selected = common.wait_for_element(
                device, panels_device_settings_dict, "time_format_selected_option"
            ).text
            if time_format_select.lower() != time_format_selected.lower():
                raise AssertionError(
                    f"{device}: Unexpected value for time_format_selected even after changing it: {time_format_selected}"
                )
            common.wait_for_and_click(device, tr_calendar_dict, "save_btn")


def verify_network_option_in_panel(device):
    settings_keywords.click_device_settings(device)
    _model = config["devices"][device]["model"].lower()

    if _model in ["beverly hills", "hollywood"]:
        device_settings_keywords.swipe_till_sign_out(device)
        common.wait_for_and_click(device, panels_device_settings_dict, "network_btn")
        common.wait_for_element(device, panels_device_settings_dict, "admin_pswd_field").set_value(
            config["devices"][device]["admin_password"]
        )
        common.wait_for_and_click(device, panels_device_settings_dict, "admin_login_btn")
        common.wait_for_element(device, panels_device_settings_dict, "wifi_txt")
        common.wait_for_element(device, panels_device_settings_dict, "Advanced_network_txt")

    elif _model == "richland":
        common.wait_for_and_click(device, tr_device_settings_dict, "teams_admin_settings1")
        common.wait_for_element(device, device_settings_dict, "admin_username_box").set_value(
            config["devices"][device]["admin_username"]
        )
        common.wait_for_element(device, settings_dict, "admin_passwd", "id1").set_value(
            config["devices"][device]["admin_password"]
        )
        common.wait_for_and_click(device, calendar_dict, "ok_button")
        common.wait_for_and_click(device, device_settings_dict, "system_settings")
        common.wait_for_and_click(device, panels_device_settings_dict, "network_btn")
        common.wait_for_and_click(device, panels_device_settings_dict, "DNS_1_txt")

    elif _model in ["westchester", "brooklyn"]:
        common.wait_for_and_click(device, tr_device_settings_dict, "teams_admin_settings1")
        common.wait_for_element(device, panels_device_settings_dict, "admin_pswd_field").set_value(
            config["devices"][device]["admin_password"]
        )
        common.hide_keyboard(device)
        common.wait_for_and_click(device, panels_device_settings_dict, "admin_login_btn")
        common.sleep_with_msg(device, 3, "Waiting for Admin settings page to load")
        common.wait_for_and_click(device, panels_device_settings_dict, "network_btn")
        common.wait_for_element(device, panels_device_settings_dict, "domain_name_txt")
        common.wait_for_element(device, panels_device_settings_dict, "host_name_txt")
        common.wait_for_and_click(device, panels_device_settings_dict, "admin_back_button")
        common.wait_for_and_click(device, device_settings_dict, "user_sign_out_yes")

    elif _model == "surprise":
        common.wait_for_and_click(device, settings_dict, "Device_administration")
        if common.is_element_present(device, panels_device_settings_dict, "login_btn"):
            common.wait_for_and_click(device, panels_device_settings_dict, "login_btn")
            common.wait_for_element(device, settings_dict, "admin_passwd", "xpath").set_value(
                config["devices"][device]["admin_password"]
            )
            common.wait_for_and_click(device, calendar_dict, "ok_button")
            device_settings_keywords.swipe_till_admin_settings(device)
            device_settings_keywords.swipe_till_admin_settings(device)
            common.wait_for_and_click(device, panels_device_settings_dict, "network_btn")
            common.wait_for_element(device, panels_device_settings_dict, "ip_address_txt")

    elif _model == "savannah":
        common.wait_for_and_click(device, panels_device_settings_dict, "admin_pswd_field")
        common.wait_for_element(device, panels_device_settings_dict, "admin_pswd_field").set_value(
            config["devices"][device]["admin_password"]
        )
        common.wait_for_and_click(device, panels_device_settings_dict, "admin_login_continue_btn")
        tr_settings_keywords.swipe_screen_page(device)
        tr_settings_keywords.swipe_screen_page(device)
        common.wait_for_and_click(device, panels_device_settings_dict, "network_btn")
        common.wait_for_element(device, panels_device_settings_dict, "ip_address_txt")
        common.wait_for_element(device, panels_device_settings_dict, "Gateway_txt")

    elif _model == "arlington":
        common.wait_for_and_click(device, tr_device_settings_dict, "admin_settings", "xpath1")
        common.wait_for_element(device, device_settings_dict, "edit_text_number_pin").set_value(
            config["devices"][device]["admin_password"]
        )
        common.wait_for_and_click(device, device_settings_dict, "submit_button")
        common.wait_for_and_click(device, device_settings_dict, "connectivity_setting")
        common.wait_for_element(device, panels_device_settings_dict, "ip_address_txt")
        common.wait_for_element(device, panels_device_settings_dict, "DNS_1_txt")
        common.wait_for_and_click(device, panels_device_settings_dict, "back_to_settings")
        common.wait_for_and_click(device, panels_device_settings_dict, "close_button1", "id")


def verify_wifi_option_inside_network_settings_is_off(device):
    _model = config["devices"][device]["model"].lower()

    if _model in ["Hollywood", "Beverly Hills"]:
        common.wait_for_and_click(device, panels_device_settings_dict, "wifi_txt")
        common.verify_toggle_button(device, panels_device_settings_dict, "wifi_toggle_btn", "off")
    call_keywords.come_back_to_home_screen(device)
