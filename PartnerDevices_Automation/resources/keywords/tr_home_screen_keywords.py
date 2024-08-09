from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Selectors import load_json_file
from initiate_driver import obj_dev as obj
from initiate_driver import config
import subprocess
import settings_keywords
import call_keywords
import common
import re
from datetime import datetime
import time
import tr_calendar_keywords
import home_screen_keywords

tr_home_screen_dict = load_json_file("resources/Page_objects/tr_home_screen.json")
tr_settings_dict = load_json_file("resources/Page_objects/tr_settings.json")
tr_calls_dict = load_json_file("resources/Page_objects/tr_calls.json")
calls_dict = load_json_file("resources/Page_objects/Calls.json")
console_calendar_dict = load_json_file("resources/Page_objects/rooms_console_calendar.json")
tr_calendar_dict = load_json_file("resources/Page_objects/tr_calendar.json")
calendar_dict = load_json_file("resources/Page_objects/Calendar.json")
tr_console_home_screen_dict = load_json_file("resources/Page_objects/rooms_console_home_screen.json")
panels_home_screen_dict = load_json_file("resources/Page_objects/panels_homescreen.json")
tr_console_signin_dict = load_json_file("resources/Page_objects/rooms_console_signin.json")
tr_console_settings_dict = load_json_file("resources/Page_objects/rooms_console_settings.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")
common_dict = load_json_file("resources/Page_objects/common.json")


display_time = 2
action_time = 3


def adjust_volume_button(device, state, functionality=None):
    print("device :", device)
    print("state :", state)
    driver = obj.device_store.get(alias=device)
    if functionality is None:
        pass
    else:
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((MobileBy.ID, calls_dict["Hang_up_button"]["id"]))
            )
            print("Call control visible on screen")
        except Exception as e:
            settings_keywords.click_device_center_point(device)
            print("Clicked on center point")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((MobileBy.ID, tr_home_screen_dict["volume_icon"]["id"])))
    print("Volume Icon is visible")
    try:
        if state.lower() == "up":
            v1 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((MobileBy.ID, tr_home_screen_dict["volume_plus"]["id"]))
            )
            for i in range(0, 2):
                v1.click()
            print("Volume up button is pressed")
        elif state.lower() == "down":
            v2 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((MobileBy.ID, tr_home_screen_dict["volume_minus"]["id"]))
            )
            for i in range(0, 2):
                v2.click()
            print("Volume down button is pressed")
    except Exception as e:
        raise AssertionError("Volume button is not visible")


def verify_no_upcoming_meetings_display_on_home_screen(device):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    try:
        ele1 = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((MobileBy.ID, tr_home_screen_dict["meeting_title"]["id"]))
        )
        print("Available Untill Time is :", ele1.text)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.XPATH, tr_home_screen_dict["dial_pad_icon"]["xpath"]))
        )
        print("Dial pad is display on the Home Screen ")
        ele3 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.XPATH, tr_home_screen_dict["meeting_button"]["xpath"]))
        )
        print("New Meeting icon is display on the home screen", ele3.text)
        user = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.ID, tr_home_screen_dict["user_name"]["id"]))
        )
        print("Signed User name is :", user.text)
        ele4 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.ID, tr_home_screen_dict["user_phone_number"]["id"]))
        )
        print("Signed user phone number is :", ele4.text)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.XPATH, tr_home_screen_dict["more_button"]["xpath"]))
        )
        print("More option is display on home screen")
    except Exception as e:
        raise AssertionError("Xpath not found")


def verify_current_or_upcoming_meetings_display_on_home_screen(to_device, from_device):
    print("to device :", to_device)
    driver = obj.device_store.get(alias=to_device)
    from_displayname = config["devices"][from_device]["user"]["displayname"]
    print("from_displayname:", from_displayname)
    try:
        ele = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((MobileBy.ID, tr_home_screen_dict["meeting_name"]["id"]))
        )
        print("meeting name is :", ele.text)
        ele1 = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((MobileBy.ID, tr_home_screen_dict["meeting_time"]["id"]))
        )
        print("Meeting time is :", ele1.text)
        meeting_organizer = (tr_home_screen_dict["meeting_organizer"]["xpath"]).replace(
            "config_display", from_displayname
        )
        print("meeting_organizer name is : ", meeting_organizer)
        user = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((MobileBy.ID, tr_home_screen_dict["user_name"]["id"]))
        )
        print(" signed User name is :", user.text)
        elem = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((MobileBy.ID, tr_home_screen_dict["user_phone_number"]["id"]))
        )
        print("Signed User phone number is : ", elem.text)
    except Exception as e:
        raise AssertionError("Meeting is not displayed on home screen")


