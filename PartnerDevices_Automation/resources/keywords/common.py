from functools import partial
import threading
import traceback
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, StaleElementReferenceException
from urllib3.exceptions import ProtocolError
import common
from initiate_driver import obj_dev as obj
from initiate_driver import config, root_console
from robot.libraries.BuiltIn import BuiltIn
import os
from io import open
import SignInOut
import settings_keywords
import call_keywords
import time
import subprocess
from datetime import datetime
from AccountSetup import AccountSetup
from Libraries.Selectors import load_json_file
from PIL import Image
import call_views_keywords
import tr_home_screen_keywords

display_time = 2
action_time = 3

obj_dev = AccountSetup.getInstance()
calls_dict = load_json_file("resources/Page_objects/Calls.json")
calendar_dict = load_json_file("resources/Page_objects/Calendar.json")
navigation_dict = load_json_file("resources/Page_objects/Navigation.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")
home_screen_dict = load_json_file("resources/Page_objects/Home_screen.json")
tr_Signin_dict = load_json_file("resources/Page_objects/tr_Signin.json")
tr_home_screen_dict = load_json_file("resources/Page_objects/tr_home_screen.json")
tr_console_signin_dict = load_json_file("resources/Page_objects/rooms_console_signin.json")
panels_home_screen_dict = load_json_file("resources/Page_objects/panels_homescreen.json")
lcp_homescreen_dict = load_json_file("resources/Page_objects/lcp_homescreen.json")
common_dict = load_json_file("resources/Page_objects/common.json")


def verify_device_users(device_list=None, user_list=None, retry=True):
    if isinstance(device_list, list):
        devices = device_list
    else:
        if device_list is None:
            devices = list(config["devices"].keys())
        else:
            devices = device_list.split(",")

    if user_list is None:
        users = ["None"] * len(devices)
    else:
        if isinstance(user_list, list):
            users = user_list
        else:
            users = user_list.split(",")
        # if len(users) > len(devices):
        #     raise AssertionError(f"More users ({len(users)}) than devices ({len(devices)}) specified")
    # Ok to trim devices back to specified users:
    devices = devices[: len(users)]

    print(" Devices : ", devices)
    device_list = ",".join(devices)
    print("users : ", users)
    user_list = ",".join(users)
    print("user_list : ", user_list)

    devices = device_list.split(",")
    users = user_list.split(",")
    signed_users = []
    signed_users_device = []
    for device, user in zip(devices, users):
        try:
            try:
                if not is_norden(device):
                    call_keywords.come_back_to_home_screen(device, disconnect=False)
                user_name = get_user_name(device)

            except Exception as e:
                print(f"{device}_Cannot identify home screen:{''.join(traceback.format_exception_only(type(e), e))}")
                settings_keywords.get_screenshot(name=f"{device}_before_verify_users")
                SignInOut.capture_cp_and_logcat_logs(device)
                print(f"{device}: Could not get user name, re-signining in. Check screenshot")
                obj_dev.re_setup_device_driver(device, config)
                SignInOut.sign_in(device_list=device, user_list=user)
                user_name = get_user_name(device)
                print(f"{device}: SUCCESS after re-signining in.")
        except Exception as e:
            print(f"{device}: FAILURE after re-signining in.")
            if retry is False:
                raise e
            verify_device_users(device, user, retry=False)
            return
        signed_users.append(user_name)
        signed_users_device.append(device)

    print("Signed Users : ", signed_users)
    print("Signed Users on Devices : ", signed_users_device)

    desired_users = []
    for device, user in zip(devices, users):
        if user == "None":
            user = None
        if user is not None:
            account = None
            if user.lower() == "pstn_user":
                account = "pstn_user"
            elif user.lower() == "cap_search_enabled":
                account = "cap_search_enabled"
            elif user.lower() == "cap_search_disabled":
                account = "cap_search_disabled"
            elif user.lower() == "meeting_user":
                account = "meeting_user"
            elif user.lower() == "user":
                account = "user"
            elif user.lower() == "delegate_user":
                account = "delegate_user"
            elif user.lower() == "gcp_user":
                account = "gcp_user"
            elif user.lower() == "cq_user":
                account = "cq_user"
            elif user.lower() == "cap_user":
                account = "cap_user"
            elif user.lower() == "hotdesk_disabled_user":
                account = "hotdesk_disabled_user"
            elif user.lower() == "premium_user":
                account = "premium_user"
            elif user.lower() == "standard_user":
                account = "standard_user"
            elif user.lower() == "pstn_disabled":
                account = "pstn_disabled"
            elif user.lower() == "auto_checkin_user":
                account = "auto_checkin_user"
            elif user.lower() == "longname_user":
                account = "longname_user"
        else:
            account = "user"
        username = config["devices"][device][account]["displayname"]
        desired_users.append(username)
    print("Desired Users :", desired_users)
    device_list_new = []
    user_list_new = []
    user_index = 0
    for signed, desired in zip(signed_users, desired_users):
        if signed != desired:
            if signed.lower() == desired.lower():
                print(
                    f"*ERROR* : Config error: Bad case-sensitive 'displayname': Configured: '{desired}', actual: '{signed}'."
                )
        if signed.lower().strip().replace(" ", "") != desired.lower().strip().replace(" ", ""):
            device_list_new.append(devices[user_index])
            user_list_new.append(users[user_index])
        else:
            print(f"Accepting configured username: {desired} as {signed.lower().strip().replace(' ', '')}")
        user_index += 1
    print("New device List : ", device_list_new)
    print("New User List : ", user_list_new)
    if len(device_list_new) != 0:
        SignInOut.sign_out(device_list=device_list_new)
        SignInOut.sign_in(device_list=device_list_new, user_list=user_list_new)
        if retry is True:
            verify_device_users(device_list_new, user_list_new, retry=False)


def get_user_name(device):
    print(f"{device}: Checking username on device")

    if is_norden(device):
        name = tr_home_screen_keywords.tr_get_user_name(device)

    elif is_panel(device):
        name = wait_for_element(device, panels_home_screen_dict, "room_name").text
    elif is_lcp(device):
        wait_for_and_click(device, lcp_homescreen_dict, "user_profile_picture")
        name = wait_for_element(device, lcp_homescreen_dict, "username").text
        common.wait_for_and_click(device, common_dict, "back")
    else:
        if not click_if_element_appears(device, navigation_dict, "Navigation"):
            if not is_portrait_mode_cnf_device(device):
                raise AssertionError(f"{device} couldn't open navigation menu")
            name = wait_for_element(device, home_screen_dict, "user_name").text
        else:
            name = wait_for_element(device, navigation_dict, "user_name").text
            wait_for_and_click(device, settings_dict, "user_displayname")
            wait_for_and_click(device, calls_dict, "Call_Back_Button")
            if not common.is_element_present(device, home_screen_dict, "call_tab"):
                if not common.is_element_present(device, calls_dict, "dialpad_tab"):
                    settings_keywords.swipe_left(device)
    print(f"{device}: username={name}")
    return name


