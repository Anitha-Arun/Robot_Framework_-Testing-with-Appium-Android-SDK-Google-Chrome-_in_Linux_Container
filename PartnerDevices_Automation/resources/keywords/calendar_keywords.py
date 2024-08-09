from appium.webdriver.common.mobileby import MobileBy
import app_bar_keywords
import people_keywords
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
from urllib3.exceptions import ProtocolError
from initiate_driver import obj_dev as obj
from initiate_driver import config
import call_keywords
import settings_keywords
import tr_calendar_keywords
import tr_call_keywords
import re
import time
import subprocess
import common
import threading
import logging
import home_screen_keywords
from Libraries.Selectors import load_json_file
import tr_console_settings_keywords
from datetime import datetime, timedelta
from collections import Counter

display_time = 5
action_time = 2
refresh_time = 10

calendar_dict = load_json_file("resources/Page_objects/Calendar.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")
navigation_dict = load_json_file("resources/Page_objects/Navigation.json")
device_settings_dict = load_json_file("resources/Page_objects/Device_settings.json")
calls_dict = load_json_file("resources/Page_objects/Calls.json")
common_dict = load_json_file("resources/Page_objects/Common.json")
tr_calendar_dict = load_json_file("resources/Page_objects/tr_calendar.json")
tr_calls_dict = load_json_file("resources/Page_objects/tr_calls.json")
homescreen_dict = load_json_file("resources/Page_objects/Home_screen.json")
app_bar_dict = load_json_file("resources/Page_objects/App_bar.json")
home_screen_dict = load_json_file("resources/Page_objects/Home_screen.json")
panels_home_screen_dict = load_json_file("resources/Page_objects/panels_homescreen.json")
people_dict = load_json_file("resources/Page_objects/People.json")


def create_meeting(
    device,
    meeting="test_meeting",
    participants=None,
    repeat=None,
    all_day_meeting="OFF",
    location="bangalore",
    date=None,
    meeting_time="off",
    meeting_duration=5,
    start_meeting_time="off",
    start_meeting_time_after=5,
    consecutive_meeting="off",
):
    print("Create meeting : ", meeting)
    print("device :", device)
    global current_meeting_end_time
    current_meeting_end_time = None
    if consecutive_meeting == "on":
        current_reserved_meeting_time = common.wait_for_element(device, calendar_dict, "meeting_time").text
        current_meeting_start_time, current_meeting_end_time = current_reserved_meeting_time.split("—")
        print(
            f"current_meeting_start_time:{current_meeting_start_time}, current_meeting_end_time:{current_meeting_end_time}"
        )

    driver = obj.device_store.get(alias=device)
    navigate_to_calendar_tab(device)
    print("Inside Calendar Tab")
    settings_keywords.refresh_main_tab(device)
    common.wait_for_and_click(device, calendar_dict, "Schedule_meeting")
    time.sleep(action_time)
    common.click_if_present(device, calendar_dict, "Schedule_a_meeting")
    time.sleep(display_time)
    common.wait_for_and_click(device, calendar_dict, "meeting_name")
    element = common.wait_for_element(device, calendar_dict, "meeting_name")
    print("Checking Meeting_name text box")
    if meeting == "test_meeting":
        element.send_keys(config["meetings"]["name"])
    else:
        element.send_keys(meeting)
    print("Entered meeting name")
    time.sleep(display_time)
    common.hide_keyboard(device)
    if config["devices"][device]["model"].lower() == "gilbert":
        settings_keywords.swipe_till_end(device)
    if not common.is_element_present(device, calendar_dict, "meeting_location"):
        scroll_only_once(device)
    element = common.wait_for_element(device, calendar_dict, "meeting_location")
    print("Checking Meeting_location text box")
    element.click()
    if location == "bangalore":
        element.send_keys(config["meetings"]["location"])
    else:
        element.send_keys(location)
    print("Entered Meeting Location")
    if config["devices"][device]["model"].lower() in [
        "san jose",
        "santa cruz",
        "bakersfield",
        "santa cruz_13",
        "bakersfield_13",
    ]:
        common.hide_keyboard(device)
    else:
        driver.execute_script("mobile: performEditorAction", {"action": "done"})
    if date is None:
        print("date :", date)
    else:
        print("Selecting random forward date")
        common.wait_for_and_click(device, calendar_dict, "start_date_text")
        common.wait_for_element(device, calendar_dict, "date_picker_header_date")
        common.wait_for_and_click(device, calendar_dict, "next_month")
        common.wait_for_and_click(device, calendar_dict, "random_date")
        common.wait_for_and_click(device, calendar_dict, "ok_button")
    if repeat is None:
        print("repeat :", repeat)
    else:
        print("repeat :", repeat)
        app_bar_keywords.swipe_page_up(device)
        common.wait_for_and_click(device, calendar_dict, "repeat_option")
        repeat_list_names = ["Every day", "Every weekday (Mon-Fri)", "Every week", "Every month", "Every year"]
        if repeat not in repeat_list_names:
            raise AssertionError(f"Illegal input specified: '{repeat}'")
        result_xpath = common.get_dict_copy(calendar_dict, "day_element", "which day", repeat)
        common.wait_for_and_click(device, result_xpath, "day_element")
    time.sleep(display_time)
    settings_keywords.refresh_main_tab(device)
    if all_day_meeting == "OFF":
        print("all_day_meeting : ", all_day_meeting)
    else:
        print("all_day_meeting : ", all_day_meeting)
        elem = common.wait_for_element(device, calendar_dict, "all_day_switch")
        element = elem.text
        print("element : ", element)
        if all_day_meeting == "ON":
            if element == "ON":
                raise AssertionError("All Day meeting switch is ON Automatic")
            else:
                elem.click()
                print("Selected All Day meeting switch ON")
    settings_keywords.refresh_main_tab(device)
    if config["devices"][device]["model"].lower() == "gilbert":
        driver.swipe(320, 270, 320, 700)
        driver.swipe(320, 270, 320, 700)
    # When meeting_time is on we are handling the meeting start time, duration/ end time of the meeting

    if meeting_time == "on":
        select_custom_time_while_creating_meeting(
            device,
            meeting_duration,
            start_meeting_time,
            start_meeting_time_after,
            consecutive_meeting,
            current_meeting_end_time,
        )
    common.wait_for_and_click(device, calendar_dict, "Add_participants")
    element = common.wait_for_element(device, calendar_dict, "search_contact_box")
    print("Found search_contact_box")
    if participants is None:
        print("Participant  : ", config["meetings"]["participant"])
        element.send_keys(config["meetings"]["participant"])
        search_result_xpath = common.get_dict_copy(
            calendar_dict, "add_user", "user_name", config["meetings"]["participant"]
        )
        print("Search result xpath : ", search_result_xpath)
        common.wait_for_and_click(device, search_result_xpath, "add_user")
    else:
        participant_list = participants.split(",")
        print("Participant  : ", participant_list)
        element.clear()
        for participant in participant_list:
            if ":" in participant:
                user = participant.split(":")[1]
                print("User account : ", user)
                account = None
                if user.lower() == "delegate_user":
                    account = "delegate_user"
                elif user.lower() == "gcp_user":
                    account = "gcp_user"
                elif user.lower() == "meeting_user":
                    account = "meeting_user"
                elif user.lower() == "cap_user":
                    account = "cap_user"
                elif user.lower() == "auto_checkin_user":
                    account = "auto_checkin_user"
                elif user.lower() == "longname_user":
                    account = "longname_user"
                participant = participant.split(":")[0]
            else:
                account = "user"
            print("Account :", account)
            participant_name = config["devices"][participant][account]["username"].split("@")[0]
            element.send_keys(participant_name)
            time.sleep(display_time)
            search_result_xpath = common.get_dict_copy(
                calendar_dict, "add_user", "user_name", config["devices"][participant][account]["displayname"]
            )
            print("Search result xpath : ", search_result_xpath)
            common.wait_for_and_click(device, search_result_xpath, "add_user")
    common.hide_keyboard(device)
    common.wait_for_and_click(device, calendar_dict, "Submit")
    common.sleep_with_msg(device, 2, "Add-user Submit click")
    common.wait_for_and_click(device, calendar_dict, "Submit")
    common.wait_while_present(device, calendar_dict, "Submit")


def clear_meetings_from_calendar_tab(devices, exclude_meeting="test_meeting"):
    thread_list = []
    device_list = devices.split(",")
    print("Creating threads")
    for device in device_list:
        device_thread = threading.Thread(target=clear_all_meetings_except_test_meeting, args=(device, exclude_meeting))
        thread_list.append(device_thread)
    print("Starting threads")
    for t in thread_list:
        t.start()
    print("Wait until all threads complete and join")
    for t in thread_list:
        t.join()
    print("All threads completed and joined")


def clear_all_meetings_except_test_meeting(device, exclude_meeting="test_meeting"):
    print(f"{device}: clear_all_meetings_except {exclude_meeting}")
    navigate_to_calendar_tab(device)
    for i in range(6):
        settings_keywords.refresh_main_tab(device)
        time.sleep(action_time)

        if not common.is_element_present(device, calendar_dict, "meeting_title_name", "id"):
            print(f"{device}: Attempt {i} - Calendar tab is empty, no meetings to delete")
            return
        # meeting_container = common.wait_for_element(device, app_bar_dict, "meeting_list")
        # swipe_within_element(device, meeting_container, False)
        meeting_name_list = common.get_all_elements_texts(device, calendar_dict, "meeting_title_name", "id")

        # the list can contain multiple instances of a meeting, or the 'excluded_meeting', filter out:
        filtered_list = []
        for name in meeting_name_list:
            if name == exclude_meeting:
                continue
            if name in filtered_list:
                continue
            filtered_list.append(name)

        for meeting_name in filtered_list:
            delete_specific_meeting(device, meeting_name)
            time.sleep(display_time)


def delete_selected_meeting(device):
    print("device : ", device)
    if common.is_element_present(device, calendar_dict, "recurrence_indicator_btn"):
        print(f"{device} has recurrence indicator in the selected meeting")
        swipe_till_cancel_event(device)
        if common.click_if_present(device, calendar_dict, "View_series"):
            print(f"{device} : Clicked on view series")
            time.sleep(action_time)
            if common.click_if_present(device, calendar_dict, "remove_from_calender"):
                print(f"{device} : Clicked on remove series from calendar")
                time.sleep(display_time)
                settings_keywords.refresh_main_tab(device)
            else:
                swipe_till_cancel_event(device)
                if common.click_if_present(device, calendar_dict, "delete_event_button"):
                    print(f"{device} : Clicked on delete series")
                    time.sleep(action_time)
                    common.click_if_present(device, calendar_dict, "ok_button")
                    print(f"{device} : Clicked on delete series ok button")
                    time.sleep(display_time)
                    settings_keywords.refresh_main_tab(device)
                else:
                    if common.click_if_present(device, calendar_dict, "Cancel_series"):
                        print(f"{device} : Clciked on cancel series")
                        time.sleep(action_time)
                        common.click_if_present(device, calendar_dict, "Cancel_series_OK_btn")
                        print(f"{device} : Clicked on cancel series ok btn")
                        time.sleep(display_time)
                        settings_keywords.refresh_main_tab(device)
                    else:
                        navigate_to_calendar_tab(device)
        else:
            navigate_to_calendar_tab(device)
    else:
        if common.click_if_present(device, calendar_dict, "remove_from_calender"):
            print(f"{device} : Clicked on remove from calendar")
            time.sleep(display_time)
            settings_keywords.refresh_main_tab(device)
        else:
            swipe_till_cancel_event(device)
            if common.click_if_present(device, calendar_dict, "delete_event_button"):
                print(f"{device} : Clicked on delete event")
                time.sleep(action_time)
                common.click_if_present(device, calendar_dict, "ok_button")
                print(f"{device} : Clicked on delete event ok btn")
                time.sleep(display_time)
                settings_keywords.refresh_main_tab(device)
            else:
                if common.click_if_present(device, calendar_dict, "Cancel_event"):
                    print(f"{device} : Clicked on cancel event btn")
                    time.sleep(action_time)
                    common.click_if_present(device, calendar_dict, "Cancel_event_OK")
                    print(f"{device} : Clicked on cancel event ok btn")
                    time.sleep(display_time)
                    settings_keywords.refresh_main_tab(device)
                else:
                    navigate_to_calendar_tab(device)


def delete_specific_meeting(device, meeting="test_meeting"):
    print(f"{device}: delete meeting {meeting}")
    scroll_till_meeting_visible(device, meeting)
    meeting_xpath = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", meeting)
    common.wait_for_and_click(device, meeting_xpath, "meeting")
    delete_selected_meeting(device)


def delete_meeting(devices, meeting="test_meeting", all_day_meeting="OFF", recurrence=None):
    devices = devices.split(",")
    for device in devices:
        print("Delete meeting : ", meeting)
        print("device :", device)
        driver = obj.device_store.get(alias=device)
        if all_day_meeting == "ON":
            pass
        else:
            navigate_to_calendar_tab(device)
        time.sleep(display_time)
        tmp_dict = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", meeting)
        print("meeting_path : ", tmp_dict)
        elem = common.wait_for_element(device, tmp_dict, "meeting")
        print("elem : ", elem)
        if elem.is_displayed():
            common.wait_for_and_click(device, tmp_dict, "meeting")
        else:
            driver.swipe(100, 400, 100, 200)
            time.sleep(action_time)
            driver.swipe(100, 400, 100, 200)
            time.sleep(action_time)
            elem.click()
        swipe_till_cancel_event(device)
        if recurrence == "ON":
            common.wait_for_and_click(device, calendar_dict, "View_series")
            swipe_till_cancel_event(device)
            common.wait_for_and_click(device, calendar_dict, "Cancel_series")
        elif recurrence is None:
            if not common.click_if_present(device, calendar_dict, "Cancel_event_container"):
                common.wait_for_and_click(device, calendar_dict, "Cancel_event")
        if not common.click_if_present(device, calendar_dict, "cancel_event_btn"):
            print("waiting for click cancel ok button")
            common.wait_for_and_click(device, calendar_dict, "Cancel_event_OK")


def swipe_till_cancel_event(device):
    driver = obj.device_store.get(alias=device)
    window_size = driver.get_window_size()
    print("Window size: ", window_size)
    height = window_size["height"]
    width = window_size["width"]
    if height > width:
        print("Swiping co-ordinates : ", width / 2, 4 * (height / 5), width / 2, height / 5)
        driver.swipe(width / 2, 4 * (height / 5), width / 2, height / 5)
        time.sleep(action_time)
        driver.swipe(width / 2, 4 * (height / 5), width / 2, height / 5)
    else:
        print("Swiping co-ordinates : ", 3 * (width / 4), 4 * (height / 5), 3 * (width / 4), height / 5)
        driver.swipe(3 * (width / 4), 4 * (height / 5), 3 * (width / 4), height / 5)
        time.sleep(action_time)
        driver.swipe(3 * (width / 4), 4 * (height / 5), 3 * (width / 4), height / 5)
    time.sleep(action_time)


def navigate_to_calendar_tab(device):
    print("device :", device)
    if is_user_on_calendar_tab(device):
        return
    else:
        common.click_if_present(device, common_dict, "back", "xpath")
        common.click_if_present(device, calls_dict, "Call_Back_Button")
        common.click_if_present(device, homescreen_dict, "home_bar_icon")
        common.click_if_element_appears(device, calendar_dict, "calendar_tab")
        time.sleep(display_time)
        status = is_user_on_calendar_tab(device)
        if status is True:
            print("Navigated to calender tab")
            return
        common.click_if_present(device, common_dict, "back")
        time.sleep(action_time)
        if not common.is_element_present(device, app_bar_dict, "calendar_tab"):
            common.wait_for_and_click(device, app_bar_dict, "more_tab")
        common.wait_for_and_click(device, calendar_dict, "calendar_tab")


def is_user_on_calendar_tab(device):
    if common.is_element_present(device, calendar_dict, "Header", "id"):
        header_text = common.wait_for_element(device, calendar_dict, "Header", "id").text
        print(f"{device} is on {header_text} tab")
        if header_text == "Calendar":
            print(f"{device}: Already on calendar tab")
            return True
    return False


def verify_join_button_displayed(device):
    print("Verify join button is displayed on device : ", device)
    driver = obj.device_store.get(alias=device)
    # time.sleep(display_time)
    try:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((MobileBy.ID, calendar_dict["join_button"]["id"])))
    except Exception as e:
        raise AssertionError("Join button not present")
    print("Meeting Join button present")
    # time.sleep(display_time)
    pass


def opens_partner_settings_page(device):
    print("Opens partner settings page on device : ", device)
    if not common.click_if_element_appears(device, navigation_dict, "Navigation"):
        if not common.is_portrait_mode_cnf_device(device):
            raise AssertionError(f"{device} couldn't open navigation menu")
        common.wait_for_and_click(device, calendar_dict, "app_bar_more")
    common.wait_for_and_click(device, navigation_dict, "Settings_button")
    time.sleep(display_time)
    settings_keywords.swipe_till_end(device)
    if config["devices"][device]["model"].lower() == "gilbert":
        settings_keywords.swipe_till_end(device)
    time.sleep(action_time)
    common.wait_for_and_click(device, settings_dict, "Device_Settings")


def comes_out_of_partner_settings_page(device):
    print("Comes out of partner settings page : ", device)
    print("device :", device)
    # time.sleep(action_time)
    driver = obj.device_store.get(alias=device)
    time.sleep(action_time)
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((MobileBy.XPATH, device_settings_dict["back_to_settings"]["xpath"]))
    ).click()
    time.sleep(display_time)
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((MobileBy.XPATH, settings_dict["back"]["xpath"]))
    ).click()
    # time.sleep(display_time)


