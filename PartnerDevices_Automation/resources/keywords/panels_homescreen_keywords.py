import subprocess
import time
import common
import panels_app_settings_keywords
from Selectors import load_json_file
from initiate_driver import obj_dev as obj
from initiate_driver import config
from datetime import datetime
from datetime import timedelta
from selenium.webdriver.support import expected_conditions as EC
import call_keywords
import settings_keywords
from appium.webdriver.common.touch_action import TouchAction
import calendar_keywords

panels_home_screen_dict = load_json_file("resources/Page_objects/panels_homescreen.json")
panels_meeting_resrv_dict = load_json_file("resources/Page_objects/panels_meeting_reservation.json")
calendar_dict = load_json_file("resources/Page_objects/Calendar.json")
panels_device_settings_dict = load_json_file("resources/Page_objects/panels_device_settings.json")
tr_console_signin_dict = load_json_file("resources/Page_objects/rooms_console_signin.json")
home_screen_dict = load_json_file("resources/Page_objects/Home_screen.json")
tr_calendar_dict = load_json_file("resources/Page_objects/tr_calendar.json")

action_time = 2


def verify_room_parameters(device):
    room_name_expected = common.device_displayname(device)
    device = device.split(":")[0]
    settings_keywords.refresh_main_tab(device)
    common.wait_for_element(device, panels_home_screen_dict, "wallpaper")
    time_text = common.wait_for_element(device, panels_home_screen_dict, "time").text
    date_text = common.wait_for_element(device, panels_home_screen_dict, "date").text
    verify_date_and_time_on_panels(time_text, date_text)
    room_name_displayed = common.wait_for_element(device, panels_home_screen_dict, "room_name").text
    if room_name_displayed != room_name_expected:
        raise AssertionError(
            f"Room name expected: {room_name_expected} doesn't match with displayed name: {room_name_displayed}"
        )
    common.wait_for_element(device, panels_home_screen_dict, "calendar_view")


def verify_date_and_time_on_panels(time_text, date_text):
    time_format = ["%H:%M %p", "%H:%M", "%H:%M%p"]
    date_format = ["%A, %B %d", "%m/%d/%y", "%A, %b %d, %Y", "%A, %d %b %Y"]
    for _format in time_format:
        try:
            datetime.strptime(time_text, _format)
            print(f"Time displayed: {time_text}")
            break
        except ValueError:
            if time_format.index(_format) == len(time_format) - 1:
                raise AssertionError(f"Invalid time format: {time_text}")
    for _format in date_format:
        try:
            datetime.strptime(date_text, _format)
            print(f"Date displayed: {date_text}")
            break
        except ValueError:
            if date_format.index(_format) == len(date_format) - 1:
                raise AssertionError(f"Invalid date format: {date_text}")


def verify_scrollable_agenda_view(device):
    device = device.split(":")[0]
    settings_keywords.refresh_main_tab(device)
    settings_keywords.refresh_main_tab(device)
    common.wait_for_element(device, panels_home_screen_dict, "agenda_view")
    title_txt = common.wait_for_element(device, panels_home_screen_dict, "available_tile").text
    if title_txt not in ["Available", "Reserved"]:
        raise AssertionError(f"{device}: current meeting title is not as expected  {title_txt}")
    # Handling All-day meeting scenario, no need to check for 24 hour availability in this case. Refer BUG: 3286571, 3292980
    all_day_time = common.wait_for_element(device, panels_home_screen_dict, "time_range").text.strip().lower()
    settings_keywords.get_screenshot("Successfully found time_range", device_list=device, with_xml=True)
    if all_day_time in ["all-day", "all day"]:
        print(
            f"{device}: Found All-day meeting, no checks required for 24 hour availability. Refer Bug: 3286571, 3292980"
        )
        return
    meeting_start_time = (
        common.wait_for_element(device, panels_home_screen_dict, "time_range").text.split("-")[0].strip()
    )
    scroll_agenda_view(device)
    scroll_agenda_view(device)
    scroll_agenda_view(device)
    last_time_slot = common.wait_for_element(
        device, panels_home_screen_dict, "agenda_view_time_range", cond=EC.presence_of_all_elements_located
    )
    print(f"start time:{meeting_start_time}\t last time slot in agenda view: {last_time_slot}")
    last_element = last_time_slot[-1].text.split("-")[1].strip()
    if meeting_start_time != last_element:
        time1 = meeting_start_time.split(":")[0].strip()
        time2 = last_element.split(":")[0].strip()
        print(f"time1: {time1}\ttime2: {time2}")
        if time1 != time2:
            raise AssertionError(f"Agenda view is not displayed for complete 24 hours")