def dial_hardkeys(device, hardkeys, acceptable_digits="+0123456789*#"):
    """Use ADB to dial the specified hard keys"""
    print(f"{device}: dial_hardkeys '{hardkeys}'")

    if common.is_element_present(device, calls_dict, "zero"):
        print(f"{device}: NOTE: dial_hardkeys: soft dialpad present and ignored")

    _udid = common.device_udid(device)

    for i in hardkeys:
        if i not in acceptable_digits:
            raise AssertionError(f"{device}: digit '{i}' is not acceptable in '{acceptable_digits}'")

        if i == "#":
            _keycode = "KEYCODE_POUND"
        elif i == "*":
            _keycode = "KEYCODE_STAR"
        elif i == "+":
            # longpress '0' for '+'
            _keycode = "--longpress KEYCODE_0"
        else:
            _keycode = f"KEYCODE_{i}"
        subprocess.call(
            f"adb -s {_udid} shell input keyevent {_keycode}",
            shell=True,
        )


def navigate_to_hamburger_menu(device):
    wait_for_and_click(device, navigation_dict, "Navigation")
    time.sleep(action_time)


def teardown_meeting_test_case(devices):
    device_list = devices.split(",")
    for device in device_list:
        print("device : ", device)
        common.click_if_present(device, calls_dict, "Call_Back_Button")
        time.sleep(2)
        if common.is_element_present(device, calendar_dict, "alert_message"):
            common.wait_for_and_click(device, calendar_dict, "discard_pop_up")


def device_type(device):
    devices = "consoles" if "console" in device else "devices"
    return devices


def device_displayname(device):
    device_name, account_type = decode_device_spec(device)
    devices = device_type(device)
    return config[devices][device_name][account_type]["displayname"]


def device_phonenumber(device):
    device_name, account_type = decode_device_spec(device)
    devices = device_type(device)
    return config[devices][device_name][account_type]["phonenumber"]


def device_pstndisplay(device):
    device_name, account_type = decode_device_spec(device)
    devices = device_type(device)
    return config[devices][device_name][account_type]["pstndisplay"]


def device_extention_number(device):
    device_name, account_type = decode_device_spec(device)
    devices = device_type(device)
    return config[devices][device_name][account_type]["extension"]


def device_username(device):
    device_name, account_type = decode_device_spec(device)
    devices = device_type(device)
    return config[devices][device_name][account_type]["username"]


def device_admin_credentials(device):
    device_name, _ = decode_device_spec(device)
    devices = device_type(device)
    _name = config[devices][device_name]["admin_username"]
    _pw = config[devices][device_name]["admin_password"]
    return _name, _pw


def device_model(device):
    device_name, _ = decode_device_spec(device)
    devices = device_type(device)
    return config[devices][device_name]["model"].lower()


def device_udid(device):
    device_name, _ = decode_device_spec(device)
    devices = device_type(device)
    return config[devices][device_name]["desired_caps"]["udid"]


def capture_logcat_logs(name, device_list=None):
    if isinstance(device_list, list):
        devices = device_list
    else:
        if device_list is None:
            devices = list(config["devices"].keys())
        else:
            devices = device_list.split(",")

    print("Devices : ", devices)

    name = filename_from_string(name)
    newpath = BuiltIn().get_variable_value("${OUTPUT DIR}") + "\\logcat_logs\\"
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    for device in devices:
        try:
            driver = obj.device_store.get(alias=device)
        except Exception as _no_driver:
            print(f"{device} No driver, logcat fetch skipped: {type(_no_driver).__name__}: {_no_driver}.")
            continue

        try:
            logs = driver.get_log("logcat")
        except Exception as _fetchfail:
            print(f"{device} Logcat fetch failed: {type(_fetchfail).__name__}: {_fetchfail}.")
            continue

        # The basic 'device crashed' crash sniffer:
        _crash_detected = False

        # These are InTune configuration error sniffers:
        _intune_bad_enroll_detected = False
        _intune_cap_limit_detected = False

        current_time = datetime.now().strftime("%H%M%S")
        log_messages = list(map(lambda log: log["message"], logs))

        file_name = "\\\\?\\" + newpath + current_time + "_" + name + "." + device + "_logcat.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            for item in log_messages:
                if "FATAL EXCEPTION" in item or "Fatal signal" in item:
                    _crash_detected = True
                if "DA_ENROLLMENT_DISABLED" in item:
                    _intune_bad_enroll_detected = True
                if "DEVICE_CAP_REACHED" in item:
                    _intune_cap_limit_detected = True
                f.write(f"{item}\n")

        if _crash_detected:
            report_crash(device, f"Logcat log, See {f.name}.")
        if _intune_bad_enroll_detected:
            # Sign-in fail message - Intune requires device enrollment to be enabled for this user, and it is not.
            print(f"*ERROR* {device} - 'DA_ENROLLMENT_DISABLED' detected: See {f.name}")
        if _intune_cap_limit_detected:
            # Sign-in fail message - Intune has recorded too many registrations for this device/user, you need to
            # manually clear these (as an admin, 'bulk delete' operaton on https://admin.microsoft.com, 'Show all', Endpoints, android devices).
            print(f"*ERROR* {device} - 'DEVICE_CAP_REACHED' detected: See {f.name}")


def report_crash(device_name: str, context: str):
    # Report as Test Execution Error
    print(f"*ERROR* {device_name} - CRASH DETECTED: {context}")
    # And insert the message in the keyword log
    print(f"{device_name} - CRASH DETECTED: {context}")


def wake_device_and_capture_screenshot(device):
    driver = obj.device_store.get(alias=device)
    subprocess.call(
        "adb -s {} shell input keyevent KEYCODE_WAKEUP".format(
            config["devices"][device]["desired_caps"]["udid"].split(":")[0]
        ),
        shell=True,
    )
    time.sleep(action_time)
    current_time = datetime.now().strftime("%H%M%S")
    file_name = "image_screen_" + current_time + ".png"
    driver.get_screenshot_as_file(file_name)
    # send_test_message(message=file_name)


def check_for_device_count(count):
    devices = list(config["devices"].keys())
    print("len(devices) : ", len(devices))
    print("count : ", count)
    if len(devices) >= int(count):
        pass
    else:
        assert False, "Required number of devices are not met by the setup for this testcase"