def join_meeting(device, meeting="test_meeting", disconnect=True, join_styles=None, dgj="false"):
    print("joins meeting named test_meeting by default unless stated otherwise; Meeting : ", meeting)
    devices = device.split(",")
    if join_styles is None:
        join_styles = ["None"] * len(devices)
    else:
        join_styles = join_styles.split(",")
        if len(devices) != len(join_styles):
            raise AssertionError(
                f"Total no of join styles: {len(join_styles)} does not match total no of devices: {len(devices)}"
            )
        for style in join_styles:
            if style not in ["conference", "None"]:
                raise AssertionError(f"incorrect join styles: {style} specified")
    for device, join_style in zip(devices, join_styles):
        print(f"device: {device}, join_style: {join_style}")
        device, user_type = common.decode_device_spec(device)
        print(f"device: {device}, user: {user_type}")
        if join_style.lower() == "conference":
            if not common.is_element_present(device, calls_dict, "call_bar"):
                settings_keywords.refresh_main_tab(device)
                refresh_cnf_device_for_meeting_visibility(device)
                scroll_till_meeting_visible(device, meeting)
            if config["devices"][device]["model"].lower() == "manhattan":
                tmp_dict = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", meeting)
                print("meeting_xpath : ", tmp_dict)
                common.wait_for_and_click(device, tmp_dict, "meeting")
                common.wait_for_and_click(device, calendar_dict, "join_button")
                common.wait_for_element(device, calls_dict, "Hang_up_button")
            else:
                expected_meeting_name = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", meeting)
                meeting_name = common.wait_for_element(device, expected_meeting_name, "meeting")
                if meeting_name.is_displayed():
                    name_list = []
                    print("Expected meeting is displayed on device")
                    join_btn_list = common.wait_for_element(
                        device,
                        calendar_dict,
                        "cnf_device_join_button_id",
                        "id",
                        cond=EC.presence_of_all_elements_located,
                    )
                    print(f"Length of join btn list : {join_btn_list}")
                    meeting_names_list = common.wait_for_element(
                        device, calendar_dict, "meeting_title_name", "id", cond=EC.presence_of_all_elements_located
                    )
                    print(f"Length of meeting names list : {meeting_names_list}")
                    for meeting_name in meeting_names_list:
                        if "Canceled:" not in meeting_name.text:
                            name_list.append(meeting_name.text)
                    print(f"Meetings displayed currently: {name_list}")
                    for m in name_list:
                        if m == meeting:
                            m_pos = name_list.index(m)
                            break
                    join_btn_list[m_pos].click()
                    common.wait_for_element(device, calls_dict, "Hang_up_button")
                    print("Joined the expected meeting")
                else:
                    raise AssertionError("Couldn't find the expected meeting to join")
        else:
            if common.is_norden(device):
                _max_attempts = 10
                # scroll_for_meeting_visibility(device, meeting=meeting)
                list_of_meetings = []
                if ":" in meeting:
                    meeting = common.device_displayname(meeting)
                m_list = common.get_all_elements_texts(device, calendar_dict, "meeting_title_name", "xpath")
                print(f"meeting title names:{m_list}")
                for _attempt in range(_max_attempts):
                    if meeting in m_list:
                        print(f"{device}: After scrolling {_attempt} times found meeting: '{meeting}'")
                        break
                    tr_calendar_keywords.scroll_up_meeting_tab(device)
                    m_list.extend(common.get_all_elements_texts(device, calendar_dict, "meeting_title_name", "xpath"))
                    if _attempt == _max_attempts - 1:
                        raise AssertionError(
                            f"{device}: After scrolling {_attempt} times meeting did not appear: '{meeting}'"
                        )
                meeting_list = common.wait_for_element(
                    device, calendar_dict, "meeting_title_name", "xpath", cond=EC.presence_of_all_elements_located
                )
                join_button_list = common.wait_for_element(
                    device, calendar_dict, "cnf_device_join_button", "xpath", cond=EC.presence_of_all_elements_located
                )
                if len(meeting_list) < len(join_button_list):
                    join_button_list = join_button_list[1:]
                    if len(meeting_list) != len(join_button_list):
                        raise AssertionError(
                            f"Number of meetings displayed: {len(meeting_list)} is not equal to number of join buttons: {len(join_button_list)}"
                        )
                for m in meeting_list:
                    list_of_meetings.append(str(m.text))
                print("List of Meeting displayed on home screen :", list_of_meetings)
                meeting_position = 0
                search_attempt = 1
                for _meeting in list_of_meetings:
                    if _meeting.lower() == meeting.lower():
                        meeting_position = list_of_meetings.index(_meeting)
                        print("Expected Meeting is displayed on screen : ", _meeting)
                        break
                    search_attempt += 1
                    if search_attempt == len(list_of_meetings) + 1:
                        raise AssertionError(f"Expected meeting: {meeting} is not displayed")
                print("Meeting position : ", meeting_position)
                join_button_list[meeting_position].click()
                print("Joined the expected meeting on device : ", device)
                if dgj.lower() == "true":
                    common.wait_for_element(device, tr_calendar_dict, "cancel")
                    common.wait_for_element(device, tr_calendar_dict, "joining_meeting")
            else:
                call_keywords.come_back_to_home_screen(device, disconnect)
                call_keywords.navigate_to_calls_tab(device)
                navigate_to_calendar_tab(device)
                time.sleep(display_time)
                settings_keywords.refresh_main_tab(device)
                tmp_dict = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", meeting)
                print("meeting_xpath : ", tmp_dict)
                scroll_for_meeting_visibility(device, meeting=meeting)
                common.wait_for_and_click(device, tmp_dict, "meeting")
                common.wait_for_and_click(device, calendar_dict, "join_button")


def join_meeting_from_all_day_meeting_tab(device, meeting):
    print("joins meeting named test_meeting by default unless stated otherwise; Meeting : ", meeting)
    devices = device.split(",")
    for device in devices:
        print("device :", device)
        scroll_till_meeting_visible(device, meeting)
        meeting_xpath = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", meeting)
        common.wait_for_and_click(device, meeting_xpath, "meeting")
        time.sleep(display_time)
        common.wait_for_and_click(device, calendar_dict, "cnf_device_join_button_id")


def add_participant_to_conversation(from_device, to_device, method):
    if method not in ["display_name", "phone_number", "extension"]:
        raise AssertionError(f"Illegal method specified: '{method}'")
    print(f"from_device: {from_device}, to_device: {to_device}, method: {method}")
    to_devices = to_device.split(",")
    devices = []
    accounts = []
    for device in to_devices:
        device, account = common.decode_device_spec(device)
        devices.append(device)
        accounts.append(account)
    print(f"Contact devices list: {devices} \n Accounts: {accounts}")
    common.click_if_present(from_device, calls_dict, "call_bar")
    navigate_to_add_participant_page(from_device)
    if common.is_norden(from_device):
        if not common.click_if_present(from_device, tr_calls_dict, "add_participants"):
            common.wait_for_and_click(from_device, calls_dict, "add_people_to_meeting")
    else:
        common.wait_for_and_click(from_device, calls_dict, "add_people_to_meeting")
    element = common.wait_for_element(from_device, calendar_dict, "search_contact_box")
    if method.lower() == "display_name":
        for device, account in zip(devices, accounts):
            print("Device and Account : ", device, account)
            displayname = config["devices"][device][account]["displayname"]
            username = config["devices"][device][account]["username"].split("@")[0]
            print("Adding Device with user name : ", device, username)
            element.send_keys(username)
            time.sleep(display_time)
            if config["devices"][from_device]["model"].lower() not in ["spokane", "sammamish", "vancouver"]:
                common.hide_keyboard(from_device)
            tmp_dict = common.get_dict_copy(calendar_dict, "add_user", "user_name", displayname)
            common.wait_for_and_click(from_device, tmp_dict, "add_user")
    elif method.lower() == "phone_number":
        for device, account in zip(devices, accounts):
            print("Device and Account : ", device, account)
            pstn_display = config["devices"][device][account]["pstndisplay"]
            print("Adding Device :", device)
            print("Phone Number : ", pstn_display)
            element.send_keys(pstn_display)
            time.sleep(display_time)
            if config["devices"][from_device]["model"].lower() not in ["spokane", "sammamish", "vancouver"]:
                common.hide_keyboard(from_device)
            tmp_dict = common.get_dict_copy(calendar_dict, "add_user", "user_name", pstn_display)
            common.wait_for_and_click(from_device, tmp_dict, "add_user")
    elif method.lower() == "extension":
        for device, account in zip(devices, accounts):
            print("Device and Account : ", device, account)
            extension = config["devices"][device][account]["extension"]
            pstn_display = config["devices"][device][account]["pstndisplay"]
            print("Adding Device :", device)
            print("Extension number : ", extension)
            element.send_keys(extension)
            time.sleep(display_time)
            if config["devices"][from_device]["model"].lower() not in ["spokane", "sammamish"]:
                common.hide_keyboard(from_device)
            tmp_dict = common.get_dict_copy(calendar_dict, "add_user", "user_name", pstn_display)
            common.wait_for_and_click(from_device, tmp_dict, "add_user")
    if common.is_norden(from_device):
        return
    if not common.is_lcp(from_device):
        common.wait_for_and_click(from_device, calls_dict, "save_contacts")
    time.sleep(action_time)
    common.wait_for_and_click(from_device, calendar_dict, "back")


def mute_all_participants(device):
    navigate_to_add_participant_page(device)

    common.wait_for_and_click(device, calendar_dict, "Mute_all")
    common.wait_for_and_click(device, calendar_dict, "Mute_all_ok")
    if common.is_norden(device):
        tr_call_keywords.close_roaster_button_on_participants_screen(device)
    else:
        common.wait_for_and_click(device, calendar_dict, "back")


def farmute_the_call(from_device, to_device):
    devices = to_device.split(",")

    navigate_to_add_participant_page(from_device)

    for device in devices:
        if ":" in device:
            account = device.split(":")[1]
            device = device.split(":")[0]
        else:
            account = "user"
        tmp_dict = common.get_dict_copy(
            calendar_dict, "farmute", "user_name", config["devices"][device][account]["displayname"]
        )
        common.wait_for_and_click(from_device, tmp_dict, "farmute")
        common.wait_for_and_click(from_device, calendar_dict, "mute_participant")
    common.wait_for_and_click(from_device, calendar_dict, "back")


def headers_shows_text_calendar(device_list):
    devices = device_list.split(",")
    print("Devices : ", devices)
    for device in devices:
        print("device : ", device)
        common.wait_for_element(device, calendar_dict, "Header")
        print("Calendar header is present")


def user_friendly_name_identity_in_the_conference_roster(device_list):
    devices = device_list.split(",")
    print("Devices : ", devices)
    for device in devices:
        print("device : ", device)
        if common.is_element_present(device, calendar_dict, "participant_name_text_view"):
            part_name = common.wait_for_element(device, calendar_dict, "participant_name_text_view").text
        else:
            part_name = common.wait_for_element(device, calendar_dict, "participant_name_text_view_v1").text

        print(
            "User friendly name in the conference roster of device {} with Participant name {}: ".format(
                device, part_name
            )
        )


def verify_teams_app_has_global_search_option(device):
    time.sleep(3)
    if not common.is_element_present(device, calls_dict, "search"):
        if not common.is_portrait_mode_cnf_device(device):
            raise AssertionError(f"User on {device} doesn't have global search option")
        people_keywords.navigate_to_people_tab(device)
        common.wait_for_element(device, calls_dict, "search")


def select_meeting(device, meeting="test_meeting", all_day_meeting="off"):
    if all_day_meeting.lower() not in ["on", "off"]:
        raise AssertionError(f"Illegal value for 'all_day_meeting': '{all_day_meeting}'")
    if all_day_meeting.lower() == "on":
        if not common.is_element_present(device, calendar_dict, "meeting_day_name"):
            scroll_to_top(device)
        common.wait_for_and_click(device, calendar_dict, "meeting_day_name")
    meeting_path = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", meeting)
    common.wait_for_and_click(device, meeting_path, "meeting")
    print("Meeting selected")
    verify_meeting_has_join_button(device)


def verify_meeting_details(device, meeting="test_meeting"):
    verify_meeting_has_meeting_name(device, meeting=meeting)
    verify_meeting_has_join_button(device)
    verify_meeting_has_edit_button(device)
    verify_meeting_has_meeting_date_and_time(device)
    verify_meeting_has_location(device)
    verify_meeting_has_see_more_option(device)


def verify_meeting_has_meeting_name(device, meeting="test_meeting"):
    print("meeting title is:", meeting)
    tmp_dict = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", meeting)
    common.wait_for_element(device, tmp_dict, "meeting")


def verify_meeting_has_join_button(device):
    common.wait_for_element(device, calendar_dict, "join_button")


def verify_meeting_has_meeting_list_item_join_button(device):
    common.wait_for_element(device, calendar_dict, "meeting_list_item_join_button", cond=EC.element_to_be_clickable)


def verify_meeting_has_edit_button(device):
    common.wait_for_element(device, calendar_dict, "edit_button", cond=EC.element_to_be_clickable)


def verify_meeting_has_meeting_date_and_time(device):
    meeting_date = common.wait_for_element(device, calendar_dict, "meeting_date").text
    meeting_time = common.wait_for_element(device, calendar_dict, "meeting_time").text
    print("Meeting has meeting date and time : ", meeting_date, meeting_time)


def verify_meeting_has_location(device):
    meeting_location = common.wait_for_element(device, calendar_dict, "meeting_location_details").text
    print("Meeting has meeting location : ", meeting_location)


def verify_meeting_has_see_more_option(device):
    driver = obj.device_store.get(alias=device)
    if config["devices"][device]["model"].lower() == "phoenix":
        driver.swipe(800, 500, 800, 200)
        time.sleep(action_time)
    common.wait_for_element(device, calendar_dict, "meeting_details_see_more")


def select_see_more_option(device):
    common.wait_for_and_click(device, calendar_dict, "meeting_details_see_more")


def verify_meeting_has_description(device):
    desc = common.wait_for_element(device, calendar_dict, "description").text
    print("Meeting has Description about meeting : ", desc)
    if len(desc) < 5:
        print(f"Meeting description text length is {len(desc)}, expected >= 5, text is:'{desc}'")
        raise AssertionError("Meeting description text length is too short")
    desc_details = common.wait_for_element(device, calendar_dict, "description_details").text
    print("Description details :: \n", desc_details)
    if len(desc_details) < 5:
        print(
            f"Meeting description details text length is {len(desc_details)}, expected >= 5, text is:'{desc_details}'"
        )
        raise AssertionError("Meeting description details text length is too short")


def view_meeting_entry_in_calendar_tab(device, meeting="test_meeting"):
    navigate_to_calendar_tab(device)
    time.sleep(display_time)
    meeting_path = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", meeting)
    common.wait_for_element(device, meeting_path, "meeting")
    print("Meeting appeared in calendar tab")


def refresh_for_meeting_visibility(device):
    call_keywords.come_back_to_home_screen(device)
    call_keywords.navigate_to_calls_tab(device)
    navigate_to_calendar_tab(device)
    settings_keywords.refresh_main_tab(device)


def wait_until_meeting_is_reflected(device, meeting):
    meeting_path = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", meeting)
    print("meeting path is : ", meeting_path)
    common.wait_for_element(device, meeting_path, "meeting")


def verify_ui_returns_to_home_page(device):
    if not (
        common.is_element_present(device, calls_dict, "search")
        or common.is_element_present(device, calendar_dict, "meet_now")
        or common.is_element_present(device, calendar_dict, "calendar_tab")
        or common.is_element_present(device, home_screen_dict, "home_bar_icon")
        or common.is_element_present(device, calendar_dict, "join_button")
    ):
        common.wait_for_element(device, calls_dict, "tool_bar")


def verify_invited_user_list_in_meeting(from_device, participants=None, meeting=""):
    if not common.is_element_present(from_device, calendar_dict, "participant_summary"):
        scroll_down_secondary_tab(from_device)
    # Scroll down more to get complete participants list
    scroll_down_secondary_tab(from_device)
    common.wait_for_element(from_device, calendar_dict, "participant_summary")
    actual_meeting_participant_list = common.get_all_elements_texts(
        from_device, calendar_dict, "meeting_participant_name"
    )
    expected_participant_list = []
    expected_organizer_name = []
    expected_organizer = common.device_displayname(from_device)
    expected_organizer_name.append(expected_organizer)
    if participants is None:
        expected_participant_list = [config["meetings"]["participant"]]
    else:
        participant_list = participants.split(",")
        for user in participant_list:
            expected_participant_list.append(common.device_displayname(user))
    expected_participant_list.sort()
    expected_meeting_participant_list = expected_organizer_name + expected_participant_list
    organizer_name = common.wait_for_element(from_device, calendar_dict, "meeting_participant_name").text
    if (
        organizer_name != expected_meeting_participant_list[0]
        or expected_meeting_participant_list != actual_meeting_participant_list
    ):
        raise AssertionError(
            f"{from_device}: Expected participant list: {expected_meeting_participant_list} doesn't match the actual list: {actual_meeting_participant_list}"
        )
    participant_role_list = common.get_all_elements_texts(
        from_device, calendar_dict, "meeting_participant_calendar_response"
    )
    if participant_role_list[0] != "Organizer":
        print(f"{from_device}: Roles of meeting participants are not as expected: {participant_role_list}")
    scroll_up_secondary_tab(from_device)


def scroll_down_secondary_tab(device):
    driver = obj.device_store.get(alias=device)
    window_size = driver.get_window_size()
    print("Window size: ", window_size)
    height = window_size["height"]
    width = window_size["width"]
    time.sleep(action_time)
    print("Window Width and height :", width, height)
    if height > width:
        driver.swipe(width / 2, 4 * (height / 5), width / 2, height / 5)
        time.sleep(action_time)
        driver.swipe(width / 2, 4 * (height / 5), width / 2, height / 5)
    else:
        driver.swipe(3 * (width / 4), 4 * (height / 5), 3 * (width / 4), height / 5)
        time.sleep(action_time)
        driver.swipe(3 * (width / 4), 4 * (height / 5), 3 * (width / 4), height / 5)
    # time.sleep(display_time)


def scroll_up_secondary_tab(device):
    driver = obj.device_store.get(alias=device)
    window_size = driver.get_window_size()
    print("Window size: ", window_size)
    height = window_size["height"]
    width = window_size["width"]
    print("Window Width and height :", width, height)
    if height > width:
        driver.swipe(width / 2, height / 5, width / 2, 4 * (height / 5))
        time.sleep(action_time)
        driver.swipe(width / 2, height / 5, width / 2, 4 * (height / 5))
    else:
        driver.swipe(3 * (width / 4), height / 5, 3 * (width / 4), 4 * (height / 5))
        time.sleep(action_time)
        driver.swipe(3 * (width / 4), height / 5, 3 * (width / 4), 4 * (height / 5))
    # time.sleep(display_time)


def hold_the_meeting(device):
    print("Hold the meeting : ", device)
    # time.sleep(action_time)
    driver = obj.device_store.get(alias=device)
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((MobileBy.ID, calendar_dict["call_more_options"]["id"]))
    ).click()
    time.sleep(action_time)
    hold_btn = driver.find_element_by_xpath(calendar_dict["Put_call_on_hold"]["xpath"])
    hold_btn.click()
    # time.sleep(display_time)


def remove_meeting_from_calender(devices):
    def attempt_remove(device):
        elem_list = common.wait_for_element(
            device, calendar_dict, "meeting_title_name", cond=EC.presence_of_all_elements_located
        )
        for meeting in elem_list:
            meeting.click()
            time.sleep(action_time)
            if common.click_if_present(device, calendar_dict, "remove_from_calender"):
                return True
            print("Remove from calendar not found")
            common.click_if_present(device, calls_dict, "Call_Back_Button")
            time.sleep(action_time)
        return False

    device_list = devices.split(",")
    for device in device_list:
        while attempt_remove(device):
            print("Removed as item from calendar")
        call_keywords.come_back_to_home_screen(device)


def get_meeting_time(device):
    devices = device.split(",")
    for device in devices:
        print("device :", device)
        time.sleep(display_time)
        driver = obj.device_store.get(alias=device)
        meeting_time = (
            WebDriverWait(driver, 30)
            .until(EC.element_to_be_clickable((MobileBy.ID, calendar_dict["meeting_time"]["id"])))
            .text
        )
        time.sleep(display_time)
        print(meeting_time)
    return str(meeting_time)


def check_rsvp_status(device):
    devices = device.split(",")
    for device in devices:
        print("device :", device)
        time.sleep(display_time)
        common.wait_for_element(device, calendar_dict, "rsvp_btn")


def respond_to_meeting(device, respond_option):
    devices = device.split(",")
    for device in devices:
        print("device :", device)
        common.wait_for_and_click(device, calendar_dict, "rsvp_btn")
        if respond_option.lower() == "accept":
            common.wait_for_and_click(device, calendar_dict, "accept_btn")
        elif respond_option.lower() == "tentative":
            common.wait_for_and_click(device, calendar_dict, "tentative_btn")
        elif respond_option.lower() == "decline":
            common.wait_for_and_click(device, calendar_dict, "decline_btn")
        else:
            raise AssertionError(f"Invalid respond_option input : {respond_option}")


def verify_meeting_response(device, respond_option):
    if respond_option.lower() not in ["accept", "tentative"]:
        raise AssertionError(f"Unexpected value for respond_option: {respond_option}")
    devices = device.split(",")
    for device in devices:
        if respond_option.lower() == "accept":
            respond_txt = common.wait_for_element(device, calendar_dict, "accept_btn").text
            expected_response = "Accepted"
        elif respond_option.lower() == "tentative":
            respond_txt = common.wait_for_element(device, calendar_dict, "tentative_btn").text
            expected_response = "Tentative"
        if respond_txt != expected_response:
            raise AssertionError(f"Expected response: {expected_response}, but found: {respond_txt}")


