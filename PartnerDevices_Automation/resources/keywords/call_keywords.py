from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
import call_views_keywords
import people_keywords
from initiate_driver import obj_dev as obj
from initiate_driver import config
from urllib3.exceptions import ProtocolError
import settings_keywords
import subprocess
import time
import common
import threading
from Libraries.Selectors import load_json_file
from selenium.webdriver.common.by import By
import calendar_keywords
import device_settings_keywords
import home_screen_keywords
import tr_home_screen_keywords
import lcp_calls
import call_keywords

display_time = 2
action_time = 3
recording_wait_time = 15
call_log_sync = 10

calls_dict = load_json_file("resources/Page_objects/Calls.json")
calendar_dict = load_json_file("resources/Page_objects/Calendar.json")
common_dict = load_json_file("resources/Page_objects/Common.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")
tr_Signin_dict = load_json_file("resources/Page_objects/tr_Signin.json")
tr_home_screen_dict = load_json_file("resources/Page_objects/tr_home_screen.json")
tr_calls_dict = load_json_file("resources/Page_objects/tr_calls.json")
tr_calendar_dict = load_json_file("resources/Page_objects/tr_calendar.json")
tr_device_settings_dict = load_json_file("resources/Page_objects/tr_device_settings.json")
navigation_dict = load_json_file("resources/Page_objects/Navigation.json")
app_bar_dict = load_json_file("resources/Page_objects/App_bar.json")
device_settings_dict = load_json_file("resources/Page_objects/Device_settings.json")
panels_device_settings_dict = load_json_file("resources/Page_objects/panels_device_settings.json")
home_screen_dict = load_json_file("resources/Page_objects/Home_screen.json")
people_dict = load_json_file("resources/Page_objects/People.json")
voicemail_dict = load_json_file("resources/Page_objects/Voicemail.json")
lcp_calls_dict = load_json_file("resources/Page_objects/lcp_calls.json")
call_view_dict = load_json_file("resources/Page_objects/Call_views.json")
tr_console_settings_dict = load_json_file("resources/Page_objects/rooms_console_settings.json")
tr_console_home_screen_dict = load_json_file("resources/Page_objects/rooms_console_home_screen.json")


def navigate_to_calls_tab(device):
    if ":" in device:
        device = device.split(":")[0]
    print("device :", device)
    devices = device.split(",")
    for device in devices:
        while common.click_if_present(device, common_dict, "back") or common.click_if_present(
            device, calls_dict, "Call_Back_Button"
        ):
            common.sleep_with_msg(device, 3, "Clicked on 'back'")
        if common.is_lcp(device):
            common.click_if_present(device, common_dict, "home_btn")
        common.click_if_present(device, home_screen_dict, "home_bar_icon")
        status = verify_calls_navigation(device)
        if status is True:
            print(f"{device}: Already on Calls Tab")
        else:
            common.wait_for_and_click(device, calls_dict, "calls_tab")
        if common.is_lcp(device):
            common.wait_for_element(device, calls_dict, "calls_list")
            return
        time.sleep(action_time)
        if not common.is_element_present(device, calls_dict, "search_contact_box"):
            common.wait_for_and_click(device, calls_dict, "recent_tab")


def click_on_calls_tab(device):
    devices = device.split(",")
    for device in devices:
        common.wait_for_and_click(device, calls_dict, "calls_tab")
        if common.is_lcp(device):
            common.wait_for_element(device, lcp_calls_dict, "call_unpark_more_option")
        else:
            common.wait_for_element(device, calls_dict, "unpark_call")


def verify_calls_navigation(device):
    if common.is_lcp(device):
        if common.is_element_present(device, calls_dict, "recent_tab"):
            return True
        else:
            return False
    if not common.is_element_present(device, calls_dict, "Header", "id"):
        return False
    head_text = common.wait_for_element(device, calls_dict, "Header", "id").text
    print(f"{device}: Heading text: ", head_text)
    return head_text == "Calls"


def place_call(from_device, to_device, method, obo_option=None, boss_list=None):
    print(
        f"from_device: {from_device}, to_device: {to_device}, method: {method}",
    )
    if not method.lower() in ["display_name", "phone_number", "extension_number", "username", "privateline_number"]:
        raise AssertionError(f"Illegal method specified: '{method}'")

    if common.is_lcp(from_device):
        common.wait_for_and_click(from_device, calls_dict, "search_icon")
    else:
        # For CAP user and Conf user
        if (
            common.is_element_present(from_device, people_dict, "people_tab_cap")
            or common.is_element_present(from_device, calendar_dict, "app_bar_dialpad_icon")
            or common.is_element_present(from_device, calls_dict, "search")
        ):
            if not common.is_element_present(from_device, calls_dict, "search"):
                people_keywords.navigate_to_people_tab(from_device)
        # For other users
        else:
            navigate_to_calls_tab(from_device)
        common.wait_for_and_click(from_device, calls_dict, "search")

    if method.lower() in ["display_name", "username"]:
        if method.lower() == "display_name":
            displayname = common.device_displayname(to_device)
        elif method.lower() == "username":
            displayname = common.device_username(to_device)

        print(f"diaplay name: {displayname}")
        common.wait_for_element(from_device, calls_dict, "search_text").send_keys(displayname)
        common.hide_keyboard(from_device)
        tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", displayname)
        common.wait_for_and_click(from_device, tmp_dict, "search_result_item_container", "xpath")
        if common.is_lcp(from_device):
            settings_keywords.swipe_till_end(from_device)
            # settings_keywords.swipe_till_end(from_device)
            # settings_keywords.swipe_till_end(from_device)
        common.wait_for_and_click(from_device, calls_dict, "Make_an_audio_call")
        common.wait_while_present(from_device, calls_dict, "Make_an_audio_call")

    elif method.lower() == "phone_number":
        pstn_displayname = common.device_pstndisplay(to_device)
        print(f"phone number: {pstn_displayname}")
        common.wait_for_element(from_device, calls_dict, "search_text").send_keys(pstn_displayname)
        tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", pstn_displayname)
        common.wait_for_and_click(from_device, tmp_dict, "search_result_item_container", "xpath")
        # if common.is_lcp(from_device):
        #     settings_keywords.swipe_till_end(from_device)
        #     settings_keywords.swipe_till_end(from_device)
        #     phone_no = "+" + common.device_phonenumber(to_device)
        #     print(phone_no)
        #     tmp_dict = common.get_dict_copy(
        #         lcp_calls_dict, "lcp_call_using_phone_no", "replace_with_phone_no", phone_no
        #     )
        #     common.wait_for_and_click(from_device, tmp_dict, "lcp_call_using_phone_no")

    elif method.lower() == "extension_number":
        extnumber = common.device_extention_number(to_device)
        print(f"extension number: {extnumber}")
        common.wait_for_element(from_device, calls_dict, "search_text").send_keys(extnumber)
        time.sleep(action_time)
        common.wait_for_and_click(from_device, calls_dict, "search_result_item_container")

    elif method.lower() == "privateline_number":
        privateline_number = common.device_privateline_number(to_device)
        print(f"phone number: {privateline_number}")
        common.wait_for_element(from_device, calls_dict, "search_text").send_keys(privateline_number)
        tmp_dict = common.get_dict_copy(
            calls_dict, "search_result_item_container", "config_display", privateline_number
        )
        common.wait_for_and_click(from_device, tmp_dict, "search_result_item_container", "xpath")

    if obo_option:
        if boss_list:
            verify_call_behalf_of_bosses_list(from_device, boss_list)
        choose_call_behalf_of(from_device, obo_option)
    else:
        # It is possible some cleanup did not happen - detect unexpected OBO:
        if common.click_if_present(from_device, calls_dict, "myself_xpath"):
            print(f"*WARN*:: {from_device}: Found and used unexpected 'myself' OBO")
    common.wait_for_element(from_device, calls_dict, "Hang_up_button")


def make_a_call_by_selecting_the_user_from_call_history(from_device, to_device):
    print("from_device :", from_device)
    print("to_device :", to_device)
    driver = obj.device_store.get(alias=from_device)
    search_result_xpath = (calls_dict["call_participant_name"]["xpath"]).replace(
        "config_display", config["devices"][to_device]["user"]["displayname"]
    )
    print("Search result xpath : ", search_result_xpath)
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((MobileBy.XPATH, search_result_xpath))).click()
    time.sleep(display_time)
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calls_dict["Make_an_audio_call"]["xpath"]))
        ).click()
    except Exception as e:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calls_dict["Make_an_audio_call"]["xpath1"]))
        ).click()
    print("Clicked on Call icon")


def make_outgoing_call_using_from_dial_pad(from_device, to_device):
    print(f"from_device: {from_device}, to_device: {to_device}")
    phonenumber = common.device_phonenumber(to_device)
    time.sleep(display_time)
    common.click_if_present(from_device, calls_dict, "calls_tab")
    time.sleep(display_time)
    if not common.is_element_present(from_device, calls_dict, "dial_pad_field"):
        if not common.click_if_present(from_device, calls_dict, "Make_a_call"):
            common.wait_for_and_click(from_device, calendar_dict, "calendar_tab")
            common.wait_for_and_click(from_device, calls_dict, "Make_a_call")
    common.wait_for_and_click(from_device, calls_dict, "dial_pad_field")
    element = common.wait_for_element(from_device, calls_dict, "entered_phn_num")
    element.clear()
    time.sleep(display_time)
    element.set_value(phonenumber)
    print(f"{from_device}: Entered the phone number")
    if config["devices"][from_device]["model"].lower() == "phoenix":
        common.wait_for_and_click(from_device, calls_dict, "call", "id_arizona")
    common.sleep_with_msg(from_device, 3, "Waiting for BOB call pop-up, if any")
    if common.click_if_present(from_device, calls_dict, "myself_xpath"):
        print(f"*WARN*:: {from_device}: Found and used unexpected 'myself' OBO")
    common.wait_for_element(from_device, calls_dict, "Hang_up_button")


def make_outgoing_call_using_from_call_icon(from_device, to_device, call_from="recent"):
    if call_from.lower() not in ["recent", "favorites"]:
        raise AssertionError(f"{from_device}: Invalid option specified for call from: {call_from}")
    print(f"from_device: {from_device}, to_device: {to_device}, call_from: {call_from}")
    to_device, account = common.decode_device_spec(to_device)
    if account != "user":
        displayname = config["devices"][to_device][account]["phonenumber"]
        pstn_display = config["devices"][to_device][account]["pstndisplay"]
    else:
        displayname = config["devices"][to_device][account]["displayname"]
    navigate_to_calls_tab(from_device)
    if call_from == "favorites":
        common.wait_for_and_click(from_device, calls_dict, "favorites_tab")
    if common.is_portrait_mode_cnf_device(from_device):
        common.wait_for_and_click(from_device, calls_dict, "Make_a_call")
        common.wait_for_and_click(from_device, calls_dict, "people_tab")
        common.wait_for_element(from_device, calls_dict, "search_contact_box").send_keys(displayname)
        common.wait_for_and_click(from_device, calls_dict, "call_icon")
    else:
        common.wait_for_and_click(from_device, calls_dict, "search")
        common.wait_for_element(from_device, calls_dict, "search_text").send_keys(displayname)
        common.hide_keyboard(from_device)
        common.sleep_with_msg(from_device, 7, "Waiting for search results to appear")
        temp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", displayname)
        if not common.click_if_present(from_device, temp_dict, "search_result_item_container", "xpath"):
            if account == "user":
                raise AssertionError(f"{from_device}: Couldn't find the expected search results")
            temp_dict1 = common.get_dict_copy(
                calls_dict, "search_result_item_container", "config_display", pstn_display
            )
            common.wait_for_and_click(from_device, temp_dict1, "search_result_item_container", "xpath")
            time.sleep(3)
        common.click_if_present(from_device, calls_dict, "Make_an_audio_call")
    if common.click_if_present(from_device, calls_dict, "myself_xpath"):
        print(f"*WARN*:: {from_device}: Found and used unexpected 'myself' OBO")
    common.wait_for_element(from_device, calls_dict, "Hang_up_button")


def come_back_to_home_screen(device_list, disconnect=True):
    common.run_parallel(device_list, navigate_to_landing_page, disconnect=disconnect)


def navigate_to_landing_page(device, disconnect):
    """
    Cleanup method for call scenarios when navigation workflow is unimportant.
    """
    if is_call_more_options_open(device):
        dismiss_call_more_options(device)

    if disconnect:
        # TODO: This is NOT a verify call, just a wrapper for 'disconnect_call'.
        verify_call_state_and_disconnect(device)

    if common.is_norden(device):
        if not common.click_if_present(device, tr_console_settings_dict, "back_layout"):
            common.click_if_present(device, tr_calls_dict, "close_dial_pad_button")

        if tr_home_screen_keywords.is_home(device):
            return

    for attempt in range(6):
        if not (
            common.click_if_present(device, calls_dict, "Call_Back_Button")
            or common.click_if_present(device, calls_dict, "Close_Call_Rating")
            or common.click_if_present(device, tr_device_settings_dict, "back_button")
            or common.click_if_present(device, device_settings_dict, "admin_settings_yes")
            or common.click_if_present(device, panels_device_settings_dict, "close_button")
            or common.click_if_present(device, home_screen_dict, "home_bar_icon")
            or common.click_if_present(device, common_dict, "home_btn")
            or common.click_if_present(device, panels_device_settings_dict, "admin_back_button")
            or common.click_if_present(device, calendar_dict, "close_button")
        ):
            break
        common.sleep_with_msg(device, 3, f"React to 'Call_Back_Button' click, attempt: {attempt}.")
    if common.is_element_present(device, calls_dict, "Call_Back_Button"):
        raise AssertionError(f"{device}: 'Call_Back_Button' still present after {attempt} clicks")
    common.click_if_present(device, tr_console_settings_dict, "back_layout")
    common.click_if_present(device, calendar_dict, "close_button")


def pick_incoming_call(device):
    for device_name in device.split(","):
        print(f"{device_name}: Accepting incoming call")
        common.wait_for_and_click(device_name, calls_dict, "Accept_call_button")
        common.wait_while_present(device_name, calls_dict, "Accept_call_button")


def rejects_the_incoming_call(device_list):
    for device_name in device_list.split(","):
        print(f"{device_name}: Rejecting incoming call")
        if common.is_lcp(device_list):
            common.wait_for_and_click(device_name, lcp_calls_dict, "incoming_call_decline")
            common.wait_while_present(device_name, lcp_calls_dict, "incoming_call_decline")
            return
        common.wait_for_and_click(device_name, calls_dict, "Hang_up_button")
        common.wait_while_present(device_name, calls_dict, "Hang_up_button")


def disconnect_call(device):
    if isinstance(device, str):
        devices = device.split(",")
    elif isinstance(device, list):
        devices = device
    time.sleep(5)
    for device in devices:
        common.click_if_present(device, calls_dict, "call_bar")
        common.wait_for_and_click(device, calls_dict, "Hang_up_button")
        common.wait_while_present(device, calls_dict, "Hang_up_button")
        for _ in range(2):
            common.sleep_with_msg(device, 2, "Allow any post-hangup Call_Rating to appear")
            if common.click_if_present(device, calls_dict, "Close_Call_Rating"):
                break
            if common.click_if_present(device, tr_calls_dict, "call_rating_dismiss"):
                break
            # Workaround for https://domoreexp.visualstudio.com/MSTeams/_workitems/edit/3209418 remove this, and selectors when fixed:
            if common.is_element_present(device, calls_dict, "rejoin_meeting_button"):
                common.wait_for_and_click(device, calls_dict, "rejoin_meeting_button_dismiss")
                print(f"{device}: WARN: Dismissed unexpected 'rejoin' button")
                break


def verify_call_state(device_list, state):
    if isinstance(device_list, str):
        devices = device_list.split(",")
    elif isinstance(device_list, list):
        devices = device_list
    print(f"Devices : {devices}, State: {state}")
    if state.lower() not in ["connected", "disconnected", "hold", "resume"]:
        raise AssertionError(f"Invalid state specified: {state}")
    time.sleep(5)
    for device in devices:
        print("device : ", device)
        if state.lower() == "connected":
            time.sleep(action_time)
            common.click_if_present(device, calls_dict, "call_action_bar")
            common.wait_for_element(device, calls_dict, "Hang_up_button")
        elif state.lower() == "disconnected":
            time.sleep(action_time)
            if common.is_element_present(device, calls_dict, "call_bar") or common.is_element_present(
                device, calendar_dict, "hang_up_btn"
            ):
                raise AssertionError(f"{device}: User is still in call")
            if common.is_norden(device):
                if not common.is_element_present(device, calls_dict, "end_call_callee_text"):
                    common.click_if_present(device, tr_calls_dict, "call_rating_dismiss")
                    common.click_if_present(device, calls_dict, "Close_Call_Rating")
                common.wait_for_element(device, tr_calls_dict, "more_button")
            else:
                common.click_if_present(device, calls_dict, "Close_Call_Rating")
                if not common.is_element_present(device, calls_dict, "tool_bar") and not common.is_element_present(
                    device, calls_dict, "user_profile_picture"
                ):
                    common.is_element_present(device, home_screen_dict, "home_bar_icon")
        elif state.lower() == "hold":
            common.click_if_present(device, calls_dict, "call_bar")
            if common.is_norden(device):
                time.sleep(3)
                common.wait_for_element(device, calls_dict, "call_on_hold")
            else:
                common.sleep_with_msg(device, 15, "Time for call to be held or for hold banner to appear")
                if not common.is_element_present(device, calls_dict, "callstatus_on_hold"):
                    elem_txt = common.wait_for_element(device, calls_dict, "hold_label_time").text.lower()
                    print(f"Hold text displayed on {device} is: {elem_txt}")
                    if "on hold" not in elem_txt:
                        raise AssertionError(f"Call is not in hold mode")
                print("Call on hold present in top Bar, call is on hold")
        elif state.lower() == "resume":
            common.wait_for_element(device, calls_dict, "Hang_up_button")
            common.wait_for_element(device, calls_dict, "call_more_options")


def open_call_details_item(from_device, to_device):
    # verify we have a list to select from:
    if not verify_calls_navigation(from_device):
        raise AssertionError(f"{from_device}: open_call_details_item: Not on Calls page")

    to_device_displayname = common.device_displayname(to_device)
    print(f"{from_device}: open_call_details_item: {to_device_displayname}")
    tmp_dict = common.get_dict_copy(calls_dict, "call_participant_name", "config_display", to_device_displayname)
    common.wait_for_and_click(from_device, tmp_dict, "call_participant_name", selector_key="xpath")

    # wait for container to open
    common.wait_for_element(from_device, calls_dict, "calls_item_options_container")


def verify_call_entries_are_synced_in_call_log(from_device, to_device, state="duration"):
    navigate_to_calls_tab(from_device)
    settings_keywords.refresh_calls_main_tab(from_device)
    common.click_if_element_appears(from_device, calls_dict, "ongoing_in_recent_tab", max_attempts=5)
    to_device_displayname_list = []
    for device_name in to_device.split(","):
        to_device_displayname = common.device_displayname(device_name)
        to_device_displayname_list.append(to_device_displayname)

    participant_list = common.get_all_elements_texts(from_device, calls_dict, "call_participant_name")
    call_details_list = common.get_all_elements_texts(from_device, calls_dict, "call_log_duration")

    for participant, to_device_displayname, call_detail in zip(
        participant_list, to_device_displayname_list, call_details_list
    ):
        if participant in to_device_displayname_list:
            if state.lower() == "duration":
                if not "sec" in call_detail:
                    raise AssertionError(f"{from_device}: Could not find 'sec' in '{call_detail}'")
            elif state.lower() == "missed":
                if not "Missed" in call_detail:
                    raise AssertionError(f"{from_device}: Could not find 'Missed' in '{call_detail}'")
            elif state.lower() == "forwarded_to":
                if not "Forwarded to:" in call_detail:
                    raise AssertionError(f"{from_device}: Could not find 'Forwarded to' in '{call_detail}'")
            else:
                raise AssertionError(f"Invalid state specified: {state}")
        else:
            raise AssertionError(f"{participant} participant name not matched with {to_device_displayname_list}")


def verify_name_of_caller_and_receiver_displayed(from_device, to_device):
    from_device_displayname = common.device_displayname(from_device)
    to_device_displayname = common.device_displayname(to_device)
    tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", to_device_displayname)
    common.wait_for_element(from_device, tmp_dict, "search_result_item_container", "xpath")
    tmp_dict1 = common.get_dict_copy(
        calls_dict, "search_result_item_container", "config_display", from_device_displayname
    )
    if ":" in to_device:
        to_device = to_device.split(":")[0]
    common.wait_for_element(to_device, tmp_dict1, "search_result_item_container", "xpath")


def verify_call_mute_state(device_list, state):
    if not state.lower() in ["mute", "unmute"]:
        raise AssertionError(f"Illegal state specified: '{state}'")
    devices = device_list.split(",")
    print("Devices : ", devices)
    for device in devices:
        common.wait_for_element(device, calls_dict, "Hang_up_button")
        if state.lower() == "mute":
            if not common.is_element_present(device, calls_dict, "call_verify_muted"):
                common.wait_for_element(device, calls_dict, "meeting_verify_muted")
        elif state.lower() == "unmute":
            if not common.is_element_present(device, calls_dict, "call_verify_unmuted"):
                common.wait_for_element(device, calls_dict, "meeting_verify_unmuted")


