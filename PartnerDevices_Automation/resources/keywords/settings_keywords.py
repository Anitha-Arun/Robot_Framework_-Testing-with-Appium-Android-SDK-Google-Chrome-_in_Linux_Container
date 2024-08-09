from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidElementStateException
from robot.libraries.BuiltIn import BuiltIn

import device_control
import initiate_driver
from Selectors import load_json_file
from initiate_driver import config
import call_keywords
import people_keywords
import calendar_keywords
import call_views_keywords
from initiate_driver import obj_dev as obj
import common
from subprocess import CalledProcessError
import time
import subprocess
from PIL import Image
import os
from datetime import datetime
import home_screen_keywords
import device_settings_keywords
import settings_keywords
import panel_meetings_device_settings_keywords
import app_bar_keywords


display_time = 2
action_time = 2
sleep_time = 5
sleep_time1 = 10

navigation_dict = load_json_file("resources/Page_objects/Navigation.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")
calls_dict = load_json_file("resources/Page_objects/Calls.json")
home_screen_dict = load_json_file("resources/Page_objects/Home_screen.json")
sign_dict = load_json_file("resources/Page_objects/Signin.json")
common_dict = load_json_file("resources/Page_objects/Common.json")
calendar_dict = load_json_file("resources/Page_objects/Calendar.json")
hot_desk_dict = load_json_file("resources/Page_objects/Hot_desk.json")
device_settings_dict = load_json_file("resources/Page_objects/Device_settings.json")
lcp_homescreen_dict = load_json_file("resources/Page_objects/lcp_homescreen.json")
lcp_calls_dict = load_json_file("resources/Page_objects/lcp_calls.json")
app_bar_dict = load_json_file("resources/Page_objects/App_bar.json")
tr_Signin_dict = load_json_file("resources/Page_objects/tr_Signin.json")
tr_device_settings_dict = load_json_file("resources/Page_objects/tr_device_settings.json")
panels_device_settings_dict = load_json_file("resources/Page_objects/panels_device_settings.json")
people_dict = load_json_file("resources/Page_objects/people.json")
# This flag is explicitly set ONLY during standalone testing.
# If set, the code deals with errors which should normally be fatal.
StandaloneTesting = False


def click_back(device):
    devices = device.split(",")
    for device in devices:
        common.wait_for_and_click(device, calls_dict, "Call_Back_Button")


def device_setting_back(device):
    """
    Avoid this - We should use the UI instead of inserting key events with ADB.
    """
    print(f"{device}: WARN - Using ADB - device back button, instead of UI back")
    _udid = common.device_udid(device)
    subprocess.call(
        f"adb -s {_udid} shell input keyevent KEYCODE_BACK",
        shell=True,
    )


def open_settings_page(device):
    for _attempt in range(20):
        common.click_if_present(device, calls_dict, "Call_Back_Button")
        common.click_if_present(device, home_screen_dict, "home_bar_icon")
        if common.is_lcp(device):
            common.wait_for_and_click(device, lcp_homescreen_dict, "homescreen_menu")
            common.wait_for_and_click(device, lcp_homescreen_dict, "settings_icon")
            return
        elif common.click_if_present(device, navigation_dict, "Navigation"):
            break
        elif common.click_if_present(device, calls_dict, "user_profile_picture"):
            break
        if _attempt == 19:
            raise AssertionError(f"{device} couldn't open navigation menu")
    time.sleep(1)
    common.wait_for_and_click(device, navigation_dict, "Settings_button")
    common.wait_for_element(device, settings_dict, "settings_page_header")


def enable_call_forwarding(device):
    devices = device.split(",")
    for device in devices:
        set_call_forwarding(device, "ON")


def disable_call_forwarding(device):
    devices = device.split(",")
    for device in devices:
        set_call_forwarding(device, "OFF")
        device_setting_back(device)
        common.click_if_present(device, device_settings_dict, "admin_settings_yes")
        device_setting_back(device)
        common.click_if_present(device, calls_dict, "Call_Back_Button")


def set_call_forwarding(device, desired_state):
    """
    Ensure Call Forwarding is the 'desired_state'. Either:
    a) Toggle Call Forwarding, or
    b) verify Call Forwarding is already in the desired state, or
    c) Verify the option is unavailable, AND there is no phone number defined.
    """

    global state
    time.sleep(display_time)
    if not common.click_if_present(device, settings_dict, "Calling"):
        swipe_till_end(device)
        swipe_till_end(device)
        common.wait_for_and_click(device, settings_dict, "Device_Settings")
        device_settings_keywords.advance_calling_option_oem(device)
        common.wait_for_element(device, settings_dict, "call_forwarding")

    time.sleep(display_time)

    # Make sure we get to the Calling Options page
    common.wait_for_element(device, settings_dict, "Calling_opts_pagetitle")

    if not common.is_element_present(
        device, settings_dict, "Call_forward_toggle", selector_key="id", cond=EC.element_to_be_clickable
    ):
        account_type = "user"
        phonenumber = config["devices"][device][account_type]["phonenumber"]
        print(f"{device}['{account_type}']['phonenumber'] is '{phonenumber}'")
        if len(phonenumber) < 3:
            print(f"{device}: No phone number configured, missing Call_forward_toggle is ignored")
            return

    call_forwarding_toggle = common.wait_for_element(device, settings_dict, "Call_forward_toggle")
    call_forwarding_status = call_forwarding_toggle.get_attribute("checked")
    print(f"call_forwarding_status :{call_forwarding_status}")

    if desired_state == "ON":
        state = "true"
    elif desired_state == "OFF":
        state = "false"
    print(f"{device}: Set call_forwarding to '{desired_state}, state: {state}'")

    if call_forwarding_status == state:
        print(f"{device}: Call forwarding is already '{desired_state}'")
    else:
        common.wait_for_and_click(device, settings_dict, "Call_forward_toggle", "id")
        call_forwarding_toggle = common.wait_for_element(device, settings_dict, "Call_forward_toggle")
        call_forwarding_status = call_forwarding_toggle.get_attribute("checked")
        if state != call_forwarding_status:
            raise AssertionError(f"{device}: Unexpected state of Call forwarding toggle")
        if state == "true":
            time.sleep(display_time)
            if common.is_element_present(device, settings_dict, "also_ring"):
                raise AssertionError(f"{device}: Call forwarding did not transition to {desired_state} after click")
        else:
            common.wait_for_element(device, settings_dict, "also_ring")


def click_device_settings(device):
    _attempt = 0
    while _attempt < 4:
        if common.click_if_present(device, settings_dict, "Device_Settings"):
            return
        swipe_till_end(device)
        _attempt += 1
    common.wait_for_and_click(device, settings_dict, "Device_Settings")


def swipe_till_end(device):
    driver = obj.device_store.get(alias=device)
    window_size = driver.get_window_size()
    print(f"{device}: Window size: ", window_size)
    height = window_size["height"]
    # print("Window Height :", height)
    width = window_size["width"]
    # print("Window Width :", width)
    try:
        if height > width:
            print(f"{device}: Swiping portrait co-ordinates : ", width / 2, 4 * (height / 5), width / 2, height / 5)
            driver.swipe(width / 2, 4 * (height / 5), width / 2, height / 5)
        else:
            print(f"{device}: Swiping landscape co-ordinates : ", width / 4, 4 * (height / 5), width / 4, height / 5)
            driver.swipe(width / 4, 4 * (height / 5), width / 4, height / 5)
    except InvalidElementStateException:
        common.sleep_with_msg(device, 5, "Trapped InvalidElementStateException, retrying...")
        if height > width:
            driver.swipe(width / 2, 4 * (height / 5), width / 2, height / 5)
        else:
            driver.swipe(width / 4, 4 * (height / 5), width / 4, height / 5)
        print(f"{device}: Retry Success!")


def click_settings_debug(device):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((MobileBy.XPATH, settings_dict["Debug"]["xpath"]))
    ).click()
    print("Clicked on settings>Debug button")
    time.sleep(display_time)


def reboot_device(device):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((MobileBy.XPATH, settings_dict["Reboot_phone"]["xpath"]))
    ).click()
    print("Clicked on Reboot phone button")
    time.sleep(display_time)
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((MobileBy.XPATH, settings_dict["Sign_out_ok"]["xpath"]))
    ).click()
    print("Clicked on Reboot OK button")
    time.sleep(display_time)


def enable_dark_theme(device):
    print("device :", device)
    common.wait_for_and_click(device, settings_dict, "Appearance_btn")
    time.sleep(action_time)
    if common.is_element_present(device, settings_dict, "dark_theme_selected"):
        print(f"{device} is already selected dark theme")
        common.wait_for_and_click(device, calendar_dict, "touch_outside")
    else:
        common.wait_for_and_click(device, settings_dict, "dark_theme")
        common.wait_for_and_click(device, settings_dict, "restart_btn")
        common.sleep_with_msg(device, 30, "Wait for app restart post tapping on dark theme")
        # Workaround for BUG:3719192(To dismiss got it button)
        common.click_if_element_appears(device, sign_dict, "Gotit_button", max_attempts=5)


def disable_dark_theme(device):
    print("device :", device)
    common.wait_for_and_click(device, settings_dict, "Appearance_btn")
    time.sleep(action_time)
    if common.is_element_present(device, settings_dict, "light_theme_selected"):
        print(f"{device} is already selected light theme")
        device_setting_back(device)
    else:
        common.wait_for_and_click(device, settings_dict, "light_theme")
        common.wait_for_and_click(device, settings_dict, "restart_btn")
    common.sleep_with_msg(device, 30, "Wait for app restart post tapping on light theme")


def verify_dark_theme_status(device, status):
    open_settings_page(device)
    if status.lower() not in ["on", "off"]:
        raise AssertionError(f"Illegal value for 'status': '{status}'")
    print("device :", device)
    time.sleep(display_time)
    common.wait_for_and_click(device, settings_dict, "Appearance_btn")
    if status.lower() == "off":
        common.wait_for_element(device, settings_dict, "light_theme_selected")
    elif status.lower() == "on":
        common.wait_for_element(device, settings_dict, "dark_theme_selected")
    device_setting_back(device)


def ignorefail_decorator(func):
    """
    Decorator to log and eat any exceptions raised by the wrapped method.
    Intended for preventing non-critical operations from interfereing with critical operations.
    """

    def _ignorefail(self, *args, **kwargs):
        try:
            result = func(self, *args)
            return result
        except Exception as e:
            # This is the last resort - exceptions should have been handled by the wrapped
            #   method. Mark these as errors and fix:
            print(f"ERROR: Ignored Exception in {func.__name__}: {type(e)}: {e})")
            return None

    return _ignorefail


def get_screenshot(name: str, device_list=None, with_xml: bool = True):
    """
    Gather device screenshots/xml (either real data or generic placeholders)
    """

    @ignorefail_decorator
    def ignorefail_get_screenshot(name: str, device_list=None, with_xml: bool = True):
        # Parameter sanith checks
        if not isinstance(name, str):
            raise AssertionError(f"get_screenshot: Cannot handle a 'name' parameter of type {type(name)}.")

        if isinstance(device_list, list):
            devices = device_list
        elif device_list is None:
            devices = list(config["devices"].keys())
        elif isinstance(device_list, str):
            devices = device_list.split(",")
        else:
            raise AssertionError(
                f"get_screenshot: Cannot handle a 'device_list' parameter of type {type(device_list)}."
            )

        if not isinstance(with_xml, bool):
            raise AssertionError(f"get_screenshot: Cannot handle a 'with_xml' parameter of type {type(with_xml)}.")

        # Default screenshot if unavailable from device
        unavailable_screenshot = "unavailable.png"

        name = (
            name.replace(" ", "_")
            .replace(":", "-")
            .replace("/", "_")
            .replace('"', "")
            .replace(".", "")
            .replace("'", "")
            .replace(",", "")
            .replace(">", "")
            .replace("<", "")
        )
        print("name : ", name)
        print("Devices : ", devices)

        img_filename_list = []
        xml_list = {}

        # Gather data from all the requested devices:
        for device in devices:
            try:
                driver = obj.device_store.get(alias=device)
            except Exception as e:
                print(f"{device}: WARNING Unable to get WebDriver: {str(e)}")
                # Continue, but fill the screenshots/XML files
                # with placeholder data (at least the timestamp will be useful)
                driver = None

            try:
                file_name = device + ".png"
                driver.get_screenshot_as_file(file_name)
                img_filename_list.append(file_name)
            except Exception as e:
                if driver:
                    print(f"{device}: WARNING Unable to fetch screenshot: {str(e)}")
                img_filename_list.append(unavailable_screenshot)

            try:
                xml_list[device] = driver.page_source.encode("utf-8")
            except Exception as e:
                if driver:
                    print(f"{device}: WARNING Unable to fetch XML: {str(e)}")
                xml_list[device] = '<?xml version="1.0" encoding="utf-8"?><ui>XML unavailable</ui>'.encode("utf-8")

        # Compose the output composite bitmap:
        border_width = 3
        images = [Image.open(x) for x in img_filename_list]
        widths, heights = list(zip(*(i.size for i in images)))
        total_width = sum(widths) + border_width + (len(devices) * border_width)
        max_height = max(heights)

        # Start with a large Black canvas to paste images onto:
        new_im = Image.new("RGB", (total_width, max_height), (0, 0, 0))

        x_offset = border_width
        for im in images:
            new_im.paste(im, (x_offset, 0))
            x_offset += im.size[0] + border_width

        # Set the output composite bitmap name:
        current_time = datetime.now().strftime("%H%M%S")
        file_name = current_time + "_" + name + ".png"

        # Save the output composite bitmap:
        try:
            newpath = BuiltIn().get_variable_value("${OUTPUT DIR}") + "\\screenshots\\"
        except Exception as e:
            if not StandaloneTesting:
                raise AssertionError(
                    f"get_screenshot: Screenshot unavailable, cannot determine output directory: {str(e)}"
                )
            # Standalone testing - using: ".\..\..\screenshots" (relative to this file).
            newpath = os.path.dirname(os.path.abspath(__file__))  # "."
            newpath = os.path.dirname(newpath)  # ".\.."
            newpath = os.path.dirname(newpath)  # ".\..\.."
            newpath = os.path.join(newpath, "screenshots")
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        new_im.save(os.path.join(newpath, file_name))

        print(f"Devices: {str(devices)} - New screenshot: {file_name}")
        try:
            BuiltIn().log(message="<image src=screenshots\\" + file_name + ' width="90%">', html=True)
        except Exception as e:
            if not StandaloneTesting:
                print(f"WARNING: Cannot log screenshot reference: {str(e)}")

        # Save XML files:
        if with_xml:
            for device_name in xml_list:
                try:
                    file_name1 = "\\\\?\\" + os.path.join(newpath, file_name) + "_" + device_name + ".xml"
                    with open(file_name1, "wb") as xml_file:
                        xml_file.write(xml_list[device_name])
                except Exception as e:
                    print(f"WARNING: Unable to write ui XML log for {device_name}! : {str(e)}")

        # Clean up any temporary device bitmaps
        for file_name in img_filename_list:
            if file_name == unavailable_screenshot:
                continue
            try:
                os.remove(file_name)
            except Exception as e:
                print(f"WARNING: Unable to clean temporary file: {file_name}: {str(e)}")

    ignorefail_get_screenshot(name, device_list, with_xml)


def refresh_calls_main_tab(device):
    devices = device.split(":")
    device = devices[0]
    driver = obj.device_store.get(alias=device)
    if common.is_phone(device):
        container = common.wait_for_element(device, calls_dict, "calls_tab_container")
        container_bounds = container.get_attribute("bounds").replace("][", ",").strip("]").strip("[").split(",")
        cont_cord = list(map(int, container_bounds))
        print(f"Container bounds: {cont_cord}")
        x1 = cont_cord[0] + (cont_cord[2] - cont_cord[0]) / 2
        y1 = cont_cord[1] + 20
        x2 = x1
        y2 = y1 + 4 * (cont_cord[3] - cont_cord[1]) / 5
        driver.swipe(x1, y1, x2, y2)
        time.sleep(action_time)
        driver.swipe(x1, y1, x2, y2)
        print(f"{device}: swiped and refreshed co-ordinates:({x1},{y1}), ({x2}, {y2})")
        return
    window_size = driver.get_window_size()
    print("Window size: ", window_size)
    height = window_size["height"]
    print("Window Height :", height)
    width = window_size["width"]
    print("Window Width :", width)
    if height > width:
        print("Refreshing co-ordinates : ", width / 2, height / 3, width / 2, 4 * (height / 5))
        driver.swipe(width / 2, height / 3, width / 2, 4 * (height / 5))
        time.sleep(action_time)
        driver.swipe(width / 2, height / 3, width / 2, 4 * (height / 5))
    else:
        print("Refreshing co-ordinates : ", 3 * (width / 4), height / 3, 3 * (width / 4), 4 * (height / 5))
        driver.swipe(3 * (width / 4), height / 3, 3 * (width / 4), 4 * (height / 5))
        time.sleep(action_time)
        driver.swipe(3 * (width / 4), height / 3, 3 * (width / 4), 4 * (height / 5))
    time.sleep(display_time)


