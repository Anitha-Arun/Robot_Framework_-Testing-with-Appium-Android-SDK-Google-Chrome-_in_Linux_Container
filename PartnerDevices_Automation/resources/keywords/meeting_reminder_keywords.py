from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Selectors import load_json_file
from initiate_driver import obj_dev as obj
import time
import home_screen_keywords
import calendar_keywords
import datetime
import common
from _datetime import date

display_time = 3
action_time = 3
wait_time = 60

meeting_reminder_dict = load_json_file("resources/Page_objects/Meeting_reminder.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")
calls_dict = load_json_file("resources/Page_objects/Calls.json")
calendar_dict = load_json_file("resources/Page_objects/Calendar.json")
navigation_dict = load_json_file("resources/Page_objects/Navigation.json")
device_settings_dict = load_json_file("resources/Page_objects/Device_settings.json")
common_dict = load_json_file("resources/Page_objects/Common.json")


def verify_meeting_notification_scroll(device):
    print("device: ", device)
    driver = obj.device_store.get(alias=device)
    window_size = driver.get_window_size()
    print("Window size: ", window_size)
    height = window_size["height"]
    print("Window Height :", height)
    width = window_size["width"]
    print("Window Width :", width)
    if height > width:
        print("Swiping co-ordinates : ", width / 2, 4 * (height / 5), width / 2, height / 5)
        driver.swipe(width / 2, 4 * (height / 5), width / 2, height / 5)
    else:
        print("Swiping co-ordinates : ", width / 4, 4 * (height / 5), width / 4, height / 5)
        driver.swipe(width / 4, 4 * (height / 5), width / 4, height / 5)
    print("scroll the meeting notification on home screen")
    pass


def verify_meeting_notification_on_home_screen(device):
    devices = device.split(",")
    print("device :", device)
    for device in devices:
        driver = obj.device_store.get(alias=device)
        try:
            ele = (
                WebDriverWait(driver, 30)
                .until(EC.element_to_be_clickable((MobileBy.ID, meeting_reminder_dict["notifications"]["id"])))
                .text
            )
            if ele.is_displayed():
                print("Notification is present on home screen")
        except Exception as e:
            print(e)
        raise AssertionError("Notification is not present on home screen")


def verify_meeting_notification_remove_from_home_screen(device):
    devices = device.split(",")
    print("device :", device)
    for device in devices:
        list_of_meeting_titles = common.get_all_elements_texts(device, meeting_reminder_dict, "notifications")
        print("List of Meeting titles:", list_of_meeting_titles)
        for ele in range(0, len(list_of_meeting_titles)):
            ele_li = len(list_of_meeting_titles) - 1
            print("Organizer Cancel the meeting Successfully", ele_li)


def validate_meeting_reminder_notification_for_upcoming_time_on_home_screen(device, meeting="test_meeting"):
    print("device :", device)
    meeting = meeting.split(",")
    print("meeting:", meeting)
    common.wait_for_element(device, meeting_reminder_dict, "notifications")
    common.wait_for_element(device, meeting_reminder_dict, "meeting_name")
    upcoming_time = common.wait_for_element(device, meeting_reminder_dict, "upcoming_time")
    item = upcoming_time.text
    print("Upcoming time is :", str(item))
    initial_time = [int(i) for i in item.split() if i.isdigit()]
    print("Current Time is :", initial_time)
    delay_time = initial_time[0]
    print("Upcoming time in Mins: ", delay_time)
    time.sleep(wait_time)
    print("Upcoming time after wait of 1 min of delay :", delay_time)
    previous_time = delay_time - wait_time
    if delay_time > previous_time:
        common.sleep_with_msg(device, delay_time * 60, "waiting for meeting start")
    join_btn = common.wait_for_element(device, meeting_reminder_dict, "join_button")
    print("Meeting Join button is present", join_btn.text)
    upcoming_time = common.wait_for_element(device, meeting_reminder_dict, "upcoming_time")
    print("Upcoming time :", upcoming_time.text)
    if upcoming_time.text == "Now":
        print("Upcoming meeting reminder time is reached to now")


