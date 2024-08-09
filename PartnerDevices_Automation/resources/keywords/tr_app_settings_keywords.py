import tr_console_settings_keywords
import tr_device_settings_keywords
from Selectors import load_json_file
from initiate_driver import config
import time
import common
import SignInOut
import call_keywords
import tr_calendar_keywords

display_time = 2
action_time = 3


navigation_dict = load_json_file("resources/Page_objects/Navigation.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")
tr_settings_dict = load_json_file("resources/Page_objects/tr_settings.json")
tr_device_settings_dict = load_json_file("resources/Page_objects/tr_device_settings.json")
tr_home_screen_dict = load_json_file("resources/Page_objects/tr_home_screen.json")
ztp_dict = load_json_file("resources/Page_objects/ztp.json")
signin_dict = load_json_file("resources/Page_objects/Signin.json")
calls_dict = load_json_file("resources/Page_objects/Calls.json")
tr_calls_dict = load_json_file("resources/Page_objects/tr_calls.json")
tr_console_settings_dict = load_json_file("resources/Page_objects/rooms_console_settings.json")
app_bar_dict = load_json_file("resources/Page_objects/App_bar.json")
device_settings_dict = load_json_file("resources/Page_objects/Device_settings.json")
tr_calendar_dict = load_json_file("resources/Page_objects/tr_calendar.json")
Calls_dict = load_json_file("resources/Page_objects/Calls.json")
tr_console_calls_dict = load_json_file("resources/Page_objects/rooms_console_calls.json")


def report_an_issue(device):
    time.sleep(3)
    if common.is_element_present(device, calls_dict, "Hang_up_button"):
        common.wait_for_and_click(device, tr_calls_dict, "call_more_option")
    common.wait_for_and_click(device, tr_settings_dict, "Report_an_issue")
    common.wait_for_element(device, settings_dict, "issue_title")
    bug_details = common.wait_for_element(device, tr_settings_dict, "Title required")
    bug_details.send_keys(config["Report_feedback"]["title"])
    bug_details2 = common.wait_for_element(device, tr_settings_dict, "bug details")
    bug_details2.send_keys(config["Report_feedback"]["bug_details"])
    common.wait_for_and_click(device, settings_dict, "send_bug")


def click_on_more_option(device):
    print("device :", device)
    common.wait_for_and_click(device, tr_settings_dict, "more_button")


def verify_app_settings_options(device):
    common.wait_for_element(device, tr_settings_dict, "settings_button")
    common.wait_for_element(device, tr_home_screen_dict, "volume_icon")
    common.wait_for_element(device, tr_home_screen_dict, "volume_plus")
    common.wait_for_element(device, tr_home_screen_dict, "volume_minus")


def verify_no_help_option_on_sign_in_screen(device):
    common.wait_for_element(device, ztp_dict, "Step1_text_on_signin_page")
    common.wait_for_element(device, ztp_dict, "Step2_text_on_signin_page")
    if not common.is_element_present(device, signin_dict, "dfc_login_code"):
        common.wait_for_element(device, signin_dict, "refresh_code_button")
    common.wait_for_and_click(device, signin_dict, "sign_in_on_the_device")
    if common.is_element_present(device, settings_dict, "Help"):
        raise AssertionError("Help option is present  in the sign in screen")
    common.hide_keyboard(device)
    if "console" in device:
        tr_console_settings_keywords.device_setting_back_btn(device)
    else:
        SignInOut.device_setting_back_till_signin_btn_visible(device)


def verify_no_help_option_on_app_settings(device):
    common.wait_for_and_click(device, tr_settings_dict, "more_button")
    common.wait_for_and_click(device, tr_settings_dict, "settings_button")
    if common.is_element_present(device, settings_dict, "Help", "xpath"):
        raise AssertionError("Help option is present  in the app settings page")
    tr_device_settings_keywords.come_back_from_admin_settings_page(device)


