import call_keywords
import common
from selenium.webdriver.support import expected_conditions as EC
import tr_calendar_keywords
from initiate_driver import config
import panels_app_settings_keywords
from Selectors import load_json_file
import time
import settings_keywords
import tr_settings_keywords
import calendar_keywords
import device_settings_keywords

action_time = 3
max_attempt = 5

panels_device_settings_dict = load_json_file("resources/Page_objects/panels_device_settings.json")
panels_home_screen_dict = load_json_file("resources/Page_objects/panels_homescreen.json")
panels_meeting_resrv_dict = load_json_file("resources/Page_objects/panels_meeting_reservation.json")
navigation_dict = load_json_file("resources/Page_objects/Navigation.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")
tr_settings_dict = load_json_file("resources/Page_objects/tr_device_settings.json")
tr_device_settings_dict = load_json_file("resources/Page_objects/tr_device_settings.json")
device_settings_dict = load_json_file("resources/Page_objects/Device_settings.json")
calendar_dict = load_json_file("resources/Page_objects/Calendar.json")
tr_calendar_dict = load_json_file("resources/Page_objects/tr_calendar.json")
calendar_dict = load_json_file("resources/Page_objects/Calendar.json")
home_screen_dict = load_json_file("resources/Page_objects/Home_screen.json")
app_bar_dict = load_json_file("resources/Page_objects/App_bar.json")
calls_dict = load_json_file("resources/Page_objects/Calls.json")


def verify_device_settings_option_in_panel(device, password_type="old"):
    if password_type.lower() not in ["old", "new"]:
        raise AssertionError(f"{device}: Unexpected value for password_type: {password_type}")
    if password_type == "new":
        password = config["devices"][device]["admin_new_password"]
    elif password_type == "old":
        password = config["devices"][device]["admin_password"]
    settings_keywords.click_device_settings(device)

    _model = config["devices"][device]["model"].lower()

    if _model == "beverly hills":
        common.wait_for_element(device, settings_dict, "About")
        common.wait_for_element(device, settings_dict, "accessibility")
        common.wait_for_element(device, panels_device_settings_dict, "Reboot_panel")
    elif _model in ["westchester", "brooklyn", "hollywood"]:
        common.hide_keyboard(device)
        common.wait_for_element(device, settings_dict, "About")
        common.wait_for_element(device, settings_dict, "accessibility")
        common.wait_for_element(device, panels_device_settings_dict, "Reboot_panel")
    elif _model == "arlington":
        common.wait_for_element(device, settings_dict, "About")
        common.wait_for_element(device, settings_dict, "accessibility")
        common.wait_for_element(device, settings_dict, "Debug")
        common.wait_for_element(device, tr_device_settings_dict, "admin_settings", "xpath1")
    elif _model == "savannah":
        common.wait_for_and_click(device, panels_device_settings_dict, "admin_pswd_field")
        common.wait_for_element(device, panels_device_settings_dict, "admin_pswd_field").set_value(password)
        common.wait_for_and_click(device, panels_device_settings_dict, "admin_login_continue_btn")
        if common.is_element_present(device, panels_device_settings_dict, "network_btn"):
            calendar_keywords.scroll_down_device_setting_tab(device)
            calendar_keywords.scroll_down_device_setting_tab(device)
        common.wait_for_element(device, settings_dict, "About")
        common.wait_for_element(device, settings_dict, "accessibility", wait_attempts=40)
        common.wait_for_and_click(device, settings_dict, "Debug")
        common.wait_for_element(device, panels_device_settings_dict, "Reboot_panel")
    elif _model == "flint":
        common.wait_for_element(device, device_settings_dict, "system_settings")
        common.wait_for_element(device, settings_dict, "accessibility")
    elif _model == "richland":
        common.wait_for_element(device, settings_dict, "accessibility")
        common.wait_for_element(device, settings_dict, "About")
        common.wait_for_element(device, tr_device_settings_dict, "admin_settings")
    elif _model == "surprise":
        if common.is_element_present(device, device_settings_dict, "teams_admin_settings"):
            calendar_keywords.scroll_down_device_setting_tab(device)
            calendar_keywords.scroll_down_device_setting_tab(device)
        common.wait_for_element(device, settings_dict, "About")
        common.wait_for_element(device, settings_dict, "accessibility")
        common.wait_for_element(device, panels_device_settings_dict, "Reboot_panel")
    else:
        raise AssertionError(f"{device}: No validation specified for device model '{_model}'")