def mutes_the_phone_call(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    time.sleep(action_time)
    if not (
        common.is_element_present(device, calls_dict, "call_verify_muted")
        or common.is_element_present(device, calls_dict, "meeting_verify_muted")
    ):
        if not common.click_if_present(device, calls_dict, "call_verify_unmuted"):
            common.wait_for_and_click(device, calls_dict, "meeting_verify_unmuted")


def unmutes_the_phone_call(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    time.sleep(action_time)
    if not (
        common.is_element_present(device, calls_dict, "call_verify_unmuted")
        or common.is_element_present(device, calls_dict, "meeting_verify_unmuted")
    ):
        if not common.click_if_present(device, calls_dict, "call_verify_muted"):
            common.wait_for_and_click(device, calls_dict, "meeting_verify_muted")


def hold_the_call(device):
    print("Hold the phone call : ", device)
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    if not common.click_if_present(device, calls_dict, "Put_call_on_hold"):
        common.wait_for_and_click(device, calls_dict, "call_more_options")
        if not common.click_if_present(device, calls_dict, "Put_call_on_hold"):
            common.wait_for_and_click(device, calendar_dict, "Put_call_on_hold")


def resume_the_call(device):
    print("Resume the phone call : ", device)
    time.sleep(display_time)
    if not common.click_if_present(device, calls_dict, "Resume"):
        common.wait_for_and_click(device, calls_dict, "Resume_banner_icon")
    common.wait_for_element(device, calls_dict, "Hang_up_button")


def blindtransfers_the_call(from_device, to_device, method):
    if method not in ["display_name", "phone_number"]:
        raise AssertionError(f"Illegal method specified: '{method}'")
    print(f"from_device : {from_device}, to_device: {to_device}, method: {method}")
    displayname = common.device_displayname(to_device)
    pstn_displayname = common.device_pstndisplay(to_device)
    username, password, contact_device, account_type = common.get_credentials(to_device)
    username = username.split("@")[0]
    if method == "display_name":
        text_to_call = username
        tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", displayname)
    elif method == "phone_number":
        text_to_call = pstn_displayname
        tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", pstn_displayname)
    print("search text :", text_to_call)
    common.wait_for_element(from_device, calls_dict, "Hang_up_button")
    if not common.click_if_present(from_device, calls_dict, "Transfer"):
        common.wait_for_and_click(from_device, calls_dict, "call_more_options")
        common.wait_for_and_click(from_device, calls_dict, "Transfer")
    common.wait_for_and_click(from_device, calls_dict, "Transfer_now")
    time.sleep(display_time)
    if not common.is_element_present(from_device, calls_dict, "dial_pad1"):
        common.wait_for_element(from_device, calls_dict, "call_dial_pad")
    if common.is_lcp(from_device):
        common.wait_for_and_click(from_device, calls_dict, "search_contact_button")
    elem = common.wait_for_element(from_device, calls_dict, "search_contact_box")
    elem.send_keys(text_to_call)
    common.hide_keyboard(from_device)
    common.wait_for_and_click(from_device, tmp_dict, "search_result_item_container", "xpath")
    common.sleep_with_msg(from_device, 3, "Waiting for any OBO call pop-up")
    if common.click_if_present(from_device, calls_dict, "myself_xpath"):
        print(f"*WARN*:: {from_device}: Found and used unexpected 'myself' OBO")
    common.wait_for_element(from_device, calls_dict, "Hang_up_button")


def consult_first_to_transfer_the_call(from_device, to_device, method, obo_option=None):
    if not method in ["display_name", "phone_number"]:
        raise AssertionError(f"Illegal method specified: '{method}'")
    username, password, to_device, account = common.get_credentials(to_device)
    displayname = config["devices"][to_device][account]["displayname"]
    username = username.split("@")[0]
    pstn_displayname = config["devices"][to_device][account]["pstndisplay"]
    print("Display, user id, phone number : ", displayname, username, pstn_displayname)
    print(f"from_device : {from_device}, to_device: {to_device}, method: {method}")
    if method == "display_name":
        text_to_call = username
        tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", displayname)
    elif method == "phone_number":
        text_to_call = pstn_displayname
        tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", pstn_displayname)
    print("search text :", text_to_call)
    common.wait_for_element(from_device, calls_dict, "Hang_up_button")
    if not common.click_if_present(from_device, calls_dict, "Transfer"):
        common.wait_for_and_click(from_device, calls_dict, "call_more_options")
        common.wait_for_and_click(from_device, calls_dict, "Transfer")
    common.wait_for_and_click(from_device, calls_dict, "consult_first")
    time.sleep(display_time)
    if not common.is_element_present(from_device, calls_dict, "dial_pad1"):
        common.wait_for_element(from_device, calls_dict, "call_dial_pad")
    if common.is_lcp(from_device):
        common.wait_for_and_click(from_device, calls_dict, "search_contact_button")
    elem = common.wait_for_element(from_device, calls_dict, "search_contact_box")
    elem.send_keys(text_to_call)
    common.hide_keyboard(from_device)
    common.wait_for_and_click(from_device, tmp_dict, "search_result_item_container", "xpath")
    if obo_option:
        choose_call_behalf_of(from_device, obo_option)
    else:
        # It is possible some cleanup did not happen - detect unexpected OBO:
        if common.click_if_present(from_device, calls_dict, "myself_xpath"):
            print(f"*WARN*:: {from_device}: Found and used unexpected 'myself' OBO")
    common.wait_for_element(from_device, calls_dict, "Hang_up_button")


def completes_the_consultation_to_accept_the_call(from_device, to_device):
    if common.is_lcp(from_device):
        common.wait_for_and_click(from_device, lcp_calls_dict, "lcp_call_bar_entry_more_option")
        common.wait_for_and_click(from_device, calls_dict, "Transfer")
    else:
        common.wait_for_and_click(from_device, calls_dict, "transfer_button")
    common.click_if_present(from_device, calls_dict, "ok")


def escalating_to_conference_call(from_device, to_device, method):
    print(f"from device: {from_device}, to device: {to_device}, method: {method}")
    username, password, to_device, account = common.get_credentials(to_device)
    username = username.split("@")[0]
    displayname = config["devices"][to_device][account]["displayname"]
    pstn_displayname = config["devices"][to_device][account]["pstndisplay"]

    if not (
        common.click_if_present(from_device, calls_dict, "Add_participants_button")
        or common.click_if_present(from_device, calls_dict, "showRoster")
    ):
        raise AssertionError(f"Couldn't navigate to add participant page")
    common.wait_for_and_click(from_device, calls_dict, "Invite_new_user")

    if method == "display_name":
        common.wait_for_element(from_device, calls_dict, "search_contact_box").send_keys(username)
        temp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", displayname)
        common.wait_for_and_click(from_device, temp_dict, "search_result_item_container", "xpath")
    elif method == "phone_number":
        common.wait_for_element(from_device, calls_dict, "search_contact_box").send_keys(pstn_displayname)
        temp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", pstn_displayname)
        common.wait_for_and_click(from_device, temp_dict, "search_result_item_container", "xpath")
    common.wait_for_and_click(from_device, calls_dict, "save_contacts")
    common.sleep_with_msg(from_device, 3, "Waiting for any OBO call pop-up")
    if common.click_if_present(from_device, calls_dict, "myself_xpath"):
        print(f"*WARN*:: {from_device}: Found and used unexpected 'myself' OBO")


def dial_and_verify_the_numbers_from_0_to_9(device_list):
    devices = device_list.split(",")
    print("Devices : ", devices)

    expected = "+9876543210"

    for device in devices:
        if common.is_screen_size_7_inch_or_more(device):
            common.wait_for_and_click(device, calls_dict, "calls_tab")
        time.sleep(action_time)
        if not common.is_norden(device):
            # Handle devices offering an early Make-Call button:
            if common.click_if_present(device, calls_dict, "Make_a_call"):
                time.sleep(1)
            else:
                if not (
                    common.is_element_present(device, calendar_dict, "app_bar_dialpad_icon")
                    or common.is_element_present(device, calls_dict, "dial_pad_field")
                ):
                    navigate_to_calls_tab(device)
                    time.sleep(2)

        # Use hard/soft dialpad?:
        if common.is_element_present(device, calls_dict, "use_hard_keys_to_dial_a_number"):
            # Use hard keys:
            common.wait_for_element(device, calls_dict, "backspace")
            common.wait_for_element(device, calls_dict, "call_icon1")
            common.wait_for_element(device, calls_dict, "dial_pad_field")
            common.dial_hardkeys(device, expected)
        else:
            # Use soft dialpad:
            driver = obj.device_store.get(alias=device)
            if common.is_norden(device):
                common.wait_for_and_click(device, tr_calls_dict, "dial_pad")
                print("Clicked on Dial Pad present on home screen")
            else:
                # Check for landscpae mode desk phones
                if not common.is_element_present(device, calls_dict, "dial_pad"):
                    # Check for portrait mode desk phones
                    time.sleep(action_time)
                    if not common.click_if_present(device, calls_dict, "Make_a_call"):
                        # Check for portrait mode conf phones
                        if common.is_portrait_mode_cnf_device(device):
                            common.wait_for_and_click(device, calendar_dict, "app_bar_dialpad_icon")
                        else:
                            # Check for landscpae mode conf phones
                            if not common.click_if_present(device, calls_dict, "call_dialpad"):
                                raise AssertionError(f"Dial pad is absent for the user on {device}")
            # Wait for phone number editing field and call button
            if common.is_norden(device):
                time.sleep(display_time)
                driver.execute_script("mobile: performEditorAction", {"action": "done"})
            common.wait_for_element(device, calls_dict, "dial_pad_field")
            if not common.is_element_present(device, calls_dict, "call_icon1"):
                common.wait_for_element(device, tr_console_home_screen_dict, "call_icon")
            common.sleep_with_msg(device, action_time, "Allow Dial Pad to be Interactive")
            elem = common.wait_for_element(device, calls_dict, "zero")
            actions = TouchAction(driver)
            actions.long_press(elem, duration=1000).release().perform()
            common.wait_for_and_click(device, calls_dict, "nine")
            common.wait_for_and_click(device, calls_dict, "eight")
            common.wait_for_and_click(device, calls_dict, "seven")
            common.wait_for_and_click(device, calls_dict, "six")
            common.wait_for_and_click(device, calls_dict, "five")
            common.wait_for_and_click(device, calls_dict, "four")
            common.wait_for_and_click(device, calls_dict, "three")
            common.wait_for_and_click(device, calls_dict, "two")
            common.wait_for_and_click(device, calls_dict, "one")
            common.wait_for_and_click(device, calls_dict, "zero")

        # And verify the dialed digits are displayed:
        if common.is_norden(device):
            common.wait_for_and_click(device, calls_dict, "call_icon1")
            called_number = common.wait_for_element(device, tr_console_home_screen_dict, "caller_num").text
            called_number = called_number.replace("1 ", "").replace("-", "")
        else:
            called_number = common.wait_for_element(device, calls_dict, "entered_phn_num").text
        print(f"{device}: Dialed number: '{expected}', displayed number: '{called_number}'")
        if not expected == called_number:
            raise AssertionError(f"Typed phone number mismatch: Expected: '{expected}', actual: '{called_number}'")
        if common.is_norden(device):
            common.wait_for_and_click(device, calls_dict, "Hang_up_button")
            common.wait_while_present(device, calls_dict, "Hang_up_button")


def get_call_participant_name(device):
    print("device :", device)
    navigate_to_calls_tab(device)
    driver = obj.device_store.get(alias=device)
    call_participant_name = (
        WebDriverWait(driver, 30)
        .until(EC.element_to_be_clickable((MobileBy.ID, calls_dict["call_participant_name"]["id"])))
        .text
    )
    print(call_participant_name)
    return str(call_participant_name)


def get_call_duration(device):
    call_duration = common.wait_for_element(device, calls_dict, "call_log_duration").text
    print(f"{device}: Call duration: {call_duration}")
    return str(call_duration)


def click_call_park(device):
    print("device :", device)
    time.sleep(display_time)
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    common.wait_for_and_click(device, calls_dict, "call_more_options")
    common.wait_for_and_click(device, calls_dict, "call_park_option")
    for _attempt in range(30):
        if (
            # Call park text displayed on full screen
            common.is_element_present(device, calls_dict, "Call_parked_text")
            # Parked call orbit number is included in multiple call banner along with other call banners
            or common.is_element_present(device, calls_dict, "expand_multiple_call")
            # Only one parked call number displayed in the banner
            or common.is_element_present(device, calls_dict, "call_unpark_code_from_banner")
        ):
            break
        time.sleep(1)
        if _attempt == 14:
            raise AssertionError(f"{device}: Couldn't park the call")


def get_call_park_code(device):
    # Get the orbit number displayed in full screen
    if common.is_lcp(device):
        call_park_code = common.wait_for_element(device, calls_dict, "call_unpark_code").text
        print(f"{device}: Call park code={call_park_code}")
        common.click_if_present(device, calls_dict, "Call_Back_Button")
        return call_park_code

    time.sleep(display_time)
    if common.is_element_present(device, calls_dict, "call_unpark_code"):
        call_park_code = common.wait_for_element(device, calls_dict, "call_unpark_code").text.split(":")[1].strip()
    # Or, get the orbit number displayed in banner (only one code is displayed)
    elif e := common.is_element_present(device, calls_dict, "call_unpark_code_from_banner"):
        call_park_code = e.text.split(":")[1].strip()
    # Or, the orbit number is displayed in the multi-call banner (multiple orbit numbers might be there)
    else:
        # Note: Something odd here - device is going crazy with tracking multiple parked
        #   calls - the list will still be updating if we open it too soon - Bug?.
        common.sleep_with_msg(device, 5, "let multiple parked calls be handled before we open the list")

        common.wait_for_and_click(device, calls_dict, "expand_multiple_call")

        call_park_code_list = common.get_all_elements_texts(device, calls_dict, "call_unpark_code_from_banner")
        # The recent orbit number is always the last number in the list
        call_park_code = call_park_code_list[-1].split(":")[1].strip()
        # to dismiss multiple  call park banner
        common.tap_outside_the_popup(
            device, common.wait_for_element(device, calls_dict, "multiple_call_pop_up_container")
        )

    print(f"{device}: Call park code={call_park_code}")
    common.click_if_present(device, calls_dict, "Call_Back_Button")
    return call_park_code


def unpark_call(park_code, device):
    if not common.is_element_present(device, calls_dict, "unpark_call"):
        for i in range(3):
            common.click_if_present(device, calls_dict, "Call_Back_Button")
        time.sleep(display_time)
        if not common.is_element_present(device, calls_dict, "unpark_call"):
            navigate_to_calls_tab(device)
        if common.is_lcp(device):
            common.wait_for_and_click(device, lcp_calls_dict, "call_unpark_more_option")
    common.wait_for_and_click(device, calls_dict, "unpark_call")
    unpark_code_input = common.wait_for_element(device, calls_dict, "unpark_code_edit_text")
    print("park_code : ", park_code)
    unpark_code_input.send_keys(park_code)
    if not common.is_lcp(device):
        common.wait_for_element(device, calls_dict, "call_park_cancel")
        common.wait_for_and_click(device, calls_dict, "unpark_call_ok_button")
    _max_attempt = 5
    for _attempt in range(_max_attempt):
        if common.is_element_present(device, calls_dict, "Hang_up_button"):
            return


def cancel_parked_call(device):
    common.click_if_element_appears(device, calls_dict, "call_park_cancel", max_attempts=5)


def click_close_btn(device_list):
    devices = device_list.split(",")
    for device in devices:
        print("device :", device)
        time.sleep(action_time)
        for attempt in range(3):
            if common.click_if_present(device, calls_dict, "close_btn"):
                print("Clicked on close button")
                break
            elif common.click_if_present(device, calls_dict, "Call_Back_Button"):
                print("Clicked on back button")
                break
            elif common.click_if_present(device, tr_calendar_dict, "Dismiss"):
                print("Clicked on Dismiss button")
                break
            elif common.click_if_present(device, calendar_dict, "back"):
                print("Clicked on back button")
                break
            elif common.click_if_present(device, tr_console_settings_dict, "back_layout"):
                print("Clicked on new UI back button")
                break


def check_sec_in_call_duration(call_duration):
    if "sec" in call_duration:
        status = "True"
    else:
        status = "False"
    return status


def verify_participant_list(from_device, connected_device_list):
    print(f"Expected connected devices list: {connected_device_list}")
    expected_connected_devices = connected_device_list.split(",")
    expected_user_list = []
    for devices in expected_connected_devices:
        if ":" in devices:
            user = devices.split(":")[1]
            if user.lower() == "pstn_user":
                expected_user_list.append(str(common.device_pstndisplay(devices)))
                continue
        expected_user_list.append(str(common.device_displayname(devices)))
    print("Expected user list : ", expected_user_list)
    common.wait_for_element(from_device, calls_dict, "Hang_up_button")
    calendar_keywords.navigate_to_add_participant_page(from_device)
    actual_user_list = get_participant_list(from_device)
    print(f"Actual connected user list: {actual_user_list}")
    if actual_user_list.sort() != expected_user_list.sort():
        raise AssertionError(
            f"{from_device}: Actual participants list: {actual_user_list} doesn't match the expected list: {expected_user_list}"
        )
    if common.is_norden(from_device):
        common.wait_for_and_click(from_device, tr_calls_dict, "close_roaster_button")
        return
    common.wait_for_and_click(from_device, calls_dict, "Call_Back_Button")
    time.sleep(3)
    if common.is_element_present(from_device, calls_dict, "Invite_new_user"):
        common.wait_for_and_click(from_device, calls_dict, "Call_Back_Button")


def get_participant_list(from_device):
    print("from device: ", from_device)
    added_participant_list = []
    common.click_if_element_appears(from_device, calls_dict, "see_more_option", max_attempts=3)
    common.sleep_with_msg(from_device, 5, "Wait for meeting participants to sync")
    participant_list = common.get_all_elements_texts(from_device, calls_dict, "call_participant_name")
    print(participant_list)
    for result in participant_list:
        added_participant_list.append(result)
    print(f"Actual connected participants list: {added_participant_list}")
    return added_participant_list


def verify_call_state_and_disconnect(device):
    # TODO: This is a cleanup method, NO verification is done and call may remain connected.
    print("NOT Verifying call state")
    devices = device.split(",")
    # Allow any active calls to establish
    time.sleep(3)
    for device in devices:
        if common.click_if_present(device, calls_dict, "Hang_up_button"):
            common.sleep_with_msg(device, 3, "allow any call rating time to appear")
            common.click_if_present(device, tr_calls_dict, "call_rating_dismiss")
            common.click_if_present(device, calls_dict, "Close_Call_Rating")
            continue
        if common.is_element_present(device, calls_dict, "call_bar"):
            disconnect_call(device)
        # Note: Here, the call may still be connected...


def get_call_time(device):
    devices = device.split(",")
    for device in devices:
        print("device :", device)
        time.sleep(display_time)
        driver = obj.device_store.get(alias=device)
        navigate_to_calls_tab(device)
        time.sleep(display_time)
        search_result_id = calls_dict["call_participant_name"]["id"]
        print("Search result id : ", search_result_id)
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, calls_dict["call_participant_name"]["id"]))
        ).click()
        print("Clicked on 1st user name fron call histroy")
        call_time = (
            WebDriverWait(driver, 30)
            .until(EC.element_to_be_clickable((MobileBy.ID, calls_dict["call_log_time"]["id"])))
            .text
        )
        time.sleep(display_time)
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, calls_dict["call_participant_name"]["id"]))
        ).click()
        time.sleep(display_time)
        print(call_time)
    return str(call_time)


def dial_dialpad_number(from_device, conference_id):
    _model = config["devices"][from_device]["model"].lower()

    print(f"{from_device}: (model '{_model}') number to dial: '{conference_id}'")

    # Ensure at least the textbox is present:
    common.wait_for_element(from_device, calls_dict, "dial_pad_field")

    if common.is_element_present(from_device, calls_dict, "use_hard_keys_to_dial_a_number"):
        if common.is_element_present(from_device, calls_dict, "hash"):
            raise AssertionError(f"{from_device}: Found '#' dialpad button, should not be present")

        common.dial_hardkeys(from_device, conference_id)

        return

    # Ensure the whole dialpad (textbox + '#' button) is present:
    if not common.is_element_present(from_device, calls_dict, "hash"):
        raise AssertionError(f"{from_device}: Missing dialpad '#' button")

    for i in conference_id:
        if i == "9":
            common.wait_for_and_click(from_device, calls_dict, "nine")
        elif i == "8":
            common.wait_for_and_click(from_device, calls_dict, "eight")
        elif i == "7":
            common.wait_for_and_click(from_device, calls_dict, "seven")
        elif i == "6":
            common.wait_for_and_click(from_device, calls_dict, "six")
        elif i == "5":
            common.wait_for_and_click(from_device, calls_dict, "five")
        elif i == "4":
            common.wait_for_and_click(from_device, calls_dict, "four")
        elif i == "3":
            common.wait_for_and_click(from_device, calls_dict, "three")
        elif i == "2":
            common.wait_for_and_click(from_device, calls_dict, "two")
        elif i == "1":
            common.wait_for_and_click(from_device, calls_dict, "one")
        elif i == "0":
            common.wait_for_and_click(from_device, calls_dict, "zero")
        elif i == "#":
            common.wait_for_and_click(from_device, calls_dict, "hash")
        else:
            raise AssertionError(f"Illegal digit '{i}' in dialpad number '{conference_id}'")


def join_meeting_by_dial_in_conference(from_device, phone_no, conference_id):
    print(f"{from_device}: join_meeting_by_dial_in_conference '{phone_no}', '{conference_id}'")
    print("phone_no :", phone_no)

    navigate_to_calls_tab(from_device)

    common.wait_for_and_click(from_device, calls_dict, "search")
    common.wait_for_element(from_device, calls_dict, "search_text").send_keys(phone_no)
    common.wait_for_and_click(from_device, calls_dict, "search_result_item_container")
    common.sleep_with_msg(from_device, 10, "Waiting for the call to connect")
    common.wait_for_element(from_device, calls_dict, "Hang_up_button")
    common.wait_for_and_click(from_device, calls_dict, "call_more_options")
    common.wait_for_and_click(from_device, calls_dict, "call_dialpad_under_more")
    dial_dialpad_number(from_device, conference_id)
    Dialed_numbr = common.get_all_elements_texts(from_device, calls_dict, "phone_number")
    listToStr = " ".join(map(str, Dialed_numbr))
    if conference_id == listToStr:
        common.sleep_with_msg(from_device, 30, "Waiting to enter # post name announcement")
        dial_dialpad_number(from_device, "#")
        common.sleep_with_msg(from_device, 5, "Waiting for the call to be connected")
        common.wait_for_and_click(from_device, calls_dict, "Call_Back_Button")
    else:
        raise AssertionError(f" Unmatched dialpad number '{Dialed_numbr}' and conference id number '{conference_id}'")


def dial_emergency_num(device_list):
    devices = device_list.split(",")
    print("Devices : ", devices)
    for device in devices:
        print("device : ", device)
        if common.is_element_present(device, calls_dict, "backspace") or common.click_if_present(
            device, calendar_dict, "app_bar_dialpad_icon"
        ):
            if not common.is_element_present(device, calendar_dict, "search_contact_box"):
                common.wait_for_element(device, calls_dict, "entered_phn_num").clear()
        else:
            if not common.is_norden(device):
                common.wait_for_and_click(device, calls_dict, "Make_a_call")
        common.sleep_with_msg(device, action_time, "Allow Dial Pad to be Interatable")
        subprocess.call(
            "adb -s {} shell input keyevent 16".format(config["devices"][device]["desired_caps"]["udid"].split(":")[0]),
            shell=True,
        )
        subprocess.call(
            "adb -s {} shell input keyevent 10".format(config["devices"][device]["desired_caps"]["udid"].split(":")[0]),
            shell=True,
        )
        subprocess.call(
            "adb -s {} shell input keyevent 10".format(config["devices"][device]["desired_caps"]["udid"].split(":")[0]),
            shell=True,
        )
        common.wait_for_and_click(device, tr_calls_dict, "place_call")


def verify_emergency_call_state(device_list, state):
    if state.lower() != "connected":
        raise AssertionError(f"Unexpected value for state: {state}")
    devices = device_list.split(",")
    print("Devices : ", devices)
    print("State : ", state)
    for device in devices:
        common.wait_for_element(device, calls_dict, "emergency_call_in_progress_label")
        common.wait_for_element(device, calls_dict, "Hang_up_button")


def verify_incoming_call(device, status):
    if status.lower() not in ["appear", "disappear"]:
        raise AssertionError(f"{device}: Unexpected value for status: {status}")
    devices = device.split(",")
    if status.lower() == "appear":
        for device in devices:
            common.wait_for_element(device, calls_dict, "Accept_call_button")
    elif status.lower() == "disappear":
        time.sleep(action_time)
        for device in devices:
            if common.is_element_present(device, calls_dict, "Accept_call_button"):
                raise AssertionError(f"{device} is still getting incoming call")


def verify_any_incoming_call_disappeared(device, max_seconds=5):
    for attempt in range(max_seconds):
        if not common.is_element_present(device, calls_dict, "Accept_call_button"):
            print(f"{device}: incoming call not present on attempt {attempt} of {max_seconds}")
            return
        time.sleep(1)
    raise AssertionError(f"{device}: incoming call still present")


def verify_call_notification(device, status):
    if status.lower() not in ["appear", "disappear"]:
        raise AssertionError(f"{device}: Unexpected value for status: {status}")
    if isinstance(device, str):
        devices = device.split(",")
    elif isinstance(device, list):
        devices = device
    for device in devices:
        print("device : ", device)
        if status.lower() == "appear":
            common.wait_for_element(device, calls_dict, "accept_call_button_banner", wait_attempts=60)
        if status.lower() == "disappear":
            time.sleep(5)
            if common.is_element_present(device, calls_dict, "accept_call_button_banner"):
                raise AssertionError(f"{device} is still showing incoming call notification")
            print(f"{device} ain't showing any incoming call notification")


def pick_incoming_call_from_call_notification(device):
    devices = device.split(",")
    for device in devices:
        print("Picking incoming call on device : ", device)
        common.wait_for_and_click(device, calls_dict, "accept_call_button_banner")


def pick_incoming_call_in_device_settings_page(device):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((MobileBy.ID, calls_dict["Notification_group_call_answer_button"]["id"]))
        ).click()
        print("Picked up the incoming from notification")
    except Exception as e:
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((MobileBy.ID, calls_dict["Accept_call_button"]["id"]))
            ).click()
            print("Picked full screen incoming Call")
        except:
            raise AssertionError("Couldn't answer the incoming call")


def resume_the_hold_call(device):
    time.sleep(action_time)
    devices = device.split(",")
    for device in devices:
        driver = obj.device_store.get(alias=device)
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, calls_dict["Resume_btn"]["id"]))
        ).click()
        time.sleep(display_time)
        print("resume the call")
    pass


def resume_call_from_call_hold_banner(device):
    common.wait_for_and_click(device, calls_dict, "Resume_call_from_hold_banner")


def click_incoming_group_call_notification(device):
    time.sleep(display_time)
    devices = device.split(",")
    for device in devices:
        driver = obj.device_store.get(alias=device)
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, calls_dict["incoming_group_call"]["id"]))
        ).click()
        time.sleep(display_time)
        print("Clicked on incoming_group_call notification")
    pass


def verify_calling_behalf_of_device_text(device, to_device, from_device):
    if from_device.lower() == "myself":
        from_device_displayname = config["devices"][device]["delegate_user"]["displayname"]
    else:
        account = "user"
        if ":" in from_device:
            user = from_device.split(":")[1]
            print("User account : ", user)
            if user.lower() == "cap_search_enabled":
                account = "cap_search_enabled"
            elif user.lower() == "delegate_user":
                account = "delegate_user"
        from_device = from_device.split(":")[0]
        from_device_displayname = config["devices"][from_device][account]["displayname"]
    to_device_displayname = config["devices"][to_device]["user"]["displayname"]
    calling_behalf_text = to_device_displayname + " for " + from_device_displayname
    print("calling_behalf_text : ", calling_behalf_text)

    tmp_dict = common.get_dict_copy(calls_dict, "calling_text", "user_name", to_device_displayname)
    calling_text = common.wait_for_element(device, tmp_dict, "calling_text").text
    print("calling_text : ", calling_text)
    # calling_text = calling_text + "for" + from_device_displayname
    if from_device.lower() == "myself":
        if calling_text == to_device_displayname:
            print("Calling text is matching")
        else:
            raise AssertionError("Calling for myself text is not matching")
    elif calling_behalf_text == calling_text:
        print("Calling " + calling_text)
    else:
        raise AssertionError("calling on behalf of text is not matching")


def choose_call_behalf_of(device, from_device):
    if from_device.lower() == "myself":
        common.wait_for_and_click(device, calls_dict, "myself_xpath")
    else:
        username = common.device_displayname(from_device)
        temp_dict = common.get_dict_copy(calls_dict, "myself_xpath", "You", username)
        print("Search result xpath : ", temp_dict["myself_xpath"]["xpath"])
        common.wait_for_and_click(device, temp_dict, "myself_xpath", "xpath")
    common.wait_for_element(device, calls_dict, "Hang_up_button")


def verify_on_behalf_of_call_text(device, from_device):
    time.sleep(display_time)
    driver = obj.device_store.get(alias=device)
    account = "user"
    if ":" in from_device:
        user = from_device.split(":")[1]
        print("User account : ", user)
        if user.lower() == "delegate_user":
            account = "delegate_user"
    from_device = from_device.split(":")[0]
    from_device_displayname = config["devices"][from_device][account]["displayname"]
    on_behalf_text = "on behalf of " + from_device_displayname
    print("on_behalf_text : ", on_behalf_text)
    calling_text = (
        WebDriverWait(driver, 30)
        .until(EC.element_to_be_clickable((MobileBy.ID, calls_dict["behalf_calling_text"]["id"])))
        .text
    )
    print("calling_text : ", calling_text)
    if calling_text == on_behalf_text:
        print("Calling ", on_behalf_text)
    else:
        raise AssertionError


def place_call_to_phone_num(from_device, phone_num):
    if phone_num.lower() == "cq_no":
        phn_num = config["cq_no"]
    else:
        phn_num = phone_num
    print("search text :", phn_num)
    common.wait_for_and_click(from_device, calls_dict, "search")
    common.wait_for_element(from_device, calls_dict, "search_text").send_keys(phn_num)
    common.hide_keyboard(from_device)
    searched_number = phn_num.replace(" ", "").replace("-", "")
    search_result = common.wait_for_element(from_device, calls_dict, "search_result_item_container").text
    displayed_num = search_result.replace(" ", "").replace("-", "")
    if searched_number != displayed_num:
        raise AssertionError(
            f"The searched number: {searched_number} doesn't match the expected number: {displayed_num}"
        )
    common.wait_for_and_click(from_device, calls_dict, "search_result_item_container")
    common.wait_for_element(from_device, calls_dict, "Hang_up_button")


def verify_display_name_on_call_toast(to_device, from_device):
    devices = to_device.split(",")
    for device in devices:
        from_device_displayname = common.device_displayname(from_device)
        tmp_dict = common.get_dict_copy(calls_dict, "calling_text", "user_name", from_device_displayname)
        common.wait_for_element(device, tmp_dict, "calling_text")


def select_first_call_participant_from_log(device):
    common.wait_for_and_click(device, calls_dict, "call_participant_name")


def get_missed_calls_count(device):
    count = common.wait_for_element(device, calls_dict, "missed_calls_count").text
    print(f"{device}: Missed calls count: {count}")
    if count.isdigit():
        return int(count)
    return 0


