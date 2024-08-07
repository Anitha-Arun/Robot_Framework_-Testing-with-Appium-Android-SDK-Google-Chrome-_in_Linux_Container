import call_keywords
import common
from Selectors import load_json_file
from initiate_driver import config
import time
import calendar_keywords
import settings_keywords

display_time = 2
action_time = 3
sleep_time = 5

call_view_dict = load_json_file("resources/Page_objects/Call_views.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")
calls_dict = load_json_file("resources/Page_objects/Calls.json")
navigation_dict = load_json_file("resources/Page_objects/Navigation.json")
home_screen_dict = load_json_file("resources/Page_objects/Home_screen.json")


def verify_call_views_option_under_callings_settings(device, verify_options_under_default_view="off"):
    if verify_options_under_default_view.lower() not in ["on", "off"]:
        raise AssertionError(f"Unexpected value for option: {verify_options_under_default_view}")
    settings_keywords.open_settings_page(device)
    common.wait_for_and_click(device, settings_dict, "Calling")
    common.wait_for_element(device, calls_dict, "Header", "id")
    for i in range(5):
        time.sleep(2)
        if common.is_element_present(device, call_view_dict, "default_view"):
            break
        calendar_keywords.scroll_only_once(device)
    common.wait_for_element(device, call_view_dict, "call_view")
    if verify_options_under_default_view == "off":
        common.wait_for_element(device, call_view_dict, "default_view")
    else:
        common.wait_for_and_click(device, call_view_dict, "default_view")
        common.wait_for_element(device, call_view_dict, "speed_dial")
        common.wait_for_element(device, call_view_dict, "recent_call_history")
        if common.is_portrait_mode_cnf_device(device):
            common.wait_for_element(device, call_view_dict, "dialpad")
        if common.is_screen_size_7_inch_or_more(device):
            common.wait_for_element(device, call_view_dict, "expanded_dialpad")
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")


def select_default_view(device, option):
    if option.lower() not in ["speed dial", "recent call history", "dialpad", "expanded_dialpad"]:
        raise AssertionError(f"Unexpected value for option: {option}")
    common.wait_for_and_click(device, settings_dict, "Calling")
    time.sleep(5)
    for i in range(5):
        time.sleep(2)
        if common.is_element_present(device, call_view_dict, "default_view"):
            break
        calendar_keywords.scroll_only_once(device)

    common.wait_for_and_click(device, call_view_dict, "default_view")
    if option.lower() == "speed dial":
        common.wait_for_and_click(device, call_view_dict, "speed_dial")
    elif option.lower() == "recent call history":
        common.wait_for_and_click(device, call_view_dict, "recent_call_history")
    elif option.lower() == "dialpad":
        if config["devices"][device]["model"].lower() in [
            "san diego",
            "san jose",
            "santa cruz",
            "bakersfield",
            "redmond",
            "long island",
            "queens",
            "santa cruz_13",
            "bakersfield_13",
        ]:
            print(f"{device} doesn't support dialpad")
            for i in range(3):
                common.wait_for_and_click(device, calls_dict, "Call_Back_Button")
            common.wait_for_element(device, navigation_dict, "Navigation")
            return
        common.wait_for_and_click(device, call_view_dict, "dialpad")
    elif option.lower() == "expanded_dialpad":
        common.wait_for_and_click(device, call_view_dict, "expanded_dialpad")
    time.sleep(sleep_time)
    if common.click_if_present(device, call_view_dict, "relaunch"):
        common.sleep_with_msg(device, 5, "Wait for app relaunch")
    else:
        print(f"{device} default view: {option} is already selected")
        for i in range(3):
            common.wait_for_and_click(device, calls_dict, "Call_Back_Button")
    common.wait_for_element(device, navigation_dict, "Navigation")


