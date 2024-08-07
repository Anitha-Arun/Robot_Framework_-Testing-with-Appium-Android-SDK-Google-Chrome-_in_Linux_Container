from initiate_driver import config
from Selectors import load_json_file
import settings_keywords
import time
import call_keywords
import common
import calendar_keywords
import people_keywords
import walkie_talkie_keywords
import voicemail_keywords

display_time = 2
action_time = 3

home_screen_dict = load_json_file("resources/Page_objects/Home_screen.json")
calls_dict = load_json_file("resources/Page_objects/Calls.json")
navigation_dict = load_json_file("resources/Page_objects/Navigation.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")
calendar_dict = load_json_file("resources/Page_objects/Calendar.json")
hot_desk_dict = load_json_file("resources/Page_objects/Hot_desk.json")
app_bar_dict = load_json_file("resources/Page_objects/App_bar.json")
voicemail_dict = load_json_file("resources/Page_objects/voicemail.json")
walkie_talkie_dict = load_json_file("resources/Page_objects/walkie_talkie.json")
people_dict = load_json_file("resources/Page_objects/People.json")
common_dict = load_json_file("resources/Page_objects/common.json")
lcp_homescreen_dict = load_json_file("resources/Page_objects/lcp_homescreen.json")


def verify_home_screen_tiles(device, device_type="home_screen_enabled"):
    if device_type.lower() not in ["home_screen_enabled", "cap_home_screen_enabled"]:
        raise AssertionError(f"Illegal value for 'device_type': '{device_type}'")
    common.click_if_present(device, home_screen_dict, "home_bar_icon")
    common.wait_for_element(device, calls_dict, "calls_tab")
    if not common.is_element_present(device, home_screen_dict, "voicemail_tab"):
        if not common.is_element_present(device, home_screen_dict, "walkie_talkie_tab"):
            common.wait_for_element(device, home_screen_dict, "people_tab")
    if device_type == "home_screen_enabled":
        common.wait_for_element(device, home_screen_dict, "calendar_tab")
        common.wait_for_element(device, home_screen_dict, "more_option")


def verify_home_screen_time_dates(device, device_type="home_screen_enabled"):
    global date_and_time, date_and_time_format
    if device_type.lower() not in ["home_screen_enabled", "cap_home_screen_enabled"]:
        raise AssertionError(f"Illegal value for 'device_type': '{device_type}'")
    if device_type == "home_screen_enabled":
        common.wait_for_element(device, home_screen_dict, "hs_date_time")
    if device_type == "cap_home_screen_enabled":
        common.wait_for_element(device, home_screen_dict, "hs_date_time_for_cap")


def verify_home_screen_notification_view(device):
    settings_keywords.traverse_to_settings_notification(device)
    settings_keywords.disable_notification(device)
    settings_keywords.traverse_to_settings_notification(device)
    settings_keywords.enable_notification(device)
    common.wait_for_element(device, home_screen_dict, "notification_view")
    common.wait_for_element(device, home_screen_dict, "clear_notification")


def verify_clear_notification_button_while_user_donot_have_notification(device):
    if common.is_element_present(device, home_screen_dict, "clear_notification"):
        raise AssertionError("Clear Notification button is visible on Home screen")
    print("Clear Notification button is not visible on Home screen")


def clear_notification_from_home_screen(device):
    common.wait_for_element(device, navigation_dict, "Navigation")
    common.click_if_present(device, home_screen_dict, "clear_notification")


def verify_user_profile_picture_on_home_screen(device):
    common.wait_for_element(device, calls_dict, "user_profile_picture")


def come_back_to_home_screen_page_and_verify(device):
    if common.is_lcp(device):
        common.wait_for_and_click(device, common_dict, "home_btn")
        common.wait_for_element(device, lcp_homescreen_dict, "homescreen_menu")
        return
    common.wait_for_and_click(device, home_screen_dict, "home_bar_icon")
    verify_home_screen_tiles(device)
    verify_home_screen_time_dates(device)


def verify_notification_option_from_app_settings_page(device, status):
    if status.lower() not in ["enable", "disable"]:
        raise AssertionError(f"Illegal value for 'status': '{status}'")
    if not common.click_if_present(device, calls_dict, "user_profile_picture"):
        common.wait_for_and_click(device, navigation_dict, "Navigation")
        time.sleep(action_time)
    common.wait_for_and_click(device, navigation_dict, "Settings_button")
    settings_keywords.swipe_till_end(device)
    if status.lower() == "enable":
        common.wait_for_element(device, home_screen_dict, "notification_btn")
    elif status.lower() == "disable":
        if common.is_element_present(device, home_screen_dict, "notification_btn"):
            raise AssertionError("Notification toggle button is visible")
        print("Notification toggle button is not visible")
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")


