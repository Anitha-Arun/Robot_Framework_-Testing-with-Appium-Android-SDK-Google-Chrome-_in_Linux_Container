import time
import common
from Libraries.Selectors import load_json_file
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from initiate_driver import config
from initiate_driver import obj_dev as obj
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import settings_keywords
import tr_console_settings_keywords
import call_keywords

display_time = 2
action_time = 3

calls_dict = load_json_file("resources/Page_objects/Calls.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")
tr_settings_dict = load_json_file("resources/Page_objects/tr_settings.json")
tr_console_signin_dict = load_json_file("resources/Page_objects/rooms_console_signin.json")
tr_device_settings_dict = load_json_file("resources/Page_objects/tr_device_settings.json")
tr_calls_dict = load_json_file("resources/Page_objects/tr_calls.json")
tr_home_screen_dict = load_json_file("resources/Page_objects/tr_home_screen.json")
tr_console_home_screen_dict = load_json_file("resources/Page_objects/rooms_console_home_screen.json")
tr_console_calls_dict = load_json_file("resources/Page_objects/rooms_console_calls.json")
tr_console_calendar_dict = load_json_file("resources/Page_objects/rooms_console_calendar.json")
tr_calendar_dict = load_json_file("resources/Page_objects/tr_calendar.json")
calendar_dict = load_json_file("resources/Page_objects/Calendar.json")
tr_console_settings_dict = load_json_file("resources/Page_objects/rooms_console_settings.json")


def pick_up_incoming_call(console):
    consoles = console.split(",")
    for console in consoles:
        print("Picking incoming call on device : ", console)
        print("Console :", console)
        driver = obj.device_store.get(alias=console)
        try:
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.ID, tr_calls_dict["accept_button"]["id"]))
            ).click()
            print("Clicked on Accept call button")
        except TimeoutException:
            try:
                WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((MobileBy.ID, tr_calls_dict["accept_button"]["id"]))
                ).click()
                print("Clicked on Accept call button")
            except TimeoutException:
                raise AssertionError("Unable to answer an incoming call")


def disconnect_the_call(console):
    consoles = console.split(",")
    for console in consoles:
        print("Disconnecting call on device : ", console)
        time.sleep(10)
        if not common.click_if_present(console, tr_console_calls_dict, "reject_call"):
            common.wait_for_and_click(console, tr_console_calls_dict, "hang_up_button")
        for attempt in range(2):
            if common.click_if_present(console, calls_dict, "Close_Call_Rating"):
                break
            common.sleep_with_msg(console, 5, "sleep until Call_Rating appear")


def check_video_call_state(console_list, device_list, state):
    consoles = console_list.split(",")
    devices = device_list.split(",")
    print("Consoles : ", consoles)
    print("Devices : ", devices)
    for console in consoles:
        print("console : ", console)
        driver_c = obj.device_store.get(alias=console)
    for device in devices:
        print("device : ", device)
        driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver_c, 15).until(EC.element_to_be_clickable((MobileBy.ID, calls_dict["Hang_up_button"]["id"])))
        print("Call control is visible on screen ")
    except Exception:
        tr_console_settings_keywords.tap_on_device_center_point(console)
        print("Call control is not visible on screen ,so clicking on center point")
    if device_list is not None:
        pass
    else:
        try:
            WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((MobileBy.ID, calls_dict["Hang_up_button"]["id"]))
            )
            print("Call control is visible on screen for devices ")
        except Exception as e:
            settings_keywords.click_device_center_point(device)
            print("Call control is not visible on screen ,so clicking on center point")
    if state.lower() == "on":
        try:
            elem1 = WebDriverWait(driver_c, 30).until(
                EC.element_to_be_clickable((MobileBy.ID, tr_console_calls_dict["video_on"]["id"]))
            )
            elem2 = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.ID, tr_calls_dict["video_on"]["id"]))
            )
            if elem1.is_displayed and elem2.is_displayed():
                print("Video icon button present, video is On state")
        except Exception as e:
            print("Video icon button absent, video is in OFF state")
    elif state.lower() == "off":
        try:
            elem3 = WebDriverWait(driver_c, 30).until(
                EC.element_to_be_clickable((MobileBy.ID, tr_console_calls_dict["video_off"]["id"]))
            )
            elem4 = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.ID, tr_calls_dict["video_off"]["id"]))
            )
            if elem3.is_displayed() and elem4.is_displayed():
                print("Video icon button absent, video is in OFF state")
        except Exception as e:
            print("Video icon button present, video is On state")
    pass


