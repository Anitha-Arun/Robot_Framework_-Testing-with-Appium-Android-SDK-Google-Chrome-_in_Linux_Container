import time
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from Selectors import load_json_file
from initiate_driver import obj_dev as obj
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import common

display_time = 3
action_time = 3

app_bar_dict = load_json_file("resources/Page_objects/App_bar.json")
calls_dict = load_json_file("resources/Page_objects/Calls.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")
common_dict = load_json_file("resources/Page_objects/Common.json")


def click_hide_more_apps(device):
    print("device :", device)
    common.wait_for_and_click(device, app_bar_dict, "hide_more_app_icon", "xpath")


def verify_available_app_present_on_screen(device):
    devices = device.split(",")
    time.sleep(display_time)
    for device in devices:
        print("device :", device)
        ele = []
        tab = common.wait_for_element(device, app_bar_dict, "available_app", "id")
        for app in tab:
            ele.append(app)
            print("Available apps", app)


def click_reorder_option(device):
    print("device :", device)
    common.wait_for_and_click(device, app_bar_dict, "reorder", "id")
    common.wait_for_element(device, app_bar_dict, "edit_navigation", "xpath")


def click_save_button(device):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    save = (
        WebDriverWait(driver, 30)
        .until(EC.element_to_be_clickable((MobileBy.ID, app_bar_dict["save_button"]["id"])))
        .click()
    )
    print("Click on the save button")
    return save


def verify_default_tabs_along_with_more_option(device):
    print("device :", device)
    common.wait_for_element(device, app_bar_dict, "call_tab")
    common.wait_for_element(device, app_bar_dict, "calendar_tab")
    common.wait_for_element(device, app_bar_dict, "people_tab")
    common.wait_for_element(device, app_bar_dict, "more_tab")


def validate_home_screen_after_reorder_of_apps(device, tab):
    time.sleep(display_time)
    tabs = tab.split(",")
    for tab in tabs:
        driver = obj.device_store.get(alias=device)
        print("device :", device)
        try:
            if tab.lower() == "calls tab":
                try:
                    WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((MobileBy.XPATH, app_bar_dict["call_tab"]["xpath"]))
                    )
                    print("Calls Tab is present on the app bar")
                except Exception as e:
                    print("Calls Tab is Not present on the app bar")
            elif tab.lower() == "calendar tab":
                try:
                    WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((MobileBy.XPATH, app_bar_dict["calendar_tab"]["xpath"]))
                    )
                    print("Calendar Tab is present on the app bar")
                except Exception as e:
                    print("Calendar Tab is Not present on the app bar")
            elif tab.lower() == "people tab":
                try:
                    WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((MobileBy.XPATH, app_bar_dict["people_tab"]["xpath"]))
                    )
                    print("People Tab is present on the app bar")
                except Exception as e:
                    print("People Tab is Not present on the app bar")
            elif tab.lower() == "voicemail tab":
                try:
                    WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((MobileBy.XPATH, app_bar_dict["voicemail_tab"]["xpath"]))
                    )
                    print("Voicemail Tab is present on the app bar")
                except Exception as e:
                    print("Voicemail Tab is Not present on the app bar")
        except Exception as e:
            raise AssertionError("xpath not found", e)
        pass


def navigate_to_more_option(device):
    print("device :", device)
    common.wait_for_and_click(device, app_bar_dict, "more_tab")
    common.wait_for_element(device, app_bar_dict, "reorder")
    common.wait_for_element(device, app_bar_dict, "voicemail_tab")


def verify_favorites_and_recent_call_tab(device):
    print("device :", device)
    common.wait_for_element(device, app_bar_dict, "favorites_tab")
    common.wait_for_element(device, app_bar_dict, "recent_tab")
    common.wait_for_element(device, app_bar_dict, "Make_a_call")
    if common.is_portrait_mode_cnf_device(device):
        common.wait_for_element(device, app_bar_dict, "call_icon")
    else:
        common.wait_for_element(device, app_bar_dict, "Details_Container")


