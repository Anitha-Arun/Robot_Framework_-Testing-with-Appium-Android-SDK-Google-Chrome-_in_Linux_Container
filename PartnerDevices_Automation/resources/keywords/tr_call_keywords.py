from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Selectors import load_json_file
from initiate_driver import obj_dev as obj
from initiate_driver import config
import settings_keywords
import common
import time
import json
import call_keywords

display_time = 2
action_time = 3
refresh_time = 10

voicemail_dict = json.loads(open("resources/Page_objects/Voicemail.json").read())
tr_settings_dict = json.loads(open("resources/Page_objects/tr_settings.json").read())
tr_device_settings_dict = json.loads(open("resources/Page_objects/tr_device_settings.json").read())
tr_calls_dict = json.loads(open("resources/Page_objects/tr_calls.json").read())
calls_dict = json.loads(open("resources/Page_objects/Calls.json").read())
tr_home_screen_dict = json.loads(open("resources/Page_objects/tr_home_screen.json").read())
tr_calendar_dict = json.loads(open("resources/Page_objects/tr_calendar.json").read())
settings_dict = json.loads(open("resources/Page_objects/Settings.json").read())
calendar_dict = load_json_file("resources/Page_objects/Calendar.json")
tr_console_home_screen_dict = load_json_file("resources/Page_objects/rooms_console_home_screen.json")
tr_console_calls_dict = load_json_file("resources/Page_objects/rooms_console_calls.json")
tr_console_calendar_dict = load_json_file("resources/Page_objects/rooms_console_calendar.json")


def accept_incoming_call(device):
    devices = device.split(",")
    for device in devices:
        print("Picking incoming call on device : ", device)
        print("device :", device)
        if common.is_norden(device):
            common.wait_for_and_click(device, tr_calls_dict, "accept_button")
        else:
            call_keywords.pick_incoming_call(device)
            print("Call Accepted Now.... ")


def disable_video_call(device):
    devices = device.split(",")
    for device in devices:
        print("Disabling video call on device : ", device)
        print("device :", device)
        common.wait_for_element(device, calendar_dict, "hang_up_btn")
        common.wait_for_and_click(device, tr_calls_dict, "video_on")
        common.wait_for_element(device, tr_calls_dict, "video_off")


def verify_video_call_state(device_list, state):
    devices = device_list.split(",")
    print("Devices : ", devices)
    for device in devices:
        print("device : ", device)
        driver = obj.device_store.get(alias=device)
        common.wait_for_element(device, calendar_dict, "hang_up_btn")
        if state.lower() == "on":
            try:
                elem1 = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((MobileBy.ID, tr_calls_dict["video_on"]["id"]))
                )
                if elem1.is_displayed():
                    print("Video icon button present, video is On state", elem1.text)
            except Exception as e:
                print("Video icon button absent, video is in OFF state", device)
        elif state.lower() == "off":
            try:
                elem2 = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((MobileBy.ID, tr_calls_dict["video_off"]["id"]))
                )
                if elem2.is_displayed():
                    print("video icon button absent, video is in OFF state".elem2.text)
            except Exception as e:
                print("video icon button present, video is On state", device)
    pass


def reject_incoming_call(device_list):
    devices = device_list.split(",")
    for device in devices:
        print("Rejecting incoming call on device : ", device)
        if common.is_norden(device):
            common.wait_for_and_click(device, tr_calls_dict, "Decline_call_button")
        else:
            call_keywords.rejects_the_incoming_call(device_list)
            print("Call Declined")


def close_roaster_button_on_participants_screen(device):
    devices = device.split(",")
    for device in devices:
        print("Trying to close roster button on participant screen on device = : ", device)
        common.wait_for_and_click(device, tr_calls_dict, "close_roaster_button")
        common.sleep_with_msg(device, 3, "sleep until roaster button is closed")
        if common.is_element_present(device, tr_calls_dict, "close_roaster_button"):
            raise AssertionError(f" {device} still able to see close roster button in {device}")


def enable_video_call(device):
    devices = device.split(",")
    for device in devices:
        print("Enabling video call on device : ", device)
        common.wait_for_element(device, calendar_dict, "hang_up_btn")
        common.wait_for_and_click(device, tr_calls_dict, "video_off")
        common.wait_for_element(device, tr_calls_dict, "video_on")