def get_meeting_conference_id(device, meeting="test_meeting"):
    print("device :", device)
    select_meeting(device, meeting)
    select_see_more_option(device)
    desc = common.wait_for_element(device, calendar_dict, "description").text
    print(f"Meeting Description page has title : {desc}")
    desc_details = common.wait_for_element(
        device, calendar_dict, "description_details", cond=EC.presence_of_all_elements_located
    )[-1].text
    print(f"{device}: Meeting Description which contanis conf_ID is : \n{desc_details}")
    phn_no_ptrn = "[+]\\d+\\s\\d+-\\d+-\\d+[,]"
    cnf_id_ptrn = "[,]\\d+[#]"
    phn_no = re.search(phn_no_ptrn, desc_details).group().rstrip(",")
    conf_id = re.search(cnf_id_ptrn, desc_details).group().lstrip(",")
    print(f"Conference Bridge Number: {phn_no}\n Conference ID: {conf_id}")
    return phn_no, conf_id


def verify_calendar_empty(device):
    navigate_to_calendar_tab(device)
    common.wait_for_element(device, calendar_dict, "no_meetings_calendar_tab")


def get_scheduled_meeting_time_on_cnf_device(device):
    devices = device.split(",")
    for device in devices:
        print("device :", device)
        # time.sleep(display_time)
        driver = obj.device_store.get(alias=device)
        elem_list = driver.find_elements_by_id(calendar_dict["meeting_time"]["id"])
        print("elem_list : ", elem_list)
        time.sleep(display_time)
        meeting_time = elem_list[-1].text
        time.sleep(display_time)
        print(meeting_time)
    return str(meeting_time)


def get_scheduled_meeting_name_on_cnf_device(device):
    devices = device.split(",")
    for device in devices:
        print("device :", device)
        # time.sleep(display_time)
        driver = obj.device_store.get(alias=device)
        elem_list = driver.find_elements_by_id(calendar_dict["meeting_title_name"]["id"])
        print("elem_list : ", elem_list)
        time.sleep(display_time)
        meeting_name = elem_list[-1].text
        time.sleep(display_time)
        print(meeting_name)
    return str(meeting_name)


def get_scheduled_meeting_organizer_name_on_cnf_device(device):
    devices = device.split(",")
    for device in devices:
        print("device :", device)
        # time.sleep(display_time)
        driver = obj.device_store.get(alias=device)
        elem_list = driver.find_elements_by_id(calendar_dict["meeting_organizer_name"]["id"])
        print("elem_list : ", elem_list)
        time.sleep(display_time)
        meeting_organizer = elem_list[-1].text
        time.sleep(display_time)
        print(meeting_organizer)
    return str(meeting_organizer)


def verify_meeting_without_location_on_cnf_device(device):
    devices = device.split(",")
    for device in devices:
        print("device :", device)
        if common.is_element_present(device, calendar_dict, "meeting_time"):
            print("Meeting object on Teams App doesn't have location information")
        else:
            raise AssertionError("Meeting object on Teams App having location information")


def verify_no_meetings_scheduled_on_saturday(device):
    devices = device.split(",")
    for device in devices:
        print("device :", device)
        time.sleep(display_time)
        if not common.is_element_present(device, calls_dict, "search"):
            if common.is_portrait_mode_cnf_device(device):
                # Skipping the execution for portrait mode conf devices
                continue
        for i in range(3):
            if common.is_element_present(device, calendar_dict, "saturday_name"):
                break
            else:
                print("i :", i)
                scroll_down_main_tab(device)
        if "Saturday" in common.get_all_elements_texts(device, calendar_dict, "meeting_day_name"):
            raise AssertionError("Meeting scheduled on Saturday")


def scroll_only_once(device):
    driver = obj.device_store.get(alias=device)
    window_size = driver.get_window_size()
    # print("Window size: ", window_size)
    height = window_size["height"]
    width = window_size["width"]
    print("Window Width and height :", width, height)
    if height > width:
        # print(
        #     "width / 2, 4 * (height / 5), width / 2, height / 5 : ", width / 2, 4 * (height / 5), width / 2, height / 5
        # )
        driver.swipe(width / 2, 4 * (height / 5), width / 2, height / 5)
    else:
        # print(
        #     "(width / 4), 4 * (height / 5), (width / 4), height / 5 : ",
        #     (width / 4),
        #     4 * (height / 5),
        #     (width / 4),
        #     height / 5,
        # )
        driver.swipe((width / 4), 4 * (height / 5), (width / 4), height / 5)
    time.sleep(1)


def scroll_down_main_tab(device):
    driver = obj.device_store.get(alias=device)
    window_size = driver.get_window_size()
    print("Window size: ", window_size)
    height = window_size["height"]
    width = window_size["width"]
    print("Window Width and height :", width, height)
    if height > width:
        print(
            "width / 2, 4 * (height / 5), width / 2, height / 5 : ", width / 2, 4 * (height / 5), width / 2, height / 5
        )
        driver.swipe(width / 2, 4 * (height / 5), width / 2, height / 5)
        time.sleep(action_time)
        driver.swipe(width / 2, 4 * (height / 5), width / 2, height / 5)
    else:
        print(
            "(width / 4), 4 * (height / 5), (width / 4), height / 5 : ",
            (width / 4),
            4 * (height / 5),
            (width / 4),
            height / 5,
        )
        driver.swipe((width / 4), 4 * (height / 5), (width / 4), height / 5)
        time.sleep(action_time)
        driver.swipe((width / 4), 4 * (height / 5), (width / 4), height / 5)
    # time.sleep(display_time)


def join_meeting_on_cnf_device(device, meeting="test_meeting"):
    print("joins meeting named test_meeting by default unless stated otherwise; Meeting : ", meeting)
    devices = device.split(",")
    for device in devices:
        print("device :", device)
        settings_keywords.refresh_main_tab(device)
        refresh_cnf_device_for_meeting_visibility(device)
        scroll_till_meeting_visible(device, meeting)
        driver = obj.device_store.get(alias=device)
        tmp_dict = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", meeting)
        common.wait_for_and_click(device, tmp_dict, "meeting")
        time.sleep(display_time)
        elem_list = driver.find_elements_by_id(calendar_dict["cnf_device_join_button_id"]["id"])
        print("elem_list : ", elem_list)
        elem_list[-1].click()
        print("Clicked Join button")
    pass


def refresh_cnf_device_for_meeting_visibility_old(device):
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((MobileBy.ID, calendar_dict["Schedule_meeting"]["id"]))
        ).click()
        print("Clicked on dial pad on the screen")
        time.sleep(display_time)
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["Close_dial_pad"]["xpath"]))
        ).click()
        print("Clicked on Close button")
    except Exception as e:
        raise AssertionError("Xpath not found")
    time.sleep(display_time)
    settings_keywords.refresh_main_tab(device)


def refresh_cnf_device_for_meeting_visibility(device):
    call_keywords.come_back_to_home_screen(device)
    people_keywords.navigate_to_people_tab(device)
    navigate_to_calendar_tab(device)
    settings_keywords.refresh_main_tab(device)


def close_dial_pad(device):
    devices = device.split(",")
    for device in devices:
        print("device :", device)
        # time.sleep(action_time)
        driver = obj.device_store.get(alias=device)
        try:
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["Close_dial_pad"]["xpath"]))
            ).click()
            print("Clicked on Close button")
        except Exception as e:
            if not common.click_if_present(device, calls_dict, "Call_Back_Button"):
                pass
        # time.sleep(display_time)


def verify_meeting_name_while_joining(device, meeting="test_meeting"):
    temp_dict = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", meeting)
    common.wait_for_element(device, temp_dict, "meeting")
    common.wait_for_element(device, calendar_dict, "hang_up_btn")


def verify_join_button_displayed_on_conf_device(device):
    devices = device.split(",")
    for device in devices:
        common.wait_for_element(device, calendar_dict, "cnf_device_join_button_id")


def scroll_till_meeting_visible(device, meeting="test_meeting"):
    devices = device.split(",")
    meeting_selector = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", meeting)

    for device in devices:
        print(f"{device}: scrolling for meeting '{meeting}'")
        for i in range(5):
            if common.is_element_present(device, meeting_selector, "meeting"):
                break
            # print("i :", i)
            scroll_only_once(device)
        common.wait_for_element(device, meeting_selector, "meeting")


def verify_participant_list_from_meeting_roster(device, connected_device_list):
    # Note: expected names:
    # The names displayed in the roster have been reformatted by Teams.
    # They have the form "[first name][space][first letter of last name]", all other text removed.
    # We are ONLY matching on "[first name]"
    from_device = device
    connected_devices = connected_device_list.split(",")
    print(f"Device: {from_device}\nConnected devices: {connected_devices}")
    expected_connected_devices = []
    actual_participant_list = []
    for device in connected_devices:
        if ":" in device:
            user = device.split(":")[1]
            if user.lower() == "pstn_user":
                expected_connected_devices.append(str(common.device_pstndisplay(device)))
            elif user.lower() == "meeting_user":
                expected_name = (str(common.device_displayname(device))).split(" ")
                expected_connected_devices.append(expected_name[0])
            else:
                raise AssertionError(f"{device}: Illegal 'user' type specified: '{user}'")
        else:
            expected_name = (str(common.device_displayname(device))).split(" ")
            expected_connected_devices.append(expected_name[0])

    navigate_to_add_participant_page(from_device)

    actual_participant = common.get_all_elements_texts(from_device, calendar_dict, "participant_name_text_view")
    for participant_name in actual_participant:
        if "+" not in participant_name:
            actual_name = participant_name.split(" ")
            actual_participant_list.append(actual_name[0])
        else:
            actual_participant_list.append(participant_name)
    print(f"Expected connected devices list: {expected_connected_devices}")
    print(f"Actual connected participants list: {actual_participant_list}")
    for participant_name in expected_connected_devices:
        if participant_name not in actual_participant_list:
            raise AssertionError(
                f"Connected devices list: {actual_participant_list} and given device list: {expected_connected_devices} is not matching"
            )


def remove_user_from_meeting(from_device, to_device):
    devices = to_device.split(",")

    navigate_to_add_participant_page(from_device)

    for device in devices:
        if ":" in device:
            user = device.split(":")[1]
            print("User account : ", user)
            account = None
            if user.lower() == "meeting_user":
                account = "meeting_user"
                device = device.split(":")[0]
            else:
                raise AssertionError("f{device}: Illegal 'user' type specified: '{user}'")
        else:
            account = "user"
        print("Account :", account)
        search_result_xpath = common.get_dict_copy(
            calendar_dict, "farmute", "user_name", config["devices"][device][account]["displayname"]
        )
        print("Search result xpath : ", search_result_xpath)
        common.wait_for_and_click(from_device, search_result_xpath, "farmute")
        common.wait_for_and_click(from_device, calendar_dict, "remove_participant")


def verify_someone_removed_you_from_the_meeting_text(device):
    for i in range(15):
        if common.is_element_present(device, calendar_dict, "someone_removed_from_the_meeting_text"):
            return
    raise AssertionError("'Someone removed you from the meeting' text is not visible on : ", device)


def swipe_within_element(device, element, swipe_up: bool):
    # Optimization - get the element rectangle locally:
    driver = obj.device_store.get(alias=device)
    element_rect = element.rect
    logging.debug("element.rect=%s" % str(element_rect))
    h_min = int(element_rect["x"])
    width = int(element_rect["width"])
    assert width > 0, "swipe_within_element: Element reports zero width"
    # Swipe in the middle of the element:
    startX = h_min + (width / 2)
    endX = startX
    v_min = int(element_rect["y"])
    height = int(element_rect["height"])
    assert height > 0, "swipe_within_element: Element reports zero height"
    if swipe_up:
        startY = v_min + (height / 2)
        endY = v_min + (height / 4)
    else:
        startY = v_min + (height / 4)
        endY = v_min + (height / 3)
    logging.debug(
        "Swipe: swipe_up=%s, startX=%s, startY=%s, endX=%s, endY=%s"
        % (str(swipe_up), str(startX), str(startY), str(endX), str(endY))
    )
    driver.swipe(startX, startY, endX, endY, 500)


def verify_meeting_under_all_day_event(device, meetings):
    meeting_container = common.wait_for_element(device, app_bar_dict, "meeting_list")
    swipe_within_element(device, meeting_container, False)
    meetings = meetings.split(",")
    common.wait_for_and_click(device, calendar_dict, "all_day_event")
    scroll_till_meeting_visible(device, meetings[-1])
    # scroll_down_main_tab(device)
    time.sleep(action_time)
    meeting_list = common.get_all_elements_texts(device, calendar_dict, "meeting_title_name")
    time.sleep(action_time)
    for meeting in meetings:
        print("meeting :", meeting)
        if not meeting in meeting_list:
            raise AssertionError(f"{meeting} is not visible inside All-Day events tab.")
        print(f"{meeting} is visible inside All-Day events tab")


def delete_all_day_meetings(device, meetings):
    settings_keywords.refresh_main_tab(device)
    common.wait_for_and_click(device, calendar_dict, "all_day_event")
    meetings = meetings.split(",")
    for meeting in meetings:
        print("meeting :", meeting)
        delete_meeting(device, meeting, all_day_meeting="ON")


def delete_multiple_meetings(device, meetings):
    meetings = meetings.split(",")
    for meeting in meetings:
        print("meeting :", meeting)
        delete_meeting(device, meeting)


def verify_conf_meeting_recurrence_indicator(device, meeting):
    driver = obj.device_store.get(alias=device)
    scroll_for_meeting_visibility(device, meeting)
    try:
        tmp_dict = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", meeting)

        meeting_name = common.wait_for_element(device, tmp_dict, "meeting").text
        if meeting_name.is_displayed():
            meeting_list = driver.find_elements_by_id(calendar_dict["meeting_title_name"]["id"])
            print("meeting_list is ", meeting_list)
            for m in meeting_list:
                if m.text.lower() == meeting:
                    print("title ", m.text)
                    meeting_pos = meeting_list.index(m)
                    meeting_time_list = driver.find_elements_by_id(calendar_dict["meeting_time"]["id"])
                    if meeting_time_list[meeting_pos].text.split()[-1] == "$":
                        print("recurrence indicator is present in the meeting")
                    else:
                        raise AssertionError("Recurrence indicator is not present in the meeting")
                    break
        else:
            raise AssertionError("Couldn't find expected meeting to check recurrence indicator")
    except NoSuchElementException:
        raise AssertionError("Expected meeting not found")


def verify_meeting_recurrence_indicator(device):
    # time.sleep(action_time)
    meeting_time = get_meeting_time(device)
    print("meeting_time : ", meeting_time)
    recurance_symbol = "$"
    print("recurance_symbol : ", recurance_symbol)
    symbol = meeting_time.split()[-1]
    print("Got symbol from Meeting time : ", symbol)
    if recurance_symbol == symbol:
        print("Teams App shows recurrence indicator in the Meeting")
    else:
        raise AssertionError("Unable to find recurrence indicator in the Meeting")


def verify_meeting_series(device, meeting):
    swipe_till_cancel_event(device)
    common.wait_for_and_click(device, calendar_dict, "View_series")
    if common.is_portrait_mode_cnf_device(device):
        common.wait_for_element(device, calls_dict, "Call_Back_Button")
    meeting_list = common.get_all_elements_texts(device, calendar_dict, "meeting_list")
    list1 = Counter(meeting_list)
    for meeting_name in list1.keys():
        if meeting_name == meeting:
            # Checking if recurring meeting name appears at least more than twice on the screen
            if list1[meeting_list] < 2:
                raise AssertionError(
                    f"{device}: '{meeting}' doesn't appear to be a recurring meeting. It only appears '{list1[meeting_list]}' times on the screen"
                )


def navigate_to_add_participant_page(device_name):
    print(f"{device_name}: opening meeting_participants")
    common.wait_for_element(device_name, calls_dict, "Hang_up_button")
    time.sleep(3)
    if not common.click_if_present(device_name, calls_dict, "participants_roster_button"):
        if not common.click_if_present(device_name, calls_dict, "Add_participants_button"):
            common.wait_for_and_click(device_name, calls_dict, "showRoster")

    # Verify add participants menu opened:
    if common.is_norden(device_name):
        if not common.is_element_present(device_name, tr_calls_dict, "add_participants"):
            common.wait_for_element(device_name, calls_dict, "add_people_to_meeting")
    else:
        common.wait_for_element(device_name, calendar_dict, "call_participant_list_items")
    print(f"{device_name}: meeting_participants is open")


def remove_meeting_from_calender_for_meeting_policy_test(count):
    if count == "1":
        print("One device connected No need to remove Meeting.")
    elif count == "2":
        clear_meetings_from_calendar_tab(devices="device_2", exclude_meeting="cnf_device_meeting")
    elif count == "3":
        clear_meetings_from_calendar_tab(devices="device_2,device_3", exclude_meeting="cnf_device_meeting")
    elif count == "4":
        clear_meetings_from_calendar_tab(devices="device_2,device_3,device_4", exclude_meeting="cnf_device_meeting")
    elif count == "5":
        clear_meetings_from_calendar_tab(
            devices="device_2,device_3,device_4,device_5", exclude_meeting="cnf_device_meeting"
        )


def remove_meeting_from_calender_for_user(count):
    if count == "1":
        clear_meetings_from_calendar_tab(devices="device_1")
    elif count == "2":
        clear_meetings_from_calendar_tab(devices="device_1,device_2")
    elif count == "3":
        clear_meetings_from_calendar_tab(devices="device_1,device_2,device_3")
    elif count == "4":
        clear_meetings_from_calendar_tab(devices="device_1,device_2,device_3,device_4")
    elif count == "5":
        clear_meetings_from_calendar_tab(devices="device_1,device_2,device_3,device_4,device_5")


def verify_truncated_meeting_title(devices, meeting):
    devices = devices.split(",")
    for device in devices:
        print("device :", device)
        title = common.wait_for_element(device, calendar_dict, "meeting_title").text
        print("title : ", title)
        compare_length = len(title)
        if title.endswith("...") and compare_length > 3:
            compare_length = compare_length - 3
        if not title.endswith("..."):
            raise AssertionError(f"{title} is not truncated")
        if not title[0:compare_length] == meeting[0:compare_length]:
            raise AssertionError(
                f"{device}: meeting title: expected {meeting[0:compare_length]}, found {title[0:compare_length]}"
            )


def verify_truncated_meeting_location(devices, location):
    devices = devices.split(",")
    for device in devices:
        print("device :", device)
        meeting_location = common.wait_for_element(device, calendar_dict, "meeting_location_from_meeting_page").text
        print("meeting_location : ", meeting_location)
        print("Given location : ", location)
        compare_length = len(meeting_location)
        if meeting_location.endswith("...") and compare_length > 3:
            compare_length = compare_length - 3
        if not meeting_location.endswith("..."):
            raise AssertionError(f"{meeting_location} is not truncated")
        if not meeting_location[0:compare_length] == location[0:compare_length]:
            raise AssertionError(
                f"{device}: meeting location : expected {location[0:compare_length]}, found {meeting_location[0:compare_length]}"
            )


def delete_long_title_meeting(device, meeting):
    select_long_title_meeting(device, meeting)
    driver = obj.device_store.get(alias=device)
    time.sleep(display_time)
    swipe_till_cancel_event(device)
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["Cancel_event"]["xpath"]))
    ).click()
    time.sleep(display_time)
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["Cancel_event_OK"]["xpath"]))
    ).click()
    # time.sleep(display_time)