def set_status_message_and_validate(device):
    common.wait_for_and_click(device, calls_dict, "user_profile_picture")
    elem = common.wait_for_element(device, settings_dict, "set_status_msg")
    elem.click()
    status_message = config["set_status_message"]["message"]
    print("status_message : ", status_message)
    time.sleep(display_time)
    common.click_if_present(device, settings_dict, "clear_status_message_icon")
    msg_input = common.wait_for_element(device, settings_dict, "set_status_msg_text_box")
    msg_input.send_keys(status_message)
    common.hide_keyboard(device)
    common.wait_for_and_click(device, settings_dict, "save_btn")
    common.wait_for_and_click(device, calls_dict, "user_profile_picture")
    elem = common.wait_for_element(device, settings_dict, "set_status_msg")
    saved_status = elem.text
    if saved_status != status_message:
        raise AssertionError(f"{device}: Invalid status message: {elem.text}, Expecting: {saved_status}")
    common.wait_for_and_click(device, calls_dict, "user_profile_picture")
    common.click_if_present(device, calls_dict, "Call_Back_Button")


def set_status_message_and_cancel(device):
    common.wait_for_and_click(device, calls_dict, "user_profile_picture")
    common.wait_for_and_click(device, settings_dict, "set_status_msg")
    status_message = config["set_status_message"]["message"]
    print("status_message : ", status_message)
    time.sleep(display_time)
    common.click_if_present(device, settings_dict, "clear_status_message_icon")
    msg_input = common.wait_for_element(device, settings_dict, "set_status_msg_text_box")
    msg_input.send_keys(status_message)
    common.hide_keyboard(device)
    time.sleep(display_time)
    common.wait_for_and_click(device, settings_dict, "cancel_btn")


def verify_missed_call_notification(to_device, from_device):
    from_device_displayname = config["devices"][from_device]["user"]["displayname"]
    temp_dict = common.get_dict_copy(
        people_dict, "search_result_item_container", "config_display", from_device_displayname
    )
    common.wait_for_element(to_device, temp_dict, "search_result_item_container")
    common.wait_for_element(to_device, home_screen_dict, "miss_call_notification")


def call_back_from_miss_call_notification(device):
    common.wait_for_and_click(device, home_screen_dict, "call_back_button", "xpath")
    time.sleep(display_time)
    if common.click_if_present(device, calls_dict, "myself_xpath"):
        print(f"*WARN*:: {device}: Found and used unexpected 'myself' OBO")
    common.wait_for_element(device, calls_dict, "Hang_up_button")


def verify_meeting_notification(device):
    settings_keywords.traverse_to_settings_notification(device)
    settings_keywords.disable_notification(device)
    settings_keywords.traverse_to_settings_notification(device)
    settings_keywords.enable_notification(device)
    meeting_name = common.wait_for_element(device, home_screen_dict, "notification_title").text
    print("Meeting notification visible, Meeting name : ", meeting_name)
    meeting_time = common.wait_for_element(device, home_screen_dict, "meeting_time").text
    print("Meeting time : ", meeting_time)
    common.wait_for_element(device, home_screen_dict, "join_btn")


def join_meeting_from_home_screen(device):
    common.wait_for_and_click(device, home_screen_dict, "join_btn", "xpath")
    time.sleep(display_time)


def verify_voicemail_notification(to_device, from_device):
    from_device_displayname = config["devices"][from_device]["user"]["displayname"]
    print("from_device_displayname : ", from_device_displayname)
    tmp_dict = common.get_dict_copy(home_screen_dict, "voicemail_notification", "username", from_device_displayname)
    common.wait_for_element(to_device, tmp_dict, "voicemail_notification")
    common.wait_for_element(to_device, home_screen_dict, "call_back_button")
    common.wait_for_element(to_device, home_screen_dict, "delete_button")


def clear_user_status_message(device):
    common.wait_for_and_click(device, calls_dict, "user_profile_picture")
    common.wait_for_and_click(device, settings_dict, "set_status_msg")
    status_message_text = common.wait_for_element(device, settings_dict, "set_status_msg_text_box").text
    if status_message_text == "Set your status message":
        time.sleep(display_time)
        if common.is_element_present(device, settings_dict, "clear_status_message_icon"):
            raise AssertionError("still status message not cleared")
        settings_keywords.click_back(device)
    else:
        common.wait_for_and_click(device, settings_dict, "clear_status_message_icon")
        status_message_text = common.wait_for_element(device, settings_dict, "set_status_msg_text_box").text
        if status_message_text != "Set your status message":
            raise AssertionError("expected text not founded")
        common.wait_for_and_click(device, settings_dict, "save_btn")
    time.sleep(display_time)


