from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib3.exceptions import ProtocolError
from appium.webdriver.common.touch_action import TouchAction
from initiate_driver import obj_dev as obj
from initiate_driver import config
from Libraries.Selectors import load_json_file
import tr_call_keywords
import settings_keywords
import tr_home_screen_keywords
from operator import add
import re
import time
import calendar_keywords
import common
import tr_settings_keywords
import tr_console_settings_keywords
import subprocess
import call_keywords
import tr_calendar_keywords

display_time = 3
added_time = 5
action_time = 2
minus_time = 60
refresh_time = 10

calendar_dict = load_json_file("resources/Page_objects/Calendar.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")
navigation_dict = load_json_file("resources/Page_objects/Navigation.json")
device_settings_dict = load_json_file("resources/Page_objects/Device_settings.json")
calls_dict = load_json_file("resources/Page_objects/Calls.json")
common_dict = load_json_file("resources/Page_objects/Common.json")
tr_calendar_dict = load_json_file("resources/Page_objects/tr_calendar.json")
tr_calls_dict = load_json_file("resources/Page_objects/tr_calls.json")
tr_home_screen_dict = load_json_file("resources/Page_objects/tr_home_screen.json")
tr_settings_dict = load_json_file("resources/Page_objects/tr_settings.json")
tr_console_calendar_dict = load_json_file("resources/Page_objects/rooms_console_calendar.json")
tr_console_home_screen_dict = load_json_file("resources/Page_objects/rooms_console_home_screen.json")
tr_console_settings_dict = load_json_file("resources/Page_objects/rooms_console_settings.json")
panels_home_screen_dict = load_json_file("resources/Page_objects/panels_homescreen.json")
tr_device_settings_dict = load_json_file("resources/Page_objects/tr_device_settings.json")
tr_console_calls_dict = load_json_file("resources/Page_objects/rooms_console_calls.json")
app_bar_dict = load_json_file("resources/Page_objects/App_bar.json")
tr_console_signin_dict = load_json_file("resources/Page_objects/rooms_console_signin.json")


def schedule_meeting(
    device,
    meeting="test_meeting",
    participants=None,
    repeat=None,
    all_day_meeting="OFF",
    location="bangalore",
    date=None,
):
    print("Create meeting : ", meeting)
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    calendar_keywords.navigate_to_calendar_tab(device)
    print("Inside Calendar Tab")
    settings_keywords.refresh_main_tab(device)
    try:
        time.sleep(display_time)
        calendar_keywords.scroll_till_meeting_visible(device, meeting=meeting)
        meeting_list = driver.find_elements_by_id(calendar_dict["meeting_list"]["id"])
        for i in range(0, len(meeting_list)):
            print("i : ", i)
            meeting_text = meeting_list[i].text
            print("Meeting text :", meeting_text)
            if meeting.lower() == meeting_text.lower():
                print(meeting, " : Meeting is already created")
                return
    except Exception as e:
        pass
        print("Pass")
    time.sleep(display_time)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((MobileBy.ID, calendar_dict["Schedule_meeting"]["id"]))
        ).click()
        time.sleep(display_time)
        print("Clicked on Schedule_meeting")
    except ProtocolError as e:
        for i in range(5):
            print("Trying : ", i)
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((MobileBy.ID, calendar_dict["Schedule_meeting"]["id"]))
                ).click()
                time.sleep(display_time)
                print("Handled ProtocolError while clicking on Schedule_meeting")
                break
            except ProtocolError as e:
                continue
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((MobileBy.ID, calendar_dict["meeting_name"]["id"]))
        ).click()
        time.sleep(display_time)
        print("Clicked on Meeting_name text box")
    except ProtocolError as e:
        for i in range(5):
            print("Trying : ", i)
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((MobileBy.ID, calendar_dict["meeting_name"]["id"]))
                ).click()
                time.sleep(display_time)
                print("Handled ProtocolError while clicking on Meeting_name text box")
                break
            except ProtocolError as e:
                continue
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((MobileBy.ID, calendar_dict["meeting_name"]["id"]))
        )
        print("Checking Meeting_name text box")
    except ProtocolError as e:
        for i in range(5):
            print("Trying : ", i)
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((MobileBy.ID, calendar_dict["meeting_name"]["id"]))
                )
                print("Handled ProtocolError while sending meeting name ")
                break
            except ProtocolError as e:
                continue
    try:
        if meeting == "test_meeting":
            element.send_keys(config["meetings"]["name"])
        else:
            element.send_keys(meeting)
        print("Entered meeting name")
    except ProtocolError as e:
        for i in range(5):
            print("Trying : ", i)
            try:
                if meeting == "test_meeting":
                    element.send_keys(config["meetings"]["name"])
                else:
                    element.send_keys(meeting)
                print("Handled ProtocolError while entering meeting name")
                break
            except ProtocolError as e:
                continue
    time.sleep(display_time)
    try:
        driver.execute_script("mobile: performEditorAction", {"action": "next"})
        print("Clicked on Action Next button")
    except ProtocolError as e:
        for i in range(5):
            print("Trying : ", i)
            try:
                driver.execute_script("mobile: performEditorAction", {"action": "next"})
                print("Handled protocol error while Clicking on Action Next button")
                break
            except ProtocolError as e:
                continue
    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.ID, calendar_dict["meeting_location"]["id"]))
        )
        print("Checking Meeting_location text box")
    except ProtocolError as e:
        for i in range(5):
            print("Trying : ", i)
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((MobileBy.ID, calendar_dict["meeting_location"]["id"]))
                )
                print("Handled ProtocolError while checking Meeting Location")
                break
            except ProtocolError as e:
                continue
    element.click()
    time.sleep(display_time)
    try:
        if location == "bangalore":
            element.send_keys(config["meetings"]["location"])
        else:
            element.send_keys(location)
        print("Entered Meeting Location")
    except ProtocolError as e:
        for i in range(5):
            print("Trying : ", i)
            try:
                if location == "bangalore":
                    element.send_keys(config["meetings"]["location"])
                else:
                    element.send_keys(location)
                print("Handled ProtocolError while Entering Meeting Location")
                break
            except ProtocolError as e:
                continue
    driver.execute_script("mobile: performEditorAction", {"action": "done"})
    if date is None:
        print("repeat :", repeat)
        pass
    elif date.lower() == "current date":
        print("Date is :", date)
        try:
            current_time = driver.find_element_by_id(tr_calendar_dict["current_time"]["id"])
            tim = current_time.text
            print("Current Time is : ", tim)
            print("Display Current time", str(tim))
            hour = re.findall(r"\d+", tim[:2])
            min = re.findall(r"\d+", tim[2:5])
            print("Hour is :", hour)
            print("Min is :", min)
            driver.find_element_by_id(tr_calendar_dict["start_time"]["id"]).click()
            print("Clicked on start time")
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((MobileBy.ID, tr_calendar_dict["toogle_btn"]["id"]))
            ).click()
            print("Clicked on toggle keypad")
            Hour_input = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.ID, tr_calendar_dict["hour_text_box"]["id"]))
            )
            Hour_input.clear()
            Hour_input.send_keys(hour)
            min_input = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((MobileBy.ID, tr_calendar_dict["min_text_box"]["id"]))
            )
            min_input.clear()
            min_input.send_keys(min)
            WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["Cancel_event_OK"]["xpath"]))
            ).click()
            print("Clicked on OK button ")
            time.sleep(display_time)
            driver.find_element_by_id(tr_calendar_dict["end_time"]["id"]).click()
            print("Clicked on End time")
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((MobileBy.ID, tr_calendar_dict["toogle_btn"]["id"]))
            ).click()
            print("Clicked on toggle keypad ")
            Hour_input.clear()
            Hour_input.send_keys(hour)
            min_input.clear()
            print("min is ", min)
            item = [int(i) for i in min]
            print("min is now ", item)
            print("added time is :", added_time)
            add_time = [added_time]
            update_min = list(map(add, item, add_time))
            print("Min is now ", update_min)
            min_input.set_value(update_min)
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["Cancel_event_OK"]["xpath"]))
            ).click()
            print("Clicked on Ok button")
        except Exception as e:
            raise AssertionError("Xpath not found", e)
    else:
        print("Selecting random forward date")
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, calendar_dict["start_date_text"]["id"]))
        ).click()
        time.sleep(display_time)
        print("Clicked on start date")
        elem = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, calendar_dict["date_picker_header_date"]["id"]))
        )
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["next_month"]["xpath"]))
        ).click()
        print("Selected next month icon")
        if elem.is_displayed():
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["random_date"]["xpath"]))
            ).click()
            time.sleep(display_time)
            print("Clicked on random date")
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["Cancel_event_OK"]["xpath"]))
            ).click()
            print("Clicked on Cancel event Ok button")
        else:
            raise AssertionError("Random date Xpath not found")
    if repeat is None:
        print("repeat :", repeat)
        pass
    else:
        print("repeat :", repeat)
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["repeat_option"]["xpath"]))
        ).click()
        if repeat.lower() == "every day":
            result_xpath = (calendar_dict["day_element"]["xpath"]).replace("which day", "Every day")
            print("Search result xpath : ", result_xpath)
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((MobileBy.XPATH, result_xpath))).click()
            print("Selected : ", repeat)
        elif repeat.lower() == "every weekday":
            result_xpath = (calendar_dict["day_element"]["xpath"]).replace("which day", "Every weekday (Mon-Fri)")
            print("Search result xpath : ", result_xpath)
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((MobileBy.XPATH, result_xpath))).click()
            print("Selected : ", repeat)
        elif repeat.lower() == "every week":
            result_xpath = (calendar_dict["day_element"]["xpath"]).replace("which day", "Every weekday")
            print("Search result xpath : ", result_xpath)
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((MobileBy.XPATH, result_xpath))).click()
            print("Selected : ", repeat)
        elif repeat.lower() == "every month":
            result_xpath = (calendar_dict["day_element"]["xpath"]).replace("which day", "Every month")
            print("Search result xpath : ", result_xpath)
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((MobileBy.XPATH, result_xpath))).click()
            print("Selected : ", repeat)
        elif repeat.lower() == "every year":
            result_xpath = (calendar_dict["day_element"]["xpath"]).replace("which day", "Every year")
            print("Search result xpath : ", result_xpath)
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((MobileBy.XPATH, result_xpath))).click()
            print("Selected : ", repeat)
    time.sleep(display_time)
    settings_keywords.refresh_main_tab(device)
    if all_day_meeting == "OFF":
        print("all_day_meeting : ", all_day_meeting)
        pass
    else:
        print("all_day_meeting : ", all_day_meeting)
        elem = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, calendar_dict["all_day_switch"]["id"]))
        )
        element = elem.text
        print("element : ", element)
        if all_day_meeting == "ON":
            if element == "ON":
                raise AssertionError("All Day meeting switch is ON Automatic")
            else:
                elem.click()
                print("Selected All Day meeting switch ON")
    settings_keywords.refresh_main_tab(device)
    time.sleep(display_time)
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.ID, calendar_dict["Add_participants"]["id"]))
        ).click()
        print("Clicked on Add_participants")
    except ProtocolError as e:
        for i in range(5):
            print("Trying : ", i)
            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((MobileBy.ID, calendar_dict["Add_participants"]["id"]))
                ).click()
                print("Handled protocol error while Clicking on Add_participants")
                break
            except ProtocolError as e:
                continue
    time.sleep(display_time)
    try:
        element = driver.find_element_by_id(calendar_dict["search_contact_box"]["id"])
        print("Found search_contact_box")
    except ProtocolError as e:
        for i in range(5):
            print("Trying : ", i)
            try:
                element = driver.find_element_by_id(calendar_dict["search_contact_box"]["id"])
                print("Handled protocol error while Finding search_contact_box")
                break
            except ProtocolError as e:
                continue
    if participants is None:
        print("Participant  : ", config["meetings"]["participant"])
        element.send_keys(config["meetings"]["participant"])
        search_result_xpath = (calendar_dict["add_user"]["xpath"]).replace(
            "user_name", config["meetings"]["participant"]
        )
        print("Search result xpath : ", search_result_xpath)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((MobileBy.XPATH, search_result_xpath))).click()
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
                participant = participant.split(":")[0]
            else:
                account = "user"
            print("Account :", account)
            participant_name = config["devices"][participant][account]["username"].split("@")[0]
            element.set_value(participant_name)
            time.sleep(display_time)
            search_result_xpath = (calendar_dict["add_user"]["xpath"]).replace(
                "user_name", config["devices"][participant][account]["displayname"]
            )
            print("Search result xpath : ", search_result_xpath)
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((MobileBy.XPATH, search_result_xpath))
                ).click()
                print("selected participant")
            except ProtocolError as e:
                for i in range(5):
                    print("Trying : ", i)
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((MobileBy.XPATH, search_result_xpath))
                        ).click()
                        print("Handled ProtocolError while selecting user name")
                        break
                    except ProtocolError as e:
                        continue
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["Submit_button_text_icon"]["xpath"]))
        ).click()
        print("Selected Submit_button")
    except ProtocolError as e:
        for i in range(5):
            print("Trying : ", i)
            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["Submit_button_text_icon"]["xpath"]))
                ).click()
                print("Handled ProtocolError while selecting Submit_button")
                break
            except ProtocolError as e:
                continue
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((MobileBy.XPATH, calendar_dict["Submit_content_icon"]["xpath"]))
    ).click()
    # time.sleep(display_time)
    pass


def verify_video_preview_on_screen(device):
    devices = device.split(",")
    for device in devices:
        common.wait_for_element(device, tr_calendar_dict, "video_view")
        print("Video preview is visible on the screen ")


def start_recording(device_list):
    devices = device_list.split(",")
    for device in devices:
        driver = obj.device_store.get(alias=device)
        print("device: ", device)
        common.wait_for_element(device, calendar_dict, "hang_up_btn")
        elem = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.ID, calls_dict["call_more_options"]["id"]))
        )
        elem.click()
        print("Clicked on call more option")
        time.sleep(action_time)
        try:
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((MobileBy.XPATH, tr_calls_dict["start_recording"]["xpath"]))
            ).click()
            print("Your recording is about to start..")
            time.sleep(5)
            try:
                WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((MobileBy.ID, tr_calls_dict["notification_text"]["id"]))
                )
            except Exception as e:
                WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((MobileBy.ID, tr_calls_dict["notification_text"]["id1"]))
                )
            print("You're recording. Make sure everyone knows they're being recorded.")
        except Exception as e:
            raise AssertionError("Xpath not found", e)


def verify_recording_notification_display_on_screen(device):
    common.wait_for_element(device, tr_calls_dict, "notification_text")


def choose_incoming_video_call(device_list, state):
    print("State is :", state)
    devices = device_list.split(",")
    for device in devices:
        driver = obj.device_store.get(alias=device)
        print("device ", device)
        common.wait_for_element(device, calendar_dict, "hang_up_btn")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.ID, calls_dict["call_more_options"]["id"]))
        ).click()
        print("Clicked on call more option")
        if state.lower() == "off":
            try:
                elem = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, tr_calls_dict["incoming_video_off"]["xpath"]))
                )
                elem.click()
                print("Successfully Turned off the Incoming video")
            except Exception as e:
                raise AssertionError("Turned off the Incoming video Failed", e)
        elif state.lower() == "on":
            try:
                elm = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, tr_calls_dict["incoming_video_on"]["xpath"]))
                )
                elm.click()
                print("Successfully Turned on the Incoming Video")
            except Exception as e:
                raise AssertionError("Turned on the Incoming Video Failed", e)
    pass


def verify_meeting_display_on_home_screen(device):
    meeting_name = common.wait_for_element(device, calendar_dict, "meeting_title_name", wait_attempts=40).text
    print("Meeting name :", meeting_name)
    if not common.is_element_present(device, tr_console_calendar_dict, "meeting_logo"):
        print("Meeting logo is visible only when meeting reached to scheduled time")
    print("Teams icon is visible on screen")
    if common.is_element_present(device, calendar_dict, "meeting_time"):
        meeting_time = common.wait_for_element(device, tr_console_calendar_dict, "meeting_time").text
        print("Meeting Time :", meeting_time)
    common.wait_for_element(device, calendar_dict, "cnf_device_join_button")
    organizer_name = common.wait_for_element(device, calendar_dict, "meeting_organizer_name").text
    print(f"Meeting organizer : {organizer_name}")