def get_bugreport_on_app_crash(name, device_list=None):
    if isinstance(device_list, list):
        devices = device_list
    else:
        if device_list is None:
            devices = list(config["devices"].keys())
        else:
            devices = device_list.split(",")
    print("Devices : ", devices)
    time.sleep(2)
    for device in devices:
        try:
            if not common.is_element_present(device, settings_dict, "close_app_btn"):
                continue
            report_crash(device, "UI - 'close_app_btn' is present!")
        except Exception as _teardown_failure:
            report_crash(device, "Appium failed, assuming App crashed!")

        # Use ADB to get a bugreport:
        newpath = BuiltIn().get_variable_value("${OUTPUT DIR}") + "\\bug_reports_for_app_crashes\\"
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        current_time = datetime.now().strftime("%H%M")
        newname = newpath + "bugreport_" + current_time + filename_from_string(name) + "_" + device
        cmd = "adb -s {} bugreport {}".format(
            (config["devices"][device]["desired_caps"]["udid"].split(":")[0]), newname
        )

        # Best effort - try to get ADB to get a bugreport:
        try:
            subprocess.check_output(cmd, shell=True)
            print(f"{device} bugreport in '{newname}'")
        except subprocess.CalledProcessError as cpe:
            print(f"{device} cannot create bugreport: '{cpe.output}'")

        # Best effort - try to acknowledge the app-crash:
        try:
            common.wait_for_and_click(device, settings_dict, "close_app_btn")
            # Done, App should be restarting
            continue
        except:
            # Here, appium cannot talk to the device. Do a full reset.
            print(f"{device} Appium failed, cannot dismiss any app crash pop-up - Full Reset the device")

        try:
            obj_dev.re_setup_device_driver(device, config)
            print(f"{device}: re_setup_device_driver sucessful")
        except Exception as e:
            print(f"{device}: Fatal: re_setup_device_driver failed with {type(e).__name__}: {e}")


def filename_from_string(name):
    name = (
        name.replace(" ", "_")
        .replace(":", "-")
        .replace("/", "_")
        .replace('"', "")
        .replace(".", "")
        .replace("'", "")
        .replace(",", "")
    )
    return name


def verify_hamburger_menu(device):
    print("device: ", device)
    driver = obj.device_store.get(alias=device)
    displayname = config["devices"][device]["user"]["displayname"]
    print("displayname : ", displayname)
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((MobileBy.ID, settings_dict["user_profile_pic"]["id"]))
        )
        print("Profile picture visible")
        try:
            elem1 = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((MobileBy.ID, settings_dict["user_designation"]["id"]))
            )
            print("User Designation is available : ", elem1.text)
        except Exception as e:
            print("Designation is not available for the user")
        elem2 = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((MobileBy.ID, settings_dict["user_displayname"]["id"]))
        )
        print("User displayname : ", elem2.text)
        if elem2.text == displayname:
            print("User displayname is matching in Hamburger menu")
        else:
            raise AssertionError("User displayname is not matching in Hamburger menu")
    except Exception as e:
        raise AssertionError("Xpath not found")


def is_norden(device):
    print(f"{device}: Selected device model is :", config["devices"][device]["model"])
    device_type = config["devices"][device]["model"].lower() in [
        "sammamish",
        "spokane",
        "oakland",
        "san francisco",
        "atlanta",
        "tucson",
        "irvine",
        "houston",
        "austin",
        "detroit",
        "everett",
        "eureka",
        "renton",
        "dearborn",
        "kodiak",
        "vernon",
        "aurora",
        "vancouver",
        "page",
        "georgia",
        "augusta",
        "jackson",
        "pasadena",
        "santamonica",
        "manchester",
        "sanantonio",
        "mesa",
        "palmer",
        "laredo",
        "barre"
    ]
    print(f"{device}: is_norden:", str(device_type))
    return device_type


_SUPPORTED_SELECTOR_STYLES = ["id", "id1", "command", "text", "xpath", "xpath1"]


def get_element_with_condition(
    device, selector_dict, selector_dict_key, selector_key, cond=EC.presence_of_element_located, wait_secs=1
):
    """
    Unconditionally fetch an element or raise
    Retry if ProtocolError encountered, recoverable.
    """
    if not isinstance(device, str):
        raise AssertionError(f"{device}: Expecting 'str', got '{type(device)}'.")

    driver = obj.device_store.get(device)
    selector = selector_dict[selector_dict_key][selector_key]
    _retry_attempts = 5
    _retry_sleep_secs = 3
    while True:
        try:
            if selector_key in ["id", "id1"]:
                return WebDriverWait(driver, wait_secs).until(cond((MobileBy.ID, selector)))
            if selector_key == "command":
                return WebDriverWait(driver, wait_secs).until(cond((MobileBy.ANDROID_UIAUTOMATOR, selector)))
            if selector_key == "text":
                command = f'new UiSelector().text("{selector}")'
                return WebDriverWait(driver, wait_secs).until(cond((MobileBy.ANDROID_UIAUTOMATOR, command)))
            return WebDriverWait(driver, wait_secs).until(cond((MobileBy.XPATH, selector)))
        except TimeoutException as _toerr:
            # _toerr.msg = f"{device}: " + _toerr.msg
            raise
        except WebDriverException as _wderror:
            _wderror.msg = f"{device}: " + _wderror.msg
            raise _wderror
        except ProtocolError as _perror:
            if _retry_attempts > 0:
                _retry_attempts = _retry_attempts - 1
                print(
                    f"{device}: ProtocolError, retry in {_retry_sleep_secs}, attempts left: {_retry_attempts}. {str(_perror)}"
                )
                time.sleep(_retry_sleep_secs)
                continue
            raise _perror


def get_all_elements_texts(device, selector_dict, selector_dict_key, selector_key=None):
    """
    Return a list containing the texts from all selector matches.
    """
    # Note: WebDriver magic: Instead of a 'WebElement', a 'list of WebElements' is
    #    returned when 'EC.presence_of_all_elements_located' is specified.
    _magic = EC.presence_of_all_elements_located

    element_list = []
    if selector_key is None:
        for _key in selector_dict[selector_dict_key]:
            if _key not in _SUPPORTED_SELECTOR_STYLES:
                print(f"{device}: Warning - get_all_elements_texts() ignoring unsupported selector key '{_key}'")
                continue
            try:
                element_list = get_element_with_condition(device, selector_dict, selector_dict_key, _key, cond=_magic)
                break
            except TimeoutException:
                continue
        if len(element_list) == 0:
            raise AssertionError(f"{device}: could not find any '{selector_dict_key}' elements")
    else:
        if not selector_key in _SUPPORTED_SELECTOR_STYLES:
            raise AssertionError(
                f"{device}: get_all_elements_texts() unsupported selector key '{selector_key}' specified"
            )
        try:
            element_list = get_element_with_condition(
                device, selector_dict, selector_dict_key, selector_key, cond=_magic
            )
        except TimeoutException:
            raise AssertionError(f"{device}: could not find any '{selector_dict_key}[{selector_key}]' elements")

    return_list = []
    try:
        for element in element_list:
            return_list.append(element.text)
    except StaleElementReferenceException:
        # While collecting element texts, the element went stale
        print(f"{device}: StaleElementReferenceException - UI changed while collecting elements texts")
        raise

    print(f"{device}: Text of '{selector_dict_key}' elements: {return_list}")
    return return_list