def verify_home_screen_is_disabled(device):
    print("feature is removed in 2023-U3 app")
    # if common.is_element_present(device, calls_dict, "user_profile_picture"):
    #     raise AssertionError(f"Home screen is still enabled on the device")
    # print(f"Home screen is not displayed, but proceeding further to check home screen option from settings page")
    # common.wait_for_and_click(device, navigation_dict, "Navigation")
    # common.wait_for_and_click(device, navigation_dict, "Settings_button")
    # settings_keywords.swipe_till_end(device)
    # common.sleep_with_msg(device, 5, "waiting for home screen toggle button")
    # if common.is_element_present(device, settings_dict, "homescreen_toggle_button"):
    #     raise AssertionError(f"Home screen option is available in Settings page on {device}")
    # common.wait_for_and_click(device, calls_dict, "Call_Back_Button")


def navigate_calls_tab_from_home_screen(device):
    common.wait_for_and_click(device, home_screen_dict, "call_tab")
    call_keywords.verify_calls_navigation(device)


def verify_home_screen_for_cnf_device(device):
    """Updated keyword as per new UI changes"""
    common.click_if_element_appears(device, home_screen_dict, "home_bar_icon", max_attempts=4)
    time.sleep(display_time)
    if not common.is_element_present(device, calendar_dict, "meet_now"):
        common.wait_for_element(device, calendar_dict, "calendar_tab")
        common.wait_for_element(device, people_dict, "people_tab")


def verify_DID_on_home_screen_for_cnf_device(device):
    phone_number = common.wait_for_element(device, calls_dict, "cnf_user_phone_num").text
    expected_phone_number = config["devices"][device]["meeting_user"]["pstndisplay"]
    if phone_number != expected_phone_number:
        raise AssertionError(f"{device} DID on home screen is {phone_number} not matched with {expected_phone_number}")


def verify_home_screen_date_and_time_for_cnf_device(device):
    date_and_time = common.wait_for_element(device, home_screen_dict, "hs_date_time").text
    print("Current date and time is:", date_and_time)


def verify_conference_room_name_on_home_screen(device):
    room_name = common.wait_for_element(device, home_screen_dict, "user_name").text
    expected_room_name = config["devices"][device]["meeting_user"]["displayname"]
    if room_name != expected_room_name:
        raise AssertionError(f"{device} Conference room name is {room_name} not matched with {expected_room_name}")


def verify_status_and_hotdesk_option(device):
    if not common.click_if_present(device, navigation_dict, "Navigation"):
        if common.is_portrait_mode_cnf_device(device):
            print(f"{device} doesn't have status and hot desk option")
            return
    common.wait_for_element(device, navigation_dict, "more_current_presence_btn")
    common.wait_for_element(device, hot_desk_dict, "hot_desk_btn")


def play_voicemail_from_home_screen(to_device, from_device):
    verify_voicemail_notification(to_device, from_device)
    common.wait_for_and_click(to_device, voicemail_dict, "voicemail_play_button")
    time.sleep(action_time)
    common.wait_for_and_click(to_device, voicemail_dict, "voicemail_play_button")


def delete_voicemail_from_home_screen(to_device, from_device):
    verify_voicemail_notification(to_device, from_device)
    common.wait_for_and_click(to_device, home_screen_dict, "delete_button")
    common.wait_for_and_click(to_device, home_screen_dict, "delete_ok_button")
    verify_clear_notification_button_on_home_screen(to_device, "disappear")


def verify_clear_notification_button_on_home_screen(device, status):
    if status.lower() not in ["appear", "disappear"]:
        raise AssertionError(f"{device}: Unexpected value for status: {status}")
    verify_home_screen_tiles(device)
    if status == "appear":
        common.common.wait_for_element(device, home_screen_dict, "clear_notification")
    elif status == "disappear":
        if common.is_element_present(device, home_screen_dict, "clear_notification"):
            raise AssertionError("Clear Notification button is visible on Home screen")


def place_call_on_home_screen_by_call_back_button(device):
    verify_home_screen_tiles(device)
    verify_clear_notification_button_on_home_screen(device, status="appear")
    common.wait_for_and_click(device, home_screen_dict, "call_back_button")
    if common.click_if_present(device, calls_dict, "myself_xpath"):
        print(f"*WARN*:: {device}: Found and used unexpected 'myself' OBO")
    common.wait_for_element(device, calls_dict, "Hang_up_button")