def meet_now_meeting(from_device, to_device, method):
    if method.lower() not in ["displayname", "phone_number"]:
        raise AssertionError(f"Unexpected value for method: {method}")
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
    print("to_device : ", to_device)
    username = config["devices"][to_device][account]["username"].split("@")[0]
    displayname = config["devices"][to_device][account]["displayname"]
    phonenumber = config["devices"][to_device][account]["pstndisplay"]
    print("Username and displayname and phone_number : ", username, displayname, phonenumber)
    common.wait_for_and_click(from_device, tr_home_screen_dict, "meeting_button", "id")
    common.wait_for_and_click(from_device, tr_calls_dict, "Add_participants_btn")
    element = common.wait_for_element(from_device, calls_dict, "search_contact_box", "id")
    if method.lower() == "displayname":
        ele_search = displayname
    elif method.lower() == "phone_number":
        ele_search = phonenumber
    element.send_keys(ele_search)
    common.wait_for_and_click(from_device, calls_dict, "search_result_item_container", "id")
    print("Meeting is Initiated now.. ")


def verify_participants_list_in_meeting(device):
    print("Device : ", device)
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    if not common.click_if_present(device, calls_dict, "Add_participants_button"):
        common.wait_for_and_click(device, tr_calls_dict, "Add_participants_btn")
    common.wait_for_element(device, tr_calls_dict, "Participants_label")
    ele = common.wait_for_element(device, tr_calls_dict, "call_roster_header")
    print("Meeting Text :", ele.text)
    participant_list = call_keywords.get_participant_list(device)
    print("Particpants List:", participant_list)
    common.wait_for_element(device, tr_calls_dict, "add_participants")
    tr_call_keywords.close_roaster_button_on_participants_screen(device)


def verify_raise_hand_state(device_list, state):
    print("state", state)
    devices = device_list.split(",")
    for device in devices:
        print("device :", device)
        driver = obj.device_store.get(alias=device)
        common.wait_for_element(device, calendar_dict, "hang_up_btn")
        elem = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.ID, tr_calendar_dict["call_control_reactions_button"]["id"]))
        )
        elem.click()
        print("Clicked on call_control reactions button")
        if state.lower() == "raise_hand":
            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, tr_calendar_dict["raise_hand"]["xpath"]))
                ).click()
                print("Clicked on Raise hand option")
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((MobileBy.ID, tr_calendar_dict["participant_raised_hand"]["id"]))
                )
                print("Participant raised hand is visible")
                print("User is able to view hand symbol on the toaster")
            except Exception as e:
                raise AssertionError("Raise Hand is not visible on the screen")
        elif state.lower() == "lower_hand":
            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, tr_calendar_dict["lower_hand"]["xpath"]))
                ).click()
                print("Clicked on lower hand")
                print("User is not able to view hand symbol on the toaster ")
            except Exception as e:
                raise AssertionError("Lower hand is not visible on the screen")


def validate_menu_bar_get_dismiss_when_clicked_outside_bar_area(device):
    print("device :", device)
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_and_click(device, calls_dict, "call_more_options")
    common.wait_for_element(device, tr_calendar_dict, "turn_on_live_captions")
    common.wait_for_element(device, tr_calls_dict, "incoming_video_off")
    common.wait_for_element(device, tr_calls_dict, "dial_pad")
    settings_keywords.click_device_center_point(device)
    if common.is_element_present(device, tr_calendar_dict, "turn_on_live_captions"):
        raise AssertionError(f"{device} : Menu bar is not dismissed")


def refresh_meeting_visibility_for_conf_device(device):
    common.wait_for_and_click(device, tr_calls_dict, "dial_pad")
    if not common.click_if_present(device, tr_calls_dict, "close_dial_pad_button"):
        if not common.click_if_present(device, calendar_dict, "close_button"):
            common.wait_for_and_click(device, tr_console_signin_dict, "back_layout")


def turn_on_live_captions_and_validate(device):
    print("device :", device)
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_and_click(device, calls_dict, "call_more_options")
    common.wait_for_and_click(device, tr_calendar_dict, "turn_on_live_captions")
    common.wait_for_element(device, calendar_dict, "live_caption_msg")


def turn_off_live_captions_and_validate(device):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((MobileBy.ID, calls_dict["call_more_options"]["id"]))
    ).click()
    print("Clicked on Call more option")
    time.sleep(action_time)
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.XPATH, tr_calendar_dict["turn_off_live_captions"]["xpath"]))
        ).click()
        print("Clicked on turn off live captions option")
    except Exception as e:
        raise AssertionError("Xpath not matching")


def tap_on_whiteboard_share_screen_settings_icon(device):
    common.wait_for_and_click(device, tr_calls_dict, "settings_menu")
    common.wait_for_element(device, tr_calls_dict, "format_background")
    common.wait_for_element(device, tr_calls_dict, "Privacy_security")
    common.wait_for_element(device, tr_calls_dict, "about_whiteboard_text")
    common.wait_for_and_click(device, tr_calls_dict, "settings_menu")


def close_setting_menu_panel_on_whiteboard(device):
    common.wait_for_and_click(device, tr_calls_dict, "close_panel")
    if common.is_element_present(device, tr_calls_dict, "close_panel"):
        raise AssertionError(f"Menu panel is still visible after closing it")


def verify_whiteboard_tools_display_on_screen(device):
    common.wait_for_element(device, tr_calls_dict, "black_pen_btn")
    common.wait_for_element(device, tr_calls_dict, "red_pen_btn")
    common.wait_for_element(device, tr_calls_dict, "galaxy_pen_btn")
    common.wait_for_element(device, tr_calls_dict, "highlighter_pen_btn")
    common.wait_for_element(device, tr_calls_dict, "eraser_btn")
    common.wait_for_element(device, tr_calls_dict, "lasso_select_btn")


def navigate_back_to_call_screen_after_tapping_on_back_button(device):
    settings_keywords.click_back(device)
    print("User has option to navigate back to call screen.")
    common.wait_for_element(device, tr_calls_dict, "whiteboard_share_text")
    common.wait_for_and_click(device, tr_calls_dict, "open_button")
    common.wait_for_element(device, tr_calls_dict, "Whiteboard")


def verify_whiteboard_visibility_for_participants(from_device, connected_device_list):
    connected_devices = connected_device_list.split(",")
    for devices in connected_devices:
        if ":" in devices:
            user = devices.split(":")[1]
            print("User account : ", user)
            account = None
            if user.lower() == "pstn_user":
                account = "pstn_user"
            elif user.lower() == "meeting_user":
                account = "meeting_user"
            device = devices.split(":")[0]
        else:
            account = "user"
            device = devices
        print("account : ", account)
        print("device : ", device)
        if account in ["pstn_user"]:
            common.wait_for_element(from_device, tr_calls_dict, "Whiteboard")
        else:
            common.wait_for_element(from_device, tr_calls_dict, "Whiteboard")


def tap_on_more_option_and_check_share_whiteboard(device):
    common.sleep_with_msg(device, 5, "waiting for the call control bar")
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_and_click(device, calls_dict, "call_more_options")
    common.wait_for_element(device, tr_calls_dict, "share_whiteboard")


def tap_on_all_day_meetings_title_bar_and_validate(device):
    print("device", device)
    common.wait_for_element(device, tr_calendar_dict, "all_day_title_on_main_screen")
    element = common.wait_for_element(device, tr_calendar_dict, "all_day_meeting_count")
    print("All day meeting count is:", element.text)
    common.wait_for_and_click(device, tr_calendar_dict, "all_day_meeting_right_arrow")
    common.get_all_elements_texts(device, calendar_dict, "meeting_title_name")


def teams_icon_visibility_for_future_meetings(device):
    print("device", device)
    driver = obj.device_store.get(alias=device)
    try:
        ele1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.ID, tr_calendar_dict["meeting_logo"]["id"]))
        )
        if ele1.is_displayed():
            print("Teams icon is visible")
    except Exception as e:
        print("Further meetings should not have Teams Icon")


def navigate_back_to_meetings(device):
    print("device", device)
    time.sleep(3)
    if not common.click_if_present(device, calls_dict, "Call_Back_Button"):
        common.wait_for_and_click(device, tr_calendar_dict, "all_day_meeting_left_arrow")
    common.wait_for_element(device, tr_home_screen_dict, "meeting_button")


def verify_background_display_of_all_day_meetings(device):
    tr_home_screen_keywords.verify_home_page_screen(device)
    common.wait_for_element(device, tr_calendar_dict, "title_bar")
    tap_on_all_day_meetings_title_bar_and_validate(device)
    verify_meeting_display_on_home_screen(device)
    settings_keywords.get_screenshot(name="verify_all_day_meeting_background")
    print(f"All day meeting are displayed with highlighted background")


def verify_functionality_of_whiteboard_tools(device):
    common.wait_for_and_click(device, tr_calls_dict, "black_pen_btn")
    common.wait_for_and_click(device, tr_calls_dict, "red_pen_btn")
    common.wait_for_and_click(device, tr_calls_dict, "galaxy_pen_btn")
    common.wait_for_and_click(device, tr_calls_dict, "highlighter_pen_btn")
    common.wait_for_and_click(device, tr_calls_dict, "eraser_btn")
    common.wait_for_and_click(device, tr_calls_dict, "add_text_btn")
    common.wait_for_and_click(device, tr_calendar_dict, "delete_text")
    common.wait_for_and_click(device, tr_calls_dict, "add_note_btn")


def remove_user_from_meeting_call(from_device, to_device, device_type=None):
    if device_type is not None and device_type.lower() != "console":
        raise AssertionError(f"Unexpected value for device type: {device_type}")
    print("from_device :", from_device)
    print("to_device :", to_device)
    account = "user"
    if ":" in to_device:
        user = to_device.split(":")[1]
        to_device = to_device.split(":")[0]
        print("User account : ", user)
        if user.lower() == "meeting_user":
            account = "meeting_user"
    print("Account :", account)
    common.wait_for_element(from_device, calendar_dict, "hang_up_btn")
    if device_type is not None and device_type.lower() == "console":
        if "console" in from_device:
            user_name = config["devices"][to_device][account]["displayname"]
        else:
            user_name = config["consoles"][to_device][account]["username"].split("@")[0]
            if not (
                common.click_if_present(from_device, calls_dict, "Add_participants_button")
                or common.click_if_present(from_device, calls_dict, "Add_participant_btn_portrait")
            ):
                raise AssertionError(f"{from_device} couldn't tap on add participants icon")
    else:
        user_name = config["devices"][to_device][account]["displayname"]
        if not (
            common.click_if_present(from_device, calls_dict, "Add_participants_button")
            or common.click_if_present(from_device, calls_dict, "Add_participant_btn_portrait")
        ):
            raise AssertionError(f"{from_device} couldn't tap on add participants icon")
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
    common.wait_for_and_click(from_device, tr_calendar_dict, "Remove_from_meeting")


def verify_someone_removed_you_from_the_meeting_call(device):
    common.wait_for_element(device, tr_calendar_dict, "someone_removed_you_from_the_call_text")


def farmute_the_call_and_validate(from_device, to_device):
    print("from_device :", from_device)
    print("to_device :", to_device)
    account = "user"
    if ":" in to_device:
        user = to_device.split(":")[1]
        to_device = to_device.split(":")[0]
        print("User account : ", user)
        if user.lower() == "meeting_user":
            account = "meeting_user"
    print("Account :", account)
    user_name = config["devices"][to_device][account]["displayname"]
    common.wait_for_element(from_device, calendar_dict, "hang_up_btn")
    time.sleep(5)
    if not common.is_element_present(from_device, tr_console_calendar_dict, "invite_someone_box", "id"):
        if not (
            common.click_if_present(from_device, calls_dict, "Add_participants_button")
            or common.click_if_present(from_device, calls_dict, "Add_participant_btn_portrait")
        ):
            raise AssertionError(f"{from_device} couldn't tap on add participants icon")
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
    common.wait_for_and_click(from_device, tr_calendar_dict, "far_mute_participant")


def select_raise_hand_option(device):
    common.sleep_with_msg(device, 5, "Waiting for call control bar display")
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_and_click(device, tr_calendar_dict, "call_control_reactions_button")
    common.wait_for_and_click(device, tr_calendar_dict, "raise_hand")


def verify_raise_hand_notification(device_list):
    devices = device_list.split(",")
    for device in devices:
        common.wait_for_element(device, tr_calendar_dict, "participant_raised_hand")
        print(f"Participant's raised hand is visible on {device}")


def select_lower_hand_option(device):
    common.sleep_with_msg(device, 5, "Waiting for call control bar display")
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_and_click(device, tr_calendar_dict, "call_control_reactions_button")
    common.wait_for_and_click(device, tr_calendar_dict, "lower_hand")


def verify_live_captions_visibility(device):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((MobileBy.ID, calls_dict["call_more_options"]["id"]))
    ).click()
    print("Clicked on Call more option")
    time.sleep(action_time)
    try:
        elem = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((MobileBy.XPATH, tr_calendar_dict["turn_on_live_captions"]["xpath"]))
        )
        if elem.is_displayed():
            print("Turn on live captions option is visble on the screen")
            for i in range(0, 2):
                settings_keywords.click_device_center_point(device)
    except Exception as e:
        raise AssertionError("Turn on live captions option is not visble on the screen")


def verify_whiteboard_sharing_support_device(device):
    print("device", device)
    driver = obj.device_store.get(alias=device)
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    elem = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((MobileBy.ID, calls_dict["call_more_options"]["id"]))
    )
    elem.click()
    print("Clicked on call more option")
    try:
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((MobileBy.XPATH, tr_calls_dict["share_whiteboard"]["xpath"]))
            )
        except Exception as e:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((MobileBy.XPATH, tr_calls_dict["share_whiteboard"]["xpath1"]))
            )
        print("Whiteboard share option is present under more option in call control")
        status = "pass"
    except Exception as e:
        status = "fail"
        print("Whiteboard share option is not present under more option in call control")
    settings_keywords.click_device_center_point(device)
    return status


def stop_recording(device):
    print("devcie", device)
    driver = obj.device_store.get(alias=device)
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    try:
        elem = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.ID, calls_dict["call_more_options"]["id"]))
        )
        elem.click()
        print("Clicked on call more option")
        stop = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.XPATH, tr_calendar_dict["stop_recording"]["xpath"]))
        )
        stop.click()
        print("Clicked on stop recording button")
    except Exception as e:
        raise AssertionError("stop recording button is not visible")


def verify_saved_chat_history_notification_display_on_screen(device_list):
    devices = device_list.split(",")
    for device in devices:
        print("device :", device)
        driver = obj.device_store.get(alias=device)
        try:
            try:
                WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable(
                        (MobileBy.XPATH, tr_calendar_dict["recording_notification_text"]["xpath"])
                    )
                )
            except Exception as e:
                WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable(
                        (MobileBy.XPATH, tr_calendar_dict["recording_notification_text"]["xpath1"])
                    )
                )
            print("Recording is saved in the chat history text is visible on the screen ")
        except Exception as e:
            raise AssertionError("Xpath not found")


def verify_text_editing_on_whiteboard_share_screen(device, text):
    common.wait_for_and_click(device, tr_calls_dict, "add_text_btn")
    common.sleep_with_msg(device, 5, "Allow soft keyboard to appear")
    common.hide_keyboard(device)
    print("text : ", text)
    common.wait_for_element(device, tr_calendar_dict, "text_field").send_keys(text)
    tmp_dict = common.get_dict_copy(tr_calendar_dict, "text_msg_xpath", "text_message", text)
    common.wait_for_element(device, tmp_dict, "text_msg_xpath")


def delete_text_from_whiteboard_sharing_screen(device, text):
    temp_dict = common.get_dict_copy(tr_calendar_dict, "text_msg_xpath", "text_message", text)
    common.wait_for_element(device, temp_dict, "text_msg_xpath")
    common.wait_for_and_click(device, tr_calendar_dict, "delete_text")


def verify_text_display_on_whiteboard_sharing_screen(devices, text):
    print("text :", text)
    devices = devices.split(",")
    for device in devices:
        print("device :", device)
        driver = obj.device_store.get(alias=device)
        try:
            try:
                text_result_xpath = (tr_calendar_dict["text_msg_xpath"]["xpath"]).replace("text_message", text)
                print("Search text result xpath : ", text_result_xpath)
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((MobileBy.XPATH, text_result_xpath)))
                print("Written text is visible on whiteboard share screen.", device)
            except Exception as e:
                print("Written text is not visible on the screen.", device)
        except Exception as e:
            raise AssertionError("Xpath not found.")


def verify_text_box_options_and_validate(device, text):
    temp_dict = common.get_dict_copy(tr_calendar_dict, "text_msg_xpath", "text_message", text)
    common.wait_for_and_click(device, temp_dict, "text_msg_xpath")
    common.wait_for_element(device, tr_calendar_dict, "edit_text_box")
    common.wait_for_element(device, tr_calendar_dict, "text_foreground_color_picker")
    common.wait_for_and_click(device, tr_calendar_dict, "delete_text")


def get_meeting_name(device):
    meeting_name_title = common.wait_for_element(device, calendar_dict, "meeting_title_name").text
    meeting_name = meeting_name_title.split()[0]
    print(f"Meeting name is : {meeting_name}")
    return meeting_name