def turn_on_video_call(console):
    common.sleep_with_msg(console, 5, "Waiting for the call control bar display")
    if not common.is_element_present(console, calls_dict, "Hang_up_button"):
        tr_console_settings_keywords.tap_on_device_center_point(console)
        print(f" {console} : Clicked on center point")
    common.wait_for_element(console, calls_dict, "Hang_up_button")
    common.wait_for_and_click(console, tr_console_calls_dict, "video_on")


def turn_off_video_call(console):
    common.sleep_with_msg(console, 5, "Waiting for the call control bar display")
    if not common.is_element_present(console, calls_dict, "Hang_up_button"):
        tr_console_settings_keywords.tap_on_device_center_point(console)
        print(f" {console} : Clicked on center point")
    common.wait_for_element(console, calls_dict, "Hang_up_button")
    common.wait_for_and_click(console, tr_console_calls_dict, "video_off")


def make_a_call(from_device, to_device, method, device_type=None, dial_mode=None):
    print(f"from_device : {from_device},to_device : {to_device}")
    phonenumber = common.device_phonenumber(to_device)
    username = common.device_username(to_device)
    search_box = phonenumber if method.lower() == "phone_number" else username
    if device_type is not None and common.is_norden(from_device):
        common.wait_for_and_click(from_device, tr_calls_dict, "dial_pad")
    else:
        common.wait_for_and_click(from_device, tr_console_home_screen_dict, "call_icon")
    time.sleep(display_time)
    common.hide_keyboard(from_device)
    if "console" in from_device:
        # common.wait_for_and_click(from_device, calls_dict, "search", "id")
        element = common.wait_for_element(from_device, tr_calls_dict, "search_box")
        element.send_keys(search_box)
        time.sleep(display_time)
        # common.wait_for_and_click(from_device, calls_dict, "search_result_name", "id")
    else:
        element = common.wait_for_element(from_device, tr_calls_dict, "search_box")
        element.send_keys(search_box)
    time.sleep(3)
    if method.lower() == "username":
        common.wait_for_and_click(from_device, calls_dict, "search_result_name", "id")
    common.wait_for_and_click(from_device, tr_calls_dict, "place_call")


def make_video_call(from_device, to_device, method, device_type=None):
    print(f"from_device : {from_device},to_device : {to_device}")
    phonenumber = common.device_phonenumber(to_device)
    username = common.device_username(to_device)
    if method.lower() == "display_name":
        if device_type is not None:
            print("Username and phone number : ", username, phonenumber)
            if common.is_norden(from_device):
                print("Search text :", username)
                common.wait_for_and_click(from_device, tr_home_screen_dict, "meeting_button", "id")
                common.wait_for_and_click(from_device, tr_calls_dict, "Add_participants_btn")
                common.wait_for_element(from_device, calls_dict, "search_contact_box", "id").send_keys(username)
                common.wait_for_and_click(from_device, calls_dict, "search_result_item_container", "id")
                print("Clicked on search user list result")
                time.sleep(display_time)
            else:
                print("Search text :", username)
                common.wait_for_and_click(from_device, calls_dict, "search_contact_box")
                ele = common.wait_for_element(from_device, calls_dict, "search_contact_box")
                ele.send_keys(username)
                common.wait_for_and_click(from_device, calls_dict, "search_result_item_container")
        else:
            print("Username and phone number : ", username, phonenumber)
            common.wait_for_and_click(from_device, tr_home_screen_dict, "meeting_button", "id")
            element = common.wait_for_element(from_device, calls_dict, "search_contact_box", "id")
            element.send_keys(username)
            common.wait_for_and_click(from_device, calls_dict, "search_result_item_container", "id")


def validate_call_control_bar_options(console):
    common.wait_for_element(console, calls_dict, "Hang_up_button")
    common.wait_for_element(console, calls_dict, "meeting_mute_control")
    common.wait_for_element(console, tr_console_calls_dict, "volume_minus", "id")
    common.wait_for_element(console, tr_console_calls_dict, "volume_icon", "id")
    common.wait_for_element(console, tr_console_calls_dict, "volume_plus", "id")
    common.wait_for_element(console, calls_dict, "call_more_options")