def navigate_inside_of_teams_admin_settings_in_panel(device, password_type="old"):
    if password_type.lower() not in ["old", "new"]:
        raise AssertionError(f"{device}: Unexpected value for password_type: {password_type}")

    _model = config["devices"][device]["model"].lower()

    if _model in ["beverly hills", "hollywood"]:
        # Device needs credentials AFTER clicking on 'Teams Admin Settings'
        # Swipe down to 'Teams Admin Settings':
        _attempt = 0
        while _attempt < 4:
            if common.is_element_present(device, tr_device_settings_dict, "deviceSettingsOption_TeamsAdminSettings"):
                break
            settings_keywords.swipe_till_end(device)
            _attempt += 1
        common.wait_for_and_click(device, tr_device_settings_dict, "deviceSettingsOption_TeamsAdminSettings")
        navigate_inside_admin_setting_in_panel(device, password_type)
        return

    # All other devices need credentials BEFORE clicking on 'Teams Admin Settings'

    navigate_inside_admin_setting_in_panel(device, password_type)
    if _model in ["westchester", "brooklyn"]:
        common.sleep_with_msg(device, 3, "Waiting for Admin settings page to load")
        device_settings_keywords.swipe_till_sign_out(device)
        time.sleep(3)
        device_settings_keywords.swipe_till_sign_out(device)
        common.wait_for_element(device, panels_device_settings_dict, "account_sign_out")
        common.wait_for_and_click(device, panels_device_settings_dict, "panels_app_settings")
        common.wait_for_and_click(device, panels_device_settings_dict, "panels_app_settings1")
    elif _model == "savannah":
        device_settings_keywords.swipe_till_sign_out(device)
        device_settings_keywords.swipe_till_sign_out(device)
        device_settings_keywords.swipe_till_sign_out(device)
        common.wait_for_and_click(device, tr_device_settings_dict, "teams_admin_settings2")
    elif _model == "arlington":
        common.wait_for_and_click(device, device_settings_dict, "system_settings")
        common.wait_for_and_click(device, tr_device_settings_dict, "service_provider")
        common.wait_for_and_click(device, tr_device_settings_dict, "teams_admin_settings1")
    elif _model == "flint":
        common.wait_for_and_click(device, tr_device_settings_dict, "teams_admin_settings2", "id1")
        common.wait_for_element(device, tr_device_settings_dict, "teams_admin_settings1")

    elif _model == "richland":
        common.wait_for_element(device, tr_device_settings_dict, "admin_settings")
        common.wait_for_and_click(device, tr_device_settings_dict, "teams_admin_settings1")
    elif _model == "surprise":
        device_settings_keywords.swipe_till_admin_settings(device)
        device_settings_keywords.swipe_till_admin_settings(device)
        common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings")
        common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings", "xpath")
    else:
        raise AssertionError(f"{device}: Cannot handle model '{_model}'")


def go_to_meetings_tab_in_panel(device):
    common.wait_for_and_click(device, panels_device_settings_dict, "meetings_in_panel")
    common.wait_for_element(device, tr_calendar_dict, "show_meeting_names_text")


def verify_room_equipment_toggle_in_panel_is_off(device):
    RE_toggle = common.wait_for_element(device, panels_device_settings_dict, "room_equipment_toggle")
    toggle_btn_status = RE_toggle.get_attribute("checked")
    if toggle_btn_status != "false":
        raise AssertionError(f"Illegal state for room equipment toggle: '{toggle_btn_status}'")


def enable_or_disable_room_equipment_toggle_in_panel(device, activity_state):
    common.change_toggle_button(device, panels_device_settings_dict, "room_equipment_toggle", activity_state)


def verify_room_reservation_toggle_in_panel(device):
    common.wait_for_element(device, panels_device_settings_dict, "room_reserve_txt")
    common.wait_for_element(device, panels_device_settings_dict, "room_reservation_toggle")


def verify_room_reservation_toggle_in_panel_is_on(device):
    RR_toggle = common.wait_for_element(device, panels_device_settings_dict, "room_reservation_toggle")
    toggle_btn_status = RR_toggle.get_attribute("checked")
    if toggle_btn_status != "true":
        raise AssertionError(f"Illegal state for room reservation toggle: '{toggle_btn_status}'")


def enable_or_disable_show_meeting_name_toggle_in_panel(device, show_meeting_state):
    common.change_toggle_button(device, panels_device_settings_dict, "show_meeting_name_toggle", show_meeting_state)


def verify_checkin_toggle_button_in_panel(device):
    checkin = common.wait_for_element(device, panels_device_settings_dict, "checkin_toggle_btn")
    checkin_status = checkin.get_attribute("checked")
    if checkin_status != "false":
        common.wait_for_and_click(device, panels_device_settings_dict, "checkin_toggle_btn")
    checkin = common.wait_for_element(device, panels_device_settings_dict, "checkin_toggle_btn")
    checkin_status = checkin.get_attribute("checked")
    if checkin_status != "false":
        raise AssertionError(f"{device}: 'Checkin button' has unexpected state by default: {checkin_status}")


def enable_or_disable_checkin_toggle_button_in_panel(device, state):
    common.change_toggle_button(device, panels_device_settings_dict, "checkin_toggle_btn", state)


