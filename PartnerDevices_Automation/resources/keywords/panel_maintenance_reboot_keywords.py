import common
from Selectors import load_json_file

panels_device_settings_dict = load_json_file("resources/Page_objects/panels_device_settings.json")


def navigate_and_verify_device_restrat_page_in_teams_admin_settings_in_panel(device):
    common.wait_for_and_click(device, panels_device_settings_dict, "device_restart_option")
    common.wait_for_element(device, panels_device_settings_dict, "maintenance_mode_header")
    common.wait_for_element(device, panels_device_settings_dict, "maintenance_details_txt")
    common.wait_for_element(device, panels_device_settings_dict, "start_reboot_txt")
    common.wait_for_element(device, panels_device_settings_dict, "end_reboot_txt")
    common.wait_for_element(device, panels_device_settings_dict, "maintenance_toggle_button")


def verify_maintenance_toggle_button_is_on_by_default(device):
    common.verify_toggle_button(device, panels_device_settings_dict, "maintenance_toggle_button", "on")


def enable_or_disable_and_verify_maintenance_toggle_button_in_panel(device, state):
    common.change_toggle_button(device, panels_device_settings_dict, "maintenance_toggle_button", state)
    desired_state = "true" if state.lower() == "on" else "false"
    common.check_clickable_state(device, panels_device_settings_dict, "start_reboot_time", desired_state)
    common.check_clickable_state(device, panels_device_settings_dict, "end_reboot_time", desired_state)