def mute_the_call(console):
    print("Mutes the phone call on : ", console)
    common.wait_for_element(console, calls_dict, "Hang_up_button")
    common.wait_for_and_click(console, calls_dict, "meeting_mute_control")
    time.sleep(3)
    if not common.is_element_present(console, calls_dict, "meeting_verify_muted"):
        if not common.is_element_present(console, calls_dict, "call_verify_muted"):
            common.wait_for_element(console, tr_console_calls_dict, "mic_button_muted")


def unmute_the_call(console):
    print("Unmutes the phone call on : ", console)
    common.wait_for_element(console, calls_dict, "Hang_up_button")
    common.wait_for_and_click(console, calls_dict, "meeting_mute_control")
    time.sleep(3)
    if not common.is_element_present(console, calls_dict, "meeting_verify_unmuted"):
        if not common.is_element_present(console, calls_dict, "call_verify_unmuted"):
            common.wait_for_element(console, tr_console_calls_dict, "mic_button_unmuted")


def verify_and_check_call_mute_state(console_list, device_list=None, state=None):
    consoles = console_list.split(",")
    print("Consoles : ", consoles)
    for console in consoles:
        print("console : ", console)
        if state is not None:
            if state.lower() == "mute":
                common.wait_for_element(console, tr_console_calls_dict, "hang_up_button")
                if not common.is_element_present(console, calls_dict, "meeting_verify_muted"):
                    if not common.is_element_present(console, calls_dict, "call_verify_muted"):
                        common.wait_for_element(console, tr_console_calls_dict, "mic_button_muted")
            elif state.lower() == "unmute":
                if not common.is_element_present(console, calls_dict, "meeting_verify_unmuted"):
                    if not common.is_element_present(console, calls_dict, "call_verify_unmuted"):
                        common.wait_for_element(console, tr_console_calls_dict, "mic_button_unmuted")
    if device_list is not None:
        devices = device_list.split(",")
        print("Devices : ", devices)
        for device in devices:
            print("device : ", device)
            if state is not None:
                if state.lower() == "mute":
                    call_keywords.verify_call_mute_state(device, "mute")
                elif state.lower() == "unmute":
                    call_keywords.verify_call_mute_state(device, "unmute")


def turn_on_incoming_video_call(console):
    consoles = console.split(",")
    for console in consoles:
        print("Console : ", console)
        driver = obj.device_store.get(alias=console)
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((MobileBy.ID, calls_dict["Hang_up_button"]["id"]))
            )
            print("Call control visible on screen")
        except Exception as e:
            tr_console_settings_keywords.tap_on_device_center_point(console)
            print("Clicked on center point")
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((MobileBy.ID, calls_dict["call_more_options"]["id"]))
        ).click()
        print("Clicked on call more options")
        try:
            elem = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((MobileBy.XPATH, tr_calls_dict["incoming_video_on"]["xpath"]))
            )
            elem.click()
            print("Successfully turn 'ON Incoming video' ")
        except Exception as e:
            raise AssertionError("Failed to turn 'ON' Incoming video")


def turn_off_incoming_video_call(console):
    consoles = console.split(",")
    for console in consoles:
        print("Console : ", console)
        driver = obj.device_store.get(alias=console)
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((MobileBy.ID, calls_dict["Hang_up_button"]["id"]))
            )
            print("Call control visible on screen")
        except Exception as e:
            tr_console_settings_keywords.tap_on_device_center_point(console)
            print("Clicked on center point")
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((MobileBy.ID, calls_dict["call_more_options"]["id"]))
        ).click()
        print("Clicked on call more options")
        try:
            elem = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((MobileBy.XPATH, tr_calls_dict["incoming_video_off"]["xpath"]))
            )
            elem.click()
            print("Successfully turn 'OFF Incoming video' ")
        except Exception as e:
            raise AssertionError("Failed to turn 'OFF' Incoming video")


def hold_current_call(console):
    print("Hold the phone call on device : ", console)
    common.wait_for_element(console, calls_dict, "Hang_up_button")
    common.wait_for_and_click(console, calls_dict, "call_more_options")
    common.wait_for_and_click(console, tr_console_calls_dict, "put_call_on_hold")


def resume_current_call(console):
    print("Resume the phone call on device : ", console)
    if common.is_element_present(console, calls_dict, "Call_Rating"):
        common.wait_for_and_click(console, calls_dict, "Close_Call_Rating")
    common.wait_for_and_click(console, tr_console_calls_dict, "resume_btn")