def verify_option_in_dfc_settings_screen_and_about_option_should_not_present(device):
    common.wait_for_element(device, signin_dict, "sign_in_on_the_device")
    common.wait_for_and_click(device, device_settings_dict, "fre_partner_settings")
    common.wait_for_element(device, ztp_dict, "Cloud_option")
    common.wait_for_element(device, ztp_dict, "Provision_device")
    common.wait_for_element(device, ztp_dict, "Report_an_issue")
    common.wait_for_element(device, ztp_dict, "Device_settings")
    if common.is_element_present(device, tr_settings_dict, "about"):
        raise AssertionError(f"{device}: in DFC screen About option is present")
    call_keywords.device_right_corner_click(device)


def get_version_number(device):
    device_version = common.wait_for_element(device, tr_device_settings_dict, "version").text
    version_number = device_version.split(":")[1]
    print(f"{device}version number is : {version_number}")
    return version_number


def get_device_id_number(device):
    device_id = common.wait_for_element(device, tr_device_settings_dict, "device_id").text
    device_id_number = device_id.split(":")[1]
    print(f"{device}version number is : {device_id_number}")
    return device_id_number


def verify_version_number_after_resign_on_device(device, device_version_before_sign, device_version_after_resign_sign):
    print("device:", device)
    print(f"{device}:'get the version number in about page': {device_version_before_sign}")
    print(f"{device}:'get the version number after resign': {device_version_after_resign_sign}")
    if device_version_before_sign != device_version_after_resign_sign:
        raise AssertionError(f"{device}:before and after resign version number is not matching")


def get_hardware_id(device):
    hardware_id = common.wait_for_element(device, tr_device_settings_dict, "hardware_id").text
    hardware_id_list = hardware_id.split(":")[2]
    hardware_id_number = hardware_id_list.split(",")[0]
    print(f"{device}version number is : {hardware_id_number}")
    return hardware_id_number


def verify_default_stage_layout(device):
    common.wait_for_element(device, tr_calendar_dict, "show_meeting_names_text")
    for i in range(5):
        if common.is_element_present(device, tr_calendar_dict, "Default_stage_layout"):
            break
        tr_calendar_keywords.swipe_the_middle_page_to_end(device)
    common.wait_for_and_click(device, tr_calendar_dict, "Default_stage_layout")
    if not common.is_element_present(device, tr_calendar_dict, "content_people"):
        common.wait_for_element(device, tr_calendar_dict, "Content_Gallery")
    if not common.is_element_present(device, tr_calendar_dict, "focus_on_content"):
        common.wait_for_element(device, tr_calendar_dict, "Content_only")
    common.wait_for_element(device, tr_calendar_dict, "front_row")
    call_keywords.dismiss_the_popup_screen(device)


def verify_content_gallery_should_be_selected(device, mode):
    if mode.lower() not in ["content_gallery", "content_only", "gallery"]:
        raise AssertionError(f"{mode}: unexpected mode got passed")
    if "console" in device:
        common.wait_for_and_click(device, tr_calendar_dict, "call_control_content_share_mode")
        if mode.lower() == "content_gallery":
            common.wait_for_element(device, tr_console_calls_dict, "content_gallery_state")
        elif mode.lower() == "gallery":
            common.wait_for_element(device, tr_console_calls_dict, "gallery_mode_state")
        elif mode.lower() == "content_only":
            common.wait_for_element(device, tr_console_calls_dict, "content_only_state")
        call_keywords.dismiss_the_popup_screen(device)
    else:
        if mode.lower() == "content_gallery":
            common.wait_for_element(device, tr_calendar_dict, "video_view")
            common.wait_for_element(device, tr_calendar_dict, "content_gallery_participant_grid")
        elif mode.lower() == "gallery":
            common.wait_for_element(device, tr_calendar_dict, "video_view")
            common.wait_for_element(device, tr_calendar_dict, "participant_view")
        elif mode.lower() == "content_only":
            common.wait_for_element(device, tr_calendar_dict, "content_container")
            common.wait_for_element(device, Calls_dict, "participant_view_container")