def validate_reorder_of_apps(device, tab, destination):
    print("device :", device)
    print("Tab is :", tab)
    print("Destination is :", destination)
    driver = obj.device_store.get(alias=device)
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((MobileBy.XPATH, app_bar_dict["more_tab"]["xpath"]))
    ).click()
    print("Click on More option button")
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((MobileBy.ID, app_bar_dict["reorder"]["id"]))).click()
    print("Click on reorder option")
    time.sleep(display_time)
    try:
        if tab.lower() == "calendar tab":
            e1 = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, app_bar_dict["calendar_app"]["xpath"]))
            )
            print("source element is :", e1)
            if destination.lower() == "people tab":
                e2 = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, app_bar_dict["people_app"]["xpath"]))
                )
                print("target element is :", e2)
                actions = TouchAction(driver)
                actions.long_press(e1).move_to(e2).release().perform()
                print("Successfully moved the source element to target element")
            else:
                raise AssertionError("Unable to move the source element to target element")
        elif tab.lower() == "people tab":
            e3 = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.XPATH, app_bar_dict["people_app"]["xpath"]))
            )
            print("source element is :", e3)
            if destination.lower() == "calendar tab":
                e4 = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, app_bar_dict["calendar_app"]["xpath"]))
                )
                print("target element is :", e4)
                actions = TouchAction(driver)
                actions.long_press(e3).move_to(e4).release().perform()
                print("Successfully moved the source element to target element")
            else:
                raise AssertionError("Unable to move the source element to target element")
        save = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, app_bar_dict["save_button"]["xpath"]))
        )
        save.click()
        print("Clicked on the save button")
    except Exception as e:
        raise AssertionError("xpath not found", e)


def validate_drag_and_drop_app_from_one_section_to_other_section(device, tab, destination):
    print("device :", device)
    print("tab :", tab)
    print("destination :", destination)
    driver = obj.device_store.get(alias=device)
    time.sleep(display_time)
    if tab.lower() == "calls tab":
        e1 = common.wait_for_element(device, app_bar_dict, "call_app", "xpath")
        print("source element is :", e1)
        if destination.lower() == "voicemail tab":
            e2 = common.wait_for_element(device, app_bar_dict, "voicemail_app", "xpath")
            print("target element is :", e2)
            actions = TouchAction(driver)
            actions.long_press(e1).move_to(e2).release().perform()
            print("Successfully moved the calls tab from main section to more section")
        elif destination.lower() == "calendar tab":
            e4 = common.wait_for_element(device, app_bar_dict, "call_app", "xpath")
            print("source element is :", e4)
            e5 = common.wait_for_element(device, app_bar_dict, "calendar_app", "xpath")
            print("target element is :", e5)
            actions = TouchAction(driver)
            actions.long_press(e4).move_to(e5).release().perform()
            print("Successfully moved the call tab from more section to main section")
            print("Come back to default setting")
        else:
            raise AssertionError(f"{device}: Illegal 'destination' specified: '{destination}'")
    elif tab.lower() == "calendar tab":
        e3 = common.wait_for_element(device, app_bar_dict, "calendar_app")
        print("source element is :", e3)
        e4 = common.wait_for_element(device, app_bar_dict, "voicemail_app", "xpath")
        print("target element is :", e4)
        actions = TouchAction(driver)
        actions.long_press(e3).move_to(e4).release().perform()
        print("Successfully moved the calendar tab from main section to more section")
    elif tab.lower() == "people tab":
        e5 = common.wait_for_element(device, app_bar_dict, "people_app", "xpath")
        print("source element is :", e5)
        e6 = common.wait_for_element(device, app_bar_dict, "voicemail_app", "xpath")
        print("target element is :", e6)
        actions = TouchAction(driver)
        actions.long_press(e5).move_to(e6).release().perform()
        print("Successfully moved the people tab from main section to more section")
    elif tab.lower() == "voicemail tab":
        e7 = common.wait_for_element(device, app_bar_dict, "voicemail_app", "xpath")
        print("source element is :", e7)
        e8 = common.wait_for_element(device, app_bar_dict, "call_app", "xpath")
        print("target element is :", e8)
        actions = TouchAction(driver)
        actions.long_press(e7).move_to(e8).release().perform()
        print("Successfully moved the voicemail tab from more section to main section")
        ele = driver.find_elements_by_xpath(app_bar_dict["more_tab"]["xpath"])
        time.sleep(display_time)
        if len(ele) == 0:
            print("All four apps are present on the main section")
    common.wait_for_and_click(device, app_bar_dict, "save_button")