def refresh_main_tab(device):
    driver = obj.device_store.get(alias=device)
    window_size = driver.get_window_size()
    print("Window size: ", window_size)
    height = window_size["height"]
    width = window_size["width"]
    if height > width:
        print("Refreshing co-ordinates : ", width / 2, height / 3, width / 2, 4 * (height / 5))
        driver.swipe(width / 2, height / 3, width / 2, 4 * (height / 5))
        time.sleep(action_time)
        driver.swipe(width / 2, height / 3, width / 2, 4 * (height / 5))
    else:
        print("Refreshing co-ordinates : ", width / 4, height / 3, width / 4, 4 * (height / 5))
        driver.swipe(width / 4, height / 3, width / 4, 4 * (height / 5))
        time.sleep(action_time)
        driver.swipe(width / 4, height / 3, width / 4, 4 * (height / 5))
    time.sleep(display_time)


def call_forward_setup(from_device, contact_device, call_forward_to):
    if not call_forward_to.lower() in ["contacts", "call group", "delegate", "voicemail"]:
        raise AssertionError(f"Illegal call_forward_to specified: '{call_forward_to}'")

    if ":" in contact_device:
        devices, account = common.decode_device_spec(contact_device)
        if account == "pstn_user":
            display_name = config["devices"][devices][account]["pstndisplay"]
        else:
            display_name = common.config["devices"][devices][account]["displayname"]
    else:
        display_name = common.device_displayname(contact_device)

    for from_device in from_device.split(","):
        print("device : ", from_device)
        if not common.click_if_present(from_device, settings_dict, "Calling", "xpath"):
            # If the user is already on calling settings page, proceed with toggle button check.
            if not common.is_element_present(from_device, settings_dict, "call_forwarding"):
                swipe_till_end(from_device)
                swipe_till_end(from_device)
                common.wait_for_and_click(from_device, settings_dict, "Device_Settings")
                device_settings_keywords.advance_calling_option_oem(from_device)
                common.wait_for_element(from_device, settings_dict, "call_forwarding")

        time.sleep(sleep_time1)
        common.change_toggle_button(from_device, settings_dict, "Call_forward_toggle", desired_state="on")
        common.wait_for_and_click(from_device, settings_dict, "forward_option_btn")

        if (call_forward_to.lower()) == "contacts":
            common.wait_for_and_click(from_device, settings_dict, "contact_option")
            time.sleep(display_time)
            common.click_if_present(from_device, settings_dict, "add_contact_option")
            element = common.wait_for_element(from_device, settings_dict, "search_contact_box")
            element.send_keys(display_name)
            time.sleep(display_time)
            common.hide_keyboard(from_device)
            tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", display_name)
            common.wait_for_and_click(from_device, tmp_dict, "search_result_item_container", "xpath")
        elif call_forward_to.lower() == "call group":
            common.wait_for_and_click(from_device, settings_dict, "also_ring_call_group_btn")
        elif call_forward_to.lower() == "delegate":
            _max_attempts = 30
            for _attempt in range(_max_attempts):
                if common.click_if_present(from_device, settings_dict, "also_ring_delegate_btn"):
                    break
                # If delegate option is absent, there might not be any delegates added. Hence, add it and continue
                if _attempt == _max_attempts - 1:
                    common.return_to_home_screen(from_device)
                    open_settings_page(from_device)
                    open_manage_delegate_page(from_device)
                    add_new_delegate(from_device, contact_device)
                    call_views_keywords.go_back_to_previous_page(from_device)
                    open_settings_page(from_device)
                    call_forward_setup(from_device, contact_device, "delegate")
        elif call_forward_to.lower() == "voicemail":
            common.wait_for_and_click(from_device, settings_dict, "voicemail_option")
        time.sleep(3)
        device_setting_back(from_device)


def select_if_unanswered_option(device):
    if not common.click_if_present(device, settings_dict, "Calling", "xpath"):
        swipe_till_end(device)
        swipe_till_end(device)
        common.wait_for_and_click(device, settings_dict, "Device_Settings")
        device_settings_keywords.advance_calling_option_oem(device)
        common.wait_for_element(device, settings_dict, "call_forwarding")
    common.wait_for_and_click(device, settings_dict, "unanswered_btn")


def unanswered_call_setup(from_device, contact_device, select_option):
    if not select_option.lower() in ["contacts", "off", "call group", "delegate", "voicemail"]:
        raise AssertionError(f"Illegal select_option specified: '{select_option}'")
    pstn_displayname = common.device_pstndisplay(contact_device)
    select_if_unanswered_option(from_device)
    if select_option.lower() == "contacts":
        common.wait_for_and_click(from_device, settings_dict, "contact_option")
        time.sleep(display_time)
        common.click_if_present(from_device, settings_dict, "add_contact_option")
        element = common.wait_for_element(from_device, settings_dict, "search_contact_box")
        element.send_keys(pstn_displayname)
        time.sleep(display_time)
        common.hide_keyboard(from_device)
        tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", pstn_displayname)
        common.wait_for_and_click(from_device, tmp_dict, "search_result_item_container", "xpath")
    elif select_option.lower() == "off":
        common.wait_for_and_click(from_device, settings_dict, "unanswerd_off")
        time.sleep(display_time)
    elif select_option.lower() == "voicemail":
        common.wait_for_and_click(from_device, settings_dict, "voicemail_option")
    elif select_option.lower() == "call group":
        common.wait_for_and_click(from_device, settings_dict, "also_ring_call_group_btn")
    elif select_option.lower() == "delegate":
        common.wait_for_and_click(from_device, settings_dict, "also_ring_delegate_btn")
    time.sleep(3)
    device_setting_back(from_device)
    device_setting_back(from_device)
    call_keywords.come_back_to_home_screen(from_device)


def select_also_ring_option(device):
    print("device :", device)
    time.sleep(display_time)
    if not common.click_if_present(device, settings_dict, "Calling", "xpath"):
        swipe_till_end(device)
        swipe_till_end(device)
        common.wait_for_and_click(device, settings_dict, "Device_Settings")
        device_settings_keywords.advance_calling_option_oem(device)
        common.wait_for_element(device, settings_dict, "call_forwarding")
    if not common.click_if_element_appears(device, settings_dict, "also_ring_btn", max_attempts=3):
        common.wait_for_and_click(device, settings_dict, "call_forward_to")


def setup_also_ring(device, select_option, contact_device=None):
    if not select_option.lower() in ["contact", "off", "call group", "delegate", "voicemail"]:
        raise AssertionError(f"Illegal select_option specified: '{select_option}'")
    time.sleep(action_time)
    if contact_device is not None:
        if ":" in contact_device:
            devices, account = common.decode_device_spec(contact_device)
            if account == "pstn_user":
                display_name = config["devices"][devices][account]["pstndisplay"]
            else:
                display_name = common.config["devices"][devices][account]["displayname"]
        else:
            display_name = common.device_displayname(contact_device)

    select_also_ring_option(device)
    if select_option.lower() == "off":
        common.wait_for_and_click(device, settings_dict, "also_ring_off_btn")
    elif select_option.lower() == "contact":
        common.wait_for_and_click(device, settings_dict, "contact_option")
        time.sleep(5)
        common.click_if_present(device, settings_dict, "add_contact_option")
        element = common.wait_for_element(device, settings_dict, "search_contact_box")
        element.send_keys(display_name)
        common.hide_keyboard(device)
        tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", display_name)
        common.wait_for_and_click(device, tmp_dict, "search_result_item_container", "xpath")
    elif select_option.lower() == "voicemail":
        common.wait_for_and_click(device, settings_dict, "voicemail_option")
    elif select_option.lower() == "call group":
        common.wait_for_and_click(device, settings_dict, "also_ring_call_group_btn")
    elif select_option.lower() == "delegate":
        common.wait_for_and_click(device, settings_dict, "also_ring_delegate_btn")
    time.sleep(3)
    device_setting_back(device)
    device_setting_back(device)
    call_keywords.come_back_to_home_screen(device)


def device_back_from_tz(device):
    if config["devices"][device]["model"].lower() in ["Olympia"]:
        device_setting_back(device)
        device_setting_back(device)
    else:
        pass


def select_user_presence(device, state):
    if not state.lower() in ["available", "busy", "dnd", "be right back", "offline", "away", "reset_status"]:
        raise AssertionError(f"Illegal state specified: '{state}'")
    device, account = common.decode_device_spec(device)
    if common.is_lcp(device):
        common.wait_for_and_click(device, lcp_homescreen_dict, "homescreen_menu")
        common.wait_for_element(device, lcp_homescreen_dict, "user_current_status")
        common.wait_for_and_click(device, lcp_homescreen_dict, "status_drop_down_button")
    else:
        common.click_if_present(device, calls_dict, "Call_Back_Button")
        time.sleep(action_time)
        common.click_if_present(device, home_screen_dict, "home_bar_icon")
        common.wait_for_and_click(device, navigation_dict, "Navigation")
        common.wait_for_and_click(device, navigation_dict, "more_current_presence_btn")
    if state.lower() == "available":
        if config["devices"][device]["model"].lower() == "riverside":
            common.wait_for_element(device, navigation_dict, "default_presence_state")
        elif config["devices"][device]["model"].lower() == "olympia" and account == "cap_search_enabled":
            common.wait_for_element(device, navigation_dict, "default_presence_state")
        else:
            common.wait_for_and_click(device, navigation_dict, "Available")
    elif state.lower() == "busy":
        common.wait_for_and_click(device, navigation_dict, "Busy")
    elif state.lower() == "dnd":
        common.wait_for_and_click(device, navigation_dict, "Do_not_disturb")
    elif state.lower() == "be right back":
        common.wait_for_and_click(device, navigation_dict, "Be_right_back")
    elif state.lower() == "offline":
        if common.is_lcp(device):
            swipe_till_end(device)
        common.wait_for_and_click(device, navigation_dict, "Offline")
    elif state.lower() == "away":
        if common.is_lcp(device):
            swipe_till_end(device)
        common.wait_for_and_click(device, navigation_dict, "Away")
    elif state.lower() == "reset_status":
        if common.is_lcp(device):
            swipe_till_end(device)
        common.wait_for_and_click(device, navigation_dict, "reset_status")
    if common.is_lcp(device):
        common.wait_for_and_click(device, lcp_homescreen_dict, "more_cancel_button")
        return
    common.wait_for_and_click(device, settings_dict, "user_displayname")
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")


def verify_user_presence(device, state):
    if state.lower() not in ["available", "busy", "dnd", "be right back", "offline", "away", "in a call"]:
        print(f"Unexpected value for state: {state}")
    if common.is_lcp(device):
        common.wait_for_and_click(device, lcp_homescreen_dict, "homescreen_menu")
        common.wait_for_element(device, lcp_homescreen_dict, "user_current_status")
    else:
        common.click_if_present(device, home_screen_dict, "home_bar_icon")
        common.wait_for_and_click(device, navigation_dict, "Navigation")
    presence_text = common.wait_for_element(device, navigation_dict, "current_presence_label").text.lower()
    print("Current presence is : ", presence_text)
    if state.lower() != presence_text:
        if not (state.lower() == "dnd" and presence_text == "do not disturb"):
            raise AssertionError(
                f"expected presence value: {state} doesn't match the actual presence value: {presence_text}"
            )
    print(f"Selected presence on {device} is {presence_text}")
    if common.is_lcp(device):
        common.wait_for_and_click(device, lcp_homescreen_dict, "more_cancel_button")
        return
    common.wait_for_and_click(device, settings_dict, "user_displayname")
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")


def open_manage_delegate_page(device):
    common.wait_for_and_click(device, settings_dict, "manage_delegates")


def add_new_delegate(from_device, to_device, permission="All"):
    if not permission.lower() in ["make call", "receive call", "all"]:
        raise AssertionError(f"Illegal permission specified: '{permission}'")
    print("from_device :", from_device)

    username = common.device_displayname(to_device)
    print("username : ", username)
    time.sleep(display_time)
    if common.is_element_present(from_device, settings_dict, "user_title", "id"):
        delegate_user_list = common.get_all_elements_texts(from_device, settings_dict, "user_title", "id")
        if username in delegate_user_list:
            print(f"{username} is already added as a delegate")
            call_views_keywords.go_back_to_previous_page(from_device)
            return

    common.kb_trigger_search(from_device, settings_dict, "add_delegates", username)

    tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", username)
    common.wait_for_and_click(from_device, tmp_dict, "search_result_item_container", "xpath")
    elems = common.wait_for_element(
        from_device, settings_dict, "permission_switch", cond=EC.presence_of_all_elements_located
    )
    make_call = elems[0]
    receive_call = elems[1]
    if permission.lower() == "make call":
        elem_text = make_call.get_attribute("checked")
        if elem_text != "true":
            make_call.click()
            print("Make calls switch is turned ON")
        elem_text = receive_call.get_attribute("checked")
        if elem_text == "true":
            receive_call.click()
            print("Receive calls switch is turned OFF")

    elif permission.lower() == "receive call":
        elem_text = receive_call.get_attribute("checked")
        if elem_text != "true":
            receive_call.click()
            print("Receive calls is turned ON")
        elem_text = make_call.get_attribute("checked")
        if elem_text == "true":
            make_call.click()
            print("Make calls switch is turned OFF")
    elif permission.lower() == "all":
        if config["devices"][from_device]["model"].lower() == "gilbert":
            swipe_till_end(from_device)
        for elem in elems:
            elem_text = elem.get_attribute("checked")
            if elem_text != "true":
                elem.click()
        print("All the permission switches are ON")
    common.wait_for_and_click(from_device, settings_dict, "save_permissions")
    for i in range(2):
        common.click_if_present(from_device, calls_dict, "Call_Back_Button")


def validate_added_delegate_user_name(from_device, to_device):
    print("from_device :", from_device)
    time.sleep(action_time)
    if not common.is_element_present(from_device, settings_dict, "manage_delegates"):
        open_settings_page(from_device)
    common.wait_for_and_click(from_device, settings_dict, "manage_delegates")
    time.sleep(action_time)
    username = common.device_displayname(to_device)
    print("username : ", username)
    tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", username)
    common.wait_for_element(from_device, tmp_dict, "search_result_item_container", "xpath")
    print(f"{username} is successfully added as a delegate")
    common.wait_for_and_click(from_device, calls_dict, "Call_Back_Button")
    common.wait_for_and_click(from_device, calls_dict, "Call_Back_Button")
    call_keywords.navigate_to_calls_favorites_page(from_device)
    refresh_calls_main_tab(from_device)


def delete_delegate_from_manage_delegate(from_device, to_device):
    common.sleep_with_msg(from_device, 5, "Wait for the favorites page to load")
    if not call_keywords.verify_delegates_in_favorites_page(from_device):
        return
    refresh_calls_main_tab(from_device)
    open_settings_page(from_device)
    common.wait_for_and_click(from_device, settings_dict, "manage_delegates")
    devices = to_device.split(",")
    for device in devices:
        username = common.device_displayname(device)
        tmp_dict = common.get_dict_copy(settings_dict, "delegate_result_username", "username", username)
        time.sleep(action_time)
        refresh_main_tab(from_device)

        # Commenting this since it was a workaround for delegtes not appearing under manage delegates when navigated firt time to tab
        # if not common.is_element_present(from_device, tmp_dict, "delegate_result_username", "xpath"):
        #     common.wait_for_and_click(from_device, calls_dict, "Call_Back_Button")
        #     common.wait_for_and_click(from_device, settings_dict, "manage_delegates")

        common.wait_for_and_click(from_device, tmp_dict, "delegate_result_username")

        if config["devices"][from_device]["model"].lower() == "gilbert":
            swipe_till_end(from_device)
        common.wait_for_and_click(from_device, settings_dict, "delete_delegates", "xpath")
        # wait for manage_delegate tab post deleting a delegate
        common.wait_for_and_click(from_device, calls_dict, "Call_Back_Button")
        common.wait_for_and_click(from_device, settings_dict, "manage_delegates")

        common.wait_for_element(from_device, settings_dict, "manage_delegates")
        if common.is_element_present(from_device, tmp_dict, "delegate_result_username"):
            raise AssertionError(f"{username} was not removed from delegate")

        print(f"Successfully removed {username} from delegate user")
    for attempt in range(3):
        if not common.click_if_present(from_device, calls_dict, "Call_Back_Button"):
            break
        common.sleep_with_msg(from_device, 3, f"React to 'Call_Back_Button' click, attempt: {attempt}.")


def validate_user_should_not_be_able_to_add_self_as_delegate(device):
    open_settings_page(device)
    common.wait_for_and_click(device, settings_dict, "manage_delegates")
    common.wait_for_and_click(device, settings_dict, "add_delegates")
    username = config["devices"][device]["user"]["displayname"]
    print("username : ", username)
    common.wait_for_element(device, settings_dict, "add_delegates").send_keys(username)
    common.hide_keyboard(device)
    time.sleep(action_time)
    tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", username)
    if common.is_element_present(device, tmp_dict, "search_result_item_container", "xpath"):
        raise AssertionError("Self can be added as a delegate")
    print("Cannot add self as delegate")