def select_release_time_for_meeting(device, release_time):
    print(f"{device}: Selecting meeting release time '{release_time}'")
    common.wait_for_and_click(device, panels_device_settings_dict, "room_release_time_dropdown")
    specific_release = common.get_dict_copy(
        panels_device_settings_dict, "room_release_time_specific", "replace", release_time
    )
    common.wait_for_and_click(device, specific_release, "room_release_time_specific")
    panels_app_settings_keywords.go_back_to_homescreen_from_admin_settings_options(device)


def checkout_of_the_reserved_meeting(device):
    settings_keywords.refresh_calls_main_tab(device)
    # Possibility that extended meeting is in the upcoming slot and current slot is available to reserve
    # checking if extended meeting is present or not
    meeting_names_list = common.get_all_elements_texts(
        device, panels_home_screen_dict, "agenda_view_meeting_name", "id"
    )
    if (
        not common.is_element_present(device, panels_home_screen_dict, "reserve_btn")
        or "[Extended]" in meeting_names_list
    ):
        # Setup for cancelling extended meeting from panel
        # waiting till we reach start time of extended meeting
        meeting_title = common.wait_for_element(
            device, panels_home_screen_dict, "agenda_view_meeting_name", "xpath"
        ).text
        if "Available" in meeting_title or "[Extended]" in meeting_title:
            common.click_if_element_appears(device, panels_home_screen_dict, "manage_btn", max_attempts=300)
        else:
            common.wait_for_and_click(device, panels_home_screen_dict, "manage_btn")
        common.wait_for_and_click(device, panels_home_screen_dict, "check_out_btn", "xpath")
        common.wait_for_and_click(device, panels_home_screen_dict, "check_out_btn", "xpath1")
        common.wait_for_element(device, panels_home_screen_dict, "available_room")


def enable_or_disable_extend_room_reservation_toggle_btn_in_panel(device, extend_rr_state):
    for i in range(max_attempt):
        if common.is_element_present(device, panels_device_settings_dict, "extend_room_reservation_txt"):
            break
        tr_settings_keywords.swipe_screen_page(device)
    common.wait_for_element(device, panels_device_settings_dict, "extend_room_reservation_txt")
    common.change_toggle_button(device, panels_device_settings_dict, "extend_room_reservation_toggle", extend_rr_state)


def verify_presence_of_check_out_and_extend_reservation_button_in_meetings(device):
    for i in range(max_attempt):
        if common.is_element_present(device, panels_device_settings_dict, "extend_room_reservation_txt"):
            break
        tr_settings_keywords.swipe_screen_page(device)
    common.wait_for_element(device, panels_device_settings_dict, "check_out_txt")
    common.wait_for_element(device, panels_device_settings_dict, "extend_room_reservation_txt")


def verify_presence_of_max_room_capacity_toggle_button_in_panel(device, presence_status):
    if presence_status.lower() not in ["present", "absent"]:
        raise AssertionError(f"{device}: Unexpected value for presence_status: {presence_status}")
    if presence_status.lower() == "present":
        common.wait_for_element(device, panels_device_settings_dict, "Max_room_occupancy_text")
    elif presence_status.lower() == "absent":
        if common.is_element_present(device, panels_device_settings_dict, "Max_room_occupancy_text"):
            raise AssertionError(f"{device}: Max room occupany option is present before device pairing")


def enable_or_disable_max_room_capacity_toggle_button_in_panel(device, activity_status):
    common.wait_for_element(device, panels_device_settings_dict, "Max_room_occupancy_text")
    common.change_toggle_button(device, panels_device_settings_dict, "Max_room_occupancy_toggle", activity_status)


def verify_max_room_capacity_toggle_in_panel_is_off(device):
    MRC_toggle = common.wait_for_element(device, panels_device_settings_dict, "Max_room_occupancy_toggle")
    MRC_toggle_status = MRC_toggle.get_attribute("checked")
    if MRC_toggle_status != "false":
        raise AssertionError(f"Illegal state for room equipment toggle: '{MRC_toggle_status}'")


def verify_room_release_activity_based_on_checkin_into_meeting(device, state, meeting):
    if state.lower() not in ["not_released", "released"]:
        raise AssertionError(f"{device}: Unexpected value for meeting release state: {state}")
    temp_dict = common.get_dict_copy(calendar_dict, "meeting", "meeting_xpath_replace", meeting)
    if state.lower() == "not_released":
        tr_calendar_keywords.verify_meeting_display_on_home_screen(device)
        if common.is_element_present(device, panels_device_settings_dict, "room_released_alert"):
            raise AssertionError(f"{device}: Room is released before time")
    elif state.lower() == "released":
        if not common.is_element_present(
            device, panels_device_settings_dict, "room_released_alert"
        ) or common.is_element_present(device, temp_dict, "meeting"):
            raise AssertionError(f"{device}: Room is not released even after release time is finished")