def verify_meeting_details_in_scrollable_agenda_view(device):
    # meeting_tile_separator has been removed
    # common.wait_for_element(device, panels_home_screen_dict, "meeting_tile_separator")
    common.wait_for_element(device, panels_home_screen_dict, "agenda_view_meeting_name")
    common.wait_for_element(device, panels_home_screen_dict, "agenda_view_time_range")


def scroll_agenda_view(device):
    driver = obj.device_store.get(alias=device)
    window_size = driver.get_window_size()
    print("Window size: ", window_size)
    height = window_size["height"]
    print("Window Height :", height)
    width = window_size["width"]
    print("Window Width :", width)
    print("Swiping co-ordinates : ", 3 * (width / 4), 7 * (height / 8), 3 * (width / 4), 3 * (height / 4))
    for i in range(10):
        driver.swipe(3 * (width / 4), 7 * (height / 8), 3 * (width / 4), 3 * (height / 4))


def validate_room_availability_status(device, status):
    if status.lower() not in ["available", "reserved"]:
        raise AssertionError(f"Unexpected value for status: {status}")
    room_available = is_room_available(device)
    if status.lower() == "available" and not room_available:
        raise AssertionError(f"{device}: Room is reserved")
    if status.lower() == "reserved" and room_available:
        raise AssertionError(f"{device}: Room is still available for reservation")


def verify_room_availability_to_reserve(device, action="verify"):
    if action.lower() not in ["verify", "reserve"]:
        raise AssertionError(f"Unexpected action specified: {action}")
    device = device.split(":")[0]
    availability_status = is_room_available(device)
    if not availability_status:
        print("Room is reserved for the current time slot")
        return
    print("Room is now available for reservation")
    if action.lower() == "reserve":
        check_details_on_scheduling_screen(device)
        reserve_room(device)
        validate_room_availability_status(device, status="reserved")


def is_room_available(device):
    common.wait_for_element(device, panels_home_screen_dict, "calendar_view")
    tile_txt = common.wait_for_element(device, panels_home_screen_dict, "available_tile").text
    print(f"Meeting tile txt is : {tile_txt}")
    if tile_txt == "Available":
        common.wait_for_element(device, panels_home_screen_dict, "available_room")
        common.wait_for_element(device, panels_home_screen_dict, "time_range")
        common.wait_for_element(device, panels_home_screen_dict, "reserve_btn")
        return True
    common.wait_for_element(device, panels_home_screen_dict, "reserved_room")
    common.wait_for_element(device, panels_home_screen_dict, "time_range")
    common.wait_for_element(device, panels_home_screen_dict, "teams_logo")
    return False


def check_details_on_scheduling_screen(device):
    location_name_expected = common.device_displayname(device)
    device = device.split(":")[0]
    common.wait_for_and_click(device, panels_home_screen_dict, "reserve_btn", "id")
    common.wait_for_element(device, panels_meeting_resrv_dict, "ad_hoc_title")
    location_name_displayed = common.wait_for_element(device, panels_meeting_resrv_dict, "location_name").text
    if location_name_displayed != location_name_expected:
        raise AssertionError(
            f"Meeting location displayed: {location_name_displayed} is not as expected: {location_name_expected}"
        )
    meeting_time_slots_verification(device)


def meeting_time_slots_verification(device):
    time1 = (
        common.wait_for_element(device, panels_home_screen_dict, "agenda_view_time_range").text.split("-")[1].strip()
    )
    time_slots_list = common.get_all_elements_texts(device, panels_meeting_resrv_dict, "time_slots")
    if time1 != time_slots_list[0]:
        raise AssertionError(
            f"Meeting end time displayed: {time1} doesn't match with first time slot: {time_slots_list[0]}"
        )
    if len(time_slots_list) > 4:
        raise AssertionError(f"More than four time slots are displayed per page")
    check_time_slots(device)
    if common.click_if_present(device, panels_meeting_resrv_dict, "next_page"):
        time.sleep(2)
        check_time_slots(device)
        common.wait_for_and_click(device, panels_meeting_resrv_dict, "prev_page")