def verify_options_inside_hamburger_menu_on_home_screen(device):
    common.wait_for_and_click(device, calls_dict, "user_profile_picture")
    common.wait_for_element(device, navigation_dict, "Set_status_message")
    common.wait_for_element(device, navigation_dict, "hot_desk_btn")
    common.wait_for_element(device, navigation_dict, "Settings_button")
    common.wait_for_and_click(device, settings_dict, "user_displayname")
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")


def Verify_user_can_navigate_back_to_home_screen_in_call_and_navigate_to_different_apps(device):
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")
    verify_home_screen_tiles(device)
    call_keywords.click_on_calls_tab(device)
    common.wait_for_and_click(device, home_screen_dict, "home_bar_icon")
    verify_home_screen_tiles(device)
    time.sleep(action_time)
    if not common.click_if_present(device, home_screen_dict, "people_tab"):
        common.wait_for_and_click(device, home_screen_dict, "more_option")
        common.wait_for_and_click(device, home_screen_dict, "people_tab")
    common.wait_for_and_click(device, home_screen_dict, "home_bar_icon")
    verify_home_screen_tiles(device)
    common.wait_for_and_click(device, home_screen_dict, "calendar_tab")
    common.wait_for_and_click(device, home_screen_dict, "home_bar_icon")
    verify_home_screen_tiles(device)
    time.sleep(action_time)
    if not common.click_if_present(device, home_screen_dict, "voicemail_tab"):
        common.wait_for_and_click(device, home_screen_dict, "more_option")
        common.wait_for_and_click(device, home_screen_dict, "voicemail_tab")
    common.wait_for_and_click(device, home_screen_dict, "home_bar_icon")
    verify_home_screen_tiles(device)


def verify_home_screen_calls_pill_count(device):
    verify_home_screen_tiles(device)
    calls_pill_count = common.wait_for_element(device, home_screen_dict, "home_screen_calls_pill_count").text
    return int(calls_pill_count)


def verify_home_screen_voicemail_pill_count(device):
    verify_home_screen_tiles(device)
    voicemail_pill_count = common.wait_for_element(device, home_screen_dict, "home_screen_voicemail_pill_count").text
    return int(voicemail_pill_count)


def verify_home_button_in_different_tabs(device, tab):
    if tab.lower() == "calls_tab":
        call_keywords.click_on_calls_tab(device)
    elif tab.lower() == "voice_mail":
        voicemail_keywords.navigate_to_voicemail_tab(device)
    elif tab.lower() == "calendar":
        common.wait_for_and_click(device, home_screen_dict, "calendar_tab")
        common.wait_for_element(device, calendar_dict, "meet_now")
    elif tab.lower() == "walkie_talkie":
        if common.is_element_present(device, home_screen_dict, "more_option"):
            common.wait_for_and_click(device, home_screen_dict, "more_option")
            common.wait_for_and_click(device, home_screen_dict, "walkie_talkie_tab")
            common.wait_for_element(device, walkie_talkie_dict, "connect_button")
            return
        common.wait_for_and_click(device, home_screen_dict, "walkie_talkie_tab")
        common.wait_for_element(device, walkie_talkie_dict, "connect_button")
    elif tab.lower() == "people_tab":
        common.click_if_present(device, home_screen_dict, "people_tab")
        if not common.is_element_present(device, people_dict, "plus_icon"):
            common.wait_for_and_click(device, home_screen_dict, "more_option")
            common.wait_for_and_click(device, home_screen_dict, "people_tab")
            common.wait_for_element(device, people_dict, "plus_icon")
    else:
        raise AssertionError(f"Invalid tab value : {tab}")
    common.wait_for_element(device, home_screen_dict, "home_bar_icon")


def verify_home_screen_UI_for_cap(device, user_type="cap_search_enabled"):
    if user_type == "cap_search_disabled":
        if not (
            common.is_element_present(device, calls_dict, "call_park")
            and common.is_element_present(device, calls_dict, "people_tab")
        ):
            return
        raise AssertionError(f"{device}: is not sign-in with Cap Search Disabled account")
    common.wait_for_element(device, calls_dict, "call_park")
    if common.is_portrait_mode_cnf_device(device):
        common.wait_for_and_click(device, calls_dict, "people_tab")
    common.wait_for_element(device, calls_dict, "search")
    if common.is_portrait_mode_cnf_device(device):
        common.wait_for_and_click(device, calls_dict, "dialpad_tab")
    common.wait_for_element(device, calls_dict, "phone_number_with_backspace")
    actual_phn_number = config["devices"][device]["cap_search_enabled"]["phonenumber"]
    did_num = common.wait_for_element(device, calls_dict, "user_phone_num").text
    did_num1 = "".join(e for e in did_num if e.isalnum())
    if actual_phn_number != did_num1:
        raise AssertionError(
            f"Expected phone number: {did_num1} is not matching with actual phone number:{actual_phn_number}"
        )


