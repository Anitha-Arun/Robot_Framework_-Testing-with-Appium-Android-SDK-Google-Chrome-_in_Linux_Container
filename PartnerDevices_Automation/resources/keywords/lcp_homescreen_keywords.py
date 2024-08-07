import common
from Selectors import load_json_file
import settings_keywords

lcp_homescreen_dict = load_json_file("resources/Page_objects/lcp_homescreen.json")
Navigation_dict = load_json_file("resources/Page_objects/Navigation.json")
calls_dict = load_json_file("resources/Page_objects/Calls.json")
home_screen_dict = load_json_file("resources/Page_objects/Home_screen.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")


def verify_date_and_time_on_lcp_homescreen(device):
    common.wait_for_element(device, lcp_homescreen_dict, "time")
    common.wait_for_element(device, lcp_homescreen_dict, "date")


def verify_and_click_contacts_on_lcp_homescreen(device):
    common.wait_for_and_click(device, lcp_homescreen_dict, "people_tab")
    common.wait_for_element(device, lcp_homescreen_dict, "all_contacts")
    common.wait_for_element(device, lcp_homescreen_dict, "contacts_display")


def verify_option_present_inside_hamburger_menu_of_lcp_homescreen(device):
    common.wait_for_and_click(device, lcp_homescreen_dict, "homescreen_menu")
    common.wait_for_element(device, lcp_homescreen_dict, "user_current_status")
    common.wait_for_and_click(device, lcp_homescreen_dict, "status_drop_down_button")
    common.wait_for_element(device, Navigation_dict, "Available")
    common.wait_for_element(device, Navigation_dict, "Busy")
    common.wait_for_element(device, Navigation_dict, "Do_not_disturb")
    common.wait_for_element(device, Navigation_dict, "Be_right_back")
    common.wait_for_and_click(device, lcp_homescreen_dict, "status_drop_down_button")
    common.wait_for_element(device, lcp_homescreen_dict, "settings_icon")
    common.wait_for_and_click(device, lcp_homescreen_dict, "more_cancel_button")


def verify_user_presence_along_with_profile_picture_on_homescreen(device, presence_status=None):
    if presence_status is not None and presence_status.lower() not in ["available", "busy", "dnd", "offline", "away"]:
        raise AssertionError(f"Unexpected value for presence_status : {presence_status}")
    status_desc = common.wait_for_element(device, lcp_homescreen_dict, "user_profile_picture")
    status_desc = status_desc.get_attribute("content-desc")
    print(status_desc)
    status_desc = str(status_desc.split(":")[1].strip())
    print(status_desc)
    if status_desc not in ["Available", "Busy", "Do not disturb", "Be right back", "Offline" "Away"]:
        raise AssertionError(f"{device}: Doesn't have presence status on homescreen")
    if presence_status is not None:
        if presence_status.lower() == "available":
            presence_status = "Available"
        elif presence_status.lower() == "busy":
            presence_status = "Busy"
        elif presence_status.lower() == "away":
            presence_status = "Away"
        elif presence_status.lower() == "dnd":
            presence_status = "Do not disturb"
        elif presence_status.lower() == "offline":
            presence_status = "Offline"
        if status_desc != presence_status:
            raise AssertionError(
                f"{device}: Expected presence state: {presence_status} is not same as actual presence state: {status_desc}"
            )


def verify_call_forwarding_label_status_on_home_screen_lcp(device, status, to_device=None):
    if status.lower() not in ["off", "voicemail", "contact_or_number", "delegate", "call_group"]:
        raise AssertionError(f"Illegal value for 'status': '{status}'")

    common.click_if_present(device, calls_dict, "Call_Back_Button")
    common.click_if_present(device, home_screen_dict, "home_bar_icon")

    common.wait_for_and_click(device, settings_dict, "call_forwarding_icon_on_home_screen")

    if status.lower() == "off":
        calendar_keywords.scroll_down_device_setting_tab(device)
        common.wait_for_element(device, lcp_homescreen_dict, "dont_call_forward_selected")

    elif status.lower() == "voicemail":
        common.wait_for_element(device, lcp_homescreen_dict, "forward_to_voicemail_selected")

    elif status.lower() == "contact_or_number":
        common.wait_for_element(device, lcp_homescreen_dict, "forward_to_contact_no_selected")

    elif status.lower() == "delegate":
        common.wait_for_element(device, lcp_homescreen_dict, "forward_to_my_delegate_selected")

    elif status.lower() == "call_group":
        common.wait_for_element(device, lcp_homescreen_dict, "forward_to_call_group_selected")

    settings_keywords.device_setting_back(device)