def check_time_slots(device):
    slots_list = common.get_all_elements_texts(device, panels_meeting_resrv_dict, "time_slots")
    print(f"{device}: Time slots are: {slots_list}")
    sorted_slot_list = sorted(slots_list, key=lambda time_string: datetime.strptime(time_string, "%I:%M %p"))
    ordered_slot_list = []
    print(f"Sorted slots list: {sorted_slot_list}")
    # Sort the time slots only if unsorted
    if slots_list != sorted_slot_list:
        for i in range(2):
            ordered_slot_list.append(slots_list[i])
            ordered_slot_list.append(slots_list[i + 2])
        slots_list = ordered_slot_list
    print(f"{device}: time slots list: {slots_list}")
    for j in range(len(slots_list) - 1):
        s1 = datetime.strptime(slots_list[j], "%I:%M %p") + timedelta(minutes=15)
        s1 = s1.strftime("%I:%M %p").lstrip("0")
        if s1.lower() != (slots_list[j + 1]).lower():
            raise AssertionError(f"Meeting timeslots aren't 15 minutes apart - slot1: {s1}, slot2: {slots_list[j + 1]}")


def reserve_room(device):
    expected_room_name = common.device_displayname(device)
    device = device.split(":")[0]
    common.wait_for_and_click(device, panels_meeting_resrv_dict, "time_slots")
    time1 = common.wait_for_element(device, panels_home_screen_dict, "agenda_view_time_range").text
    common.wait_for_and_click(device, panels_meeting_resrv_dict, "reserve_timeslot_btn")
    common.wait_for_element(device, panels_meeting_resrv_dict, "booking_success")
    time2 = common.wait_for_element(device, panels_meeting_resrv_dict, "reserved_time_slot").text
    room_name = common.wait_for_element(device, panels_meeting_resrv_dict, "room_name_on_booking_screen").text
    if time1 != time2:
        start_time_str, end_time_str = time2.split(" - ")
        start_time = datetime.strptime(start_time_str, "%I:%M %p")
        new_start_time = start_time - timedelta(minutes=1)
        new_start_time = new_start_time.strftime("%I:%M %p").lstrip("0")
        time2 = f"{new_start_time} - {end_time_str}"
        print(time2)
        if time1 != time2:
            raise AssertionError(f"Couldn't book room in expected time slot - Expected: {time1}, Reserved: {time2}")
    if room_name != expected_room_name:
        raise AssertionError(f"Expected room: {expected_room_name} name doesn't match with displayed name: {room_name}")


def verify_scheduling_screen_timeout(device):
    common.wait_for_element(device, panels_meeting_resrv_dict, "ad_hoc_title")
    common.wait_for_element(device, panels_home_screen_dict, "wallpaper", wait_attempts=110)


def cancel_room_reservation(device):
    common.wait_for_element(device, panels_meeting_resrv_dict, "ad_hoc_title")
    common.wait_for_element(device, panels_meeting_resrv_dict, "reserve_timeslot_btn")
    common.wait_for_and_click(device, panels_meeting_resrv_dict, "reservation_cancel_btn")
    common.wait_for_element(device, panels_home_screen_dict, "wallpaper")