def navigate_to_people_tab_from_home_screen_for_cap(device):
    common.wait_for_element(device, calls_dict, "call_park")
    if common.is_portrait_mode_cnf_device(device):
        common.wait_for_element(device, calls_dict, "dialpad_tab")
        common.wait_for_and_click(device, calls_dict, "people_tab")
    common.wait_for_element(device, calls_dict, "search")


def verify_options_when_tap_on_dial_pad_for_cap(device):
    common.wait_for_and_click(device, calendar_dict, "floating_dialpad_icon")
    common.wait_for_element(device, calls_dict, "make_a_call_text")
    common.wait_for_element(device, calls_dict, "dialpad_tab")
    common.wait_for_element(device, calls_dict, "people_tab")
    common.wait_for_element(device, calls_dict, "call_park")


def verify_dial_pad_in_calls_tab_for_cap(device):
    common.wait_for_and_click(device, home_screen_dict, "call_tab")
    common.wait_for_element(device, calls_dict, "Make_a_call")


def verify_app_bar_is_not_present_inside_tabs(device):
    time.sleep(action_time)
    if common.is_element_present(device, app_bar_dict, "more_tab"):
        raise AssertionError(f"{device} contains app bar more option inside other tabs")


def verify_app_bar_title_with_date_time_and_DID_number(device, other_user=None):
    # 'other_user' may be the 'device_name:usertype' whose credentials are being used by 'device':
    if other_user is None:
        device_name, account_type = common.decode_device_spec(device)
    else:
        device_name, account_type = common.decode_device_spec(other_user)

    expected_did_num = config["devices"][device_name][account_type]["pstndisplay"]
    print(f"{device}: Checking if my DID number for '{device_name}:{account_type}' == expected '{expected_did_num}'")
    if ":" in device:
        device = device.split(":")[0]
    common.wait_for_element(device, calls_dict, "user_profile_picture")
    if not common.is_element_present(device, home_screen_dict, "hs_date_time"):
        common.wait_for_element(device, home_screen_dict, "hs_date_time_for_cap")
    actual_did_num = common.wait_for_element(device, home_screen_dict, "hs_phonenum").text

    if expected_did_num != actual_did_num:
        raise AssertionError(
            f"{device}: expected DID number does not match actual: '{expected_did_num}' '{actual_did_num}'"
        )


def verify_home_screen_app_bar_user_navigates_back_from_other_tabs(device):
    specific_user_device = device
    account = "user"
    if ":" in device:
        user = device.split(":")[1]
        device = device.split(":")[0]
        print("User account : ", user)
        if user.lower() == "cap_search_enabled":
            account = "cap_search_enabled"
    print("Account :", account)
    common.wait_for_element(device, calls_dict, "user_profile_picture")
    time.sleep(action_time)
    if not common.click_if_present(device, calls_dict, "calls_tab"):
        common.wait_for_and_click(device, home_screen_dict, "more_option")
        common.wait_for_and_click(device, calls_dict, "calls_tab")
    time.sleep(display_time)
    common.wait_for_and_click(device, home_screen_dict, "home_bar_icon")
    verify_app_bar_title_with_date_time_and_DID_number(specific_user_device)
    if config["devices"][device]["model"].lower() in ["riverside", "riverside_13"]:
        print("CAP user doesn't have calendar tab")
    elif config["devices"][device]["model"].lower() == "olympia" and account == "cap_search_enabled":
        print("CAP user doesn't have calendar tab")
    else:
        common.wait_for_and_click(device, calendar_dict, "calendar_tab")
        time.sleep(display_time)
        common.wait_for_and_click(device, home_screen_dict, "home_bar_icon")
        verify_app_bar_title_with_date_time_and_DID_number(specific_user_device)
    time.sleep(action_time)
    if not common.click_if_present(device, home_screen_dict, "voicemail_tab"):
        common.wait_for_and_click(device, home_screen_dict, "more_option")
        common.wait_for_and_click(device, home_screen_dict, "voicemail_tab")
    time.sleep(display_time)
    common.wait_for_and_click(device, home_screen_dict, "home_bar_icon")
    verify_app_bar_title_with_date_time_and_DID_number(specific_user_device)
    time.sleep(action_time)
    if not common.click_if_present(device, walkie_talkie_dict, "walkie_talkie_tab"):
        common.wait_for_and_click(device, home_screen_dict, "more_option")
        common.wait_for_and_click(device, walkie_talkie_dict, "walkie_talkie_tab")
    time.sleep(display_time)
    common.wait_for_and_click(device, home_screen_dict, "home_bar_icon")
    verify_app_bar_title_with_date_time_and_DID_number(specific_user_device)
    time.sleep(action_time)
    if not common.click_if_present(device, home_screen_dict, "people_tab"):
        common.wait_for_and_click(device, home_screen_dict, "more_option")
        common.wait_for_and_click(device, home_screen_dict, "people_tab")
    time.sleep(display_time)
    common.wait_for_and_click(device, home_screen_dict, "home_bar_icon")
    verify_app_bar_title_with_date_time_and_DID_number(specific_user_device)