def verify_presence_of_room_release_warning(device, presence):
    if presence.lower() not in ["present", "absent"]:
        raise AssertionError(f"{device}: Unexpected value for meeting release warning state: {presence}")
    if presence.lower() == "present":
        common.wait_for_element(device, panels_device_settings_dict, "room_release_warning")
        common.wait_for_and_click(device, panels_home_screen_dict, "dismiss_notification_btn")
    elif presence.lower() == "absent":
        if common.is_element_present(device, panels_device_settings_dict, "room_release_warning"):
            raise AssertionError(f"{device}: Room release warning is present even after release time is completed")


def enable_or_disable_checkin_notification_toggle_button_in_panel(device, checkin_notification_state):
    common.change_toggle_button(
        device, panels_device_settings_dict, "checkin_notification_toggle", checkin_notification_state
    )


def enable_or_disable_room_reservation_toggle_in_panel(device, room_reservation_state):
    common.change_toggle_button(device, panels_device_settings_dict, "room_reservation_toggle", room_reservation_state)


def validate_room_reservation_toggle_when_enabled_or_disbaled(device, room_reservation_state):
    if room_reservation_state.lower() == "on":
        panels_app_settings_keywords.go_back_to_homescreen_from_admin_settings_options(device)
        common.wait_for_element(device, panels_home_screen_dict, "reserve_btn")
    elif room_reservation_state.lower() == "off":
        panels_app_settings_keywords.go_back_to_homescreen_from_admin_settings_options(device)
        if not common.is_element_present(device, home_screen_dict, "qr_code_container"):
            common.wait_for_element(device, panels_device_settings_dict, "room_reservation_disabled_msg")
        common.wait_for_element(device, panels_home_screen_dict, "available_room")
        if common.is_element_present(device, panels_home_screen_dict, "reserve_btn"):
            raise AssertionError(f"{device}: 'Reserve' button is displayed even after disabling 'Room reservation'")


def enable_or_disable_check_out_toggle_btn_in_panel(device, checkout_toggle_status):
    for i in range(max_attempt):
        if common.is_element_present(device, panels_device_settings_dict, "check_out_toggle_btn"):
            break
        tr_settings_keywords.swipe_screen_page(device)
    # Assuming the toggle button LABEL is at/above the toggle button itself:
    common.wait_for_element(device, panels_device_settings_dict, "check_out_txt")
    common.change_toggle_button(device, panels_device_settings_dict, "check_out_toggle_btn", checkout_toggle_status)


def Verify_extended_meeting_title_on_panel_homescreen(device, presence_status):
    if presence_status.lower() not in ["present", "absent"]:
        raise AssertionError(f"{device}: Unexpected value for presence_status: {presence_status}")
    settings_keywords.refresh_calls_main_tab(device)
    meeting_names_list = common.get_all_elements_texts(
        device, panels_home_screen_dict, "agenda_view_meeting_name", "id"
    )
    meeting_title = common.wait_for_element(device, panels_home_screen_dict, "agenda_view_meeting_name", "xpath").text
    print(f"meeting_names_list:{meeting_names_list}")
    extended_meeting_title = "[Extended] " + meeting_title
    print(f"/n extended_meeting_title: {extended_meeting_title}")
    if presence_status == "present" and meeting_title != "Available":
        if extended_meeting_title not in meeting_names_list:
            raise AssertionError(
                f"The meeting didn't get extended meetings present on homescreen are :{meeting_names_list} "
            )
    else:
        if extended_meeting_title in meeting_names_list:
            raise AssertionError(
                f"The exetend meeting got created, meetings present on homesacreen are :{meeting_names_list}"
            )


