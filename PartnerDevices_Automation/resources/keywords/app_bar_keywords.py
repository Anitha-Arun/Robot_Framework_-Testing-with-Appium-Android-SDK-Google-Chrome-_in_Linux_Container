import time
from appium.webdriver.common.mobileby import MobileBy
from Libraries.Selectors import load_json_file
from initiate_driver import obj_dev as obj
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import voicemail_keywords
import calendar_keywords
import common

display_time = 3
action_time = 3

app_bar_dict = load_json_file("resources/Page_objects/App_bar.json")
calls_dict = load_json_file("resources/Page_objects/Calls.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")
common_dict = load_json_file("resources/Page_objects/Common.json")
call_view_dict = load_json_file("resources/Page_objects/Call_views.json")
calendar_dict = load_json_file("resources/Page_objects/Calendar.json")
people_dict = load_json_file("resources/Page_objects/People.json")
navigation_dict = load_json_file("resources/Page_objects/Navigation.json")
walkie_talkie_dict = load_json_file("resources/Page_objects/walkie_talkie.json")


def click_hide_more_apps(device):
    print("device :", device)
    common.wait_for_and_click(device, app_bar_dict, "hide_more_app_icon", selector_key="xpath")


def verify_available_app_present_on_screen(device):
    devices = device.split(",")
    # time.sleep(display_time)
    for device in devices:
        print("device :", device)
        driver = obj.device_store.get(alias=device)
        try:
            ele = []
            tab = driver.find_elements_by_id(app_bar_dict["available_app"]["id"])
            for app in tab:
                ele.append(app)
                print("Available apps", app)
        except Exception as e:
            raise AssertionError
        pass


def view_scheduled_meeting_entries(device):
    print("device :", device)
    calendar_keywords.refresh_for_meeting_visibility(device)
    common.get_all_elements_texts(device, calendar_dict, "meeting_title_name")


def click_reorder_option(device):
    print("device :", device)
    common.wait_for_and_click(device, app_bar_dict, "reorder")
    common.wait_for_element(device, app_bar_dict, "edit_navigation")


def click_save_button(device):
    common.wait_for_and_click(device, app_bar_dict, "save_button")


def verify_default_tabs_along_with_more_option(device):
    print("device :", device)
    common.wait_for_element(device, app_bar_dict, "call_tab")
    common.wait_for_element(device, app_bar_dict, "calendar_tab")
    common.wait_for_element(device, walkie_talkie_dict, "walkie_talkie_tab")
    common.wait_for_element(device, app_bar_dict, "more_tab")


def validate_home_screen_after_reorder_of_apps(device, tab):
    tabs = tab.split(",")
    for tab in tabs:
        if tab.lower() == "calls tab":
            if common.is_element_present(device, app_bar_dict, "call_tab", "xpath"):
                print(f"{device}: Calls Tab is present on the app bar")
            else:
                common.wait_for_and_click(device, calendar_dict, "app_bar_more")
                common.wait_for_element(device, app_bar_dict, "call_tab", "xpath")
                common.wait_for_and_click(device, common_dict, "hide_more_app_icon")
        elif tab.lower() == "calendar tab":
            if common.is_element_present(device, app_bar_dict, "calendar_tab", "xpath"):
                print(f"{device}: Calendar Tab is present on the app bar")
            else:
                common.wait_for_and_click(device, calendar_dict, "app_bar_more")
                if not common.is_element_present(device, app_bar_dict, "calendar_tab", "xpath"):
                    if not common.is_portrait_mode_cnf_device(device):
                        raise AssertionError(f"{device}: Calendar app not found on app bar")
                    if not common.is_element_present(device, calendar_dict, "app_bar_dialpad_icon"):
                        raise AssertionError(f"{device}: Calendar app not found on device")
                print(f"{device}: Calendar Tab is present inside more options")
                common.wait_for_and_click(device, common_dict, "hide_more_app_icon")
        elif tab.lower() == "people tab":
            if common.is_element_present(device, app_bar_dict, "people_tab", "xpath"):
                print(f"{device}: People Tab is present on the app bar")
            else:
                common.wait_for_and_click(device, calendar_dict, "app_bar_more")
                common.wait_for_element(device, app_bar_dict, "people_tab", "xpath")
                common.wait_for_and_click(device, common_dict, "hide_more_app_icon")
        elif tab.lower() == "voicemail tab":
            if common.is_element_present(device, app_bar_dict, "voicemail_tab", "xpath"):
                print(f"{device}: Voicemail Tab is present on the app bar")
            else:
                common.wait_for_and_click(device, calendar_dict, "app_bar_more")
                common.wait_for_element(device, app_bar_dict, "voicemail_tab", "xpath")
                common.wait_for_and_click(device, common_dict, "hide_more_app_icon")