def verify_meeting_present_on_home_screen(device, meeting):
    devices = device.split(",")
    print("device :", device)
    calendar_keywords.navigate_to_calendar_tab(device)
    meting_exists = calendar_keywords.meeting_exist_or_not(device, meeting)
    if meting_exists:
        meeting_startTime_str = calendar_keywords.get_meeting_time(device).split("—")[0]
        current_time = datetime.datetime.now()
        todayDate = date.today()
        meeting_startTime_str = str(todayDate) + meeting_startTime_str
        meeting_time = datetime.datetime.strptime(meeting_startTime_str, "%Y-%m-%d%I:%M %p")
        timeDiff = round(((meeting_time - current_time).seconds) / 60)
        if timeDiff > 15 and meeting_time > current_time:
            notification_wait_time = int(timeDiff - 15) * 60
            print("Waiting for {0} seconds to notification present on Home Screen", notification_wait_time)
            time.sleep(notification_wait_time)
    else:
        raise AssertionError("Created Meeting has not reflected in meeting list")
    home_screen_keywords.come_back_to_home_screen_page_and_verify(device)
    for device in devices:
        common.wait_for_element(device, meeting_reminder_dict, "meeting_name")
        common.wait_for_element(device, meeting_reminder_dict, "meeting_time")
        common.wait_for_element(device, meeting_reminder_dict, "upcoming_time")
        common.wait_for_element(device, meeting_reminder_dict, "join_button")


def verify_meeting_notifications_should_not_overlap_when_meetings_scheduled_at_same_time(
    device, meetings="test_meeting"
):
    print("device :", device)
    meeting = meetings.split(",")
    print("Meeting List:", meeting)
    elem = common.get_all_elements_texts(device, meeting_reminder_dict, "notifications_recycler_view")
    for i in range(len(elem)):
        common.wait_for_element(device, meeting_reminder_dict, "notifications")
        common.wait_for_element(device, meeting_reminder_dict, "meeting_name")
        common.wait_for_element(device, meeting_reminder_dict, "meeting_time")
        verify_meeting_notification_scroll(device)
        common.wait_for_element(device, meeting_reminder_dict, "upcoming_time")
        common.wait_for_element(device, meeting_reminder_dict, "join_button")


def get_meeting_start_remaining_time(device):
    print("device :", device)
    upcoming_time = common.wait_for_element(device, meeting_reminder_dict, "upcoming_time")
    item = upcoming_time.text
    print("Upcoming time is :", str(item))
    initial_time = [int(i) for i in item.split() if i.isdigit()]
    print("Current Time is :", initial_time)
    delay_time = initial_time[0]
    print("Upcoming time in Mins: ", delay_time)
    return delay_time


def validate_meeting_reminder_notification_for_upcoming_time_interval_on_home_screen(device, meeting="test_meeting"):
    print("device :", device)
    common.wait_for_element(device, meeting_reminder_dict, "notifications")
    common.wait_for_element(device, meeting_reminder_dict, "meeting_name")
    # check for the 2nd notification 15 min timer and wait for next timer
    delay_time = get_meeting_start_remaining_time(device)
    print("Upcoming time in Mins: ", delay_time)
    if delay_time > 10:
        wait_time_2nd_notification = delay_time - 10
        print("Upcoming 10 min time notification will appear after (in mins) :", wait_time_2nd_notification)
        common.sleep_with_msg(device, wait_time_2nd_notification * 60, "waiting for meeting start")

    # check for the 2nd notification 10 min timer and wait for next timer
    delay_time_2 = get_meeting_start_remaining_time(device)
    print("Upcoming time in Mins: ", delay_time_2)
    if delay_time_2 > 5:
        wait_time_2nd_notification = delay_time_2 - 5
        print("Upcoming 5 min time notification will appear after (in mins) :", wait_time_2nd_notification)
        common.sleep_with_msg(device, wait_time_2nd_notification * 60, "waiting for meeting start")

    # check for the 2nd notification 5 min timer and wait for next timer
    delay_time_3 = get_meeting_start_remaining_time(device)
    print("Upcoming time in Mins: ", delay_time_3)
    common.sleep_with_msg(device, delay_time * 60, "waiting for meeting start")

    common.wait_for_element(device, meeting_reminder_dict, "join_button")
    upcoming_time = common.wait_for_element(device, meeting_reminder_dict, "upcoming_time")
    if upcoming_time.text == "Now":
        print("Upcoming meeting reminder time is reached to now")