def verify_no_meeting_schedule_on_landing_page(device):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    try:
        verify_home_page_screen(device)
        elem = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((MobileBy.ID, tr_home_screen_dict["Start_something_new"]["id"]))
        )
        print("No meetings today", elem.text)
    except Exception as e:
        print("Meeting is visible on landing page of home screen", e)


def verify_available_option_to_access_when_clicked_on_ellipsis(device):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    ele1 = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((MobileBy.ID, tr_home_screen_dict["volume_icon"]["id"]))
    )
    print("Volume Icon is visible")
    ele2 = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((MobileBy.XPATH, tr_settings_dict["settings_button"]["xpath"]))
    )
    print("Settings option is visible")
    ele3 = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((MobileBy.XPATH, tr_home_screen_dict["dial_pad_icon"]["xpath"]))
    )
    ele4 = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((MobileBy.XPATH, tr_home_screen_dict["new_meeting"]["xpath"]))
    )
    if ele1.is_displayed() and ele2.is_displayed() and ele3.is_displayed() and ele4.is_displayed():
        print("System volume settings ,settings ,Dial pad and New meeting option is visible")
    else:
        raise AssertionError("System volume settings ,settings ,Dial pad and New meeting option is not visible")


def verify_home_page_screen(device):
    common.wait_for_element(device, tr_home_screen_dict, "more_button")
    common.wait_for_element(device, tr_home_screen_dict, "meeting_button")
    time.sleep(5)
    if not common.is_element_present(device, tr_console_home_screen_dict, "call_icon"):
        common.wait_for_element(device, tr_home_screen_dict, "dial_btn")
    common.wait_for_element(device, tr_home_screen_dict, "share_button")
    common.wait_for_element(device, tr_calendar_dict, "Microsoft_whiteboard_sharing")
    common.wait_for_element(device, tr_calendar_dict, "join_with_an_id")
    common.wait_for_element(device, tr_home_screen_dict, "day_month_date")
    common.wait_for_element(device, tr_home_screen_dict, "clock")
    common.wait_for_element(device, settings_dict, "Help")
    account_name = tr_get_user_name(device)
    phone_number = common.wait_for_element(device, tr_home_screen_dict, "phone_number").text
    common.wait_for_element(device, tr_home_screen_dict, "ring_indicator")
    print(
        f"Phone number and Account name displayed on {device} are - Phone number: {phone_number} , Account name: {account_name}"
    )
    common.wait_for_element(device, tr_home_screen_dict, "add_this_room_label")


def tr_get_username_selector(device):
    # _model = common.device_model(device)
    # if _model in ["oakland"]:
    #     return tr_home_screen_dict, "user_name_v1"
    # if _model in ["spokane", "irvine"]:
    #     return tr_home_screen_dict, "user_name_v2"
    # Backward compatibility: Not explicitly known, assume the legacy selector is still good.
    return tr_home_screen_dict, "user_name_v1"


def tr_get_user_name(device):
    _dict, _dict_key = tr_get_username_selector(device)
    return common.wait_for_element(device, _dict, _dict_key).text


def is_home(device):
    if not common.is_element_present(device, tr_home_screen_dict, "more_button"):
        return False
    _dict, _dict_key = tr_get_username_selector(device)
    return common.is_element_present(device, _dict, _dict_key)


def verify_current_time_display_on_home_screen(device):
    cur_time = common.wait_for_element(device, tr_home_screen_dict, "clock").text
    time_format = ["%H:%M %p", "%H:%M", "%H:%M%p"]
    for _format in time_format:
        try:
            datetime.strptime(cur_time, _format)
            print("Current time is ", cur_time)
            break
        except ValueError:
            if time_format.index(_format) == len(time_format) - 1:
                raise AssertionError(f"{device}: Invalid time format: {cur_time}")


def verify_start_and_end_time_display_on_calendar_tab(device):
    start_and_end_date_and_time = common.wait_for_element(device, calendar_dict, "meeting_time").text
    print(start_and_end_date_and_time)
    split_timer = start_and_end_date_and_time.split("-")
    start_timer = split_timer[0].strip()
    end_timer = split_timer[1].strip()
    print(start_timer, end_timer)
    date_format = "%b %d"
    _format = datetime.strptime(start_timer, date_format)
    print(f"Is the date string '{start_timer}' in the correct format{_format}")
    _format = datetime.strptime(end_timer, date_format)
    print(f"Is the date string '{end_timer}' in the correct format{_format}")