def modify_admin_password_in_panel(device, status):
    admin_pass = config["devices"][device]["admin_new_password"]
    if status.lower() not in ["set", "reset"]:
        raise AssertionError(f"{device}: Unexpected value for status: {status}")
    if status.lower() == "set":
        old_pass = config["devices"][device]["admin_password"]
        new_pass = admin_pass
        password_type = "old"
    elif status.lower() == "reset":
        old_pass = admin_pass
        new_pass = config["devices"][device]["admin_password"]
        password_type = "new"

    if config["devices"][device]["model"].lower() in ["beverly hills", "hollywood"]:
        device_settings_keywords.swipe_till_sign_out(device)
        common.wait_for_and_click(device, panels_device_settings_dict, "system_button")
        navigate_inside_admin_setting_in_panel(device, password_type)
        common.wait_for_and_click(device, panels_device_settings_dict, "pass_reset_button")
        if config["devices"][device]["model"].lower() == "hollywood":
            common.wait_for_and_click(device, panels_device_settings_dict, "pass_reset_button")
        pass_edit_boxes = common.wait_for_element(
            device, panels_device_settings_dict, "pass_editbox", cond=EC.presence_of_all_elements_located
        )
        pass_edit_boxes[0].set_value(old_pass)
        pass_edit_boxes[1].set_value(new_pass)
        pass_edit_boxes[2].set_value(new_pass)
        common.hide_keyboard(device)
        common.wait_for_and_click(device, panels_device_settings_dict, "save_admin_pass")
        common.click_if_present(device, device_settings_dict, "ok")
    if config["devices"][device]["model"].lower() == "arlington":
        common.wait_for_and_click(device, tr_device_settings_dict, "admin_settings", "xpath1")
        common.wait_for_and_click(device, panels_device_settings_dict, "pass_reset_button", "id")
        common.hide_keyboard(device)
        common.wait_for_element(device, panels_device_settings_dict, "Admin_old_pwd", "id1").set_value(old_pass)
        common.wait_for_element(device, panels_device_settings_dict, "Admin_new_pwd", "id1").set_value(new_pass)
        common.wait_for_element(device, panels_device_settings_dict, "Admin_confirm_pwd", "id1").set_value(new_pass)
        common.wait_for_and_click(device, calendar_dict, "change_btn", "id")
        common.wait_for_and_click(device, panels_device_settings_dict, "close_button", "id1")

    if config["devices"][device]["model"].lower() in ["westchester", "brooklyn"]:
        common.wait_for_and_click(device, tr_device_settings_dict, "teams_admin_settings1")
        common.wait_for_element(device, panels_device_settings_dict, "admin_pswd_field").set_value(old_pass)
        common.hide_keyboard(device)
        common.wait_for_and_click(device, panels_device_settings_dict, "admin_login_btn")
        common.sleep_with_msg(device, 3, "Waiting for Admin settings page to load")
        device_settings_keywords.swipe_till_sign_out(device)
        time.sleep(3)
        device_settings_keywords.swipe_till_sign_out(device)
        common.wait_for_element(device, panels_device_settings_dict, "account_sign_out")
        common.wait_for_and_click(device, panels_device_settings_dict, "admin_pass_button")
        common.wait_for_element(device, panels_device_settings_dict, "Admin_old_pwd", "id").set_value(old_pass)
        common.wait_for_element(device, panels_device_settings_dict, "Admin_new_pwd", "id").set_value(new_pass)
        common.wait_for_element(device, panels_device_settings_dict, "Admin_confirm_pwd", "id").set_value(new_pass)
        common.hide_keyboard(device)
        common.wait_for_and_click(device, calendar_dict, "change_btn")
        common.wait_for_and_click(device, device_settings_dict, "admin_settings_yes")

    if config["devices"][device]["model"].lower() == "surprise":
        common.wait_for_and_click(device, settings_dict, "Device_administration")
        if common.is_element_present(device, panels_device_settings_dict, "login_btn"):
            common.wait_for_and_click(device, panels_device_settings_dict, "login_btn")
            common.wait_for_element(device, settings_dict, "admin_passwd", "xpath").set_value(
                config["devices"][device]["admin_password"]
            )
            common.wait_for_and_click(device, calendar_dict, "ok_button")
        common.wait_for_and_click(device, panels_device_settings_dict, "pass_reset_button")
        common.wait_for_element(device, panels_device_settings_dict, "Admin_old_pwd1").set_value(old_pass)
        common.wait_for_element(device, panels_device_settings_dict, "Admin_new_pwd1").set_value(new_pass)
        common.wait_for_element(device, panels_device_settings_dict, "Admin_confirm_pwd1").set_value(new_pass)
        common.wait_for_and_click(device, calendar_dict, "ok_button")

    if config["devices"][device]["model"].lower() == "richland":
        common.wait_for_and_click(device, panels_device_settings_dict, "admin_settings")
        common.wait_for_element(device, device_settings_dict, "admin_username_box").set_value(
            config["devices"][device]["admin_username"]
        )
        common.wait_for_element(device, settings_dict, "admin_passwd", "id1").set_value(old_pass)
        common.wait_for_and_click(device, calendar_dict, "ok_button")
        common.wait_for_and_click(device, device_settings_dict, "system_settings")
        common.wait_for_and_click(device, device_settings_dict, "security_btn")
        common.wait_for_and_click(device, calendar_dict, "change_btn")
        common.wait_for_element(device, panels_device_settings_dict, "Admin_old_pwd1").set_value(old_pass)
        common.wait_for_element(device, panels_device_settings_dict, "Admin_new_pwd1").set_value(new_pass)
        common.wait_for_element(device, panels_device_settings_dict, "Admin_confirm_pwd1").set_value(new_pass)
        common.wait_for_and_click(device, panels_device_settings_dict, "save_password")
    call_keywords.come_back_to_home_screen(device)