def verify_extensibility_apps_on_homescreen(device):
    device, account = common.decode_device_spec(device)
    print(f"{device}: account={account}")

    # Issue: no idea what a "standard_user" is - isn't this a "user"? Code below treats "user" and "standard_user" differently.
    if account not in ["user", "cap_user", "premium_user", "standard_user", "auto_checkin_user", "longname_user"]:
        raise AssertionError(f"{device} signin in with unexpexted user: {account}")

    if account not in ["cap_user", "premium_user", "standard_user", "auto_checkin_user", "longname_user"]:
        if not common.is_element_present(device, panels_home_screen_dict, "apps_grid"):
            #
            # Workaround for bug 3411136:
            # The CP AadAuthenticationActivity is gone before automation begins - Re-launch CP
            #   to fetch and re-evaluate the ECS settings (settings include 'Accessibility Apps')
            _udid = common.device_udid(device)
            _cp_app = str(config["companyPortal_Package"])
            _relaunch_cmd = f"adb -s {_udid} shell am start --activity-single-top {_cp_app}/com.microsoft.windowsintune.companyportal.views.AadAuthenticationActivity"
            print(f"{device}: Re-launch CP AadAuthenticationActivity with:\n\t{_relaunch_cmd}")

            subprocess.call(
                _relaunch_cmd,
                shell=True,
            )

            print(f"{device}: Long poll for Extensibility Apps")

            # Wait a couple minutes for the re-signin of Teams while CP is restarting, the "apps_grid" should then appear:
            common.wait_for_element(device, panels_home_screen_dict, "apps_grid", wait_attempts=120)
            common.sleep_with_msg(device, 5, "waiting for extensibility apps to stabilize")

        # See if the 'more' (extensibility apps) is present, and open them:
        common.click_if_present(device, panels_home_screen_dict, "more_extensibility_apps")

        apps_list = common.get_all_elements_texts(device, panels_home_screen_dict, "extensibility_app")

        # Note: the app list also contains the 'More' app!
        print(f"The apps displayed on home screen are: {apps_list}")

        # Dismiss any 'more' (extensibility apps) list:
        common.click_if_present(device, panels_home_screen_dict, "close_more_extensibility_apps")
        return

    # All other accounts should not see any Extensibility apps:
    if common.is_element_present(device, panels_home_screen_dict, "apps_grid") or common.is_element_present(
        device, panels_device_settings_dict, "more_apps"
    ):
        raise AssertionError(device + ": is not signed in with CAP account because apps or apps grid is present")


def tap_on_future_meeting_tiles_and_verify(device):
    # meeting_tile_separator has been removed
    # common.wait_for_element(device, panels_home_screen_dict, "meeting_tile_separator")
    common.wait_for_and_click(device, panels_home_screen_dict, "agenda_view_meeting_name")
    if not common.is_element_present(device, panels_home_screen_dict, "available_tile"):
        common.wait_for_element(device, panels_home_screen_dict, "reserved_room")


def verify_presence_of_check_in_button_on_homescreen(device, presence_status):
    if presence_status.lower() not in ["present", "absent"]:
        raise AssertionError(f"{device}: Unexpected value for presence_status: {presence_status}")
    if presence_status.lower() == "present":
        common.wait_for_element(device, panels_home_screen_dict, "teams_logo")
        common.wait_for_element(device, panels_home_screen_dict, "check_in_btn")
        if common.is_element_present(device, calendar_dict, "join_button"):
            raise AssertionError(f"{device}: Join button is present on homescreen")
    if presence_status.lower() == "absent":
        if common.is_element_present(device, panels_home_screen_dict, "check_in_btn"):
            raise AssertionError(f"{device}: check in button is present on homescreen")


def verify_room_equipment_app_from_homescreen(device, presence_status):
    if presence_status.lower() not in ["present", "absent"]:
        raise AssertionError(f"{device}: Unexpected value for presence_status: {presence_status}")
    panels_app_settings_keywords.go_back_to_homescreen_from_admin_settings_options(device)
    if presence_status.lower() == "present":
        if not common.is_element_present(device, panels_device_settings_dict, "room_equipment_app"):
            common.wait_for_and_click(device, panels_device_settings_dict, "more_apps")
            common.wait_for_element(device, panels_device_settings_dict, "room_equipment_app")
    elif presence_status.lower() == "absent":
        if not common.is_element_present(device, panels_device_settings_dict, "room_equipment_app"):
            common.click_if_present(device, panels_device_settings_dict, "more_apps")
            time.sleep(5)
            if common.is_element_present(device, panels_device_settings_dict, "room_equipment_app"):
                raise AssertionError(f"{device}: Room equipment app is present on homescreen when toggle is turned OFF")
            common.click_if_present(device, panels_device_settings_dict, "go_back_from_more_apps")
            common.wait_for_element(device, panels_home_screen_dict, "time")