def navigate_to_more_option(device):
    device, account = common.decode_device_spec(device)
    if account.lower() == "meeting_user":
        common.wait_for_and_click(device, app_bar_dict, "more_tab")
        return
    common.wait_for_and_click(device, app_bar_dict, "more_tab")
    if not common.is_element_present(device, app_bar_dict, "voicemail_tab", "xpath"):
        if not common.is_element_present(device, app_bar_dict, "walkie_talkie_tab"):
            common.wait_for_element(device, app_bar_dict, "people_tab")
    common.wait_for_element(device, app_bar_dict, "reorder")


def verify_favorites_and_recent_call_tab(device):
    print("device :", device)
    common.wait_for_element(device, app_bar_dict, "favorites_tab")
    common.wait_for_element(device, app_bar_dict, "recent_tab")
    common.wait_for_element(device, app_bar_dict, "Make_a_call")
    if not common.is_portrait_mode_cnf_device(device):
        common.wait_for_element(device, app_bar_dict, "call_icon", "xpath")


def validate_reorder_of_apps(device, tab, destination):
    if not tab.lower() in ["calendar tab", "people tab", "calls tab"]:
        raise AssertionError(f"Illegal tab specified: '{tab}'")
    if not destination.lower() in ["people tab", "calendar tab", "more tab"]:
        raise AssertionError(f"Illegal destination specified: '{destination}'")
    print("device :", device)
    print("Tab is :", tab)
    print("Destination is :", destination)
    common.wait_for_and_click(device, app_bar_dict, "more_tab")
    common.wait_for_and_click(device, app_bar_dict, "reorder")
    time.sleep(display_time)
    if tab.lower() == "calendar tab":
        if destination.lower() == "people tab":
            common.perform_drag_and_drop(
                device, tab, app_bar_dict, "calendar_app", destination, app_bar_dict, "people_app"
            )
        else:
            raise AssertionError("Unable to move the source element to target element")
    elif tab.lower() == "people tab":
        if destination.lower() == "calendar tab":
            common.perform_drag_and_drop(
                device, tab, app_bar_dict, "people_app", destination, app_bar_dict, "calendar_app"
            )
        else:
            raise AssertionError("Unable to move the source element to target element")
    elif tab.lower() == "calls tab":
        if destination.lower() == "more tab":
            common.perform_drag_and_drop(device, tab, app_bar_dict, "call_app", destination, app_bar_dict, "more_tab")
            print("Unable to move the app from main section to more section ")
            print("Two app should present on main screen")
        else:
            raise AssertionError("Able to Move the app from main section to more section")
    common.wait_for_and_click(device, app_bar_dict, "save_button")


def validate_drag_and_drop_app_from_one_section_to_other_section(device, tab, destination):
    print("device :", device)
    print("tab :", tab)
    print("destination :", destination)
    driver = obj.device_store.get(alias=device)
    time.sleep(display_time)
    apps_in_more_section = driver.find_elements_by_xpath(app_bar_dict["more_tab"]["xpath"])
    time.sleep(display_time)
    if len(apps_in_more_section) == 0:
        print("All apps are present on the main section")
        return
    if tab.lower() == "calls tab":
        if destination.lower() == "voicemail tab":
            common.perform_drag_and_drop(
                device, tab, app_bar_dict, "call_app", destination, app_bar_dict, "voicemail_app"
            )
        elif destination.lower() == "calendar tab":
            common.perform_drag_and_drop(
                device, tab, app_bar_dict, "call_app", destination, app_bar_dict, "calendar_app"
            )
            print("Come back to default setting")
        elif destination.lower() == "people tab":
            common.perform_drag_and_drop(device, tab, app_bar_dict, "call_app", destination, app_bar_dict, "people_app")
        elif destination.lower() == "walkie talkie tab":
            common.perform_drag_and_drop(
                device, tab, app_bar_dict, "call_app", destination, walkie_talkie_dict, "walkie_talkie_tab"
            )
        else:
            raise AssertionError(f"Unexpected value for destination : {destination}")
    elif tab.lower() == "calendar tab":
        if destination.lower() == "voicemail tab":
            common.perform_drag_and_drop(
                device, tab, app_bar_dict, "calendar_app", destination, app_bar_dict, "voicemail_app"
            )
        elif destination.lower() == "people tab":
            common.perform_drag_and_drop(
                device, tab, app_bar_dict, "calendar_app", destination, app_bar_dict, "people_app"
            )
        else:
            raise AssertionError("None of the Tab matched with the Destination")
    elif tab.lower() == "people tab":
        if destination.lower() == "voicemail tab":
            common.perform_drag_and_drop(
                device, tab, app_bar_dict, "people_app", destination, app_bar_dict, "voicemail_app"
            )
        elif destination.lower() == "calendar tab":
            common.perform_drag_and_drop(
                device, tab, app_bar_dict, "people_app", destination, app_bar_dict, "calendar_app"
            )
        else:
            raise AssertionError("None of the Tab matched with the Destination")
    elif tab.lower() == "voicemail tab":
        common.perform_drag_and_drop(device, tab, app_bar_dict, "voicemail_app", destination, app_bar_dict, "call_app")
    elif tab.lower() == "walkie talkie tab":
        common.perform_drag_and_drop(
            device, tab, walkie_talkie_dict, "walkie_talkie_tab", destination, app_bar_dict, "voicemail_app"
        )
    else:
        raise AssertionError(f"Unexpected value for tab : {tab}")
    common.wait_for_and_click(device, app_bar_dict, "save_button")
    common.sleep_with_msg(device, 3, "Wait for sometime post clicking on the save button")