def verify_display_settings_option_in_panel(device):
    settings_keywords.click_device_settings(device)
    if config["devices"][device]["model"].lower() in ["beverly hills", "hollywood"]:
        common.wait_for_and_click(device, panels_device_settings_dict, "display_setting")
        common.wait_for_element(device, panels_device_settings_dict, "admin_pswd_field").set_value(
            config["devices"][device]["admin_password"]
        )
        common.wait_for_and_click(device, panels_device_settings_dict, "admin_login_btn")
        common.wait_for_element(device, panels_device_settings_dict, "adaptive_brightness_txt")
    if config["devices"][device]["model"].lower() in ["westchester", "brooklyn"]:
        common.wait_for_and_click(device, tr_device_settings_dict, "teams_admin_settings1")
        common.wait_for_element(device, panels_device_settings_dict, "admin_pswd_field").set_value(
            config["devices"][device]["admin_password"]
        )
        common.hide_keyboard(device)
        common.wait_for_and_click(device, panels_device_settings_dict, "admin_login_btn")
        common.wait_for_and_click(device, panels_device_settings_dict, "display_setting")
        common.wait_for_element(device, panels_device_settings_dict, "power_saving_txt")
        common.wait_for_element(device, panels_device_settings_dict, "auto_brightness")
    if config["devices"][device]["model"].lower() == "savannah":
        common.wait_for_and_click(device, panels_device_settings_dict, "admin_pswd_field")
        common.wait_for_element(device, panels_device_settings_dict, "admin_pswd_field").set_value(
            config["devices"][device]["admin_password"]
        )
        common.wait_for_and_click(device, panels_device_settings_dict, "admin_login_continue_btn")
        device_settings_keywords.swipe_till_sign_out(device)
        common.wait_for_and_click(device, panels_device_settings_dict, "display_setting")
        common.wait_for_element(device, panels_device_settings_dict, "adaptive_brightness_txt")
    if config["devices"][device]["model"].lower() == "arlington":
        common.wait_for_and_click(device, tr_device_settings_dict, "admin_settings", "xpath1")
        common.wait_for_element(device, device_settings_dict, "edit_text_number_pin").set_value(
            config["devices"][device]["admin_password"]
        )
        common.wait_for_and_click(device, device_settings_dict, "submit_button")
        common.wait_for_and_click(device, panels_device_settings_dict, "screen_lights_txt")
        common.wait_for_and_click(device, panels_device_settings_dict, "display_setting")
        common.wait_for_and_click(device, panels_device_settings_dict, "back_to_settings")
        common.wait_for_and_click(device, panels_device_settings_dict, "close_button1", "id")
    if config["devices"][device]["model"].lower() == "surprise":
        common.wait_for_and_click(device, settings_dict, "Device_administration")
        if common.is_element_present(device, panels_device_settings_dict, "login_btn"):
            common.wait_for_and_click(device, panels_device_settings_dict, "login_btn")
            common.hide_keyboard(device)
            common.wait_for_element(device, settings_dict, "admin_pass", "id").set_value(
                config["devices"][device]["admin_password"]
            )
            common.wait_for_and_click(device, calendar_dict, "ok_button")
        common.wait_for_and_click(device, panels_device_settings_dict, "display_setting")
        common.wait_for_element(device, panels_device_settings_dict, "auto_brightness")


def verify_accessibility_settings_option_in_panel(device):
    settings_keywords.click_device_settings(device)
    if config["devices"][device]["model"].lower() == "surprise":
        # tr_settings_keywords.swipe_screen_page(device)
        common.click_if_present(device, app_bar_dict, "back")
    if config["devices"][device]["model"].lower() == "savannah":
        common.wait_for_and_click(device, panels_device_settings_dict, "admin_pswd_field")
        common.wait_for_element(device, panels_device_settings_dict, "admin_pswd_field").set_value(
            config["devices"][device]["admin_password"]
        )
        common.wait_for_and_click(device, panels_device_settings_dict, "admin_login_continue_btn")
    common.wait_for_element(device, settings_dict, "About")
    common.wait_for_and_click(device, settings_dict, "accessibility")
    common.wait_for_element(device, panels_device_settings_dict, "large_text")
    common.wait_for_element(device, panels_device_settings_dict, "high_contrast_text")
    if config["devices"][device]["model"].lower() not in ["savannah", "arlington"]:
        common.wait_for_element(device, panels_device_settings_dict, "color_correction_mode")
        common.wait_for_element(device, panels_device_settings_dict, "talkback_text")


def verify_device_info_in_about_for_panel(device):
    settings_keywords.click_device_settings(device)
    if config["devices"][device]["model"].lower() == "savannah":
        common.wait_for_and_click(device, panels_device_settings_dict, "admin_pswd_field")
        common.wait_for_element(device, panels_device_settings_dict, "admin_pswd_field").set_value(
            config["devices"][device]["admin_password"]
        )
        common.wait_for_and_click(device, panels_device_settings_dict, "admin_login_continue_btn")
    common.wait_for_and_click(device, settings_dict, "About")
    common.wait_for_element(device, panels_device_settings_dict, "model_name")
    if config["devices"][device]["model"].lower() == "surprise":
        common.wait_for_and_click(device, panels_device_settings_dict, "status_option")
    common.wait_for_element(device, panels_device_settings_dict, "serial_no")
    if config["devices"][device]["model"].lower() in ["beverly hills", "hollywood", "surprise"]:
        common.click_if_present(device, app_bar_dict, "back", "id")
    if config["devices"][device]["model"].lower() == "surprise":
        common.wait_for_and_click(device, panels_device_settings_dict, "version_info")
    common.wait_for_element(device, panels_device_settings_dict, "Firmware_version")
    if config["devices"][device]["model"].lower() == "hollywood":
        common.wait_for_and_click(device, panels_device_settings_dict, "UC_Provider")
    tr_settings_keywords.swipe_screen_page(device)
    tr_settings_keywords.swipe_screen_page(device)
    common.wait_for_element(device, settings_dict, "Company_Portal")
    common.wait_for_element(device, panels_device_settings_dict, "teams_version")
    tr_settings_keywords.swipe_screen_page(device)
    common.wait_for_element(device, panels_device_settings_dict, "partner_app_version")