def cancel_selected_default_view(device, option):
    if option.lower() not in ["speed dial", "recent call history", "dialpad", "expanded_dialpad"]:
        raise AssertionError(f"Unexpected value for option: {option}")
    common.wait_for_and_click(device, settings_dict, "Calling")
    time.sleep(action_time)
    settings_keywords.swipe_till_end(device)
    time.sleep(action_time)
    common.wait_for_and_click(device, call_view_dict, "default_view")
    if option.lower() == "speed dial":
        common.wait_for_and_click(device, call_view_dict, "speed_dial")
        time.sleep(display_time)
        common.click_if_present(device, call_view_dict, "cancel")
        elem = common.wait_for_element(device, call_view_dict, "speed_dial")
        temp = elem.get_attribute("checked")
        if temp == "false":
            raise AssertionError(f"Unable to cancel selected default view :{option} ")
    elif option.lower() == "recent call history":
        common.wait_for_and_click(device, call_view_dict, "recent_call_history")
        time.sleep(display_time)
        common.click_if_present(device, call_view_dict, "cancel")
        elem = common.wait_for_element(device, call_view_dict, "recent_call_history")
        temp = elem.get_attribute("checked")
        if temp == "false":
            raise AssertionError(f"Unable to cancel selected default view :{option} ")
    elif option.lower() == "dialpad":
        common.wait_for_and_click(device, call_view_dict, "dialpad_option")
        time.sleep(display_time)
        common.click_if_present(device, call_view_dict, "cancel")
        elem = common.wait_for_element(device, call_view_dict, "dialpad_option")
        temp = elem.get_attribute("checked")
        if temp == "false":
            raise AssertionError(f"Unable to cancel selected default view :{option} ")
    elif option.lower() == "expanded_dialpad":
        common.wait_for_and_click(device, call_view_dict, "expanded_dialpad")
        common.click_if_present(device, call_view_dict, "cancel")
        elem = common.wait_for_element(device, call_view_dict, "expanded_dialpad")
        temp = elem.get_attribute("checked")
        if temp == "false":
            raise AssertionError(f"Unable to cancel selected default view :{option} ")


def validate_calls_tab_after_default_value_change(device, default_option):
    if default_option.lower() not in ["speed dial", "recent call history", "dialpad", "expanded_dialpad"]:
        raise AssertionError(f"Unexpected value for option: {default_option}")
    call_keywords.click_on_calls_tab(device)
    print("default_option : ", default_option)
    if default_option.lower() == "speed dial":
        common.wait_for_element(device, call_view_dict, "recent_tab")
        common.wait_for_element(device, call_view_dict, "favorites_tab")
        settings_keywords.open_settings_page(device)
        common.wait_for_and_click(device, settings_dict, "Calling")
        common.wait_for_element(device, calls_dict, "Header", "id")
        for i in range(5):
            if common.is_element_present(device, call_view_dict, "default_view"):
                break
            calendar_keywords.scroll_only_once(device)
        common.wait_for_and_click(device, call_view_dict, "default_view")
        elem = common.wait_for_element(device, call_view_dict, "speed_dial")
        temp = elem.get_attribute("checked")
        if temp == "false":
            raise AssertionError(f"{default_option}: is not Selected")

    elif default_option.lower() == "recent call history":
        common.wait_for_element(device, call_view_dict, "recent_tab")
        common.wait_for_element(device, call_view_dict, "favorites_tab")
        settings_keywords.open_settings_page(device)
        common.wait_for_and_click(device, settings_dict, "Calling")
        common.wait_for_element(device, calls_dict, "Header", "id")
        for i in range(5):
            if common.is_element_present(device, call_view_dict, "default_view"):
                break
            calendar_keywords.scroll_only_once(device)
        common.wait_for_and_click(device, call_view_dict, "default_view")
        elem = common.wait_for_element(device, call_view_dict, "recent_call_history")
        temp = elem.get_attribute("checked")
        if temp == "false":
            raise AssertionError(f"{default_option}: is not Selected")

    elif default_option.lower() == "dialpad":
        common.wait_for_element(device, call_view_dict, "dialpad_option")
        common.wait_for_element(device, call_view_dict, "people_option")
        settings_keywords.open_settings_page(device)
        common.wait_for_and_click(device, settings_dict, "Calling")
        common.wait_for_element(device, calls_dict, "Header", "id")
        for i in range(5):
            if common.is_element_present(device, call_view_dict, "default_view"):
                break
            calendar_keywords.scroll_only_once(device)
        common.wait_for_and_click(device, call_view_dict, "default_view")
        elem = common.wait_for_element(device, call_view_dict, "dialpad")
        temp = elem.get_attribute("checked")
        if temp == "false":
            raise AssertionError(f"{default_option}: is not Selected")

    elif default_option.lower() == "expanded_dialpad":
        common.wait_for_element(device, calls_dict, "entered_phn_num")
        common.wait_for_element(device, calls_dict, "backspace")
        settings_keywords.open_settings_page(device)
        common.wait_for_and_click(device, settings_dict, "Calling")
        common.wait_for_element(device, calls_dict, "Header", "id")
        for i in range(5):
            if common.is_element_present(device, call_view_dict, "default_view"):
                break
            calendar_keywords.scroll_only_once(device)
        common.wait_for_and_click(device, call_view_dict, "default_view")
        elem = common.wait_for_element(device, call_view_dict, "expanded_dialpad")
        temp = elem.get_attribute("checked")
        if temp == "false":
            raise AssertionError(f"{default_option}: is not Selected")