def verify_meeting_name_on_homescreen_after_disabling(device, name_before_disable, name_post_disable):
    print("device:", device)
    print(f"Meeting name displayed on homescreen: {name_before_disable}")
    print(f"Organiser name displayed on homescreen: {name_post_disable}")
    if name_before_disable == name_post_disable:
        raise AssertionError(f"Meeting name is still displayed even after disabling show meeting name option")


def verify_live_captions_option_visibility(device):
    print("device:", device)
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_and_click(device, calls_dict, "call_more_options")
    common.wait_for_element(device, tr_calendar_dict, "turn_on_live_captions")
    # Click somewhere else on the screen to dismiss the more menu
    settings_keywords.click_device_center_point(device)


def tap_on_lock_meeting(device):
    print("device:", device)
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_and_click(device, calls_dict, "call_more_options")
    common.wait_for_and_click(device, tr_calendar_dict, "lock_the_meeting")
    common.wait_for_element(device, tr_calendar_dict, "meeting_lock_notification")


def verify_lock_meeting_visiblity(device_list, state):
    if state.lower() not in ["lock_meeting", "unlock_meeting"]:
        raise AssertionError(f"Unexpected value for state: {state}")
    print("state: ", state)
    devices = device_list.split(",")
    for device in devices:
        driver = obj.device_store.get(alias=device)
        print("device: ", device)
        common.wait_for_element(device, calendar_dict, "hang_up_btn")
        elem1 = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, calls_dict["call_more_options"]["id"]))
        )
        elem1.click()
        print("Clicked on Call more option")
        if state.lower() == "lock_meeting":
            try:
                e1 = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, tr_calendar_dict["lock_the_meeting"]["xpath"]))
                )
                if e1.is_displayed():
                    print("Lock the meeting option is visible on the screen: ", e1.text)
                else:
                    raise AssertionError("lock the meeting option is not visible on the screen")
                time.sleep(display_time)
                for i in range(0, 2):
                    settings_keywords.click_device_center_point(device)
                print("lock_the_meeting option is disappear now from screen")
            except Exception as e:
                raise AssertionError("Lock meeting option is not visible")
        elif state.lower() == "unlock_meeting":
            try:
                e2 = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, tr_calendar_dict["unlock_the_meeting"]["xpath"]))
                )
                if e2.is_displayed():
                    print("Unlock the meeting option is visible on the screen.")
                else:
                    raise AssertionError("Unlock the meeting option is not visible on the screen.")
                time.sleep(display_time)
                for i in range(0, 2):
                    settings_keywords.click_device_center_point(device)
                print("Unlock the meeting option is disappear.")
            except Exception as e:
                raise AssertionError("Unlock meeting option not visible")


def tap_on_unlock_meeting(device):
    print("device:", device)
    driver = obj.device_store.get(alias=device)
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    try:
        elem1 = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, calls_dict["call_more_options"]["id"]))
        )
        elem1.click()
        print("Clicked on Call more option")
        unlock_meeting = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.XPATH, tr_calendar_dict["unlock_the_meeting"]["xpath"]))
        )
        unlock_meeting.click()
        print("Clicked on Unlock the meeting option.")
        if common.is_norden(device):
            elm = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((MobileBy.ID, tr_calendar_dict["meeting_lock_notification"]["id"]))
            )
            if elm.is_displayed():
                print("Meeting unlocked pop is display on the screen: ", elm.text)
            else:
                raise Exception("Meeting unlocked pop is not displayed on the screen")
        else:
            pass
        time.sleep(display_time)
    except Exception as e:
        raise AssertionError("Xpath not found", e)


def verify_user_cannot_join_the_locked_meeting(device, meeting="test_meeting"):
    devices = device.split(",")
    for device in devices:
        calendar_keywords.join_meeting(device, meeting)
        if ":" in device:
            device = device.split(":")[0]
            print("device :", device)
        common.wait_for_element(device, tr_calendar_dict, "meeting_locked_msg")


def join_rooms_meeting(device, meeting=None, meeting_type="current"):
    if meeting is None:
        raise AssertionError(f"Meeting name is not specified to join")
    if meeting_type.lower() not in ["current", "upcoming"]:
        raise AssertionError(f"Unexpected value for meeting_type: {meeting_type}")
    devices = device.split(",")
    for device in devices:
        print("device :", device)
        if meeting_type == "upcoming":
            common.wait_for_and_click(device, calendar_dict, "join_upcoming_meeting_arrow")
            common.wait_for_and_click(device, calendar_dict, "upcoming_meeting_join_button")
        else:
            common.wait_for_and_click(device, calendar_dict, "cnf_device_join_button")
        common.sleep_with_msg(device, 5, "Wait for any 'allow' button to appear")
        common.click_if_present(device, calendar_dict, "allow_btn")
        if config["devices"][device]["model"].lower() == "santamonica":
            common.click_if_element_appears(device, device_settings_dict, "california_ok", max_attempts=5)
        common.wait_for_element(device, calendar_dict, "hang_up_btn")
        meeting_name = common.wait_for_element(device, tr_calendar_dict, "meeting_action_bar_title_text").text
        print(f"{device} : Meeting name is displayed on header: {meeting_name}")
        if meeting_name != meeting:
            raise AssertionError(
                f"{device}: Expected meeting name: {meeting} doesn't match with actual name : {meeting_name}"
            )


def open_dial_pad_from_call_control_bar(device):
    print("device:", device)
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_and_click(device, calls_dict, "call_more_options")
    common.wait_for_and_click(device, tr_calls_dict, "dial_pad")
    common.wait_for_element(device, calls_dict, "phone_number")
    common.wait_for_and_click(device, tr_calls_dict, "close_dial_pad_button")
    if "console" in device:
        tr_console_settings_keywords.tap_on_device_center_point(device)
    else:
        call_keywords.device_right_corner_click(device)


def verify_drag_and_drop_of_sticky_notes(device, text, source, destination):
    if source.lower() != "sticky_notes" or destination.lower() not in ["moving_up", "moving_down"]:
        raise AssertionError(
            f"{device}: Invalid values for source and destination combination - Source: {source}, Destination: {destination}"
        )
    devices = device.split(",")
    for device in devices:
        print("device :", device)
        driver = obj.device_store.get(alias=device)
        common.wait_for_and_click(device, tr_calls_dict, "add_note_btn")
        select_sticky_notes(device, "add_yellow_notes")
        common.wait_for_element(device, tr_calendar_dict, "text_field").send_keys(text)
        common.hide_keyboard(device)
        temp_dict = common.get_dict_copy(tr_calendar_dict, "text_msg_xpath", "text_msg_xpath", text)
        ele1 = common.wait_for_element(device, temp_dict, "text_msg_xpath")
        ele2 = common.wait_for_element(device, tr_calls_dict, "stop_presenting", "xpath")
        if destination.lower() == "moving_down":
            try:
                actions = TouchAction(driver)
                actions.long_press(ele1, duration=1000).move_to(y=100).release().perform()
            except Exception as e:
                raise Exception("Failed to drag and drop the sticky notes")
        elif destination.lower() == "moving_up":
            try:
                actions = TouchAction(driver)
                actions.long_press(ele1).move_to(ele2).release().perform()
            except Exception as e:
                raise Exception("Failed to drag and drop the sticky notes")
        print("Sucessfully dragged and dropped sticky notes from one location to another")


def select_sticky_notes(device, option):
    print("device :", device)
    print("option :", option)
    driver = obj.device_store.get(alias=device)
    if option.lower() in [
        "add_yellow_notes",
        "add_soft_orange_notes",
        "add_orange_notes",
        "add_soft_red_notes",
        "add_pink_notes",
        "add_green_notes",
        "add_soft_cyan_notes",
        "add_blue_notes",
        "add_soft_blue_notes",
        "add_violet_notes",
        "light_grey_notes",
        "grey_notes",
    ]:
        try:
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((MobileBy.XPATH, tr_calendar_dict[option.lower()]["xpath"]))
            ).click()
            print("Selected option is: ", option)
        except Exception as e:
            raise AssertionError("xpath not found")
    else:
        raise AssertionError("Please select proper sticky notes option.")


def delete_sticky_note_from_whiteboard_share_screen(device, text):
    print("device :", device)
    print("text :", text)
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, tr_calendar_dict["delete_text"]["xpath"]))
        ).click()
        print("Sticky note is deleted sucessfully.")
    except Exception as e:
        raise AssertionError("Xpath not found")


def verify_together_mode_and_validate(device):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.ID, tr_calls_dict["call_control_shared_mode_btn"]["id"]))
        ).click()
        print("Clicked on call_control_shared_mode_btn")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.XPATH, tr_calendar_dict["together_mode"]["xpath"]))
        ).click()
        print("Clicked on together mode button")
        print("We are in togther mode pls Check screenshot.")
        time.sleep(refresh_time)
        settings_keywords.get_screenshot(name="together_mode_screen")
    except Exception as e:
        raise AssertionError("Xpath not found")


def verify_gallery_mode_and_validate(device):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.ID, tr_calls_dict["call_control_shared_mode_btn"]["id"]))
        ).click()
        print("Clicked on call_control_shared_mode_btn")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.XPATH, tr_calendar_dict["gallery_mode"]["xpath"]))
        ).click()
        print("Clicked on gallary mode button")
        print("We are in gallery mode pls Check screenshot.")
        time.sleep(refresh_time)
        settings_keywords.get_screenshot(name="gallery_mode_screen")
    except Exception as e:
        raise AssertionError("Xpath not found")


def verify_large_gallery_mode_and_validate(device):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.ID, tr_calls_dict["call_control_shared_mode_btn"]["id"]))
        ).click()
        print("Clicked on call_control_shared_mode_btn")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.XPATH, tr_calendar_dict["large_gallery_mode"]["xpath"]))
        ).click()
        print("Clicked on Large gallary mode button")
        time.sleep(display_time)
        print("We are in Large gallery mode pls Check screenshot.")
        time.sleep(refresh_time)
        settings_keywords.get_screenshot(name="large_gallery_mode_screen")
    except Exception as e:
        raise AssertionError("Xpath not found")


def scroll_till_end_meeting_tab(device):
    driver = obj.device_store.get(alias=device)
    window_size = driver.get_window_size()
    print("Window size: ", window_size)
    height = window_size["height"]
    width = window_size["width"]
    print("Window Width and height :", width, height)
    driver.swipe(3 * (width / 4), 3 * (height / 4), 3 * (width / 4), 2 * (height / 6))
    time.sleep(action_time)
    driver.swipe(3 * (width / 4), 3 * (height / 4), 3 * (width / 4), 2 * (height / 6))


def scroll_up_meeting_tab(device):
    driver = obj.device_store.get(alias=device)
    container = common.wait_for_element(device, calendar_dict, "meeting_view")
    container_bounds = container.get_attribute("bounds").replace("][", ",").strip("]").strip("[").split(",")
    print(f"bounds: {container_bounds}")
    cont_cord = list(map(int, container_bounds))
    print(f"Container bounds: {cont_cord}")
    x1, y1 = cont_cord[2] - 30, cont_cord[3]
    x2, y2 = x1, cont_cord[1] + 50
    driver.swipe(x1, y1, x2, y2)
    print(f"{device}: Scrolled co-ordinates:({x1},{y1}), ({x2}, {y2})")


def verify_lock_meeting_option_should_not_visible_for_attendee(device):
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_and_click(device, calls_dict, "call_more_options")
    if common.is_element_present(device, tr_calendar_dict, "lock_the_meeting"):
        raise AssertionError(f"{device} : Lock meeting option is visible on screen of attendee")
    print(f"{device} : Lock meeting option is not visible on screen of attendee")
    call_keywords.dismiss_the_popup_screen(device)


def verify_lock_meeting_option_should_be_visible_for_presenter(device):
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_and_click(device, calls_dict, "call_more_options")
    if not common.is_element_present(device, tr_calendar_dict, "lock_the_meeting"):
        raise AssertionError(f"{device} : Lock meeting is not visible on the screen of presenter")
    print(f"{device} : Lock meeting is visible on the screen of presenter")
    call_keywords.device_right_corner_click(device)


def verify_meeting_names_show_meeting_organizer_name(device, user=None):
    print("Device :", device)
    if user is not None:
        if user.lower() == "pstn_user":
            account = "pstn_user"
        elif user.lower() == "meeting_user":
            account = "meeting_user"
        else:
            account = "user"
    else:
        account = "user"
    print("Account  :", account)
    driver = obj.device_store.get(alias=device)
    organizer_name = config["devices"][device][account]["displayname"]
    print("Organizer name is : ", organizer_name)
    meeting_name_title = common.wait_for_element(device, calendar_dict, "meeting_title_name").text
    print("meeting_title name  : ", meeting_name_title)
    meeting_name = meeting_name_title
    print("Meeting name is :", meeting_name)
    if organizer_name == meeting_name:
        print("Meeting name showing as the meeting organizer name")
    else:
        raise AssertionError("Meeting name is not showing as the meeting organizer name")


def verify_not_to_have_docked_ubar_options(device):
    if common.is_element_present(device, calls_dict, "Hang_up_button"):
        raise AssertionError(f" {device} : user is having the docked ubar options")


def verify_reaction_button_on_screen_after_tap_on_it(device):
    devices = device.split(",")
    for device in devices:
        common.wait_for_element(device, calendar_dict, "reaction")