def select_long_title_meeting(device, meeting):
    verify_meeting_has_meeting_list_item_join_button(device)
    elem_list = common.wait_for_element(
        device, calendar_dict, "meeting_title_name", cond=EC.presence_of_all_elements_located
    )
    print("elem_list : ", elem_list)
    for i in range(len(elem_list)):
        ui_meeting_name = elem_list[i].text
        compare_length = len(ui_meeting_name)
        if ui_meeting_name.endswith("...") and compare_length > 3:
            compare_length = compare_length - 3
        if ui_meeting_name[0:compare_length] == meeting[0:compare_length]:
            elem_list[i].click()
            print(f"{device}: Meeting '{ui_meeting_name}' selected as '{meeting}'")
            return
    raise AssertionError(f"{device}: Meeting '{meeting}' not found")


def verify_meeting_does_not_have_location(device):
    common.wait_for_element(device, calendar_dict, "join_button")
    meeting_location = common.wait_for_element(device, calendar_dict, "meeting_location_details").text
    if meeting_location != "Microsoft Teams Meeting":
        raise AssertionError(f"{device}: Meeting location is present: {meeting_location}")


def verify_meeting_respond_option_should_not_visible_for_organizer(device):
    if not common.is_element_present(device, calendar_dict, "join_button"):
        raise AssertionError(f"{device} is in an unexpected screen")
    if common.is_element_present(device, calendar_dict, "rsvp_btn"):
        raise AssertionError("Meeting respond option is visible for organizer")
    else:
        print("Meeting respond option is not visible for organizer as expected")


def verify_canceled_meeting_should_not_visible_for_organizer(device, meeting):
    time.sleep(action_time)
    if common.is_element_present(device, calendar_dict, "no_meetings_calendar_tab"):
        return print("no meeting founded")
    meeting_name_list = common.get_all_elements_texts(device, calendar_dict, "meeting_title_name")
    if meeting in meeting_name_list:
        raise AssertionError("Canceled meeting is visible for organizer")


def remove_canceled_meeting_from_calender(devices, meeting):
    device_list = devices.split(",")
    for device in device_list:
        print("device : ", device)
        driver = obj.device_store.get(alias=device)
        navigate_to_calendar_tab(device)
        settings_keywords.refresh_main_tab(device)
        try:
            select_meeting(device, meeting)
            try:
                WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((MobileBy.ID, calendar_dict["remove_from_calender"]["id"]))
                ).click()
                print("removed canceled meeting")
            except Exception as e:
                print("Remove from calendar not found")
                call_keywords.come_back_to_home_screen(device)
            time.sleep(2)
        except Exception as e:
            pass
            settings_keywords.refresh_main_tab(device)
        call_keywords.come_back_to_home_screen(device)
    pass


def verify_meeting_recurrence_indicator_symbol(device):
    common.wait_for_element(device, calendar_dict, "recurr_meeting_symbol")


def delete_all_meetings(devices):
    device_list = devices.split(",")
    for device in device_list:
        print("device : ", device)
        driver = obj.device_store.get(alias=device)
        navigate_to_calendar_tab(device)
        settings_keywords.refresh_main_tab(device)
        try:
            while driver.find_element_by_id(calendar_dict["meeting_list"]["id"]).is_displayed():
                WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((MobileBy.ID, calendar_dict["meeting_list"]["id"]))
                ).click()
                print(
                    "Proceeding to delete meeting : ",
                    driver.find_element_by_id(calendar_dict["meeting_list"]["id"]).text,
                )
                try:
                    WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((MobileBy.ID, calendar_dict["remove_from_calender"]["id"]))
                    ).click()
                    print("removed canceled meeting")
                except Exception as e:
                    swipe_till_cancel_event(device)
                    try:
                        WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["Cancel_event"]["xpath"]))
                        ).click()
                        print("Clicked on Cancel event")
                        WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["Cancel_event_OK"]["xpath"]))
                        ).click()
                        print("Clicked on Cancel event Ok Button")
                        time.sleep(display_time)
                    except Exception as e:
                        try:
                            WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["delete_event"]["xpath"]))
                            ).click()
                            print("Clicked on Delete button")
                            time.sleep(display_time)
                            WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["delete_event"]["xpath"]))
                            ).click()
                            print("Clicked on Delete button")
                        except Exception as e:
                            WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["View_series"]["xpath"]))
                            ).click()
                            print("Clicked on view series")
                            time.sleep(display_time)
                            swipe_till_cancel_event(device)
                            WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["Cancel_series"]["xpath"]))
                            ).click()
                            print("Clicked on Cancel Series")
                            time.sleep(display_time)
                            WebDriverWait(driver, 30).until(
                                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["Cancel_event_OK"]["xpath"]))
                            ).click()
                            time.sleep(display_time)
                time.sleep(2)
        except Exception as e:
            pass
            settings_keywords.refresh_main_tab(device)
        call_keywords.come_back_to_home_screen(device)
    pass


def join_meeting_from_meeting_description(device, meeting="test_meeting"):
    print("joins meeting named test_meeting by default unless stated otherwise; Meeting : ", meeting)
    devices = device.split(",")
    for device in devices:
        print("device :", device)
        call_keywords.come_back_to_home_screen(device)
        call_keywords.navigate_to_calls_tab(device)
        navigate_to_calendar_tab(device)
        settings_keywords.refresh_main_tab(device)
        driver = obj.device_store.get(alias=device)
        meeting_xpath = calendar_dict["meeting"]["xpath"].replace("meeting_xpath_replace", meeting)
        WebDriverWait(driver, 50).until(EC.element_to_be_clickable((MobileBy.XPATH, meeting_xpath))).click()
        time.sleep(display_time)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.ID, calendar_dict["meeting_details_see_more"]["id"]))
        ).click()
        print("Clicked on Meeting see more option")
        # Unable to find "join microsoft teams meeting" xpath
        # time.sleep(display_time)


def verify_meeting_does_not_have_description(device):
    meeting_description = common.wait_for_element(device, calendar_dict, "meeting_description").text
    print("meeting_description : ", meeting_description)
    if not meeting_description.startswith("Microsoft Teams"):
        raise AssertionError("Without adding description Meeting doesn't have default description")


def edit_the_meeting_and_add_new_participant(device, participants):
    common.wait_for_and_click(device, calendar_dict, "edit_button")
    common.hide_keyboard(device)
    common.wait_for_and_click(device, calendar_dict, "Add_participants")
    element = common.wait_for_element(device, calendar_dict, "search_contact_box")
    if participants is None:
        print("Participant  : ", config["meetings"]["participant"])
        element.set_value(config["meetings"]["participant"])
        search_result_xpath = common.get_dict_copy(
            calendar_dict, "add_user", "user_name", config["meetings"]["participant"]
        )
        print("Search result xpath : ", search_result_xpath)
    else:
        participant_list = participants.split(",")
        print("Participant  : ", participant_list)
        for participant in participant_list:
            if ":" in participant:
                user = participant.split(":")[1]
                print("User account : ", user)
                account = None
                if user.lower() == "delegate_user":
                    account = "delegate_user"
                elif user.lower() == "gcp_user":
                    account = "gcp_user"
                elif user.lower() == "meeting_user":
                    account = "meeting_user"
                participant = participant.split(":")[0]
            else:
                account = "user"
            print("Account :", account)
            participant_name = config["devices"][participant][account]["username"].split("@")[0]
            element.set_value(participant_name)
            time.sleep(display_time)
            search_result_xpath = common.get_dict_copy(
                calendar_dict, "add_user", "user_name", config["devices"][participant][account]["displayname"]
            )
            print("Search result xpath : ", search_result_xpath)
    common.wait_for_and_click(device, search_result_xpath, "add_user")

    common.wait_for_and_click(device, calendar_dict, "Submit")
    common.wait_for_and_click(device, calendar_dict, "Submit")


def remove_all_day_meeting_from_calender_for_user(devices):
    devicelist = devices.split(",")
    for device in devicelist:
        if not common.click_if_present(device, calendar_dict, "all_day_event"):
            print("user is not on all day event tab. Hence, continuing..")
            continue
        settings_keywords.refresh_main_tab(device)
        if common.is_element_present(device, calendar_dict, "meeting_title_name"):
            clear_all_meetings_except_test_meeting(device)


def edit_meeting_name_and_validate(device, new_meeting, all_day_meeting="off"):
    if all_day_meeting.lower() not in ["on", "off"]:
        raise AssertionError(f"Illegal value for 'all_day_meeting': '{all_day_meeting}'")
    common.wait_for_and_click(device, calendar_dict, "edit_button", selector_key="xpath")
    time.sleep(action_time)
    common.wait_for_and_click(device, calendar_dict, "meeting_name")
    element = common.wait_for_element(device, calendar_dict, "meeting_name")
    element.clear()
    element.send_keys(new_meeting)
    common.wait_for_and_click(device, calendar_dict, "Submit")
    if all_day_meeting.lower() == "on":
        select_meeting(device, new_meeting, all_day_meeting)
    tmp_dict = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", new_meeting)
    common.wait_for_element(device, tmp_dict, "meeting")
    print(f"Meeting name {new_meeting} sucsessfully updated")


def navigate_to_create_meeting_page(device):
    driver = obj.device_store.get(alias=device)
    navigate_to_calendar_tab(device)
    print("Inside Calendar Tab")
    try:
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, calendar_dict["Schedule_meeting"]["id"]))
        ).click()
        print("Clicked on create meeting calender")
        time.sleep(display_time)
        verify_create_meeting_screen(device)
    except Exception as e:
        raise AssertionError("Xpath not found ")


def verify_create_meeting_screen(device):
    driver = obj.device_store.get(alias=device)
    try:
        elem1 = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["new_event_view"]["xpath"]))
        )
        elem2 = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, calendar_dict["meeting_name"]["id"]))
        )
        if elem1.is_displayed() and elem2.is_displayed():
            print("We are in create meeting page")
        else:
            raise AssertionError("We are not in create meeting page")

        # time.sleep(display_time)
    except Exception as e:
        raise AssertionError("Xpath not found ")


def verify_declined_meeting_should_not_visible(device, meeting):
    driver = obj.device_store.get(alias=device)
    try:
        meeting_list = driver.find_elements_by_id(calendar_dict["meeting_list"]["id"])
        time.sleep(display_time)
        meeting_name_list = []
        for i in range(0, len(meeting_list) - 1):
            print("i : ", i)
            meeting_text = meeting_list[i].text
            print("Meeting text :", meeting_text)
            meeting_name_list.append(meeting_text)
        print("meeting_name_list : ", meeting_name_list)
        if meeting in meeting_name_list:
            raise AssertionError("Declined meeting is visible")
        else:
            print("Declined meeting is not visible")
    except Exception as e:
        raise AssertionError("Xpath not found")


def verify_meeting_is_visible(device, meeting="test_meeting"):
    tmp_dict = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", meeting)
    common.wait_for_element(device, tmp_dict, "meeting")


def verify_organizer_should_not_be_allowed_to_be_added_as_participant_in_meeting(device, participant, meeting):
    navigate_to_calendar_tab(device)
    settings_keywords.refresh_main_tab(device)
    common.wait_for_and_click(device, calendar_dict, "Schedule_meeting")
    common.wait_for_and_click(device, calendar_dict, "meeting_name")
    element = common.wait_for_element(device, calendar_dict, "meeting_name")
    element.send_keys(meeting)
    print(f"{device}: Entered meeting name as: {meeting}")
    time.sleep(display_time)
    common.hide_keyboard(device)
    common.wait_for_and_click(device, calendar_dict, "Add_participants")
    element = common.wait_for_element(device, calendar_dict, "search_contact_box")
    participant_username = common.device_username(participant).split("@")[0]
    element.send_keys(participant_username)
    search_result_xpath = common.get_dict_copy(calendar_dict, "add_user", "user_name", participant_username)
    print(f"{device}: Search result: {search_result_xpath}")
    common.wait_while_present(device, search_result_xpath, "add_user", max_wait_attempts=5)
    common.wait_for_and_click(device, calendar_dict, "Submit")
    common.teardown_meeting_test_case(device)


def verify_user_should_not_be_allowed_to_add_participant_who_are_already_added_into_meeting(
    device, participant, meeting
):
    print(f"{device}: participant to be added: {participant}, meetin name: {meeting}")
    navigate_to_calendar_tab(device)
    select_meeting(device, meeting)
    common.wait_for_and_click(device, calendar_dict, "edit_button")
    participant_name = config["devices"][participant]["user"]["username"].split("@")[0]
    common.wait_for_and_click(device, calendar_dict, "Add_participants")
    common.wait_for_element(device, calendar_dict, "search_contact_box").set_value(participant_name)
    temp_dict = common.get_dict_copy(
        calendar_dict, "add_user", "user_name", config["devices"][participant]["user"]["displayname"]
    )
    common.wait_for_and_click(device, temp_dict, "add_user")
    common.wait_for_element(device, calendar_dict, "participant_already_selected")
    for i in range(3):
        common.click_if_present(device, calendar_dict, "back")
        time.sleep(3)
    common.sleep_with_msg(device, 6, "react to back button click")
    common.click_if_present(device, calendar_dict, "discard_pop_up")


def verify_user_as_participant_should_not_be_displayed_with_edit_and_cancel_option(device):
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["edit_button"]["xpath"]))
        )
        raise AssertionError("Edit button is visible")
    except Exception as e:
        print("Edit button is not visible")
    time.sleep(display_time)
    swipe_till_cancel_event(device)
    try:
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["Cancel_event"]["xpath"]))
        )
        raise AssertionError("Cancel button is visible")
    except Exception as e:
        print("Cancel button is not visible")


def verify_user_not_allowed_to_save_meeting_after_removing_all_objects_in_edit_mode(device):
    common.wait_for_and_click(device, calendar_dict, "edit_button")
    common.wait_for_element(device, calendar_dict, "meeting_name").clear()
    common.wait_for_and_click(device, calendar_dict, "close_button")
    common.wait_for_and_click(device, calendar_dict, "ok_button")
    common.wait_for_and_click(device, calendar_dict, "Submit_content_icon")
    alert_text = common.wait_for_element(device, calendar_dict, "alert_title").text
    alert_message = common.wait_for_element(device, calendar_dict, "alert_message").text
    if alert_text != "Unable to schedule" or alert_message != "Add at least one attendee.":
        raise AssertionError(f"{device}: Alert title and text are not as expected: {alert_text}\t{alert_message}")
    common.wait_for_and_click(device, calendar_dict, "ok_button")
    common.wait_for_and_click(device, calendar_dict, "back")
    common.sleep_with_msg(device, 7, "react to back button click")
    common.wait_for_and_click(device, calendar_dict, "discard_pop_up")


def verify_user_should_not_be_allowed_to_create_meeting_in_past_time(device, meeting="past_meeting"):
    navigate_to_calendar_tab(device)
    settings_keywords.refresh_main_tab(device)
    common.wait_for_and_click(device, calendar_dict, "Schedule_meeting")
    common.wait_for_and_click(device, calendar_dict, "meeting_name")
    element = common.wait_for_element(device, calendar_dict, "meeting_name")
    element.send_keys(meeting)
    print(f"{device}: Entered meeting name as: {meeting}")
    time.sleep(display_time)
    common.hide_keyboard(device)
    common.wait_for_and_click(device, calendar_dict, "start_date_text")
    if common.click_if_present(device, calendar_dict, "1st_date"):
        raise AssertionError(f"{device}: User is able to select past time to schedule meeting")
    common.wait_for_and_click(device, calendar_dict, "ok_button")
    common.teardown_meeting_test_case(device)


def verify_meeting_should_not_be_displayed(device, meeting):
    _max_attempts = 3
    for _attempt in range(_max_attempts):
        temp_dict = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", meeting)
        if common.is_element_present(device, temp_dict, "meeting"):
            raise AssertionError(f"{device}: After scrolling {_attempt + 1} times found meeting: '{meeting}'")
        scroll_only_once(device)
        time.sleep(2)
    print(f"{device}: As expected, meeting: {meeting} is not displayed on device")


def scroll_to_top(device):
    driver = obj.device_store.get(alias=device)
    window_size = driver.get_window_size()
    print("Window size: ", window_size)
    height = window_size["height"]
    width = window_size["width"]
    print("Window Width and height :", width, height)
    for i in range(0, 5):
        if height > width:
            driver.swipe(width / 2, height / 2, width / 2, 3 * (height / 4))
            time.sleep(action_time)
        else:
            driver.swipe((width / 4), height / 2, (width / 4), 3 * (height / 4))
            time.sleep(action_time)
    pass


def scroll_for_meeting_visibility(device, meeting="test_meeting"):
    devices = device.split(",")
    _max_attempts = 5
    for device in devices:
        for _attempt in range(_max_attempts):
            temp_dict = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", meeting)
            if common.is_element_present(device, temp_dict, "meeting"):
                print(f"{device}: After scrolling {_attempt + 1} times found meeting: '{meeting}'")
                break
            if common.is_norden(device):
                tr_calendar_keywords.scroll_till_end_meeting_tab(device)
            else:
                scroll_only_once(device)
            if _attempt == _max_attempts - 1:
                raise AssertionError(
                    f"{device}: After scrolling {_attempt + 1} times meeting did not appear: '{meeting}'"
                )
            time.sleep(2)


def raise_hand(device):
    print("device :", device)
    # Make sure we are in a call:
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    time.sleep(5)
    if not common.click_if_present(device, calendar_dict, "call_control_reactions_button"):
        common.wait_for_and_click(device, calls_dict, "call_more_options")
    common.wait_for_and_click(device, calendar_dict, "raise_hand")


def verify_raise_hand(from_device, to_device, status):
    print("from_device :", from_device)
    print("to_device :", to_device)
    if status.lower() not in ["on", "off"]:
        raise AssertionError(f"Illegal value for 'status': '{status}'")
    if status.lower() == "on":
        common.wait_for_element(from_device, calendar_dict, "raise_hand_symbol")
        common.wait_for_element(from_device, calendar_dict, "hand_raise_text_on_meeting_screen")
        common.wait_for_element(to_device, calendar_dict, "raise_hand_symbol")
        navigate_to_add_participant_page(to_device)
        common.wait_for_element(to_device, calendar_dict, "raise_hand_symbol")
        common.wait_for_and_click(to_device, calls_dict, "Call_Back_Button")

    elif status.lower() == "off":
        if common.is_element_present(from_device, calendar_dict, "raise_hand_symbol") or common.is_element_present(
            to_device, calendar_dict, "raise_hand_symbol"
        ):
            raise AssertionError("Raise hand symbol is visible")


def lower_hand(device):
    print("device :", device)
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    if not common.click_if_present(device, calendar_dict, "call_control_reactions_button"):
        common.wait_for_and_click(device, calls_dict, "call_more_options")
    common.wait_for_and_click(device, calendar_dict, "lower_hand")
    time.sleep(5)


def verify_meet_now_icon(device):
    common.wait_for_element(device, calendar_dict, "meet_now")


def tap_on_meet_now_icon_and_validate(device):
    print("device :", device)
    if not common.click_if_element_appears(device, calendar_dict, "meet_now"):
        if not common.is_portrait_mode_cnf_device(device):
            raise AssertionError(f"{device} couldn't navigate to meet now page")
        common.wait_for_and_click(device, calendar_dict, "app_bar_meet_now")
    time.sleep(display_time)
    common.wait_for_element(device, calendar_dict, "meet_now_join_btn", wait_attempts=10)
    common.wait_for_element(device, calendar_dict, "edit_meeting_info", wait_attempts=10)
    common.wait_for_element(device, calls_dict, "mic_button_unmuted", wait_attempts=10)
    common.wait_for_element(device, calendar_dict, "call_control_speaker", wait_attempts=10)
    common.wait_for_element(device, calendar_dict, "prejoin_dropdown_menu", wait_attempts=10)