def place_a_call(from_device, to_device, method, dial_mode=None):
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
        elif user.lower() == "pstn_disabled":
            account = "pstn_disabled"
    else:
        account = "user"
    print("Account :", account)
    to_device = to_device.split(":")[0]
    print("to_device : ", to_device)
    username = config["devices"][to_device][account]["username"]
    phonenumber = config["devices"][to_device][account]["phonenumber"]
    displayname = config["devices"][to_device][account]["displayname"]
    print("Username and phone number : ", username, phonenumber, displayname)
    driver = obj.device_store.get(alias=from_device)
    if method.lower() == "phone_number":
        if common.is_norden(from_device):
            print("search text :", phonenumber)
            common.wait_for_and_click(from_device, tr_calls_dict, "dial_pad", "id")
            print("Clicked on Dial Pad present on home screen")
            time.sleep(display_time)
            try:
                if config["devices"][from_device]["model"].lower() not in ["spokane", "sammamish"]:
                    common.hide_keyboard(from_device)
                    print("Hide keyboard")
            except Exception as e:
                print("Cannot hide keyboard : ", e)
            element = common.wait_for_element(from_device, tr_calls_dict, "search_box")
            element.send_keys(phonenumber)
            print("Entered Phone number")
            time.sleep(display_time)
            if dial_mode is not None:
                print("Auto dial number place Successfully")
            else:
                common.wait_for_and_click(from_device, tr_calls_dict, "place_call")
        else:
            print("search text :", phonenumber)
            common.wait_for_and_click(from_device, calls_dict, "search", "id")
            print("Clicked on search")
            element = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.ID, calls_dict["search_text"]["id"]))
            )
            element.send_keys(phonenumber)
            print("Entered phone number")
            time.sleep(display_time)
            common.wait_for_and_click(from_device, calls_dict, "search_result_name", "id")
            print("search result name is displayed")
            # time.sleep(action_time)
        # TODO: verify that the UI says the call is in progress (eg. the hangup button appears)

    elif method.lower() == "username":
        print("search text :", username)
        common.wait_for_and_click(from_device, tr_calls_dict, "dial_pad", "id")
        time.sleep(display_time)
        if config["devices"][from_device]["model"].lower() not in ["spokane", "sammamish"]:
            common.hide_keyboard(from_device)
        element = common.wait_for_element(from_device, tr_calls_dict, "search_box")
        element.send_keys(username)
        print("Entered username")
        time.sleep(display_time)
        common.wait_for_and_click(from_device, calls_dict, "search_result_name")
        common.wait_for_and_click(from_device, tr_calls_dict, "place_call")
        print("Calling is in progress...")

    elif method.lower() == "displayname":
        print("search text :", username)
        common.wait_for_and_click(from_device, tr_calls_dict, "dial_pad", "id")
        time.sleep(display_time)
        if config["devices"][from_device]["model"].lower() not in ["spokane", "sammamish"]:
            common.hide_keyboard(from_device)
        element = common.wait_for_element(from_device, tr_calls_dict, "search_box")
        element.send_keys(displayname)
        print("Entered displayname")
        time.sleep(display_time)
        common.wait_for_and_click(from_device, calls_dict, "search_result_name")
        common.wait_for_and_click(from_device, tr_calls_dict, "place_call")
        print("Calling is in progress...")


def verify_second_incoming_call(device):
    print("device", device)
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((MobileBy.ID, tr_calls_dict["accept_button"]["id"]))
        )
        raise AssertionError("Getting Incoming call")
    except Exception as e:
        print("Not getting incoming call when user is already in the call", device)


def verify_call_control_bar(device_list):
    devices = device_list.split(",")
    print("Devices : ", devices)
    for device in devices:
        print("device ", device)
        common.wait_for_element(device, calendar_dict, "hang_up_btn")
        common.wait_for_element(device, calls_dict, "meeting_mute_control")
        common.wait_for_element(device, tr_calls_dict, "call_control_roaster")
        common.wait_for_element(device, tr_calls_dict, "call_control_shared_mode_btn")
        common.wait_for_element(device, tr_calls_dict, "call_more_option")
        common.wait_for_element(device, tr_home_screen_dict, "volume_minus")
        common.wait_for_element(device, tr_home_screen_dict, "volume_icon")
        common.wait_for_element(device, tr_home_screen_dict, "volume_plus")