def verify_for_call_state(console_list, device_list=None, state=None):
    consoles = console_list.split(",")
    print("Consoles : ", consoles)
    for console in consoles:
        print("console : ", console)
        if state is not None:
            if state.lower() == "connected":
                common.wait_for_element(console, tr_console_calls_dict, "hang_up_button")
                print("Call End Buttton present, call is connected")
                print("Call is disconnected on device : ", console)
            elif state.lower() == "disconnected":
                if common.is_element_present(console, calls_dict, "end_call_callee_text"):
                    common.click_if_present(console, calls_dict, "Close_Call_Rating")
                print("Call Rating Not asked")
                if not common.click_if_present(console, tr_console_settings_dict, "back_layout"):
                    common.click_if_present(console, calls_dict, "Call_Back_Button")
                time.sleep(3)
                common.click_if_present(console, tr_console_settings_dict, "back_layout")
                common.wait_for_element(console, tr_console_home_screen_dict, "more_option")
                print("Call is disconnected on device : ", console)
            elif state.lower() == "hold":
                common.wait_for_element(console, calls_dict, "call_on_hold")
            elif state.lower() == "resume":
                common.wait_for_element(console, calls_dict, "Hang_up_button")
                common.wait_for_element(console, calls_dict, "call_more_options")
                common.wait_for_element(console, tr_console_calendar_dict, "search_icon")
    if device_list is not None:
        devices = device_list.split(",")
        print("Devices : ", devices)
        for device in devices:
            print("device : ", device)
            if state.lower() == "connected":
                if common.is_norden(device):
                    call_keywords.verify_call_state(device, "connected")
            elif state.lower() == "disconnected":
                if common.is_norden(device):
                    call_keywords.verify_call_state(device, "disconnected")
            elif state.lower() == "hold":
                if common.is_norden(device):
                    call_keywords.verify_call_state(device, "hold")
            elif state.lower() == "resume":
                if common.is_norden(device):
                    call_keywords.verify_call_state(device, "resume")


def dial_and_validate_the_numbers_from_0_to_9(console_list, device):
    consoles = console_list.split(",")
    print("Consoles : ", consoles)
    for console in consoles:
        print("Console : ", console)
        driver = obj.device_store.get(alias=console)
        common.wait_for_and_click(console, tr_console_home_screen_dict, "call_icon")
        common.wait_for_element(console, tr_calls_dict, "search_box")
        common.hide_keyboard(console)
        elem = common.wait_for_element(console, calls_dict, "zero")
        actions = TouchAction(driver)
        actions.long_press(elem, duration=1000).release().perform()
        common.wait_for_and_click(console, calls_dict, "nine")
        common.wait_for_and_click(console, calls_dict, "eight")
        common.wait_for_and_click(console, calls_dict, "seven")
        common.wait_for_and_click(console, calls_dict, "six")
        common.wait_for_and_click(console, calls_dict, "five")
        common.wait_for_and_click(console, calls_dict, "four")
        common.wait_for_and_click(console, calls_dict, "three")
        common.wait_for_and_click(console, calls_dict, "two")
        common.wait_for_and_click(console, calls_dict, "one")
        common.wait_for_and_click(console, calls_dict, "zero")
        common.wait_for_and_click(console, tr_console_home_screen_dict, "call_icon")
        dailed_number = common.wait_for_element(device, tr_console_home_screen_dict, "caller_num").text
        print("Entered phone number :: ", dailed_number)
        expected = "+9876543210"
        if expected != dailed_number.replace("1 ", "").replace("-", ""):
            raise AssertionError(
                f"Typed phone number is not matching: Expected: '{expected}', actual: '{dailed_number}'"
            )
        common.sleep_with_msg(console, 10, "Wait until the announcement is complete.")
        common.wait_while_present(device, calls_dict, "Hang_up_button")


def verify_option_present_inside_more_option_and_validate(console):
    common.sleep_with_msg(console, 5, "Waiting for the call control bar display")
    common.wait_for_element(console, calls_dict, "Hang_up_button")
    common.wait_for_and_click(console, calls_dict, "call_more_options")
    #    common.wait_for_element(console, tr_calls_dict, "start_recording")
    common.wait_for_element(console, tr_calendar_dict, "turn_on_live_captions")
    tr_console_settings_keywords.tap_on_device_center_point(console)