def close_meet_now_conference_page(device):
    common.wait_for_and_click(device, calendar_dict, "meet_now_conference_page_dismiss")


def initiated_a_conference_call_from_meet_now(device):
    print("device :", device)
    common.wait_for_and_click(device, calendar_dict, "meet_now_join_btn")


def volume_up_using_keyevent(device):
    print("device :", device)
    subprocess.call(
        "adb -s {} shell input keyevent 24".format(config["devices"][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    print("Increased volume")


def volume_down_using_keyevent(device):
    print("device :", device)
    subprocess.call(
        "adb -s {} shell input keyevent 25".format(config["devices"][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    print("Decreased volume")


def turn_on_live_caption(device):
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_and_click(device, calendar_dict, "call_more_options")
    common.wait_for_and_click(device, calendar_dict, "turn_on_live_captions")


def turn_off_live_caption(device):
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_and_click(device, calendar_dict, "call_more_options")
    common.wait_for_and_click(device, calendar_dict, "turn_off_live_captions")


def verify_user_joined_meeting_without_any_title(device):
    meeting_title = common.wait_for_element(device, calendar_dict, "default_meeting_title").text
    if meeting_title.lower() not in ["new meeting", "meeting"]:
        raise AssertionError(f"{device}: Meeting has title: {meeting_title}")


def verify_meeting_more_options(device):
    device, account = common.decode_device_spec(device)
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    common.wait_for_and_click(device, calendar_dict, "call_more_options")
    if account.lower() == "meeting_user":
        common.wait_for_element(device, calendar_dict, "lock_the_meeting")
        common.wait_for_element(device, calendar_dict, "turn_on_live_captions")
        common.wait_for_element(device, calls_dict, "call_dialpad_under_more")
        call_keywords.dismiss_call_more_options(device)
        return
    common.wait_for_element(device, calendar_dict, "start_recording")
    common.wait_for_element(device, calendar_dict, "turn_on_live_captions")
    common.wait_for_element(device, calls_dict, "call_dialpad_under_more")
    call_keywords.dismiss_call_more_options(device)


def verify_meet_now_close_button(device):
    common.click_if_present(device, calendar_dict, "meet_now_conference_page_dismiss")


def raise_hand_symbol_verification_on_call_roster_screen(device):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((MobileBy.ID, calls_dict["Hang_up_button"]["id"])))
        print("Call control visible")
    except Exception as e:
        settings_keywords.click_device_center_point(device)
        print("Clicked on center point")
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.ID, calendar_dict["call_control_raise_hand_button"]["id"]))
        )
        print("call_control_raise_hand_button visible")
    except Exception as e:
        raise AssertionError("Xpath not found")


def add_participants_symbol_verification_on_call_roster_screen(device):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((MobileBy.ID, calls_dict["Hang_up_button"]["id"])))
        print("Call control visible")
    except Exception as e:
        settings_keywords.click_device_center_point(device)
        print("Clicked on center point")
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["Add_participants_symbol"]["xpath"]))
        )
        print("Add_participants_symbol visible")
    except Exception as e:
        raise AssertionError("Xpath not found")


def back_to_meeting_page(device):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calls_dict["Call_Back_Button"]["xpath"]))
        ).click()
        print("Clicked Back")
    except Exception as e:
        raise AssertionError("Xpath not found")


def verify_live_caption_visibility(device):
    print("device :", device)
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    common.wait_for_and_click(device, calls_dict, "call_more_options")
    common.wait_for_element(device, calendar_dict, "turn_on_live_captions")
    # dismiss any "call_more_options" pop-up
    call_keywords.dismiss_call_more_options(device)


def turn_on_live_caption_and_validate(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    common.wait_for_and_click(device, calls_dict, "call_more_options")
    common.wait_for_and_click(device, calls_dict, "turn_on_live_captions")
    for i in range(10):
        if common.is_element_present(device, calendar_dict, "live_caption_msg"):
            print("live caption started")
            return
    raise AssertionError("Live caption message not appeared")


def turn_off_live_caption_and_validate(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    common.wait_for_and_click(device, calls_dict, "call_more_options")
    common.wait_for_and_click(device, calendar_dict, "turn_off_live_captions")


def verify_meetings_btn_presence_under_app_settings(device):
    common.wait_for_and_click(device, navigation_dict, "Navigation", wait_attempts=40)
    common.wait_for_and_click(device, navigation_dict, "Settings_button")
    if not common.is_element_present(device, calendar_dict, "meetings_button"):
        scroll_only_once(device)
    common.wait_for_element(device, calendar_dict, "meetings_button")


def verify_meetings_option_under_app_settings_page(device):
    verify_meetings_btn_presence_under_app_settings(device)
    common.wait_for_and_click(device, calendar_dict, "meetings_button")
    common.wait_for_element(device, calendar_dict, "meetings_name_button")


def enable_show_meeting_names_option(device):
    enable_or_disable_show_meeting_name_option(device, "ON")


def disable_show_meeting_names_option(device):
    enable_or_disable_show_meeting_name_option(device, "OFF")


def verify_meeting_title_should_match_with_organizer_name(organizer):
    driver = obj.device_store.get(alias=organizer)
    time.sleep(action_time)
    organizer_name = config["devices"][organizer]["user"]["displayname"]
    print("organizer_name : ", organizer_name)
    try:
        meeting_titles = []
        meeting_list = driver.find_elements_by_id(calendar_dict["meeting_list"]["id"])
        for i in range(0, len(meeting_list)):
            print("i : ", i)
            meeting_text = meeting_list[i].text
            print("Meeting text :", meeting_text)
            meeting_titles.append(meeting_text.lower())
        print("meeting_titles : ", meeting_titles)
        if organizer_name.lower() in meeting_titles:
            print("Able to see Meeting Titles replaced with Organizer name")
        else:
            raise AssertionError("Unale to see Meeting Titles replaced with Organizer name")
    except Exception as e:
        raise AssertionError("Xpath not found")


def verify_all_day_meeting_title_should_match_with_organizer_name(organizer):
    driver = obj.device_store.get(alias=organizer)
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["all_day_event"]["xpath"]))
        ).click()
    except Exception as e:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["all_day_event"]["xpath1"]))
        ).click()
    print("Clicked on All Day event option")
    time.sleep(action_time)
    verify_meeting_title_should_match_with_organizer_name(organizer)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((MobileBy.XPATH, common_dict["back"]["xpath"]))).click()
    print("Clicked on BACK button")


def join_meeting_when_privacy_toggle_is_turned_off(device, organizer_name):
    organizer_username = config["devices"][organizer_name]["user"]["displayname"]
    print("organizer_username : ", organizer_username)
    join_meeting(device, meeting=organizer_username)


def verify_meeting_name_after_joining_the_meeting(device, meeting):
    driver = obj.device_store.get(alias=device)
    try:
        meeting_header = (
            WebDriverWait(driver, 5)
            .until(EC.element_to_be_clickable((MobileBy.ID, calendar_dict["Header"]["id"])))
            .text
        )
        print("meeting_header : ", meeting_header)
        if meeting_header.lower() == meeting.lower():
            print("Meeting title is matching after joining the meeting when privacy toggle is turned off on the device")
        else:
            raise AssertionError
    except Exception as e:
        raise AssertionError("Xpath not found")


def make_an_attendee(from_device, to_device, device_type=None):
    if device_type is not None and device_type.lower() != "console":
        raise AssertionError(f"Unexpected value for device type: {device_type}")
    to_device = to_device.split(",")
    print("from_device :", from_device)
    print("to_device :", to_device)
    for to_device in to_device:
        account = "user"
        if ":" in to_device:
            user = to_device.split(":")[1]
            print("User account : ", user)
            if user.lower() == "meeting_user":
                account = "meeting_user"
        print("Account :", account)
        to_device = to_device.split(":")[0]

        if "console" not in from_device:
            navigate_to_add_participant_page(from_device)

        if device_type is not None and device_type.lower() == "console":
            if "console" in from_device:
                user_name = config["devices"][to_device][account]["displayname"]
            else:
                user_name = config["consoles"][to_device][account]["username"].split("@")[0]
        else:
            user_name = config["devices"][to_device][account]["displayname"]

        ele_text = common.wait_for_element(
            from_device, calendar_dict, "add_user", "id", cond=EC.presence_of_all_elements_located
        )
        participant_list = [str(i.text) for i in ele_text]
        print(f"participant list :", participant_list)
        user_position = 0
        for _user in participant_list:
            if _user.lower() == user_name.lower():
                user_position = participant_list.index(_user)
                print(f"expected user to click:", _user)
        ele_text[user_position].click()
        common.wait_for_and_click(from_device, calendar_dict, "make_an_attendee")
        common.wait_for_and_click(from_device, calendar_dict, "change_btn")
        time.sleep(display_time)
        if "console" not in from_device:
            if not common.click_if_present(from_device, tr_calls_dict, "close_roaster_button"):
                common.wait_for_and_click(from_device, common_dict, "back")


def verify_you_are_an_attendee_now_notification(device, status="on"):
    devices = device.split(",")
    if status.lower() not in ["on", "off"]:
        raise AssertionError(f"Illegal value for 'status': '{status}'")
    for device in devices:
        common.wait_for_element(device, calendar_dict, "hang_up_btn")
        if status == "on":
            common.wait_for_element(device, calendar_dict, "you_are_an_attendee_now")
            common.wait_for_element(device, tr_calendar_dict, "attende_x_button")
        elif status == "off":
            if common.is_element_present(device, calendar_dict, "you_are_an_attendee_now"):
                raise AssertionError(f"{device} is still contains attendee notification")


def verify_add_participant_button_should_not_visible_for_attendee(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    if not common.click_if_present(device, calls_dict, "participants_roster_button"):
        if not common.click_if_present(device, calls_dict, "Add_participants_button"):
            common.wait_for_and_click(device, calls_dict, "showRoster")
    if common.is_element_present(device, calls_dict, "Invite_new_user"):
        raise AssertionError("Invite_new_user button visible for attendee")
    print("Invite_new_user button is not visible for attendee")
    time.sleep(5)
    if not common.click_if_present(device, tr_calls_dict, "close_roaster_button"):
        common.wait_for_and_click(device, common_dict, "back")


def make_an_presenter(from_device, to_device, device_type=None):
    if device_type is not None and device_type.lower() != "console":
        raise AssertionError(f"Unexpected value for device type: {device_type}")
    print("from_device :", from_device)
    print("to_device :", to_device)
    account = "user"
    if ":" in to_device:
        user = to_device.split(":")[1]
        print("User account : ", user)
        if user.lower() == "meeting_user":
            account = "meeting_user"
    print("Account :", account)
    to_device = to_device.split(":")[0]

    if "console" not in from_device:
        navigate_to_add_participant_page(from_device)

    if device_type is not None and device_type.lower() == "console":
        if "console" in from_device:
            user_name = config["devices"][to_device][account]["displayname"]
        else:
            user_name = config["consoles"][to_device][account]["username"].split("@")[0]
    else:
        user_name = config["devices"][to_device][account]["displayname"]

    ele_text = common.wait_for_element(
        from_device, calendar_dict, "add_user", "id", cond=EC.presence_of_all_elements_located
    )
    participant_list = [str(i.text) for i in ele_text]
    print(f"participant list :", participant_list)
    user_position = 0
    for _user in participant_list:
        if _user.lower() == user_name.lower():
            user_position = participant_list.index(_user)
            print(f"expected user to click:", _user)
    ele_text[user_position].click()
    common.wait_for_and_click(from_device, calendar_dict, "make_an_presenter")
    common.wait_for_and_click(from_device, calendar_dict, "change_btn")
    time.sleep(5)
    if "console" not in from_device:
        if not common.click_if_present(from_device, tr_calls_dict, "close_roaster_button"):
            common.wait_for_and_click(from_device, common_dict, "back")


def verify_you_are_an_presenter_now_notification(device):
    print("device :", device)
    common.wait_for_element(device, calendar_dict, "you_are_an_presenter_now")


def verify_add_participant_button_should_visible_for_presenter(device):
    navigate_to_add_participant_page(device)
    if not common.is_element_present(device, calls_dict, "Invite_new_user"):
        if not common.is_element_present(device, tr_calls_dict, "add_participants"):
            raise AssertionError("Invite_new_user button is not visible for presenter")
    print("Invite_new_user button is visible for presenter")
    if not common.click_if_present(device, tr_calls_dict, "close_roaster_button"):
        common.wait_for_and_click(device, common_dict, "back")


def verify_the_meeting_description_page(device, meeting="test_meeting"):
    select_meeting(device, meeting)
    select_see_more_option(device)
    desc_details = common.get_all_elements_texts(device, calendar_dict, "description_details")
    search_text_list = [
        "Join the meeting now",
        "Find a local number",
        "Reset dial-in PIN",
        "Meeting options",
    ]
    for search_term in search_text_list:
        for i in range(len(desc_details)):
            if search_term in desc_details[i]:
                break
            if i == len(desc_details) - 1:
                raise AssertionError(f"{device}: Expected link: {search_term} not found in description: {desc_details}")
    common.wait_for_and_click(device, common_dict, "back")


def verify_device_whiteboard_sharing_option_support(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    device_model = config["devices"][device]["model"].lower()
    if device_model in ["riverside", "seattle", "olympia", "tacoma", "gilbert"]:
        print(f"{device} doesn't support whiteboard sharing. Device Model is: '{device_model}'")
        status = "fail"
    else:
        common.wait_for_and_click(device, calls_dict, "call_more_options")
        common.wait_for_element(device, calendar_dict, "share_whiteboard")
        status = "pass"
        settings_keywords.click_device_center_point(device)
        common.wait_for_element(device, calls_dict, "Hang_up_button")
    return status


def tap_on_whiteboard_sharing_option(device):
    print("device ", device)
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((MobileBy.ID, calls_dict["Hang_up_button"]["id"])))
        print("Call control visible")
    except Exception as e:
        settings_keywords.click_device_center_point(device)
        print("Clicked on center point")

    elem = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((MobileBy.ID, calls_dict["call_more_options"]["id"]))
    )
    elem.click()
    print("Clicked on call more option")
    time.sleep(display_time)
    try:
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["share_whiteboard"]["xpath"]))
        ).click()
        print("Clicked on Whiteboard sharing option")
    except Exception as e:
        raise AssertionError("Whiteboard sharing option is not visible")


def verify_whiteboard_successfully_loaded(devices):
    devices = devices.split(",")
    for device in devices:
        print("device :", device)
        driver = obj.device_store.get(alias=device)
        try:
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable(
                    (MobileBy.XPATH, calendar_dict["share_whiteboard_error_refresh_icon"]["xpath"])
                )
            ).click()
            print("Clicked on share_whiteboard_error_refresh_icon")
            time.sleep(refresh_time)
        except Exception as e:
            print("No error message visible")
            pass
        time.sleep(display_time)
        try:
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["whiteboard_toolbar_title"]["xpath"]))
            )
            print("whiteboard_toolbar_title visible")
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["pan_zoom"]["xpath"]))
            )
            print("pan_zoom visible")
        except Exception as e:
            raise AssertionError("xpath not found")


def verify_whiteboard_tools(devices):
    devices = devices.split(",")
    for device in devices:
        print("device :", device)
        driver = obj.device_store.get(alias=device)
        try:
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["pan_zoom"]["xpath"]))
            )
            print("pan_zoom visible")
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["black_pen"]["xpath"]))
            )
            print("black_pen button visible")
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["red_pen"]["xpath"]))
            )
            print("red_pen button visible")
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["green_pen"]["xpath"]))
            )
            print("green_pen button visible")
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["blue_pen"]["xpath"]))
            )
            print("blue_pen button visible")

            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["eraser"]["xpath"]))
            )
            print("eraser button visible")
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["add_text"]["xpath"]))
            )
            print("add_text button visible")
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["add_note"]["xpath"]))
            )
            print("add_note button visible")
        except Exception as e:
            raise AssertionError("xpath not found")


def verify_whiteboard_tools_functionality(devices):
    devices = devices.split(",")
    for device in devices:
        print("device :", device)
        driver = obj.device_store.get(alias=device)
        try:
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["pan_zoom"]["xpath"]))
            ).click()
            print("clicked on pan_zoom button")
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["pan_zoom_view"]["xpath"]))
            )
            print("pan_zoom_view visible")
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["black_pen"]["xpath"]))
            ).click()
            print("Clicked on black_pen button button")
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["black_pen_view"]["xpath"]))
            )
            print("black_pen_view visible")
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["red_pen"]["xpath"]))
            ).click()
            print("Clicked on red_pen button button")
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["red_pen_view"]["xpath"]))
            )
            print("red_pen_view button visible")
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["green_pen"]["xpath"]))
            ).click()
            print("Clicked on green_pen button")
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["green_pen_view"]["xpath"]))
            )
            print("green_pen_view button visible")
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["blue_pen"]["xpath"]))
            ).click()
            print("Clicked on blue_pen button")
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["blue_pen_view"]["xpath"]))
            )
            print("blue_pen_view button visible")
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["eraser"]["xpath"]))
            ).click()
            print("Clicked on eraser button")
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["eraser_view"]["xpath"]))
            )
            print("eraser_view button visible")
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["add_text"]["xpath"]))
            ).click()
            print("Clicked on add_text button")
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["add_note"]["xpath"]))
            ).click()
            print("Clicked on add_note button button")
        except Exception as e:
            raise AssertionError("xpath not found")


def write_something_using_pen(device, pen_color):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    try:
        if pen_color.lower() == "black":
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["black_pen"]["xpath"]))
            ).click()
            print("Clicked on black_pen button button")
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["black_pen_view"]["xpath"]))
            )
            print("black_pen_view visible")
        elif pen_color.lower() == "red":
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["red_pen"]["xpath"]))
            ).click()
            print("Clicked on red_pen button button")
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["red_pen_view"]["xpath"]))
            )
            print("red_pen_view button visible")
        elif pen_color.lower() == "green":
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["green_pen"]["xpath"]))
            ).click()
            print("Clicked on green_pen button")
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["green_pen_view"]["xpath"]))
            )
            print("green_pen_view button visible")
        if pen_color.lower() == "blue":
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["blue_pen"]["xpath"]))
            ).click()
            print("Clicked on blue_pen button")
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["blue_pen_view"]["xpath"]))
            )
            print("blue_pen_view button visible")
        actions = TouchAction(driver)

        window_size = driver.get_window_size()
        print("Window size: ", window_size)
        height = window_size["height"]
        print("Window Height :", height)
        width = window_size["width"]
        print("Window Width :", width)

        print("width / 2,height / 2 : ", width / 2, height / 2, "width / 2,height / 3 : ", width / 2, height / 3)
        # try:
        #     actions.press(int(width / 2),int(height / 2)).move_to(int(width / 2),int(height / 3)).release().perform()
        #     print("Worked int part")
        # except Exception as e:
        # actions.press(id(width / 2), id(height / 2)).move_to(id(width / 2), id(height / 3)).release().perform()
        actions.press(512, 300).move_to(512, 200).release().perform()
        print("Worked id part")
    except Exception as e:
        print("error : ", e)
        raise AssertionError("xpath not found")


def erase_written_text(device):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["eraser"]["xpath"]))
        ).click()
        print("Clicked on eraser button")
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["eraser_view"]["xpath"]))
        )
        print("eraser_view button visible")
        actions = TouchAction(driver)
        window_size = driver.get_window_size()
        print("Window size: ", window_size)
        height = window_size["height"]
        print("Window Height :", height)
        width = window_size["width"]
        print("Window Width :", width)
        actions.tap(width / 2, height / 2)
    except Exception as e:
        raise AssertionError("xpath not found")


