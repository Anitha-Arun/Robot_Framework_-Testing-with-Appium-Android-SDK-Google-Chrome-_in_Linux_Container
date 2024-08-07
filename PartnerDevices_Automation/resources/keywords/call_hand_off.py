import time
from initiate_driver import obj_dev as obj
import json
import common
import call_keywords

display_time = 2
action_time = 3

calls_dict = json.loads(open("resources/Page_objects/Calls.json").read())
call_hand_off_dict = json.loads(open("resources/Page_objects/Call_hand_off.json").read())


def verify_call_hand_off_banner(device):
    text1_expected = "You're in a call on another device. Want to join on this one?"
    text2_expected = "Join on this device"
    expected_banner_text_list = [text1_expected, text2_expected]
    text_displayed = common.wait_for_element(device, call_hand_off_dict, "join_companion_description").text
    print(f"Call handoff text displayed on device : {text_displayed}")
    if text_displayed.strip() not in expected_banner_text_list:
        raise AssertionError("Banner text has unexpected content")


def tap_on_join_button_from_banner(device):
    print("device :", device)
    common.wait_for_and_click(device, call_hand_off_dict, "meeting_join_button")


def validate_both_options_for_joining_meeting(device):
    print("device :", device)
    common.wait_for_element(device, call_hand_off_dict, "add_this_device")
    print("add_this_device option visible")
    common.wait_for_element(device, call_hand_off_dict, "transfer_to_this_device")
    print("Transfer_to_this_device option visible")


def select_option_to_join_meeting(device, option):
    if option.lower() not in ["add this device", "transfer to this device"]:
        raise AssertionError(f"{device}: Unexpected value for 'option': {option}")
    if option.lower() == "add this device":
        common.wait_for_and_click(device, call_hand_off_dict, "add_this_device")
    elif option.lower() == "transfer to this device":
        common.wait_for_and_click(device, call_hand_off_dict, "transfer_to_this_device")
        common.click_if_present(device, call_hand_off_dict, "transfer_btn")


def verify_your_call_was_transferred_text(device):
    common.wait_for_element(device, call_hand_off_dict, "Your_call_was_transferred")


def close_options_screen(device):
    if common.is_element_present(device, calls_dict, "calls_item_options_container"):
        dismiss_call_hand_off_options(device)
        return
    for i in range(8):
        time.sleep(1)
        if common.click_if_present(device, call_hand_off_dict, "close_button"):
            common.sleep_with_msg(device, 3, "React to close button click")
            break
    if common.is_element_present(device, call_hand_off_dict, "close_button"):
        raise AssertionError(f"{device}: Unable to close the options screen")


def dismiss_call_hand_off_options(device_name):
    driver = obj.device_store.get(alias=device_name)
    # Verify the options are open:
    container_element = common.wait_for_element(device_name, calls_dict, "calls_item_options_container")

    # Get co-ordinates to tap outside the menu tray
    x_tap_loc, y_tap_loc = call_keywords.get_co_ords_to_tap(container_element)

    driver.tap([(x_tap_loc, y_tap_loc)])
    print(f"{device_name}: Tapped the co-ordinates: ({x_tap_loc}, {y_tap_loc})")

    # Verify the options are dismissed:
    common.wait_while_present(device_name, calls_dict, "calls_item_options_container")


def verify_call_hand_off_banner_after_closing(device):
    time.sleep(7)
    if common.is_element_present(device, call_hand_off_dict, "join_companion_description"):
        raise AssertionError(f"Banner appears on {device} even after closing it")


def verify_call_hand_off_banner_for_meetings(device):
    text1_expected = "Join to share content or to continue the meeting on the device"
    text2_expected = "Join on this device"
    expected_banner_text_list = [text1_expected, text2_expected]
    text_displayed = common.wait_for_element(device, call_hand_off_dict, "join_companion_description").text
    print(f"Call handoff text displayed on device : {text_displayed}")
    if text_displayed.strip() not in expected_banner_text_list:
        raise AssertionError("Banner text has unexpected content")


def close_call_hand_off_banner(device):
    common.wait_for_and_click(device, call_hand_off_dict, "close_button")


def verify_call_hand_off_banner_should_not_visible_in_device_settings_page(device):
    if common.is_element_present(device, call_hand_off_dict, "join_companion_description"):
        raise AssertionError("Banner is present in device settings page")
    print("Banner is not visible in device settings page")


def verify_call_hand_off_banner_along_with_call_park_banner(device):
    verify_call_hand_off_banner(device)
    caller_name = common.wait_for_element(device, calls_dict, "caller_name_in_hold_banner").text
    print(f"Caller name in call park banner is : {caller_name}")
    common.wait_for_element(device, calls_dict, "call_unpark_code_from_banner")
    common.wait_for_element(device, calls_dict, "close_button_in_call_park_banner")