def verifying_meeting_name_based_on_show_meeting_name_status(device, toggle):
    if toggle == "on":
        toggle = "true"
    if toggle == "off":
        toggle = "false"
    if toggle.lower() not in ["true", "false"]:
        raise AssertionError(f"Illegal value for 'toggle': '{toggle}'")
    SMN_toggle = common.wait_for_element(device, panels_device_settings_dict, "show_meeting_name_toggle")
    SMN_toggle_status = SMN_toggle.get_attribute("checked")
    call_keywords.come_back_to_home_screen(device)
    organizer_name = common.wait_for_element(device, panels_home_screen_dict, "room_name").text
    meeting_name_disabled = common.wait_for_element(
        device, panels_home_screen_dict, "agenda_view_meeting_name", "xpath"
    ).text
    if toggle.lower() != SMN_toggle_status.lower():
        raise AssertionError(f"Unexpected state for 'show meeting name toggle: {SMN_toggle_status}")
    if toggle.lower() == "false":
        if organizer_name != meeting_name_disabled:
            raise AssertionError(f"{organizer_name} is not matched with {meeting_name_disabled}")
    elif toggle.lower() == "true":
        if meeting_name_disabled not in ["Available", "Reserved"]:
            raise AssertionError(f"{meeting_name_disabled} is not matched with both Available nor Reserved")


def verify_meeting_name_on_panel_homescreen(device, meeting):
    meeting_name = common.wait_for_element(device, panels_home_screen_dict, "agenda_view_meeting_name", "xpath").text
    if meeting_name != meeting:
        settings_keywords.refresh_calls_main_tab(device)
        if meeting_name != meeting:
            raise AssertionError(f"{device}: Expected meeting name: {meeting}, but found: {meeting_name}")


def verifying_meeting_name_based_on_show_meeting_name_status_for_norden(device, toggle):
    if toggle.lower() not in ["on", "off"]:
        raise AssertionError(f"Illegal value for 'toggle': '{toggle}'")
    smn_toggle = common.wait_for_element(device, calendar_dict, "show_meeting_name_toggle").text
    call_keywords.come_back_to_home_screen(device)
    organizer_name = common.wait_for_element(device, panels_home_screen_dict, "agenda_view_meeting_name", "xpath").text
    meeting_name_disabled = common.wait_for_element(device, calendar_dict, "meeting_title_name").text
    if toggle.lower() != smn_toggle.lower():
        raise AssertionError(f"Unexpected state for 'show meeting name toggle: {smn_toggle}")
    if toggle.lower() == "off":
        if organizer_name != meeting_name_disabled:
            raise AssertionError(f"{organizer_name} is not matched with {meeting_name_disabled}")
    elif toggle.lower() == "on":
        if meeting_name_disabled not in ["Available", "Reserved"]:
            raise AssertionError(f"Current meeting tile: {meeting_name_disabled} is neither Available nor Reserved")


def verify_presence_of_check_out_and_extend_reservation_button_on_homescreen(device):
    common.wait_for_element(device, panels_home_screen_dict, "check_out_btn")
    common.wait_for_element(device, panels_home_screen_dict, "extend_room_reservation_btn")
    common.wait_for_and_click(device, panels_home_screen_dict, "dismiss_btn")


def verify_manage_button_on_homescreen(device):
    common.wait_for_element(device, panels_home_screen_dict, "manage_btn")


def verify_and_click_manage_button_on_homescreen(device):
    common.wait_for_and_click(device, panels_home_screen_dict, "manage_btn")


def extend_room_reservation_from_panel_homescreen(device, meeting_type="adhoc"):
    if meeting_type.lower() not in ["adhoc", "outlook"]:
        raise AssertionError(f"Illegal value for 'meeting_type': '{meeting_type}'")
    device_name = device.split(":")[0]
    time1 = common.wait_for_element(device, panels_home_screen_dict, "time_range").text
    start_time_str1, end_time_str1 = time1.split(" - ")
    common.wait_for_and_click(device_name, panels_home_screen_dict, "manage_btn")
    common.wait_for_and_click(device_name, panels_home_screen_dict, "extend_room_reservation_btn")
    common.wait_for_element(device_name, panels_home_screen_dict, "choose_end_time")
    reserve_room(device)
    if meeting_type == "adhoc":
        time2 = common.wait_for_element(device, panels_home_screen_dict, "time_range").text
        start_time_str2, end_time_str2 = time2.split(" - ")
        if end_time_str1 == end_time_str2:
            raise AssertionError(
                f"Couldn't extend room reservation - \nEnd time before extending meeting: {end_time_str1}, End time after extending meeting: {end_time_str2}"
            )