def click_on_home_bar_icon(device):
    common.wait_for_and_click(device, home_screen_dict, "home_bar_icon")


def verify_home_screen_more_option(device):
    common.wait_for_element(device, calls_dict, "user_profile_picture")
    common.wait_for_and_click(device, home_screen_dict, "more_option")
    common.wait_for_element(device, home_screen_dict, "reorder")
    if not common.click_if_present(device, home_screen_dict, "walkie_talkie_tab"):
        if not common.click_if_present(device, home_screen_dict, "people_tab"):
            if not common.click_if_present(device, home_screen_dict, "voicemail_tab"):
                if not common.click_if_present(device, calendar_dict, "calendar_tab"):
                    raise AssertionError(f"No tabs are present in more option in {device}")
    time.sleep(action_time)
    common.wait_for_and_click(device, home_screen_dict, "home_bar_icon")


def Verify_date_and_time_in_notification_bar_on_all_the_tabs(device, user_type="personal"):
    common.wait_for_element(device, calls_dict, "user_profile_picture")
    time.sleep(action_time)
    if not common.click_if_present(device, calls_dict, "calls_tab"):
        common.wait_for_and_click(device, home_screen_dict, "more_option")
        common.wait_for_and_click(device, calls_dict, "calls_tab")
    time.sleep(display_time)
    if common.is_element_present(device, home_screen_dict, "hs_date_time"):
        raise AssertionError(f"{device} calls tab contains time and date in notification bar")
    common.wait_for_and_click(device, home_screen_dict, "home_bar_icon")
    time.sleep(display_time)
    if not common.click_if_present(device, home_screen_dict, "voicemail_tab"):
        common.wait_for_and_click(device, home_screen_dict, "more_option")
        common.wait_for_and_click(device, home_screen_dict, "voicemail_tab")
    time.sleep(display_time)
    if common.is_element_present(device, home_screen_dict, "hs_date_time"):
        raise AssertionError(f"{device} voicemail tab contains time and date in notification bar")
    common.wait_for_and_click(device, home_screen_dict, "home_bar_icon")
    time.sleep(action_time)
    if not common.click_if_present(device, walkie_talkie_dict, "walkie_talkie_tab"):
        common.wait_for_and_click(device, home_screen_dict, "more_option")
        common.wait_for_and_click(device, walkie_talkie_dict, "walkie_talkie_tab")
    time.sleep(display_time)
    if common.is_element_present(device, home_screen_dict, "hs_date_time"):
        raise AssertionError(f"{device} walkie talkie tab contains time and date in notification bar")
    common.wait_for_and_click(device, home_screen_dict, "home_bar_icon")
    time.sleep(action_time)
    if not common.click_if_present(device, home_screen_dict, "people_tab"):
        common.wait_for_and_click(device, home_screen_dict, "more_option")
        common.wait_for_and_click(device, home_screen_dict, "people_tab")
    time.sleep(display_time)
    if common.is_element_present(device, home_screen_dict, "hs_date_time"):
        raise AssertionError(f"{device} people tab contains time and date in notification bar")
    common.wait_for_and_click(device, home_screen_dict, "home_bar_icon")
    if user_type.lower() == "cap_premium":
        print(f"{device} is in cap premium and does not support calendar tab")
        return
    else:
        if not common.click_if_present(device, calendar_dict, "calendar_tab"):
            common.wait_for_and_click(device, home_screen_dict, "more_option")
            common.wait_for_and_click(device, calendar_dict, "calendar_tab")
        time.sleep(display_time)
        if common.is_element_present(device, home_screen_dict, "hs_date_time"):
            raise AssertionError(f"{device} calender tab contains time and date in notification bar")