def verify_dial_pad_present_on_landing_page(device):
    common.wait_for_element(device, tr_home_screen_dict, "dial_btn")


def verify_qr_code_visible(device, state):
    if state.lower() not in ["visible", "invisible"]:
        raise AssertionError(f"{device}: Unexpected value for QR code toggle state: {state}")
    if state.lower() == "visible":
        common.wait_for_element(device, tr_home_screen_dict, "qr_code")
        description_text = common.wait_for_element(device, tr_home_screen_dict, "qr_code_description").text.strip()
        expected_description = "Join your meeting with this room"
        if description_text != expected_description:
            raise AssertionError(
                f"QR description does not match expectation: description {description_text} , expected {expected_description}"
            )
    else:
        if common.is_element_present(device, tr_home_screen_dict, "qr_code") or common.is_element_present(
            device, tr_home_screen_dict, "qr_code_description"
        ):
            raise AssertionError(f"{device} QR Code is still present after disabling QR toggle")


def verify_user_details_present_on_landing_page(device):
    account = "user"
    if ":" in device:
        account = device.split(":")[1]
        device = device.split(":")[0]
    verify_current_time_display_on_home_screen(device)
    account_name = tr_get_user_name(device).strip()
    phone_number = common.wait_for_element(device, tr_home_screen_dict, "phone_number").text.strip()
    print(
        f"Phone number and Account name displayed on device are - Phone number: {phone_number} , Account name: {account_name}"
    )
    account_name_expected = config["devices"][device][account]["displayname"]
    phone_number_expected = config["devices"][device][account]["pstndisplay"]
    if account_name != account_name_expected.strip():
        raise AssertionError(
            f"{device}: Account name displayed: {account_name} doesn't match with expected name: {account_name_expected}"
        )
    if phone_number != phone_number_expected.strip():
        raise AssertionError(
            f"{device}: Phone number displayed: {phone_number} doesn't match with expected number: {phone_number_expected}"
        )


def click_on_dial_pad(device):
    common.wait_for_and_click(device, tr_home_screen_dict, "dial_btn")
    common.sleep_with_msg(device, 5, "Wait until to display the dialpad")
    common.hide_keyboard(device)
    common.wait_for_element(device, calls_dict, "phone_number_with_backspace")
    common.wait_for_element(device, tr_calls_dict, "place_call")


def verify_dp_set_on_device(device):
    print("Check for dp set on :", device)
    udid_ = config["devices"][device]["desired_caps"]["udid"]
    print(udid_)
    if config["devices"][device]["model"].lower() in ["sammamish", "spokane", "houston", "laredo"]:
        pd = subprocess.check_output("adb -s " + udid_ + " shell wm density", shell=True)
        value = pd.decode("utf-8")
        print(value.rstrip())
        s = re.findall(r"\d+", value)
        elem1 = int(s[0])
        elem2 = int(s[1])
        print("Actual physical density value :", elem1)
        print("Actual overide density value is: ", elem2)
        expected_pd = config["dpi"]["phyiscal_density"]
        expected_od = config["dpi"]["override_density"]
        if elem1 == expected_pd and elem2 == expected_od:
            print("DPI value set on device is matched")
        else:
            raise AssertionError("DPI value set on device is not matched")
    else:
        pd = subprocess.check_output("adb -s " + udid_ + " shell wm density", shell=True)
        out_put = pd.splitlines()[0].rsplit()[-1].strip()
        result = int(out_put.decode("utf-8"))
        print(result)
        phyiscal_density = config["dpi"]["phyiscal_density"]
        if result == phyiscal_density:
            print("DPI value set on device is matched")
        else:
            raise AssertionError("DPI value set on device is not matched")


def check_teams_app_supported_UI(device):
    print("Check supported UI for :", device)
    udid_ = config["devices"][device]["desired_caps"]["udid"]
    print(udid_)
    py_size = subprocess.check_output("adb -s " + udid_ + " shell wm size", shell=True)
    out_put = py_size.splitlines()[0].rsplit()[-1].strip()
    result = str(out_put, "utf-8")
    print(result)
    expected_val = config["physical_size"]
    if result == expected_val:
        print("Supported Physical UI size is matched")
    else:
        raise AssertionError("Supported Physical UI size is not matched")