def navigate_inside_room_equipment_app(device):
    common.wait_for_and_click(device, panels_device_settings_dict, "room_equipment_app")
    common.wait_for_element(device, panels_device_settings_dict, "room_equipment_title")


def verify_home_page_of_room_equipment_app(device):
    common.wait_for_element(device, tr_console_signin_dict, "room_name")
    common.wait_for_element(device, home_screen_dict, "hs_time")


def navigate_back_to_home_screen_from_app(device):
    if not common.is_element_present(device, panels_home_screen_dict, "time"):
        common.wait_for_and_click(device, panels_home_screen_dict, "home_btn_on_app")
        common.click_if_present(device, panels_device_settings_dict, "go_back_from_more_apps")


def checkin_into_meeting_from_panel(device, notification_appear):
    if notification_appear.lower() not in ["appear", "not_appear"]:
        raise AssertionError(f"Illegal value for 'state': '{notification_appear}'")
    common.wait_for_and_click(device, panels_home_screen_dict, "check_in_btn")
    if notification_appear.lower() == "appear":
        for i in range(5):
            if common.is_element_present(device, panels_meeting_resrv_dict, "booking_success"):
                return
        raise AssertionError(
            f"when state is: '{notification_appear}' check in successful notification did not appeared"
        )
    if notification_appear.lower() == "not_appear":
        if common.is_element_present(device, panels_meeting_resrv_dict, "booking_success"):
            raise AssertionError(f"when state is: '{notification_appear}' check in successful notification appeared")


def navigate_back_to_home_screen_from_more_apps(device):
    common.click_if_present(device, panels_device_settings_dict, "go_back_from_more_apps")
    common.wait_for_element(device, panels_home_screen_dict, "time")


def verify_no_meeting_can_be_reserved_on_panel(device):
    if common.is_element_present(device, panels_home_screen_dict, "reserve_btn"):
        raise AssertionError(f"{device}: Panel is still available to reserve the meeting")


def verify_state_of_extend_room_reservation_or_check_out_option_on_homescreen(device, option, state):
    if option.lower() not in ["check_out", "extend_rr"]:
        raise AssertionError(f"Illegal value for 'option': '{option}'")
    if state.lower() not in ["enabled", "disabled"]:
        raise AssertionError(f"Illegal value for 'state': '{state}'")
    verify_and_click_manage_button_on_homescreen(device)
    if option.lower() == "check_out":
        ele = common.wait_for_element(device, panels_home_screen_dict, "check_out_btn", "id")
    elif option.lower() == "extend_rr":
        ele = common.wait_for_element(device, panels_home_screen_dict, "extend_room_reservation_btn", "id")
    temp = ele.get_attribute("enabled")
    if state.lower() == "disabled":
        if temp == "true":
            raise AssertionError(f"Unexpected state of {option}, state is:{temp}")
    elif state.lower() == "enabled":
        if temp == "false":
            raise AssertionError(f"Unexpected state of {option}, state is:{temp} :{temp}")
    common.wait_for_and_click(device, panels_home_screen_dict, "dismiss_btn")


def verify_chat_option_on_homescreen(device):
    if common.is_element_present(device, tr_calendar_dict, "chat_option"):
        raise AssertionError(f"{device}: Chat option is present on panel home screen ")


def is_meeting_got_cancelled_in_panel(device):
    print("device :", device)
    if not common.is_element_present(device, panels_home_screen_dict, "reserve_btn"):
        status = "fail"
    else:
        status = "pass"
    return status


def verify_nearby_rooms_app_on_panel_homescreen(device):
    if not common.is_element_present(device, panels_device_settings_dict, "nearby_rooms_app"):
        common.wait_for_and_click(device, panels_device_settings_dict, "more_apps")
        common.wait_for_element(device, panels_device_settings_dict, "nearby_rooms_app")


def navigate_inside_nearby_rooms_app(device):
    common.wait_for_and_click(device, panels_device_settings_dict, "nearby_rooms_app")