def navigate_inside_admin_setting_in_panel(device, password_type="old"):
    if password_type == "new":
        password = config["devices"][device]["admin_new_password"]
    elif password_type == "old":
        password = config["devices"][device]["admin_password"]
    if config["devices"][device]["model"].lower() in ["beverly hills", "hollywood"]:
        common.wait_for_element(device, panels_device_settings_dict, "admin_pswd_field", "xpath").set_value(password)

        common.wait_for_and_click(device, panels_device_settings_dict, "admin_login_btn")
        return

    if config["devices"][device]["model"].lower() in ["westchester", "brooklyn"]:
        device_settings_keywords.swipe_till_sign_out(device)
        common.wait_for_and_click(device, tr_device_settings_dict, "teams_admin_settings1")
        common.wait_for_element(device, panels_device_settings_dict, "admin_pswd_field").set_value(password)
        common.hide_keyboard(device)
        common.wait_for_and_click(device, panels_device_settings_dict, "admin_login_btn")
        common.sleep_with_msg(device, 3, "Waiting for Admin settings page to load")
    if config["devices"][device]["model"].lower() == "arlington":
        common.wait_for_and_click(device, tr_device_settings_dict, "admin_settings", "xpath1")
        common.wait_for_element(device, device_settings_dict, "edit_text_number_pin").set_value(password)
        common.wait_for_and_click(device, device_settings_dict, "submit_button")
    if config["devices"][device]["model"].lower() == "flint":
        common.wait_for_and_click(device, device_settings_dict, "admin_settings", "id1")
        ele = common.wait_for_element(
            device, panels_device_settings_dict, "admin_pass_field", cond=EC.presence_of_all_elements_located
        )
        ele[-1].click()
        ele[-1].set_value(password)
        common.wait_for_and_click(device, calendar_dict, "ok_button")
    if config["devices"][device]["model"].lower() == "richland":
        common.wait_for_and_click(device, tr_device_settings_dict, "admin_settings", "xpath")
        common.wait_for_element(device, device_settings_dict, "admin_username_box").set_value(
            config["devices"][device]["admin_username"]
        )
        common.wait_for_element(device, settings_dict, "admin_passwd", "id1").set_value(password)
        common.wait_for_and_click(device, calendar_dict, "ok_button")
    if config["devices"][device]["model"].lower() == "surprise":
        if common.is_element_present(device, device_settings_dict, "teams_admin_settings"):
            calendar_keywords.scroll_down_device_setting_tab(device)
            calendar_keywords.scroll_down_device_setting_tab(device)
        common.wait_for_and_click(device, settings_dict, "Device_administration")
        if common.is_element_present(device, panels_device_settings_dict, "login_btn"):
            common.wait_for_and_click(device, panels_device_settings_dict, "login_btn")
            common.wait_for_element(device, settings_dict, "admin_passwd", "xpath").set_value(password)
            common.wait_for_and_click(device, calendar_dict, "ok_button")


def verify_debug_option_in_panel(device):
    settings_keywords.click_device_settings(device)
    _model = config["devices"][device]["model"].lower()
    if _model == "richland":
        common.wait_for_and_click(device, tr_device_settings_dict, "admin_settings", "xpath")
        common.wait_for_element(device, device_settings_dict, "admin_username_box").set_value(
            config["devices"][device]["admin_username"]
        )
        common.wait_for_element(device, settings_dict, "admin_passwd", "id1").set_value(
            config["devices"][device]["admin_password"]
        )
        common.wait_for_and_click(device, calendar_dict, "ok_button")
        common.wait_for_and_click(device, settings_dict, "Debug")
        common.wait_for_element(device, panels_device_settings_dict, "reset_custom_config")
        common.wait_for_and_click(device, panels_device_settings_dict, "debug_Back_Button")
        common.wait_for_and_click(device, panels_device_settings_dict, "debug_Back_Button")
        common.wait_for_and_click(device, panels_device_settings_dict, "debug_Back_Button")
    if _model == "arlington":
        common.wait_for_and_click(device, settings_dict, "Debug")
        common.wait_for_element(device, panels_device_settings_dict, "Reboot_panel")
    if _model in ["westchester", "brooklyn"]:
        common.wait_for_and_click(device, panels_device_settings_dict, "admin_settings")
        common.wait_for_element(device, panels_device_settings_dict, "admin_pswd_field").set_value(
            config["devices"][device]["admin_password"]
        )
        common.hide_keyboard(device)
        common.wait_for_and_click(device, panels_device_settings_dict, "admin_login_btn")
        common.wait_for_and_click(device, settings_dict, "Debug")
        common.wait_for_element(device, panels_device_settings_dict, "reset_custom_config")
        common.wait_for_and_click(device, device_settings_dict, "admin_back_button")
        common.wait_for_and_click(device, device_settings_dict, "user_sign_out_yes")
    if _model == "savannah":
        common.wait_for_and_click(device, panels_device_settings_dict, "admin_pswd_field")
        common.wait_for_element(device, panels_device_settings_dict, "admin_pswd_field").set_value(
            config["devices"][device]["admin_password"]
        )
        common.wait_for_and_click(device, panels_device_settings_dict, "admin_login_continue_btn")
        common.wait_for_and_click(device, settings_dict, "Debug")
        common.wait_for_element(device, panels_device_settings_dict, "Reboot_panel")
        common.wait_for_and_click(device, panels_device_settings_dict, "debug_Back_Button")
    if _model in ["beverly hills", "hollywood"]:
        common.wait_for_and_click(device, panels_device_settings_dict, "Reboot_panel")
        common.wait_for_element(device, panels_device_settings_dict, "Reboot_panel")
    call_keywords.come_back_to_home_screen(device)


