from initiate_driver import config
from Libraries.Selectors import load_json_file
import common

display_time = 2
action_time = 3

calls_dict = load_json_file("resources/Page_objects/Calls.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")
tr_settings_dict = load_json_file("resources/Page_objects/tr_settings.json")
tr_device_settings_dict = load_json_file("resources/Page_objects/tr_device_settings.json")
tr_console_signin_dict = load_json_file("resources/Page_objects/rooms_console_signin.json")
tr_console_home_screen_dict = load_json_file("resources/Page_objects/rooms_console_home_screen.json")
tr_console_calls_dict = load_json_file("resources/Page_objects/rooms_console_calls.json")
tr_console_settings_dict = load_json_file("resources/Page_objects/rooms_console_settings.json")
tr_calendar_dict = load_json_file("resources/Page_objects/tr_calendar.json")
tr_calls_dict = load_json_file("resources/Page_objects/tr_calls.json")


def verify_report_an_issue_and_validate(console):
    print("Console :", console)
    common.wait_for_and_click(console, settings_dict, "Report_an_issue")
    common.wait_for_element(console, settings_dict, "issue_title").send_keys(config["Report_feedback"]["title"])
    common.wait_for_element(console, settings_dict, "bug_details").send_keys(config["Report_feedback"]["bug_details"])
    common.wait_for_and_click(console, settings_dict, "send_bug")
    common.wait_for_element(console, settings_dict, "feedback_sent_toast")


def tap_on_more_option(console):
    common.wait_for_and_click(console, tr_console_signin_dict, "more_option")


def verify_more_options(console):
    common.wait_for_element(console, tr_console_home_screen_dict, "meet_now_icon")
    common.wait_for_element(console, tr_calls_dict, "Whiteboard")
    common.wait_for_element(console, tr_calendar_dict, "join_with_an_id")
    common.wait_for_element(console, tr_settings_dict, "settings_button")
    common.wait_for_element(console, tr_console_calls_dict, "volume_icon")
    common.wait_for_element(console, tr_console_calls_dict, "volume_plus")
    common.wait_for_element(console, tr_console_calls_dict, "volume_minus")
    common.wait_for_element(console, settings_dict, "Help")
    common.wait_for_element(console, tr_console_settings_dict, "back_layout")