def is_element_present(
    device, selector_dict, selector_dict_key, selector_key=None, cond=EC.presence_of_element_located, silent=False
):
    """
    Return Element or False if specified element is present with specified element condition.
    """

    def single_selector_is_element_present(device, selector_dict, selector_dict_key, selector_key, cond):
        if selector_key not in _SUPPORTED_SELECTOR_STYLES:
            return False
        try:
            _element = get_element_with_condition(device, selector_dict, selector_dict_key, selector_key, cond=cond)
            if not silent:
                if _element:
                    print(f"{device}: element is present: '{selector_dict_key}[{selector_key}]'")
            return _element
        except TimeoutException:
            pass
        return False

    _element = None
    if selector_key is None:
        _has_valid_selector_key = False

        for _selector_key in selector_dict[selector_dict_key]:
            if _selector_key in _SUPPORTED_SELECTOR_STYLES:
                _has_valid_selector_key = True
                try:
                    if _element := single_selector_is_element_present(
                        device, selector_dict, selector_dict_key, _selector_key, cond
                    ):
                        break
                except TimeoutException:
                    pass
        if not _has_valid_selector_key:
            raise AssertionError(f"{device}: Selector dictionary '{selector_dict_key}' has no valid selector keys")
    else:
        if not selector_key in _SUPPORTED_SELECTOR_STYLES:
            raise AssertionError(f"{device}: Unsupported selector key '{selector_key}'")
        try:
            _element = single_selector_is_element_present(device, selector_dict, selector_dict_key, selector_key, cond)
        except TimeoutException:
            pass

    if not silent:
        if not _element:
            print(f"{device}: element is not present: '{selector_dict_key}'")

    return _element


def click_if_present(device, selector_dict, selector_dict_key, selector_key=None):
    """
    If element exists, click on it and return True
    Otherwise return False
    """

    def single_selector_click_if_present(device, selector_dict, selector_dict_key, selector_key):
        if selector_key not in _SUPPORTED_SELECTOR_STYLES:
            return False

        _element = is_element_present(
            device, selector_dict, selector_dict_key, selector_key, cond=EC.element_to_be_clickable
        )
        if not _element:
            return False

        # It's possible that the element disappears. Warn if it does - UI could be crashing...
        try:
            _element.click()
            return True
        except TimeoutException:
            print(f"{device}: WARN - UI changed, '{selector_dict_key}' disappeared after being present")
        except StaleElementReferenceException:
            print(f"{device}: WARN - UI changed, '{selector_dict_key}' became stale after being not stale")
        return False

    if selector_key is None:
        for _selector_key in selector_dict[selector_dict_key]:
            if single_selector_click_if_present(device, selector_dict, selector_dict_key, _selector_key):
                print(f"{device}: Clicked on '{selector_dict_key}' using '{_selector_key}'")
                return True
    elif single_selector_click_if_present(device, selector_dict, selector_dict_key, selector_key):
        print(f"{device}: Clicked on '{selector_dict_key}'")
        return True

    # print(f"{device}: '{selector_dict_key}' was not present")
    return False


def wait_for_element(
    device, selector_dict, selector_dict_key, selector_key=None, wait_attempts=30, cond=EC.presence_of_element_located
):
    """
    This method waits for, and returns the first element found in the specified selector dictionary.
    """
    attempt = 0
    for attempt in range(wait_attempts):
        if selector_key is None:
            for k in selector_dict[selector_dict_key]:
                if _element := is_element_present(device, selector_dict, selector_dict_key, k, cond, silent=True):
                    print(f"{device}: found '{selector_dict_key}[{k}]' on attempt {attempt + 1} of {wait_attempts}")
                    return _element
                # print(f"DEBUG: Attempt {attempt}: element '{selector_dict_key}[{key}]' not present")
        elif _element := is_element_present(device, selector_dict, selector_dict_key, selector_key, cond, silent=True):
            print(f"{device}: found '{selector_dict_key}[{selector_key}]' on attempt {attempt + 1} of {wait_attempts}")
            return _element

    # Dump screenshot and XML whenever this raises:
    #   This will dump if robot is invoked with:
    #       "-v dump_on_wait_fail:any"
    #   default is None:
    #       "-v dump_on_wait_fail:"
    _dump = BuiltIn().get_variable_value("${dump_on_wait_fail}")
    print(f"{device}: variable 'dump_on_wait_fail' is '{_dump}'")
    if _dump:
        BuiltIn().log_to_console(f"{device}: 'dump_on_wait_fail' - {selector_dict_key}__not_found")
        settings_keywords.get_screenshot(f"{selector_dict_key}__not_found", device_list=device, with_xml=True)

    raise AssertionError(f"{device}: could not find '{selector_dict_key}' after {attempt + 1} attempts")


def wait_for_and_click(device, selector_dict, selector_dict_key, selector_key=None, wait_attempts=30):
    """
    This method waits for the specified element to be clickable and clicks on it.
    """
    _el = wait_for_element(
        device,
        selector_dict,
        selector_dict_key,
        selector_key=selector_key,
        wait_attempts=wait_attempts,
        cond=EC.element_to_be_clickable,
    )
    try:
        _el.click()
    except StaleElementReferenceException:
        print(
            f"*WARN* {device}: WARN - UI changed, '{selector_dict_key}' became stale after being not stale, retrying..."
        )
        sleep_with_msg(device, 2, "Let element become stable")
        wait_for_element(
            device,
            selector_dict,
            selector_dict_key,
            selector_key=selector_key,
            wait_attempts=wait_attempts,
            cond=EC.element_to_be_clickable,
        ).click()

    print(f"{device}: clicked on '{selector_dict_key}'")


def wait_while_present(device_name, selector_dict, selector_dict_key, selector_key=None, max_wait_attempts=10):
    """
    This method waits for the specified element to disappear and raises if it doesn't.
    """
    attempt = 0
    for attempt in range(max_wait_attempts):
        if not is_element_present(device_name, selector_dict, selector_dict_key, selector_key, silent=True):
            return
        time.sleep(1)
    raise AssertionError(f"{device_name}: '{selector_dict_key}' still present after {attempt + 1} attempts")