def verify_phone_number_on_call_toast(to_device, from_device):
    time.sleep(display_time)
    devices = to_device.split(",")
    for device in devices:
        print("Picking incoming call on device : ", device)
        print("device :", device)
        driver = obj.device_store.get(alias=to_device)
        from_device_pstndisplay = config["devices"][from_device]["user"]["pstndisplay"]
        print("from_device_pstndisplay : ", from_device_pstndisplay)
        calling_text = (
            WebDriverWait(driver, 30)
            .until(EC.element_to_be_clickable((MobileBy.ID, calls_dict["calling_text"]["id"])))
            .text
        )
        print("calling_text : ", calling_text)
        if calling_text == from_device_pstndisplay:
            print("Calling ", from_device_pstndisplay)
        else:
            raise AssertionError("Phone number is not matching on Call toast")


def get_display_name_on_call_toast(device):
    time.sleep(display_time)
    devices = device.split(",")
    for device in devices:
        print("device :", device)
        driver = obj.device_store.get(alias=device)
        calling_text = (
            WebDriverWait(driver, 30)
            .until(EC.element_to_be_clickable((MobileBy.ID, calls_dict["calling_text"]["id"])))
            .text
        )
        print("calling_text : ", calling_text)

    return calling_text


def verify_forward_by_call_text(device, from_device):
    from_device_displayname = config["devices"][from_device]["user"]["displayname"]
    forward_by_text = "Forwarded by " + from_device_displayname
    calling_text = common.wait_for_element(device, calls_dict, "behalf_calling_text").text
    if calling_text != forward_by_text:
        raise AssertionError(
            f"Forwarded by text displayed: {calling_text} doesn't match the expected text: {forward_by_text}"
        )


def place_video_call(from_device, to_device, method):
    print("from_device :", from_device)
    print("to_device :", to_device)
    print("method : ", method)
    if ":" in to_device:
        user = to_device.split(":")[1]
        print("User account : ", user)
        account = None
        if user.lower() == "pstn_user":
            account = "pstn_user"
        elif user.lower() == "cap_search_enabled":
            account = "cap_search_enabled"
        elif user.lower() == "cap_search_disabled":
            account = "cap_search_disabled"
        elif user.lower() == "delegate_user":
            account = "delegate_user"
        elif user.lower() == "gcp_user":
            account = "gcp_user"
        elif user.lower() == "meeting_user":
            account = "meeting_user"
    else:
        account = "user"
    print("Account :", account)
    to_device = to_device.split(":")[0]
    print("to_device : ", to_device)
    displayname = config["devices"][to_device][account]["displayname"]
    username = config["devices"][to_device][account]["username"].split("@")[0]
    phonenumber = config["devices"][to_device][account]["phonenumber"]
    extnumber = config["devices"][to_device][account]["extension"]
    print("Display, userid, phone and ext number : ", displayname, username, phonenumber, extnumber)

    driver = obj.device_store.get(alias=from_device)
    if method.lower() == "display_name":
        if common.is_norden(from_device):
            print("search text :", username)
            common.wait_for_and_click(from_device, tr_home_screen_dict, "meeting_button")
            common.wait_for_and_click(from_device, tr_calls_dict, "Add_participants_btn")
            element = common.wait_for_element(from_device, calls_dict, "search_contact_box", "id")
            element.send_keys(username)
            common.wait_for_and_click(from_device, calls_dict, "search_result_item_container", "id")
        else:
            print("search text :", username)
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.ID, calls_dict["search"]["id"]))
            ).click()
            element = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.ID, calls_dict["search_text"]["id"]))
            )
            element.send_keys(username)
            time.sleep(display_time)
            try:
                driver.hide_keyboard()
            except Exception as e:
                print("Cannot hide keyboard : ", e)
            search_result_xpath = (calls_dict["search_result_item_container"]["xpath"]).replace(
                "config_display", displayname
            )
            print("Search result xpath : ", search_result_xpath)
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((MobileBy.XPATH, search_result_xpath))).click()
            time.sleep(display_time)
            try:
                WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, calls_dict["Make_an_video_call"]["xpath"]))
                ).click()
                time.sleep(display_time)
            except Exception as e:
                raise AssertionError("This device doesn't support Video Call")
    elif method.lower() == "phone_number":
        print("search text :", phonenumber)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((MobileBy.ID, calls_dict["search"]["id"]))).click()
        element = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, calls_dict["search_text"]["id"]))
        )
        element.send_keys(phonenumber)
        time.sleep(display_time)
        try:
            driver.hide_keyboard()
        except Exception as e:
            print("Cannot hide keyboard : ", e)
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, calls_dict["search_result_item_container"]["id"]))
        ).click()
        time.sleep(display_time)
        try:
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calls_dict["Make_an_video_call"]["xpath1"]))
            ).click()
            time.sleep(display_time)
        except Exception as e:
            raise AssertionError("This device doesn't support Video Call")


def verify_video_status(device, status):
    time.sleep(5)
    devices = device.split(",")
    if not status.lower() in ["on", "off"]:
        raise AssertionError("Invalid status")
    if common.is_element_present(device, calls_dict, "Make_an_video_call"):
        for device in devices:
            print("device :", device)
            if status.lower() == "on":
                common.wait_for_element(device, calls_dict, "video_on")
                time.sleep(display_time)
                print("Video is ON for ", device, " device")
            elif status.lower() == "off":
                common.wait_for_element(device, calls_dict, "video_off")
                time.sleep(display_time)
                print("Video is OFF for ", device, " device")
    else:
        print("This device doesn't support video call")


def verify_device_video_call_support(device):
    if ":" in device:
        device = device.split(":")[0]
    print("device :", device)
    if config["devices"][device]["model"].lower() in ["san jose", "miami"]:
        status = "pass"
    elif common.is_norden(device):
        status = "pass"
    else:
        status = "fail"
    return status


def navigate_to_calls_favorites_page(device):
    devices = device.split(",")
    for device in devices:
        if ":" in device:
            device = device.split(":")[0]
        print("device :", device)
        status = verify_calls_navigation(device)
        print("Status : ", status)
        if status is True:
            print("Already on Calls Tab")
        else:
            time.sleep(3)
            if not common.click_if_present(device, calls_dict, "calls_tab"):
                common.wait_for_and_click(device, home_screen_dict, "home_bar_icon")
                common.wait_for_and_click(device, calls_dict, "calls_tab")
        time.sleep(display_time)
        if not common.click_if_present(device, calls_dict, "favorites_tab"):
            common.wait_for_and_click(device, calls_dict, "Make_a_call")
            common.click_if_present(device, calls_dict, "favorites_tab")
            print("This user doesn't have FAVORITES Tab")
        time.sleep(display_time)
        if not common.is_element_present(device, calls_dict, "favorites_more_options"):
            if not common.is_element_present(device, calls_dict, "call_more_options", "id"):
                common.wait_for_element(device, calls_dict, "favorites_without_contacts_grid")


def verify_latest_call_details(from_device, to_device, option="close_pop_up"):
    if option.lower() not in ["close_pop_up", "verify_pop_up"]:
        print(f"Illegal item specified: '{option}'")
    navigate_to_calls_tab(from_device)
    settings_keywords.refresh_calls_main_tab(from_device)
    user_name = common.get_all_elements_texts(from_device, calls_dict, "call_participant_name")
    call_duration = common.wait_for_element(from_device, calls_dict, "call_duration").text
    print("Call Duration in call Details : ", call_duration)
    to_device_displayname = common.device_displayname(to_device)
    to_device_phonenumber = common.device_pstndisplay(to_device)
    if user_name[0] == to_device_displayname:
        print("Display name visible in call Details : ", to_device_displayname)
    elif user_name[0] == to_device_phonenumber:
        print("Phone number visible in call Details : ", to_device_phonenumber)
    else:
        raise AssertionError("user_text not found in to_device")
    common.wait_for_and_click(from_device, calls_dict, "call_participant_info_button")
    common.wait_for_element(from_device, calls_dict, "call_list_item_call_action")
    common.wait_for_element(from_device, calls_dict, "call_list_view_profile_action")
    if common.is_element_present(from_device, calls_dict, "call_list_item_favorites_action"):
        common.wait_for_element(from_device, calls_dict, "add_user_to_speed_dial")
    else:
        common.wait_for_element(from_device, calls_dict, "remove_user_from_speed_dial")
        print("User is already added to speed dial")
    if option == "close_pop_up":
        dismiss_call_more_options(from_device)
    elif option == "verify_pop_up":
        print("waiting for pop-up dismiss")
    # elem = common.wait_for_element(from_device, calls_dict, "recent_user_entry")
    # contact_name_with_presence = elem.get_attribute("content-desc")
    # current_presence = contact_name_with_presence.split(":")[1].strip()
    # if current_presence.lower() not in ["available", "busy", "dnd", "be right back", "offline", "away"]:
    #     raise AssertionError(f"Unexpected value for state: {current_presence}")
    # common.wait_for_and_click(from_device, calls_dict, "call_participant_name")


def verify_no_calls_object_display_for_new_user(device):
    driver = obj.device_store.get(alias=device)
    time.sleep(action_time)
    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((MobileBy.ID, calls_dict["new_user_error_title"]["id"]))
        )
        print("This is a new user So able to see 'no_calls_page' page")
    except Exception as e:
        print("This is not a new user, So unable to see 'no_calls_page' page", e)
        raise AssertionError("This is not a new user, So unable to see 'no_calls_page' page")


def verify_call_control_visibility(device_list, e2ee="disabled"):
    devices = device_list.split(",")
    print("Devices : ", devices)
    for device in devices:
        print("device : ", device)
        common.wait_for_element(device, calls_dict, "Hang_up_button")
        if common.is_lcp(device):
            common.wait_for_element(device, calls_dict, "showRoster")
            common.wait_for_element(device, calls_dict, "Transfer")
            common.wait_for_and_click(device, calls_dict, "call_more_options")
            common.wait_for_element(device, calls_dict, "Put_call_on_hold")
            common.wait_for_element(device, calls_dict, "call_dial_pad")
            settings_keywords.device_setting_back(device)
            return
        if not common.is_element_present(device, calls_dict, "call_control_speaker"):
            common.wait_for_element(device, calls_dict, "Put_call_on_hold")
            common.wait_for_element(device, calls_dict, "Transfer")
        common.wait_for_element(device, calls_dict, "call_mute_control")

        open_call_more_options(device)

        common.wait_for_element(device, calls_dict, "turn_on_live_captions")
        # Note: Call Park is only present if the tenant has the option enabled for the user:
        if not e2ee == "enabled":
            common.wait_for_element(device, calls_dict, "call_park_option")
        common.wait_for_element(device, calls_dict, "call_dialpad_under_more")
        # verify video devices
        if not common.is_element_present(device, calls_dict, "Put_call_on_hold"):
            # for audio devices
            common.wait_for_element(device, calls_dict, "switch_audio_route")
        dismiss_call_more_options(device)


def is_call_more_options_open(device_name):
    return common.is_element_present(device_name, calls_dict, "call_more_options_container")


def dismiss_call_more_options(device_name, container_element=None):
    driver = obj.device_store.get(alias=device_name)
    # Verify the options are open:
    if container_element is None:
        container_element = common.wait_for_element(device_name, calls_dict, "call_more_options_container")

    # Get co-ordinates to tap outside the menu tray
    x_tap_loc, y_tap_loc = get_co_ords_to_tap(container_element)

    driver.tap([(x_tap_loc, y_tap_loc)])
    print(f"{device_name}: Tapped the co-ordinates: ({x_tap_loc}, {y_tap_loc})")

    # Verify the options are dismissed:
    common.wait_while_present(device_name, calls_dict, "call_more_options_container")


def open_call_more_options(device_name):
    # Open the options:
    common.wait_for_and_click(device_name, calls_dict, "call_more_options")

    # Verify the options are opened:
    common.wait_for_element(device_name, calls_dict, "call_more_options_container")


def get_co_ords_to_tap(container_element):
    # Getting the location of the container_element x and y
    c_location_x = container_element.location["x"]
    c_location_y = container_element.location["y"]
    print(f"Container coordinates location: ({c_location_x}, {c_location_y})")

    # Getting the size of the container_element width and height
    c_size_width = container_element.size["width"]
    print(f"Width of the container: {c_size_width}")

    # Getting the location to tap outside (above) the container
    x_tap_loc = c_location_x + (c_size_width / 2)
    y_tap_loc = c_location_y - 10

    return x_tap_loc, y_tap_loc


def device_right_corner_click(device):
    devices = device.split(",")
    for device in devices:
        _model = config["devices"][device]["model"]

        # Temporary workaround - exclude IpPhone nightly run devices.
        # Note: The following list includes "riverside" (the tap is harmless/ignored but still inappropriate).
        if _model.lower() in [
            "santa cruz",
            "bakersfield",
            "riverside",
            "riverside_13",
            "santa cruz_13",
            "bakersfield_13",
        ]:
            print(f"{device}: IpPhone '{_model}' device_right_corner_click skipped.")
            continue
        # Temporary workaround - exclude MTRA nightly run devices.
        # Note: The tap is harmless/ignored but still inappropriate.
        if _model.lower() in ["spokane", "sammamish", "oakland"]:
            print(f"{device}: MTRA '{_model}' device_right_corner_click skipped.")
            continue

        driver = obj.device_store.get(alias=device)
        window_size = driver.get_window_size()
        print("Window size: ", window_size)
        # height = window_size["height"]
        width = window_size["width"]
        subprocess.call(
            "adb -s {} shell input tap {} {}".format(
                config["devices"][device]["desired_caps"]["udid"].split(":")[0], width - 20, 20
            ),
            shell=True,
        )
        time.sleep(display_time)
        print("Tapped co-ordinates : ", width - 20, 20)


def verify_call_history_log(device):
    common.wait_for_and_click(device, calls_dict, "recent_tab")
    settings_keywords.refresh_calls_main_tab(device)
    common.wait_for_element(device, calls_dict, "call_duration")
    common.get_all_elements_texts(device, calls_dict, "call_participant_name")


def verify_group_call_in_call_history(device, call_participants):
    call_views_keywords.go_back_to_previous_page(device)
    common.wait_for_and_click(device, calls_dict, "recent_tab")
    settings_keywords.refresh_calls_main_tab(device)
    call_participant = call_participants.split(",")
    display_names = []
    for participants in call_participant:
        display_name = common.device_displayname(participants)
        display_names.append(display_name)
    search_text = " and ".join(display_names)
    call_log_name = common.get_all_elements_texts(device, calls_dict, "call_participant_name")
    if search_text not in call_log_name:
        raise AssertionError(
            f"{device}: Call logs doesn't show the expected logs- Expected: '{search_text}', Displayed: '{call_log_name}'"
        )


def call_first_participant_from_log(device):
    time.sleep(display_time)
    common.wait_for_and_click(device, calls_dict, "call_participant_info_button")
    common.wait_for_and_click(device, calls_dict, "call_list_item_call_action")
    if common.click_if_present(device, calls_dict, "myself_xpath"):
        print(f"*WARN*:: {device}: Found and used unexpected 'myself' OBO")
    common.wait_for_element(device, calls_dict, "Hang_up_button")


def select_call_list_item(device, item):
    if item.lower() not in ["call", "view profile", "favorite", "leave_voicemail"]:
        print(f"Illegal item specified: '{item}'")
    navigate_to_calls_tab(device)
    time.sleep(display_time)
    settings_keywords.refresh_calls_main_tab(device)
    if common.is_lcp(device):
        if not common.click_if_present(device, calls_dict, "call_list_item_favorites_action"):
            common.wait_for_and_click(device, calls_dict, "call_log_option")
    else:
        common.wait_for_and_click(device, calls_dict, "call_participant_info_button")
    if item.lower() == "call":
        common.wait_for_and_click(device, calls_dict, "call_list_item_call_action")
    elif item.lower() == "view profile":
        common.wait_for_and_click(device, calls_dict, "call_list_view_profile_action")
    elif item.lower() == "favorite":
        if common.is_element_present(device, calls_dict, "call_list_item_favorites_action"):
            common.wait_for_and_click(device, calls_dict, "add_user_to_speed_dial")
        else:
            common.wait_for_element(device, calls_dict, "remove_user_from_speed_dial")
            print("User is already added to speed dial")
            if common.is_lcp(device):
                settings_keywords.device_setting_back(device)
            else:
                dismiss_call_more_options(device)
    elif item.lower() == "leave_voicemail":
        common.wait_for_and_click(device, calls_dict, "call_list_leave_voicemail")
        common.wait_for_element(device, calls_dict, "Hang_up_button")


def verify_contact_card_page(device):
    display_name = common.wait_for_element(device, calls_dict, "contact_card_display_name").text
    print(f"{device}: Name displayed: {display_name}")
    common.wait_for_element(device, calls_dict, "Make_an_audio_call")


def verify_contact_card_page_and_call(device):
    verify_contact_card_page(device)
    common.wait_for_and_click(device, calls_dict, "Make_an_audio_call")
    common.wait_while_present(device, calls_dict, "Make_an_audio_call")


def verify_favorites_user_option(from_device, to_device):
    navigate_to_calls_favorites_page(from_device)
    if config["devices"][from_device]["model"].lower() == "gilbert":
        calendar_keywords.scroll_down_secondary_tab(from_device)
    added_user_displayname = config["devices"][to_device]["user"]["displayname"]
    temp_dict = common.get_dict_copy(calls_dict, "favorites_more_options", "user_name", added_user_displayname)
    common.wait_for_and_click(from_device, temp_dict, "favorites_more_options", "xpath")
    common.wait_for_element(from_device, calls_dict, "call_option")
    common.wait_for_element(from_device, calls_dict, "view_profile_option")
    common.wait_for_element(from_device, calls_dict, "remove_favorites_option")

    dismiss_calls_item_options(from_device)


def is_calls_item_options_open(device_name):
    return common.is_element_present(device_name, calls_dict, "calls_item_options_container")


def dismiss_calls_item_options(device_name):
    # Make sure the container is open:
    common.wait_for_element(device_name, calls_dict, "calls_item_options_container")
    # Dismiss it:
    common.wait_for_and_click(device_name, calls_dict, "dismiss_calls_item_options_container")
    # Make sure the container is gone:
    if common.is_element_present(device_name, calls_dict, "calls_item_options_container"):
        raise AssertionError(f"{device_name}: calls_item_options_container still present after dismiss")


def select_favorites_user_option(device, option):
    if not option.lower() in ["call", "view profile", "remove favorite"]:
        raise AssertionError(f"Illegal option specified: '{option}'")
    if option.lower() == "call":
        common.wait_for_and_click(device, calls_dict, "call_option")
    elif option.lower() == "view profile":
        common.wait_for_and_click(device, calls_dict, "view_profile_option")
    elif option.lower() == "remove favorite":
        common.wait_for_and_click(device, calls_dict, "remove_favorites_option")


def verify_added_favorite_user_in_favorites_page(from_device, to_device):
    navigate_to_calls_favorites_page(from_device)
    added_user_displayname = common.device_displayname(to_device)
    if config["devices"][from_device]["model"].lower() == "gilbert":
        if common.is_element_present(from_device, calls_dict, "people_you_support") or common.is_element_present(
            from_device, calls_dict, "your_delegates"
        ):
            calendar_keywords.swipe_till_cancel_event(from_device)
    temp_dict = common.get_dict_copy(calls_dict, "favorites_more_options", "user_name", added_user_displayname)
    common.wait_for_element(from_device, temp_dict, "favorites_more_options", "xpath")
    common.wait_for_element(from_device, calls_dict, "speed_dial_header")


def remove_favorite_user_from_favorites_page(from_device, to_device):
    navigate_to_calls_favorites_page(from_device)
    added_user_displayname = common.device_displayname(to_device)
    if ":" in to_device:
        user = to_device.split(":")[1]
        if user.lower() == "pstn_user":
            added_user_displayname = common.device_pstndisplay(to_device)
    temp_dict = common.get_dict_copy(calls_dict, "favorites_more_options", "user_name", added_user_displayname)
    common.wait_for_and_click(from_device, temp_dict, "favorites_more_options", "xpath")
    select_favorites_user_option(from_device, "remove favorite")


def calling_from_favorite_page(from_device, to_device):
    navigate_to_calls_favorites_page(from_device)
    added_user_displayname = common.device_displayname(to_device)
    if ":" in to_device:
        user = to_device.split(":")[1]
        if user.lower() == "pstn_user":
            added_user_displayname = common.device_pstndisplay(to_device)
    temp_dict = common.get_dict_copy(calls_dict, "favorites_more_options", "user_name", added_user_displayname)
    common.wait_for_and_click(from_device, temp_dict, "favorites_more_options", "xpath")
    select_favorites_user_option(from_device, "call")
    common.wait_for_element(from_device, calls_dict, "Hang_up_button")


def verify_favorite_icon_should_not_display_for_group_call(device):
    navigate_to_calls_tab(device)
    settings_keywords.refresh_calls_main_tab(device)
    if common.is_lcp(device):
        common.wait_for_and_click(device, calls_dict, "call_list_item_favorites_action")
    else:
        common.wait_for_and_click(device, calls_dict, "call_participant_info_button")
    time.sleep(display_time)
    if common.is_element_present(device, calls_dict, "call_list_item_favorites_action"):
        raise AssertionError("Favorite icon visible for group call")
    common.wait_for_element(device, calls_dict, "call_list_item_call_action")
    common.wait_for_element(device, calls_dict, "call_list_view_profile_action")
    # device_right_corner_click(device)
    dismiss_calls_item_options(device)


def verify_group_call_participant_details_in_contact_card_page(device, device_list):
    expected_device_list = device_list.split(",")
    expected_user_list = []
    for _device in expected_device_list:
        expected_user_list.append(common.device_displayname(_device))
    group_display_name = common.wait_for_element(device, calls_dict, "group_display_name").text
    print(f"{device}: Expected participants: {expected_user_list}, Actual participants: {group_display_name}")
    for user_name in expected_user_list:
        if user_name not in str(group_display_name):
            raise AssertionError(
                f"{device}: Expected participants: {expected_user_list} & Actual participants: {group_display_name} doesn't match"
            )
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")


def resume_the_hold_call_from_call_bar(device):
    time.sleep(action_time)
    devices = device.split(",")
    for device in devices:
        driver = obj.device_store.get(alias=device)
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, calls_dict["Call_bar_resume_btn"]["id"]))
        ).click()
        time.sleep(display_time)
        print("resume the call from top bar")


def come_back_home_screen_for_user(count):
    if int(count) == 1:
        come_back_to_home_screen(device_list="device_1")
    elif int(count) == 2:
        come_back_to_home_screen(device_list="device_1,device_2")
    elif int(count) == 3:
        come_back_to_home_screen(device_list="device_1,device_2,device_3")
    elif int(count) == 4:
        come_back_to_home_screen(device_list="device_1,device_2,device_3,device_4")
    elif int(count) == 5:
        come_back_to_home_screen(device_list="device_1,device_2,device_3,device_4,device_5")


def verify_lobby_notification(devices):
    devices = devices.split(",")
    for device in devices:
        common.wait_for_element(device, calls_dict, "view_lobby")


def view_lobby_and_select_option(from_device, option):
    common.wait_for_and_click(from_device, calls_dict, "view_lobby")
    common.wait_for_and_click(from_device, calls_dict, "attendee")
    if option.lower() == "admit":
        common.wait_for_and_click(from_device, calls_dict, "admit_lobby")
    elif option.lower() == "decline":
        common.wait_for_and_click(from_device, calls_dict, "decline_lobby")
    elif option.lower() == "view profile":
        common.wait_for_and_click(from_device, calls_dict, "view_profile_lobby")
    common.wait_for_and_click(from_device, calendar_dict, "back")


def get_participant_count(from_device, connected_device_list):
    connected_devices = connected_device_list.split(",")
    print("connected_devices length : ", len(connected_devices))
    device_list = []
    for devices in connected_devices:
        if ":" in devices:
            user = devices.split(":")[1]
            print("User account : ", user)
            if user.lower() == "meeting_user":
                account = "meeting_user"
            elif user.lower() == "pstn_user":
                account = "pstn_user"
            device = devices.split(":")[0]
        else:
            account = "user"
            device = devices
        print("account : ", account)
        print("device : ", device)
        if ":" in devices:
            user = devices.split(":")[1]
            if user.lower() == "pstn_user":
                device_list.append(str(config["devices"][device][account]["pstndisplay"]))
            elif user.lower() == "meeting_user":
                device_list.append(str(config["devices"][device][account]["pstndisplay"]))
        else:
            device_list.append(str(config["devices"][device][account]["displayname"]))
    print("device_list : ", device_list)
    calendar_keywords.navigate_to_add_participant_page(from_device)
    get_connected_devices_list = get_participant_list(from_device)
    print("get_connected_devices_list length : ", len(get_connected_devices_list))
    print("get_connected_devices_list : ", get_connected_devices_list)
    if len(device_list) == len(get_connected_devices_list):
        print("Connected device length and given device length is matching")
        count = len(get_connected_devices_list)
    else:
        raise AssertionError("Connected device length and given device length is not matching")
    common.wait_for_and_click(from_device, calls_dict, "Call_Back_Button")
    return count


def validate_could_not_complete_the_call(device):
    common.wait_for_element(device, calls_dict, "end_call_callee_text")


def cancel_call_park(park_code, device):
    time.sleep(display_time)
    for i in range(3):
        common.click_if_present(device, calls_dict, "Call_Back_Button")
    time.sleep(display_time)
    if not common.is_element_present(device, calls_dict, "unpark_call"):
        navigate_to_calls_tab(device)
    common.wait_for_and_click(device, calls_dict, "unpark_call")
    unpark_code_input = common.wait_for_element(device, calls_dict, "unpark_code_edit_text")
    print("park_code : ", park_code)
    unpark_code_input.send_keys(park_code)
    common.wait_for_and_click(device, calls_dict, "call_park_cancel")


def reject_incoming_call_from_call_notification(device):
    devices = device.split(",")
    for device in devices:
        common.wait_for_and_click(device, calls_dict, "Notification_ignore_call_button")


def navigate_contact_search_page(device):
    navigate_to_calls_tab(device)
    common.wait_for_and_click(device, calls_dict, "search")
    common.wait_for_element(device, calls_dict, "search_text")


def navigate_to_call_park_page(device):
    print("device :", device)
    click_on_calls_tab(device)
    common.wait_for_and_click(device, calls_dict, "unpark_call")


def cancel_call_park_page(device):
    print("device :", device)
    time.sleep(display_time)
    common.wait_for_and_click(device, calls_dict, "call_park_cancel")


