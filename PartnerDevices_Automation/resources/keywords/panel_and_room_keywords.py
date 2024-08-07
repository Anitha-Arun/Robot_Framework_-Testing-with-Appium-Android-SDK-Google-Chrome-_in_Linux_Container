import common
from Selectors import load_json_file
import panel_meetings_device_settings_keywords

panels_device_settings_dict = load_json_file("resources/Page_objects/panels_device_settings.json")
tr_console_signin_dict = load_json_file("resources/Page_objects/rooms_console_signin.json")


def navigate_to_device_pairing_tab_on_panel(device, pair_status):
    if pair_status.lower() not in ["paired", "unpaired"]:
        raise AssertionError(f"{device}: Unexpected value for pair_status: {pair_status}")
    navigate_to_device_pairing_page_on_panel(device)
    if pair_status.lower() == "paired":
        common.wait_for_element(device, panels_device_settings_dict, "reset_pairing")
    if pair_status.lower() == "unpaired":
        common.wait_for_element(device, panels_device_settings_dict, "panel_user_name")


def verify_device_is_paired(device):
    common.wait_for_element(device, panels_device_settings_dict, "reset_pairing")


def reset_device_pairing_in_panel(device):
    common.wait_for_and_click(device, panels_device_settings_dict, "device_pairing_in_panel")
    common.wait_for_and_click(device, panels_device_settings_dict, "reset_pairing")
    panel_meetings_device_settings_keywords.go_to_meetings_tab_in_panel(device)
    common.wait_for_and_click(device, panels_device_settings_dict, "device_pairing_in_panel")
    common.wait_for_element(device, panels_device_settings_dict, "panel_user_name")


def pass_incorrect_pairing_code_to_panel(device):
    code_field_on_panel = common.wait_for_element(device, tr_console_signin_dict, "room_code")
    code_field_on_panel.click()
    code_field_on_panel.send_keys("123456")
    print(f"{device}: Entered the pair code displayed on rooms device")
    common.hide_keyboard(device)
    common.wait_for_and_click(device, tr_console_signin_dict, "pair_button")
    common.wait_for_element(device, panels_device_settings_dict, "incorrect_code_error")


def navigate_to_device_pairing_page_on_panel(device):
    panel_meetings_device_settings_keywords.go_to_meetings_tab_in_panel(device)
    common.wait_for_and_click(device, panels_device_settings_dict, "device_pairing_in_panel")


def is_device_paired_to_panel(device):
    print("device :", device)
    if not common.is_element_present(device, panels_device_settings_dict, "reset_pairing"):
        status = "fail"
    else:
        status = "pass"
    return status