def get_dict_copy(parent_dict, parent_dict_key, replace_token, replace_val):
    """
    Return a clone of the specified parent dictionary containing all
    valid selectors which contain the 'replace_token' replaced by 'replace_val'.
    """
    _new_parent_copy = dict()
    _new_child_dict = dict()

    for child_dict_key in parent_dict[parent_dict_key]:
        if not child_dict_key in _SUPPORTED_SELECTOR_STYLES:
            # ignore unknown keys
            continue
        if not replace_token in parent_dict[parent_dict_key][child_dict_key]:
            # In case we want to fix these:
            # print(f"*WARN* Problematic dictionary passed to get_dict_copy(),'{parent_dict_key}'['{child_dict_key}'] has no '{replace_token}' token.")
            continue

        # Looks good, add the selector with the replaced value:
        _new_child_dict[child_dict_key] = parent_dict[parent_dict_key][child_dict_key].replace(
            replace_token, replace_val
        )

    if len(_new_child_dict) == 0:
        raise AssertionError(f"Dictionary '{parent_dict_key}' has no valid selectors containing '{replace_token}'")

    _new_parent_copy[parent_dict_key] = _new_child_dict
    return _new_parent_copy


def kb_trigger_search(device, selector_dict, selector_dict_key, search_text, selector_key=None, wait_attempts=10):
    """
    Trigger search using virtual keyboard events.
    Note: The element 'selector_dict_key' must have property 'clickable' == True
    """
    # Bring up the virtual keyboard for the search box, type the name, and close the keyboard.
    common.wait_for_and_click(device, selector_dict, selector_dict_key, selector_key, wait_attempts)

    subprocess.call(
        "adb -s {} shell input keyboard text '{}'".format(
            config["devices"][device]["desired_caps"]["udid"].split(":")[0], search_text
        ),
        shell=True,
    )
    common.hide_keyboard(device)


def hide_keyboard(device):
    """Hide the device soft keyboard"""
    print(f"{device}: hide keyboard")
    driver = obj.device_store.get(device)
    driver.hide_keyboard()


def sleep_with_msg(device, wait_seconds, why_message):
    """Sleep after emitting a message why"""
    print(f"{device}: sleeping {wait_seconds}: {why_message}")
    time.sleep(wait_seconds)


def is_panel(device):
    print("Selected Device is :", config["devices"][device]["model"])
    print("Device :", device)
    device_type = config["devices"][device]["model"].lower() in [
        "westchester",
        "beverly hills",
        "brooklyn",
        "arlington",
        "flint",
        "savannah",
        "hollywood",
        "richland",
        "surprise",
    ]
    return device_type


def is_lcp(device):
    print(f"Selected device is {device}:{config['devices'][device]['model']}")
    device_type = config["devices"][device]["model"].lower() in ["malibu", "glendale", "bothell", "malibu_13"]
    return device_type


def perform_drag_and_drop(
    device,
    src_element_name,
    src_selector_dict,
    src_selector_dict_key,
    dest_element_name,
    dest_selector_dict,
    dest_selector_dict_key,
):
    print("Devices for Action :", device)
    driver = obj.device_store.get(alias=device)
    source_element = wait_for_element(device, src_selector_dict, src_selector_dict_key)
    print(f"{src_element_name} source element is :", source_element)
    destination_element = wait_for_element(device, dest_selector_dict, dest_selector_dict_key)
    print(f"{dest_element_name} destination element is :", destination_element)
    try:
        actions = TouchAction(driver)
        actions.long_press(source_element).move_to(destination_element).release().perform()
    except Exception as e:
        raise AssertionError("Unable to move the {src_element_name} tab from one section to another section", e)


def is_touch_console(console):
    print("Selected console is :", config["consoles"][console]["model"])
    print("Device type :", console)
    device_type = config["consoles"][console]["model"].lower() in [
        "fresno",
        "yakima",
        "lansing",
        "dallas",
        "sequim",
        "pittsford",
        "denver",
        "athens",
        "tempe",
        "wrangell",
    ]
    return device_type


def verify_console_users(device_list=None, console_list=None, user_list=None, retry=True):
    if device_list is None:
        devices = list(config["devices"].keys())
        if user_list is None:
            users = ["None"] * len(devices)
        else:
            users = user_list.split(",")
    else:
        devices = device_list.split(",")
        users = user_list.split(",")
    if console_list is None:
        consoles = list(config["consoles"].keys())
        if user_list is None:
            users = ["None"] * len(consoles)
        else:
            users = user_list.split(",")
    else:
        consoles = console_list.split(",")
        users = user_list.split(",")
    print("devices : ", devices)
    device_list = ",".join(devices)
    print("consoles : ", consoles)
    console_list = ",".join(consoles)
    print("Users : ", users)
    user_list = ",".join(users)
    print("User list : ", user_list)
    devices = device_list.split(",")
    consoles = console_list.split(",")
    users = user_list.split(",")
    signed_users = []
    signed_users_console = []
    for device, console, user in zip(devices, consoles, users):
        try:
            try:
                user_name = get_console_user_name(console)
                signed_users.append(user_name)
                signed_users_console.append(console)
            except Exception as e:
                print("Could not get user name, re-signing in. Check screenshot")
                capture_screenshot(name=f"{console}_before_verify_users")
                SignInOut.capture_console_cp_and_logcat_logs(console)
                obj_dev.re_setup_console_driver(console, config, root_console)
                SignInOut.sign_in_console(console_list=console, user_list=user)
                SignInOut.get_device_pairing_code(device_list=device, console_list=console, user_list=user)
                user_name = get_console_user_name(console)
                signed_users.append(user_name)
                signed_users_console.append(console)
                capture_screenshot(name=f"{console}_after_verify_users")
        except Exception as e:
            if retry is True:
                verify_console_users(device, console, user, retry=False)
            else:
                pass
    print("Signed Users : ", signed_users)
    print("Signed Users on Consoles : ", signed_users_console)
    desired_users = []
    for device, console, user in zip(devices, consoles, users):
        if user == "None":
            user = None
        if user is not None:
            account = None
            if user.lower() == "pstn_user":
                account = "pstn_user"
            elif user.lower() == "meeting_user":
                account = "meeting_user"
            elif user.lower() == "user":
                account = "user"
        else:
            account = "user"
        username = config["consoles"][console][account]["displayname"]
        desired_users.append(username)
    print("Desired Users :", desired_users)
    device_list_new = []
    console_list_new = []
    user_list_new = []
    for signed, desired in zip(signed_users, desired_users):
        if signed != desired:
            device_list_new.append(devices[signed_users.index(signed)])
            console_list_new.append(consoles[signed_users.index(signed)])
            user_list_new.append(users[signed_users.index(signed)])
        else:
            pass

    print("New device List : ", device_list_new)
    print("New Console List : ", console_list_new)
    print("New User List : ", user_list_new)
    if len(console_list_new) != 0:
        SignInOut.sign_out_console(console_list=console_list_new)
        SignInOut.sign_in_console(console_list=console_list_new, user_list=user_list_new)
        SignInOut.get_device_pairing_code(
            device_list=device_list_new,
            console_list=console_list_new,
            user_list=user_list_new,
        )
        if retry is True:
            verify_device_users(device_list_new, user_list_new, retry=False)
        else:
            raise AssertionError(
                f"{console_list}: unable to complete sign in and pairing Sign-in Failed after retrying"
            )