def verify_and_close_more_menu_options_on_home_screen(device):
    if common.is_element_present(device, home_screen_dict, "more_menu_container"):
        common.tap_outside_the_popup(device, common.wait_for_element(device, home_screen_dict, "more_menu_container"))
    common.wait_for_element(device, navigation_dict, "Navigation")


def navigate_to_reorder_tab(device):
    common.wait_for_and_click(device, home_screen_dict, "more_option")
    common.wait_for_and_click(device, home_screen_dict, "reorder")
    common.wait_for_element(device, home_screen_dict, "edit_navigation")


def verfy_and_reorder_homescreen_tiles(device, tab, destination, option="save"):
    if not option.lower() in ["save", "verify"]:
        raise AssertionError(f"Illegal option specified: {option}")
    print("device, tab, destination:", device, tab, destination)
    if tab.lower() == "calls":
        tab_dict = "call_tab"
    elif tab.lower() == "calendar":
        tab_dict = "calendar_tab"
    elif tab.lower() == "voicemail":
        tab_dict = "voicemail_tab"
    elif tab.lower() == "people":
        tab_dict = "people_tab"
    elif tab.strip().lower() == "walkie talkie".strip():
        tab_dict = "walkie_talkie_tab"
    else:
        raise AssertionError(f"Unexpected value for tab : {tab}")

    if destination.lower() == "calls":
        destination_dict = "call_tab"
    elif destination.lower() == "calendar":
        destination_dict = "calendar_tab"
    elif destination.lower() == "voicemail":
        destination_dict = "voicemail_tab"
    elif destination.lower() == "people":
        destination_dict = "people_tab"
    elif destination.strip().lower() == "walkie talkie".strip():
        destination = "walkie_talkie_tab"
    else:
        raise AssertionError(f"Unexpected value for destination : {destination}")

    common.perform_drag_and_drop(device, tab, app_bar_dict, tab_dict, destination, app_bar_dict, destination_dict)

    if option == "verify":
        common.wait_for_element(device, app_bar_dict, "save_button")
    elif option == "save":
        common.wait_for_and_click(device, app_bar_dict, "save_button")
    common.sleep_with_msg(device, 3, "Wait for sometime post clicking on the save button")


def get_destination_tab_on_home_screen(device):
    destination_tab = common.get_all_elements_texts(device, home_screen_dict, "home_screen_tiles")
    print(destination_tab)
    return destination_tab[2]


def select_tab_to_move(device):
    home_screen_tabs = common.get_all_elements_texts(device, home_screen_dict, "home_screen_tiles")
    print(home_screen_tabs)
    home_screen_tiles = ["Calls", "Calendar", "Voicemail", "People", "Walkie Talkie", "More"]
    change_tab = [tab for tab in home_screen_tiles if tab not in home_screen_tabs]
    print(change_tab)
    return change_tab[1]


def get_home_screen_tiles(device):
    home_screen_tiles = common.get_all_elements_texts(device, home_screen_dict, "home_screen_tiles")
    print(home_screen_tiles)
    return home_screen_tiles


def verify_updated_home_screen_tile_after_editing(before_changing, after_changing):
    if before_changing == after_changing:
        raise AssertionError(f"home screen tiles not changed:{before_changing},{after_changing}")
    print("home screen tile changed")


def verify_home_screen_tile_not_changed(before_changing, after_changing):
    if before_changing != after_changing:
        raise AssertionError(f"home screen tiles have changed:{before_changing},{after_changing}")
    print("home screen tile not changed")


def navigate_to_tab(device, tab):
    if tab.lower() == "calls":
        call_keywords.navigate_to_calls_tab(device)
    elif tab.lower() == "calendar":
        calendar_keywords.navigate_to_calendar_tab(device)
    elif tab.lower() == "voicemail":
        voicemail_keywords.navigate_to_voicemail_tab(device)
    elif tab.lower() == "people":
        people_keywords.navigate_to_people_tab(device)
    elif tab.strip().lower() == "walkie talkie".strip():
        walkie_talkie_keywords.navigate_to_walkie_talkie_tab(device)
    else:
        raise AssertionError(f"Unexpected value for tab : {tab}")


def get_the_tab_moved_to_more_option(device, before_changing, after_changing):
    print(device, before_changing, after_changing)
    change_tab = [tab for tab in before_changing if tab not in after_changing]
    print(change_tab)
    return change_tab[0]