def verify_user_should_not_get_the_option_to_call_on_behalf(device):
    print("device :", device)
    time.sleep(display_time)
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calls_dict["myself_xpath"]["xpath"]))
        )
        raise AssertionError("User getting the option to call on behalf")
    except Exception as e:
        print("User is not getting the option to call on behalf")


def validate_People_you_support_tab(device):
    devices = device.split(",")
    for device in devices:
        print("device :", device)
        common.wait_for_element(device, calls_dict, "people_you_support")


def validate_delegates_tab(device):
    devices = device.split(",")
    for device in devices:
        print("device :", device)
        driver = obj.device_store.get(alias=device)
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calls_dict["your_delegates"]["xpath"]))
            )
            print("Delegates tab is avalable")
        except Exception as e:
            raise AssertionError("Delegates tab is not avalable")
    pass


def validate_delegate_view_permissions_on_favorites_page(device):
    navigate_to_calls_favorites_page(device)
    common.wait_for_and_click(device, calls_dict, "favorites_more_options")
    common.wait_for_and_click(device, calls_dict, "view_Permissions")
    common.wait_for_element(device, calls_dict, "make_calls")
    common.wait_for_element(device, calls_dict, "receive_calls")
    common.wait_for_element(device, calls_dict, "change_call_and_delegate_settings")


def verify_contacts_option_in_call_transfer_section(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    if not common.click_if_present(device, calls_dict, "Transfer"):
        common.wait_for_and_click(device, calls_dict, "call_more_options")
        common.wait_for_and_click(device, calls_dict, "Transfer")
    common.wait_for_and_click(device, calls_dict, "Transfer_now")
    common.wait_for_element(device, calls_dict, "contacts_title")


def verify_initial_list_contacts_in_the_call_transfer_section(from_device, to_device):
    displayname = config["devices"][to_device]["user"]["displayname"]
    print("from_device :", from_device)
    print("to_device :", to_device)
    print("search text :", displayname)
    common.wait_for_element(from_device, calls_dict, "Hang_up_button")
    if not common.click_if_present(from_device, calls_dict, "Transfer"):
        common.wait_for_and_click(from_device, calls_dict, "call_more_options")
        common.wait_for_and_click(from_device, calls_dict, "Transfer")
    common.wait_for_and_click(from_device, calls_dict, "Transfer_now")
    common.wait_for_element(from_device, calls_dict, "contacts_title")
    element = common.wait_for_element(from_device, calls_dict, "search_contact_box")
    element.send_keys(displayname[0:-1])
    common.hide_keyboard(from_device)
    name = common.wait_for_element(from_device, calls_dict, "search_result_name").text
    if name != displayname:
        raise AssertionError(f"{from_device}: Contact searched for: {displayname}, but search result obtained: {name}")


def disconnect_call_and_verify_call_rating_screen(device):
    devices = device.split(",")
    for device in devices:
        common.wait_for_and_click(device, calls_dict, "Hang_up_button")
        common.sleep_with_msg(device, 5, "Waiting to check if call rating screen appears")
        if common.is_element_present(device, calls_dict, "Call_Rating"):
            common.sleep_with_msg(device, 5, "Waiting for auto dismissal of call rating screen")
            if common.is_element_present(device, calls_dict, "Call_Rating"):
                raise AssertionError(f"Call rating screen didn't auto dismiss in 5 seconds")


def verify_call_decline_screen(device):
    time.sleep(2)
    if not common.is_element_present(device, calls_dict, "call_declined_screen"):
        print(f"{device}: Call decline screen is not being displayed")
        return
    common.sleep_with_msg(device, 3, "Waiting for auto dismissal of call decline screen")
    if common.is_element_present(device, calls_dict, "call_declined_screen"):
        raise AssertionError(f"{device}: Call decline screen is still displayed after 5 seconds")


def verify_call_merge_failure(device):
    print("Device : ", device)
    common.wait_for_element(device, calls_dict, "Call_Merging_Failure")
    common.wait_for_and_click(device, calls_dict, "Call_Merging_Failure_Ok_button")


def verify_and_merge_call(device, from_device, status="merge"):
    print("Device : ", device)
    print("from device : ", from_device)
    verify_call_control_visibility(device)
    name_list = []
    user = "user"
    display_name = "displayname"
    if "," in from_device:
        from_device = from_device.split(",")
        for d in from_device:
            if ":" in d:
                user = d.split(":")[1]
                d = d.split(":")[0]
            name_list.append(config["devices"][d][user][display_name].split()[0])
        name_list.sort()
        print(f"merged call participant's first name list : {name_list}")
        search_string = name_list[0] + " and " + name_list[1]
        replace_str = "Merge with " + search_string
    else:
        if ":" in from_device:
            if not common.click_if_present(device, calls_dict, "pstn_merge_button"):
                open_call_more_options(device)
                common.wait_for_and_click(device, calls_dict, "pstn_merge_button")
            return

        else:
            display_name = common.device_displayname(from_device)
            replace_str = "Merge with " + display_name

    print(f"Search string is: {replace_str}")
    temp_dict = common.get_dict_copy(calls_dict, "Merge_button", "merge_display", replace_str)
    if status == "merge":
        if not common.click_if_present(device, temp_dict, "Merge_button", "xpath"):
            open_call_more_options(device)
            common.wait_for_and_click(device, temp_dict, "Merge_button", "xpath")
    elif status == "verify":
        if not common.is_element_present(device, temp_dict, "Merge_button", "xpath"):
            open_call_more_options(device)
            common.wait_for_element(device, temp_dict, "Merge_button", "xpath")
        dismiss_call_more_options(device)


def verify_call_merge_failure_scenario(device, merge_with_device, disconnect_from_device):
    verify_call_control_visibility(device)
    username = common.device_displayname(merge_with_device)
    replace_str = "Merge with " + username
    print(f"Search string is: {replace_str}")
    temp_dict = common.get_dict_copy(calls_dict, "Merge_button", "merge_display", replace_str)
    if not common.is_element_present(device, temp_dict, "Merge_button", "xpath"):
        common.wait_for_and_click(device, calls_dict, "call_more_options")
    common.wait_for_and_click(device, temp_dict, "Merge_button", "xpath")
    common.wait_for_and_click(disconnect_from_device, calls_dict, "Hang_up_button")
    verify_call_merge_failure(device)


def verify_call_merge_option_ability_with_multiple_calls(device, from_device):
    print("Device : ", device)
    print("from device : ", from_device)
    devices = from_device.split(",")
    verify_call_control_visibility(device)
    if not common.click_if_present(device, calls_dict, "Merge_button", "xpath1"):
        common.wait_for_and_click(device, calls_dict, "call_more_options")
        common.wait_for_and_click(device, calls_dict, "Merge_button", "xpath1")
    for d in devices:
        replace_str = "Merge with " + config["devices"][d]["user"]["displayname"]
        temp_dict = common.get_dict_copy(calls_dict, "Merge_button", "merge_display", replace_str)
        common.wait_for_element(device, temp_dict, "Merge_button")
        if devices.index(d) == len(devices) - 1:
            common.wait_for_and_click(device, temp_dict, "Merge_button")
    verify_transition_screen_during_call_merge(device)


def verify_user_did_num_on_home_screen(device):
    account = "user"
    if ":" in device:
        user = device.split(":")[1]
        print("User account : ", user)
        if user.lower() == "cap_search_enabled":
            account = "cap_search_enabled"
        elif user.lower() == "cap_search_disabled":
            account = "cap_search_disabled"
    print("Account :", account)
    device = device.split(":")[0]
    print("to_device : ", device)
    user_phone_num = config["devices"][device][account]["phonenumber"]
    if common.is_element_present(device, home_screen_dict, "hs_phonenum"):
        did_num = common.wait_for_element(device, home_screen_dict, "hs_phonenum").text
    else:
        did_num = common.wait_for_element(device, calls_dict, "user_phone_num").text
    did_num1 = "".join(e for e in did_num if e.isalnum())
    if user_phone_num != did_num1:
        raise AssertionError("DID number is not matching :", user_phone_num, did_num1)


def verify_search_option_in_call_transfer_section(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    common.wait_for_and_click(device, calls_dict, "Transfer")
    common.wait_for_and_click(device, calls_dict, "Transfer_now")
    elem = common.wait_for_element(device, calls_dict, "search_contact_box")
    elem.send_keys("T")
    print("Searching 'T'")
    common.hide_keyboard(device)
    search_results = common.get_all_elements_texts(device, calls_dict, "user_title", "xpath")
    print(f"Search results are: {search_results} ")
    elem.send_keys("Te")
    print("Searching 'Te'")
    common.hide_keyboard(device)
    search_results = common.get_all_elements_texts(device, calls_dict, "user_title", "xpath")
    print(f"Search results are: {search_results} ")


def validate_call_cancelled(device):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    time.sleep(display_time)
    try:
        end_call_callee = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, calls_dict["end_call_callee_text"]["id"]))
        )
        print("end_call_callee", end_call_callee.text)
        print("Call cancelled is visible .")
        try:
            driver.find_element_by_id(calls_dict["Redial_button"]["id"]).is_displayed()
            print("Redial button is present ")
        except Exception as e:
            time.sleep(display_time)
            pass
    except Exception as e:
        print("Call cancelled screen dismisses within 5 seconds ", e)
    pass


def verify_transition_screen_during_call_merge(device):
    if common.is_element_present(device, calls_dict, "Merging_call_text"):
        print(f"Merging call on {device}")
    else:
        print("'Merging Call...' text is not visible")


def verify_header_of_call_roster(device, from_device):
    name_list = []
    from_device = from_device.split(",")
    for devices in from_device:
        name_list.append(common.device_displayname(devices))
    search_name = name_list[0]
    if len(name_list) == 2:
        search_name = name_list[0] + " and " + name_list[1]
    name_displayed = common.wait_for_element(device, calls_dict, "caller_name_in_full_screen_call").text
    if name_displayed != search_name:
        raise AssertionError(
            f"Name didn't get updated after call merge - Name displayed: {name_displayed}, Name expected: {search_name}"
        )


def verify_merge_call_option(from_device, to_device, merge_option="present"):
    if not merge_option.lower() in ["present", "absent"]:
        raise AssertionError(f"Illegal merge_option specified: '{merge_option}'")
    if merge_option.lower() == "absent":
        if common.is_element_present(from_device, calls_dict, "call_more_options"):
            # Checking here call more option because call merge option present inside it
            raise AssertionError(f"{from_device}: 'Call_more_otions' is present")
    else:
        verify_call_control_visibility(from_device)
        merge_with_user_name = "Merge with " + common.device_displayname(to_device)
        temp_dict = common.get_dict_copy(calls_dict, "Merge_button", "merge_display", merge_with_user_name)
        print("search_result_xpath : ", temp_dict)
        if not common.is_element_present(from_device, temp_dict, "Merge_button", "xpath"):
            open_call_more_options(from_device)
            common.wait_for_element(from_device, temp_dict, "Merge_button", "xpath")
            dismiss_call_more_options(from_device)
        else:
            raise AssertionError(f"{from_device}: 'Merge_button' is missing")


def select_call_list_item_from_recent_tab(device, item):
    driver = obj.device_store.get(alias=device)
    try:
        time.sleep(display_time)
        recent_xpath = driver.find_element_by_id(calls_dict["recent_tab"]["id"])
        recent_xpath.click()
        print("Clicked Calls>Recent tab")
    except Exception as e:
        print("This user doesn't have Recent Tab")
        pass
    time.sleep(display_time)
    user_name = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((MobileBy.ID, calls_dict["call_participant_name"]["id"]))
    )
    user_name.click()
    print("Clicked on 1st user name fron call histroy")
    if item.lower() == "call":
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, calls_dict["call_list_item_call_action"]["id"]))
        ).click()
        print("Clicked on CALL icon from call Details")
    elif item.lower() == "view profile":
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, calls_dict["call_list_view_profile_action"]["id"]))
        ).click()
        print("Clicked on VIEW PROFILE icon from call Details")
    elif item.lower() == "favorite":
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, calls_dict["call_list_item_favorites_action"]["id"]))
        ).click()
        print("Clicked on FAVORITES icon from call Details")
    else:
        raise AssertionError("Provide proper option to select from Call list")


def wait_till_incoming_call_visibility(device):
    devices = device.split(",")
    for device in devices:
        common.wait_for_element(device, calls_dict, "Accept_call_button")


def click_on_call_action_bar(device):
    print("device:", device)
    devices = device.split(",")
    for device in devices:
        driver = obj.device_store.get(alias=device)
        time.sleep(display_time)
        try:
            call_action_bar_status = driver.find_element_by_id(calls_dict["call_action_bar"]["id"])
            if call_action_bar_status.is_displayed():
                call_action_bar_status.click()
            print("Active call on Action Bar found on device : ", device)
        except Exception as e:
            print("Active call on Action Bar not found on device")


def verify_delegates_in_favorites_page(device):
    navigate_to_calls_favorites_page(device)
    if common.is_element_present(device, calls_dict, "your_delegates"):
        return True
    return False


def verify_favorite_page_when_there_are_no_delegate_user_added(device):
    if not common.is_element_present(device, calls_dict, "add_your_speed_dial_numbers"):
        if common.is_element_present(device, calls_dict, "your_delegates"):
            raise AssertionError(f"{device}: Delegates tile is still displayed in favorites tab")
        common.wait_for_element(device, calls_dict, "speed_dial_header")


def verify_favorite_page_when_there_are_no_favorite_contacts(device):
    if not common.is_element_present(device, calls_dict, "favorites_without_contacts_grid"):
        if not common.is_element_present(device, calls_dict, "people_you_support"):
            common.wait_for_element(device, calls_dict, "your_delegates")
        common.wait_while_present(device, calls_dict, "speed_dial_header")


def verify_call_behalf_of_bosses_list(from_device, boss_list):
    time.sleep(display_time)
    bosses = boss_list.split(",")
    boss_list_1 = []
    for boss_1 in bosses:
        boss = common.device_displayname(boss_1)
        boss_list_1.append(boss)
    boss_list_1.append("You")
    user_name_list = common.get_all_elements_texts(from_device, calls_dict, "user_name")

    for boss in boss_list_1:
        if boss not in user_name_list:
            raise AssertionError(f"Expected boss names are not displayed:{bosses},{user_name_list}")


def check_the_presence_of_another_user(from_device, to_device):
    print("from_device :", from_device)
    print("to_device :", to_device)
    displayname = common.device_displayname(to_device)
    print("search text :", displayname)
    common.wait_for_and_click(from_device, calls_dict, "search")
    common.wait_for_element(from_device, calls_dict, "search_text").send_keys(displayname)
    time.sleep(display_time)
    common.hide_keyboard(from_device)
    search_result_xpath = common.get_dict_copy(calls_dict, "call_participant_name", "config_display", displayname)
    common.wait_for_and_click(from_device, search_result_xpath, "call_participant_name")
    common.wait_for_element(from_device, calls_dict, "user_presence")


def validate_address_information_on_the_screen(device):
    common.wait_for_element(device, calls_dict, "emergency_call_in_progress_label")
    common.wait_for_element(device, calls_dict, "emergency_call_icon")
    your_num = common.wait_for_element(device, calls_dict, "your_number").text
    if not "Your number:" in your_num:
        raise AssertionError(your_num, " is not Visible")
    print(your_num, " is  Visible")


def verify_dialpad_in_call_control(device):
    devices = device.split(",")
    print(f"Devices: {devices}")
    for device in devices:
        open_call_more_options(device)
        common.wait_for_and_click(device, calls_dict, "call_dialpad_under_more")
        given_numbers = "12345"
        for i in given_numbers:
            common.wait_for_and_click(device, calendar_dict, i)
        text_field = common.wait_for_element(device, calls_dict, "phone_number")
        typed_number = text_field.text
        if given_numbers != typed_number:
            print(f"{device}: Input number: '{given_numbers}' is not matching with typed number: '{typed_number}'")


def start_recording_call(device):
    devices = device.split(",")
    for device in devices:
        common.wait_for_element(device, calls_dict, "Hang_up_button")
        open_call_more_options(device)

        common.wait_for_and_click(device, calls_dict, "start_recording")
        common.wait_for_element(device, calls_dict, "notification_text")


def verify_recording_notification_on_screen(device):
    text = common.wait_for_element(device, calls_dict, "2nd_notification_text").text
    if not (
        text == "You're recording. Make sure everyone knows they're being recorded. Privacy Policy"
        or text == "Recording is about to start..."
    ):
        raise AssertionError(f"{device}: Expected message not found: {text}")


def stop_recording_call(device):
    devices = device.split(",")
    for device in devices:
        common.wait_for_element(device, calls_dict, "Hang_up_button")
        open_call_more_options(device)

        common.wait_for_and_click(device, calls_dict, "stop_recording")
        common.wait_for_and_click(device, calls_dict, "ok")
        common.wait_for_element(device, calls_dict, "stop_recording_notification_text")


def verify_call_forwarded_text(device, from_device):
    time.sleep(display_time)
    driver = obj.device_store.get(alias=device)
    from_device_displayname = config["devices"][from_device]["user"]["displayname"]
    forward_by_text = "call for " + from_device_displayname
    print("Forwarded by : ", forward_by_text)
    calling_text = (
        WebDriverWait(driver, 30)
        .until(EC.element_to_be_clickable((MobileBy.ID, calls_dict["behalf_calling_text"]["id"])))
        .text
    )
    print("calling_text : ", calling_text)
    if calling_text == forward_by_text:
        print("Calling ", forward_by_text)
    else:
        raise AssertionError


def auto_dial_with_valid_num_from_dial_pad(from_device, to_device, method="phonenumber"):
    common.click_if_element_appears(from_device, calls_dict, "dialpad_tab", max_attempts=5)
    if not (
        common.is_element_present(from_device, calendar_dict, "app_bar_dialpad_icon")
        or common.is_element_present(from_device, calls_dict, "dial_pad_field")
    ):
        common.wait_for_and_click(from_device, calls_dict, "Make_a_call")
    common.click_if_present(from_device, calendar_dict, "app_bar_dialpad_icon")
    common.click_if_present(from_device, calls_dict, "dial_pad")
    common.wait_for_and_click(from_device, calls_dict, "dial_pad_field")
    element = common.wait_for_element(from_device, calls_dict, "entered_phn_num")
    element.clear()
    if method.lower() == "phonenumber":
        phonenumber = common.device_phonenumber(to_device)

    elif method.lower() == "extension":
        phonenumber = common.device_extention_number(to_device)

    model_ = common.device_model(from_device)
    if model_ in ["riverside", "riverside_13", "gilbert"]:
        common.wait_for_element(from_device, calls_dict, "use_hard_keys_to_dial_a_number")
        if common.is_element_present(from_device, calls_dict, "hash"):
            raise AssertionError(f"{from_device}: Found '#' dialpad button, should not be present")

        common.dial_hardkeys(from_device, phonenumber)
        common.wait_for_element(from_device, calls_dict, "Hang_up_button")
        return
    else:
        time.sleep(display_time)
        # Ensure the whole dialpad (textbox + '#' button) is present:
        if common.is_element_present(from_device, calls_dict, "use_hard_keys_to_dial_a_number"):
            raise AssertionError(f"{from_device}: soft dailpad is not present")

        for i in phonenumber:
            if i == "9":
                common.wait_for_and_click(from_device, calls_dict, "nine")
            elif i == "8":
                common.wait_for_and_click(from_device, calls_dict, "eight")
            elif i == "7":
                common.wait_for_and_click(from_device, calls_dict, "seven")
            elif i == "6":
                common.wait_for_and_click(from_device, calls_dict, "six")
            elif i == "5":
                common.wait_for_and_click(from_device, calls_dict, "five")
            elif i == "4":
                common.wait_for_and_click(from_device, calls_dict, "four")
            elif i == "3":
                common.wait_for_and_click(from_device, calls_dict, "three")
            elif i == "2":
                common.wait_for_and_click(from_device, calls_dict, "two")
            elif i == "1":
                common.wait_for_and_click(from_device, calls_dict, "one")
            elif i == "0":
                common.wait_for_and_click(from_device, calls_dict, "zero")
            else:
                raise AssertionError(f"Illegal digit '{i}' in dialpad number '{phonenumber}'")

    common.wait_for_element(from_device, calls_dict, "Hang_up_button")


def auto_dial_edited_valid_num_from_dial_pad(from_device, to_device, method="phonenumber"):
    print("from_device :", from_device)
    print("to_device :", to_device)
    if ":" in to_device:
        user = to_device.split(":")[1]
        print("User account : ", user)
        account = None
        if user.lower() == "pstn_user":
            account = "pstn_user"
        elif user.lower() == "cap_search_enabled":
            account = "cap_search_enabled"
        elif user.lower() == "cap_search_disabled":
            account = "cap_search_disabled"
        elif user.lower() == "delegate_user":
            account = "delegate_user"
    else:
        account = "user"
    print("Account :", account)
    to_device = to_device.split(":")[0]
    print("to_device : ", to_device)
    displayname = config["devices"][to_device][account]["displayname"]
    phonenumber = config["devices"][to_device][account]["phonenumber"]
    extnumber = config["devices"][to_device][account]["extension"]
    print("Display phone and ext number : ", displayname, phonenumber, extnumber)
    common.click_if_element_appears(from_device, calls_dict, "dialpad_tab")
    if not (
        common.is_element_present(from_device, calendar_dict, "app_bar_dialpad_icon")
        or common.is_element_present(from_device, calls_dict, "dial_pad_field")
    ):
        common.wait_for_and_click(from_device, calls_dict, "Make_a_call")
    common.click_if_present(from_device, calendar_dict, "app_bar_dialpad_icon")
    common.click_if_present(from_device, calls_dict, "dial_pad")
    common.wait_for_and_click(from_device, calls_dict, "dial_pad_field")
    element = common.wait_for_element(from_device, calls_dict, "entered_phn_num")
    element.clear()
    time.sleep(display_time)
    invalid_num = phonenumber, "abc"
    element.send_keys(invalid_num)
    time.sleep(display_time)
    if method.lower() == "phonenumber":
        element.clear()
        time.sleep(display_time)
        element.send_keys(phonenumber)
        print("entered phone no.")
    elif method.lower() == "extension":
        element.clear()
        time.sleep(display_time)
        element.send_keys(extnumber)
        print("entered extension no.")
    common.wait_for_element(from_device, calendar_dict, "hang_up_btn", wait_attempts=40)


def verify_call_more_option_for_emergency_call(device):
    driver = obj.device_store.get(alias=device)
    settings_keywords.click_device_center_point(device)
    print("Clicked on center point")
    if len(driver.find_elements(By.ID, calls_dict["call_more_options"]["id"])) > 0:
        raise AssertionError("Call More option present for Emergency Call")
    else:
        print("No Call more Option is not there ")


def verify_call_dropdown_from_favorites_tab(device, from_device, to_device, tile, status="verify"):
    print("from_device :", from_device)
    print("to_device :", to_device)
    account = "user"
    if ":" in to_device:
        user = to_device.split(":")[1]
        print("User account : ", user)
        if user.lower() == "meeting_user":
            account = "meeting_user"
        elif user.lower() == "cap_search_enabled":
            account = "cap_search_enabled"
        elif user.lower() == "delegate_user":
            account = "delegate_user"
        print("Account :", account)
        to_device = to_device.split(":")[0]
        print("to_device : ", to_device)
    elif ":" in from_device:
        account = from_device.split(":")[1]
        from_device = from_device.split(":")[0]
    if tile.lower() not in ["delegate", "boss", "user"]:
        raise AssertionError(f"Unexpected value for tile : {tile}")
    if status.lower() not in ["verify", "call"]:
        raise AssertionError(f"Unexpected value for status : {status}")
    if tile.lower() == "delegate":
        from_device_displayname = config["devices"][from_device]["delegate_user"]["displayname"]
        to_device_displayname = config["devices"][to_device][account]["displayname"]
        call_icons_list = common.wait_for_element(
            device, calls_dict, "sla_active_calls_dropdown", cond=EC.presence_of_all_elements_located
        )
        call_icons_list[1].click()
    elif tile.lower() == "boss":
        from_device_displayname = config["devices"][from_device][account]["displayname"]
        to_device_displayname = config["devices"][to_device]["delegate_user"]["displayname"]
        call_icons_list = common.wait_for_element(
            device, calls_dict, "sla_active_calls_dropdown", cond=EC.presence_of_all_elements_located
        )
        call_icons_list[0].click()
    elif tile.lower() == "user":
        from_device_displayname = config["devices"][from_device][account]["displayname"]
        to_device_displayname = config["devices"][to_device][account]["displayname"]
        common.wait_for_and_click(device, calls_dict, "sla_active_call_icon")
        in_call_text = "In a call with " + from_device_displayname
        call_to_text = "Call " + to_device_displayname
    if not tile.lower() == "user":
        in_call_text = "In a call with " + to_device_displayname
        call_to_text = "Call " + from_device_displayname
    print("in_call_text ", in_call_text)
    print("call_to_text ", call_to_text)
    common.sleep_with_msg(device, 5, "Wait for the call dropdown text")
    dropdown_obj = common.get_all_elements_texts(device, calls_dict, "dropdown_text")
    print(dropdown_obj)
    if not (in_call_text in dropdown_obj[:2] and dropdown_obj[-1] == call_to_text):
        raise AssertionError(f"{device} : The text on the call dropdown menu is not as expected")
    dropdown_obj1 = common.wait_for_element(
        device, calls_dict, "dropdown_text", cond=EC.presence_of_all_elements_located
    )
    if status.lower() == "verify":
        dropdown_obj1[0].click()
    elif status.lower() == "call":
        dropdown_obj1[1].click()


def check_call_dropdown_menu_state(device):
    if common.is_element_present(device, calls_dict, "Call_dropdown_menu"):
        # TODO: This looks odd, does this ever fire?
        device_right_corner_click(device)
        if common.is_element_present(device, calls_dict, "Call_dropdown_menu"):
            raise AssertionError(f"{device} : Call dropdown menu is still displayed")
    print(f"Call dropdown menu is not displayed in {device}")


def verify_active_call_pill(device):
    common.wait_for_element(device, calls_dict, "favorites_tab")
    if common.is_element_present(device, calls_dict, "sla_active_call_icon"):
        raise AssertionError(f"{device} : Call dropdown icon is still displayed on boss tile")