def Navigate_recent_tab(device):
    common.wait_for_and_click(device, call_view_dict, "call_plus_icon")
    common.wait_for_and_click(device, call_view_dict, "favorites_option")
    common.wait_for_and_click(device, call_view_dict, "recent_tab")


def verify_callplus_icon_on_favorites_tab(device):
    common.wait_for_and_click(device, call_view_dict, "favorites_option")
    if common.is_portrait_mode_cnf_device(device):
        common.wait_for_element(device, calls_dict, "Make_a_call")
    else:
        # Landscape mode device doesn't have "plus" icon on calls tab
        common.wait_for_element(device, calls_dict, "call")


def verify_default_view_screen(device):
    common.wait_for_element(device, calls_dict, "default_call_screen_view")
    common.wait_for_element(device, call_view_dict, "recent_call_history")


def verify_default_call_screen_view_selected_option(device, option):
    if option.lower() not in ["speed dial", "recent call history", "dialpad"]:
        raise AssertionError(f"Unexpected value for option: {option}")
    common.wait_for_element(device, settings_dict, "Calling")
    for i in range(5):
        time.sleep(2)
        if common.is_element_present(device, call_view_dict, "default_view"):
            break
        calendar_keywords.scroll_only_once(device)
    common.wait_for_and_click(device, calls_dict, "default_view")
    common.wait_for_element(device, calls_dict, "default_call_screen_view")
    if option.lower() == "speed dial":
        elem = common.wait_for_element(device, call_view_dict, "speed_dial")
    elif option.lower() == "recent call history":
        elem = common.wait_for_element(device, call_view_dict, "recent_call_history")
    elif option.lower() == "dialpad":
        elem = common.wait_for_element(device, call_view_dict, "dialpad_option")
    temp = elem.get_attribute("checked")
    if temp == "false":
        raise AssertionError(f"{option} : radio button is not selected")


def verify_and_add_favorite_contacts_under_speed_dial_group(from_device, to_device):
    call_keywords.navigate_to_calls_favorites_page(from_device)
    time.sleep(display_time)
    if not common.is_element_present(from_device, calls_dict, "speed_dial"):
        call_keywords.select_call_list_item(from_device, item="favorite")
        call_keywords.verify_added_favorite_user_in_favorites_page(from_device, to_device)


def go_back_to_previous_page(device):
    for i in range(3):
        common.click_if_present(device, calls_dict, "Call_Back_Button")
        time.sleep(2)


def navigates_to_recent_tab_while_default_view_as_dailpad(device):
    time.sleep(display_time)
    if not common.is_element_present(device, calls_dict, "use_hard_keys_to_dial_a_number"):
        common.wait_for_element(device, call_view_dict, "dialpad_option")
    common.wait_for_and_click(device, call_view_dict, "call_history_button_in_dailpad_view")
    common.wait_for_element(device, calls_dict, "favorites_tab")
    common.wait_for_and_click(device, calls_dict, "recent_tab")


def verify_profile_form_search_results(from_device, to_device):
    displayname = common.device_displayname(to_device)
    user_email = config["devices"][to_device]["user"]["username"]
    common.wait_for_and_click(from_device, calls_dict, "search")
    common.wait_for_element(from_device, calls_dict, "search_text").clear()
    common.wait_for_element(from_device, calls_dict, "search_text").send_keys(displayname)
    common.hide_keyboard(from_device)
    tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", displayname)
    common.wait_for_and_click(from_device, tmp_dict, "search_result_item_container", "xpath")
    common.wait_for_element(from_device, calls_dict, "user_display_name", "xpath")
    mail_id = common.wait_for_element(from_device, calls_dict, "mail_id").text
    if mail_id != user_email:
        raise AssertionError(f"{from_device}: Expected email ID: '{user_email}', but  found: '{mail_id}'")
    common.wait_for_element(from_device, calls_dict, "Make_an_audio_call")


def go_to_call_views_options_screen(device):
    common.wait_for_and_click(device, call_view_dict, "default_view")
    common.wait_for_element(device, call_view_dict, "speed_dial")
    common.wait_for_element(device, call_view_dict, "recent_call_history")


def verify_fab_icon_not_present_in_people_tab_when_calls_views_set_to_dial_pad(device):
    call_keywords.click_on_calls_tab(device)
    common.wait_for_and_click(device, calls_dict, "people_tab")
    if common.is_element_present(device, call_view_dict, "call_history_button_in_dailpad_view"):
        raise AssertionError(f"{device} : fab icon is present in people tab")


def navigate_to_dial_pad_tab_from_home_screen_when_call_views_set_to_speed_dial(device):
    call_keywords.click_on_calls_tab(device)
    common.wait_for_and_click(device, calls_dict, "Make_a_call")
    common.wait_for_element(device, calls_dict, "dialpad_tab")
