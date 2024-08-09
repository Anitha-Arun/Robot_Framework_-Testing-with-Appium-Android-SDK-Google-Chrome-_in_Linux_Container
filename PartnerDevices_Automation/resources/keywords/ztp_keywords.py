import time
import common
from Libraries.Selectors import load_json_file
from initiate_driver import config

display_time = 2
action_time = 3

ztp_dict = load_json_file("resources/Page_objects/ztp.json")
signin_dict = load_json_file("resources/Page_objects/Signin.json")
device_settings_dict = load_json_file("resources/Page_objects/Device_settings.json")
calls_dict = load_json_file("resources/Page_objects/Calls.json")
home_screen_dict = load_json_file("resources/Page_objects/Home_screen.json")
tr_calls_dict = load_json_file("resources/Page_objects/tr_calls.json")
common_dict = load_json_file("resources/Page_objects/Common.json")
sign_dict = load_json_file("resources/Page_objects/Signin.json")
tr_Signin_dict = load_json_file("resources/Page_objects/tr_Signin.json")


def verify_ztp_signin_ui(device):
    common.wait_for_element(device, ztp_dict, "Step1_text_on_signin_page")
    common.wait_for_element(device, ztp_dict, "Step2_text_on_signin_page")
    timer_text = "Code expires in 04:59"
    if not common.click_if_present(device, signin_dict, "refresh_code_button"):
        if not common.is_element_present(device, signin_dict, "dfc_login_code"):
            raise AssertionError(f"{device} : DFC code expiry timeout is not displayed as expected")
    common.wait_for_element(device, signin_dict, "dfc_login_code")
    timer_info = common.wait_for_element(device, ztp_dict, "dfc_code_start_expiry_time", wait_attempts=600).text
    print("Timer text is : ", timer_info)
    if timer_info != timer_text:
        if "Code expires in 04:5" not in timer_info:
            if "Code expires in " not in timer_info:
                raise AssertionError(f"{device} : DFC code expiry timeout is not displayed 5 minutes before expiry")
    common.wait_for_element(device, signin_dict, "sign_in_on_the_device")


def verify_settings_from_signin_page(device):
    common.wait_for_and_click(device, device_settings_dict, "fre_partner_settings")
    common.wait_for_element(device, ztp_dict, "Cloud_option")
    common.wait_for_element(device, ztp_dict, "Provision_device")
    common.wait_for_element(device, ztp_dict, "Report_an_issue")
    common.wait_for_element(device, ztp_dict, "Device_settings")


def close_settings_window_from_signin_page(device, action="close"):
    if action.lower() not in ["verify", "close"]:
        raise AssertionError(f"Unexpected value for action : {action}")
    if action.lower() == "verify":
        common.wait_for_element(device, ztp_dict, "Close_icon")
    elif action.lower() == "close":
        common.wait_for_and_click(device, ztp_dict, "Close_icon")


def verify_teams_app_signin_page(device):
    common.wait_for_element(device, ztp_dict, "Step1_text_on_signin_page")
    common.wait_for_element(device, ztp_dict, "Step2_text_on_signin_page")
    if not common.is_element_present(device, signin_dict, "dfc_login_code"):
        common.wait_for_element(device, signin_dict, "refresh_code_button")
    common.wait_for_element(device, signin_dict, "sign_in_on_the_device")


def verify_cloud_option(device):
    common.wait_for_and_click(device, ztp_dict, "Cloud_option")
    common.wait_for_element(device, ztp_dict, "Public")
    common.wait_for_element(device, ztp_dict, "GCC")
    common.wait_for_element(device, ztp_dict, "GCC_High")
    if "consoles" not in config:
        common.wait_for_element(device, ztp_dict, "GCC_DoD")
    common.wait_for_element(device, ztp_dict, "Back_button")


def navigate_back_to_signin_page_form_cloud(device):
    common.wait_for_and_click(device, ztp_dict, "Back_button")
    common.wait_for_element(device, signin_dict, "sign_in_on_the_device")


def verify_provision_phone_ui(device):
    common.wait_for_and_click(device, ztp_dict, "Provision_device")
    common.wait_for_element(device, ztp_dict, "Verification_code_text_field")
    if "console" not in device:
        if common.is_lcp(device):
            common.wait_for_and_click(device, ztp_dict, "cross_mark")
            return
    common.wait_for_element(device, ztp_dict, "Code_keypad")
    common.wait_for_element(device, ztp_dict, "Provision_device_button")
    common.wait_for_element(device, ztp_dict, "Back_button")