def verify_network_configuration_option_in_panel(device):
    _model = config["devices"][device]["model"].lower()

    if _model in ["beverly hills", "hollywood"]:
        common.wait_for_and_click(device, panels_device_settings_dict, "Network_info_txt")
        common.wait_for_element(device, panels_device_settings_dict, "MAC_txt")
        common.wait_for_element(device, panels_device_settings_dict, "Gateway_txt")
    elif _model in ["richland"]:
        common.wait_for_and_click(device, tr_device_settings_dict, "admin_settings", "xpath")
        common.wait_for_element(device, device_settings_dict, "admin_username_box").set_value(
            config["devices"][device]["admin_username"]
        )
        common.wait_for_element(device, settings_dict, "admin_passwd", "id1").set_value(
            config["devices"][device]["admin_password"]
        )
        common.wait_for_and_click(device, calendar_dict, "ok_button")
        common.wait_for_and_click(device, device_settings_dict, "system_settings")
        common.wait_for_and_click(device, panels_device_settings_dict, "network_btn")
        common.wait_for_element(device, panels_device_settings_dict, "Gateway_txt")

    elif _model == "arlington":
        navigate_inside_admin_setting_in_panel(device)
        common.wait_for_and_click(device, device_settings_dict, "connectivity_setting")

    elif _model == "savannah":
        device_settings_keywords.swipe_till_sign_out(device)
        common.wait_for_and_click(device, panels_device_settings_dict, "network_btn")
        common.wait_for_element(device, panels_device_settings_dict, "Gateway_txt")
        common.wait_for_element(device, panels_device_settings_dict, "MAC_txt")

    if _model in ["beverly hills", "hollywood", "savannah", "arlington"]:
        common.wait_for_element(device, panels_device_settings_dict, "ip_address_txt")
        tr_settings_keywords.swipe_screen_page(device)
        common.wait_for_element(device, panels_device_settings_dict, "DNS_1_txt")
        common.wait_for_element(device, panels_device_settings_dict, "DNS_2_txt")

    elif _model in ["westchester", "brooklyn"]:
        navigate_inside_admin_setting_in_panel(device)
        common.wait_for_and_click(device, panels_device_settings_dict, "network_btn")
        common.wait_for_element(device, panels_device_settings_dict, "DNS_1_txt")
        common.wait_for_element(device, panels_device_settings_dict, "DNS_2_txt")
        common.wait_for_element(device, panels_device_settings_dict, "ip_address_txt")

    else:
        raise AssertionError(f"{device}: Cannot handle model '{_model}'")


def verify_background_page_in_teams_admin_settings_in_panel(device, status):
    if status.lower() not in ["custom", "default"]:
        raise AssertionError(f"{device}: Unexpected value for status: {status}")
    if status.lower() == "default":
        common.wait_for_element(device, panels_device_settings_dict, "background_button")
        common.wait_for_element(device, panels_device_settings_dict, "choose_image_text")
        common.wait_for_element(device, panels_device_settings_dict, "background_info_text")
    else:
        common.wait_for_element(device, panels_device_settings_dict, "custom_bg_header")
        common.wait_for_element(device, panels_device_settings_dict, "custom_wallpaper_list")


def verify_background_wallpaper_selected(device, status):
    if status.lower() not in ["custom", "default"]:
        raise AssertionError(f"{device}: Unexpected value for status: {status}")
    if status.lower() == "custom":
        common.wait_for_element(device, panels_device_settings_dict, "custom_wallpaper_selected")
    else:
        common.wait_for_element(device, panels_device_settings_dict, "default_wallpaper_selected")