def verify_text_editing(device, text):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["add_text"]["xpath"]))
        ).click()
        print("Clicked on add_text button")
        elem = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["empty_text_selected"]["xpath"]))
        )
        print("text : ", text)
        time.sleep(display_time)
        elem.send_keys(text)
        try:
            driver.hide_keyboard()
            print("Hide keyboard")
        except Exception as e:
            print("Cannot hide keyboard : ", e)
        time.sleep(display_time)
        search_result_xpath = (calendar_dict["text_xpath"]["xpath"]).replace("text_msg", text)
        print("Search result xpath : ", search_result_xpath)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((MobileBy.XPATH, search_result_xpath)))
        print("Written text is visible.")
    except Exception as e:
        raise AssertionError("xpath not found")


def delete_text_from_whiteboard_sharing(device, text):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    try:
        search_result_xpath = (calendar_dict["text_xpath"]["xpath"]).replace("text_msg", text)
        print("Search result xpath : ", search_result_xpath)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((MobileBy.XPATH, search_result_xpath))).click()
        print("Clicked on written text")
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["delete_text"]["xpath"]))
        ).click()
        print("Clicked on Delete button")
    except Exception as e:
        raise AssertionError("xpath not found")


def verify_yellow_sticky_note_editing(device, text):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["add_note"]["xpath"]))
        ).click()
        print("Clicked on add_note button button")
        elem = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["sticky_note_selected"]["xpath"]))
        )
        print("text : ", text)
        time.sleep(display_time)
        elem.send_keys(text)
        try:
            driver.hide_keyboard()
            print("Hide keyboard")
        except Exception as e:
            print("Cannot hide keyboard : ", e)
        time.sleep(display_time)
        search_result_xpath = (calendar_dict["text_xpath"]["xpath"]).replace("text_msg", text)
        print("Search result xpath : ", search_result_xpath)
        time.sleep(display_time)
        try:
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((MobileBy.XPATH, search_result_xpath)))
            print("Written text is visible.")
        except Exception as e:
            open_whiteboard_sharing_screen_from_notification(device)
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((MobileBy.XPATH, search_result_xpath)))
            print("Written text is visible.")
    except Exception as e:
        raise AssertionError("xpath not found")


def delete_yellow_sticky_note_from_whiteboard_sharing(device, text):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    try:
        search_result_xpath = (calendar_dict["text_xpath"]["xpath"]).replace("text_msg", text)
        print("Search result xpath : ", search_result_xpath)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((MobileBy.XPATH, search_result_xpath))).click()
        print("Clicked on written text")
        time.sleep(display_time)
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["delete_text"]["xpath"]))
        ).click()
        print("Clicked on Delete button")
    except Exception as e:
        raise AssertionError("xpath not found")


def verify_whiteboard_is_being_shared_notification(device):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["whiteboard_is_being_shared_text"]["xpath"]))
        )
        print("'whiteboard is being shared' notification Visible")
    except Exception as e:
        raise AssertionError("xpath not found")


def open_whiteboard_sharing_screen_from_notification(device):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, calendar_dict["open_whiteboard_shared_screen"]["id"]))
        ).click()
        print("Clicked on OPEN button to open Whiteboard shared screen")
    except Exception as e:
        raise AssertionError("xpath not found")


def stop_sharing_whiteboard_from_notification(device):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, calendar_dict["stop_share_whiteboard_shared_screen"]["id"]))
        ).click()
        print("Clicked on STOP Sharing button to stop Whiteboard shared screen")
    except Exception as e:
        raise AssertionError("xpath not found")


def stop_whiteboard_sharing_from_more_option(device):
    print("device ", device)
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((MobileBy.ID, calls_dict["Hang_up_button"]["id"])))
        print("Call control visible")
    except Exception as e:
        settings_keywords.click_device_center_point(device)
        print("Clicked on center point")

    elem = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((MobileBy.ID, calls_dict["call_more_options"]["id"]))
    )
    elem.click()
    print("Clicked on call more option")
    time.sleep(display_time)
    try:
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["stop_sharing_whiteboard"]["xpath"]))
        ).click()
        print("Clicked on stop_sharing_whiteboard button")
    except Exception as e:
        raise AssertionError("xpath not found")


def mutes_the_meeting_from_whiteboard_sharing_screen(device):
    print("Mutes the meeting : ", device)
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((MobileBy.ID, calls_dict["mute"]["id"]))).click()
        print("Clicked on Mute button from Whiteboard sharing screen")
    except Exception as e:
        raise AssertionError("xpath not found")


def verify_settings_option_on_whiteboard(device):
    print("Mutes the meeting : ", device)
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["settings_button"]["xpath"]))
        ).click()
        print("Clicked on Settings button on Whiteboard sharing screen")
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["export_button"]["xpath"]))
        )
        print("export_button visible")
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["about_button"]["xpath"]))
        )
        print("about_button visible")
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["help_button"]["xpath"]))
        )
        print("help_button visible")
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["send_feedback_button"]["xpath"]))
        )
        print("send_feedback_button visible")
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["close_panel"]["xpath"]))
        ).click()
        print("Clicked on Settings close panel button on Whiteboard sharing screen")
    except Exception as e:
        raise AssertionError("xpath not found")


def verify_text_from_whiteboard_sharing(device, text):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    try:
        search_result_xpath = (calendar_dict["text_xpath"]["xpath"]).replace("text_msg", text)
        print("Search result xpath : ", search_result_xpath)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((MobileBy.XPATH, search_result_xpath)))
        print(text, " text visible")
    except TimeoutException as e:
        raise AssertionError("xpath not found")


def verify_reaction_button_in_call_control(device):
    print("device :", device)
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    # wait for sometime for reactions to load
    time.sleep(5)
    if not common.click_if_present(device, calendar_dict, "call_control_reactions_button"):
        common.wait_for_and_click(device, calls_dict, "call_more_options")
    common.wait_for_element(device, calendar_dict, "icon_like")
    # dismiss any "call_more_options" pop-up
    common.wait_for_and_click(device, calendar_dict, "icon_like")


def tap_on_reaction_button_in_call_control(device):
    print("device :", device)
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    if not common.click_if_present(device, calendar_dict, "call_control_reactions_button"):
        common.wait_for_and_click(device, calls_dict, "call_more_options")
    common.wait_for_element(device, calendar_dict, "icon_applause")
    # dismiss any "call_more_options" pop-up
    common.wait_for_and_click(device, calendar_dict, "icon_applause")


def verify_presence_of_reactions_button_in_call_control(device):
    print("device :", device)
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    if not common.click_if_present(device, calendar_dict, "call_control_reactions_button"):
        common.wait_for_and_click(device, calls_dict, "call_more_options")
    common.wait_for_element(device, calendar_dict, "icon_like")
    common.wait_for_element(device, calendar_dict, "icon_heart")
    common.wait_for_element(device, calendar_dict, "icon_applause")
    common.wait_for_element(device, calendar_dict, "icon_laugh")
    common.wait_for_element(device, calendar_dict, "icon_surprised")
    common.wait_for_element(device, calendar_dict, "raise_hand")
    # dismiss any "call_more_options" pop-up
    common.wait_for_and_click(device, calendar_dict, "icon_like")


def verify_raise_hand_reaction(device):
    print("device :", device)
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    if not common.click_if_present(device, calendar_dict, "call_control_reactions_button"):
        common.wait_for_and_click(device, calls_dict, "call_more_options")
    common.wait_for_element(device, calendar_dict, "raise_hand")
    if "console" in device:
        tr_console_settings_keywords.tap_on_device_center_point(device)
    # dismiss any "call_more_options" pop-up
    else:
        settings_keywords.click_device_center_point(device)


def tap_on_like_button(device):
    print("device :", device)
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    if not common.click_if_present(device, calendar_dict, "call_control_reactions_button"):
        common.wait_for_and_click(device, calls_dict, "call_more_options")
    common.wait_for_and_click(device, calendar_dict, "icon_like")


def verify_like_button_after_tap_on_it(device):
    common.wait_for_element(device, calendar_dict, "reaction")


def verify_reaction_on_screen(device):
    common.wait_for_element(device, calendar_dict, "reaction")


def meeting_exist_or_not(device, meeting_name):
    print("device :", device)
    scroll_for_meeting_visibility(device, meeting=meeting_name)
    list_of_meeting_titles = common.get_all_elements_texts(device, calendar_dict, "meeting_title_name")
    print("List of Meeting titles:", list_of_meeting_titles)
    if meeting_name in list_of_meeting_titles:
        return True
    return False


def verify_manage_audio_and_video_option(device, count, role):
    if role not in ["organiser", "presenter", "attendee"]:
        raise AssertionError(f"Unexpected value for role : {role}")
    if count not in ["1", "2", "3"]:
        raise AssertionError(f"Unexpected value for count : {count}")
    if role.lower() == "organiser" or role.lower() == "presenter":
        navigate_to_add_participant_page(device)
        common.wait_for_element(device, calendar_dict, "manage_audio_and_video")
    elif role.lower() == "attendee":
        add_participants_button_not_present_for_attendee(device)
        if common.is_element_present(device, calendar_dict, "manage_audio_and_video"):
            raise AssertionError(f"{device} : Manage audio and video option is available for attendee")
    in_meeting_text = common.wait_for_element(device, calendar_dict, "Call_roster_header_text").text
    if not in_meeting_text == f"In the meeting ({count})":
        raise AssertionError(f"{device} : Meeting participant list is not displayed properly")
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")


def verify_options_to_manage_audio_and_video(device):
    navigate_to_add_participant_page(device)
    common.wait_for_and_click(device, calendar_dict, "manage_audio_and_video")
    common.wait_for_element(device, calendar_dict, "disable_mic_for_attendees")
    common.wait_for_element(device, calendar_dict, "disable_camera_for_attendees")
    common.wait_for_element(device, calendar_dict, "audio_toggle_button")
    toggle_btn = common.wait_for_element(device, calendar_dict, "audio_toggle_button")
    toggle_status = toggle_btn.get_attribute("checked")
    if not toggle_status.lower() == "false":
        raise AssertionError(f"{device} : Audio toggle button is not disabled by default: {toggle_status}")
    common.wait_for_element(device, calendar_dict, "video_toggle_button")
    toggle_btn = common.wait_for_element(device, calendar_dict, "video_toggle_button")
    toggle_status = toggle_btn.get_attribute("checked")
    if not toggle_status.lower() == "false":
        raise AssertionError(f"{device} : Video toggle button is not disabled by default: {toggle_status}")
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")


def disable_camera_and_mic_for_attendees(from_device, to_device, mic, camera):
    if mic.lower() not in ["on", "off"] or camera.lower() not in ["on", "off"]:
        raise AssertionError(f"Unexpected state for mic: {mic} , camera: {camera}")

    navigate_to_add_participant_page(from_device)

    if common.is_norden(from_device):
        common.wait_for_and_click(from_device, tr_calls_dict, "participant_more_option")
    common.wait_for_and_click(from_device, calendar_dict, "manage_audio_and_video")
    if mic.lower() == "off":
        toggle_text = common.wait_for_element(from_device, calendar_dict, "audio_toggle_button").text
        if not toggle_text.lower() == "off":
            raise AssertionError(f"{from_device} : Audio toggle button is not disabled by default")
        common.wait_for_and_click(from_device, calendar_dict, "audio_toggle_button")
        if common.is_norden(from_device):
            verify_attendee_mic_and_camera_status(to_device, "disabled")
    elif camera.lower() == "off":
        toggle_text = common.wait_for_element(from_device, calendar_dict, "video_toggle_button").text
        if not toggle_text.lower() == "off":
            raise AssertionError(f"{from_device} : Video toggle button is not disabled by default")
        common.wait_for_and_click(from_device, calendar_dict, "video_toggle_button")
    if common.is_norden(from_device):
        common.wait_for_and_click(from_device, tr_calls_dict, "participant_settings_back_btn")
        common.wait_for_and_click(from_device, tr_calls_dict, "close_roaster_button")
    else:
        common.wait_for_and_click(from_device, calls_dict, "Call_Back_Button")
        common.wait_for_and_click(from_device, calls_dict, "Call_Back_Button")


def verify_attendee_mic_and_camera_status(device, mic):
    if mic.lower() not in ["enabled", "disabled"]:
        raise AssertionError(f"Unexpected value for mic: {mic}")
    if mic.lower() == "disabled":
        for attempt in range(5):
            if common.is_element_present(device, calendar_dict, "your_mic_has_been_disabled"):
                print(f"found disabled mic xpath on attempt {attempt + 1} of 5")
                common.wait_for_element(device, calendar_dict, "disabled_mic")
                return
        raise AssertionError(f"Couldn't find the disabled mic xpath on {device}")
    if mic.lower() == "enabled":
        for attempt in range(5):
            if common.is_element_present(device, calendar_dict, "you_can_now_unmute_mic"):
                print(f"found your mic has been enbaled xpath on attempt {attempt} of 5")
                common.wait_for_element(device, calls_dict, "mic_button_muted")
                return
        raise AssertionError(f"Couldn't find the enabled mic xpath on {device}")


def verify_and_allow_individual_permissions_to_attendees(from_device, to_device):
    print("from_device :", from_device)
    print("to_device :", to_device)
    if ":" in to_device:
        user = to_device.split(":")[1]
        print("User account : ", user)
        account = None
        if user.lower() == "meeting_user":
            account = "meeting_user"
    else:
        account = "user"
    print("Account :", account)
    to_device = to_device.split(":")[0]

    navigate_to_add_participant_page(from_device)

    temp_dict = common.get_dict_copy(
        calendar_dict, "add_user", "user_name", config["devices"][to_device][account]["displayname"]
    )
    common.wait_for_and_click(from_device, temp_dict, "add_user")
    time.sleep(action_time)
    if not common.is_element_present(from_device, calendar_dict, "allow_mic"):
        common.wait_for_element(from_device, calendar_dict, "disabled_mic")
    common.wait_for_element(from_device, calendar_dict, "Pin")
    common.wait_for_element(from_device, calendar_dict, "make_a_presenter")
    common.wait_for_element(from_device, calendar_dict, "remove_from_meeting")
    common.wait_for_element(from_device, calendar_dict, "view_profile")
    if common.is_element_present(from_device, calendar_dict, "disabled_mic"):
        common.wait_for_and_click(from_device, calendar_dict, "disabled_mic")
        common.wait_for_element(to_device, calendar_dict, "your_mic_is_disabled")
        common.wait_for_and_click(from_device, temp_dict, "add_user")
        common.wait_for_and_click(from_device, calendar_dict, "allow_mic")
    else:
        common.wait_for_and_click(from_device, calendar_dict, "allow_mic")
    verify_attendee_mic_and_camera_status(to_device, "enabled")
    common.wait_for_and_click(from_device, calls_dict, "Call_Back_Button")


def make_an_spotlight(from_device, to_device):
    print("from_device :", from_device)
    print("to_device :", to_device)
    account = "user"
    if ":" in to_device:
        user = to_device.split(":")[1]
        print("User account : ", user)
        if user.lower() == "meeting_user":
            account = "meeting_user"
    print("Account :", account)
    to_device = to_device.split(":")[0]

    navigate_to_add_participant_page(from_device)

    temp_dict = common.get_dict_copy(
        calendar_dict, "add_user", "user_name", config["devices"][to_device][account]["displayname"]
    )
    common.wait_for_and_click(from_device, temp_dict, "add_user", "xpath")
    common.wait_for_and_click(from_device, calendar_dict, "spotlight_for_everyone")
    common.wait_for_and_click(from_device, calendar_dict, "spotlight")
    common.wait_for_and_click(from_device, common_dict, "back")


def verify_you_are_joined_as_an_attendee_notification(device):
    print("device :", device)
    common.wait_for_element(device, calendar_dict, "you_are_joined_as_an_attendee")


def verify_no_option_to_change_organizer_role(from_device, to_device):
    print("from_device :", from_device)
    print("to_device :", to_device)
    account = "user"
    if ":" in to_device:
        user = to_device.split(":")[1]
        print("User account : ", user)
        if user.lower() == "meeting_user":
            account = "meeting_user"
    print("Account :", account)
    to_device = to_device.split(":")[0]

    navigate_to_add_participant_page(from_device)

    temp_dict = common.get_dict_copy(
        calendar_dict, "add_user", "user_name", config["devices"][to_device][account]["displayname"]
    )
    common.wait_for_and_click(from_device, temp_dict, "add_user", "xpath")
    if common.is_element_present(from_device, calendar_dict, "make_an_attendee"):
        raise AssertionError(f"{to_device} : has option to change the organizer role")
    settings_keywords.click_device_center_point(from_device)
    common.wait_for_and_click(from_device, calendar_dict, "back")


def verify_user_role_in_a_meeting(device, role):
    if role.lower() not in ["Organizer", "Presenter", "Attendee"]:
        print(f"Unexpected value for role: {role}")

    navigate_to_add_participant_page(device)

    role_text = common.wait_for_element(device, calendar_dict, "current_role_tag").text.lower()
    print("Current role is : ", role_text)
    if role.lower() != role_text:
        raise AssertionError(f"expected role : {role} doesn't match the present role: {role_text}")
    common.wait_for_and_click(device, common_dict, "back")


def verify_presenter_options_in_meeting_from_attendee(from_device, to_device):
    print("from_device :", from_device)
    print("to_device :", to_device)
    account = "user"
    if ":" in to_device:
        user = to_device.split(":")[1]
        print("User account : ", user)
        if user.lower() == "meeting_user":
            account = "meeting_user"
    print("Account :", account)
    to_device = to_device.split(":")[0]

    navigate_to_add_participant_page(from_device)

    temp_dict = common.get_dict_copy(
        calendar_dict, "add_user", "user_name", config["devices"][to_device][account]["displayname"]
    )
    common.wait_for_and_click(from_device, temp_dict, "add_user", "xpath")
    common.wait_for_element(from_device, calendar_dict, "pin_for_me")
    common.wait_for_element(from_device, calendar_dict, "view_profile")
    settings_keywords.click_device_center_point(from_device)
    common.wait_for_and_click(from_device, common_dict, "back")


def verify_presenter_options_in_meeting_from_organizer_or_presenter(
    from_device, to_device, check_presenter_options_from_presenter="off"
):
    if check_presenter_options_from_presenter.lower() not in ["on", "off"]:
        raise AssertionError(f"Illegal value for 'presenter': '{check_presenter_options_from_presenter}'")
    print("from_device :", from_device)
    print("to_device :", to_device)
    account = "user"
    if ":" in to_device:
        user = to_device.split(":")[1]
        print("User account : ", user)
        if user.lower() == "meeting_user":
            account = "meeting_user"
    print("Account :", account)
    to_device = to_device.split(":")[0]

    navigate_to_add_participant_page(from_device)

    temp_dict = common.get_dict_copy(
        calendar_dict, "add_user", "user_name", config["devices"][to_device][account]["displayname"]
    )
    common.wait_for_and_click(from_device, temp_dict, "add_user", "xpath")
    common.wait_for_element(from_device, calendar_dict, "spotlight_for_everyone")
    common.wait_for_element(from_device, calendar_dict, "pin_for_me")
    if check_presenter_options_from_presenter == "off":
        if not common.is_element_present(from_device, calendar_dict, "make_an_attendee"):
            common.wait_for_element(from_device, calendar_dict, "make_an_presenter")
            common.wait_for_element(from_device, calendar_dict, "remove_from_meeting")
    if check_presenter_options_from_presenter == "on":
        common.wait_for_element(from_device, calendar_dict, "raise_hand")
    common.wait_for_element(from_device, calendar_dict, "view_profile")
    settings_keywords.click_device_center_point(from_device)
    common.wait_for_and_click(from_device, common_dict, "back")