def verify_login_url_with_cloud_settings_as_public(device):
    common.wait_for_and_click(device, ztp_dict, "Public")
    common.wait_for_and_click(device, ztp_dict, "Back_button")
    common.sleep_with_msg(device, 3, "Wait for sometime post changing cloud option")
    common.wait_for_element(device, ztp_dict, "Public_login_url")


def verify_login_url_with_cloud_setting_as_gcc(device):
    common.wait_for_and_click(device, ztp_dict, "GCC")
    common.wait_for_and_click(device, ztp_dict, "Back_button")
    common.sleep_with_msg(device, 3, "Wait for sometime post changing cloud option")
    common.wait_for_element(device, ztp_dict, "GCC_login_url")


def verify_login_url_with_cloud_setting_as_gcc_high(device):
    common.wait_for_and_click(device, ztp_dict, "GCC_High")
    common.wait_for_and_click(device, ztp_dict, "Back_button")
    common.sleep_with_msg(device, 3, "Wait for sometime post changing cloud option")
    common.wait_for_element(device, ztp_dict, "GCC_High_login_url")


def verify_login_url_with_cloud_setting_as_gcc_dod(device):
    common.wait_for_and_click(device, ztp_dict, "GCC_DoD")
    common.wait_for_and_click(device, ztp_dict, "Back_button")
    common.sleep_with_msg(device, 3, "Wait for sometime post changing cloud option")
    common.wait_for_element(device, ztp_dict, "GCC_DoD_login_url")


def verify_emergency_call_label_in_sign_in_page(device):
    ele = common.wait_for_element(device, ztp_dict, "emergency_label_signin_page").text
    ele_label = "Sign in to make an emergency call."
    if ele != ele_label:
        raise AssertionError(f"{device} : Emergency call banner message is not displayed in signin page, {ele}")


def verify_able_to_edit_the_code_on_provision_phone_ui(device):
    common.wait_for_element(device, ztp_dict, "Verification_code_text_field")
    if "console" not in device:
        if config["devices"][device]["model"].lower() in ["riverside", "riverside_13"]:
            common.wait_for_element(device, ztp_dict, "physical_dial_pad_message")
            return
    common.wait_for_and_click(device, calls_dict, "five")
    common.wait_for_and_click(device, calls_dict, "four")
    common.wait_for_and_click(device, calls_dict, "three")
    common.wait_for_and_click(device, calls_dict, "two")
    common.wait_for_and_click(device, calls_dict, "one")
    common.wait_for_and_click(device, calls_dict, "zero")
    ele1 = common.wait_for_element(device, ztp_dict, "Verification_code_text_field").text
    ele1_txt = "543210"
    print("ele :", ele1)
    if ele1 != ele1_txt:
        raise AssertionError(f"{device} : User code {ele1} not equal  {ele1_txt}in provision phone ui")
    common.wait_for_and_click(device, ztp_dict, "provision_backspace_btn")
    ele2 = common.wait_for_element(device, ztp_dict, "Verification_code_text_field").text
    print("ele :", ele2)
    ele2_txt = "54321"
    if ele2 != ele2_txt:
        raise AssertionError(f"{device} : User code {ele2} not equal  {ele2_txt}in provision phone ui")
    if ele1 == ele2:
        raise AssertionError(
            f"{device} : User code {ele1} can not edit/delete the verification code {ele2} in provision phone ui"
        )


def report_an_issue_from_signin_page(device):
    common.wait_for_and_click(device, device_settings_dict, "fre_partner_settings")
    common.wait_for_and_click(device, ztp_dict, "Report_an_issue")
    alias = common.wait_for_element(device, ztp_dict, "alias")
    alias.send_keys(config["meetings"]["participant"])
    title = common.wait_for_element(device, ztp_dict, "title_required")
    title.send_keys(config["Report_feedback"]["title"])
    bug_details = common.wait_for_element(device, ztp_dict, "bug_details")
    bug_details.send_keys(config["Report_feedback"]["bug_details"])
    common.wait_for_and_click(device, ztp_dict, "send_button")
    common.wait_while_present(device, ztp_dict, "send_button")