def verify_manage_audio_and_video_options_in_participants(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    if not common.click_if_present(device, calls_dict, "Add_participants_button"):
        common.wait_for_and_click(device, tr_calls_dict, "Add_participants_btn")
    common.wait_for_and_click(device, tr_calls_dict, "participant_more_option")
    common.wait_for_element(device, calendar_dict, "manage_audio_and_video")
    common.wait_for_element(device, calendar_dict, "disable_mic_for_attendees")
    common.wait_for_element(device, calendar_dict, "disable_camera_for_attendees")
    common.wait_for_and_click(device, tr_calls_dict, "participant_settings_back_btn")
    tr_call_keywords.close_roaster_button_on_participants_screen(device)


def verify_reactions_buttons_in_call_control(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    common.wait_for_and_click(device, calendar_dict, "call_control_reactions_button")
    common.wait_for_element(device, calendar_dict, "icon_like")
    common.wait_for_element(device, calendar_dict, "icon_heart")
    common.wait_for_element(device, calendar_dict, "icon_applause")
    common.wait_for_element(device, calendar_dict, "icon_laugh")
    common.wait_for_element(device, calendar_dict, "raise_hand")
    print("Raise hand reaction buttons available")
    settings_keywords.click_device_center_point(device)
    print("Clicked on center point")


def tap_on_heart_button(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    common.wait_for_and_click(device, calendar_dict, "call_control_reactions_button")
    common.wait_for_and_click(device, calendar_dict, "icon_heart")


def tap_on_laugh_button(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    common.wait_for_and_click(device, calendar_dict, "call_control_reactions_button")
    common.wait_for_and_click(device, calendar_dict, "icon_laugh")


def tap_on_clap_button(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    common.wait_for_and_click(device, calendar_dict, "call_control_reactions_button")
    common.wait_for_and_click(device, calendar_dict, "icon_applause")


def click_like_button(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    if not common.click_if_present(device, tr_console_calendar_dict, "reactions_button"):
        common.wait_for_and_click(device, calendar_dict, "call_control_reactions_button")
    common.wait_for_and_click(device, calendar_dict, "icon_like")


def lower_the_raised_hand_from_another_user(from_device, to_device, device_type=None):
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
    print("to_device : ", to_device)
    if device_type is not None and device_type.lower() == "console":
        if "console" in from_device:
            user_name = config["devices"][to_device][account]["displayname"]
        else:
            user_name = config["consoles"][to_device][account]["username"].split("@")[0]
            if not (
                common.click_if_present(from_device, calls_dict, "Add_participants_button")
                or common.click_if_present(from_device, calls_dict, "Add_participant_btn_portrait")
            ):
                raise AssertionError(f"{from_device} couldn't tap on add participants icon")
    else:
        user_name = config["devices"][to_device][account]["displayname"]
        if not (
            common.click_if_present(from_device, calls_dict, "Add_participants_button")
            or common.click_if_present(from_device, calls_dict, "Add_participant_btn_portrait")
        ):
            raise AssertionError(f"{from_device} couldn't tap on add participants icon")
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
    common.wait_for_and_click(from_device, tr_calendar_dict, "lower_hand")
    time.sleep(3)
    common.click_if_present(from_device, tr_calls_dict, "close_roaster_button")


def verify_whiteboard_visibility_for_all_participants(device_list):
    device_list = device_list.split(",")
    for devices in device_list:
        account = "user"
        device = devices
        if ":" in devices:
            user = devices.split(":")[1]
            print("User account : ", user)
            if user.lower() == "pstn_user":
                account = "pstn_user"
            elif user.lower() == "meeting_user":
                account = "meeting_user"
            device = devices.split(":")[0]
        print("account : ", account)
        print("device : ", device)
        if account in ["pstn_user"]:
            common.wait_for_element(device, tr_calls_dict, "Whiteboard")
        else:
            common.wait_for_element(device, tr_calls_dict, "Whiteboard")
            if not common.is_element_present(device, tr_calls_dict, "canvas_lasso_select"):
                common.wait_for_element(device, tr_calls_dict, "canvas_view")


def verify_not_to_have_manage_audio_and_video_option(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    if not common.click_if_present(device, calls_dict, "Add_participants_button"):
        common.wait_for_and_click(device, tr_calls_dict, "Add_participants_btn")
    if common.is_element_present(device, tr_calls_dict, "participant_more_option"):
        raise AssertionError(f"{device} user able to see the manage audio and video option")
    tr_call_keywords.close_roaster_button_on_participants_screen(device)


def verify_pin_icon(device):
    time.sleep(5)
    if not common.is_element_present(device, tr_console_calendar_dict, "invite_someone_box"):
        calendar_keywords.navigate_to_add_participant_page(device)
    common.wait_for_element(device, tr_calendar_dict, "verify_pin")
    time.sleep(3)
    if not common.is_element_present(device, tr_console_calendar_dict, "invite_someone_box"):
        common.wait_for_and_click(device, tr_calls_dict, "close_roaster_button")


def verify_spotlight_icon_disable(device):
    time.sleep(5)
    if not common.is_element_present(device, tr_console_calendar_dict, "invite_someone_box"):
        calendar_keywords.navigate_to_add_participant_page(device)
    if common.is_element_present(device, tr_calendar_dict, "participant_spotlight"):
        raise AssertionError(f"{device} spotlight icon is persent")
    time.sleep(3)
    if not common.is_element_present(device, tr_console_calendar_dict, "invite_someone_box"):
        common.wait_for_and_click(device, tr_calls_dict, "close_roaster_button")


def verify_pin_icon_disable(device):
    calendar_keywords.navigate_to_add_participant_page(device)
    if common.is_element_present(device, tr_calendar_dict, "verify_pin"):
        raise AssertionError(f"{device} spotlight icon is persent")
    common.wait_for_and_click(device, tr_calendar_dict, "close")


def verify_spotlight_text_on_device(device, text):
    if text.lower() not in ["spotlight", "no_spotlight"]:
        raise AssertionError(f"{device} Illegal value for the text:{text}")
    test = common.wait_for_element(device, tr_calendar_dict, "you_are_spotlighted", "id").text
    if text == "spotlight":
        if test.lower() != "you're spotlighted":
            raise AssertionError(f"spotlight : {test} text is not visible on the {device}")
    elif text == "no_spotlight":
        if test.lower() != "you're no longer spotlighted":
            raise AssertionError(f"no_spotlight : {test} text is not visible on the {device}")


def verify_spotlight_icon(device):
    time.sleep(5)
    if not common.is_element_present(device, tr_console_calendar_dict, "invite_someone_box"):
        calendar_keywords.navigate_to_add_participant_page(device)
    common.wait_for_element(device, tr_calendar_dict, "participant_spotlight")
    time.sleep(3)
    if not common.is_element_present(device, tr_console_calendar_dict, "invite_someone_box"):
        common.wait_for_and_click(device, tr_calls_dict, "close_roaster_button")


def verify_spotlight_icon_user_is_attendee(device):
    if not common.click_if_present(device, calls_dict, "participants_roster_button"):
        common.wait_for_and_click(device, calls_dict, "Add_participants_button")
    common.wait_for_element(device, tr_calendar_dict, "participant_spotlight")
    if common.is_element_present(device, tr_calls_dict, "add_participants"):
        raise AssertionError(f"{device} add participants button is present for when user is attendee")
    common.wait_for_and_click(device, tr_calls_dict, "close_roaster_button")


def spotlight_icon_should_not_present(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    calendar_keywords.navigate_to_add_participant_page(device)
    if common.is_element_present(device, tr_calendar_dict, "participant_spotlight"):
        raise AssertionError(f"{device} spotlight icon is persent")
    if not common.is_element_present(device, tr_console_calendar_dict, "invite_someone_box"):
        common.wait_for_and_click(device, tr_calls_dict, "close_roaster_button")


def remove_spotlight_from_other_user(from_device, to_device, device_type=None, action_type="Modify"):
    if device_type is not None and device_type.lower() != "console":
        raise AssertionError(f"Unexpected value for device type: {device_type}")
    if action_type.lower() not in ["modify", "verify"]:
        raise AssertionError(f"Unexpected value for action type: {action_type}")
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
    print("to_device : ", to_device)
    common.wait_for_element(from_device, calendar_dict, "hang_up_btn")
    if device_type is not None and device_type.lower() == "console":
        if "console" in from_device:
            user_name = config["devices"][to_device][account]["displayname"]
        else:
            user_name = config["consoles"][to_device][account]["username"].split("@")[0]
            if not (
                common.click_if_present(from_device, calls_dict, "Add_participants_button")
                or common.click_if_present(from_device, calls_dict, "Add_participant_btn_portrait")
            ):
                raise AssertionError(f"{from_device} couldn't tap on add participants icon")
    else:
        user_name = config["devices"][to_device][account]["displayname"]
        if not (
            common.click_if_present(from_device, calls_dict, "Add_participants_button")
            or common.click_if_present(from_device, calls_dict, "Add_participant_btn_portrait")
        ):
            raise AssertionError(f"{from_device} couldn't tap on add participants icon")
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
    if action_type is not None and action_type.lower() == "verify":
        common.wait_for_and_click(from_device, tr_calendar_dict, "stop_spotlight")
        common.wait_for_element(from_device, tr_calendar_dict, "stop_spotlight_pop_up_message")
        common.wait_for_element(from_device, tr_calendar_dict, "stop_spotlight_ok_btn")
        common.wait_for_and_click(from_device, tr_calendar_dict, "stop_spot_light_cancel_button")
        return
    common.wait_for_and_click(from_device, tr_calendar_dict, "stop_spotlight")
    common.wait_for_element(from_device, tr_calendar_dict, "stop_spotlight_pop_up_message")
    common.wait_for_element(from_device, tr_calendar_dict, "stop_spot_light_cancel_button")
    common.wait_for_and_click(from_device, tr_calendar_dict, "stop_spotlight_ok_btn")


def make_a_pin(from_device, to_device, device_type=None):
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
    print("to_device : ", to_device)
    common.wait_for_element(from_device, calendar_dict, "hang_up_btn")
    if device_type is not None and device_type.lower() == "console":
        if "console" in from_device:
            user_name = config["devices"][to_device][account]["displayname"]
        else:
            user_name = config["consoles"][to_device][account]["username"].split("@")[0]
            if not (
                common.click_if_present(from_device, calls_dict, "Add_participants_button")
                or common.click_if_present(from_device, calls_dict, "Add_participant_btn_portrait")
            ):
                raise AssertionError(f"{from_device} couldn't tap on add participants icon")
    else:
        user_name = config["devices"][to_device][account]["displayname"]
        if not (
            common.click_if_present(from_device, calls_dict, "Add_participants_button")
            or common.click_if_present(from_device, calls_dict, "Add_participant_btn_portrait")
        ):
            raise AssertionError(f"{from_device} couldn't tap on add participants icon")
    ele_text = common.wait_for_element(
        from_device, calendar_dict, "add_user", "id", cond=EC.presence_of_all_elements_located
    )
    participant_list = [str(i.text) for i in ele_text]
    print(f"participant list :", participant_list)
    user_position = 0
    for _user in participant_list:
        if _user.lower() == user_name:
            user_position = participant_list.index(_user)
            print(f"expected user to click:", _user)
    ele_text[user_position].click()
    common.wait_for_and_click(from_device, calendar_dict, "pin_for_me")


def make_a_spotlight(from_device, to_device, device_type=None, action_type="Modify"):
    if device_type is not None and device_type.lower() != "console":
        raise AssertionError(f"Unexpected value for device type: {device_type}")
    if action_type.lower() not in ["modify", "verify"]:
        raise AssertionError(f"Unexpected value for action type: {action_type}")
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
    print("to_device : ", to_device)
    common.wait_for_element(from_device, calendar_dict, "hang_up_btn")
    if device_type is not None and device_type.lower() == "console":
        if "console" in from_device:
            user_name = config["devices"][to_device][account]["displayname"]
        else:
            user_name = config["consoles"][to_device][account]["username"].split("@")[0]
            if not (
                common.click_if_present(from_device, calls_dict, "Add_participants_button")
                or common.click_if_present(from_device, calls_dict, "Add_participant_btn_portrait")
            ):
                raise AssertionError(f"{from_device} couldn't tap on add participants icon")
    else:
        user_name = config["devices"][to_device][account]["displayname"]
        if not (
            common.click_if_present(from_device, calls_dict, "Add_participants_button")
            or common.click_if_present(from_device, calls_dict, "Add_participant_btn_portrait")
        ):
            raise AssertionError(f"{from_device} couldn't tap on add participants icon")
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
    if action_type is not None and action_type.lower() == "verify":
        common.wait_for_and_click(from_device, tr_calendar_dict, "spotlight_for_everyone")
        common.wait_for_element(from_device, tr_calendar_dict, "spotlight_popup_dscrpt")
        common.wait_for_element(from_device, calendar_dict, "spotlight")
        common.wait_for_and_click(from_device, tr_calendar_dict, "stop_spot_light_cancel_button")
        return
    if common.is_element_present(from_device, tr_calendar_dict, "spotlight_for_everyone"):
        common.wait_for_and_click(from_device, tr_calendar_dict, "spotlight_for_everyone")
    else:
        common.wait_for_and_click(from_device, tr_calendar_dict, "add_spotlight")
    common.wait_for_and_click(from_device, calendar_dict, "spotlight")
    # common.wait_for_and_click(from_device, tr_calendar_dict, "close")


def verify_whiteboard_sharing_option_on_call_control_bar(device):
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_and_click(device, tr_calendar_dict, "share_button")
    common.wait_for_element(device, tr_calendar_dict, "Microsoft_whiteboard_sharing")
    if "console" in device:
        tr_console_settings_keywords.tap_on_device_right_corner(device)
    else:
        call_keywords.device_right_corner_click(device)


def verify_options_visible_after_making_an_attendee(from_device, to_device, device_type=None):
    if device_type is not None and device_type.lower() != "console":
        raise AssertionError(f"Unexpected value for device type: {device_type}")
    print("from_device :", from_device)
    print("to_device :", to_device)
    to_devices = to_device.split(",")
    for to_device in to_devices:
        account = "user"
        if ":" in to_device:
            user = to_device.split(":")[1]
            print("User account : ", user)
            if user.lower() == "meeting_user":
                account = "meeting_user"
        print("Account :", account)
        to_device = to_device.split(":")[0]
        print("to_device : ", to_device)
        common.wait_for_element(from_device, calendar_dict, "hang_up_btn")
        if device_type is not None and device_type.lower() == "console":
            if "console" in from_device:
                user_name = config["devices"][to_device][account]["displayname"]
            else:
                user_name = config["consoles"][to_device][account]["username"].split("@")[0]
                if not (
                    common.click_if_present(from_device, calls_dict, "Add_participants_button")
                    or common.click_if_present(from_device, calls_dict, "Add_participant_btn_portrait")
                ):
                    raise AssertionError(f"{from_device} couldn't tap on add participants icon")
        else:
            user_name = config["devices"][to_device][account]["displayname"]
            if not (
                common.click_if_present(from_device, calls_dict, "Add_participants_button")
                or common.click_if_present(from_device, calls_dict, "Add_participant_btn_portrait")
            ):
                raise AssertionError(f"{from_device} couldn't tap on add participants icon")
        ele_text = common.wait_for_element(
            from_device, calendar_dict, "add_user", "id", cond=EC.presence_of_all_elements_located
        )
        participant_list = [str(i.text) for i in ele_text]
        print("user names are:", participant_list)
        user_position = 0
        for _user in participant_list:
            if _user.lower() == user_name.lower():
                user_position = participant_list.index(_user)
                print(f"expected user to click:", _user)
        ele_text[user_position].click()
        common.wait_for_element(from_device, calendar_dict, "spotlight_for_everyone")
        common.wait_for_element(from_device, calendar_dict, "pin_for_me")
        common.wait_for_element(from_device, calendar_dict, "make_an_presenter")
        common.wait_for_element(from_device, calendar_dict, "remove_from_meeting")
        if not common.is_element_present(from_device, tr_calendar_dict, "Disable_camera"):
            common.wait_for_element(from_device, tr_calendar_dict, "allow_camera")
        if not common.is_element_present(from_device, tr_calendar_dict, "Disable_mic"):
            common.wait_for_element(from_device, calendar_dict, "allow_mic")


def disable_and_allow_camera_options_for_attendees(from_device, to_device, camera):
    if camera.lower() not in ["allow", "disable"]:
        raise AssertionError(f"Unexpected state for  camera: {camera}")
    if ":" in to_device:
        to_device = to_device.split(":")[0]
    if camera.lower() == "disable":
        common.wait_for_and_click(from_device, tr_calendar_dict, "Disable_camera")
        common.wait_for_element(to_device, tr_calendar_dict, "Camera_disabled")
    elif camera.lower() == "allow":
        common.wait_for_and_click(from_device, tr_calendar_dict, "allow_camera")
        common.wait_for_element(to_device, tr_calls_dict, "video_on")
    time.sleep(5)
    common.click_if_present(from_device, tr_calls_dict, "close_roaster_button")
    common.wait_for_element(from_device, calls_dict, "Hang_up_button")


def disable_and_allow_mic_options_for_attendees(from_device, to_device, mic):
    if mic.lower() not in ["allow", "disable"]:
        raise AssertionError(f"Unexpected state for mic: {mic}")
    if ":" in to_device:
        to_device = to_device.split(":")[0]
    if mic.lower() == "disable":
        common.wait_for_and_click(from_device, tr_calendar_dict, "Disable_mic")
        common.wait_for_element(to_device, calendar_dict, "disabled_mic")
    elif mic.lower() == "allow":
        common.wait_for_and_click(from_device, calendar_dict, "allow_mic")
        common.wait_for_element(to_device, calendar_dict, "call_control_mute")
    time.sleep(5)
    common.click_if_present(from_device, tr_calls_dict, "close_roaster_button")
    common.wait_for_element(from_device, calls_dict, "Hang_up_button")


def add_participants_button_not_present(device):
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_and_click(device, calls_dict, "Add_participants_button")
    if common.is_element_present(device, tr_calls_dict, "add_participants"):
        raise AssertionError(f"{device} add participants button is present")


def disable_and_enable_camera_for_attendees(from_device, to_device, state):
    if state.lower() not in ["on", "off"]:
        raise AssertionError(f"Unexpected state for camera: {state}")
    if not common.click_if_present(from_device, calls_dict, "Add_participants_button"):
        common.click_if_present(from_device, calls_dict, "Add_participant_btn_portrait")
    common.wait_for_and_click(from_device, tr_calls_dict, "participant_more_option")
    common.change_toggle_button(from_device, calendar_dict, "video_toggle_button", state)
    if state.lower() == "on":
        common.wait_for_element(to_device, calendar_dict, "your_camera_has_been_disabled")
        common.wait_for_element(to_device, tr_calendar_dict, "Camera_disabled", "xpath1")
    elif state.lower() == "off":
        common.wait_for_element(to_device, tr_calendar_dict, "video_off")
    common.wait_for_and_click(from_device, tr_calls_dict, "participant_settings_back_btn")
    time.sleep(5)
    if not common.is_element_present(from_device, tr_console_calendar_dict, "invite_someone_box"):
        common.wait_for_and_click(from_device, tr_calls_dict, "close_roaster_button")


def verify_farmute_text_on_device(device, text):
    ele = common.wait_for_element(device, tr_calendar_dict, "you_have_muted").text
    if ele.lower() != text:
        raise AssertionError(f"{device} : user muted {text}is not expected as{ele}")


def verify_mute_off_icon(device):
    common.wait_for_element(device, tr_calendar_dict, "mute_off_icon")


def verify_mic_camera_in_participants_list(device):
    print("Device : ", device)
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    time.sleep(5)
    if not common.is_element_present(device, tr_calls_dict, "participant_more_option"):
        if not common.click_if_present(device, calls_dict, "Add_participants_button"):
            common.wait_for_and_click(device, tr_calls_dict, "Add_participants_btn")
    common.wait_for_element(device, tr_calls_dict, "Participants_label")
    common.wait_for_element(device, tr_calls_dict, "participant_mute")
    common.wait_for_element(device, tr_calendar_dict, "participant_video")
    if not common.click_if_present(device, tr_calls_dict, "close_roaster_button"):
        common.wait_for_and_click(device, common_dict, "back")


def verify_send_feedback_text(device):
    common.wait_for_element(device, tr_calendar_dict, "report_an_issue_feedback")


def verify_meeting_name_on_homescreen_enabled_state(device, name_before_disable, name_on_enable_state):
    print("device:", device)
    print(f"Meeting name displayed on homescreen: {name_before_disable}")
    print(f"Organiser name displayed on homescreen: {name_on_enable_state}")
    if not name_before_disable == name_on_enable_state:
        raise AssertionError(f"Meeting name is still displayed even after disabling show meeting name option")


def disable_and_enable_mic_for_attendees(from_device, to_device, state):
    if state.lower() not in ["on", "off"]:
        raise AssertionError(f"Unexpected state for mic: {state}")
    if not common.click_if_present(from_device, calls_dict, "Add_participants_button"):
        common.click_if_present(from_device, calls_dict, "Add_participant_btn_portrait")
    common.wait_for_and_click(from_device, tr_calls_dict, "participant_more_option")
    common.change_toggle_button(from_device, calendar_dict, "audio_toggle_button", state)
    if state.lower() == "on":
        common.wait_for_element(to_device, calendar_dict, "your_mic_has_been_disabled")
        common.wait_for_element(to_device, calendar_dict, "disabled_mic")
    if state.lower() == "off":
        common.wait_for_element(to_device, calls_dict, "call_verify_muted")
    common.wait_for_and_click(from_device, tr_calls_dict, "participant_settings_back_btn")
    time.sleep(5)
    if not common.is_element_present(from_device, tr_console_calendar_dict, "invite_someone_box"):
        common.wait_for_and_click(from_device, tr_calls_dict, "close_roaster_button")


def verifying_and_removing_spotlight(device):
    device = device.split(":")[0]
    print("device : ", device)
    account = "user"
    if ":" in device:
        user = device.split(":")[1]
        print("User account : ", user)
        if user.lower() == "meeting_user":
            account = "meeting_user"
    print("Account :", account)
    if "console" in device:
        user_name = config["consoles"][device][account]["displayname"]
    else:
        user_name = config["devices"][device][account]["displayname"]
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    if "console" not in device:
        if not (
            common.click_if_present(device, calls_dict, "Add_participants_button")
            or common.click_if_present(device, calls_dict, "Add_participant_btn_portrait")
        ):
            raise AssertionError(f"{device} couldn't tap on add participants icon")
    ele_text = common.wait_for_element(
        device, calendar_dict, "add_user", "id", cond=EC.presence_of_all_elements_located
    )
    participant_list = [str(i.text) for i in ele_text]
    print(f"participant list :", participant_list)
    user_position = 0
    for _user in participant_list:
        if _user.lower() == user_name:
            user_position = participant_list.index(_user)
            print(f"expected user to click:", _user)
    ele_text[user_position].click()
    common.wait_for_and_click(device, tr_calendar_dict, "stop_spotlight")
    common.wait_for_and_click(device, tr_calendar_dict, "stop_spotlight_ok_btn")


def verify_whiteboard_sharing_is_disconnected(device):
    if common.is_element_present(device, tr_calls_dict, "canvas_toolbar"):
        raise AssertionError(f"{device} whiteboard sharing is persent on the screen")


def verify_reaction_window_will_dissmiss(device):
    if common.is_element_present(device, calendar_dict, "icon_heart"):
        raise AssertionError(f"{device} reaction window is present on the screen")


def disable_camera_for_attendees_avatar(device):
    common.wait_for_element(device, tr_calendar_dict, "Camera_disabled")


def block_the_numbers(from_device, to_device):
    print("from_device :", from_device)
    print("to_device :", to_device)
    account = "user"
    if ":" in to_device:
        user = to_device.split(":")[1]
        print("User account : ", user)
        account = None
        if user.lower() == "pstn_user":
            account = "pstn_user"
        elif user.lower() == "meeting_user":
            account = "meeting_user"
    print("Account :", account)
    blocked_device_num = config["devices"][to_device][account]["phonenumber"]
    common.wait_for_element(from_device, tr_settings_dict, "calling_button_text")
    tr_call_keywords.swipe_till_end_page(from_device)
    common.wait_for_and_click(from_device, tr_settings_dict, "Blocked_numbers")
    common.wait_for_and_click(from_device, tr_settings_dict, "Add_number")
    common.wait_for_and_click(from_device, tr_settings_dict, "Block_number_field")
    blocknum = common.wait_for_element(from_device, tr_settings_dict, "Block_number_field")
    blocknum.send_keys(blocked_device_num)
    common.wait_for_and_click(from_device, tr_settings_dict, "block_ok_button")
    common.wait_for_element(from_device, tr_settings_dict, "blocked_list")
    call_keywords.device_right_corner_click(from_device)
    if not common.click_if_present(from_device, tr_calls_dict, "close_roaster_button"):
        common.wait_for_and_click(from_device, common_dict, "back")


def verify_lock_meeting_is_not_present(device):
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_and_click(device, calls_dict, "call_more_options")
    if common.is_element_present(device, tr_calendar_dict, "lock_the_meeting"):
        raise AssertionError(f"{device} lock meeting option is present")
    call_keywords.dismiss_the_popup_screen(device)


def check_user_options_after_making_an_attendee(from_device, to_device):
    verify_options_visible_after_making_an_attendee(from_device, to_device)
    call_keywords.dismiss_the_popup_screen(from_device)


def verify_raise_hand_should_not_be_displayed_on_dockedubar(device):
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_and_click(device, calls_dict, "call_more_options")
    if common.is_element_present(device, tr_calendar_dict, "raise_hand"):
        raise AssertionError(f"{device} rais hand option is present in docked Ubar")
    call_keywords.dismiss_the_popup_screen(device)


def verify_join_with_an_meeting_id_options(device):
    click_on_join_by_id(device)
    common.wait_for_element(device, tr_calendar_dict, "join_with_a_meeting_ID")
    common.wait_for_element(device, tr_calendar_dict, "meeting_id_field")
    common.wait_for_element(device, tr_calendar_dict, "passcode_field")
    common.wait_for_element(device, tr_calendar_dict, "join_meeting")


def verify_join_with_an_meeting_id_options_after_enabling_third_party_meetings(device):
    click_on_join_by_id(device)
    common.wait_for_and_click(device, tr_device_settings_dict, "Teams")
    common.wait_for_element(device, tr_calendar_dict, "zoom_button")
    common.wait_for_and_click(device, tr_console_settings_dict, "back_layout")


def verify_the_join_by_id_on_home_seceen_when_zoom_meeting_toggle_is_disabled(device):
    click_on_join_by_id(device)
    common.wait_for_element(device, tr_calendar_dict, "join_with_a_meeting_ID")
    common.wait_for_element(device, tr_calendar_dict, "meeting_id_field")
    common.wait_for_element(device, tr_calendar_dict, "passcode_field")
    common.wait_for_element(device, tr_calendar_dict, "join_meeting")
    if common.is_element_present(device, tr_calendar_dict, "Change_provider"):
        raise AssertionError(f"{device} change provider is present in join by id")
    common.click_if_present(device, tr_console_settings_dict, "back_layout")


def join_with_an_meeting_id(device, meeting_type="teams"):
    if meeting_type.lower() not in ["teams", "zoom"]:
        raise AssertionError(f"Unexpected state for meeting_type: {meeting_type}")
    click_on_join_by_id(device)
    common.wait_for_element(device, tr_calendar_dict, "join_with_a_meeting_ID")
    if meeting_type.lower() == "teams":
        common.sleep_with_msg(device, 5, "waiting for the until teams launch")
        # when we will enable the zooom toggle only we will get the zoom btn
        if common.is_element_present(device, tr_calendar_dict, "zoom_button"):
            common.wait_for_and_click(device, tr_device_settings_dict, "Teams")
            common.wait_for_and_click(device, tr_calendar_dict, "Next")
        meeting_id_field = common.wait_for_element(device, tr_calendar_dict, "meeting_id_field")
        meeting_id_field.send_keys(config["meeting_details"]["meeting_id"])
        meeting_passcode = common.wait_for_element(device, tr_calendar_dict, "passcode_field")
        meeting_passcode.send_keys(config["meeting_details"]["meeting_passcode"])
        common.wait_for_and_click(device, tr_calendar_dict, "join_meeting")

    elif meeting_type.lower() == "zoom":
        common.wait_for_element(device, tr_calendar_dict, "join_with_a_meeting_ID")
        common.wait_for_and_click(device, tr_calendar_dict, "zoom_button")
        common.wait_for_and_click(device, tr_calendar_dict, "Next")
        meeting_id_field = common.wait_for_element(device, tr_calendar_dict, "meeting_id_field")
        meeting_id_field.send_keys(config["zoom_meeting_details"]["meeting_id"])
        meeting_passcode = common.wait_for_element(device, tr_calendar_dict, "passcode_field")
        meeting_passcode.send_keys(config["zoom_meeting_details"]["meeting_passcode"])
        common.wait_for_and_click(device, tr_calendar_dict, "join_zooom_meeting_button")


def join_with_an_meeting_id_with_extend_meeting_details(device):
    click_on_join_by_id(device)
    common.wait_for_element(device, tr_calendar_dict, "join_with_a_meeting_ID")
    meeting_id_field = common.wait_for_element(device, tr_calendar_dict, "meeting_id_field")
    meeting_id_field.send_keys(config["extend_meeting_details"]["meeting_id"])
    meeting_passcode = common.wait_for_element(device, tr_calendar_dict, "passcode_field")
    meeting_passcode.send_keys(config["extend_meeting_details"]["meeting_passcode"])
    common.wait_for_and_click(device, tr_calendar_dict, "join_meeting")


def verify_join_meeting_ID_with_less_than_and_greater_than_7_digit_number(device):
    click_on_join_by_id(device)
    common.wait_for_element(device, tr_calendar_dict, "join_with_a_meeting_ID")
    meeting_id_field = common.wait_for_element(device, tr_calendar_dict, "meeting_id_field")
    meeting_id_field.send_keys(config["meeting_details"]["meeting_id"])
    elem = common.wait_for_element(device, tr_calendar_dict, "join_meeting")
    temp = elem.get_attribute("enabled")
    if temp == "false":
        raise AssertionError(f"{device}:join meeting button is in disable state")
    seven_digit_number = config["meeting_details"]["meeting_id"]
    common.wait_for_element(device, tr_calendar_dict, "meeting_id_field").clear()
    seven_digit_number = seven_digit_number[:7]
    print(seven_digit_number, "7digit number")
    common.wait_for_element(device, tr_calendar_dict, "meeting_id_field").send_keys(seven_digit_number)
    elem = common.wait_for_element(device, tr_calendar_dict, "join_meeting")
    temp = elem.get_attribute("enabled")
    if temp != "false":
        raise AssertionError(f"{device}:join meeting button is in enabled state")


def verify_that_user_enter_only_meeting_passcode(device):
    click_on_join_by_id(device)
    common.wait_for_element(device, tr_calendar_dict, "join_with_a_meeting_ID")
    meeting_passcode = common.wait_for_element(device, tr_calendar_dict, "passcode_field")
    meeting_passcode.send_keys(config["meeting_details"]["meeting_passcode"])
    elem = common.wait_for_element(device, tr_calendar_dict, "join_meeting")
    temp = elem.get_attribute("enabled")
    if temp != "false":
        raise AssertionError(f"{device}:join meeting button is in enabled state")


def verify_invalid_number_and_edit_the_meeting_id_and_passcode(device):
    click_on_join_by_id(device)
    common.wait_for_element(device, tr_calendar_dict, "join_with_a_meeting_ID")
    meeting_id_field = common.wait_for_element(device, tr_calendar_dict, "meeting_id_field")
    meeting_id_field.send_keys(config["meeting_details"]["invalid_meeting_id"])
    meeting_passcode = common.wait_for_element(device, tr_calendar_dict, "passcode_field")
    meeting_passcode.send_keys(config["meeting_details"]["invalid_passcode"])
    common.wait_for_and_click(device, tr_calendar_dict, "join_meeting")
    common.wait_for_element(device, tr_calendar_dict, "invalid_credentials_popup")
    elem = common.wait_for_element(device, tr_calendar_dict, "Retry")
    temp = elem.get_attribute("enabled")
    if temp != "false":
        raise AssertionError(f"{device}:Retry button is in enabled state")
    meeting_id = config["meeting_details"]["meeting_id"]
    editing_meeting_id = meeting_id[:6]
    common.wait_for_element(device, tr_calendar_dict, "meeting_id_field").send_keys(editing_meeting_id)
    passcode = config["meeting_details"]["meeting_passcode"]
    editing_passcode = passcode[:6]
    common.wait_for_element(device, tr_calendar_dict, "passcode_field").send_keys(editing_passcode)
    time.sleep(action_time)
    common.wait_for_element(device, tr_calendar_dict, "Retry")


def verify_Join_meeting_with_incorrect_meeting_detail(device, expected_result="success", meeting_type="teams"):
    if meeting_type.lower() not in ["teams", "zoom"]:
        raise AssertionError(f"Unexpected state for meeting_type: {meeting_type}")
    click_on_join_by_id(device)
    common.wait_for_element(device, tr_calendar_dict, "join_with_a_meeting_ID")
    if meeting_type.lower() == "teams":
        common.sleep_with_msg(device, 5, "waiting for the until teams launch")
        # when we will enable the zooom toggle only we will get the zoom btn
        if common.is_element_present(device, tr_calendar_dict, "zoom_button"):
            common.wait_for_and_click(device, tr_device_settings_dict, "Teams")
            common.wait_for_and_click(device, tr_calendar_dict, "Next")
        meeting_id = common.wait_for_element(device, tr_calendar_dict, "meeting_id_field")
        meeting_id.send_keys(config["meeting_details"]["invalid_meeting_id"])
        meeting_passcode = common.wait_for_element(device, tr_calendar_dict, "passcode_field")
        meeting_passcode.send_keys(config["meeting_details"]["invalid_passcode"])

    elif meeting_type.lower() == "zoom":
        common.sleep_with_msg(device, 5, "waiting for the until zoom launch")
        common.wait_for_and_click(device, tr_calendar_dict, "zoom_button")
        common.wait_for_and_click(device, tr_calendar_dict, "Next")
        meeting_id_field = common.wait_for_element(device, tr_calendar_dict, "meeting_id_field")
        meeting_id_field.send_keys(config["zoom_meeting_details"]["invalid_meeting_id"])
        meeting_passcode = common.wait_for_element(device, tr_calendar_dict, "passcode_field")
        meeting_passcode.send_keys(config["zoom_meeting_details"]["invalid_passcode"])

    if expected_result.lower() == "success":
        common.sleep_with_msg(device, 5, "waiting for the until call complete")
        if meeting_type.lower() == "teams":
            common.wait_for_and_click(device, tr_calendar_dict, "join_meeting")
            common.wait_for_element(device, tr_calendar_dict, "invalid_credentials_popup")
        elif meeting_type.lower() == "zoom":
            common.wait_for_and_click(device, tr_calendar_dict, "join_zooom_meeting_button")
            common.wait_for_element(device, tr_calendar_dict, "invalid_credentials_zoom_popup")
            common.wait_for_and_click(device, tr_calendar_dict, "cancel")
            if not common.click_if_present(device, tr_calls_dict, "close_roaster_button"):
                common.wait_for_and_click(device, tr_console_settings_dict, "back_layout")


def verify_meeting_info_options_when_user_join_a_meeting(device):
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_and_click(device, calls_dict, "call_more_options")
    common.wait_for_and_click(device, tr_calendar_dict, "Meeting_info")
    common.wait_for_element(device, tr_calendar_dict, "Meeting_info_field")
    common.wait_for_element(device, tr_calendar_dict, "info_meeting_id")
    common.wait_for_element(device, tr_calendar_dict, "info_passcode_field")
    common.wait_for_element(device, tr_calendar_dict, "conference_id")


def verify_meeting_field_should_not_accept_alphabets_for_meeting_id(device):
    if "console" in device:
        device_name = "consoles"
    else:
        device_name = "devices"
    verify_join_with_an_meeting_id_options(device)
    subprocess.call(
        "adb -s {} shell input keyevent 48".format(config[device_name][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    subprocess.call(
        "adb -s {} shell input keyevent 33".format(config[device_name][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    subprocess.call(
        "adb -s {} shell input keyevent 47".format(config[device_name][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    subprocess.call(
        "adb -s {} shell input keyevent 48".format(config[device_name][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    meeting_id_text = common.wait_for_element(device, tr_calendar_dict, "meeting_id_field").text
    if meeting_id_text == "TEST":
        raise AssertionError(f"{device}: meeting field is taking the alphabets in meeting id to enter the meeting")


def verify_meeting_field_should_not_accept_alphanumeric(device):
    if "console" in device:
        device_name = "consoles"
    else:
        device_name = "devices"
    verify_join_with_an_meeting_id_options(device)
    subprocess.call(
        "adb -s {} shell input keyevent 48".format(config[device_name][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    subprocess.call(
        "adb -s {} shell input keyevent 33".format(config[device_name][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    subprocess.call(
        "adb -s {} shell input keyevent 47".format(config[device_name][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    subprocess.call(
        "adb -s {} shell input keyevent 48".format(config[device_name][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    subprocess.call(
        "adb -s {} shell input keyevent 8".format(config[device_name][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    subprocess.call(
        "adb -s {} shell input keyevent 9".format(config[device_name][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    meeting_id_text = common.wait_for_element(device, tr_calendar_dict, "meeting_id_field").text
    if meeting_id_text == "TEST12":
        raise AssertionError(
            f"{device}: meeting field is taking the alphanumeric value in meeting id to enter the meeting"
        )


def verify_user_cannot_join_a_meeting_without_passcode(device):
    click_on_join_by_id(device)
    common.wait_for_element(device, tr_calendar_dict, "join_with_a_meeting_ID")
    meeting_id_field = common.wait_for_element(device, tr_calendar_dict, "meeting_id_field")
    meeting_id_field.send_keys(config["meeting_details"]["meeting_id"])
    common.wait_for_and_click(device, tr_calendar_dict, "join_meeting")
    time.sleep(refresh_time)
    common.wait_for_element(device, tr_calendar_dict, "invalid_credentials_popup")


def verify_meeting_info_option_in_meeting(device):
    open_call_more_options(device)
    common.wait_for_element(device, tr_calendar_dict, "Meeting_info")
    dismiss_call_more_options(device)


def open_call_more_options(device_name):
    # Assert call_more_options is available:
    common.wait_for_element(device_name, calls_dict, "Hang_up_button")
    # open call_more_options:
    common.wait_for_and_click(device_name, calls_dict, "call_more_options")
    common.wait_while_present(device_name, calls_dict, "call_more_options")

    # Verify that it opened:
    if not is_call_more_options_open(device_name):
        raise AssertionError(f"{device_name}: 'call more options' click was ignored, options did not open")
    print(f"{device_name}: call_more_options is now open")


def is_call_more_options_open(device_name):
    # There is no unique container for 'call_more_options', using this button presence instead:
    return common.is_element_present(device_name, tr_calendar_dict, "Meeting_info")


def dismiss_call_more_options(device_name):
    # Assert call_more_options is open:
    if not is_call_more_options_open(device_name):
        raise AssertionError(f"{device_name}: Cannot dismiss 'call more options' - it is not open")

    # Attempt to dismiss:
    # There is no 'close' button or 'touch_outside' area defined. Using
    #   the bottom bar container as a 'touch_outside' area:
    if not common.click_if_present(device_name, calls_dict, "in_call_buttons_container"):
        # Can this be removed? (Yes for 'spokane')
        print(f"{device_name}: Warning - tapping on random location in hopes it closes the 'call more options' menu")
        if "console" in device_name:
            tr_console_settings_keywords.tap_on_device_right_corner(device_name)
        else:
            call_keywords.device_right_corner_click(device_name)

    # verify dismissed:
    common.wait_while_present(device_name, tr_calendar_dict, "Meeting_info")
    print(f"{device_name}: call_more_options is now dismissed")


def verify_meeting_info_in_meeting(device):
    open_call_more_options(device)
    common.wait_for_and_click(device, tr_calendar_dict, "Meeting_info")
    common.wait_for_element(device, tr_calendar_dict, "Meeting_info_field")
    common.wait_for_element(device, tr_calendar_dict, "info_meeting_id")
    common.wait_for_element(device, tr_calendar_dict, "info_passcode_field")
    common.wait_for_and_click(device, calls_dict, "close_btn")


def meeting_details_containes_space_for_every_3_characters(device):
    click_on_join_by_id(device)
    common.wait_for_element(device, tr_calendar_dict, "join_with_a_meeting_ID")
    meeting_id_field = common.wait_for_element(device, tr_calendar_dict, "meeting_id_field")
    meeting_id_field.send_keys(config["meeting_details"]["meeting_id"])
    time.sleep(action_time)
    meeting_id_field_text = common.wait_for_element(device, tr_calendar_dict, "meeting_id_field").text.strip()
    print(meeting_id_field_text, f"{device} meeting_id_field_text text is")
    count = 0
    for i in meeting_id_field_text:
        if i.isspace():
            count = count + 1
    print("The number of blank spaces is: ", count)
    if count != 3:
        raise AssertionError(f"{device} join id not has space for every 3 characters ")
    meeting_id_field_text = meeting_id_field_text.replace(" ", "")
    if not meeting_id_field_text.isnumeric():
        raise AssertionError(f"{device} meeting id field is not containing numeric values")


def click_on_join_by_id(device):
    time.sleep(3)
    if not common.click_if_present(device, tr_calendar_dict, "join_with_an_id"):
        common.wait_for_and_click(device, tr_console_home_screen_dict, "more_option")
        common.wait_for_and_click(device, tr_calendar_dict, "join_with_an_id")
    common.wait_for_element(device, tr_calendar_dict, "join_with_a_meeting_ID")


def change_meeting_mode(device, mode):
    if mode.lower() not in ["gallery", "front_row", "large_gallery", "together"]:
        raise AssertionError(f"value for 'mode' is not defined properly: {mode}")
    common.wait_for_and_click(device, tr_calls_dict, "call_control_shared_mode_btn")
    if mode.lower() == "gallery":
        common.wait_for_and_click(device, tr_calendar_dict, "gallery_mode")
    elif mode.lower() == "front_row":
        common.wait_for_and_click(device, tr_calendar_dict, "front_row_mode")
    elif mode.lower() == "large_gallery":
        common.wait_for_and_click(device, tr_calendar_dict, "large_gallery_mode")
    elif mode.lower() == "together":
        common.wait_for_and_click(device, tr_calendar_dict, "together_mode")
    call_keywords.dismiss_the_popup_screen(device)


def verify_front_row_mode(device, chat_toggle="on"):
    if chat_toggle.lower() not in ["on", "off"]:
        raise AssertionError(f"value for 'chat_toggle' is not defined properly: {chat_toggle}")
    if chat_toggle.lower() == "off":
        if common.is_element_present(device, tr_calendar_dict, "chat"):
            raise AssertionError(
                f" {device} After disabling the show meeting chat option in settings still chat panel is visible in the meeting"
            )
    else:
        common.wait_for_element(device, tr_calendar_dict, "chat")
    time.sleep(3)
    if not common.is_element_present(device, tr_calendar_dict, "front_row_participant_view"):
        common.wait_for_element(device, tr_calendar_dict, "Waiting_others_join")


def verify_front_row_participant(from_device, connected_device_list):
    connected_devices = connected_device_list.split(",")
    print("connected_devices length : ", len(connected_devices))
    device_list = []
    for devices in connected_devices:
        account = "user"
        if ":" in devices:
            user = devices.split(":")[1]
            if user.lower() == "meeting_user":
                account = "meeting_user"
            devices = devices.split(":")[0]
        print("account : ", account)
        device_list.append(str(config["devices"][devices][account]["displayname"]))
    print("device_list : ", device_list)
    common.wait_for_element(from_device, tr_calendar_dict, "front_row_participant_view")
    get_front_row_participant_list = common.get_all_elements_texts(
        from_device, tr_calendar_dict, "front_row_participant_view", "id"
    )
    print("get_connected_front_row_list length : ", get_front_row_participant_list)
    if device_list.sort() != get_front_row_participant_list.sort():
        raise AssertionError("Participant list is not matching")


def verify_chat_switch_orientation_toggle_is_not_present(device):
    if common.is_element_present(device, tr_calendar_dict, "chat_toggle_btn"):
        raise AssertionError(f"{device} chat_toggle_btn is present in front row ")


def verify_top_bar_in_front_row(device):
    common.wait_for_element(device, tr_calendar_dict, "chat")
    common.wait_for_element(device, tr_calendar_dict, "front_row_timer")


def enable_front_row_toggle_from_device_setting(device, default_state_layout):
    if default_state_layout.lower() not in ["content_gallery", "content_only", "front_row"]:
        raise AssertionError(f"value for Default state layout is not defined properly: '{default_state_layout}'")
    for i in range(7):
        if common.is_element_present(device, tr_calendar_dict, "Default_stage_layout"):
            break
        swipe_the_middle_page_to_end(device)
    common.wait_for_and_click(device, tr_calendar_dict, "Default_stage_layout")
    if default_state_layout.lower() == "content_only":
        common.sleep_with_msg(device, 3, "waiting for getting the content option")
        if not common.click_if_present(device, tr_calendar_dict, "focus_on_content"):
            common.wait_for_and_click(device, tr_calendar_dict, "Content_only")
    elif default_state_layout.lower() == "content_gallery":
        common.sleep_with_msg(device, 3, "waiting for getting the content gallery option")
        if not common.click_if_present(device, tr_calendar_dict, "content_people"):
            common.wait_for_and_click(device, tr_calendar_dict, "Content_Gallery")
    elif default_state_layout.lower() == "front_row":
        common.wait_for_and_click(device, tr_calendar_dict, "front_row_mode")


def verify_meet_info(device):
    common.wait_for_and_click(device, tr_home_screen_dict, "meeting_button", "id")
    common.wait_for_element(device, tr_calls_dict, "Add_participants_btn")
    common.wait_for_element(device, tr_calendar_dict, "meeting_id_text")
    common.wait_for_element(device, tr_calendar_dict, "enter_passcode_text")
    common.wait_for_and_click(device, tr_calendar_dict, "dail_info")
    if not common.click_if_present(device, tr_calls_dict, "close_roaster_button"):
        common.wait_for_and_click(device, tr_calendar_dict, "dismiss")
    common.wait_for_element(device, calls_dict, "Hang_up_button")


def verify_meet_dail_info_is_not_present_in_meeting(device):
    if common.is_element_present(device, tr_calendar_dict, "dail_info"):
        raise AssertionError(f"{device} meet dail info option is present in meeting")


def verify_whiteboard_sharing_option_on_home_screen_option(device):
    common.wait_for_element(device, tr_settings_dict, "more_button")
    common.wait_for_and_click(device, tr_calendar_dict, "Microsoft_whiteboard_sharing")
    if not common.is_element_present(device, tr_calls_dict, "canvas_lasso_select"):
        common.wait_for_element(device, tr_calls_dict, "canvas_view")


def start_meeting_from_whiteboard_sharing(device):
    if not common.is_element_present(device, tr_calls_dict, "canvas_lasso_select"):
        common.wait_for_element(device, tr_calls_dict, "canvas_view")
    common.wait_for_and_click(device, tr_calendar_dict, "white_board_start_meeting")
    time.sleep(5)
    if not common.is_element_present(device, tr_calls_dict, "canvas_lasso_select"):
        common.wait_for_element(device, tr_calls_dict, "canvas_view")


def verify_that_chat_toggle_button_should_be_disabled_by_default(device):
    time.sleep(5)
    if not common.is_element_present(device, tr_calendar_dict, "chat_toggle_btn"):
        common.wait_for_and_click(device, tr_calls_dict, "call_control_shared_mode_btn")
    common.wait_for_element(device, tr_calendar_dict, "customize_your_view_text")
    toggle_btn = common.wait_for_element(device, tr_calendar_dict, "chat_toggle_btn")
    toggle_btn_status = toggle_btn.get_attribute("checked")
    if toggle_btn_status.lower() != "false":
        raise AssertionError(f"{device} toggle button state is: {toggle_btn_status.lower()}")
    call_keywords.dismiss_the_popup_screen(device)


def enable_and_disable_the_chat_toggle_in_meeting(device, state):
    common.wait_for_and_click(device, tr_calls_dict, "call_control_shared_mode_btn")
    common.change_toggle_button(device, tr_calendar_dict, "chat_toggle_btn", state)
    call_keywords.dismiss_the_popup_screen(device)


def verify_the_chat_options_in_meeting(device):
    common.wait_for_element(device, tr_calendar_dict, "chat_header")
    if not common.is_element_present(device, tr_calendar_dict, "front_row_timer"):
        common.wait_for_element(device, tr_calendar_dict, "meeting_chat_timer")


def enable_and_disable_the_chat_toggle_in_admin_setting(device, state):
    common.wait_for_element(device, tr_calendar_dict, "show_meeting_names_text")
    for i in range(7):
        if common.is_element_present(device, tr_calendar_dict, "chat_toggle_in_device_setting"):
            break
        tr_settings_keywords.swipe_screen_page(device)
    common.change_toggle_button(device, tr_calendar_dict, "chat_toggle_in_device_setting", state)


def verify_chat_toggle_in_admin_setting(device):
    common.wait_for_element(device, tr_calendar_dict, "chat_toggle_in_device_setting")


def verify_that_chat_toggle_button_is_not_present(device):
    common.wait_for_and_click(device, tr_calls_dict, "call_control_shared_mode_btn")
    if common.is_element_present(device, tr_calendar_dict, "chat_toggle_btn"):
        raise AssertionError(f"{device} chat toggle button is present ")
    call_keywords.dismiss_the_popup_screen(device)


def join_meeting_with_meeting_id_and_passscode_from_meet_now(from_device, to_device):
    common.wait_for_element(from_device, tr_settings_dict, "more_button")
    common.wait_for_and_click(to_device, tr_home_screen_dict, "meeting_button")
    time.sleep(15)
    meeting_id = common.wait_for_element(to_device, tr_calendar_dict, "meeting_id_text").text
    print(f"{to_device} meeting id number : {meeting_id}")
    Passcode = common.wait_for_element(to_device, tr_calendar_dict, "enter_passcode_text").text
    print(f"{to_device} meeting id passcode is : {Passcode}")
    common.wait_for_element(from_device, tr_settings_dict, "more_button")
    common.wait_for_and_click(from_device, tr_calendar_dict, "join_with_an_id")
    common.wait_for_element(from_device, tr_calendar_dict, "join_with_a_meeting_ID")
    common.wait_for_element(from_device, tr_calendar_dict, "meeting_id_field").send_keys(meeting_id)
    common.wait_for_element(from_device, tr_calendar_dict, "passcode_field").send_keys(Passcode)
    common.wait_for_and_click(from_device, tr_calendar_dict, "join_meeting")


def verify_user_cannot_join_locked_meeting_notification(device):
    common.wait_for_element(device, tr_calendar_dict, "meeting_locked_msg")


def swipe_the_middle_page_to_end(device):
    driver = obj.device_store.get(alias=device)
    window_size = driver.get_window_size()
    print("Window size: ", window_size)
    height = window_size["height"]
    print("Window Height :", height)
    width = window_size["width"]
    print("Window Width :", width)
    print("Swiping co-ordinates : ", width / 3, 2 * (height / 4), width / 3, height / 4)
    driver.swipe(width / 3, 2 * (height / 4), width / 3, height / 4)


def verify_extend_room_reservation_option_inside_meeting_settings(device):
    common.wait_for_element(device, tr_calendar_dict, "show_meeting_names_text")
    for i in range(5):
        if common.is_element_present(device, tr_calendar_dict, "extend_room_reservation_tgl"):
            break
        tr_settings_keywords.swipe_screen_page(device)
    common.wait_for_element(device, tr_calendar_dict, "extend_room_reservation")
    common.wait_for_and_click(device, calendar_dict, "back")
    if "console" in device:
        tr_console_settings_keywords.device_setting_back_btn(device)


def verify_extend_reservation_options(device):
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_and_click(device, calls_dict, "call_more_options")
    common.wait_for_and_click(device, tr_calendar_dict, "extend_reservation")
    common.wait_for_element(device, tr_calendar_dict, "new_end_time_for_meeting")
    common.wait_for_element(device, tr_calendar_dict, "extend_reservation_15_minutes")
    common.wait_for_element(device, tr_calendar_dict, "extend_reservation_30_minutes")
    common.wait_for_element(device, tr_calendar_dict, "extend_reservation_45_minutes")
    common.wait_for_element(device, tr_calendar_dict, "extend_reservation_60_minutes")
    common.wait_for_element(device, tr_calendar_dict, "confirm_button")
    common.wait_for_and_click(device, tr_calendar_dict, "Dismiss")


def verify_error_banner_for_extend_meeting_while_using_meetnow(device):
    common.wait_for_and_click(device, calls_dict, "call_more_options")
    common.wait_for_and_click(device, tr_calendar_dict, "extend_reservation")
    common.wait_for_element(device, tr_calendar_dict, "unable_extend_reservation")
    common.wait_for_element(device, tr_calendar_dict, "unable_extend_reservation_message")
    common.wait_for_and_click(device, calls_dict, "ok")


def verify_changed_mode(device, changed_mode):
    if not changed_mode.lower() in ["together_mode", "large_gallery"]:
        raise AssertionError(f"value for 'changed_mode' is not defined properly: '{changed_mode}'")
    if changed_mode.lower() == "together_mode":
        common.wait_for_element(device, tr_calendar_dict, "together_mode_title")
    elif changed_mode.lower() == "large_gallery":
        common.wait_for_element(device, tr_calendar_dict, "large_gallery_title")


def verify_layout_options(device):
    common.wait_for_and_click(device, tr_calls_dict, "call_control_shared_mode_btn")
    common.wait_for_element(device, tr_calendar_dict, "gallery_mode")
    common.wait_for_element(device, tr_calendar_dict, "front_row_mode")
    common.wait_for_element(device, tr_calendar_dict, "large_gallery_mode")
    common.wait_for_element(device, tr_calendar_dict, "together_mode")
    call_keywords.dismiss_the_popup_screen(device)


def verify_layout_options_after_disable_video_call(device):
    common.wait_for_and_click(device, tr_calls_dict, "call_control_shared_mode_btn")
    common.wait_for_element(device, tr_calendar_dict, "gallery_mode")
    common.wait_for_element(device, tr_calendar_dict, "front_row_mode")
    if common.is_element_present(device, tr_calendar_dict, "large_gallery_mode"):
        raise AssertionError(f"{device} large_gallery_mode is present ")
    call_keywords.dismiss_the_popup_screen(device)


def verify_highlighted_raised_hand_in_meeting(device):
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_and_click(device, tr_calendar_dict, "call_control_reactions_button")
    common.wait_for_element(device, tr_calendar_dict, "hightlighted_raised_hand")
    call_keywords.dismiss_the_popup_screen(device)


def verify_spotlight_icon_on_top_left_in_the_meeting(device):
    common.wait_for_element(device, tr_calendar_dict, "spotlight_border")
    common.wait_for_element(device, calendar_dict, "spotlight_avatar")


def verify_spotlight_icon_on_main_screen_in_the_meeting(device):
    common.wait_for_element(device, calendar_dict, "spotlight_avatar")


def verify_front_row_mode_after_disabeling_the_chat_option(device):
    common.wait_for_and_click(device, tr_calls_dict, "call_control_shared_mode_btn")
    common.wait_for_element(device, tr_calendar_dict, "gallery_mode")
    if common.is_element_present(device, tr_calendar_dict, "chat_toggle_btn"):
        raise AssertionError(f"{device} chat toggle button is present ")
    if common.is_element_present(device, tr_calendar_dict, "chat"):
        raise AssertionError(
            f"{device} Still chat is present on the device after disabeling the chat option from settings"
        )
    call_keywords.dismiss_the_popup_screen(device)


def verify_layouts_option_should_not_present_on_call_control_bar(device):
    time.sleep(3)
    if common.is_element_present(device, tr_calls_dict, "call_control_shared_mode_btn"):
        raise AssertionError(f"{device} Layout options button is present on the call control bar")


def enable_and_disable_the_max_room_occupancy_notification_toggle_button(device, state):
    common.wait_for_element(device, tr_calendar_dict, "show_meeting_names_text")
    for i in range(7):
        if common.is_element_present(device, tr_calendar_dict, "max_room_occupancy_notification_toggle"):
            break
        tr_settings_keywords.swipe_screen_page(device)
    common.change_toggle_button(device, tr_calendar_dict, "max_room_occupancy_notification_toggle", state)


def enable_and_disable_hdmi_content_sharing(device, state):
    common.wait_for_element(device, tr_calendar_dict, "show_meeting_names_text")
    for i in range(5):
        if common.is_element_present(device, tr_calendar_dict, "hdmi_content_sharing_option"):
            break
        tr_settings_keywords.swipe_screen_page(device)
    common.change_toggle_button(device, tr_calendar_dict, "hdmi_content_sharing", state)


def verify_share_content_hdmi_is_not_present(device):
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_and_click(device, tr_calendar_dict, "share_button")
    if common.is_element_present(device, tr_calendar_dict, "share_content_hdmi_in_meeting"):
        raise AssertionError(f"{device} share content hdmi is present ")
    call_keywords.dismiss_the_popup_screen(device)


def verify_show_chat_bubble_is_enabled_default(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    common.wait_for_and_click(device, calls_dict, "call_more_options")
    if not common.is_element_present(device, tr_console_calendar_dict, "dont_show_chat_bubble"):
        raise AssertionError(f"{device} show chat bubble is disabled default")
    call_keywords.dismiss_the_popup_screen(device)


def verify_layout_option_is_not_present(device):
    if common.is_element_present(device, tr_calls_dict, "call_control_shared_mode_btn"):
        raise AssertionError(f"{device} layout option is present in call control bar")


def verify_whiteboard_should_not_visible_on_all_participants(device_list):
    devices = device_list.split(",")
    for device in devices:
        common.wait_while_present(device, calls_dict, "call_more_options")


def join_rooms_meeting_after_hiding_the_title_name(device, organizer_name):
    calendar_keywords.join_meeting(device, meeting=organizer_name)
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    actual_meeting = common.wait_for_element(device, tr_calendar_dict, "meeting_action_bar_title_text").text
    expected_meeting = [
        "all_day_meeting",
        "all_day_meeting_1",
        "all_day_meeting_2",
        "cnf_device_meeting",
        "lock_meeting",
    ]
    if actual_meeting not in expected_meeting:
        raise AssertionError(f"{device} is not joined in the expected meeting {actual_meeting}")


def verify_start_meeting_and_stop_whiteboard_options_when_the_dut_user_launch_whiteboard(device):
    common.wait_for_element(device, tr_calendar_dict, "white_board_start_meeting")
    common.wait_for_and_click(device, tr_calendar_dict, "stop_whiteboard_sharing")
    common.wait_for_element(device, app_bar_dict, "cancel_btn")
    common.wait_for_and_click(device, tr_calendar_dict, "stop_whiteboard_sharing")


def enable_and_disable_white_board_sharing_toggle(device, state):
    common.wait_for_and_click(device, tr_settings_dict, "meetings_button")
    common.wait_for_element(device, tr_calendar_dict, "show_meeting_names_text")
    for i in range(7):
        if common.is_element_present(device, tr_calendar_dict, "whiteboard_sharing_toggle"):
            break
        tr_settings_keywords.swipe_screen_page(device)
    common.change_toggle_button(device, tr_calendar_dict, "whiteboard_sharing_toggle", state)


def verify_whiteboard_sharing_option_is_not_present_in_home_screen(device):
    common.wait_for_element(device, tr_settings_dict, "more_button")
    if common.is_element_present(device, tr_calendar_dict, "Microsoft_whiteboard_sharing"):
        raise AssertionError(f"{device} whiteboard sharing option is present in home screen")


def verify_Start_meeting_and_verify_Whiteboard_launch(device):
    common.wait_for_element(device, tr_settings_dict, "more_button")
    common.wait_for_and_click(device, tr_calendar_dict, "Microsoft_whiteboard_sharing")
    common.wait_for_and_click(device, tr_calendar_dict, "start_meeting")
    if not common.is_element_present(device, tr_calls_dict, "canvas_lasso_select"):
        common.wait_for_element(device, tr_calls_dict, "canvas_view")


def enable_and_disable_require_passcode_for_all_meetings_toggle(device, state):
    max_attempt = 5
    for i in range(max_attempt):
        if common.is_element_present(device, tr_calendar_dict, "require_passcode_all_meetings_txt"):
            break
        tr_settings_keywords.swipe_screen_page(device)
        if i == max_attempt - 1:
            raise AssertionError(f"{device} couldn't find require passcode all meetings option{i + 1} attempts")
    common.wait_for_element(device, tr_calendar_dict, "require_passcode_for_all_meetings_toggle")
    return common.change_toggle_button(device, tr_calendar_dict, "require_passcode_for_all_meetings_toggle", state)


def verify_that_Require_passcode_for_all_meetings_toggle_should_be_disabled_by_default(device):
    common.wait_for_and_click(device, tr_settings_dict, "meetings_button")
    common.wait_for_element(device, tr_calendar_dict, "show_meeting_names_text")
    for i in range(7):
        if common.is_element_present(device, tr_calendar_dict, "require_passcode_for_all_meetings_toggle"):
            break
        tr_settings_keywords.swipe_screen_page(device)
    toggle_btn = common.wait_for_element(device, tr_calendar_dict, "require_passcode_for_all_meetings_toggle")
    toggle_btn_status = toggle_btn.get_attribute("checked")
    if toggle_btn_status.lower() != "false":
        raise AssertionError(f"{device} toggle button state is: {toggle_btn_status.lower()}")


def join_meeting_with_Require_passcode(device, meeting):
    devices = device.split(",")
    for device in devices:
        calendar_keywords.join_meeting(device, meeting)
        if ":" in device:
            device = device.split(":")[0]
            print("device :", device)
    join_meeting = common.wait_for_element(device, tr_calendar_dict, "join_with_a_meeting_ID").text
    print("join in:", {join_meeting})
    meeting_passcode = common.wait_for_element(device, tr_calendar_dict, "passcode_field")
    meeting_passcode.send_keys(config["meeting_details"]["meeting_passcode"])
    common.wait_for_and_click(device, tr_calendar_dict, "join_meeting")


def join_meeting_with_an_invalid_password_under_require_passcode_meeting(device, meeting):
    devices = device.split(",")
    for device in devices:
        if "console" not in device:
            calendar_keywords.join_meeting(device, meeting)
    if ":" in device:
        device = device.split(":")[0]
        print("device :", device)
    common.wait_for_element(device, tr_calendar_dict, "join_with_a_meeting_ID")
    meeting_id = common.wait_for_element(device, tr_calendar_dict, "meeting_id_field")
    meeting_id.clear()
    meeting_id.send_keys(config["meeting_details"]["invalid_meeting_id"])
    meeting_passcode = common.wait_for_element(device, tr_calendar_dict, "passcode_field")
    meeting_passcode.send_keys(config["meeting_details"]["invalid_passcode"])
    common.wait_for_and_click(device, tr_calendar_dict, "join_meeting")
    common.sleep_with_msg(device, 5, "waiting for the until call complete")
    common.wait_for_element(device, tr_calendar_dict, "invalid_credentials_popup")


def verify_options_available_under_meeting_ID_field_in_a_meeting_when_user_enables_Require_passcode_for_all_meetings_toggle(
    device, meeting
):
    devices = device.split(",")
    for device in devices:
        if "console" not in device:
            calendar_keywords.join_meeting(device, meeting)
    if ":" in device:
        device = device.split(":")[0]
        print("device :", device)
    common.sleep_with_msg(device, 5, "waiting for the until the meeting field reflected")
    common.wait_for_element(device, tr_calendar_dict, "join_with_a_meeting_ID")
    common.wait_for_element(device, tr_calendar_dict, "meeting_id_field")
    common.wait_for_element(device, tr_calendar_dict, "passcode_field")
    common.wait_for_element(device, tr_calendar_dict, "join_meeting")


def verify_user_should_not_accept_alphabet_for_meeting_id_in_meeting_field_when_user_enables_require_passcode_for_all_meetings(
    device, meeting
):
    devices = device.split(",")
    for device in devices:
        if "console" not in device:
            calendar_keywords.join_meeting(device, meeting)
    if ":" in device:
        device = device.split(":")[0]
        print("device :", device)
    if "console" in device:
        device_name = "consoles"
    else:
        device_name = "devices"
    common.wait_for_element(device, tr_calendar_dict, "meeting_id_field").clear()
    subprocess.call(
        "adb -s {} shell input keyevent 48".format(config[device_name][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    subprocess.call(
        "adb -s {} shell input keyevent 33".format(config[device_name][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    subprocess.call(
        "adb -s {} shell input keyevent 47".format(config[device_name][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    subprocess.call(
        "adb -s {} shell input keyevent 48".format(config[device_name][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    meeting_id_text = common.wait_for_element(device, tr_calendar_dict, "meeting_id_field").text
    if meeting_id_text == "TEST":
        raise AssertionError(f"{device}: meeting field is taking the alphabets in meeting id to enter the meeting")


def verify_user_cannot_join_a_meeting_without_passcode_once_user_enables_require_passcode_for_all_meetings(
    device, meeting
):
    devices = device.split(",")
    for device in devices:
        if "console" not in device:
            calendar_keywords.join_meeting(device, meeting)
    if ":" in device:
        device = device.split(":")[0]
        print("device :", device)
    elem = common.wait_for_element(device, tr_calendar_dict, "join_meeting")
    temp = elem.get_attribute("enabled")
    if temp != "false":
        raise AssertionError(f"{device}:join meeting button is in enabled state")


def verify_meeting_id_should_be_formatted_with_a_white_space_every_three_characters_when_user_enables_require_passcode_for_all_meetings(
    device, meeting
):
    devices = device.split(",")
    for device in devices:
        calendar_keywords.join_meeting(device, meeting)
        if ":" in device:
            device = device.split(":")[0]
            print("device :", device)
    common.sleep_with_msg(device, 5, "waiting for the until the meeting field reflected")
    common.wait_for_element(device, tr_calendar_dict, "meeting_id_field").clear()
    common.sleep_with_msg(device, 5, "waiting for the until the meeting field reflected")
    meeting_id_field = common.wait_for_element(device, tr_calendar_dict, "meeting_id_field")
    meeting_id_field.send_keys(config["meeting_details"]["meeting_id"])
    time.sleep(action_time)
    meeting_id_field_text = common.wait_for_element(device, tr_calendar_dict, "meeting_id_field").text.strip()
    print(meeting_id_field_text, f"{device} meeting_id_field_text text is")
    count = 0
    for i in meeting_id_field_text:
        if i.isspace():
            count = count + 1
    print("The number of blank spaces is: ", count)
    if count != 3:
        raise AssertionError(f"{device} join id not has space for every 3 characters ")
    meeting_id_field_text = meeting_id_field_text.replace(" ", "")
    if not meeting_id_field_text.isnumeric():
        raise AssertionError(f"{device} meeting id field is not containing numeric values")


def verify_invalid_number_and_edit_the_meeting_id_and_passcode_for_require_passcode_meeting(device, meeting):
    devices = device.split(",")
    for device in devices:
        device, user_type = common.decode_device_spec(device)
        print(f"device: {device}, user: {user_type}")
        calendar_keywords.join_meeting(device, meeting)
    print(f"WARNING: Bug: passcode will be entered only for last device from loop")
    meeting_passcode = common.wait_for_element(device, tr_calendar_dict, "passcode_field")
    meeting_passcode.send_keys(config["meeting_details"]["invalid_passcode"])
    common.wait_for_and_click(device, tr_calendar_dict, "join_meeting")
    common.wait_for_element(device, tr_calendar_dict, "invalid_credentials_popup")
    elem = common.wait_for_element(device, tr_calendar_dict, "Retry")
    temp = elem.get_attribute("enabled")
    if temp != "false":
        raise AssertionError(f"{device}:Retry button is in enabled state")
    meeting_id = config["meeting_details"]["meeting_id"]
    editing_meeting_id = meeting_id[:6]
    common.wait_for_element(device, tr_calendar_dict, "meeting_id_field").send_keys(editing_meeting_id)
    passcode = config["meeting_details"]["meeting_passcode"]
    editing_passcode = passcode[:6]
    common.wait_for_element(device, tr_calendar_dict, "passcode_field").send_keys(editing_passcode)
    time.sleep(action_time)
    elem = common.wait_for_element(device, tr_calendar_dict, "Retry")
    temp = elem.get_attribute("enabled")
    if temp != "false":
        raise AssertionError(f"{device}:Retry button is in disabled state")


def verify_meeting_field_should_not_accept_alphanumeric_for_require_passcode_meeting(device, meeting):
    devices = device.split(",")
    for device in devices:
        if "console" not in device:
            calendar_keywords.join_meeting(device, meeting)
    if ":" in device:
        device = device.split(":")[0]
        print("device :", device)
    if "console" in device:
        device_name = "consoles"
    else:
        device_name = "devices"
    common.wait_for_element(device, tr_calendar_dict, "meeting_id_field").clear()
    subprocess.call(
        "adb -s {} shell input keyevent 48".format(config[device_name][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    subprocess.call(
        "adb -s {} shell input keyevent 33".format(config[device_name][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    subprocess.call(
        "adb -s {} shell input keyevent 47".format(config[device_name][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    subprocess.call(
        "adb -s {} shell input keyevent 48".format(config[device_name][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    subprocess.call(
        "adb -s {} shell input keyevent 8".format(config[device_name][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    subprocess.call(
        "adb -s {} shell input keyevent 9".format(config[device_name][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    meeting_id_text = common.wait_for_element(device, tr_calendar_dict, "meeting_id_field").text
    if meeting_id_text == "TEST12":
        raise AssertionError(
            f"{device}: meeting field is taking the alphanumeric value in meeting id to enter the meeting"
        )


def verify_the_gallery_layout_selected_default_and_with_chat(device):
    common.wait_for_and_click(device, tr_calls_dict, "call_control_shared_mode_btn")
    common.wait_for_element(device, tr_calendar_dict, "gallery_mode")
    common.wait_for_and_click(device, tr_calendar_dict, "chat_toggle_btn")
    call_keywords.dismiss_the_popup_screen(device)
    common.wait_for_element(device, tr_calendar_dict, "chat")
    common.wait_for_element(device, tr_calendar_dict, "chat_panel")
    common.wait_for_element(device, tr_calendar_dict, "chat_view_container")


def verify_chat_on_the_front_row_ui(device):
    change_meeting_mode(device, mode="front_row")
    verify_front_row_mode(device)
    common.wait_for_element(device, tr_calendar_dict, "chat")
    common.wait_for_element(device, tr_calendar_dict, "chat_panel")
    common.wait_for_element(device, tr_calendar_dict, "chat_view_container")
    common.wait_for_and_click(device, tr_calls_dict, "call_control_shared_mode_btn")
    common.wait_for_element(device, tr_calendar_dict, "Hide")
    if common.is_element_present(device, tr_calendar_dict, "chat_toggle_btn"):
        raise AssertionError(f"{device} chat toggle is present in front row mode")
    call_keywords.dismiss_the_popup_screen(device)


def verify_require_passcode_for_all_meetings_option_under_the_meetings(device):
    common.wait_for_and_click(device, tr_settings_dict, "meetings_button")
    common.wait_for_element(device, tr_calendar_dict, "show_meeting_names_text")
    max_attempt = 5
    for i in range(max_attempt):
        if common.is_element_present(device, tr_calendar_dict, "require_passcode_all_meetings_txt"):
            break
        tr_settings_keywords.swipe_screen_page(device)
        if i == max_attempt - 1:
            raise AssertionError(f"{device} couldn't find require passcode all meetings option{i + 1} attempts")
    common.wait_for_element(device, tr_calendar_dict, "require_passcode_for_all_meetings_toggle")


def verify_layout_switcher_ui(device):
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_and_click(device, tr_calls_dict, "call_control_shared_mode_btn")
    common.wait_for_element(device, tr_calendar_dict, "gallery_mode")
    common.wait_for_element(device, tr_calendar_dict, "front_row_mode")
    common.wait_for_element(device, tr_calendar_dict, "show_chat_option")


def verify_that_gallery_mode_should_be_selected_by_default(device):
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_and_click(device, tr_calls_dict, "call_control_shared_mode_btn")
    common.wait_for_element(device, tr_calendar_dict, "default_gallery_check")


def verify_large_gallery_mode_after_switching(device):
    common.wait_for_and_click(device, tr_calls_dict, "call_control_shared_mode_btn")
    common.wait_for_element(device, tr_calendar_dict, "default_large_gallery_check")
    call_keywords.dismiss_the_popup_screen(device)


def verify_together_mode_after_switching(device):
    common.wait_for_and_click(device, tr_calls_dict, "call_control_shared_mode_btn")
    common.wait_for_element(device, tr_calendar_dict, "default_together_check")
    call_keywords.dismiss_the_popup_screen(device)


def verify_require_passcode_for_all_meetings_with_less_than_and_greater_than_7_digit_number(device, meeting):
    devices = device.split(",")
    for device in devices:
        if "console" not in device:
            calendar_keywords.join_meeting(device, meeting)
    if ":" in device:
        device = device.split(":")[0]
        print("device :", device)
    common.wait_for_element(device, tr_calendar_dict, "meeting_id_field").clear()
    common.wait_for_element(device, tr_calendar_dict, "join_with_a_meeting_ID")
    meeting_id_field = common.wait_for_element(device, tr_calendar_dict, "meeting_id_field")
    meeting_id_field.send_keys(config["meeting_details"]["meeting_id"])
    meeting_passcode = common.wait_for_element(device, tr_calendar_dict, "passcode_field")
    meeting_passcode.send_keys(config["meeting_details"]["meeting_passcode"])
    elem = common.wait_for_element(device, tr_calendar_dict, "join_meeting")
    temp = elem.get_attribute("enabled")
    if temp == "false":
        raise AssertionError(f"{device}:join meeting button is in disable state")
    seven_digit_number = config["meeting_details"]["meeting_id"]
    common.wait_for_element(device, tr_calendar_dict, "meeting_id_field").clear()
    seven_digit_number = seven_digit_number[:7]
    print(seven_digit_number, "7digit number")
    common.wait_for_element(device, tr_calendar_dict, "meeting_id_field").send_keys(seven_digit_number)
    elem = common.wait_for_element(device, tr_calendar_dict, "join_meeting")
    temp = elem.get_attribute("enabled")
    if temp != "false":
        raise AssertionError(f"{device}:join meeting button is in enabled state")


def verify_that_when_the_user_enter_only_meeting_passcode(device, meeting):
    devices = device.split(",")
    for device in devices:
        if "console" not in device:
            calendar_keywords.join_meeting(device, meeting)
    if ":" in device:
        device = device.split(":")[0]
        print("device :", device)
    common.wait_for_element(device, tr_calendar_dict, "meeting_id_field").clear()
    join_meeting = common.wait_for_element(device, tr_calendar_dict, "join_with_a_meeting_ID").text
    print("join in:", {join_meeting})
    meeting_passcode = common.wait_for_element(device, tr_calendar_dict, "passcode_field")
    meeting_passcode.send_keys(config["meeting_details"]["meeting_passcode"])
    elem = common.wait_for_element(device, tr_calendar_dict, "join_meeting")
    temp = elem.get_attribute("enabled")
    if temp != "false":
        raise AssertionError(f"{device}:join meeting button is in 'enabled' state")


def click_dropdown_option(device, dropdown_name, option):
    common.wait_for_and_click(device, tr_calendar_dict, dropdown_name)
    if option == "raised_hands":
        common.wait_for_and_click(device, calendar_dict, "raise_hand")
    elif option == "chat":
        common.wait_for_and_click(device, tr_calendar_dict, "chat_header")
    elif option == "hide":
        common.wait_for_and_click(device, tr_calendar_dict, "Hide")


def select_the_drop_down_under_show_on_left_and_show_on_right(device, show_on_left, show_on_right):
    expected_values = ["raised_hands", "chat", "hide"]
    if show_on_left.lower() not in expected_values and show_on_right.lower() not in expected_values:
        raise AssertionError(
            f"Value for 'show_on_left' or 'show_on_right' is not defined properly. show_on_left: {show_on_left}, show_on_right: {show_on_right}"
        )
    common.wait_for_and_click(device, tr_calls_dict, "call_control_shared_mode_btn")
    click_dropdown_option(device, "show_on_left_dropdown", show_on_left)
    click_dropdown_option(device, "show_on_right_dropdown", show_on_right)
    call_keywords.dismiss_the_popup_screen(device)


def select_front_row_left_default_panel_option_in_admin_setting(device, show_on_left):
    if show_on_left.lower() not in ["raised_hands", "chat", "hide"]:
        raise AssertionError(f"Value for 'show_on_left' is not defined properly. show_on_left: {show_on_left}")
    common.wait_for_element(device, tr_calendar_dict, "show_meeting_names_text")
    for i in range(7):
        if common.is_element_present(device, tr_calendar_dict, "show_on_left_dropdown"):
            break
        tr_settings_keywords.swipe_screen_page(device)
    click_dropdown_option(device, "show_on_left_dropdown", show_on_left)


def verify_waiting_in_the_lobby_message(device):
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_element(device, tr_calendar_dict, "lobby_meeting_title")
    common.wait_for_element(device, tr_calendar_dict, "lobby_meeting_subtitle_title")


def verify_meeting_name_and_preview_video_are_displayed_in_waiting_lobby(device, meeting):
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    lobby_meeting_title = common.wait_for_element(device, tr_calendar_dict, "lobby_meeting_title").text
    if lobby_meeting_title.lower() != meeting.lower():
        raise AssertionError(
            f"{device}: meeting name displayed in lobby {lobby_meeting_title} title  is not matching with actual {meeting} title"
        )
    common.wait_for_element(device, tr_calendar_dict, "lobby_meeting_subtitle_title")
    common.wait_for_element(device, tr_calendar_dict, "lobby_video_container")


def make_admit_and_deny_in_the_meeting(from_device, to_device, lobby):
    if not lobby.lower() in ["admit_lobby", "decline_lobby"]:
        raise AssertionError(f"value for 'lobby' is not defined properly: '{lobby}'")
    print(f"from_device: {from_device}, to_device: {to_device}, lobby: {lobby}")
    common.wait_for_and_click(from_device, calls_dict, "Add_participants_button")
    to_devices = to_device.split(",")
    devices = []
    accounts = []
    for device in to_devices:
        device, account = common.decode_device_spec(device)
        devices.append(device)
        accounts.append(account)
    print(f"Contact devices list: {devices} \n Accounts: {accounts}")
    ele_text = common.wait_for_element(
        from_device, calendar_dict, "add_user", "id", cond=EC.presence_of_all_elements_located
    )
    participant_list = [str(i.text).split()[0] for i in ele_text]
    print(f"participant list :", participant_list)
    user_position = 0
    for _user in participant_list:
        if _user.lower() == account:
            user_position = participant_list.index(_user)
            print(f"expected user to click:", _user)
    ele_text[user_position].click()
    to_device = to_device.split(":")[0]
    if lobby.lower() == "admit_lobby":
        common.wait_for_and_click(from_device, calls_dict, "admit_lobby")
        time.sleep(3)
        if common.is_element_present(to_device, tr_calendar_dict, "lobby_meeting_subtitle_title"):
            raise AssertionError(
                f" After user admit to the meeting from {from_device} but still {to_device} it is in lobby state"
            )
    elif lobby.lower() == "decline_lobby":
        common.wait_for_and_click(from_device, calendar_dict, "decline_btn")
        common.wait_for_element(to_device, tr_calendar_dict, "denied_access_popup")
        common.wait_for_and_click(to_device, device_settings_dict, "ok")
        common.wait_for_element(to_device, calls_dict, "rejoin_meeting_button")
        common.wait_for_and_click(to_device, calls_dict, "rejoin_meeting_button_dismiss")


def verify_the_right_and_left_after_switching_the_dropdown_options_in_front_row(device, mode):
    if mode.lower() not in ["raised_hands", "chat", "hide"]:
        raise AssertionError(f"Value for 'show_on_left' is not defined properly. show_on_left: {mode}")
    modes = mode.split(",")
    for mode in modes:
        if mode.lower() == "raised_hands":
            common.wait_for_element(device, tr_calendar_dict, "raise_hand_container")


def enable_and_disable_third_party_meetings_zoom_toggle(device, state):
    common.wait_for_and_click(device, tr_settings_dict, "meetings_button")
    common.wait_for_element(device, tr_calendar_dict, "show_meeting_names_text")
    _max_attempts = 7
    for _attempt in range(_max_attempts):
        if common.is_element_present(device, tr_calendar_dict, "zoom_button"):
            print(f"{device}: After scrolling {_attempt} times found User survey")
            break
        tr_call_keywords.swipe_till_end_page(device)
    common.wait_for_element(device, tr_calendar_dict, "zoom_button")
    common.change_toggle_button(device, tr_calendar_dict, "zoom_toggle", state)


def enable_and_disable_third_party_meetings_webex_toggle(device, state):
    common.wait_for_and_click(device, tr_settings_dict, "meetings_button")
    common.wait_for_element(device, tr_calendar_dict, "show_meeting_names_text")
    _max_attempts = 7
    for _attempt in range(_max_attempts):
        if common.is_element_present(device, tr_calendar_dict, "webex_toggle"):
            print(f"{device}: After scrolling {_attempt} times found User survey")
            break
        time.sleep(1)
        tr_call_keywords.swipe_till_end_page(device)
    common.change_toggle_button(device, tr_calendar_dict, "webex_toggle", state)


def verify_third_party_zoom_meetings_toggle_disable_default(device):
    _max_attempts = 7
    for _attempt in range(_max_attempts):
        if common.is_element_present(device, tr_calendar_dict, "zoom_button"):
            print(f"{device}: After scrolling {_attempt} times found User survey")
            break
        tr_settings_keywords.swipe_screen_page(device)
    common.wait_for_element(device, tr_calendar_dict, "zoom_button")
    common.verify_toggle_button(device, tr_calendar_dict, "zoom_toggle", desired_state="off")


def verify_the_docked_ubar_when_third_party_meeting_joins(device, meetting_mode="zoom"):
    if meetting_mode.lower() not in ["zoom", "webex"]:
        raise AssertionError(f"{device} meeting is not defined proper manner: {meetting_mode}")
    common.wait_for_element(device, calendar_dict, "hang_up_btn")
    common.wait_for_element(device, calls_dict, "meeting_mute_control")
    common.wait_for_element(device, tr_home_screen_dict, "volume_minus")
    common.wait_for_element(device, tr_home_screen_dict, "volume_icon")
    common.wait_for_element(device, tr_home_screen_dict, "volume_plus")
    if meetting_mode == "zoom":
        common.wait_for_element(device, tr_calendar_dict, "3p_more")
        common.wait_for_element(device, tr_calendar_dict, "3p_settings")
        common.wait_for_element(device, tr_calendar_dict, "3p_Ai_companion")
        common.wait_for_element(device, tr_calendar_dict, "3p_caption")
        common.wait_for_element(device, tr_calendar_dict, "3p_record")
        common.wait_for_element(device, tr_calendar_dict, "3p_chat")
    elif meetting_mode == "webex":
        common.wait_for_element(device, calendar_dict, "mute_participant")
        common.wait_for_element(device, tr_calendar_dict, "3p_stop_video")
        common.wait_for_element(device, tr_calendar_dict, "3p_leave_meeting")
        common.wait_for_element(device, calendar_dict, "call_control_reactions_button")


def verify_third_party_meeting_both_call_controls_should_be_in_sync(device, mute_state, video_state):
    if not mute_state.lower() in ["mute", "unmute"]:
        raise AssertionError(f"Illegal state specified: '{mute_state}'")
    if not video_state.lower() in ["on", "off"]:
        raise AssertionError(f"Illegal state specified: '{video_state}'")
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    if mute_state.lower() == "mute":
        common.click_if_present(device, tr_calendar_dict, "3p_unmute")
        common.wait_for_and_click(device, calendar_dict, "call_control_mute")
        common.wait_for_element(device, tr_calendar_dict, "3p_unmute")
    elif mute_state.lower() == "unmute":
        common.click_if_present(device, tr_calendar_dict, "3p_mute")
        common.wait_for_element(device, calendar_dict, "call_control_mute")
        common.wait_for_element(device, tr_calendar_dict, "3p_mute")
    elif video_state.lower() == "on":
        common.click_if_present(device, tr_calendar_dict, "3p_video_off")
        common.wait_for_and_click(device, tr_calls_dict, "video_on")
        common.wait_for_element(device, tr_calendar_dict, "3p_video_off")
    elif video_state.lower() == "off":
        common.click_if_present(device, tr_calendar_dict, "3p_video_on")
        common.wait_for_element(device, tr_calls_dict, "video_off")
        common.wait_for_element(device, tr_calendar_dict, "3p_video_on")


def verify_zoom_icon_on_calendar_tab(device):
    common.wait_for_element(device, tr_home_screen_dict, "more_button")
    _max_attempts = 7
    for _attempt in range(_max_attempts):
        if common.is_element_present(device, tr_calendar_dict, "zoom_button"):
            print(f"{device}: After scrolling {_attempt} times found User survey")
            break
        tr_calendar_keywords.scroll_up_meeting_tab(device)
    common.wait_for_element(device, tr_calendar_dict, "zoom_button")


def verify_webex_icon_on_calendar_tab(device):
    common.wait_for_element(device, tr_home_screen_dict, "more_button")
    _max_attempts = 7
    for _attempt in range(_max_attempts):
        if common.is_element_present(device, tr_calendar_dict, "webex_icon"):
            print(f"{device}: After scrolling {_attempt} times found User survey")
            break
        tr_calendar_keywords.scroll_up_meeting_tab(device)
    common.wait_for_element(device, tr_calendar_dict, "webex_icon")


def verify_video_should_be_enabled_by_default_while_joining_the_meeting(device):
    common.wait_for_element(device, tr_calls_dict, "video_on")


def verify_back_and_setting_button_is_not_present_in_meeting(device):
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    if common.is_element_present(device, common_dict, "back"):
        raise AssertionError(f"{device} back is present in meeting")
    if common.is_element_present(device, navigation_dict, "Settings_button"):
        raise AssertionError(f"{device} Settings_button is present in meeting")