def get_list_of_scheduled_meetings_on_cnf_device(device):
    print("device :", device)
    time.sleep(action_time)
    meeting_list = []
    meeting_name = common.wait_for_element(
        device, calendar_dict, "meeting_title_name", cond=EC.presence_of_all_elements_located
    )
    print(meeting_name)
    for result in meeting_name:
        meeting_list.append(str(result.text))
    print("List of scheduled meetings is : ", meeting_list)


def edit_the_meeting_name(device, new_meeting):
    driver = obj.device_store.get(alias=device)
    common.wait_for_and_click(device, calendar_dict, "edit_btn")
    element = common.wait_for_element(device, calendar_dict, "new_meeting_edit")
    element.clear()
    element.send_keys(new_meeting)
    driver.execute_script("mobile: performEditorAction", {"action": "done"})
    new_meeting_title = common.wait_for_element(device, calendar_dict, "new_meeting_edit").text
    print("New Meeting Name is :", new_meeting_title)
    if new_meeting_title != new_meeting:
        raise AssertionError("Meeting Name that has Changed is different")
    print(f"{device}: Meeting Name that has changed is Same")


def verify_mic_in_meet_now_prejoin_screen(device, mic):
    if mic.lower() not in ["disable", "enable"]:
        raise AssertionError(f"Unexpected value for mic: {mic}")
    common.wait_for_element(device, calendar_dict, "call_control_mute")
    if mic.lower() == "enable":
        common.wait_for_and_click(device, calls_dict, "mic_button_muted")
    if mic.lower() == "disable":
        common.wait_for_and_click(device, calls_dict, "mic_button_unmuted")


def verify_speaker_in_meet_now_prejoin_screen(device, speaker):
    if speaker.lower() not in ["enable", "disable"]:
        raise AssertionError(f"Unexpected value for speaker: {speaker}")
    common.wait_for_and_click(device, calendar_dict, "call_control_speaker")
    if speaker.lower() == "disable":
        common.wait_for_and_click(device, calendar_dict, "audio_off")
    if speaker.lower() == "enable":
        common.wait_for_and_click(device, calendar_dict, "speaker")


def verify_default_mic_and_speaker_state_in_meet_now_prejoin_screen(device):
    common.wait_for_element(device, calls_dict, "mic_button_muted")
    common.wait_for_element(device, calendar_dict, "call_control_speaker")


def verify_spotlight_text(device, text):
    if text.lower() not in ["spotlight", "remove spotlight"]:
        raise AssertionError(f"Unexpected value for text: {text}")
    if text == "spotlight":
        common.wait_for_element(device, calendar_dict, "you_are_spotlighted")
    if text == "remove spotlight":
        common.wait_for_element(device, calendar_dict, "you_are_no_longer_spotlighted")


def verify_spotlight_icon_for_user(device):
    navigate_to_add_participant_page(device)
    common.wait_for_element(device, calendar_dict, "participant_spotlight")
    common.wait_for_and_click(device, common_dict, "back")


def verify_no_spotlight_icon_for_user_in_add_participant_page(device):
    navigate_to_add_participant_page(device)
    if common.is_element_present(device, calendar_dict, "participant_spotlight"):
        raise AssertionError(f"{device} : is having spotlight icon")


def remove_spotlight(from_device, to_device, action="click"):
    if not action.lower() in ["click", "verify"]:
        raise AssertionError(f"Illegal option specified: '{action}'")
    print("from_device :", from_device)
    print("to_device :", to_device)
    account = "user"
    if ":" in to_device:
        user = to_device.split(":")[1]
        print("User account : ", user)
        if user.lower() == "meeting_user":
            account = "meeting_user"
    print("Account :", account)
    to_device = to_device.split(":")[0]

    navigate_to_add_participant_page(from_device)

    temp_dict = common.get_dict_copy(
        calendar_dict, "add_user", "user_name", config["devices"][to_device][account]["displayname"]
    )
    common.wait_for_and_click(from_device, temp_dict, "add_user", "xpath")
    if action.lower() == "verify":
        common.wait_for_element(from_device, calendar_dict, "stop_spotlight")
        common.wait_for_and_click(from_device, calendar_dict, "touch_outside")
    else:
        common.wait_for_and_click(from_device, calendar_dict, "stop_spotlight")
        common.wait_for_and_click(from_device, calendar_dict, "stop_spotlight_ok_btn")

    common.wait_for_and_click(from_device, common_dict, "back")


def verify_spotlight_avatar(device_list):
    devices = device_list.split(",")
    print("Devices : ", devices)
    for device in devices:
        print("device : ", device)
        if not common.is_element_present(device, calendar_dict, "spotlight_avatar"):
            common.wait_for_and_click(device, calendar_dict, "call_more_options")
            common.wait_for_and_click(device, calendar_dict, "full_meeting_experience")
            common.wait_for_element(device, calendar_dict, "spotlight_avatar")


def make_an_pin(from_device, to_device):
    print("from_device :", from_device)
    print("to_device :", to_device)
    account = "user"
    if ":" in to_device:
        user = to_device.split(":")[1]
        print("User account : ", user)
        if user.lower() == "meeting_user":
            account = "meeting_user"
    print("Account :", account)
    to_device = to_device.split(":")[0]

    navigate_to_add_participant_page(from_device)

    temp_dict = common.get_dict_copy(
        calendar_dict, "add_user", "user_name", config["devices"][to_device][account]["displayname"]
    )
    common.wait_for_and_click(from_device, temp_dict, "add_user", "xpath")
    common.wait_for_and_click(from_device, calendar_dict, "pin_for_me")
    common.wait_for_and_click(from_device, common_dict, "back")


def verify_remove_spotlight_option(from_device, to_device):
    user_name = common.device_displayname(to_device)

    navigate_to_add_participant_page(from_device)

    temp_dict = common.get_dict_copy(calendar_dict, "add_user", "user_name", user_name)
    common.wait_for_and_click(from_device, temp_dict, "add_user", "xpath")
    common.wait_for_element(from_device, calendar_dict, "stop_spotlight")
    call_keywords.dismiss_call_more_options(from_device)
    common.wait_for_and_click(from_device, common_dict, "back")


def verify_participant_name_which_is_pinned_in_main_stage(device_list):
    devices = device_list.split(",")
    for device in devices:
        print("devices : ", device)
        common.wait_for_and_click(device, calendar_dict, "call_more_options")
        if not common.click_if_present(device, calendar_dict, "full_meeting_experience"):
            common.wait_for_and_click(device, calendar_dict, "touch_outside")
        common.wait_for_element(device, calendar_dict, "profile_view")


def verify_participant_name_which_is_spotlighted_in_main_stage(device_list):
    devices = device_list.split(",")
    for device in devices:
        print("devices : ", device)
        common.wait_for_and_click(device, calendar_dict, "call_more_options")
        if not common.click_if_present(device, calendar_dict, "full_meeting_experience"):
            common.wait_for_and_click(device, calendar_dict, "touch_outside")
        common.wait_for_element(device, calendar_dict, "profile_view")


def verify_spotlighted_participant_can_not_pin_from_other_participant(from_device, to_device):
    print("from_device :", from_device)
    print("to_device :", to_device)
    account = "user"
    if ":" in to_device:
        user = to_device.split(":")[1]
        print("User account : ", user)
        if user.lower() == "meeting_user":
            account = "meeting_user"
    print("Account :", account)
    to_device = to_device.split(":")[0]

    navigate_to_add_participant_page(from_device)

    temp_dict = common.get_dict_copy(
        calendar_dict, "add_user", "user_name", config["devices"][to_device][account]["displayname"]
    )
    common.wait_for_and_click(from_device, temp_dict, "add_user", "xpath")
    common.wait_for_and_click(from_device, calendar_dict, "pin_for_me")
    common.wait_for_element(from_device, calendar_dict, "can_not_pin_for_me")
    common.wait_for_and_click(from_device, calendar_dict, "can_not_pin_for_me_ok_button")
    common.wait_for_and_click(from_device, common_dict, "back")


def tap_to_return_to_meeting(device, action="click"):
    if action.lower() not in ["click", "verify"]:
        raise AssertionError(f"Illegal value for 'action': '{action}'")
    if action.lower() == "verify":
        common.wait_for_element(device, calls_dict, "call_bar")
    else:
        common.wait_for_and_click(device, calls_dict, "call_bar")


def check_display_when_clicked_on_spotlight_icon(device):
    common.wait_for_and_click(device, calendar_dict, "call_more_options")
    common.wait_for_and_click(device, calendar_dict, "full_meeting_experience")
    common.wait_for_and_click(device, calendar_dict, "spotlight_avatar")
    if common.is_element_present(device, calendar_dict, "stop_spotlight_ok_btn"):
        raise AssertionError(f"{device} have spotlight disable option")


def verify_user_not_having_spotlight_avatar_option(device):
    if common.is_element_present(device, calendar_dict, "spotlight_avatar"):
        raise AssertionError(f"{device} have spotlight option enabled")


def join_meeting_from_tap_to_return_banner(device):
    common.wait_for_and_click(device, calendar_dict, "return_meeting_banner")


def verify_and_join_meeting_when_show_meeting_title_toggle_is_off(
    device, organizer_name, meeting, all_day_meeting="off"
):
    organizer_username = config["devices"][organizer_name]["user"]["displayname"]
    print("organizer_username:", organizer_username)
    if config["devices"][device]["model"].lower() in ["tacoma", "berkely", "manhattan"]:
        refresh_cnf_device_for_meeting_visibility(device)
    else:
        call_keywords.come_back_to_home_screen(device)
        navigate_to_calendar_tab(device)
        settings_keywords.refresh_main_tab(device)
    temp_dict = common.get_dict_copy(calendar_dict, "add_user", "user_name", organizer_username)
    if not all_day_meeting == "off":
        common.wait_for_and_click(device, calendar_dict, "meeting_day_name")
    if not common.is_element_present(device, temp_dict, "add_user"):
        _max_attempts = 5
        for _attempt in range(_max_attempts):
            if common.is_element_present(device, temp_dict, "add_user"):
                print(f"{device}: After scrolling {_attempt} meeting title founded")
                break
            else:
                scroll_only_once(device)
    common.wait_for_and_click(device, temp_dict, "add_user", "xpath")
    tmp_dict = common.get_dict_copy(
        calendar_dict, "meeting_title_in_meeting_join_screen", "meeting_name_replace", meeting
    )
    time.sleep(display_time)
    if not common.click_if_present(device, calendar_dict, "join_button"):
        common.wait_for_and_click(device, calendar_dict, "meeting_list_item_join_button")
    common.wait_for_element(device, tmp_dict, "meeting_title_in_meeting_join_screen")
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    common.wait_for_element(device, calendar_dict, "meeting_name_on_meeting_screen")
    ele1 = common.get_all_elements_texts(device, calendar_dict, "meeting_name_on_meeting_screen")
    print(ele1)
    if ele1[0].lower() != meeting:
        raise AssertionError("meeting title not founded on meeting screen")


def clear_all_day_meeting_and_meeting_history_from_calendar(devices):
    device_list = devices.split(",")
    _max_attempts = 8
    for device in device_list:
        navigate_to_calendar_tab(device)
        settings_keywords.refresh_main_tab(device)
        if common.is_element_present(device, calendar_dict, "no_meetings_calendar_tab"):
            continue
        for _attempt in range(_max_attempts):
            time.sleep(action_time)
            if common.is_element_present(device, calendar_dict, "no_meetings_calendar_tab"):
                print("all meetings are removed")
                break
            if common.click_if_present(device, calendar_dict, "meeting_day_name", "command"):
                time.sleep(2)
                settings_keywords.refresh_main_tab(device)
                common.click_if_present(device, calendar_dict, "meeting_day_name", "command")
            if common.click_if_present(device, calendar_dict, "meeting_list"):
                time.sleep(action_time)
            if not common.click_if_present(device, calendar_dict, "remove_from_calender"):
                swipe_till_cancel_event(device)
            if common.is_element_present(device, calendar_dict, "Cancel_event"):
                common.wait_for_and_click(device, calendar_dict, "Cancel_event")
                common.wait_for_and_click(device, calendar_dict, "Cancel_event_OK")
            elif common.is_element_present(device, calendar_dict, "delete_event"):
                common.wait_for_and_click(device, calendar_dict, "delete_event")
                common.wait_for_and_click(device, calendar_dict, "Cancel_event_OK")

        common.wait_for_element(device, calendar_dict, "no_meetings_calendar_tab")


def verify_meeting_name_after_meeting_canceled(device, organizer, meeting, show_meeting_toggle):
    navigate_to_calendar_tab(device)
    settings_keywords.refresh_main_tab(device)
    common.click_if_present(device, calendar_dict, "meeting_day_name")
    meeting_name = common.get_all_elements_texts(device, calendar_dict, "meeting_title_name")
    if show_meeting_toggle == "on":
        meeting_title = "Canceled: " + meeting
        if meeting_title not in meeting_name:
            raise AssertionError("meeting title not found")
    elif show_meeting_toggle == "off":
        organizer_username = config["devices"][organizer]["user"]["displayname"]
        if organizer_username not in meeting_name:
            raise AssertionError("meeting title not found")


def verify_meeting_title_shows_meeting_organizer_name(device, organizer, all_day_meeting="off"):
    if all_day_meeting.lower() not in ["on", "off"]:
        raise AssertionError(f"Illegal value for 'all_day_meeting_toggle': '{all_day_meeting}'")
    organizer_name = config["devices"][organizer]["user"]["displayname"]
    print("Organizer name is : ", organizer_name)
    navigate_to_calendar_tab(device)
    settings_keywords.refresh_main_tab(device)
    if not all_day_meeting == "off":
        common.wait_for_and_click(device, calendar_dict, "meeting_day_name")
    time.sleep(action_time)
    meeting_name = common.get_all_elements_texts(device, calendar_dict, "meeting_title_name")
    for title in meeting_name:
        if organizer_name not in title:
            raise AssertionError(f"{device}: Expected organizer name: {organizer_name}, but found: {title}")


def verify_cancelled_meetings_appearance_on_home_screen_for_cnf_device(device):
    print("device :", device)
    if common.is_portrait_mode_cnf_device(device):
        status = "fail"
    else:
        status = "pass"
    return status


def verify_mute_and_unmute_button_in_meet_now(device):
    # Verify unmuted call
    common.wait_for_element(device, calls_dict, "mic_button_unmuted")
    common.wait_for_and_click(device, calendar_dict, "meet_now_join_btn")
    common.wait_for_element(device, calls_dict, "call_verify_unmuted", wait_attempts=40)
    common.wait_for_and_click(device, calls_dict, "Hang_up_button")

    tap_on_meet_now_icon_and_validate(device)
    # Verify muted call
    common.wait_for_and_click(device, calls_dict, "mic_button_unmuted")
    common.wait_for_and_click(device, calendar_dict, "meet_now_join_btn")
    common.wait_for_element(device, calls_dict, "call_verify_muted", wait_attempts=40)
    common.wait_for_and_click(device, calls_dict, "Hang_up_button")
    common.wait_while_present(device, calls_dict, "Hang_up_button")


def verify_join_meeting_screen_after_end_meeting(device, meeting):
    time.sleep(display_time)
    if common.is_element_present(device, calls_dict, "Hang_up_button"):
        raise AssertionError(f"{device}: Meeting is still on-going")
    common.wait_for_element(device, calendar_dict, "join_button")
    meeting_title = common.wait_for_element(device, calendar_dict, "meeting_title").text
    if not meeting_title == meeting:
        raise AssertionError(f"{device}: Expected meeting title: {meeting}, but found: {meeting_title}")


def verify_meeting_screen_after_click_back_button(device, meeting):
    verify_join_meeting_screen_after_end_meeting(device, meeting)
    common.wait_for_and_click(device, calls_dict, "call_bar")


def select_custom_time_while_creating_meeting(
    device,
    meeting_duration,
    start_meeting_time,
    start_meeting_time_after,
    consecutive_meeting,
    current_meeting_end_time=None,
):
    # when we need to create the new consecutive meeting
    # we are providing the current_meeting_end_time for creating consecutive meeting
    if consecutive_meeting == "on":
        time_val = current_meeting_end_time.strip()
        print(f"current_meeting_end_time is :{current_meeting_end_time} and {type(current_meeting_end_time)}")
    else:
        time_val = common.wait_for_element(device, tr_calendar_dict, "current_time").text
        print(f"current_time is :{time_val}")
    start_time, current_time_convention = time_val.split()
    print(f"start_time is :{start_time}")
    print(f"current_time_convention is :{current_time_convention}")

    # If start_meeting_time is on and if consecutive_meeting is off
    # we are calculating the start_time for creating meeting in future
    if start_meeting_time == "on" and consecutive_meeting == "off":
        start_time = datetime.strptime(start_time, "%I:%M") + timedelta(minutes=start_meeting_time_after)
        start_time = start_time.strftime("%I:%M").lstrip("0")

    # else it will take current time as start time of the meeting
    start_hours, start_minutes = map(int, start_time.split(":"))
    print(f"{device}: START Hour:{start_hours} and Start minutes:{start_minutes}")
    meeting_start_time = common.wait_for_element(device, tr_calendar_dict, "start_time").text
    common.wait_for_and_click(device, tr_calendar_dict, "start_time")
    common.wait_for_and_click(device, tr_calendar_dict, "toogle_btn")
    # if time convention are different we are adjusting it
    if meeting_start_time.split()[1] != current_time_convention:
        change_time_convention_for_meeting_time(device, current_time_convention)
    hour_input = common.wait_for_element(device, tr_calendar_dict, "hour_text_box", "id")
    hour_input.clear()
    hour_input.send_keys(start_hours)
    min_input = common.wait_for_element(device, tr_calendar_dict, "min_text_box", "id")
    min_input.clear()
    min_input.send_keys(start_minutes)
    common.wait_for_and_click(device, calendar_dict, "ok_button")

    end_time = datetime.strptime(start_time, "%I:%M") + timedelta(minutes=meeting_duration)
    end_time = end_time.strftime("%I:%M").lstrip("0")
    end_hours, end_minutes = map(int, end_time.split(":"))
    print(f"{device}: END Hour:{end_hours} and End minutes:{end_minutes}")

    common.wait_for_and_click(device, tr_calendar_dict, "end_time")
    common.wait_for_and_click(device, tr_calendar_dict, "toogle_btn")

    # The 'hour_input'/'min_text_box' elements are stale, refresh them:
    hour_input = common.wait_for_element(device, tr_calendar_dict, "hour_text_box", "id")
    hour_input.clear()
    hour_input.send_keys(end_hours)
    min_input = common.wait_for_element(device, tr_calendar_dict, "min_text_box", "id")
    min_input.clear()
    min_input.set_value(end_minutes)
    if start_hours == 12 and end_hours == 1:
        change_time_convention_for_meeting_time(device, current_time_convention)
    common.wait_for_and_click(device, calendar_dict, "ok_button", "xpath")


def verify_meeting_after_organizer_cancel_event(device, meeting):
    common.wait_for_and_click(device, calendar_dict, "calendar_tab")
    tmp_dict = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", meeting)
    print("meeting_path : ", tmp_dict)
    time.sleep(action_time)
    if common.is_element_present(device, tmp_dict, "meeting"):
        raise AssertionError(f"{meeting}  not yet removed from calender tab")


def verify_meeting_name_and_join_meeting_from_home_screen(device, meeting):
    home_screen_keywords.verify_home_screen_tiles(device)
    time.sleep(action_time)
    if not common.is_element_present(device, home_screen_dict, "clear_notification"):
        common.wait_for_and_click(device, home_screen_dict, "calendar_tab")
        settings_keywords.refresh_main_tab(device)
        common.wait_for_and_click(device, home_screen_dict, "home_bar_icon")
    expected_meeting_name = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", meeting)
    common.wait_for_element(device, expected_meeting_name, "meeting")
    common.wait_for_and_click(device, home_screen_dict, "meeting_join_button")
    common.wait_for_element(device, calls_dict, "Decline_call_button")