def initiate_simultaneous_call(devices, target_device, method):
    thread_list = []
    device_list = devices.split(",")
    for device in device_list:
        account = "user"
        if ":" in device:
            user = device.split(":")[1]
            print("User account : ", user)
            if user.lower() == "pstn_user":
                account = "pstn_user"
        print("Account :", account)
        device = device.split(":")[0]
        print(f"Device : {device}")
        device_thread = threading.Thread(target=place_call, args=(device, target_device, method))
        thread_list.append(device_thread)
    print("Starting call threads")
    for d in thread_list:
        d.start()
    print("Waiting for the threads to complete and join")
    for d in thread_list:
        d.join()
    print("All call threads completed and joined")


def verify_multiple_incoming_calls(device):
    if common.is_element_present(device, calls_dict, "Multiple_call_hold_ribbon"):
        common.wait_for_and_click(device, calls_dict, "Multiple_call_hold_ribbon_dropdown")
    common.wait_for_element(device, calls_dict, "Accept_call_button")
    print(f"{device} : User is getting full screen call")
    common.wait_for_element(device, calls_dict, "Notification_group_call_answer_button")
    print(f"{device} : User is getting notification call")


def accept_multiple_incoming_calls(
    device,
    full_screen_call="accept",
    notification_call="reject",
    count="3",
    transfer_method=None,
    from_device=None,
    to_device=None,
    method=None,
):
    print(
        f"Passed parameters : device: {device} full_screen_call: {full_screen_call} notification_call: {notification_call} count: {count}"
    )
    if full_screen_call == "accept" and notification_call == "verify":
        common.wait_for_element(device, calls_dict, "Accept_call_button")
        caller_name = common.wait_for_element(device, calls_dict, "caller_name_in_full_screen_call").text
        print("Caller name : ", caller_name)
        common.wait_for_and_click(device, calls_dict, "Accept_call_button")
        common.sleep_with_msg(device, 3, "Waiting after accepting full screen call")
        verify_call_connectivity_using_callee_text(caller_name)
        if common.is_element_present(device, calls_dict, "Accept_call_button"):
            raise AssertionError(f"{device} : Full screen call is still visible post accepting the same")
        common.wait_for_element(device, calls_dict, "Notification_group_call_answer_button")
    elif full_screen_call == "verify" and notification_call == "accept":
        common.wait_for_element(device, calls_dict, "Notification_group_call_answer_button")
        caller_name = common.wait_for_element(device, calls_dict, "caller_name_in_notification_call").text
        print("Caller name : ", caller_name)
        common.wait_for_and_click(device, calls_dict, "Notification_group_call_answer_button")
        common.sleep_with_msg(device, 3, "Waiting after accepting notification call")
        verify_call_connectivity_using_callee_text(caller_name)
        if common.is_element_present(device, calls_dict, "Accept_call_button"):
            raise AssertionError(f"{device} : Full screen call is still visible post accepting notification call")
        common.wait_for_element(device, calls_dict, "Notification_group_call_answer_button")
    elif full_screen_call == "accept" and notification_call == "accept":
        common.wait_for_element(device, calls_dict, "Accept_call_button")
        caller_name = common.wait_for_element(device, calls_dict, "caller_name_in_full_screen_call").text
        print("Caller name on full screen call: ", caller_name)
        common.wait_for_and_click(device, calls_dict, "Accept_call_button")
        common.sleep_with_msg(device, 3, "Waiting after accepting full screen call")
        verify_call_connectivity_using_callee_text(caller_name)
        if common.is_element_present(device, calls_dict, "Accept_call_button"):
            raise AssertionError(f"{device} : Full screen call is still visible post accepting the same")
        if common.is_element_present(device, calls_dict, "Multiple_call_hold_ribbon"):
            common.wait_for_and_click(device, calls_dict, "Multiple_call_hold_ribbon_dropdown")
        common.wait_for_element(device, calls_dict, "Notification_group_call_answer_button")
        caller_name = common.wait_for_element(device, calls_dict, "caller_name_in_notification_call").text
        print("Caller name on notification call: ", caller_name)
        common.wait_for_and_click(device, calls_dict, "Notification_group_call_answer_button")
        common.sleep_with_msg(device, 3, "Waiting after accepting notification call")
        if transfer_method is not None:
            if transfer_method.lower() == "blind":
                blindtransfers_the_call(from_device, to_device, method)
                common.sleep_with_msg(device, 5, "Waiting after transfering the call ")
        if common.is_element_present(device, calls_dict, "Multiple_call_hold_ribbon"):
            common.wait_for_and_click(device, calls_dict, "Multiple_call_hold_ribbon_dropdown")
        if common.is_element_present(device, calls_dict, "Resume_call_from_hold_banner"):
            settings_keywords.click_device_center_point(device)
            verify_call_connectivity_using_callee_text(caller_name, count, state="toggle")
    elif full_screen_call == "accept" and notification_call == "reject":
        common.wait_for_element(device, calls_dict, "Accept_call_button")
        caller_name = common.wait_for_element(device, calls_dict, "caller_name_in_full_screen_call").text
        print("Caller name : ", caller_name)
        common.wait_for_and_click(device, calls_dict, "Accept_call_button")
        common.sleep_with_msg(device, 3, "Waiting after accepting full screen call")
        verify_call_connectivity_using_callee_text(caller_name)
        if common.is_element_present(device, calls_dict, "Accept_call_button"):
            raise AssertionError(f"{device} : Full screen call is still visible post accepting the same")
        if common.is_element_present(device, calls_dict, "Multiple_call_hold_ribbon"):
            common.wait_for_and_click(device, calls_dict, "Multiple_call_hold_ribbon_dropdown")
        common.wait_for_element(device, calls_dict, "Notification_group_call_answer_button")
        common.wait_for_and_click(device, calls_dict, "Reject_notification_call_btn")
        common.sleep_with_msg(device, 5, "Wait for notification call to disappear post rejecting it")
        if common.is_element_present(device, calls_dict, "Reject_notification_call_btn"):
            raise AssertionError(f"{device} : Notification call is still visible post rejecting the same")
    elif full_screen_call == "reject" and notification_call == "accept":
        common.wait_for_element(device, calls_dict, "Notification_group_call_answer_button")
        caller_name = common.wait_for_element(device, calls_dict, "caller_name_in_notification_call").text
        print("Caller name: ", caller_name)
        common.wait_for_and_click(device, calls_dict, "Notification_group_call_answer_button")
        common.sleep_with_msg(device, 3, "Waiting after accepting notification call")
        verify_call_connectivity_using_callee_text(caller_name)
        if common.is_element_present(device, calls_dict, "Accept_call_button"):
            raise AssertionError(f"{device} : Full screen call is still visible post accepting notification call")
        common.wait_for_element(device, calls_dict, "Notification_group_call_answer_button")
        common.wait_for_and_click(device, calls_dict, "Reject_notification_call_btn")
        common.sleep_with_msg(device, 5, "Wait for notification call to disappear post rejecting it")
        if common.is_element_present(device, calls_dict, "Reject_notification_call_btn"):
            raise AssertionError(f"{device} : Notification call is still visible post rejecting the same")
    else:
        raise AssertionError(
            f"Unexpected values for full_screen_call: {full_screen_call} , notification_call: {notification_call}"
        )
    return


def verify_call_connectivity_using_callee_text(caller_name, count="3", state=None):
    print(f"passed parameters: caller_name: {caller_name} count: {count} state: {state}")
    devices = list(config["devices"].keys())[: int(count)]
    print("devices : ", devices)
    for user in devices:
        if config["devices"][user]["user"]["displayname"] == caller_name:
            print(f"Answered the incoming call from device : {user}")
            determine_device_and_check_call_connectivity(user, state, count)


def determine_device_and_check_call_connectivity(device_name, state, count):
    print(f"passed parameters: user: {device_name} count: {count} state: {state}")
    if count not in ["3", "4"]:
        raise AssertionError(f"Unexpected value for count : {count}")
    if state is not None and state != "toggle":
        raise AssertionError(f"Unexpected value for state : {state}")
    devices_list = common.get_device_name_list(count)
    if device_name not in devices_list:
        raise AssertionError(f"Unexpected value for user : {device_name}")
    print(f"Devices list: {devices_list}")
    if state is None and count == "3":
        print(f"{device_name} : Verifying call connectivity state between two devices")
        if device_name == devices_list[1]:
            verify_call_state(device_list=devices_list[0:2], state="connected")
        elif device_name == devices_list[2]:
            verify_call_state(device_list=prepare_devices_list(0, 1, int(count)), state="connected")
    elif state == "toggle" and count == "3":
        print(f"{device_name} : Verifying call connectivity state between three devices")
        if device_name == devices_list[1]:
            verify_call_state(device_list=devices_list[0:2], state="connected")
            verify_call_state(device_list=devices_list[2], state="hold")
            resume_one_of_the_multiple_calls(device=devices_list[0], count=count)
            common.sleep_with_msg(
                device=devices_list[0], wait_seconds=5, why_message="Wait post resuming the held call"
            )
            verify_call_state(device_list=prepare_devices_list(0, 1, int(count)), state="connected")
            verify_call_state(device_list=devices_list[1], state="hold")
            resume_one_of_the_multiple_calls(device=devices_list[0], count=count)
            common.sleep_with_msg(
                device=devices_list[0], wait_seconds=5, why_message="Wait post resuming the held call"
            )
            verify_call_state(device_list=devices_list[0:2], state="connected")
            verify_call_state(device_list=devices_list[2], state="hold")
            disconnect_call(device=devices_list[2])
        elif device_name == devices_list[2]:
            verify_call_state(device_list=prepare_devices_list(0, 1, int(count)), state="connected")
            verify_call_state(device_list=devices_list[1], state="hold")
            resume_one_of_the_multiple_calls(device=devices_list[0], count=count)
            common.sleep_with_msg(
                device=devices_list[0], wait_seconds=5, why_message="Wait post resuming the held call"
            )
            verify_call_state(device_list=devices_list[0:2], state="connected")
            verify_call_state(device_list=devices_list[2], state="hold")
            resume_one_of_the_multiple_calls(device=devices_list[0], count=count)
            common.sleep_with_msg(
                device=devices_list[0], wait_seconds=5, why_message="Wait post resuming the held call"
            )
            verify_call_state(device_list=prepare_devices_list(0, 1, int(count)), state="connected")
            verify_call_state(device_list=devices_list[1], state="hold")
            disconnect_call(device=devices_list[1])
    elif state == "toggle" and count == "4":
        print(f"{device_name} : Verifying call connectivity state between four devices")
        if device_name == devices_list[1]:
            verify_call_state(device_list=devices_list[0:2], state="connected")
            verify_call_state(device_list=prepare_devices_list(0, 1, int(count)), state="hold")
            resume_one_of_the_multiple_calls(device=devices_list[0], count=count)
            common.sleep_with_msg(
                device=devices_list[0], wait_seconds=5, why_message="Wait post resuming the held call"
            )
            verify_call_state(device_list=prepare_devices_list(1, 2, int(count)), state="connected")
            verify_call_state(device_list=prepare_devices_list(0, 3, int(count)), state="hold")
            resume_one_of_the_multiple_calls(device=devices_list[0], count=count)
            common.sleep_with_msg(
                device=devices_list[0], wait_seconds=5, why_message="Wait post resuming the held call"
            )
            verify_call_state(device_list=prepare_devices_list(1, 3, int(count)), state="connected")
            verify_call_state(device_list=prepare_devices_list(0, 2, int(count)), state="hold")
            disconnect_call(device=prepare_devices_list(0, 2, int(count)))
        elif device_name == devices_list[2]:
            verify_call_state(device_list=prepare_devices_list(1, 3, int(count)), state="connected")
            verify_call_state(device_list=prepare_devices_list(0, 2, int(count)), state="hold")
            resume_one_of_the_multiple_calls(device=devices_list[0], count=count)
            common.sleep_with_msg(
                device=devices_list[0], wait_seconds=5, why_message="Wait post resuming the held call"
            )
            verify_call_state(device_list=prepare_devices_list(1, 2, int(count)), state="connected")
            verify_call_state(device_list=prepare_devices_list(0, 3, int(count)), state="hold")
            resume_one_of_the_multiple_calls(device=devices_list[0], count=count)
            common.sleep_with_msg(
                device=devices_list[0], wait_seconds=5, why_message="Wait post resuming the held call"
            )
            verify_call_state(device_list=devices_list[0:2], state="connected")
            verify_call_state(device_list=prepare_devices_list(0, 1, int(count)), state="hold")
            disconnect_call(device=prepare_devices_list(0, 1, int(count)))


def prepare_devices_list(start_index, end_index, count):
    if count not in [3, 4]:
        raise AssertionError(f"Unexpected value for count : {count}")
    if start_index > end_index or end_index > count - 1:
        raise AssertionError(f"Unexpected values for indices - start_index: {start_index} end_index: {end_index}")
    dev_list = common.get_device_name_list(count)
    req_dev_list = []
    if count == 3:
        for dev in dev_list[0:count]:
            if not dev_list.index(dev) == end_index:
                req_dev_list.append(dev)
    elif count == 4:
        for dev in dev_list[0:count]:
            if dev_list.index(dev) not in [start_index, end_index]:
                req_dev_list.append(dev)
    return req_dev_list


def verify_in_call_ribbon_from_main_tab(device):
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")
    common.sleep_with_msg(device, 5, "Wait for active call ribbon to appear")
    common.wait_for_and_click(device, calls_dict, "call_action_bar")
    verify_call_state(device, "connected")


def resume_one_of_the_multiple_calls(device, count):
    if count not in ["3", "4"]:
        raise AssertionError(f"Unexpected value for count : {count}")
    if count == "3":
        common.wait_for_and_click(device, calls_dict, "Resume_banner_icon")
    elif count == "4":
        common.wait_for_element(device, calls_dict, "Multiple_call_hold_ribbon")
        print(f"{device} : Multiple Calls are on hold ribbon is displayed")
        common.wait_for_and_click(device, calls_dict, "Multiple_call_hold_ribbon_dropdown")
        held_call_resume_btns = common.wait_for_element(
            device, calls_dict, "Resume_banner_icon", cond=EC.presence_of_all_elements_located
        )
        if len(held_call_resume_btns) == 2:
            held_call_resume_btns[0].click()
            common.tap_outside_the_popup(
                device, common.wait_for_element(device, calls_dict, "multiple_call_pop_up_container")
            )
        else:
            raise AssertionError(f"{device} : One of the held calls have dropped")


def verify_call_control_bar_in_meeting(device):
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_element(device, calls_dict, "meeting_mute_control")
    if not (
        common.is_element_present(device, calls_dict, "Add_participants_button")
        or common.is_element_present(device, calls_dict, "Add_participant_btn_portrait")
        or common.is_element_present(device, calls_dict, "participants_roster_button")
    ):
        raise AssertionError(f"{device} doesn't have add participant icon")

    open_call_more_options(device)
    # common.wait_for_and_click(device, calls_dict, "call_more_options")

    common.wait_for_element(device, calls_dict, "start_recording")
    if not common.is_element_present(device, calls_dict, "lock_meeting"):
        print(f"{device} : The user is not the organiser for this meeting. Hence, continuing")
    common.wait_for_element(device, calls_dict, "turn_on_live_captions")
    common.wait_for_element(device, calls_dict, "call_dialpad_under_more")

    dismiss_call_more_options(device)
    # device_right_corner_click(device)


def verify_work_voicemail_during_call_transfer(from_device, to_device, transfer_method):
    if transfer_method.lower() not in ["blind", "consult"]:
        raise AssertionError(f"Unexpected value for transfer method : {transfer_method}")
    common.wait_for_element(from_device, calls_dict, "Hang_up_button")
    if not common.click_if_present(from_device, calls_dict, "Transfer"):
        common.wait_for_and_click(from_device, calls_dict, "call_more_options")
        common.wait_for_and_click(from_device, calls_dict, "Transfer")
    if transfer_method.lower() == "blind":
        common.wait_for_and_click(from_device, calls_dict, "Transfer_now")
    elif transfer_method.lower() == "consult":
        common.wait_for_and_click(from_device, calls_dict, "consult_first")
    username = config["devices"][to_device]["user"]["displayname"]
    common.wait_for_element(from_device, calls_dict, "search_contact_box").send_keys(username)
    common.hide_keyboard(from_device)
    search_result = common.wait_for_element(from_device, calls_dict, "search_result_name")
    if not search_result.text == username:
        raise AssertionError(f"Expected user : {username} is not displayed in the search results on {from_device}")
    if transfer_method.lower() == "consult":
        if common.is_element_present(from_device, calls_dict, "overflow_menu"):
            raise AssertionError(f"{from_device} has overflow menu for displayed search result during consult transfer")
        common.wait_for_and_click(from_device, calls_dict, "Call_Back_Button")
        return
    common.wait_for_and_click(from_device, calls_dict, "overflow_menu")
    common.wait_for_element(from_device, calls_dict, "work_voicemail")


def transfer_call_to_work_voicemail(device):
    common.wait_for_and_click(device, calls_dict, "work_voicemail")


def verify_call_hold_banner(from_device, to_device):
    if ":" in to_device:
        account = to_device.split(":")[1]
        to_device = to_device.split(":")[0]
    else:
        account = "user"
    caller_name = common.wait_for_element(from_device, calls_dict, "caller_name_in_hold_banner").text
    print(f"Caller name in call banner is : {caller_name}")
    if caller_name != config["devices"][to_device][account]["displayname"]:
        raise AssertionError(f"Caller name in the call hold banner is not as expected")
    if common.is_element_present(from_device, calls_dict, "hold_label_time"):
        common.wait_for_element(from_device, calls_dict, "Resume")
    else:
        common.wait_for_element(from_device, calls_dict, "Resume_call_from_hold_banner")
        common.wait_for_element(from_device, calls_dict, "end_button_in_hold_banner")


def validate_notification_displayed_on_the_screen(device):
    print("device : ", device)
    if ":" in device:
        user = device.split(":")[1]
        print("User account : ", user)
        account = None
        if user.lower() == "cap_search_enabled":
            account = "cap_search_enabled"
    else:
        account = "user"
    print("Account :", account)
    device = device.split(":")[0]
    account_num = config["devices"][device][account]["pstndisplay"]
    your_num = common.wait_for_element(device, calls_dict, "your_number").text
    print(f"{your_num}, is your_num")
    print("Account_num:", account_num)
    common.wait_for_element(device, calls_dict, "emergency_call_in_progress_label")
    common.wait_for_element(device, calls_dict, "emergency_call_icon")
    num = str(your_num)
    if num.split(": ")[1] != account_num.strip("+"):
        raise AssertionError(f"Number '{num.split(':')[1]}' does not match account number '{account_num.strip('+')}' ")


def verify_user_name_display_on_call_toast(to_device, from_device):
    time.sleep(display_time)
    if ":" in from_device:
        user = from_device.split(":")[1]
        print("User account : ", user)
        account = None
        if user.lower() == "cap_search_enabled":
            account = "cap_search_enabled"
        elif user.lower() == "pstn_user":
            account = "pstn_user"
    else:
        account = "user"
    print("Account :", account)
    from_device = from_device.split(":")[0]
    from_device_displayname = config["devices"][from_device][account]["displayname"]
    print("from_device_displayname : ", from_device_displayname)
    calling_text = common.wait_for_element(to_device, calls_dict, "calling_text").text
    print("calling_text : ", calling_text)
    if calling_text != from_device_displayname:
        raise AssertionError("Display Name is not matching on Call toast")


def verify_did_number_on_dialpad(device):
    prt_flag = False
    user = "user"
    if ":" in device:
        user = device.split(":")[1]
        device = device.split(":")[0]
    if not common.click_if_present(device, calendar_dict, "floating_dialpad_icon"):
        if not common.is_portrait_mode_cnf_device(device):
            raise AssertionError(f"{device} unable to click on dialpad icon")
        common.wait_for_and_click(device, calendar_dict, "app_bar_dialpad_icon")
        prt_flag = True
    print(f"portrait flag: {prt_flag}")
    if not prt_flag:
        text1 = common.wait_for_element(device, calls_dict, "user_phone_num").text
    else:
        text1 = common.wait_for_element(device, calls_dict, "cnf_user_phone_num").text
    text2 = "Your number is: " + config["devices"][device][user]["pstndisplay"]
    print(f"Number on {device} : {text1}")
    print(f"Number expected : {text2}")
    if text1 != text2:
        raise AssertionError(f"{user} in {device} is not displayed with DID number on diaplad")


def is_dialpad_supported(device):
    if config["devices"][device]["model"].lower() in ["los angeles", "riverside", "phoenix", "gilbert", "riverside_13"]:
        common.wait_for_and_click(device, calls_dict, "Call_Back_Button")
        return False
    # Check for landscpae mode desk phones
    if not common.is_element_present(device, calls_dict, "dial_pad"):
        # Check for portrait mode desk phones
        if not common.click_if_present(device, calls_dict, "Make_a_call"):
            # Check for portrait mode conf phones
            if common.is_portrait_mode_cnf_device(device):
                common.wait_for_and_click(device, calendar_dict, "app_bar_dialpad_icon")
            else:
                # Check for landscpae mode conf phones
                if not common.click_if_present(device, calls_dict, "call_dialpad"):
                    raise AssertionError(f"Dial pad is absent for the user on {device}")
    common.wait_for_element(device, calls_dict, "dial_pad_field")
    common.wait_for_element(device, calls_dict, "call_icon1")
    return True


def place_outgoing_call_from_soft_dialpad(from_device, to_device):
    driver = obj.device_store.get(alias=from_device)
    if ":" in to_device:
        account = to_device.split(":")[1]
        to_device = to_device.split(":")[0]
    else:
        account = "user"
    number_list = list(config["devices"][to_device][account]["phonenumber"])
    entered_number = config["devices"][to_device][account]["pstndisplay"]
    temp_dict = common.get_dict_copy(calls_dict, "user_phone_number", "phone_number", entered_number)
    num_map = {
        "0": "zero",
        "1": "one",
        "2": "two",
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
        "8": "eight",
        "9": "nine",
    }
    elem = common.wait_for_element(from_device, calls_dict, "zero")
    actions = TouchAction(driver)
    actions.long_press(elem, duration=1000).release().perform()
    for num in number_list:
        if num not in num_map.keys():
            raise AssertionError(f"Unexpected character encountered: {num}")
        common.wait_for_and_click(from_device, calls_dict, num_map[num])
    common.wait_for_element(from_device, temp_dict, "user_phone_number")
    if common.click_if_present(from_device, calls_dict, "myself_xpath"):
        print(f"*WARN*:: {from_device}: Found and used unexpected 'myself' OBO")
    common.wait_for_element(from_device, calls_dict, "Hang_up_button")


def call_from_recent_tab_using_call_history(from_device, to_device):
    temp_dict = common.get_dict_copy(
        calls_dict, "call_participant_name", "config_display", config["devices"][to_device]["user"]["displayname"]
    )
    common.wait_for_and_click(from_device, temp_dict, "call_participant_name", "xpath")
    common.wait_for_and_click(from_device, calls_dict, "call_list_item_call_action")
    if common.click_if_present(from_device, calls_dict, "myself_xpath"):
        print(f"*WARN*:: {from_device}: Found and used unexpected 'myself' OBO")
    common.wait_for_element(from_device, calls_dict, "Hang_up_button")


def verify_not_have_video_option_in_conference_window(device):
    if common.is_element_present(device, calls_dict, "video_on"):
        raise AssertionError(f"{device} user having video option in conference window")


def calling_with_dailpad(from_device, to_device):
    driver = obj.device_store.get(alias=from_device)
    account = "user"
    if ":" in to_device:
        user = to_device.split(":")[1]
        print("User account : ", user)
        if user.lower() == "pstn_user":
            account = "pstn_user"
    print("Account :", account)
    to_device = to_device.split(":")[0]
    print("to_device : ", to_device)
    if common.is_screen_size_7_inch_or_more(from_device):
        common.wait_for_and_click(from_device, calls_dict, "calls_tab")
    time.sleep(action_time)
    common.click_if_element_appears(from_device, calls_dict, "Make_a_call", max_attempts=5)
    user_phonenumber = config["devices"][to_device][account]["phonenumber"]
    elem = common.wait_for_element(from_device, calls_dict, "zero")
    actions = TouchAction(driver)
    actions.long_press(elem, duration=1000).release().perform()
    entered_number = config["devices"][to_device][account]["pstndisplay"]
    temp_dict = common.get_dict_copy(calls_dict, "user_phone_number", "phone_number", entered_number)
    ele = common.wait_for_element(from_device, calls_dict, "dial_pad_field")
    for no in user_phonenumber:
        if no == str(9):
            common.wait_for_and_click(from_device, calls_dict, "nine")
        elif no == str(8):
            common.wait_for_and_click(from_device, calls_dict, "eight")
        elif no == str(7):
            common.wait_for_and_click(from_device, calls_dict, "seven")
        elif no == str(6):
            common.wait_for_and_click(from_device, calls_dict, "six")
        elif no == str(5):
            common.wait_for_and_click(from_device, calls_dict, "five")
        elif no == str(4):
            common.wait_for_and_click(from_device, calls_dict, "four")
        elif no == str(3):
            common.wait_for_and_click(from_device, calls_dict, "three")
        elif no == str(2):
            common.wait_for_and_click(from_device, calls_dict, "two")
        elif no == str(1):
            common.wait_for_and_click(from_device, calls_dict, "one")
        elif no == str(0):
            common.wait_for_and_click(from_device, calls_dict, "zero")
    common.wait_for_element(from_device, temp_dict, "user_phone_number")
    # common.wait_for_and_click(from_device, calls_dict, "call_icon1")
    common.wait_for_element(from_device, calls_dict, "Decline_call_button")


def dial_an_incorrect_number(device, method):
    if method.lower() not in config["incorrect_number"].keys():
        raise AssertionError(f"Unexpected value for method : {method}")
    phonenumber = config["incorrect_number"]["phonenumber"]
    common.click_if_present(device, calendar_dict, "floating_dialpad_icon")
    common.click_if_element_appears(device, calls_dict, "dialpad_tab")
    element = common.wait_for_element(device, calls_dict, "dial_pad_field")
    element.send_keys(phonenumber)
    time.sleep(display_time)
    common.wait_for_and_click(device, calls_dict, "call_icon1")
    print(f"{device}:Entered Phone number:{phonenumber}")
    time.sleep(action_time)


def verify_ui_came_to_home_page(device):
    if not common.is_element_present(device, calls_dict, "dial_pad"):
        if not common.is_element_present(device, calls_dict, "recent_tab"):
            raise AssertionError(f"{device} UI is not returned to the home screen")