def fetch_and_validate_time_format_inside_app(device, time_format):
    if time_format.lower() not in ["24hr", "12hr"]:
        raise AssertionError(f"{device}: Unexpected value for time_format: {time_format}")
    common.wait_for_element(device, panels_device_settings_dict, "nearby_rooms_app")
    actual_time_value = common.wait_for_element(device, home_screen_dict, "hs_time").text
    print(f"actual_time_value:{actual_time_value}")
    am_pm_list = ["am", "pm"]
    if time_format == "12hr":
        time_value = actual_time_value.split(" ")[1].lower()
        if time_value not in ["am", "pm"]:
            raise AssertionError(f"{device}: Time format(12hr) inside app is not as per expected: {time_value}")
    if time_format == "24hr":
        if "am" in actual_time_value.lower() or "pm" in actual_time_value.lower():
            raise AssertionError(f"{device}: Time format(24hr) inside app is not as per expected{actual_time_value}")
    navigate_back_to_home_screen_from_app(device)


def perform_gestures_on_homescreen_panel(device, action):
    driver = obj.device_store.get(alias=device)
    window_size = driver.get_window_size()
    print("Window size: ", window_size)
    height = window_size["height"]
    width = window_size["width"]
    print("Window Width and height :", width, height)
    if width > height:
        if action == "swipe_right":
            print(
                "(0), (height / 2), (width / 5), height / 2: ",
                0,
                height / 2,
                (width / 5),
                height / 2,
            )
            driver.swipe((0), (height / 2), (width / 5), (height / 2))
            time.sleep(action_time)
            driver.swipe((0), height / 2, (width / 5), (height / 2))
        elif action == "swipe_left":
            print(
                "(width-10), (height / 2), (width - 300), height / 2: ",
                width - 10,
                height / 2,
                (width - 200),
                height / 2,
            )
            driver.swipe((width - 10), (height / 2), (width - 300), (height / 2))
            time.sleep(action_time)
            driver.swipe((width - 10), height / 2, (width - 300), (height / 2))
        elif action == "swipe_up":
            print(
                "(width / 2), (height-10), (width / 2), (height) / 2): ",
                width / 2,
                height - 10,
                (width / 2),
                (height / 2),
            )
            driver.swipe((width / 2), (height - 10), (width / 2), (height / 2))
            time.sleep(action_time)
            driver.swipe((width / 2), height - 10, (width / 2), (height / 2))
        elif action == "swipe_down":
            calendar_keywords.scroll_down_main_tab(device)
        elif action == "drag_and_drop":
            common.perform_drag_and_drop(
                device,
                "QR code",
                home_screen_dict,
                "qr_code_container",
                "Agenda view",
                panels_home_screen_dict,
                "agenda_view",
            )
        elif action == "swipe_top_to_bottom":
            print(
                "(width / 2), (10), (width / 2), (height-5): ",
                width / 2,
                10,
                (width / 2),
                (height - 5),
            )
            driver.swipe((width / 2), (10), (width / 2), (height - 5))
            time.sleep(action_time)
            driver.swipe((width / 2), 10, (width / 2), (height - 5))
        elif action == "double_tap":
            for i in range(2):
                common.wait_for_and_click(device, panels_home_screen_dict, "wallpaper")
    else:
        raise AssertionError(f"{device}: Width is less than height")


def verify_presence_of_check_in_button_for_upcoming_meeting_on_homescreen(device, presence_status):
    if presence_status.lower() not in ["present", "absent"]:
        raise AssertionError(f"{device}: Unexpected value for presence_status: {presence_status}")
    if presence_status.lower() == "present":
        common.wait_for_element(device, panels_home_screen_dict, "check_in_btn")
    if presence_status.lower() == "absent":
        if common.is_element_present(device, panels_home_screen_dict, "check_in_btn"):
            raise AssertionError(f"{device}: check in button is present on homescreen")


def verify_long_username_on_panel_homescreen(device):
    expected_room_name = common.device_displayname(device)
    device = device.split(":")[0]
    displayed_room_name = common.wait_for_element(device, panels_home_screen_dict, "room_name").text
    longname_length1 = len(expected_room_name)
    longname_length2 = len(displayed_room_name)
    if longname_length2 <= 50 or (longname_length1 != longname_length2):
        raise AssertionError(
            f"{device}: meeting title: expected {expected_room_name[0:longname_length1]}, displayed {displayed_room_name[0:longname_length2]}"
        )