def verify_lightweight_meeting_ui(device, participants):
    common.wait_for_element(device, calls_dict, "Decline_call_button")
    common.wait_for_element(device, calendar_dict, "call_control_reactions_button")
    common.wait_for_element(device, calendar_dict, "call_control_mute")
    common.wait_for_and_click(device, calendar_dict, "call_more_options")
    if config["devices"][device]["model"].lower() in ["tacoma", "manhattan", "sunnyvale", "berkely"]:
        print("Meeting user doesn't have start recording option")
    else:
        common.wait_for_element(device, calendar_dict, "start_recording")
    common.wait_for_element(device, calendar_dict, "turn_on_live_captions")
    common.wait_for_element(device, calendar_dict, "dial_pad")
    common.wait_for_element(device, calendar_dict, "full_meeting_experience")
    common.wait_for_element(device, calendar_dict, "switch_audio_route")
    call_keywords.dismiss_call_more_options(device)

    navigate_to_add_participant_page(device)
    # common.wait_for_and_click(device, calendar_dict, "meeting_call_ui_people")
    common.wait_for_element(device, calendar_dict, "add_people_to_meeting")
    common.wait_for_element(device, calendar_dict, "manage_audio_and_video")
    expected_participants_list = participants.split(",")
    time.sleep(action_time)
    actual_participants_list = common.get_all_elements_texts(device, calendar_dict, "participant_name_text_view")
    for to_device in expected_participants_list:
        display_name = common.device_displayname(to_device)
        if display_name not in actual_participants_list:
            raise AssertionError(
                f"Actual participants list: {actual_participants_list} doesn't match the expected participants list: {display_name}"
            )
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")
    common.wait_for_element(device, calls_dict, "Decline_call_button")


def verify_and_add_participant_to_conversation_by_ask_to_join_option_and_view_profile_option_in_meeting(
    from_device, to_device, option="ask_to_join"
):
    if option.lower() not in ["ask_to_join", "view_profile"]:
        raise AssertionError(f"Illegal value for 'option': '{option}'")
    common.wait_for_element(from_device, calls_dict, "Decline_call_button")
    navigate_to_add_participant_page(from_device)
    # common.wait_for_and_click(from_device, calendar_dict, "meeting_call_ui_people")
    display_name = common.device_displayname(to_device)
    temp_dict = common.get_dict_copy(calendar_dict, "add_user", "user_name", display_name)
    common.wait_for_and_click(from_device, temp_dict, "add_user")

    if option == "ask_to_join":
        common.wait_for_element(from_device, calls_dict, "view_profile_option")
        common.wait_for_and_click(from_device, calendar_dict, "ask_to_join")
        common.wait_for_element(to_device, calls_dict, "Accept_call_button")
    elif option == "view_profile":
        common.wait_for_element(from_device, calendar_dict, "ask_to_join")
        common.wait_for_and_click(from_device, calls_dict, "view_profile_option")
        common.wait_for_element(from_device, temp_dict, "add_user")
        user_name = common.device_username(to_device)
        temp_dict = common.get_dict_copy(calendar_dict, "add_user", "user_name", user_name)
        common.wait_for_element(from_device, temp_dict, "add_user")
        tap_to_return_to_meeting(from_device)


def switch_meeting_from_one_meeting_to_another_meeting(device, current_meeting, next_meeting):
    device, account = common.decode_device_spec(device)
    if account.lower() == "meeting_user":
        common.wait_for_element(device, calls_dict, "Decline_call_button")
        current_meeting_xpath = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", current_meeting)
        print("meeting_xpath : ", current_meeting_xpath)
        common.wait_for_element(device, current_meeting_xpath, "meeting")
        common.wait_for_and_click(device, calls_dict, "Call_Back_Button")
        next_meeting_xpath = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", next_meeting)
        print("meeting_xpath : ", next_meeting_xpath)
        scroll_for_meeting_visibility(device, meeting=next_meeting)
        expected_meeting_name = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", next_meeting)
        common.wait_for_element(device, expected_meeting_name, "meeting")
        name_list = []
        join_btn_list = common.wait_for_element(
            device,
            calendar_dict,
            "cnf_device_join_button_id",
            "id",
            cond=EC.presence_of_all_elements_located,
        )
        print(f"Length of join btn list : {join_btn_list}")
        meeting_names_list = common.wait_for_element(
            device, calendar_dict, "meeting_title_name", "id", cond=EC.presence_of_all_elements_located
        )
        print(f"Length of meeting names list : {meeting_names_list}")
        for meeting_name in meeting_names_list:
            if "Canceled:" not in meeting_name.text:
                name_list.append(meeting_name.text)
        print(f"Meetings displayed currently: {name_list}")
        for m in name_list:
            if m == next_meeting:
                m_pos = name_list.index(m)
                break
        join_btn_list[m_pos].click()
        print("Joined the expected meeting")
    else:
        common.wait_for_element(device, calls_dict, "Decline_call_button")
        current_meeting_xpath = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", current_meeting)
        print("meeting_xpath : ", current_meeting_xpath)
        common.wait_for_element(device, current_meeting_xpath, "meeting")
        common.wait_for_and_click(device, calls_dict, "Call_Back_Button")
        next_meeting_xpath = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", next_meeting)
        print("meeting_xpath : ", next_meeting_xpath)
        if common.is_portrait_mode_cnf_device(device):
            common.wait_for_and_click(device, calls_dict, "Call_Back_Button")
        scroll_for_meeting_visibility(device, meeting=next_meeting)
        common.wait_for_and_click(device, next_meeting_xpath, "meeting")
        time.sleep(action_time)
        common.wait_for_and_click(device, calendar_dict, "join_button")
        time.sleep(display_time)
        common.wait_for_element(device, calls_dict, "Decline_call_button")
        current_meeting_xpath = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", current_meeting)
        print("meeting_xpath : ", current_meeting_xpath)
        common.wait_for_element(device, current_meeting_xpath, "meeting")
        next_meeting_xpath = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", next_meeting)
        print("meeting_xpath : ", next_meeting_xpath)
        common.wait_for_element(device, next_meeting_xpath, "meeting")
    common.wait_for_element(device, calls_dict, "hold_label_time")
    common.wait_for_element(device, calls_dict, "Resume")
    common.wait_for_element(device, calls_dict, "end_button_in_hold_banner")


def end_meeting_from_hold_banner(device):
    common.wait_for_element(device, calls_dict, "hold_label_time")
    common.wait_for_and_click(device, calls_dict, "end_button_in_hold_banner")


def verify_meeting_title_in_hold_banner(device, meeting_1, meeting_2):
    common.wait_for_element(device, calls_dict, "Decline_call_button")
    meeting = common.get_all_elements_texts(device, calendar_dict, "meeting_name_on_meeting_screen")
    if not (meeting[0] == meeting_1 and meeting[1] == meeting_2):
        raise AssertionError(f"meeting name in hold banner not in expected position", meeting)


def verify_legacy_meeting_ui(device):
    common.wait_for_element(device, calls_dict, "Decline_call_button")
    common.wait_for_element(device, calendar_dict, "call_control_mute")
    if config["devices"][device]["model"].lower() in ["tacoma", "manhattan", "berkely"]:
        common.wait_for_and_click(device, calendar_dict, "call_more_options")
        common.wait_for_element(device, calendar_dict, "turn_on_live_captions")
        common.wait_for_element(device, calendar_dict, "dial_pad")
        common.wait_for_and_click(device, calendar_dict, "touch_outside")
        return
    common.wait_for_element(device, calendar_dict, "call_control_reactions_button")
    common.wait_for_and_click(device, calendar_dict, "call_more_options")
    common.wait_for_element(device, calendar_dict, "start_recording")
    common.wait_for_element(device, calendar_dict, "turn_on_live_captions")
    common.wait_for_element(device, calendar_dict, "dial_pad")
    common.wait_for_element(device, calendar_dict, "full_meeting_experience")
    common.wait_for_element(device, calendar_dict, "switch_audio_route")
    common.wait_for_and_click(device, calendar_dict, "touch_outside")


def verify_full_meeting_experience_option_in_meeting(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    common.wait_for_and_click(device, calls_dict, "call_more_options")
    common.wait_for_element(device, calendar_dict, "full_meeting_experience")
    common.wait_for_and_click(device, calendar_dict, "touch_outside")


def enable_or_disable_show_meeting_name_option(device, desired_state):
    show_meeting_name = common.wait_for_element(device, calendar_dict, "show_meeting_name_toggle")
    show_meeting_name_status = show_meeting_name.get_attribute("checked")
    print(f"call_forwarding_status :{show_meeting_name_status}")
    if desired_state == "ON":
        state = "true"
    elif desired_state == "OFF":
        state = "false"
    print(f"{device}: Set show_meeting_name toggle to '{desired_state}, state: {state}'")

    if show_meeting_name_status == state:
        print(f"{device}: Show meeting name is already '{desired_state}'")
    else:
        common.wait_for_and_click(device, calendar_dict, "show_meeting_name_toggle")
        show_meeting_name = common.wait_for_element(device, calendar_dict, "show_meeting_name_toggle")
        show_meeting_name_status = show_meeting_name.get_attribute("checked")
        if state != show_meeting_name_status:
            raise AssertionError(f"{device}: Unexpected state of show meeting name toggle")


def enable_or_disable_lightweight_meeting_experience(device, desired_state):
    lightweight_meeting_experience_toggle = common.wait_for_element(
        device, settings_dict, "Enable_lightweight_meeting_experience_toggle_btn"
    )
    lightweight_meeting_experience_toggle_status = lightweight_meeting_experience_toggle.get_attribute("checked")
    print(f"lightweight_meeting_experience_toggle_status :{lightweight_meeting_experience_toggle_status}")
    if desired_state == "ON":
        state = "true"
    elif desired_state == "OFF":
        state = "false"
    print(f"{device}: Set lightweight_meeting_experience_toggle to '{desired_state}, state: {state}'")

    if lightweight_meeting_experience_toggle_status == state:
        print(f"{device}: lightweight meeting experience toggle status is already '{desired_state}'")
    else:
        common.wait_for_and_click(device, settings_dict, "Enable_lightweight_meeting_experience_toggle_btn")
        lightweight_meeting_experience_toggle = common.wait_for_element(
            device, settings_dict, "Enable_lightweight_meeting_experience_toggle_btn"
        )
        lightweight_meeting_experience_toggle_status = lightweight_meeting_experience_toggle.get_attribute("checked")
        if state != lightweight_meeting_experience_toggle_status:
            raise AssertionError(f"{device}: Unexpected state of lightweight meeting experience toggle")


def verify_raised_hand_notification_on_another_user(device, from_device):
    account = "user"
    if ":" in device:
        user = device.split(":")[1]
        print("User account : ", user)
        if user.lower() == "meeting_user":
            account = "meeting_user"
    print("Account :", account)
    device = device.split(":")[0]
    print("device : ", device)
    user_name = config["devices"][device][account]["displayname"]
    reaction_msg = common.wait_for_element(from_device, tr_calendar_dict, "notification_text")
    reaction_msg = reaction_msg.text
    print(f"Recieved the notification : {reaction_msg}")
    name = re.findall("raised hand", reaction_msg)
    result = " ".join(str(i) for i in name)
    if reaction_msg != user_name + " " + result:
        raise AssertionError(f" Not got the {device} raised hand notification on the {from_device}")


def add_participants_button_not_present_for_attendee(device):
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    if not common.click_if_present(device, calls_dict, "participants_roster_button"):
        if not common.click_if_present(device, calls_dict, "Add_participants_button"):
            common.wait_for_and_click(device, calls_dict, "showRoster")
    if common.is_element_present(device, tr_calls_dict, "add_participants"):
        raise AssertionError(f"{device} add participants button is present")


def verify_reactions_options_not_present_in_call_more_options(device):
    common.wait_for_and_click(device, calls_dict, "call_more_options")
    time.sleep(action_time)
    if common.is_element_present(device, calendar_dict, "icon_like"):
        raise AssertionError(f"{device}: have reactions option in call more options")
    common.wait_for_and_click(device, calendar_dict, "touch_outside")


def verify_recording_notification_in_participant(from_device, to_device):
    display_name = common.device_displayname(to_device)
    meeting_notification_text = common.wait_for_element(from_device, calls_dict, "2nd_notification_text", "id").text
    expected_text = display_name + "started recording. Privacy Policy"
    if meeting_notification_text.lower().strip().replace(" ", "") != expected_text.lower().strip().replace(" ", ""):
        raise AssertionError(
            f"{display_name} started recording. Privacy Policy text not found: {meeting_notification_text}"
        )


def verify_and_lower_hand_for_attendee(from_device, to_device):
    common.wait_for_element(from_device, calls_dict, "Hang_up_button")
    navigate_to_add_participant_page(from_device)
    display_name = common.device_displayname(to_device)
    temp_dict = common.get_dict_copy(calendar_dict, "add_user", "user_name", display_name)
    common.wait_for_and_click(from_device, temp_dict, "add_user")
    if not common.is_element_present(from_device, calendar_dict, "allow_mic"):
        common.wait_for_element(from_device, calendar_dict, "disabled_mic")
    common.wait_for_element(from_device, calendar_dict, "Pin")
    common.wait_for_element(from_device, calendar_dict, "make_a_presenter")
    common.wait_for_element(from_device, calendar_dict, "remove_from_meeting")
    common.wait_for_element(from_device, calendar_dict, "view_profile")
    common.wait_for_and_click(from_device, calendar_dict, "lower_hand")
    common.wait_for_element(to_device, calendar_dict, "lower_hand_notification")
    common.wait_for_and_click(from_device, calls_dict, "Call_Back_Button")


def verify_lock_meeting_option_for_organizer(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    common.wait_for_and_click(device, calendar_dict, "call_more_options")
    common.wait_for_element(device, calendar_dict, "turn_on_live_captions")
    common.wait_for_element(device, calendar_dict, "lock_the_meeting")
    call_keywords.dismiss_call_more_options(device)


def verify_meetings_displayed_in_calendar_tab(device, meeting_list):
    expected_meetings_list = meeting_list.split(",")
    meeting_names_list = common.get_all_elements_texts(device, calendar_dict, "meeting_list")
    join_button_list = common.wait_for_element(
        device, calendar_dict, "meeting_list_item_join_button", cond=EC.presence_of_all_elements_located
    )
    meeting_time_list = common.get_all_elements_texts(device, calendar_dict, "meeting_time")
    meeting_location_list = common.get_all_elements_texts(device, calendar_dict, "meeting_location_details")
    print(f"Displayed meetings on {device}: {meeting_names_list}")
    for meeting in meeting_names_list:
        if meeting not in expected_meetings_list:
            raise AssertionError(f"{device}: Expected meeting is not displayed: {meeting}")
    if len(join_button_list) < len(meeting_list):
        raise AssertionError(
            f"{device}: One or more meetings is not displayed with join button: {len(join_button_list)}"
        )
    if len(meeting_time_list) < len(meeting_list):
        raise AssertionError(f"{device}: One or more meetings is not displayed with meeting time: {meeting_time_list}")
    if len(meeting_location_list) < len(meeting_list):
        raise AssertionError(
            f"{device}: One or more meetings is not displayed with meeting location: {meeting_location_list}"
        )


def verify_switch_audio_route_options_in_meeting_UI(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    common.wait_for_and_click(device, calendar_dict, "call_more_options")
    common.wait_for_and_click(device, calendar_dict, "switch_audio_route")
    common.wait_for_element(device, calendar_dict, "switch_audio_route_speaker")
    common.wait_for_and_click(device, calendar_dict, "switch_audio_route_audio_off")
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    common.wait_for_and_click(device, calendar_dict, "call_more_options")
    common.wait_for_and_click(device, calendar_dict, "switch_audio_route")
    common.wait_for_element(device, calendar_dict, "switch_audio_route_turn_audio_on")
    common.wait_for_and_click(device, calendar_dict, "switch_audio_route_turn_audio_on_yes")
    common.wait_for_and_click(device, calendar_dict, "switch_audio_route_speaker")
    common.wait_for_element(device, calls_dict, "Hang_up_button")


def verify_available_option_when_no_meetings_created_for_conf(device):
    if common.is_portrait_mode_cnf_device(device):
        navigate_to_calendar_tab(device)
        common.wait_for_element(device, navigation_dict, "Available")
    else:
        print(f"{device}: is a landscape device where 'available' option won't be present")


def scroll_down_device_setting_tab(device):
    driver = obj.device_store.get(alias=device)
    window_size = driver.get_window_size()
    print("Window size: ", window_size)
    height = window_size["height"]
    width = window_size["width"]
    print("Window Width and height :", width, height)
    if height > width:
        print(
            "width / 2, 4 * (height / 5), width / 2, height / 5 : ", width / 2, 4 * (height / 5), width / 2, height / 5
        )
        driver.swipe(width / 2, 4 * (height / 5), width / 2, height / 5)
        time.sleep(action_time)
        driver.swipe(width / 2, 4 * (height / 5), width / 2, height / 5)
    else:
        print(
            "(width / 4), 4 * (height / 5), (width / 4), height / 5 : ",
            (width / 4),
            height / 5,
            (width / 4),
            4 * (height / 5),
        )
        driver.swipe((width / 4), (height / 5), (width / 4), 4 * (height / 5))
        time.sleep(action_time)
        driver.swipe((width / 4), height / 5, (width / 4), 4 * (height / 5))


def verify_meeting_hold_banner_when_user_in_call(device, meeting):
    common.wait_for_element(device, calls_dict, "hold_label_time")
    common.wait_for_element(device, calls_dict, "Resume")
    common.wait_for_element(device, calls_dict, "end_button_in_hold_banner")
    temp_dict = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", meeting)
    common.wait_for_element(device, temp_dict, "meeting")


def change_time_convention_for_meeting_time(device, current_time_convention):
    common.wait_for_and_click(device, calendar_dict, "timezone_dropdown")
    time_convention_dict = common.get_dict_copy(
        device_settings_dict, "time_convention_xpath", "timezone_replace", current_time_convention
    )
    common.wait_for_and_click(device, time_convention_dict, "time_convention_xpath")


def verify_options_in_calendar_tab(device, phone_number, meeting=None):
    common.wait_for_element(device, home_screen_dict, "home_bar_icon")
    common.wait_for_element(device, calendar_dict, "Header")
    common.wait_for_element(device, calls_dict, "call_park")
    common.wait_for_element(device, calls_dict, "search")
    common.wait_for_element(device, calendar_dict, "meet_now")
    actual_phone_number = common.get_all_elements_texts(device, calls_dict, "user_phone_num")
    expected_phone_number = common.device_pstndisplay(phone_number)
    if expected_phone_number not in actual_phone_number:
        raise AssertionError(
            f"{device}: Expected phone number {expected_phone_number} is not matching with actual phone number:{actual_phone_number}"
        )
    if meeting:
        expected_meeting_name = meeting
        actual_meeting_name = common.wait_for_element(device, calendar_dict, "meeting_list").text
        if actual_meeting_name.lower() != expected_meeting_name.lower():
            raise AssertionError(f"{actual_meeting_name} meeting name is not same as expected: {expected_meeting_name}")
    else:
        verify_calendar_empty(device)
    common.wait_for_element(device, calls_dict, "Make_a_call")


def verify_functionality_of_dialpad(device):
    common.wait_for_and_click(device, calls_dict, "Make_a_call")
    common.wait_for_element(device, calls_dict, "Make_a_call")