def verify_call_control_bar_in_meeting_for_cnf_device(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    common.wait_for_element(device, calls_dict, "call_control_speaker")
    common.wait_for_element(device, calls_dict, "meeting_mute_control")
    if not common.is_element_present(device, calls_dict, "Add_participants_button"):
        if not common.is_element_present(device, calls_dict, "Add_participant_btn_portrait"):
            raise AssertionError(f"{device} couldn't find add participants btn")
    common.wait_for_and_click(device, calls_dict, "call_more_options")
    common.wait_for_element(device, calls_dict, "lock_meeting")
    common.wait_for_element(device, calendar_dict, "turn_on_live_captions")
    common.wait_for_element(device, calendar_dict, "dial_pad")
    common.wait_for_and_click(device, calendar_dict, "touch_outside")


def verify_call_cancelled_screen_autodismiss(device):
    ele = common.wait_for_element(device, calls_dict, "call_cancelled_screen", wait_attempts=50)
    common.wait_for_element(device, calls_dict, "Redial_button", "xpath")
    print(f"{device} Call cancelled screen is visible :", ele.text)
    text = "Call canceled"
    if ele.text != text:
        raise AssertionError("Call cancelled screen is not visible ", ele.text)
    time.sleep(5)
    if common.is_element_present(device, calls_dict, "Redial_button") and common.is_element_present(
        device, calls_dict, "end_call_callee_text"
    ):
        raise AssertionError("Call cancelled  screen still visible after 5 seconds")
    print("Call cancelled screen got dismiss automatically within 5 seconds")


def dial_a_number_from_dialpad(device):
    devices = device.split(",")
    time.sleep(10)
    print("Devices : ", devices)
    if not common.click_if_present(device, calendar_dict, "floating_dialpad_icon"):
        common.wait_for_and_click(device, calendar_dict, "app_bar_dialpad_icon")
    given_numbers = "12345"
    ele = common.wait_for_element(device, calls_dict, "phone_number")
    ele.click()
    for i in given_numbers:
        common.wait_for_and_click(device, calendar_dict, i)
    print(f"Dialed number from dial pad is : {ele.text}")


def click_on_the_dial_pad(device):
    if not common.click_if_present(device, calendar_dict, "floating_dialpad_icon"):
        common.wait_for_and_click(device, calendar_dict, "app_bar_dialpad_icon")


def verify_multiple_incoming_calls_in_DND_status(device):
    if common.is_element_present(device, calls_dict, "Accept_call_button") or common.is_element_present(
        device, calls_dict, "Notification_group_call_answer_button"
    ):
        raise AssertionError("Device still received Incoming call")


def make_multiple_outgoing_calls_using_call_icon(from_device, to_devices):
    print(f"from_device: {from_device}, to_device: {to_devices}")
    to_device = to_devices.split(",")
    devices = []
    accounts = []
    for device in to_device:
        device, account = common.decode_device_spec(device)
        devices.append(device)
        accounts.append(account)
    print("Contact devices : ", devices)
    print("Accounts : ", accounts)
    navigate_to_calls_tab(from_device)
    time.sleep(display_time)
    if common.is_portrait_mode_cnf_device(from_device):
        common.wait_for_and_click(from_device, calls_dict, "Make_a_call")
        common.wait_for_and_click(from_device, calls_dict, "people_tab")
    for device, account in zip(devices, accounts):
        displayname = config["devices"][device][account]["displayname"]
        username = config["devices"][device][account]["username"].split("@")[0]
        common.wait_for_and_click(from_device, calls_dict, "search")
        time.sleep(3)
        if common.is_element_present(from_device, calls_dict, "search_contact_box"):
            common.wait_for_element(from_device, calls_dict, "search_contact_box").send_keys(username)
        else:
            common.wait_for_element(from_device, calls_dict, "search_text").send_keys(username)
        tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", displayname)
        common.wait_for_and_click(from_device, tmp_dict, "search_result_item_container", "xpath")
    common.wait_for_and_click(from_device, calls_dict, "Make_an_audio_call")
    common.wait_while_present(from_device, calls_dict, "Make_an_audio_call")
    if common.click_if_present(from_device, calls_dict, "myself_xpath"):
        print(f"*WARN*:: {from_device}: Found and used unexpected 'myself' OBO")
    common.wait_for_element(from_device, calls_dict, "Hang_up_button")


def tap_on_the_banner(device):
    print("device :", device)
    common.wait_for_and_click(device, calls_dict, "caller_name_in_hold_banner")


def verify_call_park_banner(from_device, to_device):
    caller_name = common.wait_for_element(from_device, calls_dict, "caller_name_in_hold_banner").text
    print(f"Caller name in call park banner is : {caller_name}")
    if caller_name != common.device_displayname(to_device):
        raise AssertionError(f"{caller_name} in call park banner is not expected as {to_device}")
    common.wait_for_element(from_device, calls_dict, "call_unpark_code_from_banner")
    common.wait_for_element(from_device, calls_dict, "close_button_in_call_park_banner")


def verify_multiple_calls_on_hold_in_banner(from_device, to_device):
    hold_banner_devices = []
    to_devices = to_device.split(",")
    for device in to_devices:
        disp_name = common.device_displayname(device)
        hold_banner_devices.append(disp_name)
    print("Expected users in hold banner are :", hold_banner_devices)
    common.click_if_present(from_device, calls_dict, "Call_Back_Button")
    time.sleep(2)
    common.wait_for_and_click(from_device, calls_dict, "Multiple_call_hold_ribbon_dropdown")
    held_user_call_list = common.get_all_elements_texts(from_device, calls_dict, "caller_name_in_hold_banner")
    print(f"User names inside multiple call banner are :{held_user_call_list}")
    for device_name in hold_banner_devices:
        if device_name not in held_user_call_list:
            raise AssertionError(
                f"{from_device}: Expected user: {device_name} not in list of held calls {held_user_call_list}"
            )
    common.wait_for_element(from_device, calls_dict, "Resume_call_from_hold_banner")
    common.wait_for_element(from_device, calls_dict, "end_button_in_hold_banner")
    if common.is_element_present(from_device, calls_dict, "close_button_in_call_park_banner"):
        common.wait_for_element(from_device, calls_dict, "call_unpark_code_from_banner")
    common.tap_outside_the_popup(
        from_device, common.wait_for_element(from_device, calls_dict, "multiple_call_pop_up_container")
    )


def close_call_park_banner(device):
    common.wait_for_and_click(device, calls_dict, "close_button_in_call_park_banner")


def verify_and_close_call_park_banner(device):
    if common.is_element_present(device, calls_dict, "close_button_in_call_park_banner"):
        close_call_park_banner(device)


def verify_gcp_call_name_on_call_toast(device, from_device):
    time.sleep(display_time)
    devices = device.split(",")
    for device in devices:
        print("device : ", device)
        account = "user"
        if ":" in from_device:
            user = from_device.split(":")[1]
            print("User account : ", user)
            if user.lower() == "cap_search_enabled":
                account = "cap_search_enabled"
            elif user.lower() == "delegate_user":
                account = "delegate_user"
        from_device = from_device.split(":")[0]
        from_device_displayname = config["devices"][from_device][account]["displayname"]
        print("from_device_discplayname: ", from_device_displayname)
        gcp_call_text = "Call " + "for " + from_device_displayname
        print("gcp_call_text : ", gcp_call_text)
        time.sleep(display_time)
        call_text = common.wait_for_element(
            device, calls_dict, "caller_name_in_notification_call", wait_attempts=40
        ).text
        print("call_text : ", call_text)
        if gcp_call_text != call_text:
            raise AssertionError(f"{gcp_call_text} gcp incoming call name is not matched with the  {call_text}")


def verify_call_rating_screen_after_disconnect_call(device, status="appear"):
    devices = device.split(",")
    for device in devices:
        if status == "appear":
            common.wait_for_and_click(device, calls_dict, "Hang_up_button")
            # Call rating screen doesn't appear after every call
            if common.is_element_present(device, calls_dict, "Call_Rating"):
                common.sleep_with_msg(device, 5, "Waiting for auto dismissal of call rating screen")
                if common.is_element_present(device, calls_dict, "Call_Rating"):
                    raise AssertionError(f"{device}: Call rating screen didn't auto dismiss in 5 seconds")
        elif status == "disappear":
            common.wait_for_and_click(device, calls_dict, "Hang_up_button")
            time.sleep(display_time)
            if common.is_element_present(device, calls_dict, "Call_Rating"):
                raise AssertionError(f"Call rating screen still appear at {device}")


def verify_view_profile_options_in_favorites_page(from_device, to_device):
    navigate_to_calls_favorites_page(from_device)
    added_user_displayname = config["devices"][to_device]["user"]["displayname"]
    added_user_username = config["devices"][to_device]["user"]["username"]
    if config["devices"][from_device]["model"].lower() == "gilbert":
        calendar_keywords.scroll_down_secondary_tab(from_device)
    temp_dict = common.get_dict_copy(calls_dict, "favorites_more_options", "user_name", added_user_displayname)
    common.wait_for_and_click(from_device, temp_dict, "favorites_more_options", "xpath")
    common.wait_for_and_click(from_device, calls_dict, "view_profile_option")
    user_displayname = common.wait_for_element(from_device, calls_dict, "user_display_name", "xpath").text
    if user_displayname != added_user_displayname:
        raise AssertionError(f"{to_device} display name is not founded")
    mail_id = common.wait_for_element(from_device, calls_dict, "mail_id").text
    if mail_id != added_user_username:
        raise AssertionError(f"{from_device}: Expected email ID: '{added_user_username}', but  found: '{mail_id}'")
    common.wait_for_element(from_device, calls_dict, "Make_an_audio_call")


def navigate_to_user_survey(device):
    if common.is_element_present(device, settings_dict, "Calling"):
        common.wait_for_and_click(device, settings_dict, "Calling")
    else:
        settings_keywords.open_settings_page(device)
        if not common.click_if_element_appears(device, settings_dict, "Calling", max_attempts=5):
            print(f"{device}: Calling option mostly inside device settings")
            common.wait_for_and_click(device, settings_dict, "Device_Settings")
            device_settings_keywords.advance_calling_option_oem(device)
    _max_attempts = 5
    for _attempt in range(_max_attempts):
        time.sleep(display_time)
        if common.is_element_present(device, device_settings_dict, "dismiss_rate_my_call"):
            common.wait_for_element(device, device_settings_dict, "user_survey")
            print(f"{device}: After scrolling {_attempt} times found User survey")
            break
        else:
            calendar_keywords.scroll_only_once(device)
    common.wait_for_element(device, device_settings_dict, "user_survey")


def enable_dismiss_rate_my_call_toggle(device):
    enable_or_disable_dismiss_rate_my_call_toggle(device, "ON")


def disable_dismiss_rate_my_call_toggle(device):
    enable_or_disable_dismiss_rate_my_call_toggle(device, "OFF")
    come_back_to_home_screen(device)


def verify_dismiss_rate_my_call_toggle(device, toggle):
    global state
    if toggle.lower() not in ["on", "off"]:
        raise AssertionError(f"Illegal value for 'toggle': '{toggle}'")
    if not common.is_element_present(device, device_settings_dict, "dismiss_rate_toggle_btn"):
        navigate_to_user_survey(device)
    dismiss_rate_my_call_toggle = common.wait_for_element(device, device_settings_dict, "dismiss_rate_toggle_btn")
    dismiss_rate_my_call_toggle_status = dismiss_rate_my_call_toggle.get_attribute("checked")
    print(f"dismiss_rate_my_call_toggle_status :{dismiss_rate_my_call_toggle_status}")
    if toggle == "on":
        state = "true"
    elif toggle == "off":
        state = "false"
    if toggle.lower() == "on":
        if state != dismiss_rate_my_call_toggle_status:
            raise AssertionError(f"Displayed toggle is not enabled state")
    if toggle.lower() == "off":
        if state != dismiss_rate_my_call_toggle_status:
            raise AssertionError(f"Displayed toggle is not in disabled state")


def verify_pstn_display_number_on_incoming_call_UI(from_device, to_device):
    print("from_device :", from_device)
    print("to_device :", to_device)
    expected_pstn_display_num = common.device_pstndisplay(to_device)
    common.wait_for_element(from_device, calls_dict, "Accept_call_button")
    common.wait_for_element(from_device, calls_dict, "Decline_call_button")
    tmp_dict = common.get_dict_copy(calendar_dict, "add_user", "user_name", expected_pstn_display_num)
    common.wait_for_element(from_device, tmp_dict, "add_user")


def verify_call_hold_banner_for_pstn(from_device, to_device):
    if ":" in to_device:
        account = to_device.split(":")[1]
        to_device = to_device.split(":")[0]
    caller_name = common.wait_for_element(from_device, calls_dict, "caller_name_in_hold_banner").text
    expected_pstn_display_num = config["devices"][to_device][account]["phonenumber"]
    caller_phone_number = "".join(e for e in caller_name if e.isalnum())
    expected_pstn_display_num1 = "".join(e for e in expected_pstn_display_num if e.isalnum())
    print(f"Caller name in call banner is : {caller_name}")
    if caller_phone_number != expected_pstn_display_num1:
        raise AssertionError(
            f"{caller_name} Caller name in the call hold banner is not as expected {expected_pstn_display_num}"
        )
    if common.is_element_present(from_device, calls_dict, "hold_label_time"):
        common.wait_for_element(from_device, calls_dict, "Resume")
    else:
        common.wait_for_element(from_device, calls_dict, "Resume_call_from_hold_banner")
        common.wait_for_element(from_device, calls_dict, "end_button_in_hold_banner")


def remove_favorite_contacts_from_favorites_tab(device):
    time.sleep(display_time)
    if common.is_element_present(device, calls_dict, "favorites_without_contacts_grid"):
        print(f"{device}: Favorites tab is empty, no contacts, returning..")
        return
    if not common.is_element_present(device, calls_dict, "speed_dial_header"):
        print(f"{device}: User doesn't have any speed dial contacts")
        return
    common.click_if_element_appears(device, calls_dict, "people_you_support", max_attempts=5)
    common.click_if_element_appears(device, calls_dict, "your_delegates", max_attempts=5)
    _max_attempts = 5
    for _attempt in range(_max_attempts):
        time.sleep(display_time)
        if common.is_element_present(device, calls_dict, "favorites_more_options"):
            common.wait_for_and_click(device, calls_dict, "favorites_more_options")
            common.wait_for_and_click(device, calls_dict, "remove_favorites_option")
            time.sleep(5)
            settings_keywords.refresh_calls_main_tab(device)
            time.sleep(display_time)
            if not common.is_element_present(device, calls_dict, "speed_dial_header"):
                print("Speed dial header not found. Hence breaking the loop.")
                break
        else:
            raise AssertionError(f"{device}: Couldn't remove the user from favorites tab")
    common.click_if_element_appears(device, calls_dict, "people_you_support", max_attempts=5)
    common.click_if_element_appears(device, calls_dict, "your_delegates", max_attempts=5)


def verify_call_transfer_option_in_CAP_search_disabled_user(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    common.wait_for_and_click(device, calls_dict, "Transfer")
    if common.is_element_present(device, calls_dict, "Transfer_now"):
        raise AssertionError(f"{device} contain call Transfer option during outgoing call")
    common.wait_for_and_click(device, calls_dict, "call_more_options")
    time.sleep(action_time)
    if common.click_if_present(device, calls_dict, "Transfer"):
        if common.is_element_present(device, calls_dict, "Transfer_now"):
            raise AssertionError(f"{device} contain call Transfer option during outgoing call")


def verify_call_park_cancel_button(park_code, device):
    common.wait_for_and_click(device, calls_dict, "unpark_call")
    unpark_code_input = common.wait_for_element(device, calls_dict, "unpark_code_edit_text")
    print("park_code : ", park_code)
    unpark_code_input.send_keys(park_code)
    common.wait_for_element(device, calls_dict, "unpark_call_ok_button")
    common.wait_for_element(device, calls_dict, "call_park_cancel")
    common.wait_for_and_click(device, calls_dict, "call_park_cancel")
    common.wait_for_element(device, calls_dict, "unpark_call")


def verify_auto_dial_with_insufficient_extension_num_from_dial_pad(from_device, to_device):
    print("from_device :", from_device)
    print("to_device :", to_device)
    if ":" in to_device:
        user = to_device.split(":")[1]
        print("User account : ", user)
        account = None
        if user.lower() == "pstn_user":
            account = "pstn_user"
        elif user.lower() == "cap_search_enabled":
            account = "cap_search_enabled"
        elif user.lower() == "cap_search_disabled":
            account = "cap_search_disabled"
        elif user.lower() == "delegate_user":
            account = "delegate_user"
    else:
        account = "user"
    print("Account :", account)
    to_device = to_device.split(":")[0]
    print("to_device : ", to_device)
    displayname = config["devices"][to_device][account]["displayname"]
    extnumber = config["devices"][to_device][account]["extension"]
    time.sleep(action_time)
    if not common.is_element_present(from_device, calls_dict, "call"):
        common.wait_for_and_click(from_device, calls_dict, "Make_a_call")
    number_field = common.wait_for_element(from_device, calls_dict, "phone_number")
    insufficient_extension_num = extnumber[3:7]
    number_field.send_keys(insufficient_extension_num)
    time.sleep(10)
    if common.is_element_present(from_device, calls_dict, "Hang_up_button"):
        raise AssertionError("Device is auto dailed")


def verify_call_tab_in_expanded_dialpad(device):
    common.wait_for_and_click(device, calls_dict, "calls_tab")
    common.wait_for_element(device, calls_dict, "dial_pad_field")
    common.wait_for_element(device, calls_dict, "call_icon1")
    common.wait_for_element(device, calls_dict, "call_park")
    common.wait_for_element(device, calls_dict, "search")
    common.wait_for_element(device, calls_dict, "backspace")
    common.wait_for_element(device, calls_dict, "nine")
    common.wait_for_element(device, calls_dict, "eight")
    common.wait_for_element(device, calls_dict, "seven")
    common.wait_for_element(device, calls_dict, "six")
    common.wait_for_element(device, calls_dict, "five")
    common.wait_for_element(device, calls_dict, "four")
    common.wait_for_element(device, calls_dict, "three")
    common.wait_for_element(device, calls_dict, "two")
    common.wait_for_element(device, calls_dict, "one")
    common.wait_for_element(device, calls_dict, "zero")


def verify_and_navigate_to_call_plus_icon_people_tab(device):
    navigate_to_calls_tab(device)
    common.wait_for_and_click(device, calls_dict, "Make_a_call")
    common.wait_for_element(device, calls_dict, "make_a_call_text")
    common.wait_for_element(device, calls_dict, "call_park")
    if common.is_portrait_mode_cnf_device(device):
        common.wait_for_and_click(device, calls_dict, "people_tab")
    common.wait_for_element(device, calls_dict, "search_contact_box")


def verify_dailpad_is_selected_by_default(device):
    elem = common.wait_for_element(device, calls_dict, "dialpad_tab")
    temp = elem.get_attribute("selected")
    if temp != "true":
        raise AssertionError(f"Dial Pad option is not selected by default")


def verify_options_in_make_call_icon(device):
    common.wait_for_and_click(device, calls_dict, "Make_a_call")
    common.wait_for_element(device, calls_dict, "make_a_call_text")
    common.wait_for_element(device, calls_dict, "call_park")
    if common.is_portrait_mode_cnf_device(device):
        verify_dailpad_is_selected_by_default(device)
        common.wait_for_and_click(device, calls_dict, "people_tab")
    common.wait_for_element(device, calls_dict, "search_contact_box")


def verify_outgoing_call_ui(device, state):
    if state.lower() not in ["connecting", "connected"]:
        raise AssertionError(f"Illegal value for 'state': '{state}'")
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    common.wait_for_element(device, calls_dict, "call_mute_control")
    common.wait_for_element(device, calls_dict, "call_more_options")
    if state.lower() == "connecting":
        elem = common.wait_for_element(device, calls_dict, "Put_call_on_hold")
        temp = elem.get_attribute("enabled")
        if temp != "false":
            raise AssertionError(f"Hold option is in enabled state")
        elem = common.wait_for_element(device, calls_dict, "Transfer", "id")
        temp = elem.get_attribute("enabled")
        if temp != "false":
            raise AssertionError(f"Transfer option is in enabled state")
    elif state.lower() == "connected":
        elem = common.wait_for_element(device, calls_dict, "Put_call_on_hold")
        temp = elem.get_attribute("enabled")
        if temp != "true":
            raise AssertionError(f"Hold option is not in enabled state")
        elem = common.wait_for_element(device, calls_dict, "Transfer", "id")
        temp = elem.get_attribute("enabled")
        if temp != "true":
            raise AssertionError(f"Transfer option is not in enabled state")


def verify_resume_banner(device_list):
    devices = device_list.split(",")
    for device in devices:
        common.wait_for_element(device, calls_dict, "Resume_banner_icon")


def verify_people_you_support_in_favorites_page(from_device, to_device):
    print("from_device :", from_device)
    print("to_device :", to_device)
    navigate_to_calls_favorites_page(from_device)
    time.sleep(action_time)
    to_devices = to_device.split(",")
    for device in to_devices:
        account = "user"
        if ":" in device:
            user = to_device.split(":")[1]
            print("User account : ", user)
            if user.lower() == "delegate_user":
                account = "delegate_user"
            elif user.lower() == "meeting_user":
                account = "meeting_user"
            elif user.lower() == "cap_search_enabled":
                account = "cap_search_enabled"
        print("Account :", account)
        to_device = to_device.split(":")[0]
        print("to_device : ", to_device)
        added_delegate_user_displayname = config["devices"][to_device][account]["displayname"]
        print("added_delegate_user_displayname is :", added_delegate_user_displayname)
        people_you_support_text = common.wait_for_element(from_device, calls_dict, "people_you_support").text
        if people_you_support_text != "People you support":
            raise AssertionError(f"{from_device}: doesn't have people you support under favorites tab")
        temp_dict = common.get_dict_copy(
            calls_dict, "favorite_user_in_favorite_page", "user_name", added_delegate_user_displayname
        )
        common.wait_for_element(from_device, temp_dict, "favorite_user_in_favorite_page")


def navigate_to_lightweight_calling_experience(device):
    time.sleep(action_time)
    if not common.is_element_present(device, settings_dict, "Calling"):
        settings_keywords.open_settings_page(device)
        if not common.click_if_element_appears(device, settings_dict, "Calling", max_attempts=5):
            print(f"{device}: Calling option mostly inside device settings")
            common.wait_for_and_click(device, settings_dict, "Device_Settings")
            device_settings_keywords.advance_calling_option_oem(device)
            device_settings_keywords.swipe_till_sign_out(device)
            device_settings_keywords.swipe_till_sign_out(device)
            common.wait_for_and_click(device, settings_dict, "Calling")
    time.sleep(display_time)
    _max_attempts = 5
    for _attempt in range(_max_attempts):
        if common.is_element_present(device, settings_dict, "Calling_experience"):
            common.wait_for_element(device, settings_dict, "Enable_lightweight_meeting_experience")
            break
        else:
            calendar_keywords.scroll_only_once(device)


def disable_lightweight_calling_experience(device):
    ele = common.wait_for_element(device, settings_dict, "Enable_lightweight_calling_experience_toggle_btn").text
    print(ele)
    if ele.lower() != "off":
        common.wait_for_and_click(device, settings_dict, "Enable_lightweight_calling_experience_toggle_btn")
    ele = common.wait_for_element(device, settings_dict, "Enable_lightweight_calling_experience_toggle_btn").text
    if ele.lower() != "off":
        raise AssertionError(
            f"{device} is unable to disable lightweight calling experience toggle,toggle status :{ele}"
        )


def enable_lightweight_calling_experience(device):
    ele = common.wait_for_element(device, settings_dict, "Enable_lightweight_calling_experience_toggle_btn").text
    print(ele)
    if ele.lower() != "on":
        common.wait_for_and_click(device, settings_dict, "Enable_lightweight_calling_experience_toggle_btn")
    ele = common.wait_for_element(device, settings_dict, "Enable_lightweight_calling_experience_toggle_btn").text
    if ele.lower() != "on":
        raise AssertionError(
            f"{device} is unable to enable lightweight calling experience toggle ,toggle status :{ele}"
        )


def verify_lightweight_calling_experience_toggle_enabled_by_default(device):
    navigate_to_lightweight_calling_experience(device)
    ele = common.wait_for_element(device, settings_dict, "Enable_lightweight_calling_experience_toggle_btn").text
    if ele.lower() != "on":
        raise AssertionError(
            f"{device} lightweight calling experience toggle not enabled by default ,toggle status :{ele}"
        )


def verify_calling_ui_at_lightweight_calling_experience_is_disabled(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    time.sleep(action_time)
    if common.is_element_present(device, calls_dict, "Transfer") or common.is_element_present(
        device, calls_dict, "Put_call_on_hold"
    ):
        raise AssertionError(f"{device} calling ui not changed after lightweight calling experience toggle disabled")


def verify_no_resume_banner_present_in_home_screen(device):
    if common.is_element_present(device, calls_dict, "Resume_banner_icon"):
        raise AssertionError(f"{device} contain resume banner in home screen")


def verify_call_plus_icon_absence_in_landscape_devices(device):
    if common.is_portrait_mode_cnf_device(device):
        return
    navigate_to_calls_tab(device)
    time.sleep(action_time)
    if common.is_element_present(device, calls_dict, "Make_a_call"):
        raise AssertionError(f"{device} still contains call plus icon")
    common.wait_for_element(device, calls_dict, "recent_tab")
    common.wait_for_element(device, calls_dict, "favorites_tab")
    common.wait_for_element(device, calls_dict, "call_icon1")
    common.wait_for_element(device, calls_dict, "call_park")
    common.wait_for_element(device, calls_dict, "entered_phn_num")
    common.wait_for_element(device, calls_dict, "search")


def verify_default_all_call_history_should_be_selected(device):
    common.wait_for_element(device, calls_dict, "recent_tab")
    common.wait_for_and_click(device, calls_dict, "recent_filter_button")
    common.wait_for_element(device, calls_dict, "recent_tab_filter_selected_all")
    common.wait_for_and_click(device, calls_dict, "recent_tab_filter_all")
    ele = common.wait_for_element(device, calls_dict, "recent_tab_filter_title").text
    if ele != "All":
        raise AssertionError(f"{device} is not founded expected text in recent tab sort filter title:{ele}")


def verify_sorting_options_in_recent_tab(device):
    navigate_to_calls_tab(device)
    common.wait_for_element(device, calls_dict, "recent_tab")
    common.wait_for_and_click(device, calls_dict, "recent_filter_button")
    common.wait_for_and_click(device, calls_dict, "recent_tab_filter_all")
    common.sleep_with_msg(device, 5, "Waiting for sorting to be complete")
    ele = common.wait_for_element(device, calls_dict, "recent_tab_filter_title").text
    if ele != "All":
        raise AssertionError(f"{device} is not founded expected text in recent tab sort filter title:{ele}")
    duration_text = common.get_all_elements_texts(device, calls_dict, "call_duration")
    duration_texts = [item.split(":")[0] for item in duration_text]
    if len(set(duration_texts)) <= 1:
        raise AssertionError(f"{device}: recent tab is not showing all the items:{duration_texts}")
    common.wait_for_and_click(device, calls_dict, "recent_filter_button")
    common.wait_for_and_click(device, calls_dict, "recent_tab_filter_incoming")
    ele = common.wait_for_element(device, calls_dict, "recent_tab_filter_title").text
    if ele != "Incoming":
        raise AssertionError(f"{device} is not founded expected text in recent tab sort filter title:{ele}")
    duration_text = common.get_all_elements_texts(device, calls_dict, "call_duration")
    duration_texts = list(set([item.split(":")[0] for item in duration_text]))
    if duration_texts[0] != "Incoming" or len(duration_texts) != 1:
        raise AssertionError(f"recent tab is not showing the incoming calls only:{duration_texts}")
    common.wait_for_and_click(device, calls_dict, "recent_filter_button")
    common.wait_for_and_click(device, calls_dict, "recent_tab_filter_outgoing")
    ele = common.wait_for_element(device, calls_dict, "recent_tab_filter_title").text
    if ele != "Outgoing":
        raise AssertionError(f"{device} is not founded expected text in recent tab sort filter title:{ele}")
    duration_text = common.get_all_elements_texts(device, calls_dict, "call_duration")
    duration_texts = list(set([item.split(":")[0] for item in duration_text]))
    if duration_texts[0] != "Outgoing" or len(duration_texts) != 1:
        raise AssertionError(f"recent tab is not showing the outgoing calls only:{duration_text}")
    common.wait_for_and_click(device, calls_dict, "recent_filter_button")
    common.wait_for_and_click(device, calls_dict, "recent_tab_filter_missed")
    ele = common.wait_for_element(device, calls_dict, "recent_tab_filter_title").text
    if ele != "Missed":
        raise AssertionError(f"{device} is not founded expected text in recent tab sort filter title:{ele}")
    duration_text = list(set(common.get_all_elements_texts(device, calls_dict, "call_duration")))
    if duration_text[0] != "Missed call" or len(duration_texts) != 1:
        raise AssertionError(f"recent tab is not showing the missed calls only:{duration_text}")


def set_default_sorting_option_in_recent_tab(device):
    navigate_to_calls_tab(device)
    common.wait_for_element(device, calls_dict, "recent_tab")
    common.wait_for_and_click(device, calls_dict, "recent_filter_button")
    common.wait_for_and_click(device, calls_dict, "recent_tab_filter_all")
    ele = common.wait_for_element(device, calls_dict, "recent_tab_filter_title").text
    if ele != "All":
        raise AssertionError(f"{device} is not founded expected text in recent tab sort filter title:{ele}")
    time.sleep(display_time)
    if not (
        common.is_element_present(device, calls_dict, "call_duration")
        or common.is_element_present(device, calls_dict, "call_participant_name")
    ):
        common.wait_for_and_click(device, calls_dict, "dropdown_icon_in_recent_tab")


def verify_specific_sorting_option_recent_tab(device, option):
    if not option.lower() in ["all", "incoming", "outgoing", "missed"]:
        raise AssertionError(f"Illegal method specified: '{option}'")
    verify_option_names_in_sorting_button(device)
    common.wait_for_and_click(device, calls_dict, "recent_filter_button")
    if option == "all":
        common.wait_for_and_click(device, calls_dict, "recent_tab_filter_all")
        ele = common.wait_for_element(device, calls_dict, "recent_tab_filter_title").text
        if ele != "All":
            raise AssertionError(f"{device} is not founded expected text in recent tab sort filter title:{ele}")
        duration_text = common.get_all_elements_texts(device, calls_dict, "call_duration")
        duration_texts = [item.split(":")[0] for item in duration_text]
        if len(set(duration_texts)) <= 1:
            raise AssertionError(f"recent tab is not showing all the items:{duration_text}")

    elif option == "incoming":
        common.wait_for_and_click(device, calls_dict, "recent_tab_filter_incoming")
        ele = common.wait_for_element(device, calls_dict, "recent_tab_filter_title").text
        if ele != "Incoming":
            raise AssertionError(f"{device} is not founded expected text in recent tab sort filter title:{ele}")
        duration_text = common.get_all_elements_texts(device, calls_dict, "call_duration")
        duration_texts = list(set([item.split(":")[0] for item in duration_text]))
        if duration_texts[0] != "Incoming" or len(duration_texts) != 1:
            raise AssertionError(f"recent tab is not showing the incoming calls only:{duration_texts}")

    elif option == "outgoing":
        common.wait_for_and_click(device, calls_dict, "recent_tab_filter_outgoing")
        ele = common.wait_for_element(device, calls_dict, "recent_tab_filter_title").text
        if ele != "Outgoing":
            raise AssertionError(f"{device} is not founded expected text in recent tab sort filter title:{ele}")
        duration_text = common.get_all_elements_texts(device, calls_dict, "call_duration")
        duration_texts = list(set([item.split(":")[0] for item in duration_text]))
        if duration_texts[0] != "Outgoing" or len(duration_texts) != 1:
            raise AssertionError(f"recent tab is not showing the outgoing calls only:{duration_text}")

    elif option == "missed":
        common.wait_for_and_click(device, calls_dict, "recent_tab_filter_missed")
        ele = common.wait_for_element(device, calls_dict, "recent_tab_filter_title").text
        if ele != "Missed":
            raise AssertionError(f"{device} is not founded expected text in recent tab sort filter title:{ele}")
        duration_text = list(set(common.get_all_elements_texts(device, calls_dict, "call_duration")))
        if duration_text[0] != "Missed call" or len(duration_text) != 1:
            raise AssertionError(f"recent tab is not showing the missed calls only:{duration_text}")


def verify_option_names_in_sorting_button(device):
    common.wait_for_element(device, calls_dict, "recent_tab")
    common.wait_for_and_click(device, calls_dict, "recent_filter_button")
    common.wait_for_element(device, calls_dict, "recent_tab_filter_incoming")
    common.wait_for_element(device, calls_dict, "recent_tab_filter_outgoing")
    common.wait_for_element(device, calls_dict, "recent_tab_filter_missed")
    if common.is_element_present(device, voicemail_dict, "voicemail_tab"):
        raise AssertionError("voicemail button is founded at sorting button")
    # To dismmis sorting button pop-up
    common.wait_for_and_click(device, calls_dict, "recent_tab_filter_all")


def verify_ongoing_call_notification_in_recent_tab(from_device, to_device):
    time.sleep(action_time)
    if not common.click_if_present(from_device, calls_dict, "recent_tab"):
        navigate_to_calls_tab(from_device)
    time.sleep(display_time)
    common.click_if_present(from_device, calls_dict, "Dismiss_location_missing_banner_icon")
    settings_keywords.refresh_calls_main_tab(from_device)
    time.sleep(display_time)
    ongoing_call_title = common.get_all_elements_texts(from_device, calls_dict, "recent_tab_filter_title")
    if "Ongoing" not in ongoing_call_title:
        raise AssertionError(f"{from_device} ongoing call notification not found in recent tab:{ongoing_call_title}")
    common.wait_for_element(from_device, calls_dict, "ongoing_active_call_duration")
    display_name = common.device_displayname(to_device)
    ongoing_call_user_name = common.wait_for_element(from_device, calls_dict, "contact_display_name").text
    if display_name != ongoing_call_user_name:
        raise AssertionError(
            f"{to_device} display name is not founded in recent tab: {display_name},{ongoing_call_user_name}"
        )


def resume_the_call_from_recent_tab_notification(from_device, to_device, option="resume"):
    if not option.lower() in ["resume", "verify"]:
        raise AssertionError(f"Illegal method specified: '{option}'")
    verify_ongoing_call_notification_in_recent_tab(from_device, to_device)
    on_hold_label = (common.wait_for_element(from_device, calls_dict, "ongoing_active_call_duration").text).split(":")
    if "On hold" != on_hold_label[0]:
        raise AssertionError(f"{from_device} hold lable time is not founded : {on_hold_label}")
    if option.lower() == "resume":
        common.wait_for_and_click(from_device, calls_dict, "resume_button_in_recent_tab")
        common.wait_for_element(from_device, calls_dict, "Hang_up_button")
    elif option.lower() == "verify":
        common.wait_for_element(from_device, calls_dict, "resume_button_in_recent_tab")


def verify_call_hold_banner_for_delegates(from_device, to_device):
    to_devices = to_device.split(",")
    display_names = []
    for device in to_devices:
        display_name = common.device_displayname(device)
        display_names.append(display_name)
    print(display_names)
    time.sleep(action_time)
    common.click_if_present(from_device, calls_dict, "Multiple_call_hold_ribbon_dropdown")
    common.wait_for_element(from_device, calls_dict, "Call_bar_resume_btn")
    hold_banner_display_names = common.get_all_elements_texts(from_device, calls_dict, "caller_name_in_hold_banner")
    for display_name_1 in hold_banner_display_names:
        if display_name_1 not in display_names:
            raise AssertionError(
                f"{display_names} not found in call hold banner in {from_device}:{hold_banner_display_names}"
            )


def verify_DID_number_should_not_present_on_dialpad(device):
    if ":" in device:
        device = device.split(":")[0]
    print("device :", device)
    phone_number = common.device_pstndisplay(device)
    tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", phone_number)
    if common.is_element_present(device, tmp_dict, "search_result_item_container", "xpath"):
        raise AssertionError(f"{device}: DID number is displayed")


def enable_or_disable_dismiss_rate_my_call_toggle(device, desired_state):
    navigate_to_user_survey(device)
    dismiss_rate_my_call_toggle = common.wait_for_element(device, device_settings_dict, "dismiss_rate_toggle_btn")
    dismiss_rate_my_call_toggle_status = dismiss_rate_my_call_toggle.get_attribute("checked")
    print(f"dismiss_rate_my_call_toggle_status :{dismiss_rate_my_call_toggle_status}")
    if desired_state == "ON":
        state = "true"
    elif desired_state == "OFF":
        state = "false"
    print(f"{device}: Set dismiss_rate_my_call_toggle to '{desired_state}, state: {state}'")

    if dismiss_rate_my_call_toggle_status == state:
        print(f"{device}: dismiss rate my call toggle status is already '{desired_state}'")
    else:
        common.wait_for_and_click(device, device_settings_dict, "dismiss_rate_toggle_btn")
        dismiss_rate_my_call_toggle = common.wait_for_element(device, device_settings_dict, "dismiss_rate_toggle_btn")
        dismiss_rate_my_call_toggle_status = dismiss_rate_my_call_toggle.get_attribute("checked")
        if state != dismiss_rate_my_call_toggle_status:
            raise AssertionError(
                f"{device}: Unexpected state of dismiss_rate_my_call_toggle :{dismiss_rate_my_call_toggle_status}"
            )


def verify_calls_recent_tab_pill_count(from_device, to_device):
    common.wait_for_element(from_device, calls_dict, "calls_tab")
    common.wait_for_element(from_device, home_screen_dict, "home_screen_calls_pill_count")
    common.wait_for_and_click(from_device, calls_dict, "calls_tab")
    pill_count = common.wait_for_element(from_device, calls_dict, "recent_tab_pill_count").text
    if pill_count != "1":
        raise AssertionError(f"In {from_device} not increased pill count on recent tab. {pill_count}")
    settings_keywords.refresh_calls_main_tab(from_device)
    participant_names = common.get_all_elements_texts(from_device, calls_dict, "call_participant_name")
    missed_call_log = common.get_all_elements_texts(from_device, calls_dict, "call_duration")
    display_name = common.device_displayname(to_device)
    if not ((participant_names[0] == display_name) and (missed_call_log[0] == "Missed call")):
        raise AssertionError(
            f"{from_device} not founded display name of {to_device}.{participant_names},{missed_call_log},{display_name}"
        )


def verify_and_resume_call_for_parked_call_at_recent_tab(park_code, from_device, to_device, option="resume"):
    if option.lower() not in ["resume", "verify"]:
        raise AssertionError(f"Illegal value for 'state': '{option}'")
    verify_ongoing_call_notification_in_recent_tab(from_device, to_device)
    ongoing_call_text = (common.wait_for_element(from_device, calls_dict, "ongoing_active_call_duration").text).split(
        ":"
    )
    ongoing_call_text_1 = ongoing_call_text[1].split(" ")
    if park_code not in ongoing_call_text_1:
        raise AssertionError(f"{from_device} call park code is not founded : {ongoing_call_text_1}")
    common.wait_for_and_click(from_device, calls_dict, "favorites_more_options")
    common.wait_for_element(from_device, calls_dict, "resume_call_at_recent_tab_more")
    common.wait_for_element(from_device, calls_dict, "dismiss_at_recent_tab_more")
    common.wait_for_and_click(from_device, calendar_dict, "touch_outside")
    if option == "verify":
        common.wait_for_element(from_device, calls_dict, "resume_button_in_recent_tab")
    elif option == "resume":
        common.wait_for_and_click(from_device, calls_dict, "resume_button_in_recent_tab")
        common.wait_for_element(from_device, calls_dict, "Hang_up_button")


def verify_resume_button_dismissed_after_2_minutes(device):
    common.wait_for_element(device, calls_dict, "recent_tab")
    time.sleep(display_time)
    common.click_if_present(device, calls_dict, "Dismiss_location_missing_banner_icon")
    settings_keywords.refresh_calls_main_tab(device)
    ongoing_call_title = common.get_all_elements_texts(device, calls_dict, "recent_tab_filter_title")
    if "Ongoing" in ongoing_call_title:
        raise AssertionError(f"{device} ongoing call notification is found in recent tab:{ongoing_call_title}")

    if common.is_element_present(device, calls_dict, "resume_button_in_recent_tab"):
        raise AssertionError(f"{device} after 2 minutes have resume button at recent tab")


def verify_calls_recent_tab(device):
    time.sleep(action_time)
    if not common.is_element_present(device, calls_dict, "recent_tab"):
        navigate_to_calls_tab(device)
    common.wait_for_element(device, calls_dict, "recent_tab")
    common.wait_for_element(device, calls_dict, "favorites_tab")
    common.wait_for_element(device, calls_dict, "search")
    common.wait_for_element(device, calls_dict, "unpark_call")
    if common.is_portrait_mode_cnf_device(device):
        common.wait_for_element(device, calls_dict, "Make_a_call")
    else:
        common.wait_for_element(device, calls_dict, "dial_pad_field")


def verify_option_in_latest_call_details(device):
    common.wait_for_element(device, calls_dict, "call_list_item_call_action")
    common.wait_for_element(device, calls_dict, "call_list_view_profile_action")
    if common.is_element_present(device, calls_dict, "call_list_item_favorites_action"):
        common.wait_for_element(device, calls_dict, "add_user_to_speed_dial")
    else:
        common.wait_for_element(device, calls_dict, "remove_user_from_speed_dial")
        print("User is already added to speed dial")
    dismiss_calls_item_options(device)


def verify_dismiss_option_should_not_present_inside_the_more_info_icon_for_ongoing_call(from_device, to_device):
    common.click_if_present(from_device, calls_dict, "Call_Back_Button")
    time.sleep(action_time)
    if not common.click_if_present(from_device, calls_dict, "recent_tab"):
        navigate_to_calls_tab(from_device)
    time.sleep(display_time)
    common.click_if_present(from_device, calls_dict, "Dismiss_location_missing_banner_icon")
    settings_keywords.refresh_calls_main_tab(from_device)
    ongoing_call_title = common.get_all_elements_texts(from_device, calls_dict, "recent_tab_filter_title")
    if "Ongoing" not in ongoing_call_title:
        raise AssertionError(f"{from_device} ongoing call notification not found in recent tab:{ongoing_call_title}")
    common.wait_for_element(from_device, calls_dict, "ongoing_active_call_duration")
    common.wait_for_and_click(from_device, calls_dict, "favorites_more_options")
    if common.is_element_present(from_device, calls_dict, "dismiss_at_recent_tab_more"):
        raise AssertionError(f"{from_device} is founded dismiss option in ongoing call")
    display_name = common.device_displayname(to_device)
    user_displayname = "Active call: " + display_name
    print(user_displayname)
    temp_dict = common.get_dict_copy(calls_dict, "active_call_user_name", "user_name", user_displayname)
    common.wait_for_element(from_device, temp_dict, "active_call_user_name")
    common.wait_for_and_click(from_device, calendar_dict, "touch_outside")


def calling_from_people_tab_when_speed_dial_is_added_for_cap(from_device, to_device):
    people_keywords.navigate_to_people_tab(from_device)
    user_displayname = common.device_displayname(to_device)
    call_icon_in_people_tab = common.wait_for_element(
        from_device, calls_dict, "call_icon_in_people_tab", cond=EC.presence_of_all_elements_located
    )
    users_in_people_tab = common.get_all_elements_texts(from_device, calls_dict, "user_title")
    max_attempts = len(call_icon_in_people_tab)
    for _attempt in range(max_attempts):
        for call_option, user_name in zip(call_icon_in_people_tab, users_in_people_tab):
            if user_name == user_displayname:
                print(user_name, user_displayname)
                call_option.click()
                time.sleep(display_time)
                common.wait_for_element(from_device, calls_dict, "Hang_up_button")
                return

            else:
                if _attempt == max_attempts - 1:
                    raise AssertionError(f"{from_device}: Could not found {user_displayname} in {users_in_people_tab}'")


def reject_incoming_call_when_already_in_call(device_list):
    for device_name in device_list.split(","):
        print(f"{device_name}: Rejecting incoming call")
        common.wait_for_and_click(device_name, calls_dict, "Hang_up_button")
        common.click_if_present(device_name, calls_dict, "Close_Call_Rating")
        common.click_if_present(device_name, tr_calls_dict, "call_rating_dismiss")
        common.sleep_with_msg(device_name, 5, "sleep until Call_Rating appear")


def dial_and_clear_invalid_number_for_cap(device):
    driver = obj.device_store.get(alias=device)
    if config["devices"][device]["model"].lower() in ["riverside", "riverside_13"]:
        print(f"{device}: Doesn't support Dail Pad")
        return
    common.wait_for_element(device, calls_dict, "dial_pad_field")
    common.wait_for_element(device, calls_dict, "call_icon1")
    common.sleep_with_msg(device, action_time, "Allow Dial Pad to be Interactive")
    common.wait_for_and_click(device, calls_dict, "nine")
    common.wait_for_and_click(device, calls_dict, "eight")
    common.wait_for_and_click(device, calls_dict, "seven")
    common.wait_for_and_click(device, calls_dict, "six")
    common.wait_for_and_click(device, calls_dict, "five")
    common.wait_for_and_click(device, calls_dict, "four")
    common.wait_for_and_click(device, calls_dict, "three")
    common.wait_for_and_click(device, calls_dict, "two")
    common.wait_for_and_click(device, calls_dict, "one")
    common.wait_for_and_click(device, calls_dict, "zero")
    elem = common.wait_for_element(device, calls_dict, "zero")
    actions = TouchAction(driver)
    actions.long_press(elem, duration=1000).release().perform()
    typed_phone_number = common.wait_for_element(device, calls_dict, "entered_phn_num").text
    print("Entered phone number : ", typed_phone_number)
    expected = "9876543210+"
    if not expected == typed_phone_number:
        raise AssertionError(f"Typed phone number mismatch: Expected: '{expected}', actual: '{typed_phone_number}'")
    text = common.wait_for_element(device, calls_dict, "dial_pad_field")
    text.clear()
    time.sleep(display_time)


def Verify_the_functionality_of_the_dropdown_icon_beside_all_options_under_the_recent_tab(device):
    common.wait_for_and_click(device, calls_dict, "recent_tab")
    common.wait_for_element(device, calls_dict, "call_duration")
    common.wait_for_and_click(device, calls_dict, "dropdown_icon_in_recent_tab")
    time.sleep(action_time)
    if common.is_element_present(device, calls_dict, "call_participant_name") or common.is_element_present(
        device, calls_dict, "call_duration"
    ):
        raise AssertionError(f"{device} after click on dropdown icon beside all options still logs is appear")
    common.wait_for_and_click(device, calls_dict, "dropdown_icon_in_recent_tab")
    common.wait_for_element(device, calls_dict, "call_participant_name")
    common.wait_for_element(device, calls_dict, "call_duration")


def resume_the_call_from_recent_tab_notification_in_more_option(from_device, to_device):
    verify_ongoing_call_notification_in_recent_tab(from_device, to_device)
    on_hold_label = (common.wait_for_element(from_device, calls_dict, "ongoing_active_call_duration").text).split(":")
    if "On hold" != on_hold_label[0]:
        raise AssertionError(f"{from_device} hold lable time is not founded : {on_hold_label}")
    common.wait_for_element(from_device, calls_dict, "resume_button_in_recent_tab")
    common.wait_for_and_click(from_device, calls_dict, "favorites_more_options")
    common.wait_for_and_click(from_device, calls_dict, "resume_call_at_recent_tab_more")
    common.wait_for_element(from_device, calls_dict, "Hang_up_button")


def verify_calls_favorites_tab(device):
    time.sleep(action_time)
    if not common.is_element_present(device, calls_dict, "recent_tab"):
        navigate_to_calls_tab(device)
    common.wait_for_and_click(device, calls_dict, "favorites_tab")
    common.wait_for_element(device, calls_dict, "recent_tab")
    common.wait_for_element(device, calls_dict, "speed_dial")
    common.wait_for_element(device, calls_dict, "your_delegates")
    common.wait_for_element(device, calls_dict, "search")
    common.wait_for_element(device, calls_dict, "unpark_call")
    if common.is_portrait_mode_cnf_device(device):
        common.wait_for_element(device, calls_dict, "Make_a_call")
    else:
        common.wait_for_element(device, calls_dict, "dial_pad_field")


def dismiss_multiple_call_park_banner(device):
    common.click_if_present(device, calls_dict, "Hang_up_button")
    time.sleep(action_time)
    for attampt in range(3):
        if common.click_if_present(device, calls_dict, "Multiple_call_hold_ribbon_dropdown"):
            time.sleep(action_time)
            common.click_if_present(device, calls_dict, "parked_call_dismiss_button")
        else:
            common.click_if_present(device, calls_dict, "parked_call_dismiss_button")


def verify_ring_back_to_retrieve_the_parked_call(device):
    common.wait_for_element(device, calls_dict, "Accept_call_button", wait_attempts=80)


def verify_Voice_quality_recording_option_under_callings_settings(device):
    settings_keywords.open_settings_page(device)
    time.sleep(display_time)
    if not common.click_if_present(device, settings_dict, "Calling"):
        common.wait_for_and_click(device, settings_dict, "Device_Settings")
        device_settings_keywords.advance_calling_option_oem(device)
    common.wait_for_element(device, calls_dict, "Header", "id")
    for i in range(5):
        time.sleep(2)
        if common.is_element_present(device, calls_dict, "enable_voice_quality_recording_toggle"):
            break
        calendar_keywords.scroll_only_once(device)

    common.wait_for_element(device, calls_dict, "voice_quality_recording")


def verify_emergency_location_option_under_callings_settings(device):
    settings_keywords.open_settings_page(device)
    time.sleep(display_time)
    if not common.click_if_present(device, settings_dict, "Calling"):
        common.wait_for_and_click(device, settings_dict, "Device_Settings")
        device_settings_keywords.advance_calling_option_oem(device)
    common.wait_for_element(device, calls_dict, "Header", "id")
    for i in range(5):
        time.sleep(2)
        if common.is_element_present(device, settings_dict, "set_your_emergency_location"):
            break
        calendar_keywords.scroll_only_once(device)
    common.wait_for_element(device, settings_dict, "set_your_emergency_location")


def enable_or_disable_Voice_quality_recording_option(device, desired_state):
    voice_quality_recording_toggle = common.wait_for_element(
        device, calls_dict, "enable_voice_quality_recording_toggle"
    )
    voice_quality_recording_toggle_status = voice_quality_recording_toggle.get_attribute("checked")
    print(f"voice quality recording toggle status :{voice_quality_recording_toggle_status}")
    if desired_state.lower() == "on":
        state = "true"
    elif desired_state.lower() == "off":
        state = "false"
    print(f"{device}: Set show_meeting_name toggle to '{desired_state}, state: {state}'")

    if voice_quality_recording_toggle_status == state:
        print(f"{device}: Show voice quality recording toggle is already '{desired_state}'")
    else:
        common.wait_for_and_click(device, calls_dict, "enable_voice_quality_recording_toggle")
        voice_quality_recording_toggle = common.wait_for_element(
            device, calls_dict, "enable_voice_quality_recording_toggle"
        )
        voice_quality_recording_toggle_status = voice_quality_recording_toggle.get_attribute("checked")
        if state != voice_quality_recording_toggle_status:
            raise AssertionError(
                f"{device}: Unexpected state of  Voice quality recording toggle: '{voice_quality_recording_toggle_status}'"
            )


def verify_toggle_status_for_Voice_quality_is_disabled(device):
    voice_quality_recording_toggle = common.wait_for_element(
        device, calls_dict, "enable_voice_quality_recording_toggle"
    )
    voice_quality_recording_toggle_status = voice_quality_recording_toggle.get_attribute("checked")
    if voice_quality_recording_toggle_status != "false":
        raise AssertionError(
            f"Illegal state for voice quality recording toggle status: '{voice_quality_recording_toggle_status}'"
        )


def navigate_to_dial_pad_tab_for_cap(device):
    time.sleep(3)
    if not common.is_element_present(device, calls_dict, "backspace"):
        common.wait_for_and_click(device, calls_dict, "dialpad_tab")
        common.wait_for_element(device, calls_dict, "call")


def navigate_to_dial_pad_tab_for_conf(device):
    common.wait_for_and_click(device, calendar_dict, "calendar_tab")
    common.wait_for_and_click(device, calls_dict, "Make_a_call")


def verify_call_transfer_option_is_disabled_when_first_transferred_call_is_rejected(device):
    common.click_if_present(device, calls_dict, "caller_name_in_hold_banner")
    ele = common.wait_for_element(device, calls_dict, "Transfer", "id")
    tmp = ele.get_attribute("enabled")
    print(tmp)
    if tmp != "false":
        raise AssertionError(f"{device}: Transfer option is still enabled")


def verify_work_voicemail_option_in_call_transfer(from_device, to_device, method):
    if method.lower() not in ["display_name", "phone_number"]:
        raise AssertionError(f"Illegal method specified: '{method}'")
    common.wait_for_element(from_device, calls_dict, "Hang_up_button")
    if not common.click_if_present(from_device, calls_dict, "Transfer"):
        common.wait_for_and_click(from_device, calls_dict, "call_more_options")
        common.wait_for_and_click(from_device, calls_dict, "Transfer")
    common.wait_for_and_click(from_device, calls_dict, "Transfer_now")
    disp_name = common.device_displayname(to_device)
    phone_number = common.device_pstndisplay(to_device)
    if method.lower() == "display_name":
        elem = common.wait_for_element(from_device, calls_dict, "search_contact_box")
        elem.send_keys(disp_name)
    elif method.lower() == "phone_number":
        elem = common.wait_for_element(from_device, calls_dict, "search_contact_box")
        elem.send_keys(phone_number)
    common.wait_for_element(from_device, calls_dict, "search_result_name")
    common.wait_for_and_click(from_device, calls_dict, "overflow_menu")
    common.wait_for_element(from_device, calls_dict, "work_voicemail")
    settings_keywords.click_device_center_point(from_device)


def dismiss_the_popup_screen(device):
    common.tap_outside_the_popup(device, common.wait_for_element(device, calls_dict, "pop_up_container"))


def verify_and_click_in_call_park_banner(from_device, to_device):
    verify_call_park_banner(from_device, to_device)
    common.wait_for_and_click(from_device, calls_dict, "caller_name_in_hold_banner")
    user_displayname = common.device_displayname(to_device)
    temp_dict = common.get_dict_copy(calls_dict, "active_call_user_name", "user_name", user_displayname)
    common.wait_for_element(from_device, temp_dict, "active_call_user_name")


def verify_call_UI_when_e2ee_is_enabled(device):
    devices = device.split(",")
    for device in devices:
        common.wait_for_element(device, calls_dict, "Hang_up_button")
        common.wait_for_element(device, calls_dict, "call_mute_control")
        common.wait_for_element(device, calls_dict, "Put_call_on_hold")
        common.wait_for_and_click(device, calls_dict, "call_more_options")
        common.wait_for_element(device, calls_dict, "switch_audio_route", "command")
        dismiss_call_more_options(device)


def verify_search_option_not_present_in_add_participant_when_e2ee_enabled(device):
    devices = device.split(",")
    for device in devices:
        common.wait_for_element(device, calls_dict, "Hang_up_button")
        time.sleep(3)
        if not common.click_if_present(device, calls_dict, "participants_roster_button"):
            if not common.click_if_present(device, calls_dict, "Add_participants_button"):
                common.wait_for_and_click(device, calls_dict, "showRoster")
        time.sleep(display_time)
        if common.is_element_present(device, calls_dict, "add_people_to_meeting"):
            raise AssertionError(f"{device}: Search option is still visible")
        common.wait_for_and_click(device, calls_dict, "Call_Back_Button")


def verify_E2EE_icon_is_not_displaying_in_call_UI(device):
    devices = device.split(",")
    for device in devices:
        time.sleep(display_time)
        if common.is_element_present(device, device_settings_dict, "e2ee_icon"):
            raise AssertionError(f"{device}: E2EE icon is visible")


def verify_E2EE_security_code_on_user(device_list):
    devices = device_list.split(",")
    security_code = []
    for device in devices:
        common.wait_for_element(device, calls_dict, "Hang_up_button")
        common.wait_for_and_click(device, device_settings_dict, "e2ee_icon")
        common.wait_for_element(device, calls_dict, "e2ee_code_security_code_title")
        security_code_01 = common.get_all_elements_texts(device, calls_dict, "e2ee_security_code")
        security_code.append(security_code_01)
        dismiss_call_more_options(device)
        print(security_code)
    if security_code[0] != security_code[1]:
        raise AssertionError(f"security code is not matching: {security_code}")


def verify_multiple_incoming_group_call_notification(device):
    common.wait_for_element(device, calls_dict, "Multiple_call_hold_ribbon")
    common.wait_for_and_click(device, calls_dict, "Multiple_call_hold_ribbon_dropdown")
    common.wait_for_element(device, calls_dict, "Notification_group_call_answer_button")
    common.wait_for_element(device, calls_dict, "Notification_ignore_call_button")
    common.tap_outside_the_popup(device, common.wait_for_element(device, calls_dict, "multiple_call_pop_up_container"))
    time.sleep(display_time)
    if common.is_element_present(device, calls_dict, "Notification_group_call_answer_button"):
        raise AssertionError("Answer button is still present after clicking on dropdown button")


def verify_unpark_call_icon(device):
    common.wait_for_element(device, calls_dict, "unpark_call")


def verif_dialpad_in_call_more_option(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    common.wait_for_and_click(device, calls_dict, "call_more_options")
    common.wait_for_and_click(device, calls_dict, "call_dial_pad")
    common.wait_for_element(device, calls_dict, "phone_number_with_backspace")
    common.wait_for_element(device, calls_dict, "dial_pad_field")
    settings_keywords.get_screenshot("dark theme enabled", device_list=device)
    common.wait_for_and_click(device, calls_dict, "call_dialpad_close_btn")
    common.wait_for_element(device, calls_dict, "Hang_up_button")


def verify_call_transfer_option_is_disabled(device):
    ele = common.wait_for_element(device, calls_dict, "Transfer", "id")
    tmp = ele.get_attribute("enabled")
    print(tmp)
    if tmp.lower() == "true":
        raise AssertionError(f"{device}: Transfer option is still enabled")


def verify_default_setting_under_call_forwarding_section(device, status):
    common.verify_toggle_button(device, settings_dict, "Call_forward_toggle", desired_state=status)
    common.wait_for_element(device, lcp_calls_dict, "also_ring_off")
    common.wait_for_and_click(device, calls_dict, "when_in_another_call")
    common.wait_for_element(device, calls_dict, "play_a_busy_signal")
    common.wait_for_element(device, calls_dict, "new_calls_ring_me")
    common.wait_for_element(device, calls_dict, "redirect_unanswered_call")
    common.wait_for_and_click(device, app_bar_dict, "back")


def verify_when_in_another_call_option_inside_calling(device):
    common.wait_for_element(device, settings_dict, "Calling")
    common.wait_for_element(device, calls_dict, "when_in_another_call")


def verify_default_status_for_when_in_another_call_option(device):
    common.wait_for_element(device, calls_dict, "when_in_another_call")
    common.wait_for_element(device, calls_dict, "play_a_busy_signal")


def select_the_options_inside_when_in_another_call_option(device, option):
    if option.lower() not in ["play_a_busy_signal", "new_calls_ring_me", "redirect_unanswered_call"]:
        raise AssertionError(f"Illegal value for 'status': '{option}'")

    if not common.is_element_present(device, settings_dict, "Calling"):
        settings_keywords.open_settings_page(device)
        time.sleep(display_time)
        if not common.click_if_present(device, settings_dict, "Calling"):
            common.wait_for_and_click(device, settings_dict, "Device_Settings")
            device_settings_keywords.advance_calling_option_oem(device)

    common.wait_for_element(device, settings_dict, "call_forwarding")
    common.wait_for_and_click(device, calls_dict, "when_in_another_call")

    if option.lower() == "play_a_busy_signal":
        common.wait_for_and_click(device, calls_dict, "play_a_busy_signal")

    elif option.lower() == "new_calls_ring_me":
        common.wait_for_and_click(device, calls_dict, "new_calls_ring_me")

    elif option.lower() == "redirect_unanswered_call":
        common.wait_for_and_click(device, calls_dict, "redirect_unanswered_call")

    common.wait_for_and_click(device, app_bar_dict, "back")

    verify_the_status_of_when_in_another_call_option(device, option)


def verify_the_status_of_when_in_another_call_option(device, option):
    if option.lower() not in ["play_a_busy_signal", "new_calls_ring_me", "redirect_unanswered_call"]:
        raise AssertionError(f"Illegal value for 'status': '{option}'")

    common.wait_for_element(device, settings_dict, "call_forwarding")

    if option.lower() == "play_a_busy_signal":
        common.wait_for_element(device, calls_dict, "play_a_busy_signal")

    elif option.lower() == "new_calls_ring_me":
        common.wait_for_element(device, calls_dict, "new_calls_ring_me")

    elif option.lower() == "redirect_unanswered_call":
        common.wait_for_element(device, calls_dict, "redirect_unanswered_call")


def verify_call_as_myself_drop_down_button(device):
    if common.is_portrait_mode_cnf_device(device):
        common.wait_for_and_click(device, calls_dict, "dialpad_tab")
        common.wait_for_element(device, calls_dict, "call_as_myself_history_button")

    common.wait_for_element(device, calls_dict, "call_as_myself_arrow")


def verify_option_in_call_as_myself_drop_down_button(device, to_device):
    verify_call_as_myself_drop_down_button(device)
    display_name = common.device_displayname(to_device)
    user_display = "Call as " + display_name
    temp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", user_display)
    common.wait_for_and_click(device, calls_dict, "call_as_myself_arrow")
    common.wait_for_element(device, calls_dict, "call_as_myself")
    common.wait_for_element(device, temp_dict, "search_result_item_container", "xpath")
    common.tap_outside_the_popup(device, common.wait_for_element(device, calls_dict, "call_as_myself_bottom_pop_up"))


def verify_and_set_dialpad_option_for_portrait_device(device):
    if common.is_portrait_mode_cnf_device(device):
        call_views_keywords.verify_call_views_option_under_callings_settings(device)
        call_views_keywords.select_default_view(device, option="dialpad")


def verify_call_as_boss_name_option_not_appear_when_permission_to_make_a_calls_is_disabled(device, to_device):
    verify_call_as_myself_drop_down_button(device)
    display_name = common.device_displayname(to_device)
    common.wait_for_and_click(device, calls_dict, "call_as_myself_arrow")
    user_display = "Call as " + display_name
    temp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", user_display)
    common.wait_for_element(device, calls_dict, "call_as_myself")
    if common.is_element_present(device, temp_dict, "search_result_item_container", "xpath"):
        raise AssertionError(
            f"{to_device} after disabled make a calls permission still we can able to see 'call as {display_name}' in {device}"
        )
    common.tap_outside_the_popup(device, common.wait_for_element(device, calls_dict, "call_as_myself_bottom_pop_up"))


def verify_call_as_myself_option_should_not_appear_when_permission_to_make_a_calls_is_disabled_by_all_boss(device):
    common.wait_for_element(device, calls_dict, "recent_tab")
    if common.is_portrait_mode_cnf_device(device):
        common.wait_for_and_click(device, calls_dict, "dialpad_tab")
        common.wait_for_element(device, calls_dict, "call_as_myself_history_button")
    common.wait_for_element(device, calls_dict, "call_as_myself")
    if common.is_element_present(device, calls_dict, "call_as_myself_arrow"):
        raise AssertionError(
            f"After disabled make a calls permission still we can able to see 'call as myself' drop down in {device}"
        )


def navigate_to_shared_line_option_from_history_button(device, to_device):
    verify_call_as_myself_drop_down_button(device)
    if common.is_portrait_mode_cnf_device(device):
        common.wait_for_and_click(device, calls_dict, "call_as_myself_history_button")
    else:
        common.wait_for_and_click(device, calls_dict, "favorites_tab")

    display_name = common.device_displayname(to_device)

    temp_dict = common.get_dict_copy(calls_dict, "favorites_more_options", "user_name", display_name)
    common.wait_for_and_click(device, temp_dict, "favorites_more_options", "xpath")

    common.wait_for_and_click(device, calls_dict, "view_shared_line")
    common.wait_for_element(device, calls_dict, "delegates")


def select_option_inside_call_as_myself_dropdown(device, to_device):
    common.wait_for_element(device, calls_dict, "recent_tab")
    common.wait_for_and_click(device, calls_dict, "call_as_myself_arrow")
    if to_device == "my_self":
        common.wait_for_and_click(device, calls_dict, "call_as_myself")
    else:
        display_name = common.device_displayname(to_device)
        user_display = "Call as " + display_name
        temp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", user_display)
        common.wait_for_and_click(device, temp_dict, "search_result_item_container", "xpath")

    common.wait_for_element(device, calls_dict, "recent_tab")
    if to_device == "my_self":
        common.wait_for_and_click(device, calls_dict, "call_as_myself")
    else:
        common.wait_for_element(device, temp_dict, "search_result_item_container", "xpath")


def verify_text_on_call_as_myself_button(device, to_device):
    common.wait_for_element(device, calls_dict, "call_as_myself_arrow")
    if to_device == "my_self":
        common.wait_for_element(device, calls_dict, "call_as_myself")
    else:
        display_name = common.device_displayname(to_device)
        user_display = "Call as " + display_name
        temp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", user_display)
        common.wait_for_element(device, temp_dict, "search_result_item_container", "xpath")


def verify_call_as_myself_option_should_not_appear_when_no_boss(device):
    if common.is_element_present(device, calls_dict, "call_as_myself_arrow") or common.is_element_present(
        device, calls_dict, "call_as_myself"
    ):
        raise AssertionError(
            f"After disabled make a calls permission still we can able to see 'call as myself' drop down in {device}"
        )


def verify_and_change_boss_in_shared_lines(device, from_device, to_device):
    if common.is_portrait_mode_cnf_device(device):
        if common.is_element_present(device, calls_dict, "dialpad_tab"):
            common.wait_for_and_click(device, calls_dict, "Call_Back_Button")
    common.wait_for_and_click(device, calls_dict, "delegates")
    from_device_display_name = common.device_displayname(from_device)
    temp_dict = common.get_dict_copy(
        calls_dict, "search_result_item_container", "config_display", from_device_display_name
    )
    common.wait_for_and_click(device, temp_dict, "search_result_item_container", "xpath")
    to_device_display_name = common.device_displayname(to_device)
    temp_dict = common.get_dict_copy(
        calls_dict, "search_result_item_container", "config_display", to_device_display_name
    )
    common.wait_for_and_click(device, temp_dict, "search_result_item_container", "xpath")
    common.wait_for_element(device, calls_dict, "delegates")
    common.wait_for_element(device, temp_dict, "search_result_item_container", "xpath")


def verify_busy_on_busy_error_message_while_already_in_call(device, to_device):
    if common.is_lcp(device):
        common.wait_for_and_click(device, calls_dict, "search_icon")
    else:
        common.wait_for_and_click(device, calls_dict, "search")
    displayname = common.device_displayname(to_device)
    print(f"diaplay name: {displayname}")
    common.wait_for_element(device, calls_dict, "search_text").send_keys(displayname)
    common.hide_keyboard(device)
    tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", displayname)
    common.wait_for_and_click(device, tmp_dict, "search_result_item_container", "xpath")
    if common.is_lcp(device):
        if common.is_lcp(device):
            settings_keywords.swipe_till_end(device)
            # settings_keywords.swipe_till_end(from_device)
            # settings_keywords.swipe_till_end(from_device)
    common.wait_for_and_click(device, calls_dict, "Make_an_audio_call")
    common.wait_for_element(device, calls_dict, "call_busy_text")
    common.wait_while_present(device, calls_dict, "call_busy_text", max_wait_attempts=5)


def verify_and_move_incoming_call_to_notification_redirect_to_voicemail(from_device, to_device):
    common.wait_for_element(from_device, calls_dict, "Accept_call_button")
    common.wait_for_and_click(from_device, calls_dict, "hold_label_time")
    common.wait_for_and_click(from_device, calls_dict, "Multiple_call_hold_ribbon_dropdown")
    displayname = common.device_displayname(to_device)
    temp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", displayname)
    common.wait_for_element(from_device, temp_dict, "search_result_item_container", "xpath")
    common.wait_for_and_click(from_device, calls_dict, "Notification_redirect_voicemail_button")
    common.wait_for_element(to_device, calls_dict, "Hang_up_button")
    common.wait_for_element(to_device, calls_dict, "ongoing_active_call_duration")


def verify_group_incoming_call_notification_should_not_contains_redirect_to_voicemail(device, from_device, to_device):
    common.wait_for_element(device, calls_dict, "Reject_notification_call_btn")
    common.wait_for_element(device, calls_dict, "Notification_group_call_answer_button")

    device_name = common.device_displayname(to_device)
    displayname = "Call for " + device_name
    temp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", displayname)
    common.wait_for_element(device, temp_dict, "search_result_item_container", "xpath")

    device_name = common.device_displayname(from_device)
    displayname = device_name + " is calling"
    temp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", displayname)
    common.wait_for_element(device, temp_dict, "search_result_item_container", "xpath")

    common.wait_while_present(device, calls_dict, "Notification_redirect_voicemail_button")


def validate_search_results_and_send_voicemail_in_multiple_tabs(from_device, to_device):
    common.wait_for_and_click(from_device, calls_dict, "search")
    displayname = common.device_displayname(to_device)
    common.wait_for_element(from_device, calls_dict, "search_text").send_keys(displayname)
    common.hide_keyboard(from_device)
    tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", displayname)
    common.wait_for_and_click(from_device, tmp_dict, "search_result_item_container", "xpath")
    common.wait_for_element(from_device, tmp_dict, "search_result_item_container", "xpath")
    common.wait_for_element(from_device, calls_dict, "Make_an_audio_call")
    common.wait_for_and_click(from_device, calls_dict, "Make_a_call_to_voicemail")
    common.wait_for_element(from_device, voicemail_dict, "voicemail_tab")
    common.wait_for_element(from_device, calls_dict, "Hang_up_button")


def verify_privateline_label_on_call_screen(device):
    common.wait_for_element(device, calls_dict, "private_line")


def verify_privateline_on_recent_tab(device):
    common.wait_for_element(device, calls_dict, "privateline_user")


def click_and_verify_dial_pad_from_call_control_UI(device_list):
    devices = device_list.split(",")
    for device in devices:
        common.wait_for_element(device, calls_dict, "Hang_up_button")
        common.wait_for_and_click(device, calls_dict, "call_more_options")
        common.wait_for_and_click(device, calls_dict, "call_dialpad_under_more")
        if common.is_hard_dial_pad_present(device):
            common.wait_for_element(device, calls_dict, "use_hard_keys_to_dial_a_number")
        else:
            common.wait_for_element(device, calls_dict, "dial_pad1")
        common.wait_for_element(device, calls_dict, "backspace")
        common.wait_for_element(device, calls_dict, "phone_number")
        common.wait_for_element(device, calls_dict, "participants_roster_button")
        common.wait_for_and_click(device, calls_dict, "call_dialpad_close_btn")


def verify_dial_pad_UI_for_CAP(device):
    if common.is_portrait_mode_cnf_device(device):
        common.wait_for_and_click(device, calls_dict, "people_tab")
        common.wait_for_element(device, calls_dict, "search")
        common.wait_for_and_click(device, calls_dict, "dialpad_tab")
    if common.is_hard_dial_pad_present(device):
        common.wait_for_element(device, calls_dict, "use_hard_keys_to_dial_a_number")
        common.wait_for_element(device, calls_dict, "search")
    else:
        common.wait_for_element(device, calls_dict, "soft_dial_pad")
    common.wait_for_element(device, calls_dict, "call_park")
    common.wait_for_element(device, calls_dict, "call_as_myself")
    common.wait_for_element(device, calls_dict, "backspace")
    common.wait_for_element(device, calls_dict, "phone_number")


def verify_dial_pad_UI_for_CONF(device):
    navigate_to_dial_pad_tab_for_conf(device)
    common.wait_for_and_click(device, calls_dict, "people_tab")
    common.wait_for_element(device, calls_dict, "search")
    common.wait_for_and_click(device, calls_dict, "dialpad_tab")
    common.wait_for_element(device, calls_dict, "call_park")
    common.wait_for_element(device, calls_dict, "backspace")
    common.wait_for_element(device, calls_dict, "phone_number")
    common.wait_for_element(device, calls_dict, "call_icon1")
    common.wait_for_element(device, calls_dict, "call_as_myself_history_button")
    if common.is_hard_dial_pad_present(device):
        common.wait_for_element(device, calls_dict, "use_hard_keys_to_dial_a_number")
    else:
        common.wait_for_element(device, calls_dict, "soft_dial_pad")
    common.click_if_present(device, calls_dict, "Call_Back_Button")
    common.click_if_present(device, home_screen_dict, "home_bar_icon")


def wait_until_call_disconnected(device):
    common.wait_while_present(device, calls_dict, "Accept_call_button", max_wait_attempts=50)


def verify_options_when_click_on_transfer_btn_in_call_UI(device):
    common.wait_for_and_click(device, calls_dict, "Transfer")
    common.wait_for_element(device, calls_dict, "Transfer_now")
    common.wait_for_element(device, calls_dict, "consult_first")
    dismiss_call_more_options(device)


def transfer_call_using_dial_pad(from_device, to_device, option):
    if option.lower() not in ["transfer_now", "consult_first"]:
        raise AssertionError(f"{from_device}: Unexpected value for Transfer option: {option}")
    to_device_phonenumber = common.device_phonenumber(to_device)
    print(to_device_phonenumber)
    common.wait_for_element(from_device, calls_dict, "Hang_up_button")
    common.wait_for_and_click(from_device, calls_dict, "Transfer")
    if option.lower() == "transfer_now":
        common.wait_for_and_click(from_device, calls_dict, "Transfer_now")
    elif option.lower() == "consult_first":
        common.wait_for_and_click(from_device, calls_dict, "consult_first")
    common.wait_for_and_click(from_device, calls_dict, "dial_pad1", "xpath")
    common.wait_for_element(from_device, calls_dict, "call_icon1")
    common.wait_for_element(from_device, calls_dict, "backspace")
    ele = common.wait_for_element(from_device, calls_dict, "phone_number")
    ele.send_keys(to_device_phonenumber)
    if common.is_element_present(from_device, calls_dict, "call_icon1"):
        common.wait_for_and_click(from_device, calls_dict, "call_icon1")
    else:
        common.wait_for_element(from_device, calls_dict, "Hang_up_button")


def verify_call_transfer_UI_when_in_call(from_device, to_device, speed_dial_user, option):
    if option.lower() not in ["transfer_now", "consult_first"]:
        raise AssertionError(f"{from_device}: Unexpected value for Transfer option: {option}")
    common.wait_for_element(from_device, calls_dict, "Hang_up_button")
    common.wait_for_and_click(from_device, calls_dict, "Transfer")
    to_device_displayname = common.device_displayname(to_device)
    tmp_dict = common.get_dict_copy(calls_dict, "call_participant_name", "config_display", to_device_displayname)
    if option.lower() == "transfer_now":
        common.wait_for_and_click(from_device, calls_dict, "Transfer_now")
        common.wait_for_element(from_device, calls_dict, "transfer_to")
    elif option.lower() == "consult_first":
        common.wait_for_and_click(from_device, calls_dict, "consult_first")
        common.wait_for_element(from_device, calls_dict, "consult")
    common.wait_for_element(from_device, tmp_dict, "call_participant_name", selector_key="xpath")
    common.wait_for_element(from_device, calls_dict, "search_contact_box")
    common.wait_for_element(from_device, calls_dict, "hold_label_time")
    common.wait_for_element(from_device, calls_dict, "dial_pad1", "xpath")
    actual_speed_dial_user = common.get_all_elements_texts(from_device, calls_dict, "contact_display_name")
    expected_speed_dial_user = common.device_displayname(speed_dial_user)
    if expected_speed_dial_user not in actual_speed_dial_user:
        raise AssertionError(
            f"{from_device}: Expected Speed Dial user {speed_dial_user} is not matching with actual speed dial:{actual_speed_dial_user}"
        )
    common.wait_for_and_click(from_device, calls_dict, "Call_Back_Button")


def click_and_verify_dial_pad_in_call_transfer(device, option):
    if option.lower() not in ["transfer_now", "consult_first"]:
        raise AssertionError(f"{device}: Unexpected value for Transfer option: {option}")
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    common.wait_for_and_click(device, calls_dict, "Transfer")
    if option.lower() == "transfer_now":
        common.wait_for_and_click(device, calls_dict, "Transfer_now")
        common.wait_for_element(device, calls_dict, "transfer_to")
    elif option.lower() == "consult_first":
        common.wait_for_and_click(device, calls_dict, "consult_first")
        common.wait_for_element(device, calls_dict, "consult")
    common.wait_for_and_click(device, calls_dict, "dial_pad1")
    common.wait_for_element(device, calls_dict, "dial_pad1", "id")
    common.wait_for_element(device, calls_dict, "backspace")
    common.wait_for_element(device, calls_dict, "call_icon1")
    common.wait_for_and_click(device, calls_dict, "close_btn")


def transfer_call_using_speed_dial_from_call_transfer_ui(device, speed_dial_user, transfer_option, obo_option=None):
    if transfer_option.lower() not in ["transfer_now", "consult_first"]:
        raise AssertionError(f"{device}: Unexpected value for Transfer option: {transfer_option}")
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    common.wait_for_and_click(device, calls_dict, "Transfer")
    speed_dial_disp_name = common.device_displayname(speed_dial_user)
    if transfer_option.lower() == "transfer_now":
        common.wait_for_and_click(device, calls_dict, "Transfer_now")
        common.wait_for_element(device, calls_dict, "transfer_to")
    elif transfer_option.lower() == "consult_first":
        common.wait_for_and_click(device, calls_dict, "consult_first")
        common.wait_for_element(device, calls_dict, "consult")
    common.wait_for_element(device, calls_dict, "dial_pad1")
    tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", speed_dial_disp_name)
    common.wait_for_and_click(device, tmp_dict, "search_result_item_container", "xpath")
    if obo_option:
        choose_call_behalf_of(device, obo_option)
    else:
        # It is possible some cleanup did not happen - detect unexpected OBO:
        if common.click_if_present(device, calls_dict, "myself_xpath"):
            print(f"*WARN*:: {device}: Found and used unexpected 'myself' OBO")
    common.wait_for_element(device, calls_dict, "Hang_up_button")


def place_a_call_from_search_results_page(from_device, to_device):
    display_name = common.device_displayname(to_device)
    temp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", display_name)
    common.wait_for_element(from_device, temp_dict, "search_result_item_container")
    common.wait_for_element(from_device, calls_dict, "Make_a_call_to_voicemail")
    common.wait_for_and_click(from_device, calls_dict, "Make_an_audio_call")