def get_destination_tab_on_home_screen_except_walkie_talkie(device):
    home_scree_tabs = common.get_all_elements_texts(device, home_screen_dict, "home_screen_tiles")
    destination_tab = [
        tab.strip() for tab in home_scree_tabs if "Walkie Talkie".strip() not in tab and "More" not in tab
    ]
    print(destination_tab)
    return destination_tab[-1]


def verify_home_screen_missed_call_notification(device, to_device, call_type):
    if not call_type.lower() in ["missed_call", "missed_transfer", "missed_forward", "private_line"]:
        raise AssertionError(f"Illegal option specified: {call_type}")
    if call_type.lower() == "missed_call":
        common.wait_for_element(device, home_screen_dict, "missed_call")
    elif call_type.lower() == "missed_transfer":
        common.wait_for_element(device, home_screen_dict, "missed_transfer")
    elif call_type.lower() == "missed_forward":
        common.wait_for_element(device, home_screen_dict, "missed_forward")
    elif call_type.lower() == "private_line":
        common.wait_for_element(device, home_screen_dict, "missed_call")
        common.wait_for_element(device, calls_dict, "private_line")
    common.wait_for_element(device, home_screen_dict, "call_back_button")
    common.wait_for_element(device, home_screen_dict, "call_time_stamp")
    expected_display_name = common.device_displayname(to_device)
    actual_display_name = common.wait_for_element(device, calls_dict, "caller_name_in_hold_banner").text
    if actual_display_name != expected_display_name:
        raise AssertionError(
            f"{actual_display_name} Caller name in the miss call banner is not as expected {expected_display_name}"
        )


def navigate_to_dial_pad_tab_from_home_screen(device):
    for i in range(2):
        common.click_if_present(device, calls_dict, "Call_Back_Button")
        common.click_if_present(device, home_screen_dict, "home_bar_icon")
    common.wait_for_and_click(device, calls_dict, "calls_tab")
    common.wait_for_element(device, calls_dict, "call_park")
    if common.is_hard_dial_pad_present(device):
        common.wait_for_element(device, calls_dict, "use_hard_keys_to_dial_a_number")
    else:
        if common.is_portrait_mode_cnf_device(device):
            common.wait_for_and_click(device, calls_dict, "Make_a_call")
            common.wait_for_and_click(device, calls_dict, "dialpad_tab")
            common.wait_for_element(device, people_dict, "people_tab_cap")
            common.wait_for_element(device, calls_dict, "call_as_myself_history_button")
        common.wait_for_element(device, calls_dict, "soft_dial_pad")
    common.wait_for_element(device, calls_dict, "call_park")
    common.wait_for_element(device, calls_dict, "phone_number")
    common.wait_for_element(device, calls_dict, "backspace")
    common.wait_for_element(device, calls_dict, "call_icon1")
    common.click_if_present(device, calls_dict, "Call_Back_Button")
    common.click_if_present(device, home_screen_dict, "home_bar_icon")


def verify_home_screen_tabs_and_more_option_tabs(device):
    home_screen_tabs = common.get_all_elements_texts(device, home_screen_dict, "home_screen_tiles")
    expected_home_screen_tiles = ["Calls", "Calendar", "Voicemail", "People", "Walkie Talkie", "More"]
    expected_tab_in_more_option = [tab for tab in expected_home_screen_tiles if tab not in home_screen_tabs]
    print(expected_tab_in_more_option)
    common.wait_for_and_click(device, home_screen_dict, "more_option")
    common.wait_for_element(device, home_screen_dict, "reorder")
    for tab in expected_tab_in_more_option:
        tmp_dict = common.get_dict_copy(home_screen_dict, "search_result_for_tabs", "tab_name", tab)
        common.wait_for_element(device, tmp_dict, "search_result_for_tabs", "xpath")
    verify_and_close_more_menu_options_on_home_screen(device)


def verify_home_screen_meeting_notification(device, meeting):
    common.click_if_present(device, home_screen_dict, "home_bar_icon")
    common.wait_for_element(device, home_screen_dict, "meeting_join_button")
    common.wait_for_element(device, home_screen_dict, "cross_icon")
    expected_notification_name = meeting
    actual_meeting_name = common.wait_for_element(device, home_screen_dict, "notification_meeting_name").text
    if actual_meeting_name.lower() != expected_notification_name.lower():
        raise AssertionError(
            f"{actual_meeting_name} meeting name is not same as expected: {expected_notification_name}"
        )