def edit_delegate(from_device, to_device, permission="All"):
    if not permission.lower() in [
        "make call",
        "receive call",
        "change call and delegate settings",
        "join active calls",
        "pick up held calls",
        "all",
    ]:
        raise AssertionError(f"Illegal permission specified: '{permission}'")
    print("from_device :", from_device)
    username = common.device_displayname(to_device)
    tmp_dict = common.get_dict_copy(settings_dict, "delegate_result_username", "username", username)
    del_list = common.wait_for_element(from_device, tmp_dict, "delegate_result_username")
    del_list.click()
    time.sleep(action_time)
    elems = common.wait_for_element(
        from_device, settings_dict, "permission_switch", cond=EC.presence_of_all_elements_located
    )
    make_call = elems[0]
    receive_call = elems[1]
    change_call_and_delegate_settings = elems[2]
    join_active_calls = elems[3]
    pick_up_held_calls = elems[4]
    if permission.lower() == "make call":
        elem_text = make_call.get_attribute("checked")
        if elem_text == "true":
            print("Make calls switch is already ON")
        else:
            make_call.click()
            print("Make calls switch is turned ON")
        for elem in elems:
            elem_text = elem.get_attribute("checked")
            elem_index = elems.index(elem)
            if elem_index != 0:
                if elem_text != "false":
                    elem.click()
        print("All the other permission switches are OFF")
    elif permission.lower() == "receive call":
        elem_text = receive_call.get_attribute("checked")
        if elem_text == "true":
            print("Receive calls switch is already ON")
        else:
            receive_call.click()
            print("Receive calls switch is turned ON")
        for elem in elems:
            elem_text = elem.get_attribute("checked")
            elem_index = elems.index(elem)
            if elem_index != 1:
                if elem_text != "false":
                    elem.click()
        print("All the other permission switches are OFF")
    elif permission.lower() == "change call and delegate settings":
        elem_text = change_call_and_delegate_settings.get_attribute("checked")
        if elem_text == "true":
            print("Change call and delegate settings switch is already ON")
        else:
            change_call_and_delegate_settings.click()
            print("Change call and delegate settings switch is turned ON")
        for elem in elems:
            elem_text = elem.get_attribute("checked")
            elem_index = elems.index(elem)
            if elem_index != 2:
                if elem_text != "false":
                    elem.click()
        print("All the other permission switches are OFF")
    elif permission.lower() == "join active calls":
        elem_text = join_active_calls.get_attribute("checked")
        if elem_text == "true":
            print("Join active calls switch is already ON")
        else:
            join_active_calls.click()
            print("Join active calls switch is turned ON")
        for elem in elems:
            elem_text = elem.get_attribute("checked")
            elem_index = elems.index(elem)
            if elem_index != 3:
                if elem_text != "false":
                    elem.click()
        print("All the other permission switches are OFF")
    elif permission.lower() == "pick up held calls":
        elem_text = pick_up_held_calls.get_attribute("checked")
        if elem_text == "true":
            print("Pick up held calls switch is already ON")
        else:
            pick_up_held_calls.click()
            print("Pick up held calls switch is turned ON")
        for elem in elems:
            elem_text = elem.get_attribute("checked")
            elem_index = elems.index(elem)
            if elem_index != 4:
                if elem_text != "false":
                    elem.click()
        print("All the other permission switches are OFF")
    elif permission.lower() == "all":
        for elem in elems:
            elem_text = elem.get_attribute("checked")
            if elem_text != "true":
                elem.click()
        print("All the permission switches are ON")
    common.click_if_present(from_device, settings_dict, "save_permissions")
    common.wait_for_and_click(from_device, calls_dict, "Call_Back_Button")


def verify_user_unable_to_toggle_the_permissions(device):
    permission_titles_list = common.wait_for_element(
        device, settings_dict, "delegate_permissions", cond=EC.presence_of_all_elements_located
    )
    permission_switches_list = common.wait_for_element(
        device, settings_dict, "permission_switch", cond=EC.presence_of_all_elements_located
    )
    switch_status_before_toggling = []
    switch_status_after_toggling = []
    for i in range(len(permission_switches_list)):
        switch_status_before_toggling.append(permission_switches_list[i].get_attribute("checked"))
        permission_switches_list[i].click()
        switch_status_after_toggling.append(permission_switches_list[i].get_attribute("checked"))
    if switch_status_before_toggling != switch_status_after_toggling:
        raise AssertionError(
            f"{device}: User is able to toggle the permissions\nPermission titles: {permission_titles_list}\nExpected permission list: {switch_status_before_toggling}\nActual permission list: {switch_status_after_toggling}"
        )


def navigate_to_change_delegates_page(device):
    call_keywords.navigate_to_calls_favorites_page(device)
    common.wait_for_and_click(device, calls_dict, "favorites_more_options")
    common.wait_for_element(device, settings_dict, "view_permissions_xpath")
    common.wait_for_and_click(device, calls_dict, "change_delegates")
    common.wait_for_element(device, settings_dict, "add_delegates")


def click_device_center_point(device):
    devices = device.split(",")
    for device in devices:
        time.sleep(action_time)
        driver = obj.device_store.get(alias=device)
        window_size = driver.get_window_size()
        height = window_size["height"]
        print("Window Height :", height)
        width = window_size["width"]
        print("Window Width :", width)
        subprocess.call(
            "adb -s {} shell input tap {} {}".format(
                config["devices"][device]["desired_caps"]["udid"].split(":")[0], width / 2, height / 2
            ),
            shell=True,
        )
        time.sleep(display_time)
        print("Tapped co-ordinates : ", width / 2, height / 2)


def enable_home_screen(device):
    print("device :", device)
    home_screen_toggle_btn = common.wait_for_element(
        device, settings_dict, "home_screen_toggle_btn", cond=EC.element_to_be_clickable
    )
    toggle_text = home_screen_toggle_btn.text
    print(f"{device}: Home screen option text currently: '{toggle_text}'")
    if toggle_text == "OFF":
        home_screen_toggle_btn.click()
        time.sleep(action_time)
        print(f"{device}: Clicked on Home Screen toggle_btn button")
        common.wait_for_and_click(device, settings_dict, "restart_btn")
        time.sleep(10)
    elif toggle_text == "ON":
        print(f"{device}: Homescreen is already enabled on the device, continuing ..")
        common.wait_for_and_click(device, calls_dict, "Call_Back_Button")
        home_screen_keywords.come_back_to_home_screen_page_and_verify(device)
    else:
        raise AssertionError(f"{device}: Invalid toggle text")


def disable_home_screen(device):
    print("device :", device)
    home_screen_toggle_btn = common.wait_for_element(
        device, settings_dict, "home_screen_toggle_btn", cond=EC.element_to_be_clickable
    )
    toggle_text = home_screen_toggle_btn.text
    print(f"{device}: Home screen option text currently: '{toggle_text}'")
    if toggle_text == "ON":
        home_screen_toggle_btn.click()
        print(f"{device}: Clicked on Home screen button")
        common.wait_for_and_click(device, settings_dict, "restart_btn")
        time.sleep(10)
    elif toggle_text == "OFF":
        print("Homescreen is already disabled on the device, continuing ..")
        common.wait_for_and_click(device, calls_dict, "Call_Back_Button")
        call_keywords.navigate_to_calls_tab(device)
    else:
        raise AssertionError(f"{device}: Invalid toggle text")


def verify_home_screen_status(device, status):
    if status.lower() not in ["on", "off"]:
        raise AssertionError(f"Illegal value for 'status': '{status}'")
    print(f"{device}: verify_home_screen_status={status}")
    if status.lower() == "off":
        common.wait_for_element(device, calls_dict, "recent_tab")
    elif status.lower() == "on":
        # Homescreen is enabled, but user is on different tab
        common.click_if_present(device, home_screen_dict, "home_bar_icon")
        common.wait_for_element(device, calls_dict, "user_profile_picture")


def navigate_to_device_setting_page_from_home_screen_enable_page(device):
    print("device :", device)
    if common.is_lcp(device):
        common.wait_for_and_click(device, lcp_homescreen_dict, "homescreen_menu")
        common.wait_for_and_click(device, lcp_homescreen_dict, "settings_icon")
        swipe_till_end(device)
        swipe_till_end(device)
        click_device_settings(device)
        return
    common.wait_for_and_click(device, calls_dict, "user_profile_picture", wait_attempts=60)
    common.wait_for_and_click(device, navigation_dict, "Settings_button")
    time.sleep(action_time)
    click_device_settings(device)


def navigate_to_app_setting_page_from_home_screen(device):
    print("device :", device)
    if common.is_lcp(device):
        common.wait_for_and_click(device, lcp_homescreen_dict, "homescreen_menu")
        common.wait_for_and_click(device, lcp_homescreen_dict, "settings_icon")
        swipe_till_end(device)
        swipe_till_end(device)
        return
    common.wait_for_and_click(device, calls_dict, "user_profile_picture", wait_attempts=60)
    common.wait_for_and_click(device, navigation_dict, "Settings_button")
    time.sleep(action_time)
    print("Clicked on settings option")


def swipe_left(device):
    driver = obj.device_store.get(alias=device)
    window_size = driver.get_window_size()
    print("Window size: ", window_size)
    height = window_size["height"]
    print("Window Height :", height)
    width = window_size["width"]
    print("Window Width :", width)
    if height > width:
        print("Swiping co-ordinates : ", (3 * (width / 4), height / 2, 50, height / 2))
        driver.swipe(3 * (width / 4), height / 2, 50, height / 2)
    else:
        print("Swiping co-ordinates : ", (width / 3, height / 2, 50, height / 2))
        driver.swipe(width / 3, height / 2, 50, height / 2)


def enable_notification(device):
    toggle_button = common.wait_for_element(device, settings_dict, "notification_toggle")
    toggle_btn_state = toggle_button.get_attribute("checked")
    if toggle_btn_state.lower() == "false":
        common.wait_for_and_click(device, settings_dict, "notification_toggle")
        toggle_button = common.wait_for_element(device, settings_dict, "notification_toggle")
        toggle_btn_state = toggle_button.get_attribute("checked")
        if toggle_btn_state.lower() != "true":
            raise AssertionError(f"{device}: Cannot change the notification toggle status: {toggle_button}")
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")


def disable_notification(device):
    toggle_button = common.wait_for_element(device, settings_dict, "notification_toggle")
    toggle_btn_state = toggle_button.get_attribute("checked")
    if toggle_btn_state.lower() == "true":
        common.wait_for_and_click(device, settings_dict, "notification_toggle")
        toggle_button = common.wait_for_element(device, settings_dict, "notification_toggle")
        toggle_btn_state = toggle_button.get_attribute("checked")
        if toggle_btn_state.lower() != "false":
            raise AssertionError(f"{device}: Cannot change the notification toggle status: {toggle_button}")
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")


def verify_notification_status(device, status):
    if status.lower() not in ["on", "off"]:
        raise AssertionError(f"Illegal value for 'status': '{status}'")
    print("device :", device)
    time.sleep(display_time)
    if status.lower() == "off":
        if common.is_element_present(device, home_screen_dict, "notification_view"):
            raise AssertionError("Still notifications are visible on homescreen")
        print("Notifications are not visible on homescreen")
    elif status.lower() == "on":
        common.wait_for_element(device, home_screen_dict, "notification_view")


def verify_signin_with_invalid_user(device, user=None):
    invalid_username = config["user"]["invalid_username"]
    time.sleep(6)
    if common.is_element_present(device, sign_dict, "refresh_code_button"):
        common.wait_for_and_click(device, sign_dict, "refresh_code_button")
        common.sleep_with_msg(device, 5, "Allow refresh of DFC code")
    common.wait_for_element(device, sign_dict, "dfc_login_code")
    common.wait_for_and_click(device, sign_dict, "sign_in_on_the_device")

    common.wait_for_and_click(device, sign_dict, "Username")
    common.wait_for_element(device, sign_dict, "Username").send_keys(invalid_username)
    print(f"{device} entered the invalid username '{invalid_username}'")

    common.wait_for_and_click(device, sign_dict, "Sign_in_button")

    # Username passed to CP, which might take several seconds:
    # On few devices, the password page elements are not accessible
    # if "console" not in device:
    #     if config["devices"][device]["model"].lower() in [
    #         "seattle",
    #         "tacoma",
    #         "redmond",
    #         "manhattan",
    #         "kirkland",
    #     ]:
    #         common.sleep_with_msg(device, 30, "Waiting to manually tap on 'Next' button")
    #         udid_ = config["devices"][device]["desired_caps"]["udid"]
    #         subprocess.run(
    #             "adb -s " + udid_ + " shell input keyevent KEYCODE_ENTER",
    #             stdout=subprocess.PIPE,
    #             shell=True,
    #         )
    #     else:
    #         common.wait_for_and_click(device, sign_dict, "Next_button")
    # else:
    #     common.wait_for_and_click(device, sign_dict, "Next_button")
    common.wait_for_and_click(device, sign_dict, "Next_button")
    common.sleep_with_msg(device, 5, "Allow soft keyboard to appear")
    if "console" not in device:
        if config["devices"][device]["model"].lower() not in ["spokane", "sammamish"]:
            common.hide_keyboard(device)
    invalid_username_error = common.wait_for_element(device, sign_dict, "invalid_username_error").text
    invalid_username_error_list = [
        "This username may be incorrect. Make sure that you typed it correctly. Otherwise, contact your admin.",
        "This username may be incorrect. Make sure you typed it correctly. Otherwise, contact your admin.",
    ]
    if invalid_username_error not in invalid_username_error_list:
        raise AssertionError(
            f"{device}: Expected error message is not displayed for invalid username: {invalid_username_error}"
        )
    common.wait_for_and_click(device, tr_Signin_dict, "sign_back")


def verify_signin_with_invalid_domain(device, user=None):
    invalid_domain = config["user"]["invalid_domain"]
    time.sleep(6)
    if common.is_element_present(device, sign_dict, "refresh_code_button"):
        common.wait_for_and_click(device, sign_dict, "refresh_code_button")
        common.sleep_with_msg(device, 5, "Allow refresh of DFC code")
    common.wait_for_element(device, sign_dict, "dfc_login_code")
    common.wait_for_and_click(device, sign_dict, "sign_in_on_the_device")
    common.wait_for_and_click(device, sign_dict, "Username")
    search_input = common.wait_for_element(device, sign_dict, "Username")
    search_input.send_keys(invalid_domain)
    print(f"{device} entered the invalid username '{invalid_domain}'")
    if "console" not in device:
        if config["devices"][device]["model"].lower() not in ["spokane", "sammamish"]:
            common.hide_keyboard(device)

    common.wait_for_and_click(device, sign_dict, "Sign_in_button")
    error_text = common.wait_for_element(device, sign_dict, "invalid_domain_error").text
    error_text_list = [
        "Couldn’t connect to Workplace Join. Try again, or contact your admin.",
        "You’ll need to sign in with a work account.",
        "Please enter a valid sign-in address.",
    ]
    if error_text not in error_text_list:
        raise AssertionError(f"{device}: Couldn't find the invalid domain name error")


def verify_signin_with_wrong_password(device, user=None):
    if "console" in device:
        username = config["consoles"][device]["user"]["username"]
    else:
        username = config["devices"][device]["user"]["username"]
    wrong_password = config["user"]["invalid_password"]
    time.sleep(6)
    if common.is_element_present(device, sign_dict, "refresh_code_button"):
        common.wait_for_and_click(device, sign_dict, "refresh_code_button")
        common.sleep_with_msg(device, 5, "Allow refresh of DFC code")
    common.wait_for_element(device, sign_dict, "dfc_login_code")
    common.wait_for_and_click(device, sign_dict, "sign_in_on_the_device")
    common.wait_for_and_click(device, sign_dict, "Username")
    search_input = common.wait_for_element(device, sign_dict, "Username")
    search_input.send_keys(username)
    print("Entered username")
    if "console" not in device:
        if config["devices"][device]["model"].lower() not in ["spokane", "sammamish"]:
            common.hide_keyboard(device)

    common.wait_for_and_click(device, sign_dict, "Sign_in_button")

    if "console" not in device:
        # Manually tapping on the password field on devices where password screen is not visible
        if config["devices"][device]["model"].lower() in [
            "olympia",
            "seattle",
            "tacoma",
            "redmond",
            "manhattan",
            "kirkland",
        ]:
            common.sleep_with_msg(device, 40, "Waiting for the password entry screen to appear")
            udid_ = config["devices"][device]["desired_caps"]["udid"]
            try:
                if config["devices"][device]["model"].lower() in ["olympia", "seattle", "tacoma", "kirkland"]:
                    subprocess.run("adb -s " + udid_ + " shell input tap 100 450", stdout=subprocess.PIPE, shell=True)
                elif config["devices"][device]["model"].lower() == "redmond":
                    subprocess.run("adb -s " + udid_ + " shell input tap 400 330", stdout=subprocess.PIPE, shell=True)
                elif config["devices"][device]["model"].lower() == "manhattan":
                    subprocess.run("adb -s " + udid_ + " shell input tap 600 430", stdout=subprocess.PIPE, shell=True)
                common.sleep_with_msg(device, 7, f"Waiting to enter password on {device}")
                cmd = "adb -s " + udid_ + " shell input text " + wrong_password
                subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
                subprocess.run(
                    "adb -s " + udid_ + " shell input keyevent KEYCODE_ENTER",
                    stdout=subprocess.PIPE,
                    shell=True,
                )
                print(f"{device}: Manually entered the wrong password")
            except CalledProcessError as failure:
                print(f"{device}: Failed ({failure.returncode}) manual input of the wrong password: {failure.output}")
                raise AssertionError("Manual password entry failed.")
        else:
            common.wait_for_element(device, sign_dict, "Password").send_keys(wrong_password)
    else:
        common.wait_for_element(device, sign_dict, "Password").send_keys(wrong_password)
        print(f"{device}: entered the wrong password")

    if not common.click_if_present(device, sign_dict, "Sign_in"):
        common.wait_for_and_click(device, sign_dict, "signin_button")

    common.wait_for_element(device, sign_dict, "invalid_password_error")