def navigate_to_different_screens_and_refresh_button_should_not_present_in_dfc_screen(device):
    common.click_if_present(device, signin_dict, "refresh_code_button")
    dfc_main_login_code = common.wait_for_element(device, signin_dict, "dfc_login_code").text
    common.wait_for_and_click(device, device_settings_dict, "fre_partner_settings")
    common.wait_for_and_click(device, ztp_dict, "Cloud_option")
    common.wait_for_element(device, ztp_dict, "Public")
    if not common.click_if_present(device, tr_calls_dict, "close_roaster_button"):
        common.wait_for_and_click(device, common_dict, "back")
    dfc_login_code = common.wait_for_element(device, signin_dict, "dfc_login_code").text
    if dfc_main_login_code != dfc_login_code:
        raise AssertionError(f"{device}:'DFC code is changed'")
    common.wait_for_and_click(device, device_settings_dict, "fre_partner_settings")
    common.wait_for_and_click(device, ztp_dict, "Provision_device")
    common.wait_for_element(device, ztp_dict, "Verification_code_text_field")
    if not common.click_if_present(device, tr_calls_dict, "close_roaster_button"):
        common.wait_for_and_click(device, common_dict, "back")
    common.click_if_present(device, ztp_dict, "Close_icon")
    dfc_login_code = common.wait_for_element(device, signin_dict, "dfc_login_code").text
    if dfc_main_login_code != dfc_login_code:
        raise AssertionError(f"{device}:'DFC code is changed'")
    common.wait_for_and_click(device, device_settings_dict, "fre_partner_settings")
    common.wait_for_and_click(device, ztp_dict, "Report_an_issue")
    common.wait_for_element(device, ztp_dict, "alias")
    if not common.click_if_present(device, tr_calls_dict, "close_roaster_button"):
        common.wait_for_and_click(device, common_dict, "back")
    dfc_login_code = common.wait_for_element(device, signin_dict, "dfc_login_code").text
    if dfc_main_login_code != dfc_login_code:
        raise AssertionError(f"{device}:'DFC code is changed'")


def verify_dfc_settings_popup_closed_successfully(device):
    common.click_if_present(device, ztp_dict, "Close_icon")
    if common.is_element_present(device, ztp_dict, "Cloud_option"):
        raise AssertionError(f"{device}: DFC settings screen was still visible")


def verify_welcome_message_on_dfc_screen(device):
    common.wait_for_and_click(device, sign_dict, "sign_in_on_the_device")
    common.wait_for_element(device, ztp_dict, "welcome_message")
    common.wait_for_and_click(device, tr_Signin_dict, "sign_back")


def verify_ztp_signin_ui_on_lcp(device):
    common.wait_for_element(device, ztp_dict, "login_info_lcp")
    common.wait_for_element(device, ztp_dict, "enter_the_code_for_sign_in_text_lcp")
    timer_text = "Code expires in 04:59"
    if common.is_element_present(device, sign_dict, "refresh_code_button"):
        common.wait_for_and_click(device, sign_dict, "refresh_code_button")
        common.sleep_with_msg(device, 5, "Allow refresh of DFC code")
    common.wait_for_element(device, sign_dict, "dcf_code")
    timer_info = common.wait_for_element(device, ztp_dict, "dfc_code_start_expiry_time", wait_attempts=800).text
    print("Timer text is : ", timer_info)
    if timer_info != timer_text or "04:5" not in timer_info or "Code expires in" not in timer_info:
        raise AssertionError(f"{device} : DFC code expiry timeout is not displayed 5 minutes before expiry")
    common.wait_for_element(device, sign_dict, "dcf_code")


def fetch_dfc_code(device):
    common.click_if_element_appears(device, sign_dict, "refresh_code_button", max_attempts=5)
    time.sleep(display_time)
    dfc_login_code = common.wait_for_element(device, sign_dict, "dfc_login_code").text
    return str(dfc_login_code)


def validate_dfc_code(old_dfc_code, new_dfc_code, device, status):
    if status.lower() not in ["same", "different"]:
        raise AssertionError(f"{device}: Unexpected value for status: {status}")
    if status.lower() == "same":
        if old_dfc_code != new_dfc_code:
            raise AssertionError(f"{device}:  old:{old_dfc_code} DFC Code is refreshed with {new_dfc_code} ")
        else:
            print("both dfc code are same as per expected")
    elif status.lower() == "different":
        if old_dfc_code == new_dfc_code:
            raise AssertionError(f"{device}:  old:{old_dfc_code} DFC Code is refreshed with {new_dfc_code} ")
        else:
            print("both dfc code are diferent as per expected")