def verify_did_displayed_on_homescreen_and_on_dialpad(device):
    account = "user"
    if ":" in device:
        account = device.split(":")[1]
        device = device.split(":")[0]
    phone_number = common.wait_for_element(device, tr_home_screen_dict, "phone_number").text
    if phone_number != config["devices"][device][account]["pstndisplay"]:
        raise AssertionError(f"Phone number displayed is not as expected on homescreen: {phone_number}")
    common.wait_for_and_click(device, tr_home_screen_dict, "dial_btn")
    common.sleep_with_msg(device, 5, "Wait until to display the dialpad")
    common.hide_keyboard(device)
    ph_no_dialpad = common.wait_for_element(device, tr_home_screen_dict, "user_phone_number").text
    expected_text = "Your number is: " + config["devices"][device][account]["pstndisplay"]
    if ph_no_dialpad != expected_text:
        raise AssertionError(f"Phone number {ph_no_dialpad} displayed is not as expected on dialpad: {expected_text}")
    if not common.click_if_present(device, tr_calls_dict, "close_dial_pad_button"):
        if not common.click_if_present(device, calendar_dict, "close_button"):
            common.wait_for_and_click(device, tr_console_signin_dict, "back_layout")


def tap_on_meet_now_and_validate(device):
    common.wait_for_and_click(device, tr_home_screen_dict, "meeting_button")
    common.wait_for_and_click(device, tr_calls_dict, "Add_participants_btn")
    common.wait_for_element(device, console_calendar_dict, "invite_someone_box")
    common.hide_keyboard(device)
    common.wait_for_and_click(device, tr_calls_dict, "close_roaster_button")
    common.wait_for_and_click(device, tr_calls_dict, "close_roaster_button")
    common.wait_for_and_click(device, calls_dict, "Hang_up_button")


def tap_on_dialpad_and_validate(device):
    common.wait_for_and_click(device, tr_home_screen_dict, "dial_btn")
    common.wait_for_element(device, calls_dict, "dial_pad")
    model_ = common.device_model(device)
    if model_ in ["spokane", "sammamish"]:
        common.hide_keyboard(device)
    else:
        driver = obj.device_store.get(alias=device)
        driver.execute_script("mobile: performEditorAction", {"action": "done"})
    common.wait_for_element(device, calls_dict, "phone_number_with_backspace")
    common.wait_for_element(device, tr_calls_dict, "place_call")
    common.wait_for_and_click(device, tr_console_settings_dict, "back_layout")


def tap_on_more_and_validate(device):
    common.wait_for_and_click(device, tr_home_screen_dict, "more_button")
    common.wait_for_element(device, tr_settings_dict, "settings_button")
    common.wait_for_element(device, tr_home_screen_dict, "volume_minus")
    common.wait_for_element(device, tr_home_screen_dict, "volume_plus")
    common.wait_for_element(device, tr_home_screen_dict, "volume_icon")
    common.wait_for_and_click(device, tr_console_settings_dict, "back_layout")


def verify_current_or_upcoming_meetings_displays_on_home_screen(device):
    meeting_name = common.wait_for_element(device, calendar_dict, "meeting_title_name").text
    print("Meeting name :", meeting_name)
    for i in range(6):
        if common.is_element_present(device, panels_home_screen_dict, "next_day_text"):
            break
        tr_calendar_keywords.scroll_up_meeting_tab(device)
    common.wait_for_element(device, tr_home_screen_dict, "next_day_upcoming_meeting")
    if not common.is_element_present(device, panels_home_screen_dict, "teams_logo"):
        print("Meeting logo is visible only when meeting reached to scheduled time")
    meeting_time = common.wait_for_element(device, calendar_dict, "meeting_time").text
    print("Meeting Time :", meeting_time)
    common.wait_for_element(device, calendar_dict, "cnf_device_join_button")
    organizer_name = common.wait_for_element(device, calendar_dict, "meeting_organizer_name").text
    print(f"Meeting organizer : {organizer_name}")


def verify_give_feedback_page(device):
    common.wait_for_and_click(device, settings_dict, "Help")
    common.wait_for_element(device, tr_home_screen_dict, "report_problem")
    common.wait_for_and_click(device, tr_home_screen_dict, "give_feedback")
    common.wait_for_element(device, tr_home_screen_dict, "give_feedback_title")
    common.wait_for_element(device, tr_settings_dict, "send_button")
    common.wait_for_element(device, tr_home_screen_dict, "summarize_feedback_txt")
    common.wait_for_element(device, tr_home_screen_dict, "feedback_text_box")
    common.wait_for_element(device, tr_home_screen_dict, "min_characters_text")
    common.wait_for_element(device, tr_home_screen_dict, "feedback_survey")
    common.wait_for_and_click(device, common_dict, "back")