def verify_calling_settings_options(device):
    print("device", device)
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, settings_dict["Calling"]["xpath"]))
        ).click()
        print("Clicked on Calling button")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.XPATH, voicemail_dict["voicemail_tab"]["xpath"]))
        )
        print("Change Voicemail greetings is visible")
        elem2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.XPATH, tr_calls_dict["ringtones"]["xpath"]))
        )
        print("Ringtones is visible:", elem2.text)
        time.sleep(display_time)
        swipe_till_end_page(device)
        time.sleep(display_time)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.XPATH, tr_calls_dict["block_calls"]["xpath"]))
        )
        print("Block Calls is visible")
    except Exception as e:
        raise AssertionError("Xpath not found", e)


def swipe_till_end_page(device):
    driver = obj.device_store.get(alias=device)
    window_size = driver.get_window_size()
    print("Window size: ", window_size)
    height = window_size["height"]
    print("Window Height :", height)
    width = window_size["width"]
    print("Window Width :", width)
    if height > width:
        print("Swiping co-ordinates : ", width / 2, 3 * (height / 5), width / 2, height / 5)
        driver.swipe(width / 2, 4 * (height / 5), width / 2, height / 5)
    else:
        print("Swiping co-ordinates : ", width / 2, 3 * (height / 4), width / 2, height / 4)
        driver.swipe(width / 2, 3 * (height / 4), width / 2, height / 4)
    pass


def verify_whiteboard_sharing_option_under_more_option(device):
    common.sleep_with_msg(device, 5, "Waiting for call control bar display")
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_and_click(device, tr_calendar_dict, "share_button")
    common.sleep_with_msg(device, 5, "wait till canvas_tool_bar reflected")
    common.wait_for_and_click(device, tr_calendar_dict, "Microsoft_whiteboard_sharing")
    if "console" not in device:
        common.wait_for_element(device, tr_calls_dict, "Whiteboard")
        time.sleep(refresh_time)
        if not common.is_element_present(device, tr_calls_dict, "canvas_lasso_select"):
            common.wait_for_element(device, tr_calls_dict, "canvas_view")


def click_stop_presenting_whiteboard(device):
    print("device", device)
    if "console" in device:
        common.wait_for_and_click(device, tr_calendar_dict, "stop_whiteboard_sharing")
    else:
        time.sleep(3)
        common.click_if_present(device, tr_calls_dict, "stop_presenting")
        common.click_if_present(device, tr_calls_dict, "stop_whiteboard_presenting")
        common.sleep_with_msg(device, 5, "sleep until whiteboard share disappear")
        if common.is_element_present(device, tr_calls_dict, "Whiteboard"):
            raise AssertionError(
                f" {device} is able to see whiteboard sharing after clicking on stop whiteboard in {device}"
            )


def check_participants_profile_view(device):
    print("device", device)
    driver = obj.device_store.get(alias=device)
    try:
        elem = driver.find_element_by_id(calls_dict["call_participant_name"]["id"])
        elem.click()
        print("Click on first participant")
        view_profile = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calls_dict["view_profile_option"]["xpath"]))
        )
        if view_profile.is_displayed():
            print("Profile view is visible")
            view_profile.click()
        print("Clicked on profile view option")
        time.sleep(display_time)
        settings_keywords.click_back(device)
        print("Successfully come out from profile screen")
        time.sleep(display_time)
        close_roaster_button_on_participants_screen(device)
    except Exception as e:
        raise AssertionError("Profile view is not visible")


def select_view_profile_option(device):
    print("device", device)
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calls_dict["view_profile_option"]["xpath"]))
        ).click()
        print("Clicked on view profile option")
        time.sleep(display_time)
        settings_keywords.click_back(device)
        print("Navigated back to call screen")
    except Exception as e:
        raise AssertionError("Xpath not found", device)


