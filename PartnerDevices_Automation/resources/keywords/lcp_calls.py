import common
from Selectors import load_json_file
import settings_keywords
import call_keywords

lcp_calls_dict = load_json_file("resources/Page_objects/lcp_calls.json")
calls_dict = load_json_file("resources/Page_objects/Calls.json")
common_dict = load_json_file("resources/Page_objects/Common.json")
lcp_homescreen_dict = load_json_file("resources/Page_objects/lcp_homescreen.json")


def swap_calls(device):
    common.wait_for_and_click(device, lcp_calls_dict, "lcp_call_bar_entry_more_option")
    common.wait_for_and_click(device, lcp_calls_dict, "call_swap")


def make_emergency_call_lcp(device):
    emergency_phone_no = "933"
    common.wait_for_and_click(device, calls_dict, "search_icon")
    contact = common.wait_for_element(device, calls_dict, "search_text")
    contact.send_keys(emergency_phone_no)
    tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", emergency_phone_no)
    common.wait_for_and_click(device, tmp_dict, "search_result_item_container", "xpath")
    # settings_keywords.swipe_till_end(device)
    # settings_keywords.swipe_till_end(device)
    # tmp_dict1 = common.get_dict_copy(
    #     lcp_calls_dict, "lcp_call_using_phone_no", "replace_with_phone_no", emergency_phone_no
    # )
    # common.wait_for_and_click(device, tmp_dict1, "lcp_call_using_phone_no")
    common.wait_for_element(device, calls_dict, "Hang_up_button")


def verify_options_inside_calls_tab(device):
    call_keywords.navigate_to_calls_tab(device)
    common.wait_for_element(device, calls_dict, "recent_tab")
    common.wait_for_element(device, calls_dict, "favorites_tab")
    common.wait_for_and_click(device, common_dict, "home_btn")


def verify_calls_tab_when_signed_in_with_cap_account(device):
    common.wait_for_and_click(device, lcp_homescreen_dict, "calls_tab")
    common.wait_for_element(device, lcp_calls_dict, "lcp_dial_tab")


def verify_transfer_target_search_screen_for_lcp(device, to_device, speed_dial_user, option):
    if option.lower() not in ["transfer_now", "consult_first"]:
        raise AssertionError(f"{device}: Unexpected value for Transfer option: {option}")
    common.wait_for_element(device, calls_dict, "Hang_up_button")
    common.wait_for_and_click(device, calls_dict, "Transfer")
    if option.lower() == "transfer_now":
        common.wait_for_and_click(device, calls_dict, "Transfer_now")
        common.wait_for_element(device, lcp_calls_dict, "transfer_title")
    elif option.lower() == "consult_first":
        common.wait_for_and_click(device, calls_dict, "consult_first")
        common.wait_for_element(device, lcp_calls_dict, "consult")
    common.wait_for_element(device, calls_dict, "Call_Back_Button")
    common.wait_for_element(device, lcp_calls_dict, "dialpad_button")
    common.wait_for_element(device, lcp_calls_dict, "search_button")
    common.wait_for_element(device, calls_dict, "call_action_bar")
    common.wait_for_and_click(device, lcp_calls_dict, "search_button")
    common.wait_for_element(device, calls_dict, "search_contact_box")
    common.wait_for_element(device, lcp_calls_dict, "people_or_phone")
    actual_speed_dial_user = common.get_all_elements_texts(device, calls_dict, "contact_display_name")
    expected_speed_dial_user = common.device_displayname(speed_dial_user)
    if expected_speed_dial_user not in actual_speed_dial_user:
        raise AssertionError(
            f"{actual_speed_dial_user} user in the speed dial is not as expected {expected_speed_dial_user}"
        )
    user_name = common.device_displayname(to_device)
    common.wait_for_element(device, calls_dict, "search_contact_box").send_keys(user_name)
    tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", user_name)
    common.wait_for_element(device, tmp_dict, "search_result_item_container", "xpath")