def navigate_to_manage_delegate_page(device):
    open_settings_page(device)
    common.wait_for_and_click(device, settings_dict, "manage_delegates")


def validate_view_permissions_option(from_device, to_device):
    to_device_displayname = common.device_displayname(to_device)
    temp_dict = common.get_dict_copy(settings_dict, "user_title", "user_name", to_device_displayname)
    common.wait_for_and_click(from_device, temp_dict, "user_title")
    select_permission(from_device, permission="View Permissions")
    validate_call_permissions(from_device)
    call_keywords.come_back_to_home_screen(from_device)


def validate_permissions_for_people_you_support(from_device, to_device):
    to_device_displayname = common.device_displayname(to_device)
    temp_dict = common.get_dict_copy(settings_dict, "user_title", "user_name", to_device_displayname)
    common.wait_for_and_click(from_device, temp_dict, "user_title")
    validate_call_permissions(from_device)
    common.return_to_home_screen(from_device)


def validate_change_delegates_option(from_device, to_device):
    to_device_displayname = common.device_displayname(to_device)
    temp_dict = common.get_dict_copy(settings_dict, "user_title", "user_name", to_device_displayname)
    common.wait_for_and_click(from_device, temp_dict, "user_title")
    select_permission(from_device, permission="Change delegates")


def validate_change_call_settings_option_and_enable_call_forward(from_device, to_device, contact_device):
    to_device_displayname = common.device_displayname(to_device)
    temp_dict = common.get_dict_copy(settings_dict, "user_title", "user_name", to_device_displayname)
    common.wait_for_and_click(from_device, temp_dict, "user_title")
    select_permission(from_device, permission="Change call settings")
    pstn_displayname = config["devices"][contact_device]["user"]["pstndisplay"]
    phonenumber = config["devices"][contact_device]["user"]["phonenumber"]
    common.wait_for_and_click(from_device, settings_dict, "Call_forward_toggle")
    common.wait_for_and_click(from_device, settings_dict, "forward_option_btn")
    common.wait_for_and_click(from_device, settings_dict, "contact_option")
    common.wait_for_and_click(from_device, settings_dict, "add_contact_option")
    common.wait_for_element(from_device, settings_dict, "search_contact_box").send_keys(phonenumber)
    common.hide_keyboard(from_device)
    temp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", pstn_displayname)
    common.wait_for_and_click(from_device, temp_dict, "search_result_item_container")
    device_setting_back(from_device)


def select_permission(device, permission):
    if not permission.lower() in ["view permissions", "change delegates", "change call settings"]:
        raise AssertionError(f"Illegal permission specified: '{permission}'")
    common.wait_for_element(device, settings_dict, "view_permissions_xpath")
    common.wait_for_element(device, settings_dict, "change_delegates_xpath")
    common.wait_for_element(device, settings_dict, "change_call_settings_xpath")
    if permission.lower() == "view permissions":
        common.wait_for_and_click(device, settings_dict, "view_permissions_xpath")
    elif permission.lower() == "change delegates":
        common.wait_for_and_click(device, settings_dict, "change_delegates_xpath")
    elif permission.lower() == "change call settings":
        common.wait_for_and_click(device, settings_dict, "change_call_settings_xpath")


def validate_call_permissions(device):
    common.wait_for_element(device, settings_dict, "make_calls_xpath")
    common.wait_for_element(device, settings_dict, "receive_calls_xpath")
    common.wait_for_element(device, settings_dict, "change_call_xpath")
    common.wait_for_element(device, settings_dict, "join_active_calls")
    common.wait_for_element(device, settings_dict, "pick_up_held_calls")


def validate_change_call_settings_option_and_validate_also_ring(from_device, to_device):
    to_device_displayname = common.device_displayname(to_device)
    temp_dict = common.get_dict_copy(settings_dict, "user_title", "user_name", to_device_displayname)
    common.wait_for_and_click(from_device, temp_dict, "user_title")
    select_permission(from_device, permission="Change call settings")
    common.wait_for_and_click(from_device, settings_dict, "also_ring_btn")
    common.wait_for_element(from_device, settings_dict, "also_ring_off_btn")
    common.wait_for_element(from_device, settings_dict, "contact_option")
    common.wait_for_element(from_device, settings_dict, "also_ring_delegate_btn")


def select_change_call_settings_permission(device):
    common.wait_for_and_click(device, calls_dict, "favorites_more_options")
    select_permission(device, permission="Change call settings")


def validate_if_unanswered_in_people_you_support_page(from_device, to_device):
    to_device_displayname = common.device_displayname(to_device)
    temp_dict = common.get_dict_copy(settings_dict, "user_title", "user_name", to_device_displayname)
    common.wait_for_and_click(from_device, temp_dict, "user_title")
    select_permission(from_device, permission="Change call settings")
    common.wait_for_and_click(from_device, settings_dict, "unanswered_btn")
    common.wait_for_element(from_device, settings_dict, "unanswerd_off")
    common.wait_for_element(from_device, settings_dict, "voicemail_option")
    common.wait_for_element(from_device, settings_dict, "contact_option")
    common.wait_for_element(from_device, settings_dict, "also_ring_call_group_btn")
    common.wait_for_element(from_device, settings_dict, "also_ring_delegate_btn")


def verify_user_presence_from_other_user(from_device, to_device, state):
    if state.lower() not in ["in call", "available", "busy", "dnd", "be right back", "offline", "away"]:
        raise AssertionError(f"Unexpected value for option : {state}")
    print(f"Arguments: {from_device}, {to_device}, {state}")
    to_device, account = common.decode_device_spec(to_device)
    to_device_displayname = config["devices"][to_device][account]["displayname"]
    to_device_username = config["devices"][to_device][account]["username"].split("@")[0]
    common.return_to_home_screen(from_device)
    people_keywords.click_on_people_tab(from_device)
    if common.is_lcp(from_device):
        common.wait_for_and_click(from_device, calls_dict, "search_icon")
    else:
        common.wait_for_and_click(from_device, calls_dict, "search")
    element = common.wait_for_element(from_device, calls_dict, "search_text")
    element.send_keys(to_device_username)
    time.sleep(display_time)
    common.hide_keyboard(from_device)
    search_result_xpath = common.get_dict_copy(
        calls_dict, "search_result_item_container", "config_display", to_device_displayname
    )
    if common.is_lcp(from_device):
        common.wait_for_element(from_device, search_result_xpath, "search_result_item_container", "xpath")
    else:
        common.wait_for_and_click(from_device, search_result_xpath, "search_result_item_container", "xpath")
    if state.lower() == "in call":
        presence_xpath = common.get_dict_copy(
            settings_dict, "in_call_presence_xpath", "username", to_device_displayname
        )
        common.wait_for_element(from_device, presence_xpath, "in_call_presence_xpath", wait_attempts=180)
    elif state.lower() == "available":
        presence_xpath = common.get_dict_copy(
            settings_dict, "available_presence_xpath", "username", to_device_displayname
        )
        common.wait_for_element(from_device, presence_xpath, "available_presence_xpath", wait_attempts=180)
    elif state.lower() == "busy":
        presence_xpath = common.get_dict_copy(settings_dict, "busy_presence_xpath", "username", to_device_displayname)
        common.wait_for_element(from_device, presence_xpath, "busy_presence_xpath")
    elif state.lower() == "dnd":
        presence_xpath = common.get_dict_copy(settings_dict, "dnd_presence_xpath", "username", to_device_displayname)
        common.wait_for_element(from_device, presence_xpath, "dnd_presence_xpath", wait_attempts=180)
    elif state.lower() == "be right back":
        presence_xpath = common.get_dict_copy(
            settings_dict, "be_right_back_presence_xpath", "username", to_device_displayname
        )
        common.wait_for_element(from_device, presence_xpath, "be_right_back_presence_xpath")
    elif state.lower() == "offline":
        presence_xpath = common.get_dict_copy(
            settings_dict, "offline_presence_xpath", "username", to_device_displayname
        )
        common.wait_for_element(from_device, presence_xpath, "offline_presence_xpath", wait_attempts=180)
    elif state.lower() == "away":
        presence_xpath = common.get_dict_copy(settings_dict, "away_presence_xpath", "username", to_device_displayname)
        common.wait_for_element(from_device, presence_xpath, "away_presence_xpath")
    common.return_to_home_screen(from_device)


def traverse_to_settings_notification(device):
    # Click if home screen is not enabled on device or the home screen is enabled, but user is on different tab
    if not common.click_if_present(device, navigation_dict, "Navigation"):
        # If the home screen is already enabled on the device, user's profile picture will be visible
        common.wait_for_and_click(device, calls_dict, "user_profile_picture")
    common.wait_for_and_click(device, navigation_dict, "Settings_button")
    time.sleep(action_time)


def disable_call_forwarding_and_verify(device):
    print(f"disable_call_forwarding_and_verify('{device}')")
    open_settings_page(device)
    disable_call_forwarding(device)
    call_keywords.come_back_to_home_screen(device, disconnect=False)


def verify_and_change_call_settings(device):
    open_settings_page(device)
    set_call_forwarding(device, "OFF")
    verify_and_change_busy_on_busy_settings(device)
    common.click_if_present(device, calls_dict, "Call_Back_Button")
    device_setting_back(device)
    common.click_if_present(device, device_settings_dict, "admin_settings_yes")
    device_setting_back(device)
    common.click_if_present(device, calls_dict, "Call_Back_Button")


def verify_and_change_busy_on_busy_settings(device):
    common.sleep_with_msg(device, 5, "Waiting for 'calling' page to load")
    if not common.is_element_present(device, calls_dict, "when_in_another_call"):
        print(f"*WARN*:: {device} doesn't have 'when in another call' option under 'calling' tab")
        return
    common.wait_for_element(device, calls_dict, "when_in_another_call")
    if not common.is_element_present(device, calls_dict, "new_calls_ring_me"):
        common.wait_for_and_click(device, calls_dict, "when_in_another_call")
        common.wait_for_and_click(device, calls_dict, "new_calls_ring_me")
    common.wait_for_and_click(device, common_dict, "back")
    common.wait_for_element(device, settings_dict, "Calling")