def get_console_user_name(console):
    print("Checking username on console device : ", console)
    driver = obj.device_store.get(alias=console)
    name = (
        WebDriverWait(driver, 30)
        .until(EC.presence_of_element_located((MobileBy.ID, tr_console_signin_dict["room_user_name"]["id"])))
        .text
    )
    print("Name : ", name)
    return name


def logcat_logs_capture(name, console_list=None):
    if isinstance(console_list, list):
        consoles = console_list
    else:
        if console_list is None:
            consoles = list(config["consoles"].keys())
        else:
            consoles = console_list.split(",")
    name = filename_from_string(name)

    print("Consoles : ", consoles)
    new_path = BuiltIn().get_variable_value("${OUTPUT DIR}") + "\\console_logcat_logs\\"
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    for console in consoles:
        driver = obj.device_store.get(alias=console)
        logs = driver.get_log("logcat")
        log_messages = list(map(lambda log: log["message"], logs))
        file_name1 = "\\\\?\\" + new_path + name + console + "_logcat.txt"
        with open(file_name1, "w", encoding="utf-8") as f:
            for item in log_messages:
                item = item.encode().decode()
                f.write("{}\n".format(item))
    pass


def capture_screenshot(name, console_list=None, with_xml=True):
    if isinstance(console_list, list):
        consoles = console_list
    else:
        if console_list is None:
            consoles = list(config["consoles"].keys())
        else:
            consoles = console_list.split(",")
    name = filename_from_string(name)

    print("name : ", name)
    print("Consoles : ", consoles)
    img_list = []
    xml_list = {}
    for console in consoles:
        driver = obj.device_store.get(alias=console)
        file_name = console + ".png"
        driver.get_screenshot_as_file(file_name)
        img_list.append(file_name)
        if with_xml:
            xml_list[console] = driver.page_source.encode("utf-8")
    images = [Image.open(x) for x in img_list]
    widths, heights = list(zip(*(i.size for i in images)))
    total_width = sum(widths)
    max_height = max(heights)
    new_im = Image.new("RGB", (total_width, max_height))
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]
    current_time = datetime.now().strftime("%H%M%S")
    file_name = name + "_" + current_time + ".png"
    new_path = BuiltIn().get_variable_value("${OUTPUT DIR}") + "\\console_screenshots\\"
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    new_im.save(new_path + file_name)
    BuiltIn().log(message="<image src=screenshots\\" + file_name + ' width="90%">', html=True)
    for console in consoles:
        try:
            os.remove(console + ".png")
        except Exception as e:
            print(f"*WARN* Unable to clean temporary file: {console + '.png'}: {str(e)}")
        if with_xml:
            try:
                file_name1 = "\\\\?\\" + new_path + file_name + "_" + console + ".xml"
                with open(file_name1, "wb") as xml_file:
                    xml_file.write(xml_list[console])
            except Exception as e:
                print(f"*WARN* Unable to write ui XML log! : {str(e)}")
    pass


def get_device_name_list(count):
    _device_names = list(config["devices"].keys())
    if len(_device_names) < int(count):
        raise AssertionError(f"Config error: {count} devices requested, but only {len(_device_names)} available")
    return _device_names[0 : int(count)]


def is_portrait_mode_cnf_device(device):
    driver = obj.device_store.get(alias=device)
    window_size = driver.get_window_size()
    height = window_size["height"]
    width = window_size["width"]
    if height > width:
        print(f"{device} is a portrait mode device")
        return True
    return False


def click_if_element_appears(device, selector_dict, selector_dict_key, max_attempts=15):
    """
    This method waits for the specified element to be clickable, clicks on it if found and returns True.
    Else, returns False
    """
    attempt = 0
    for attempt in range(1, max_attempts):
        if click_if_present(device, selector_dict, selector_dict_key):
            print(f"{selector_dict_key} appeared on attempt {attempt} of {max_attempts}")
            return True
        time.sleep(1)
    print(f"{device}: '{selector_dict_key}' did not appear after {attempt + 1} attempts")
    return False


def is_phone(device):
    device_model = config["devices"][device]["model"].lower()
    print(f"Device {device}, model '{device_model}'")
    device_type = device_model in [
        "phoenix",
        "scottsdale",
        "gilbert",
        "chandler",
        "long island",
        "queens",
        "olympia",
        "seattle",
        "redmond",
        "san jose",
        "santa cruz",
        "riverside",
        "bakersfield",
        "kirkland",
        "riverside_13",
        "santa cruz_13",
        "bakersfield_13",
    ]
    return device_type


def verify_devices_configured_in_panels_setup(device_list=None):
    if device_list is not None:
        device_list = device_list.split(",")
        if len(device_list) != 1 and device_list[0] != list(config["devices"].keys())[0]:
            raise AssertionError(f"Specified list does not start with the configured list: {device_list}")
    else:
        device_list = list(config["devices"].keys())
    if len(device_list) > 4:
        raise AssertionError(f"Required '5' devices but found '{len(device_list)}' devices")
    if len(device_list) == 1:
        verify_device_category(device_list[0], "panel")
    elif len(device_list) == 2:
        verify_device_category(device_list[0], "panel")
        verify_device_category(device_list[1], "norden")
    elif len(device_list) == 3:
        verify_device_category(device_list[0], "panel")
        verify_device_category(device_list[1], "norden")
        verify_device_category(device_list[2], "phone")
    elif len(device_list) == 4:
        verify_device_category(device_list[0], "panel")
        verify_device_category(device_list[1], "norden")
        verify_device_category(device_list[2], "phone")
        verify_device_category(device_list[3], "panel")


def verify_device_category(device, category):
    if category.lower() not in ["phone", "panel", "norden"]:
        raise AssertionError(f"Unexpected value for device category: {category}")
    if category.lower() == "panel":
        if is_panel(device):
            return
    if category.lower() == "norden":
        if is_norden(device):
            return
    if category.lower() == "phone":
        if is_phone(device):
            return
    raise AssertionError(f"{device} is not a {category}")