def dial_incorrect_number(device, method, dial_mode=None):
    print("device", device)
    phonenumber = config["incorrect_number"]["phonenumber"]
    print("phone_number : ", phonenumber)
    if method.lower() == "phone_number":
        print("search text :", phonenumber)
        time.sleep(display_time)
        if not common.click_if_present(device, tr_calls_dict, "dial_pad"):
            common.wait_for_and_click(device, tr_console_home_screen_dict, "call_icon")
        element = common.wait_for_element(device, tr_calls_dict, "search_box")
        print("Clicked on search edit text box")
        element.send_keys(phonenumber)
        print("Entered Phone number")
        if dial_mode is not None:
            print("Call icon is still visble, No AUTO DIALLING happen")
            common.sleep_with_msg(device, 35, "user is getting announcment as a wrong number")
            common.click_if_present(device, tr_calls_dict, "close_dial_pad_button")
        else:
            if not common.click_if_present(device, tr_console_calls_dict, "call_button"):
                common.wait_for_and_click(device, tr_calls_dict, "place_call")
            common.sleep_with_msg(device, 30, "user is getting announcment as a wrong number")
            print("Clicked on Call icon")


def close_dial_pad_screen(device):
    common.wait_for_and_click(device, tr_calls_dict, "close_dial_pad_button")


def verify_for_call_decline_screen(device):
    common.wait_for_element(device, calls_dict, "call_declined_screen")


def verify_meeting_name(device, meeting):
    meeting_name = common.wait_for_element(device, tr_calendar_dict, "meeting_action_bar_title_text").text
    if meeting_name != meeting:
        raise AssertionError("meeting name is not matched")


def verify_more_options_in_call_control_bar(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    common.wait_for_and_click(device, tr_calls_dict, "call_more_option")
    # common.wait_for_element(device, tr_calls_dict, "put_on_hold")
    common.wait_for_element(device, tr_calendar_dict, "turn_on_live_captions")
    common.wait_for_element(device, tr_calls_dict, "incoming_video_off")
    common.wait_for_element(device, tr_calls_dict, "dial_pad")
    common.wait_for_element(device, tr_calendar_dict, "turn_off_remote_control")
    common.wait_for_element(device, tr_calendar_dict, "report_an_issue")
    settings_keywords.click_device_center_point(device)


def disconnect_call_and_verify_ended_screen(device):
    devices = device.split(",")
    for device in devices:
        common.wait_for_and_click(device, calls_dict, "Hang_up_button")
    if not common.is_element_present(device, tr_calls_dict, "call_rating_dismiss"):
        common.is_element_present(device, tr_calls_dict, "call_ended")
    common.sleep_with_msg(device, 3, "Waiting for auto dismissal of call rating screen")
    if not common.is_element_present(device, tr_calls_dict, "call_rating_dismiss"):
        if common.is_element_present(device, tr_calls_dict, "call_ended"):
            raise AssertionError(f"Call rating screen didn't auto dismiss in 3 seconds")


def verify_user_should_not_have_stop_presenting_button(device):
    if common.is_element_present(device, tr_calls_dict, "stop_presenting"):
        raise AssertionError(f"Stop presenting button is displayed on other user during whiteboard sharing {device}")


def verify_user_should_not_get_second_incoming_call(device):
    if common.is_element_present(device, tr_calls_dict, "accept_button"):
        raise AssertionError(f"{device}:Second incoming call is getting while in call with another user")


def verify_dailpad_on_call_controlbar(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    common.wait_for_and_click(device, calls_dict, "call_more_options")
    common.wait_for_and_click(device, calls_dict, "call_dial_pad")
    common.wait_for_element(device, tr_calls_dict, "dailpad_layout")


def verify_mic_on_calling_screen_is_not_clickable(device):
    if common.click_if_present(device, calls_dict, "meeting_mute_control"):
        raise AssertionError(f" mic on calling screen is able to click {device}")
    common.wait_for_and_click(device, tr_calls_dict, "close_dial_pad_button")


def wait_for_voicemail_timeout_disconnect(device):
    common.wait_while_present(device, calls_dict, "Hang_up_button", None, 60)


def verify_back_button_when_user_enters_text_in_search_field(device):
    username = common.device_displayname(device)
    common.wait_for_and_click(device, tr_calls_dict, "dial_pad", "id")
    time.sleep(display_time)
    if config["devices"][device]["model"].lower() not in ["spokane", "sammamish"]:
        common.hide_keyboard(device)
    element = common.wait_for_element(device, tr_calls_dict, "search_box")
    element.send_keys(username)
    print("Entered username")
    time.sleep(display_time)
    common.wait_for_and_click(device, calls_dict, "search_result_name")
    call_keywords.click_close_btn(device)