def navigate_back_once(device):
    print("device :", device)
    subprocess.call(
        "adb -s {} shell input keyevent 4".format(config["devices"][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    pass


if __name__ == "__main__":
    #
    # Standalone testing of methods in this file.
    # (may require changes to "PYTHONPATH")
    #

    # Enable workarounds:
    StandaloneTesting = True

    # Run some tests
    try:
        get_screenshot("one_device", "device1")
        get_screenshot("defaults")
        get_screenshot("noXML", with_xml=False)
        get_screenshot({"xx": "bb"})
        get_screenshot(None)
        get_screenshot("badList", device_list={"xx": "bb"})
        get_screenshot("badBool", with_xml="XFalse")
        print("All good, no exceptions from 'get_screenshot()'")
    except Exception as e:
        print(f"ERROR! Unexpected Exception: {e}")


def verify_presence_feature(device):
    print("device :", device)
    if common.is_portrait_mode_cnf_device(device):
        status = "fail"
    else:
        status = "pass"
    return status


def verify_appearance_button_for_conference_devices(device):
    if common.is_portrait_mode_cnf_device(device):
        print(f"Feature not applicable: Skipping verifications on portrait mode devices")
        return
    common.wait_for_and_click(device, settings_dict, "Appearance_btn")
    common.wait_for_element(device, settings_dict, "dark_theme")


def verify_options_under_settings_for_cnf_device(device):
    print("device :", device)
    common.wait_for_element(device, settings_dict, "profile_btn")
    common.wait_for_element(device, settings_dict, "auto_restart")
    common.wait_for_element(device, settings_dict, "send_feedback")
    common.wait_for_element(device, settings_dict, "about_btn")
    common.wait_for_element(device, settings_dict, "Device_Settings")


def verify_appearance_option(device):
    print("device :", device)
    if common.is_portrait_mode_cnf_device(device):
        status = "fail"
    else:
        status = "pass"
    return status


def verify_cancel_button_and_validate_not_to_enable_advance_calling(device):
    open_settings_page(device)
    _max_attempts = 3
    for _attempt in range(_max_attempts):
        if common.is_element_present(device, settings_dict, "Device_Settings"):
            common.wait_for_and_click(device, settings_dict, "Device_Settings")
            break
        else:
            swipe_till_end(device)
    device_settings_keywords.advance_calling_option_oem(device)
    common.wait_for_and_click(device, settings_dict, "adv_call_toggle_btn")
    print(f"{device}: Clicked on Advance calling toggle button")
    common.wait_for_element(device, settings_dict, "adv_call_restart_btn")
    common.wait_for_and_click(device, settings_dict, "adv_call_cancel_btn")
    print(
        f"{device} : Acknowledge window is displayed stating You'll need to restart the app to apply changes with Cancel and Restart button"
    )
    common.wait_for_element(device, settings_dict, "adv_call_toggle_btn")
    device_setting_back(device)
    device_setting_back(device)
    time.sleep(action_time)
    common.click_if_present(device, device_settings_dict, "admin_settings_yes")
    device_setting_back(device)
    common.click_if_present(device, calls_dict, "Call_Back_Button")
    time.sleep(display_time)
    if not common.is_element_present(device, home_screen_dict, "call_tab"):
        common.wait_for_element(device, calls_dict, "dialpad_tab")


def verify_cap_premium_calling_setting_options(device):
    open_settings_page(device)
    swipe_till_end(device)
    swipe_till_end(device)
    common.wait_for_and_click(device, settings_dict, "Device_Settings")
    device_settings_keywords.advance_calling_option_oem(device)
    common.wait_for_element(device, settings_dict, "call_forwarding")
    common.wait_for_element(device, settings_dict, "also_ring")
    device_setting_back(device)
    device_setting_back(device)
    device_setting_back(device)


def verify_and_enable_advance_calling_option(device):
    print(f"device : {device}")
    if common.is_lcp(device):
        for i in range(10):
            if common.is_element_present(device, lcp_homescreen_dict, "homescreen_menu"):
                break
            common.sleep_with_msg(device, 1, "Waiting for sign-in to complete")
    set_advance_calling(device, "ON")
    time.sleep(3)
    common.wait_for_element(device, home_screen_dict, "people_tab")
    disable_call_forwarding_and_verify(device)


def disable_advance_calling_option(device):
    set_advance_calling(device, "OFF")


def set_advance_calling(device, status):
    if status.lower() not in ["on", "off"]:
        raise AssertionError(f"Illegal value for 'status': '{status}'")
    print(f"device : {device}")
    open_settings_page(device)
    _max_attempts = 5
    for _attempt in range(_max_attempts):
        if common.is_element_present(device, settings_dict, "Device_Settings"):
            common.wait_for_and_click(device, settings_dict, "Device_Settings")
            break
        else:
            swipe_till_end(device)
    device_settings_keywords.advance_calling_option_oem(device)
    adv_call_toggle_button = common.wait_for_element(device, settings_dict, "adv_call_toggle_btn")
    adv_call_toggle_status = adv_call_toggle_button.get_attribute("checked")
    print(f"{device}: Advance calling option status currently: '{adv_call_toggle_status}'")
    if status == "ON":
        state = "true"
    elif status == "OFF":
        state = "false"
    if adv_call_toggle_status == state:
        print(f"{device}: Advance calling Option status is already: {adv_call_toggle_status}")
    else:
        adv_call_toggle_button.click()
        print(f"{device}: Clicked on Advance calling option toggle button")
        common.wait_for_element(device, settings_dict, "adv_call_cancel_btn")
        common.wait_for_and_click(device, settings_dict, "adv_call_restart_btn")
        print(f"{device}: Clicked on Restart button")
    time.sleep(10)
    if common.is_lcp(device):
        print(f"{device}: already in home screen")
    else:
        call_keywords.come_back_to_home_screen(device)
    time.sleep(display_time)
    if not (
        common.is_element_present(device, home_screen_dict, "call_tab")
        or common.is_element_present(device, lcp_homescreen_dict, "forward_screen_menu")
    ):
        common.wait_for_element(device, calls_dict, "dialpad_tab")


def verify_advance_calling_toggle_status_for_cap(device, toggle):
    if not common.click_if_element_appears(device, settings_dict, "hotline_settings_btn", max_attempts=5):
        open_settings_page(device)
        swipe_till_end(device)
        swipe_till_end(device)
        common.wait_for_and_click(device, settings_dict, "Device_Settings")
    device_settings_keywords.advance_calling_option_oem(device)
    common.verify_toggle_button(device, settings_dict, "adv_call_toggle_btn", desired_state=toggle)
    call_keywords.come_back_to_home_screen(device)


def change_delegate_of_delegate_user(from_device, to_device, add_device):
    navigate_to_manage_delegate_page(from_device)
    common.return_to_home_screen(from_device)
    call_keywords.navigate_to_calls_favorites_page(from_device)
    common.wait_for_element(from_device, calls_dict, "contacts_grid")
    delegate_username = common.device_displayname(to_device)
    temp_dict = common.get_dict_copy(calls_dict, "favorites_more_options", "user_name", delegate_username)
    common.wait_for_and_click(from_device, temp_dict, "favorites_more_options", "xpath")
    common.wait_for_and_click(from_device, settings_dict, "change_delegates_xpath")
    add_delegate_displayname = common.device_displayname(add_device)
    common.wait_for_element(from_device, settings_dict, "add_delegates").send_keys(add_delegate_displayname)
    subprocess.call(
        "adb -s {} shell input keyevent 66".format(
            config["devices"][from_device]["desired_caps"]["udid"].split(":")[0]
        ),
        shell=True,
    )
    subprocess.call(
        "adb -s {} shell input keyevent 67".format(
            config["devices"][from_device]["desired_caps"]["udid"].split(":")[0]
        ),
        shell=True,
    )
    common.wait_for_and_click(from_device, calls_dict, "search_result_name")
    common.wait_for_and_click(from_device, settings_dict, "change_call_and_delegate_setting_toggle_off")
    if common.is_element_present(from_device, settings_dict, "change_call_and_delegate_setting_toggle_off"):
        raise AssertionError(f"{from_device} permission toggle not changed")
    common.wait_for_and_click(from_device, settings_dict, "save_permissions")
    time.sleep(sleep_time)
    users = common.get_all_elements_texts(from_device, settings_dict, "user_title")
    if add_delegate_displayname not in users:
        raise AssertionError(f"{to_device} is not added in delegate user")
    click_back(from_device)


def verify_auto_restart_option_inside_settings_page(device):
    _max_attempts = 3
    for i in range(_max_attempts):
        if common.is_element_present(device, settings_dict, "auto_restart"):
            break
        calendar_keywords.scroll_only_once(device)
        time.sleep(3)
    common.wait_for_element(device, settings_dict, "auto_restart")


def verify_app_restart_toggle(device, toggle):
    if toggle.lower() not in ["on", "off"]:
        raise AssertionError(f"Illegal value for 'toggle': '{toggle}'")
    common.wait_for_and_click(device, settings_dict, "auto_restart")
    common.wait_for_element(device, settings_dict, "app_restart")
    common.verify_toggle_button(device, settings_dict, "app_restart_toggle_btn", toggle)


def click_on_toggle_btn(device, status):
    if status.lower() not in ["on", "off"]:
        raise AssertionError(f"Illegal value for 'status': '{status}'")
    common.wait_for_and_click(device, settings_dict, "auto_restart")
    common.wait_for_element(device, settings_dict, "app_restart")
    common.change_toggle_button(device, settings_dict, "app_restart_toggle_btn", status)
    common.verify_toggle_button(device, settings_dict, "app_restart_toggle_btn", status)


def verify_options_after_enabling_auto_restart_toggle_btn(device):
    common.wait_for_element(device, settings_dict, "automatically_toggle_btn")


def verify_options_after_disabling_automatically_toggle_btn(device):
    common.wait_for_element(device, settings_dict, "daily")


def disable_automatically_toggle_btn_inside_app_restart(device):
    common.wait_for_and_click(device, settings_dict, "automatically_toggle_btn")


def verify_conf_room_UI_feature(device):
    print("device :", device)
    if common.is_portrait_mode_cnf_device(device):
        status = "pass"
    else:
        status = "fail"
    return status


def verify_delegate_permission_option_in_manage_delegates(device, to_device):
    delegate_displayname = config["devices"][to_device]["user"]["displayname"]
    users = common.get_all_elements_texts(device, settings_dict, "user_title")
    if delegate_displayname not in users:
        raise AssertionError(
            f"{device}: Expected delegate user: '{delegate_displayname}' is not in list of delegate users: {users}"
        )
    search_result_xpath = common.get_dict_copy(
        calls_dict,
        "search_result_item_container",
        "config_display",
        config["devices"][to_device]["user"]["displayname"],
    )
    common.wait_for_and_click(device, search_result_xpath, "search_result_item_container")
    common.click_if_present(device, settings_dict, "view_permissions_xpath")
    time.sleep(display_time)
    delegate_permissions_list = [
        "Make calls",
        "Receive calls",
        "Change call and delegate settings",
        "Join active calls",
        "Pick up held calls",
    ]
    permissions_title_list = common.get_all_elements_texts(device, settings_dict, "delete_delegates")
    permission_toggle_list = common.wait_for_element(
        device, settings_dict, "permission_switch", cond=EC.presence_of_all_elements_located
    )
    if permissions_title_list != delegate_permissions_list:
        raise AssertionError(
            f"{device}: Not all permissions are displayed: '{permissions_title_list}' for the user: {delegate_displayname}. Expected permissions: '{delegate_permissions_list}'"
        )
    for permission_toggle in permission_toggle_list:
        if permission_toggle.get_attribute("checked") != "true":
            raise AssertionError(
                f"{device}: Permission toggle is not enabled for all permissions: '{permission_toggle_list}'"
            )
    click_back(device)
    common.wait_for_element(device, settings_dict, "user_title")


def disable_option_in_delegates_permission(device, to_device, option):
    if option not in [
        "Make_calls",
        "Receive_calls",
        "Change_call_and_delegate_settings",
        "Join_active_calls",
        "Pick_up_held_calls",
    ]:
        raise AssertionError(f"Illegal value for status: {option}")
    option1 = option.replace("_", " ")
    delegate_displayname = common.device_displayname(to_device)
    search_result_xpath = common.get_dict_copy(
        calls_dict, "search_result_item_container", "config_display", delegate_displayname
    )
    common.wait_for_and_click(device, search_result_xpath, "search_result_item_container", "xpath")
    delegate_options = option1
    title = common.get_all_elements_texts(device, settings_dict, "delete_delegates")
    toggle_switch = common.wait_for_element(
        device, settings_dict, "permission_switch", cond=EC.presence_of_all_elements_located
    )
    for name, toggle in zip(title, toggle_switch):
        if name == delegate_options:
            print(name, delegate_options)
            toggle_status1 = toggle.get_attribute("checked")
            print(f"{device}: Toggle for {delegate_options} current state is: {toggle_status1}")
            if toggle_status1 != "false":
                toggle.click()
                toggle_status2 = toggle.get_attribute("checked")
                print(f"{device}: Toggle for {delegate_options} current sate after clicking is: {toggle_status2}")
                if toggle_status2 != "false":
                    raise AssertionError(
                        f"{device}: Toggle for {delegate_options} is not clicked old state:{toggle_status1}, current state:{toggle_status2}"
                    )
            time.sleep(display_time)
    common.wait_for_and_click(device, settings_dict, "save_delegate_permissions")
    common.wait_for_element(device, settings_dict, "user_title")
    users = common.get_all_elements_texts(device, settings_dict, "user_title")
    if delegate_displayname not in users:
        raise AssertionError(f"{to_device} is not added in delegate user")


def verify_search_results_for_delegates_at_Manage_delegates_screen(device, to_device):
    delegate_displayname = config["devices"][to_device]["user"]["displayname"]
    common.wait_for_element(device, settings_dict, "add_delegates").send_keys(delegate_displayname)
    subprocess.call(
        "adb -s {} shell input keyevent 66".format(config["devices"][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    subprocess.call(
        "adb -s {} shell input keyevent 67".format(config["devices"][device]["desired_caps"]["udid"].split(":")[0]),
        shell=True,
    )
    ele = common.wait_for_element(device, calls_dict, "search_result_item_container").text
    if not ele == delegate_displayname:
        raise AssertionError(f"{to_device} user name not founded")
    click_back(device)


def verify_people_you_support_more_option_at_favorites_page(from_device, to_device):
    refresh_calls_main_tab(from_device)
    common.wait_for_element(from_device, calls_dict, "people_you_support")
    boss_displayname = common.device_displayname(to_device)
    temp_dict = common.get_dict_copy(calls_dict, "favorites_more_options", "user_name", boss_displayname)
    common.wait_for_and_click(from_device, temp_dict, "favorites_more_options", "xpath")
    common.wait_for_element(from_device, calls_dict, "view_Permissions")
    common.wait_for_and_click(from_device, calendar_dict, "touch_outside")


def verify_existing_delegates_and_delegators_in_manage_delegates(device, people_you_support, your_delegates):
    your_delegate_displayname = common.device_displayname(your_delegates)
    people_you_support_displayname = common.device_displayname(people_you_support)
    common.wait_for_element(device, calls_dict, "your_delegates")
    common.wait_for_element(device, calls_dict, "people_you_support")
    ele = common.get_all_elements_texts(device, calls_dict, "user_title")
    if your_delegate_displayname not in ele:
        raise AssertionError(f"{device}: Couldn't find {your_delegate_displayname} in {ele}")
    if people_you_support_displayname not in ele:
        raise AssertionError(f"{device}: Couldn't find {people_you_support_displayname} in {ele}")


def enable_permission_for_delegates(device, to_device):
    navigate_to_manage_delegate_page(device)
    delegate_displayname = common.device_displayname(to_device)
    search_result_xpath = common.get_dict_copy(
        calls_dict, "search_result_item_container", "config_display", delegate_displayname
    )
    common.wait_for_and_click(device, search_result_xpath, "search_result_item_container")
    while common.is_element_present(device, settings_dict, "change_call_and_delegate_setting_toggle_off"):
        common.wait_for_and_click(device, settings_dict, "change_call_and_delegate_setting_toggle_off")
    common.wait_while_present(device, settings_dict, "change_call_and_delegate_setting_toggle_off")
    common.return_to_home_screen(device)


def disable_lightweight_meeting_experience(device):
    if not common.is_element_present(device, settings_dict, "Enable_lightweight_meeting_experience"):
        common.return_to_home_screen(device)
        calendar_keywords.verify_meetings_option_under_app_settings_page(device)
    calendar_keywords.enable_or_disable_lightweight_meeting_experience(device, "OFF")


def enable_lightweight_meeting_experience(device):
    if not common.is_element_present(device, settings_dict, "Enable_lightweight_meeting_experience"):
        common.return_to_home_screen(device)
        calendar_keywords.verify_meetings_option_under_app_settings_page(device)
    calendar_keywords.enable_or_disable_lightweight_meeting_experience(device, "ON")


def verify_lightweight_meeting_experience_in_meeting_option(device):
    if not common.is_element_present(device, settings_dict, "Enable_lightweight_meeting_experience"):
        call_keywords.come_back_to_home_screen(device)
        calendar_keywords.verify_meetings_option_under_app_settings_page(device)
    common.wait_for_element(device, settings_dict, "Enable_lightweight_meeting_experience")
    lightweight_meeting_experience_toggle = common.wait_for_element(
        device, settings_dict, "Enable_lightweight_meeting_experience_toggle_btn"
    )
    lightweight_meeting_experience_toggle_status = lightweight_meeting_experience_toggle.get_attribute("checked")
    if lightweight_meeting_experience_toggle_status != "true":
        raise AssertionError(
            f"light weight meeting toggle have been disabled :{lightweight_meeting_experience_toggle_status}"
        )


def verify_device_display_type(device):
    print("device :", device)
    if common.is_portrait_mode_cnf_device(device):
        display_type = "portrait"
    else:
        display_type = "landscape"
    return display_type


def verify_join_call_option_should_not_present_inside_the_more_icon_of_boss(from_device, to_device):
    refresh_calls_main_tab(from_device)
    common.wait_for_element(from_device, calls_dict, "people_you_support")
    boss_displayname = common.device_displayname(to_device)
    temp_dict = common.get_dict_copy(calls_dict, "favorites_more_options", "user_name", boss_displayname)
    common.wait_while_present(
        from_device, settings_dict, "join_call_option_inside_the_more_icon_of_boss", max_wait_attempts=3
    )
    common.wait_for_and_click(from_device, temp_dict, "favorites_more_options", "xpath")
    common.wait_for_element(from_device, calls_dict, "view_Permissions")
    common.wait_while_present(
        from_device, settings_dict, "join_call_option_inside_the_more_icon_of_boss", max_wait_attempts=3
    )
    common.wait_for_and_click(from_device, calendar_dict, "touch_outside")


def enable_option_in_delegates_permission(device, to_device, option):
    if option not in [
        "Make_calls",
        "Receive_calls",
        "Change_call_and_delegate_settings",
        "Join_active_calls",
        "Pick_up_held_calls",
    ]:
        raise AssertionError(f"Illegal value for status: {option}")
    option1 = option.replace("_", " ")
    navigate_to_manage_delegate_page(device)
    delegate_displayname = common.device_displayname(to_device)
    search_result_xpath = common.get_dict_copy(
        calls_dict, "search_result_item_container", "config_display", delegate_displayname
    )
    common.wait_for_and_click(device, search_result_xpath, "search_result_item_container", "xpath")
    time.sleep(action_time)
    title = common.get_all_elements_texts(device, settings_dict, "delete_delegates")
    delegate_options = option1
    toggle_switch = common.wait_for_element(
        device, settings_dict, "permission_switch", cond=EC.presence_of_all_elements_located
    )
    for name, toggle in zip(title, toggle_switch):
        if name == delegate_options:
            print(name, delegate_options)
            toggle_status1 = toggle.get_attribute("checked")
            print(f"{device}: Toggle for {delegate_options} current state is: {toggle_status1}")
            if toggle_status1 != "true":
                toggle.click()
                toggle_status2 = toggle.get_attribute("checked")
                print(f"{device}: Toggle for {delegate_options} current sate after clicking is: {toggle_status2}")
                if toggle_status2 != "true":
                    raise AssertionError(
                        f"{device}: Toggle for {delegate_options} is not clicked old state:{toggle_status1},current state:{toggle_status2}"
                    )
            time.sleep(display_time)
    common.wait_for_and_click(device, settings_dict, "save_delegate_permissions")
    common.wait_for_element(device, settings_dict, "user_title")
    users = common.get_all_elements_texts(device, settings_dict, "user_title")
    if delegate_displayname not in users:
        raise AssertionError(f"{to_device} is not added in delegate user")


def verify_and_join_call_using_join_button_with_boss(from_device, to_device, option="join_call"):
    if option.lower() not in ["verify", "join_call"]:
        raise AssertionError(f"Illegal value for 'option': '{option}'")
    refresh_calls_main_tab(from_device)
    common.wait_for_element(from_device, calls_dict, "people_you_support")
    user_displayname = common.device_displayname(to_device)
    boss = common.get_all_elements_texts(from_device, settings_dict, "contact_display_name")
    if user_displayname not in boss:
        raise AssertionError(f"{from_device} is not found {to_device} name:{boss}")
    active_call_duration = (
        common.wait_for_element(from_device, calls_dict, "ongoing_active_call_duration").text
    ).split(":")
    if active_call_duration[0] != "Active call":
        raise AssertionError(f"{from_device} active call duration: '{option}'")
    if option == "join_call":
        common.wait_for_and_click(from_device, settings_dict, "join_call_option_of_boss")
        common.wait_for_element(from_device, calls_dict, "Hang_up_button")
    elif option == "verify":
        common.wait_for_element(from_device, settings_dict, "join_call_option_of_boss")


def verify_and_resume_call_using_resume_call_in_more_option_with_boss(from_device, to_device, option="join_call"):
    if option.lower() not in ["verify", "join_call"]:
        raise AssertionError(f"Illegal value for 'option': '{option}'")
    refresh_calls_main_tab(from_device)
    common.wait_for_element(from_device, calls_dict, "people_you_support")
    boss_displayname = common.device_displayname(to_device)
    temp_dict = common.get_dict_copy(calls_dict, "favorites_more_options", "user_name", boss_displayname)
    common.wait_for_element(from_device, calls_dict, "Resume")
    common.wait_for_and_click(from_device, temp_dict, "favorites_more_options", "xpath")
    common.wait_for_element(from_device, calls_dict, "view_Permissions")
    common.wait_for_element(from_device, calls_dict, "call_list_item_call_action")
    common.wait_for_element(from_device, calls_dict, "call_list_view_profile_action")
    if option == "join_call":
        common.wait_for_and_click(from_device, settings_dict, "resume_call_in_more_option_with_boss")
        common.wait_for_element(from_device, calls_dict, "Hang_up_button")
    elif option == "verify":
        common.wait_for_element(from_device, settings_dict, "resume_call_in_more_option_with_boss")
        common.tap_outside_the_popup(
            from_device, common.wait_for_element(from_device, calls_dict, "calls_item_options_container")
        )


def verify_and_join_call_using_join_call_in_more_option_with_boss_and_delegate(
    from_device, to_device, option="join_call"
):
    if option.lower() not in ["verify", "join_call", "call"]:
        raise AssertionError(f"Illegal value for 'option': '{option}'")
    refresh_calls_main_tab(from_device)
    boss_displayname = common.device_displayname(to_device)
    temp_dict = common.get_dict_copy(calls_dict, "favorites_more_options", "user_name", boss_displayname)
    active_call_duration = common.wait_for_element(from_device, calls_dict, "ongoing_active_call_duration").text.split(
        ":"
    )
    if active_call_duration[0] != "Active call":
        raise AssertionError(f"{from_device}: There are no active calls on device: {active_call_duration[0]}")
    common.wait_for_element(from_device, settings_dict, "join_call_option_of_boss")
    common.wait_for_and_click(from_device, temp_dict, "favorites_more_options", "xpath")
    common.wait_for_element(from_device, calls_dict, "view_Permissions")
    common.wait_for_element(from_device, calls_dict, "call_list_item_call_action")
    common.wait_for_element(from_device, calls_dict, "call_list_view_profile_action")
    if option == "join_call":
        common.wait_for_and_click(from_device, settings_dict, "join_call_option_of_boss")
        common.wait_for_element(from_device, calls_dict, "Hang_up_button")
    elif option == "verify":
        common.wait_for_element(from_device, settings_dict, "join_call_option_of_boss")
        common.tap_outside_the_popup(
            from_device, common.wait_for_element(from_device, calls_dict, "calls_item_options_container")
        )
    elif option == "call":
        common.wait_for_and_click(from_device, settings_dict, "call_option_inside_the_more_icon_of_boss")
        common.wait_for_element(from_device, calls_dict, "Hang_up_button")


def verify_hotline_option(device):
    print("device :", device)
    open_settings_page(device)
    swipe_till_end(device)
    swipe_till_end(device)
    common.wait_for_and_click(device, settings_dict, "Device_Settings")
    device_settings_keywords.advance_calling_option_oem(device)
    common.wait_for_element(device, calls_dict, "hotline")


def verify_hotline_option_is_disabled_by_default(device):
    common.wait_for_element(device, calls_dict, "hotline")
    hotline_text = common.wait_for_element(device, settings_dict, "hotline_status_text").text
    if hotline_text != "Disabled":
        raise AssertionError("Hotline Toggle is not disabled")


def configure_contact_number_in_hotline(device, configured_user):
    print("device :", device)
    display_name = common.device_displayname(configured_user)
    user_phone_number = common.device_phonenumber(configured_user)
    common.wait_for_and_click(device, calls_dict, "hotline")
    time.sleep(display_time)
    if not common.click_if_present(device, calls_dict, "add_contact"):
        common.wait_for_and_click(device, settings_dict, "hotline_edit_btn")
    common.wait_for_and_click(device, settings_dict, "search_contact_box")
    contact = common.wait_for_element(device, settings_dict, "search_contact_box")
    contact.clear()
    contact.send_keys(user_phone_number)
    common.wait_for_and_click(device, settings_dict, "hotline_display_name")
    disp_name = common.wait_for_element(device, settings_dict, "hotline_display_name")
    disp_name.clear()
    disp_name.send_keys(display_name)
    common.wait_for_and_click(device, settings_dict, "hotline_save_btn")
    common.wait_for_and_click(device, settings_dict, "hotline_toogle")
    common.wait_for_and_click(device, settings_dict, "restart_btn")


def verify_cancel_btn_while_adding_contact_number_in_hotline(device, configured_user):
    print("device :", device)
    display_name = common.device_displayname(configured_user)
    user_phone_number = common.device_phonenumber(configured_user)
    common.wait_for_and_click(device, calls_dict, "hotline")
    time.sleep(display_time)
    if not common.click_if_present(device, calls_dict, "add_contact"):
        common.wait_for_and_click(device, settings_dict, "hotline_edit_btn")
    common.wait_for_and_click(device, settings_dict, "search_contact_box")
    contact = common.wait_for_element(device, settings_dict, "search_contact_box")
    contact.clear()
    contact.send_keys(user_phone_number)
    common.wait_for_and_click(device, settings_dict, "hotline_display_name")
    disp_name = common.wait_for_element(device, settings_dict, "hotline_display_name")
    disp_name.clear()
    disp_name.send_keys(display_name)
    common.wait_for_and_click(device, calls_dict, "cancel_btn")


def verify_not_saved_user_name_in_hotline_while_adding_or_editing(device, configured_user):
    common.wait_for_and_click(device, calls_dict, "hotline")
    expected_user = common.device_displayname(configured_user)
    print("Expected Hotline Users are:", expected_user)
    if common.is_element_present(device, calls_dict, "add_contact"):
        print(f"{device}:configured user name is not saved in hotline")
        return
    actual_user = common.get_all_elements_texts(device, settings_dict, "hotline_user_name")
    print("Actual Hotline Users are:", actual_user)
    if expected_user in actual_user:
        raise AssertionError(f"Expected Hotline user names {expected_user} displayed in {actual_user}")


def verify_hotline_homescreen_UI(device, state="Enabled"):
    if state.lower() not in ["enabled", "disabled"]:
        raise AssertionError(f"Illegal value for 'state': '{state}'")
    if state.lower() == "disabled":
        if not common.is_element_present(device, calls_dict, "calls_tab"):
            common.wait_for_element(device, calls_dict, "call_park")
    else:
        common.wait_for_element(device, settings_dict, "hotline_UI")


def verify_user_can_not_call_to_anyone_when_hotline_is_enabled(device):
    time.sleep(display_time)
    if common.is_element_present(device, settings_dict, "hotline_UI"):
        return
    else:
        if not common.is_element_present(device, calls_dict, "calls_tab"):
            common.wait_for_element(device, calls_dict, "dialpad_tab")


def disable_hotline_option_from_home_screen(device):
    common.wait_for_and_click(device, settings_dict, "hotline_settings_btn")
    device_settings_keywords.advance_calling_option_oem(device)
    common.wait_for_and_click(device, calls_dict, "hotline")
    common.wait_for_and_click(device, settings_dict, "hotline_toogle")
    common.wait_for_and_click(device, settings_dict, "restart_btn")


def change_hotline_toggle_for_cap(device, toogle_status):
    if toogle_status.lower() not in ["enable", "disable"]:
        raise AssertionError(f"Illegal value for 'status': '{toogle_status}'")
    toogle_btn = common.wait_for_element(device, settings_dict, "hotline_toogle").text
    print(toogle_btn)
    if toogle_status.lower() == "disable":
        if toogle_btn != "ON":
            raise AssertionError(f"f{device} Hotline toggle is already disabled by default")
    if toogle_status.lower() == "enable":
        if toogle_btn != "OFF":
            raise AssertionError(f"f{device} Hotline toggle is already enabled by default")
    common.wait_for_and_click(device, settings_dict, "hotline_toogle")
    common.wait_for_and_click(device, settings_dict, "restart_btn")


def verify_hotline_toggle_status_for_cap(device, toogle_status):
    if toogle_status.lower() not in ["enabled", "disabled"]:
        raise AssertionError(f"Illegal value for 'status': '{toogle_status}'")
    common.wait_for_and_click(device, settings_dict, "hotline_settings_btn")
    device_settings_keywords.advance_calling_option_oem(device)
    common.wait_for_and_click(device, calls_dict, "hotline")
    toogle_btn = common.wait_for_element(device, settings_dict, "hotline_toogle").text
    print(toogle_btn)
    if toogle_status.lower() == "enabled":
        if toogle_btn != "ON":
            raise AssertionError(f"{device} Hotline toggle is not enabled")
    if toogle_status.lower() == "disabled":
        if toogle_btn != "OFF":
            raise AssertionError(f"{device} Hotline toggle is not disabled")


def edit_configured_hotline_contact_details_from_hotline_homescreen(device, edited_configured_user):
    for i in range(5):
        if not common.click_if_present(device, calls_dict, "Call_Back_Button"):
            break
    user_phone_number = config["devices"][edited_configured_user]["user"]["phonenumber"]
    display_name = config["devices"][edited_configured_user]["user"]["displayname"]
    common.wait_for_and_click(device, settings_dict, "hotline_settings_btn")
    device_settings_keywords.advance_calling_option_oem(device)
    common.wait_for_and_click(device, calls_dict, "hotline")
    common.wait_for_and_click(device, settings_dict, "hotline_edit_btn")
    common.wait_for_and_click(device, settings_dict, "search_contact_box")
    contact = common.wait_for_element(device, settings_dict, "search_contact_box")
    contact.clear()
    contact.send_keys(user_phone_number)
    common.wait_for_and_click(device, settings_dict, "hotline_display_name")
    disp_name = common.wait_for_element(device, settings_dict, "hotline_display_name")
    disp_name.clear()
    disp_name.send_keys(display_name)
    common.wait_for_and_click(device, settings_dict, "hotline_save_btn")
    common.wait_for_and_click(device, settings_dict, "restart_btn")


def come_back_to_home_screen_from_hotline_page(device):
    call_keywords.come_back_to_home_screen(device)
    if not (
        common.is_element_present(device, home_screen_dict, "call_tab")
        or common.is_element_present(device, calls_dict, "dialpad_tab")
    ):
        common.wait_for_element(device, settings_dict, "hotline_UI")


def configure_emergency_number_in_hotline(device):
    print("device :", device)
    emergency_phone_number = "933"
    display_name = "Emergency Contact"
    common.wait_for_and_click(device, calls_dict, "hotline")
    time.sleep(display_time)
    if not common.click_if_present(device, calls_dict, "add_contact"):
        common.wait_for_and_click(device, settings_dict, "hotline_edit_btn")
    common.wait_for_and_click(device, settings_dict, "search_contact_box")
    contact = common.wait_for_element(device, settings_dict, "search_contact_box")
    contact.clear()
    contact.send_keys(emergency_phone_number)
    common.wait_for_and_click(device, settings_dict, "hotline_display_name")
    disp_name = common.wait_for_element(device, settings_dict, "hotline_display_name")
    disp_name.clear()
    disp_name.send_keys(display_name)
    common.wait_for_and_click(device, settings_dict, "hotline_save_btn")
    common.wait_for_and_click(device, settings_dict, "hotline_toogle")
    common.wait_for_and_click(device, settings_dict, "restart_btn")


def configure_invalid_contact_details_in_hotline(device):
    print("device :", device)
    invalid_contact_number = config["incorrect_number"]["phonenumber"]
    invalid_display_name = config["user"]["invalid_username"]
    common.wait_for_and_click(device, calls_dict, "hotline")
    time.sleep(display_time)
    if not common.click_if_present(device, calls_dict, "add_contact"):
        common.wait_for_and_click(device, settings_dict, "hotline_edit_btn")
    common.wait_for_and_click(device, settings_dict, "search_contact_box")
    contact = common.wait_for_element(device, settings_dict, "search_contact_box")
    contact.clear()
    contact.send_keys(invalid_contact_number)
    common.wait_for_and_click(device, settings_dict, "hotline_display_name")
    disp_name = common.wait_for_element(device, settings_dict, "hotline_display_name")
    disp_name.clear()
    disp_name.send_keys(invalid_display_name)
    common.wait_for_and_click(device, settings_dict, "hotline_save_btn")
    common.wait_for_and_click(device, settings_dict, "hotline_toogle")
    common.wait_for_and_click(device, settings_dict, "restart_btn")


def navigate_to_settings_page_from_hotline_home_screen(device):
    common.wait_for_element(device, settings_dict, "hotline_UI")
    common.wait_for_and_click(device, settings_dict, "hotline_settings_btn")
    common.wait_for_element(device, settings_dict, "About")
    device_setting_back(device)


def verify_and_enable_cap_premium(device):
    """This keyword just verifies  whether device is cap or cap premium,
    and enables to cap premium if device is in cap"""
    time.sleep(display_time)
    if common.is_lcp(device):
        if common.is_element_present(device, lcp_homescreen_dict, "voicemail_tab") and common.is_element_present(
            device, lcp_homescreen_dict, "lock"
        ):
            set_advance_calling(device, status="ON")
        return
    elif common.is_element_present(device, calls_dict, "dialpad_tab") and common.is_element_present(
        device, calls_dict, "call_park"
    ):
        set_advance_calling(device, status="ON")
    else:
        print(f"{device} is already in cap premium")


def verify_presence_of_other_user_from_calls_tab(from_device, to_device, state):
    if state.lower() not in ["in call", "available", "busy", "dnd", "be right back", "offline", "away"]:
        raise AssertionError(f"Unexpected value for option : {state}")
    to_device_displayname = common.device_displayname(to_device)
    time.sleep(display_time)
    common.wait_for_element(from_device, lcp_calls_dict, "recent_user_entry_lcp")
    if state.lower() == "in call":
        presence_xpath = common.get_dict_copy(
            settings_dict, "in_call_presence_xpath", "username", to_device_displayname
        )
        common.wait_for_element(from_device, presence_xpath, "in_call_presence_xpath", wait_attempts=180)
    elif state.lower() == "available":
        presence_xpath = common.get_dict_copy(
            settings_dict, "available_presence_xpath", "username", to_device_displayname
        )
        common.wait_for_element(from_device, presence_xpath, "available_presence_xpath", wait_attempts=180)
    elif state.lower() == "busy":
        presence_xpath = common.get_dict_copy(settings_dict, "busy_presence_xpath", "username", to_device_displayname)
        common.wait_for_element(from_device, presence_xpath, "busy_presence_xpath")
        print(f"{to_device_displayname} is Busy")
    elif state.lower() == "dnd":
        presence_xpath = common.get_dict_copy(settings_dict, "dnd_presence_xpath", "username", to_device_displayname)
        common.wait_for_element(from_device, presence_xpath, "dnd_presence_xpath", wait_attempts=180)
    elif state.lower() == "be right back":
        presence_xpath = common.get_dict_copy(
            settings_dict, "be_right_back_presence_xpath", "username", to_device_displayname
        )
        common.wait_for_element(from_device, presence_xpath, "be_right_back_presence_xpath")
        print(f"{to_device_displayname} in Be Right Back mode")
    elif state.lower() == "offline":
        presence_xpath = common.get_dict_copy(
            settings_dict, "offline_presence_xpath", "username", to_device_displayname
        )
        common.wait_for_element(from_device, presence_xpath, "offline_presence_xpath", wait_attempts=180)
    elif state.lower() == "away":
        presence_xpath = common.get_dict_copy(settings_dict, "away_presence_xpath", "username", to_device_displayname)
        common.wait_for_element(from_device, presence_xpath, "away_presence_xpath")
        print(f"{to_device_displayname} is Away")


def verify_delegate_options_inside_call_info_with_boss_when_boss_is_in_call_with_other_user(from_device, boss):
    call_keywords.navigate_to_calls_favorites_page(from_device)
    refresh_calls_main_tab(from_device)
    common.wait_for_element(from_device, calls_dict, "people_you_support")
    boss_displayname = common.device_displayname(boss)
    temp_dict = common.get_dict_copy(calls_dict, "favorites_more_options", "user_name", boss_displayname)
    common.wait_while_present(from_device, calls_dict, "Resume", max_wait_attempts=3)
    common.wait_for_and_click(from_device, temp_dict, "favorites_more_options", "xpath")
    common.wait_for_element(from_device, calls_dict, "call_list_item_call_action")
    common.wait_for_element(from_device, calls_dict, "call_list_view_profile_action")
    common.wait_for_element(from_device, calls_dict, "view_Permissions")
    common.wait_for_and_click(from_device, calendar_dict, "touch_outside")


def verify_boss_options_inside_call_info_with_delegate_when_delegate_is_in_call_with_other_user(from_device, delegate):
    call_keywords.navigate_to_calls_favorites_page(from_device)
    refresh_calls_main_tab(from_device)
    common.wait_for_element(from_device, calls_dict, "your_delegates")
    delegate_displayname = common.device_displayname(delegate)
    temp_dict = common.get_dict_copy(calls_dict, "favorites_more_options", "user_name", delegate_displayname)
    common.wait_for_element(from_device, calls_dict, "Resume")
    common.wait_for_and_click(from_device, temp_dict, "favorites_more_options", "xpath")
    common.wait_for_element(from_device, calls_dict, "resume_call_at_recent_tab_more")
    common.wait_for_element(from_device, calls_dict, "call_list_item_call_action")
    common.wait_for_element(from_device, calls_dict, "call_list_view_profile_action")
    common.wait_for_element(from_device, calls_dict, "view_Permissions")
    common.wait_for_and_click(from_device, calendar_dict, "touch_outside")


def verify_resume_call_option_should_not_present_inside_the_more_icon_of_boss(from_device, to_device):
    refresh_calls_main_tab(from_device)
    common.wait_for_element(from_device, calls_dict, "people_you_support")
    boss_displayname = common.device_displayname(to_device)
    temp_dict = common.get_dict_copy(calls_dict, "favorites_more_options", "user_name", boss_displayname)
    common.wait_for_and_click(from_device, temp_dict, "favorites_more_options", "xpath")
    common.wait_for_element(from_device, calls_dict, "view_Permissions")
    common.wait_while_present(from_device, settings_dict, "resume_call_in_more_option_with_boss", max_wait_attempts=3)
    common.wait_for_and_click(from_device, calendar_dict, "touch_outside")


def verify_default_options_present_in_delegate_settings_page(from_device, to_device):
    navigate_to_manage_delegate_page(from_device)
    username = common.device_displayname(to_device)
    common.kb_trigger_search(from_device, settings_dict, "add_delegates", username)
    tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", username)
    common.wait_for_and_click(from_device, tmp_dict, "search_result_item_container", "xpath")
    time.sleep(display_time)
    common.wait_for_element(from_device, settings_dict, "save_permissions")
    title = common.get_all_elements_texts(from_device, settings_dict, "delete_delegates")
    print(f"{from_device}: Delegate options present while adding delegate are :{title}")
    expected_delegate_options = [
        "Make calls",
        "Receive calls",
        "Change call and delegate settings",
        "Join active calls",
        "Pick up held calls",
    ]
    if title != expected_delegate_options:
        raise AssertionError(f"{from_device}: Delegate options present are incorrect")


def verify_default_options_enabled_while_adding_delegate_in_delegate_settings_page(device):
    title = common.get_all_elements_texts(device, settings_dict, "delete_delegates")
    print(f"{device}: Delegate options present while adding delegate are :{title}")
    toggle_switch = common.wait_for_element(
        device, settings_dict, "permission_switch", cond=EC.presence_of_all_elements_located
    )
    toggles_state_list = []
    for ele in toggle_switch:
        ele1 = ele.get_attribute("checked")
        toggles_state_list.append(ele1)
        print(toggles_state_list)
    enabled_toggles_list = toggles_state_list[:2]
    disabled_toggles_list = toggles_state_list[2:]
    print(
        f"{device}: enabled and disabled toggles list are respectively :", enabled_toggles_list, disabled_toggles_list
    )
    for i in enabled_toggles_list:
        if i != "true":
            raise AssertionError(f"{device}: Default enabled toggle options are not as expected")
    for j in disabled_toggles_list:
        if j != "false":
            raise AssertionError(f"{device}: Default disabled toggle options are not as expected")
    click_back(device)


def verify_and_resume_call_using_resume_button_with_boss(from_device, to_device, option="join_call"):
    if option.lower() not in ["verify", "join_call"]:
        raise AssertionError(f"Illegal value for 'option': '{option}'")
    refresh_calls_main_tab(from_device)
    common.wait_for_element(from_device, calls_dict, "people_you_support")
    user_displayname = common.device_displayname(to_device)
    boss = common.get_all_elements_texts(from_device, settings_dict, "contact_display_name")
    if user_displayname not in boss:
        raise AssertionError(f"{from_device} is not found {to_device} name:{boss}")
    if option == "join_call":
        common.wait_for_and_click(from_device, calls_dict, "Resume")
        common.wait_for_element(from_device, calls_dict, "Hang_up_button")
    elif option == "verify":
        common.wait_for_element(from_device, calls_dict, "Resume")


def is_dial_pad_applicable_for_cap(device):
    print("device :", device)
    if config["devices"][device]["model"].lower() in ["riverside", "riverside_13"]:
        status = "pass"
    else:
        status = "fail"
    return status


def verify_signin_with_license_is_not_supported_account_used_for_signin_phones(device):
    username, password, device, account_type = common.get_credentials(device)
    print(username, password, device, account_type)
    if common.is_element_present(device, sign_dict, "refresh_code_button"):
        common.wait_for_and_click(device, sign_dict, "refresh_code_button")
        common.sleep_with_msg(device, 5, "Allow refresh of DFC code")
    common.wait_for_element(device, sign_dict, "dfc_login_code")
    common.wait_for_and_click(device, sign_dict, "sign_in_on_the_device")
    common.wait_for_and_click(device, sign_dict, "Username")
    search_input = common.wait_for_element(device, sign_dict, "Username")
    search_input.send_keys(username)
    print("Entered username")
    common.wait_for_and_click(device, sign_dict, "Sign_in_button")
    common.wait_for_element(device, sign_dict, "Password").send_keys(password)
    print(f"{device}: entered the password")
    if not common.click_if_present(device, sign_dict, "Sign_in"):
        common.wait_for_and_click(device, sign_dict, "signin_button")
    if account_type == "mtra_basic_account":
        error_message = common.wait_for_element(device, sign_dict, "signin_failure_error", wait_attempts=40).text
        if (
            error_message.strip()
            != "Your current license is not supported on this device. Ask your IT administrator for details.".strip()
        ):
            raise AssertionError(f"unsupported account error message is not found: {error_message}")

    elif account_type in ["maximum_os_account", "minimum_os_account"]:
        error_message = common.wait_for_element(device, sign_dict, "signin_failure_error", wait_attempts=40).text
        allowed_error_messages = [
            "Device OS version doesn't meet the maximum OS company Policy. Contact your admin.",
            "Device OS version doesn't meet the minimum OS company Policy. Contact your admin.",
        ]
        if error_message.strip() not in [msg.strip() for msg in allowed_error_messages]:
            raise AssertionError(f"Unsupported account error message is not found: {error_message}")

    elif account_type in ["cap_limit_reached_account", "enrollment_restrict_account"]:
        error_message = common.wait_for_element(device, sign_dict, "signin_failure_error", wait_attempts=40).text
        allowed_error_messages = [
            "Couldn’t connect to Workplace Join. Try again, or contact your admin.",
            "This device needs to be enrolled in device administrator. Contact your IT admin.",
            "Couldn’t enroll in Intune due to the device limit. Contact your admin.",
        ]
        if error_message.strip() not in [msg.strip() for msg in allowed_error_messages]:
            raise AssertionError(f"Unsupported account error message is not found: {error_message}")

    elif account_type in [
        "cap_mtra_pro_license_with_personal_policy_assigned_account",
        "cap_personal_license_with_personal_policy_assigned_account",
    ]:
        common.sleep_with_msg(device, 30, "waiting for complete sign-in")
        home_screen_keywords.verify_home_screen_tiles(device)
        home_screen_keywords.verify_home_screen_time_dates(device)


def verify_set_your_emergency_location_option_under_user_profile(device):
    expected_mail_id, password, device, account = common.get_credentials(device)
    common.wait_for_and_click(device, navigation_dict, "Navigation")
    common.wait_for_and_click(device, settings_dict, "user_displayname")
    actual_mail_id = common.wait_for_element(device, calls_dict, "mail_id").text.lower()
    if actual_mail_id != expected_mail_id:
        raise AssertionError(f"{device}: Expected mail id: '{expected_mail_id}', but found: '{actual_mail_id}'")
    common.wait_for_element(device, settings_dict, "set_your_emergency_location")


def verify_each_option_in_teams_admin_setting_for_conf(device):
    driver = obj.device_store.get(alias=device)
    if config["devices"][device]["model"].lower() == "manhattan":
        common.wait_for_and_click(device, device_settings_dict, "admin_settings")
        element1 = common.wait_for_element(device, settings_dict, "admin_passwd")
        element1.set_value(config["devices"][device]["admin_password"])
        common.hide_keyboard(device)
        common.wait_for_and_click(device, settings_dict, "Login_btn")
        common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings")
        common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings_btn")
    elif config["devices"][device]["model"].lower() == "tacoma":
        common.wait_for_and_click(device, settings_dict, "Admin_Only", "xpath")
        common.wait_for_element(device, settings_dict, "admin_passwd", "xpath").set_value(
            config["devices"][device]["admin_password"]
        )
        driver.execute_script("mobile: performEditorAction", {"action": "done"})
        app_bar_keywords.swipe_page_up(device)
    elif config["devices"][device]["model"].lower() == "berkely":
        common.wait_for_and_click(device, settings_dict, "device_admin_pswd")
        common.wait_for_element(device, settings_dict, "device_admin_pswd").set_value(
            config["devices"][device]["admin_password"]
        )
        driver.execute_script("mobile: performEditorAction", {"action": "done"})
        common.hide_keyboard(device)
        settings_keywords.swipe_till_end(device)
        common.wait_for_and_click(device, device_settings_dict, "teams_admin_settings", "text")
    common.wait_for_and_click(device, settings_dict, "Sign_out")
    common.wait_for_element(device, calendar_dict, "alert_title")
    common.wait_for_and_click(device, settings_dict, "adv_call_cancel_btn")
    common.wait_for_and_click(device, settings_dict, "Calling")
    common.wait_for_element(device, settings_dict, "call_forwarding")
    common.wait_for_and_click(device, app_bar_dict, "back")


def verify_signin_with_unsupported_account_for_phones(device):
    username = "device@g.com"
    time.sleep(6)
    if common.is_element_present(device, sign_dict, "refresh_code_button"):
        common.wait_for_and_click(device, sign_dict, "refresh_code_button")
        common.sleep_with_msg(device, 5, "Allow refresh of DFC code")
    common.wait_for_element(device, sign_dict, "dfc_login_code")
    common.wait_for_and_click(device, sign_dict, "sign_in_on_the_device")
    common.wait_for_and_click(device, sign_dict, "Username")
    search_input = common.wait_for_element(device, sign_dict, "Username")
    search_input.send_keys(username)
    print("Entered username")
    common.wait_for_and_click(device, sign_dict, "Sign_in_button")
    error_message = common.wait_for_element(device, sign_dict, "unsupported_account_error").text
    if error_message != "You’ll need to sign in with a work account.":
        raise AssertionError(f"unsupported account error message is not found: {error_message}")


def verify_admin_setting_signout_for_conf(device):
    driver = obj.device_store.get(alias=device)
    model = config["devices"][device]["model"].lower()
    if model == "manhattan":
        common.wait_for_and_click(device, device_settings_dict, "admin_settings")
        element1 = common.wait_for_element(device, settings_dict, "admin_passwd")
        element1.set_value(config["devices"][device]["admin_password"])
        common.hide_keyboard(device)
        common.wait_for_and_click(device, settings_dict, "Login_btn")
        common.wait_for_and_click(device, device_settings_dict, "admin_back_button")
        common.wait_for_and_click(device, device_settings_dict, "user_sign_out_yes")
    elif model == "tacoma":
        common.wait_for_and_click(device, settings_dict, "Admin_Only", "xpath")
        common.wait_for_element(device, settings_dict, "admin_passwd", "xpath").set_value(
            config["devices"][device]["admin_password"]
        )
        driver.execute_script("mobile: performEditorAction", {"action": "done"})
        common.wait_for_and_click(device, tr_device_settings_dict, "back_button")
    elif model == "berkely":
        common.wait_for_and_click(device, settings_dict, "device_admin_pswd")
        common.wait_for_element(device, settings_dict, "device_admin_pswd").set_value(
            config["devices"][device]["admin_password"]
        )
        driver.execute_script("mobile: performEditorAction", {"action": "done"})
        common.hide_keyboard(device)
        settings_keywords.swipe_till_end(device)
        common.wait_for_and_click(device, device_settings_dict, "admin_sign_out")
        common.wait_for_and_click(device, device_settings_dict, "ok")
    call_keywords.come_back_to_home_screen(device)
    settings_keywords.open_settings_page(device)
    settings_keywords.click_device_settings(device)
    common.wait_for_and_click(device, settings_dict, "Admin_Only", "xpath")
    common.wait_for_element(device, settings_dict, "admin_passwd")
    common.wait_for_and_click(device, device_settings_dict, "admin_setting_popup_close_btn")


def verify_call_forwarding_label_status_on_home_screen(device, status, to_device=None):
    if status.lower() not in ["off", "voicemail", "contact_or_number", "delegate", "call_group"]:
        raise AssertionError(f"Illegal value for 'status': '{status}'")

    if to_device is not None:
        if ":" in to_device:
            devices, account = common.decode_device_spec(to_device)
            if account == "pstn_user":
                display_name = config["devices"][devices][account]["pstndisplay"]
            else:
                display_name = common.config["devices"][devices][account]["displayname"]
        else:
            display_name = common.device_displayname(to_device)

    common.click_if_present(device, calls_dict, "Call_Back_Button")
    common.click_if_present(device, home_screen_dict, "home_bar_icon")

    if not common.is_element_present(device, navigation_dict, "Navigation"):
        common.wait_for_element(device, calls_dict, "user_profile_picture")

    if status.lower() == "off":
        common.wait_for_element(device, home_screen_dict, "dont_forward_calls")

    elif status.lower() == "voicemail":
        common.wait_for_element(device, home_screen_dict, "forward_to_voicemail")

    elif status.lower() == "contact_or_number":
        forwarding_display_name = "Forward to " + display_name
        tmp_dict = common.get_dict_copy(
            calls_dict, "search_result_item_container", "config_display", forwarding_display_name
        )
        common.wait_for_element(device, tmp_dict, "search_result_item_container", "xpath")

    elif status.lower() == "delegate":
        common.wait_for_element(device, home_screen_dict, "forward_to_my_delegates")

    elif status.lower() == "call_group":
        common.wait_for_element(device, home_screen_dict, "forward_to_call_group")


def verify_and_change_toggle_status_for_call_forwarding_display_on_home_screen(device, status):
    if status.lower() not in ["on", "off"]:
        raise AssertionError(f"Illegal value for 'status': '{status}'")

    open_settings_page(device)
    time.sleep(display_time)

    if not common.click_if_present(device, settings_dict, "Calling"):
        swipe_till_end(device)
        swipe_till_end(device)
        common.wait_for_and_click(device, settings_dict, "Device_Settings")
        device_settings_keywords.advance_calling_option_oem(device)
        common.wait_for_element(device, settings_dict, "call_forwarding")
    if common.is_lcp(device):
        swipe_till_end(device)
    common.change_toggle_button(
        device, settings_dict, "call_forwarding_display_on_home_screen_toggle", desired_state=status
    )

    # come back to home screen page
    call_views_keywords.go_back_to_previous_page(device)

    if status.lower() == "on":
        if not common.is_lcp(device):
            common.wait_for_element(device, settings_dict, "call_forwarding_label_text_on_home_screen")
        common.wait_for_element(device, settings_dict, "call_forwarding_icon_on_home_screen")

    elif status.lower() == "off":
        if common.is_element_present(
            device, settings_dict, "call_forwarding_icon_on_home_screen"
        ) or common.is_element_present(device, settings_dict, "call_forwarding_label_text_on_home_screen"):
            raise AssertionError(
                f"{device} is after disable toggle also appearing call forwarding  status on home screen: {status}"
            )


def reboot_panel(device):
    _model = config["devices"][device]["model"].lower()
    if _model in ["beverly hills", "westchester", "brooklyn", "hollywood", "savannah", "surprise"]:
        common.wait_for_and_click(device, panels_device_settings_dict, "Reboot_panel")
    elif _model == "arlington":
        common.wait_for_and_click(device, settings_dict, "Debug")
        common.wait_for_and_click(device, panels_device_settings_dict, "Reboot_panel", "xpath1")
        common.wait_for_and_click(device, calendar_dict, "ok_button")
    elif _model == "richland":
        panel_meetings_device_settings_keywords.navigate_inside_admin_setting_in_panel(device, password_type="old")
        common.wait_for_and_click(device, device_settings_dict, "system_settings")
        swipe_till_end(device)
        common.wait_for_and_click(device, panels_device_settings_dict, "reset_button")
        common.wait_for_and_click(device, tr_device_settings_dict, "restart")
        common.wait_for_element(device, panels_device_settings_dict, "system_restart_alert")
        common.wait_for_and_click(device, tr_device_settings_dict, "restart")

    else:
        raise AssertionError(f"{device}: No validation specified for device model '{_model}'")


def verify_adb_access_is_disabled_for_device():
    print("verify device is online")
    _udid = config["adb_disabled_device"]["udid"].strip(":5555")
    print(f"connect device : {_udid}")
    cmd_ping = "ping  " + str(_udid.split(":")[0])
    _result = subprocess.run(
        cmd_ping,
        stdout=subprocess.PIPE,
        text=True,
        check=True,
        timeout=float(1 * 60),
    )
    if f"Reply from {_udid}" in _result.stdout:
        print(f"{_udid}: is online.")
        print("Check if ADB is disabled on :", _udid)
        cmd_connect = "adb connect " + str(_udid.split(":")[0])
        time.sleep(2)
        result = subprocess.run(
            cmd_connect,
            stdout=subprocess.PIPE,
            text=True,
            check=True,
            timeout=float(1 * 60),
        )
        if f"cannot connect to {_udid}:5555" not in result.stdout.lower():
            raise AssertionError(
                f"{_udid}: is not in adb disabled build as per expected and able to connect using adb."
            )
        print(f"Verified {_udid}: is in adb disabled build as per expected.")
    else:
        raise AssertionError(f"{_udid}: is not online.")


def connect_panel():
    for device in list(config["devices"].keys()):
        device_control.connect_device(device, config)


def verify_and_set_call_forwarding_on_home_screen(device, option, to_device=None):
    if option.lower() not in ["off", "voicemail", "contact_or_number", "delegate", "call_group"]:
        raise AssertionError(f"Illegal value for 'status': '{option}'")
    if to_device is not None:
        if ":" in to_device:
            devices, account = common.decode_device_spec(to_device)
            if account == "pstn_user":
                display_name = config["devices"][devices][account]["pstndisplay"]
            else:
                display_name = common.config["devices"][devices][account]["displayname"]
        else:
            display_name = common.device_displayname(to_device)

    common.click_if_present(device, calls_dict, "Call_Back_Button")
    common.click_if_present(device, home_screen_dict, "home_bar_icon")

    if not common.is_element_present(device, navigation_dict, "Navigation"):
        common.wait_for_element(device, calls_dict, "user_profile_picture")

    if not (
        common.click_if_present(device, settings_dict, "call_forwarding_icon_on_home_screen")
        or common.click_if_present(device, settings_dict, "forwarding_icon_on_calls_tab")
    ):
        common.wait_for_and_click(device, settings_dict, "call_forwarding_pop_up_open_or_close_button")

    if option.lower() == "off":
        if common.is_lcp(device):
            calendar_keywords.scroll_down_device_setting_tab(device)
        common.wait_for_and_click(device, home_screen_dict, "dont_forward_calls")

    elif option.lower() == "voicemail":
        common.wait_for_and_click(device, home_screen_dict, "forward_to_voicemail")

    elif option.lower() == "contact_or_number":
        common.wait_for_and_click(device, home_screen_dict, "forward_to_contact_or_number")
        common.click_if_element_appears(device, settings_dict, "add_contact_option", max_attempts=3)
        element = common.wait_for_element(device, settings_dict, "search_contact_box")
        element.send_keys(display_name)
        common.hide_keyboard(device)
        tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", display_name)
        common.wait_for_and_click(device, tmp_dict, "search_result_item_container", "xpath")
        common.wait_for_and_click(device, calls_dict, "Call_Back_Button")

    elif option.lower() == "delegate":
        common.wait_for_and_click(device, home_screen_dict, "forward_to_my_delegates")

    elif option.lower() == "call_group":
        common.wait_for_and_click(device, home_screen_dict, "forward_to_call_group")

    if common.is_lcp(device):
        device_setting_back(device)
        return
    common.click_if_present(device, calls_dict, "Call_Back_Button")
    dismiss_call_forwarding_pop_up_on_home_screen(device)
    time.sleep(action_time)
    if not (
        common.is_element_present(device, people_dict, "people_tab_cap")
        or common.is_element_present(device, calls_dict, "search")
    ):
        verify_call_forwarding_label_status_on_home_screen(device=device, status=option, to_device=to_device)


def dismiss_call_forwarding_pop_up_on_home_screen(device):
    time.sleep(action_time)
    if common.is_element_present(device, settings_dict, "forwarding_text"):
        common.wait_for_and_click(device, settings_dict, "call_forwarding_pop_up_open_or_close_button")
    elif common.is_element_present(device, settings_dict, "call_forwarding_pop_up_layout_on_calls_tab"):
        call_keywords.dismiss_call_more_options(
            device, common.wait_for_element(device, settings_dict, "call_forwarding_pop_up_layout_on_calls_tab")
        )


def verify_display_home_screen_toggle_status_under_calling(device, status):
    if status.lower() not in ["on", "off"]:
        raise AssertionError(f"Illegal value for 'status': '{status}'")
    open_settings_page(device)
    time.sleep(display_time)
    if not common.click_if_present(device, settings_dict, "Calling"):
        swipe_till_end(device)
        swipe_till_end(device)
        common.wait_for_and_click(device, settings_dict, "Device_Settings")
        device_settings_keywords.advance_calling_option_oem(device)
        common.wait_for_element(device, settings_dict, "call_forwarding")
    common.wait_for_element(device, settings_dict, "display_on_home_screen")
    common.wait_for_element(device, settings_dict, "call_forwarding_display_on_home_screen_toggle")
    if common.is_lcp(device):
        swipe_till_end(device)

    if status == "on":
        common.verify_toggle_button(
            device, settings_dict, "call_forwarding_display_on_home_screen_toggle", desired_state=status
        )

    elif status == "off":
        common.verify_toggle_button(
            device, settings_dict, "call_forwarding_display_on_home_screen_toggle", desired_state=status
        )

    # come back to home screen page
    call_views_keywords.go_back_to_previous_page(device)


def verify_call_forwarding_option_in_call_forward_icon(device, verify_call_group="on"):
    if verify_call_group.lower() not in ["off", "on"]:
        raise AssertionError(f"Illegal value for 'verify_call_group': '{verify_call_group}'")
    time.sleep(action_time)
    if common.is_lcp(device):
        common.wait_for_and_click(device, settings_dict, "call_forwarding_icon_on_home_screen")
    elif not common.click_if_present(device, settings_dict, "forwarding_icon_on_calls_tab"):
        common.wait_for_and_click(device, settings_dict, "call_forwarding_icon_on_home_screen")

    common.wait_for_element(device, home_screen_dict, "forward_to_voicemail")
    common.wait_for_element(device, home_screen_dict, "forward_to_my_delegates")
    common.wait_for_element(device, home_screen_dict, "forward_to_contact_or_number")
    if verify_call_group == "on":
        common.wait_for_element(device, home_screen_dict, "forward_to_call_group")

    if common.is_lcp(device):
        calendar_keywords.scroll_down_device_setting_tab(device)
    common.wait_for_element(device, home_screen_dict, "dont_forward_calls")
    # To disimiss pop-up
    if common.is_lcp(device):
        device_setting_back(device)
    else:
        common.wait_for_and_click(device, home_screen_dict, "dont_forward_calls")
        if not common.is_element_present(device, people_dict, "people_tab_cap"):
            dismiss_call_forwarding_pop_up_on_home_screen(device)


def verify_call_forwarding_option_when_no_delegate_present_on_device(device):
    common.wait_for_and_click(device, settings_dict, "call_forwarding_icon_on_home_screen")
    common.wait_for_element(device, home_screen_dict, "dont_forward_calls")
    common.wait_for_element(device, home_screen_dict, "forward_to_voicemail")
    common.wait_while_present(device, home_screen_dict, "forward_to_my_delegates")
    common.wait_for_element(device, home_screen_dict, "forward_to_contact_or_number")
    common.wait_for_and_click(device, settings_dict, "call_forwarding_icon_on_home_screen")


def verify_call_forwarding_icon(device):
    time.sleep(action_time)
    if not common.is_element_present(device, settings_dict, "forwarding_icon_on_calls_tab"):
        common.wait_for_element(device, settings_dict, "call_forwarding_icon_on_home_screen")


def verify_call_forwarding_icon_should_not_appear_on_home_screen(device):
    if common.is_element_present(
        device, settings_dict, "call_forwarding_icon_on_home_screen"
    ) or common.is_element_present(device, settings_dict, "forwarding_icon_on_calls_tab"):
        raise AssertionError(f"{device} is after disable toggle also appearing call forwarding icon")


def verify_call_forwarding_status_on_calling(device, option, to_device=None):
    if option.lower() not in ["off", "voicemail", "contact_or_number", "delegate", "call_group"]:
        raise AssertionError(f"Illegal value for 'status': '{option}'")

    if to_device is not None:
        if ":" in to_device:
            devices, account = common.decode_device_spec(to_device)
            if account == "pstn_user":
                display_name = config["devices"][devices][account]["pstndisplay"]
            else:
                display_name = common.config["devices"][devices][account]["displayname"]
        else:
            display_name = common.device_displayname(to_device)

    open_settings_page(device)
    time.sleep(display_time)
    if not common.click_if_present(device, settings_dict, "Calling"):
        swipe_till_end(device)
        swipe_till_end(device)
        common.wait_for_and_click(device, settings_dict, "Device_Settings")
        device_settings_keywords.advance_calling_option_oem(device)

    common.wait_for_element(device, settings_dict, "call_forwarding")

    if option.lower() == "off":
        common.verify_toggle_button(device, settings_dict, "Call_forward_toggle", desired_state="off")

    elif option.lower() == "voicemail":
        common.wait_for_element(device, settings_dict, "call_forward_to")
        common.wait_for_element(device, settings_dict, "voicemail_option")

    elif option.lower() == "contact_or_number":
        common.wait_for_and_click(device, settings_dict, "call_forward_to")
        tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", display_name)
        common.wait_for_element(device, tmp_dict, "search_result_item_container", "xpath")

    elif option.lower() == "delegate":
        common.wait_for_element(device, settings_dict, "call_forward_to")
        common.wait_for_element(device, settings_dict, "my_delegates_option")

    elif option.lower() == "call_group":
        common.wait_for_element(device, settings_dict, "call_forward_to")
        common.wait_for_element(device, settings_dict, "call_group_option")

    # come back to home screen page
    call_views_keywords.go_back_to_previous_page(device)


def remove_all_delegates_on_device(devices):
    devices = devices.split(",")
    for device in devices:
        driver = obj.device_store.get(alias=device)
        navigate_to_manage_delegate_page(device)
        for i in range(5):
            common.wait_for_element(device, settings_dict, "manage_delegates_tab_text")
            if common.is_element_present(device, settings_dict, "admin_boss_list"):
                common.wait_for_and_click(device, settings_dict, "admin_boss_list")
                if config["devices"][devices]["model"].lower() == "gilbert":
                    swipe_till_end(devices)
                username = common.wait_for_element(device, settings_dict, "username_in_permission_tab").text
                common.wait_for_element(device, settings_dict, "delegate_actions_text")
                if common.is_element_present(device, settings_dict, "delete_delegates", "xpath"):
                    common.wait_for_and_click(device, settings_dict, "delete_delegates", "xpath")
                    print(f"{device}: Deleted delegate: {username}")
                else:
                    toggle_btn = common.wait_for_element(device, settings_dict, "permission_switch")
                    attr_status = toggle_btn.get_attribute("enabled")
                    if attr_status != "false":
                        raise AssertionError(f"{device}: Delegate user: '{username}' doesn't have option to delete")
                    print(f"{device}: User is a boss: '{username}'; Hence, no option to delete the user from list")
                    common.wait_for_and_click(device, common_dict, "back")
                WebDriverWait(driver, 10).until(
                    EC.staleness_of(common.wait_for_element(device, settings_dict, "username_in_permission_tab"))
                )


def verify_options_after_disabling_auto_restart_toggle_btn(device):
    common.wait_while_present(device, settings_dict, "automatically_toggle_btn", max_wait_attempts=3)


def verify_and_change_the_contact_on_forward_to_contact_or_number_on_home_screen(device, contact_device):
    if ":" in contact_device:
        devices, account = common.decode_device_spec(contact_device)
        if account == "pstn_user":
            display_name = config["devices"][devices][account]["pstndisplay"]
        else:
            display_name = common.config["devices"][devices][account]["displayname"]
    else:
        display_name = common.device_displayname(contact_device)

    if not (
        common.click_if_present(device, settings_dict, "call_forwarding_icon_on_home_screen")
        or common.click_if_present(device, settings_dict, "forwarding_icon_on_calls_tab")
    ):
        common.wait_for_and_click(device, settings_dict, "call_forwarding_pop_up_open_or_close_button")

    common.wait_for_and_click(device, home_screen_dict, "forward_to_contact_or_number")
    common.wait_for_and_click(device, settings_dict, "add_contact_option")
    common.wait_for_element(device, settings_dict, "search_contact_box").send_keys(display_name)
    common.hide_keyboard(device)
    temp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", display_name)
    common.wait_for_and_click(device, temp_dict, "search_result_item_container")
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")
    dismiss_call_forwarding_pop_up_on_home_screen(device)


def verify_send_feedback_page(device):
    open_settings_page(device)
    settings_keywords.swipe_till_end(device)
    common.wait_for_and_click(device, settings_dict, "Help")
    common.wait_for_element(device, settings_dict, "summarize_your_feedback")
    if common.is_lcp(device):
        _max_attempts = 4
        for i in range(_max_attempts):
            calendar_keywords.scroll_only_once(device)
    if config["devices"][device]["model"].lower() == "gilbert":
        swipe_till_end(device)
    common.wait_for_element(device, settings_dict, "allow_microsoft_to_contact_me_text")
    common.wait_for_element(device, settings_dict, "allow_microsoft_to_contact_me_toggle")
    common.wait_for_element(device, settings_dict, "attach_logs_to_help_troubleshoot_text")
    common.wait_for_element(device, settings_dict, "attach_logs_to_help_troubleshoot_toggle")


def give_feedback_to_microsoft(device):
    if common.is_lcp(device):
        calendar_keywords.scroll_down_device_setting_tab(device)
        calendar_keywords.scroll_down_device_setting_tab(device)
    if config["devices"][device]["model"].lower() == "gilbert":
        calendar_keywords.scroll_down_device_setting_tab(device)
        calendar_keywords.scroll_down_device_setting_tab(device)
    common.wait_for_and_click(device, settings_dict, "feedback_text_section")
    common.wait_for_element(device, settings_dict, "feedback_text_section").send_keys(
        config["Report_feedback"]["bug_details"]
    )
    common.hide_keyboard(device)
    if common.is_lcp(device):
        swipe_till_end(device)
        swipe_till_end(device)
    if config["devices"][device]["model"].lower() == "gilbert":
        swipe_till_end(device)
    common.change_toggle_button(device, settings_dict, "allow_microsoft_to_contact_me_toggle", desired_state="on")
    common.change_toggle_button(device, settings_dict, "attach_logs_to_help_troubleshoot_toggle", desired_state="on")
    common.wait_for_and_click(device, settings_dict, "send_bug")
    common.wait_while_present(device, settings_dict, "send_bug")


def verify_delegate_permissions_selectively(device, from_device, exclude_permission):
    if exclude_permission not in [
        "make_calls",
        "receive_calls",
        "change_call_settings",
        "join_calls",
        "pick_up_held_calls",
    ]:
        raise AssertionError(f"{device}: Wrong value for 'exclude_permission': '{exclude_permission}'")
    permission_dict = {
        "make_calls": "Make calls",
        "receive_calls": "Receive calls",
        "change_call_settings": "Change call and delegate settings",
        "join_calls": "Join active calls",
        "pick_up_held_calls": "Pick up held calls",
    }
    delegate_displayname = common.device_displayname(from_device)
    users = common.get_all_elements_texts(device, settings_dict, "user_title")
    if delegate_displayname not in users:
        raise AssertionError(
            f"{device}: Expected delegate user: '{delegate_displayname}' is not in list of delegate users: {users}"
        )
    search_result_xpath = common.get_dict_copy(
        calls_dict, "search_result_item_container", "config_display", delegate_displayname
    )
    common.wait_for_and_click(device, search_result_xpath, "search_result_item_container", "xpath")
    time.sleep(display_time)
    delegate_permissions_list = [
        "Make calls",
        "Receive calls",
        "Change call and delegate settings",
        "Join active calls",
        "Pick up held calls",
    ]
    permissions_title_list = common.get_all_elements_texts(device, settings_dict, "delete_delegates")
    permission_toggle_list = common.wait_for_element(
        device, settings_dict, "permission_switch", cond=EC.presence_of_all_elements_located
    )
    if permissions_title_list != delegate_permissions_list:
        raise AssertionError(
            f"{device}: Not all permissions are displayed: '{permissions_title_list}' for the user: {delegate_displayname}. Expected permissions: '{delegate_permissions_list}'"
        )
    permission_toggle_state_list = []
    for permission_toggle in permission_toggle_list:
        permission_toggle_state_list.append(permission_toggle.get_attribute("checked"))
    if permission_toggle_state_list[delegate_permissions_list.index(permission_dict[exclude_permission])] != "False":
        raise AssertionError(
            f"{device}: permission toggle for '{permission_dict[exclude_permission]}' is not disabled: '{permission_toggle_state_list[delegate_permissions_list.index(permission_dict[exclude_permission])]}'"
        )
    click_back(device)
    common.wait_for_element(device, settings_dict, "user_title")