def navigate_to_hidden_app_inside_more_option(device):
    # time.sleep(display_time)
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((MobileBy.ID, app_bar_dict["voicemail_tab"]["id"]))
        ).click()
        voicemail_keywords.navigate_to_voicemail_tab(device)
    except Exception as e:
        raise AssertionError("Navigate to Voicemail Tab is Failed")


def select_default_view_option(device, option):
    if option.lower() not in ["speed dial", "recent call history", "call dialpad"]:
        raise AssertionError(f"{device}: Unexpected value for option: {option}")
    if not common.is_portrait_mode_cnf_device(device) and option.lower() == "call dialpad":
        print(f"{device} is not a portrait mode device. Hence, dialpad is not supported under default view section")
        common.click_if_present(device, calls_dict, "Call_Back_Button")
        return
    common.wait_for_and_click(device, app_bar_dict, "Calling")
    swipe_page_up(device)
    common.wait_for_and_click(device, app_bar_dict, "default_view")
    if option.lower() == "speed dial":
        common.wait_for_and_click(device, app_bar_dict, "speed_dial")
    elif option.lower() == "recent call history":
        common.wait_for_and_click(device, app_bar_dict, "recent_call_history")
    elif option.lower() == "call dialpad":
        common.wait_for_and_click(device, app_bar_dict, "call_dialpad", "id")
    common.wait_for_and_click(device, app_bar_dict, "relaunch_btn")
    common.wait_for_element(device, calls_dict, "search")


def validate_default_app_present_on_main_screen(device):
    common.wait_for_element(device, app_bar_dict, "call_app")
    common.wait_for_element(device, people_dict, "people_app")


def swipe_page_up(device):
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
        print("Swiping co-ordinates : ", width / 8, 4 * (height / 5), width / 8, height / 5)
        driver.swipe(width / 8, 4 * (height / 5), width / 8, height / 5)
    pass


def verify_apps_under_more_option(device, tab=None):
    if ":" in device:
        user = device.split(":")[1]
        device = device.split(":")[0]
    else:
        user = "user"
    common.wait_for_and_click(device, calendar_dict, "app_bar_more")
    if user == "meeting_user":
        if common.is_portrait_mode_cnf_device(device):
            common.wait_for_element(device, calendar_dict, "app_bar_meet_now")
            common.wait_for_element(device, calendar_dict, "app_bar_dialpad_icon")
            common.wait_for_element(device, people_dict, "people_tab")
            common.wait_for_element(device, navigation_dict, "Settings_button")
            common.wait_for_element(device, navigation_dict, "what's_new")
            common.wait_for_element(device, calls_dict, "Call_Back_Button")
            return
        common.wait_for_element(device, app_bar_dict, "reorder")
    else:
        more_apps_list = common.get_all_elements_texts(device, app_bar_dict, "hidden_app_name")
        if tab is not None:
            tabs = tab.split(",")
            for tab_name in tabs:
                if tab_name.lower() not in more_apps_list:
                    raise AssertionError(f"{tab_name} is not present under more options")
    common.wait_for_and_click(device, app_bar_dict, "hide_more_app_icon")


def app_bar_feature(device):
    print("device :", device)
    if common.is_portrait_mode_cnf_device(device):
        status = "fail"
    else:
        status = "pass"
    return status