def select_start_recording_option(console):
    common.sleep_with_msg(console, 5, "Waiting for the call control bar display")
    if not common.is_element_present(console, calls_dict, "Hang_up_button"):
        tr_console_settings_keywords.tap_on_device_center_point(console)
        print(f" {console} : Clicked on center point")
    common.wait_for_element(console, calls_dict, "Hang_up_button")
    common.wait_for_and_click(console, calls_dict, "call_more_options")
    common.wait_for_element(console, tr_calls_dict, "start_recording")
    common.wait_for_element(console, tr_calls_dict, "notification_text")


def select_stop_recording_option(console):
    common.sleep_with_msg(console, 5, "Waiting for the call control bar display")
    if not common.is_element_present(console, calls_dict, "Hang_up_button"):
        tr_console_settings_keywords.tap_on_device_center_point(console)
        print(f" {console} : Clicked on center point")
    common.wait_for_element(console, calls_dict, "Hang_up_button")
    common.wait_for_and_click(console, calls_dict, "call_more_options")
    common.wait_for_and_click(console, tr_calls_dict, "stop_recording")


def verify_docked_ubar_options(console):
    common.wait_for_element(console, calls_dict, "Hang_up_button")
    common.wait_for_element(console, calls_dict, "meeting_mute_control")
    common.wait_for_element(console, tr_console_calls_dict, "video_on")
    common.wait_for_element(console, tr_console_calls_dict, "volume_minus", "id")
    common.wait_for_element(console, tr_console_calls_dict, "volume_icon", "id")
    common.wait_for_element(console, tr_console_calls_dict, "volume_plus", "id")
    common.wait_for_element(console, calls_dict, "call_more_options")
    common.wait_for_element(console, tr_console_calendar_dict, "reactions_button")
    common.wait_for_element(console, tr_console_calendar_dict, "share_button")
    common.wait_for_element(console, tr_calls_dict, "call_control_shared_mode_btn")


def check_the_call_state_and_disconnect(console):
    print("Verifying call state")
    consoles = console.split(",")
    for console in consoles:
        time.sleep(5)
        if common.is_element_present(console, calls_dict, "Hang_up_button"):
            disconnect_the_call(console)
        common.sleep_with_msg(console, 5, "sleep until call disconnects")
        common.click_if_present(console, calls_dict, "Close_Call_Rating")


def verify_user_not_to_get_second_incoming_call(console):
    if common.is_element_present(console, tr_calls_dict, "accept_button"):
        raise AssertionError(f" {console} user is getting second incoming call while in video call with another user")


def check_emergency_call_state(console, device, state):
    common.wait_for_element(console, calls_dict, "Hang_up_button")
    if state.lower() == "connected":
        common.wait_for_element(device, calls_dict, "emergency_call_icon")


def click_on_stop_whiteboard_sharing(console, device):
    common.wait_for_and_click(console, tr_console_calendar_dict, "stop_sharing_whiteboard")
    time.sleep(3)
    if common.is_element_present(device, tr_calls_dict, "Whiteboard"):
        raise AssertionError(
            f" {device} is able to see whiteboard sharing after clicking on stop witheboard in {console}"
        )


def decline_the_incoming_call(console):
    common.wait_for_and_click(console, tr_console_calls_dict, "reject_call")


def whiteboard_sharing_should_not_visible_after_disconnect_from_the_meeting(console, device):
    common.wait_for_and_click(console, tr_console_calls_dict, "hang_up_button")
    common.wait_while_present(device, tr_calls_dict, "canvas_lasso_select")


def verify_external_text_when_entered_cross_tenant_mail_id(from_device, to_device):
    print(f"from_device : {from_device},to_device : {to_device}")
    username = common.device_username(to_device)
    print("Search text :", username)
    common.wait_for_and_click(from_device, tr_console_home_screen_dict, "call_icon")
    time.sleep(display_time)
    element = common.wait_for_element(from_device, tr_calls_dict, "search_box")
    element.send_keys(username)
    common.wait_for_element(from_device, tr_calls_dict, "External_text")
    common.wait_for_and_click(from_device, tr_console_settings_dict, "back_layout")


def verify_accept_call_on_msg_should_not_get_on_device(device):
    time.sleep(3)
    if common.is_element_present(device, tr_console_calls_dict, "accept_call_on_msg"):
        raise AssertionError(
            f"Accept call on console message is still showing {device} After disabling the touch screen controls "
        )
