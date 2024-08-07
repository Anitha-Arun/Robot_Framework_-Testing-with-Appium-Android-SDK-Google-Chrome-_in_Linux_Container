from initiate_driver import config
from Libraries.Selectors import load_json_file
import time
import common

display_time = 5
action_time = 5

calls_dict = load_json_file("resources/Page_objects/Calls.json")
calendar_dict = load_json_file("resources/Page_objects/Calendar.json")
navigation_dict = load_json_file("resources/Page_objects/Navigation.json")


def search_text(from_device, to_device):
    user = config["devices"][to_device]["user"]["displayname"]
    if common.is_lcp(from_device):
        common.wait_for_and_click(from_device, calls_dict, "search_icon")
    else:
        common.wait_for_and_click(from_device, calls_dict, "search")
    common.wait_for_element(from_device, calls_dict, "search_text").clear()
    common.wait_for_element(from_device, calls_dict, "search_text").send_keys(user)
    common.hide_keyboard(from_device)


def validate_search_results_presented(device):
    common.wait_for_element(device, calls_dict, "directory_contacts_text")
    common.get_all_elements_texts(device, calls_dict, "search_result_name")
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")


def clear_search_history_and_validate(device):
    common.wait_for_and_click(device, calls_dict, "search")
    common.wait_for_and_click(device, navigation_dict, "Clear_Text")
    time.sleep(display_time)
    if common.is_element_present(device, navigation_dict, "Clear_Text"):
        raise AssertionError("Unable to clear search history")
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")


def get_search_text_validate(from_device, to_device, verify_make_a_call_people_tab="off"):
    if verify_make_a_call_people_tab.lower() not in ["on", "off"]:
        raise AssertionError(f"{from_device}: Unexpected value for option: {verify_make_a_call_people_tab}")
    user = common.device_displayname(to_device)
    if verify_make_a_call_people_tab == "off":
        common.wait_for_and_click(from_device, calls_dict, "search")
        common.wait_for_element(from_device, calls_dict, "search_text").clear()
        common.wait_for_element(from_device, calls_dict, "search_text").send_keys(user)
    elif verify_make_a_call_people_tab == "on":
        common.wait_for_and_click(from_device, calls_dict, "search_contact_box")
        common.wait_for_element(from_device, calls_dict, "search_contact_box").clear()
        common.wait_for_element(from_device, calls_dict, "search_contact_box").send_keys(user)
    common.hide_keyboard(from_device)
    get_search_text = common.get_all_elements_texts(from_device, calls_dict, "search_result_name")
    if user not in get_search_text:
        raise AssertionError(f"Expected {user}, found {get_search_text}")
    common.wait_for_and_click(from_device, calls_dict, "Call_Back_Button")


def verify_search_text(from_device, to_device, verify_make_a_call_people_tab="off"):
    if verify_make_a_call_people_tab.lower() not in ["on", "off"]:
        raise AssertionError(f"{from_device}: Unexpected value for option: {verify_make_a_call_people_tab}")
    user = common.device_displayname(to_device)
    if verify_make_a_call_people_tab == "off":
        if common.is_lcp(from_device):
            common.wait_for_and_click(from_device, calls_dict, "search_icon")
        else:
            common.wait_for_and_click(from_device, calls_dict, "search")
        common.wait_for_element(from_device, calls_dict, "search_text").clear()
        common.wait_for_element(from_device, calls_dict, "search_text").send_keys(user)
        common.hide_keyboard(from_device)
        tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", user)
        common.wait_for_and_click(from_device, tmp_dict, "search_result_item_container", "xpath")
    else:
        common.wait_for_and_click(from_device, calls_dict, "search_contact_box")
        common.wait_for_element(from_device, calls_dict, "search_contact_box").clear()
        common.wait_for_element(from_device, calls_dict, "search_contact_box").send_keys(user)
        common.hide_keyboard(from_device)
        tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", user)
        common.wait_for_and_click(from_device, tmp_dict, "search_result_item_container", "xpath")
        elem = common.wait_for_element(from_device, calls_dict, "call_icon", "id1")
        temp = elem.get_attribute("enabled")
        if temp != "true":
            raise AssertionError(f"{from_device}: Call icon is not enable: {temp}")
    common.wait_for_and_click(from_device, calls_dict, "Call_Back_Button")


def verify_recent_search_item(from_device, to_device):
    username = config["devices"][to_device]["user"]["displayname"]
    if common.is_lcp(from_device):
        common.wait_for_and_click(from_device, calls_dict, "search_icon")
    else:
        common.wait_for_and_click(from_device, calls_dict, "search")
    common.wait_for_and_click(from_device, calls_dict, "search_text")
    common.hide_keyboard(from_device)
    common.wait_for_element(from_device, calls_dict, "recent_search_text")
    recent_search_list = common.get_all_elements_texts(from_device, calls_dict, "Recent_Searches")
    if not username in recent_search_list:
        raise AssertionError(f"{from_device}: Failed to find '{username}' in search results: {recent_search_list}")
    common.wait_for_and_click(from_device, calls_dict, "Call_Back_Button")


def verify_recent_search_empty(device):
    if common.is_lcp(device):
        common.wait_for_and_click(device, calls_dict, "search_icon")
    else:
        common.wait_for_and_click(device, calls_dict, "search")
    search_text = common.wait_for_element(device, calls_dict, "search_text").text
    if "Search" not in search_text:
        raise AssertionError(f"{device}: search text was not cleared, found '{search_text}'")
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")


def verify_and_search_for_unknown_user(device):
    unknown_user = "user A"
    common.wait_for_and_click(device, calls_dict, "search")
    common.wait_for_element(device, calls_dict, "search_text").clear()
    common.wait_for_element(device, calls_dict, "search_text").send_keys(unknown_user)
    common.hide_keyboard(device)
    common.wait_for_element(device, calls_dict, "no_user_found_error")
    common.wait_for_and_click(device, calls_dict, "search_close_btn")
    common.click_if_element_appears(device, navigation_dict, "Clear_Text")
    time.sleep(display_time)
    if common.is_element_present(device, navigation_dict, "Clear_Text"):
        raise AssertionError("Unable to clear search history")
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")