def verify_device_users_in_panels_setup(device_list=None):
    if device_list is None:
        device_list = list(config["devices"].keys())
    else:
        device_list = device_list.split(",")
    if len(device_list) == 4:
        panel_login_account1 = config["devices"][device_list[0]]["user"]["username"]
        rooms_login_account1 = config["devices"][device_list[1]]["user"]["username"]
        phone_login_account = config["devices"][device_list[2]]["user"]["username"]
        panel_login_account2 = config["devices"][device_list[3]]["user"]["username"]
        if (
            panel_login_account1 != rooms_login_account1
            and panel_login_account1 != panel_login_account2
            and rooms_login_account1 == phone_login_account
        ):
            raise AssertionError(
                f"Panels login account and Rooms login account are expected to be same, but found:\n Panels login account1: {panel_login_account1}\tRooms login account1: {rooms_login_account1}\n Panels login account2: {panel_login_account2}\nPhones login account is expected to be different than panels login account, but found: {phone_login_account}"
            )
    if len(device_list) == 3:
        panel_login_account = config["devices"][device_list[0]]["user"]["username"]
        rooms_login_account = config["devices"][device_list[1]]["user"]["username"]
        phone_login_account = config["devices"][device_list[2]]["user"]["username"]
        if panel_login_account != rooms_login_account and rooms_login_account == phone_login_account:
            raise AssertionError(
                f"Panels login account and Rooms login account are expected to be same, but found:\n Panels login account: {panel_login_account}\tRooms login account: {rooms_login_account}\nPhones login account is expected to be different than panels login account, but found: {phone_login_account}"
            )
    elif len(device_list) == 2:
        panel_login_account = config["devices"][device_list[0]]["user"]["username"]
        rooms_login_account = config["devices"][device_list[1]]["user"]["username"]
        if panel_login_account != rooms_login_account:
            raise AssertionError(
                f"Panels login account and Rooms login account are expected to be same, but found:\n Panels login account: {panel_login_account}\tRooms login account: {rooms_login_account}"
            )


def capture_bugreport_post_run(device_list=None):
    if "capture_bug_reports_post_run" not in config.keys() or config["capture_bug_reports_post_run"].lower() == "false":
        print("Bug reports collection post the automation run hasn't been enabled in the config")
        return
    if isinstance(device_list, list):
        devices = device_list
    else:
        if device_list is None:
            devices = list(config["devices"].keys())
        else:
            devices = device_list.split(",")
    print("Devices : ", devices)
    for device in devices:
        newpath = BuiltIn().get_variable_value("${OUTPUT DIR}") + "\\bug_reports\\"
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        current_time = datetime.now().strftime("%H%M")
        newname = newpath + "bugreport_" + current_time + "_" + device
        cmd = "adb -s {} bugreport {}".format(
            (config["devices"][device]["desired_caps"]["udid"].split(":")[0]), newname
        )
        try:
            subprocess.check_output(cmd, shell=True)
            print(f"{device} bugreport in '{newname}'")
        except subprocess.CalledProcessError as cpe:
            print(f"{device} cannot create bugreport: '{cpe.output}'")


def is_ecs_enabled():
    if "ecs_flag" not in config.keys() or config["ecs_flag"] == "disabled":
        return False
    if config["ecs_flag"] != "enabled":
        raise AssertionError(f"'ecs_flag' field in config has unexpected value: {config['ecs_flag']}")
    # ECS flag is enabled for these accounts
    return True


def decode_device_spec(device):
    """
    This method decodes a 'device' specifier.
    Any device specifier can be encoded as '[device name]:[account type]'.
    If not specified, the default account type is 'user'.
    It returns device name and account type.
    """
    if type(device) != str:
        raise AssertionError(f"'{device}' is not a str type")

    _pieces = device.split(":")

    device_name = _pieces[0]

    if len(_pieces) > 1:
        account_type = _pieces[1]
    else:
        account_type = "user"

    # Sanity checks, test for KeyError:
    devices = device_type(device)

    if device_name not in config[devices]:
        raise AssertionError(f"Config error: referenced device: '{device_name}' in not defined")
    if account_type not in config[devices][device_name]:
        raise AssertionError(f"Config error: device '{device_name}' has no '{account_type}' defined")

    return device_name, account_type


def get_credentials(device):
    """
    This method fetchs user credentials associated with the specified device.
    It returns username, password and account type.
    """
    if type(device) != str:
        raise AssertionError(f"'{device}' is not a str type")

    device_name, account_type = decode_device_spec(device)

    # Sanity checks, test for KeyError:
    if not config["devices"][device_name][account_type]["username"]:
        raise AssertionError(f"Config error: device '{device}' has no 'username' defined")
    if not config["devices"][device_name][account_type]["password"]:
        raise AssertionError(f"Config error: device '{device}' has no 'password' defined")

    username = config["devices"][device_name][account_type]["username"]
    password = config["devices"][device_name][account_type]["password"]

    return username, password, device_name, account_type


def capture_config_details():
    """To disable config capturing for partners"""
    if "capture_config" not in config.keys() or config["capture_config"].lower() == "enabled":
        return True
    return False


def is_screen_size_7_inch_or_more(device):
    if config["devices"][device]["model"].lower() in [
        "redmond",
        "san jose",
        "long island",
        "queens",
    ]:
        # "santa cruz","bakersfield" removed due to this bug 3318018
        print("device have 7 inch and above screen size")
        return True
    return False


def is_hard_dial_pad_present(device):
    if config["devices"][device]["model"].lower() in [
        "riverside",
        "riverside_13",
        "bakersfield",
        "bakersfield_13",
        "santa cruz",
        "santa cruz_13",
        "gilbert",
    ]:
        print(f"{device}: is having Hard Keys Dial Pad")
        return True
    return False


def is_conf(device):
    device_type = config["devices"][device]["model"].lower() in ["tacoma", "manhattan", "berkely"]
    print(f"{device} is_conf={device_type}")
    return device_type


def return_to_home_screen(device_list):
    devices = device_list.split(",")
    for device in devices:
        call_views_keywords.go_back_to_previous_page(device)
        time.sleep(2)
        common.click_if_present(device, home_screen_dict, "home_bar_icon")
        call_views_keywords.go_back_to_previous_page(device)


class ChildThreadError(Exception):
    """One or more child threads raised exceptions."""

    def __init__(self, msg):
        self.msg = msg


def determine_function_name(function):
    function_name = str(function)
    if type(function) == partial:
        function = function.func
    if hasattr(function, "func_name"):
        function_name = function.func_name
    elif hasattr(function, "__name__"):
        function_name = function.__name__
    return function_name


def run_parallel(device_list, func, *args, **kwargs) -> list:
    """
    Execute 'func' for each of the keys in 'device_list', on separate threads.
        When threads are finished:
            results are reported to caller (a list, same order as the keys) OR
            a SINGLE 'composite' ChildThreadError is raised.

        NOTE: The first argument to 'func' MUST be a device name (or deviceName:role).
    """

    def threaded_child(d_name: str, results: dict, real_func, *_args, **_kwargs):
        """
        This wrapper hides the 'results' linkage used between the parent and thread child.
        """
        try:
            results[d_name]["result"] = real_func(d_name, *_args, **_kwargs)
        except Exception as ex:
            results[d_name]["result"] = ex

    def format_thread_exception(d_name: str, exception):
        """
        Return an exception string which can be concatenated with
            others to form a 'summary' exception message for multiple threads.
        """
        tb_only = traceback.format_tb(exception.__traceback__)
        ex_only = "".join(traceback.format_exception_only(type(exception), exception))

        return "----" + d_name + ":\n  " + "".join(tb_only).strip() + f"\n  {ex_only.strip()}\n"

    if device_list is None:
        # ISSUE: We should not take this dependency on 'config', raise instead:
        # device_list = list(config["devices"].keys())
        raise AssertionError("No thread list specified")
    elif isinstance(device_list, str):
        device_list = device_list.split(",")
    elif not isinstance(device_list, list):
        raise AssertionError(f"'device_list' unexpected type: '{type(device_list).__name__}'")

    _func_name = determine_function_name(func)
    print(f"run_parallel: device_list={device_list}, func={_func_name}")

    # Create and initialize the parent/child result relay dictionary:
    thread_dict = {}
    for device_name in device_list:
        thread_dict[device_name] = {
            "thread": threading.Thread(
                target=threaded_child,
                name=device_name + "_thread",
                args=(device_name, thread_dict, func, *args),
                kwargs=kwargs,
            ),
            "result": None,
        }

    # Start child threads:
    for device_name in device_list:
        thread_dict[device_name]["thread"].start()

    # Wait for child threads to finish:
    # Future: This 'join' is sequential.
    #   We could possibly do any(), and early-abort all others on failure...
    for device_name in device_list:
        thread_dict[device_name]["thread"].join()

    # Assemble composite results/exceptions:
    all_errors = ""
    all_failed_names = []
    ret_list = []
    for device_name in device_list:
        _retval = thread_dict[device_name]["result"]
        if isinstance(_retval, Exception):
            all_errors = all_errors + format_thread_exception(device_name, _retval)
            all_failed_names.append(device_name)
        else:
            ret_list.append(_retval)

    # And return/raise the composite:
    if len(all_errors) > 1:
        which = '"' + '", "'.join(all_failed_names) + '"'
        raise ChildThreadError(f"'{_func_name}' ({which}) failed:\n" + all_errors.strip())

    # All threads completed:
    print(f"run_parallel: {_func_name} complete. results={ret_list}")
    return ret_list


def tap_outside_the_popup(device, container_element):
    driver = obj.device_store.get(alias=device)
    device_size = driver.get_window_size()
    device_height = device_size["height"]
    device_width = device_size["width"]
    time.sleep(display_time)
    print("Device co-ordinates : ", device_width, device_height)

    # Getting the location of the container_element x and y
    c_location_x = container_element.location["x"]
    c_location_y = container_element.location["y"]
    print(f"container coordinates location: ", c_location_x, c_location_y)

    # Getting the size of the container_element width and height
    c_size_width = container_element.size["width"]
    c_size_height = container_element.size["height"]
    print(f"Size of the container: ", c_size_width, c_size_height)

    if "console" not in device:
        if common.is_lcp(device):
            if c_location_x >= 0:
                ele_tap_x = c_size_width + 10

            if c_location_y >= 0:
                ele_tap_y = c_size_width + 10

            try:
                driver.tap([(ele_tap_x, ele_tap_y)])
                print(f"{device}: Tapped the coordinates: ", ele_tap_x, ele_tap_y)
            except Exception as e:
                print(f"Error tapping coordinates: \n{traceback.format_exc()}")
            return

    if c_location_x <= 0:
        ele_tap_x = c_size_width - 10
    elif c_location_x >= device_width:
        ele_tap_x = c_location_x - 10
    else:
        ele_tap_x = c_location_x - 10

    if c_location_y <= 0:
        ele_tap_y = c_size_height + 10
    elif c_location_y >= device_height:
        ele_tap_y = c_location_y - 10
    else:
        ele_tap_y = device_height - 10

    if ele_tap_x >= device_width:
        ele_tap_x = device_width - 10
    elif ele_tap_y >= device_height:
        ele_tap_y = device_height - 10

    try:
        driver.tap([(ele_tap_x, ele_tap_y)])
        print(f"{device}: Tapped the coordinates: ", ele_tap_x, ele_tap_y)
    except Exception as e:
        print(f"Error tapping coordinates: \n{traceback.format_exc()}")


def change_toggle_button(device, sel_dict, sel_dict_key, desired_state, must_change=False):
    # Check/Uncheck a toggle button.
    # If 'must_change' is True and the toggle is already in 'desired_state', raise
    if desired_state.lower() not in ["on", "off"]:
        raise AssertionError(f"{device}: Illegal value for 'desired_state': {desired_state}")

    if desired_state.lower() == "on":
        desired_state = "true"
    else:
        desired_state = "false"

    toggle_button = common.wait_for_element(device, sel_dict, sel_dict_key)
    actual_checked_state = toggle_button.get_attribute("checked").lower()
    if actual_checked_state != desired_state:
        toggle_button.click()
        toggle_button = common.wait_for_element(device, sel_dict, sel_dict_key)
        actual_checked_state = toggle_button.get_attribute("checked").lower()
        if actual_checked_state != desired_state:
            raise AssertionError(
                f"{device}: Toggle button '{sel_dict_key}' did not change after clicking. Expected '{desired_state}', actual '{actual_checked_state}'"
            )
    elif must_change:
        raise AssertionError(f"{device}: Toggle button '{sel_dict_key}' is already '{actual_checked_state}'")

    print(f"{device}: Toggle button '{sel_dict_key}' is now '{actual_checked_state}'")


def verify_toggle_button(device, sel_dict, sel_dict_key, desired_state):
    if desired_state.lower() not in ["on", "off"]:
        raise AssertionError(f"{device}: Illegal value for 'desired_state': {desired_state}")

    if desired_state.lower() == "on":
        desired_state = "true"
    else:
        desired_state = "false"

    toggle_button = common.wait_for_element(device, sel_dict, sel_dict_key)
    actual_checked_state = toggle_button.get_attribute("checked").lower()
    if actual_checked_state != desired_state:
        raise AssertionError(
            f"{device}: Toggle button '{sel_dict_key}' is not in desired state:{desired_state} actual state:'{actual_checked_state}'"
        )
    else:
        print(f"Toggle is already in desired state: {desired_state}")


def is_portrait_conf(device):
    device_type = config["devices"][device]["model"].lower() in ["tacoma", "berkely"]
    print(f"{device} is_portrait_conf={device_type}")
    return device_type


def get_adb_output(device, adb_command):
    _ret = subprocess.check_output(f"adb -s {device_udid(device)} {adb_command}", shell=True, encoding="utf-8").strip()
    return _ret


def device_privateline_number(device):
    device_name, account_type = decode_device_spec(device)
    devices = device_type(device)
    return config[devices][device_name][account_type]["privatelinenumber"]


def check_clickable_state(device, sel_dict, sel_dict_key, desired_state):
    element_time = common.wait_for_element(device, sel_dict, sel_dict_key)
    actual_clickable_state = element_time.get_attribute("clickable").lower()
    if actual_clickable_state != desired_state:
        raise AssertionError(
            f"{device}: {sel_dict_key} did not change after clicking. Expected :'{desired_state}', actual :'{actual_clickable_state}'"
        )
