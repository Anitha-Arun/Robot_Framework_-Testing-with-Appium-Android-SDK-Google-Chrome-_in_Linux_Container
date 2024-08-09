from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from Selectors import load_json_file
from initiate_driver import obj_dev as obj
from initiate_driver import config
import settings_keywords
import call_keywords
import calendar_keywords
import time
import common
import device_settings_keywords
import home_screen_keywords


display_time = 2
action_time = 3

voicemail_dict = load_json_file("resources/Page_objects/Voicemail.json")
calls_dict = load_json_file("resources/Page_objects/Calls.json")
common_dict = load_json_file("resources/Page_objects/Common.json")
settings_dict = load_json_file("resources/Page_objects/Settings.json")
home_screen_dict = load_json_file("resources/Page_objects/Home_screen.json")
calendar_dict = load_json_file("resources/Page_objects/Calendar.json")


def navigate_to_voicemail_tab(device):
    print("device :", device)
    time.sleep(display_time)
    status = verify_voicemail_navigation(device)
    if status is True:
        print("Already on Voicemail Tab")
        return

    common.click_if_present(device, common_dict, "back")
    common.click_if_present(device, common_dict, "home_btn")
    common.click_if_present(device, home_screen_dict, "home_bar_icon")
    home_screen_keywords.clear_notification_from_home_screen(device)
    time.sleep(action_time)
    if not common.is_element_present(device, voicemail_dict, "voicemail_tab"):
        common.wait_for_and_click(device, common_dict, "more_tab")

    common.wait_for_and_click(device, voicemail_dict, "voicemail_tab")
    time.sleep(display_time)
    status = verify_voicemail_navigation(device)
    if status is True:
        print("Navigated to Voicemail tab")
        if common.is_lcp(device):
            common.wait_for_element(device, voicemail_dict, "voicemail_list")
        return


def verify_voicemail_navigation(device):
    if common.is_lcp(device):
        if common.is_element_present(device, voicemail_dict, "Header", "id1"):
            return True
        else:
            return False
    if not common.is_element_present(device, voicemail_dict, "Header", "id"):
        return False
    head_text = common.wait_for_element(device, voicemail_dict, "Header", "id").text
    print(f"{device}: Heading text: ", head_text)
    return head_text == "Voicemail"


def play_voicemail_from_left(device):
    common.wait_for_and_click(device, voicemail_dict, "1st_voicemail")
    voicemail_duration = common.wait_for_element(device, voicemail_dict, "playback_time").text.split(":")[1]
    print(f"Voicemail duration: {voicemail_duration}")
    common.wait_for_and_click(device, voicemail_dict, "voicemail_play_button")
    common.wait_for_element(device, voicemail_dict, "voicemail_play_button", wait_attempts=int(voicemail_duration) + 1)


def play_multiple_voicemail(on_device, from_devices):
    devices = from_devices.split(",")
    for device in devices:
        device_name = config["devices"][device]["user"]["displayname"]
        temp_dict = common.get_dict_copy(voicemail_dict, "user_display_name", "to_replace", device_name)
        common.wait_for_and_click(on_device, temp_dict, "user_display_name", "xpath")
        time.sleep(7)
        if not common.is_element_present(on_device, voicemail_dict, "playback_time"):
            common.wait_for_and_click(on_device, temp_dict, "user_display_name", "xpath")
        playback_duration = common.wait_for_element(on_device, voicemail_dict, "playback_time").text.split(":")[1]
        print(f"voicemail from {device} has duration: {playback_duration}")
        common.wait_for_and_click(on_device, voicemail_dict, "voicemail_play_button")
        common.wait_for_element(on_device, voicemail_dict, "pause_voicemail")
        common.sleep_with_msg(on_device, int(playback_duration) + 1, "wait until voicemail is played completely")
        common.wait_for_element(on_device, voicemail_dict, "voicemail_play_button")


def get_missed_voicemail_count(device):
    print("device :", device)
    common.click_if_present(device, common_dict, "back")
    common.click_if_element_appears(device, home_screen_dict, "home_bar_icon", max_attempts=5)
    if not common.is_element_present(device, voicemail_dict, "voicemail_tab"):
        common.wait_for_and_click(device, common_dict, "more_tab")
        common.wait_for_element(device, voicemail_dict, "voicemail_tab")
    time.sleep(action_time)
    voicemail_count = common.wait_for_element(device, voicemail_dict, "missed_voicemail_count").text
    print(f"{device}: Voicemail count: {voicemail_count}")
    home_screen_keywords.verify_and_close_more_menu_options_on_home_screen(device)
    if voicemail_count.isdigit():
        return int(voicemail_count)
    return 0


def get_first_voicemail_time(device):
    print("device :", device)
    navigate_to_voicemail_tab(device)
    first_voicemail_text = common.wait_for_element(device, voicemail_dict, "voicemail_time", "id").text
    first_voicemail_time = first_voicemail_text.split()[0]
    print("First voicemail time : ", first_voicemail_time)
    time.sleep(display_time)
    return str(first_voicemail_time)


def verify_first_voicemail_displayname(to_device, from_device):
    if ":" in from_device:
        device, account = common.decode_device_spec(from_device)
        if account == "pstn_user":
            voicemail_received_device_name = config["devices"][device][account]["pstndisplay"]
        else:
            voicemail_received_device_name = common.config["devices"][device][account]["displayname"]
    else:
        voicemail_received_device_name = common.device_displayname(from_device)
    first_voicemail_user_name = common.wait_for_element(to_device, voicemail_dict, "1st_voicemail").text
    if voicemail_received_device_name != first_voicemail_user_name:
        raise AssertionError(
            f"{to_device}: Expected voicemail sender: {voicemail_received_device_name}, but found: {first_voicemail_user_name} "
        )


def play_and_validate_voicemail_count(new_vm_num, device):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    total_vm_num = int(get_missed_voicemail_count(device))
    new_vm_num = int(new_vm_num)
    print("new_vm_num : ", new_vm_num)
    time.sleep(action_time)
    navigate_to_voicemail_tab(device)
    search_result = driver.find_elements_by_id(voicemail_dict["1st_voicemail"]["id"])
    print("object List : ", search_result)
    for i in range(0, new_vm_num):
        print("i : ", i)
        time.sleep(display_time)
        search_result[i].click()
        time.sleep(display_time)
        playback_duration = (
            WebDriverWait(driver, 30)
            .until(EC.element_to_be_clickable((MobileBy.ID, voicemail_dict["playback_time"]["id"])))
            .text
        )
        voicemail_time = playback_duration.split(":")[1]
        print("playback_duration", voicemail_time)
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, voicemail_dict["voicemail_play_button"]["id"]))
        ).click()
        print("Clicked on ", device, " voicemail play button")
        time.sleep(action_time)
    vm_count = int(get_missed_voicemail_count(device))
    print("vm count: ", vm_count)
    total_vm_num = total_vm_num - new_vm_num
    print("total_vm_num", total_vm_num)
    assert vm_count == total_vm_num, "VM Count is not matching"


def read_last_5_voicemail(device):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    navigate_to_voicemail_tab(device)
    for i in range(0, 5):
        settings_keywords.swipe_till_end(device)
    search_result = driver.find_elements_by_id(voicemail_dict["1st_voicemail"]["id"])
    print("object List : ", search_result)
    list_len = len(search_result)
    print("list_len : ", list_len)
    for i in range(0, list_len - 1):
        print("i : ", i)
        try:
            search_result[i].click()
            time.sleep(action_time)
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((MobileBy.ID, voicemail_dict["voicemail_play_button"]["id"]))
            ).click()
            print("Clicked on ", device, " voicemail play button")
            time.sleep(action_time)
        except StaleElementReferenceException as e:
            pass
        except TimeoutException as e:
            print("Skipping this iteration and continuing")
    for i in range(0, 5):
        settings_keywords.refresh_main_tab(device)


def verify_no_voicemail_object_display_for_new_user(device):
    driver = obj.device_store.get(alias=device)
    navigate_to_voicemail_tab(device)
    time.sleep(action_time)
    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((MobileBy.ID, calls_dict["new_user_error_title"]["id"]))
        )
        print("This is a new user So able to see 'no_voicemail_page' page")
    except Exception as e:
        print("This is not a new user, So unable to see 'no_voicemail_page' page", e)
        raise AssertionError("This is not a new user, So unable to see 'no_voicemail_page' page")
    pass


def scroll_through_voicemails(device):
    print("device :", device)
    for i in range(0, 5):
        settings_keywords.swipe_till_end(device)
    for i in range(0, 5):
        settings_keywords.refresh_main_tab(device)


def play_voicemail(device):
    if not common.is_element_present(device, voicemail_dict, "voicemail_play_button"):
        common.wait_for_and_click(device, voicemail_dict, "1st_voicemail")
    common.wait_for_and_click(device, voicemail_dict, "voicemail_play_button")
    if not common.is_element_present(device, voicemail_dict, "pause_voicemail"):
        # Probably a very short voicemail which completed playing even before pausing it.
        common.wait_for_element(device, voicemail_dict, "voicemail_play_button")


def resume_voicemail(device):
    voicemail_list = common.wait_for_element(
        device, voicemail_dict, "1st_voicemail", cond=EC.presence_of_all_elements_located
    )
    if len(voicemail_list) < 3:
        raise AssertionError(f"{device}: Can't switch between voicemails ")
    if not common.is_element_present(device, voicemail_dict, "voicemail_play_button"):
        voicemail_list[1].click()
    time.sleep(3)
    if not common.is_element_present(device, voicemail_dict, "voicemail_play_button"):
        voicemail_list[2].click()
    common.click_if_present(device, voicemail_dict, "voicemail_play_button")


def pause_voicemail(device):
    if not common.click_if_present(device, voicemail_dict, "pause_voicemail"):
        # Voicemail playing has completed. Need to play the next voicemail.
        common.wait_for_element(device, voicemail_dict, "voicemail_play_button")


def delete_voicemail(device):
    common.wait_for_and_click(device, voicemail_dict, "voicemail_delete_btn")
    common.wait_for_and_click(device, voicemail_dict, "voicemail_delete_notification")


def delete_voicemails_from_page(device):
    vm_count = len(
        common.wait_for_element(device, voicemail_dict, "1st_voicemail", cond=EC.presence_of_all_elements_located)
    )
    for i in range(vm_count):
        common.wait_for_and_click(device, voicemail_dict, "1st_voicemail")
        delete_voicemail(device)


def select_voicemail_option(device, option):
    if option.lower() not in ["call", "view profile", "remove favorite"]:
        raise AssertionError(f"Unexpected value for option : {option}")
    driver = obj.device_store.get(alias=device)
    elm2 = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((MobileBy.ID, voicemail_dict["call_action"]["id"]))
    )
    elm3 = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((MobileBy.ID, voicemail_dict["profile_action"]["id"]))
    )
    elm4 = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((MobileBy.ID, voicemail_dict["voicemail_delete_btn"]["id"]))
    )
    time.sleep(display_time)
    if elm2.is_displayed() and elm3.is_displayed() and elm4.is_displayed():
        print("Speaker, Call, View profile, Remove VM options are visible")
    else:
        raise AssertionError("Speaker, Call, View profile, Remove VM options are not visible")
    if option.lower() == "call":
        elm2.click()
        print("Selected CALL option")
        if common.click_if_present(device, calls_dict, "myself_xpath"):
            print(f"*WARN*:: {device}: Found and used unexpected 'myself' OBO")
        common.wait_for_element(device, calls_dict, "Hang_up_button")
    elif option.lower() == "view profile":
        elm3.click()
        print("Selected VIEW PROFILE option")
    elif option.lower() == "remove favorite":
        elm4.click()
        print("Selected REMOVE VOICEMAIL option")
    else:
        raise AssertionError("Provide proper option to select from Voicemail user option")


def play_vm_with_diff_speed(device):
    print("device :", device)
    time.sleep(display_time)
    if not common.is_element_present(device, voicemail_dict, "voicemail_play_button"):
        common.wait_for_and_click(device, voicemail_dict, "1st_voicemail")
    for n in range(3):
        common.wait_for_and_click(device, voicemail_dict, "voicemail_play_button")
        common.wait_for_and_click(device, voicemail_dict, "speed_button")
        common.sleep_with_msg(device, 2, "Playing voicemail")


def call_user_who_left_voice_mail(device):
    print("device :", device)
    select_voicemail_option(device, "call")


def verify_user_contact_details_who_left_voice_mail(device, from_device):
    navigate_to_voicemail_tab(device)
    common.wait_for_and_click(device, voicemail_dict, "1st_voicemail", "id")
    select_voicemail_option(device, "view profile")
    user_name = common.device_displayname(from_device)
    user_mail_id = common.device_username(from_device)

    temp_dict = common.get_dict_copy(calendar_dict, "add_user", "user_name", user_name)
    common.wait_for_element(device, temp_dict, "add_user", "xpath")

    mail_id = common.wait_for_element(from_device, calls_dict, "mail_id").text
    if mail_id != user_mail_id:
        raise AssertionError(f"{device}: expected mail-id: {user_mail_id}, but found: {mail_id}")
    common.click_if_present(device, calls_dict, "Call_Back_Button")
    # first_vm.click()


def delete_voicemail_while_playing_it(device):
    if not common.is_element_present(device, voicemail_dict, "voicemail_play_button"):
        common.wait_for_and_click(device, voicemail_dict, "1st_voicemail")
    common.wait_for_and_click(device, voicemail_dict, "voicemail_play_button")
    delete_voicemail(device)


def delete_all_voicemails(device):
    time.sleep(2)
    while common.is_element_present(device, voicemail_dict, "1st_voicemail"):
        if not common.is_element_present(device, voicemail_dict, "voicemail_delete_btn"):
            common.wait_for_and_click(device, voicemail_dict, "1st_voicemail")
        delete_voicemail(device)
        time.sleep(2)


def verify_1st_voicemail(device):
    navigate_to_voicemail_tab(device)
    vm_list = common.wait_for_element(device, voicemail_dict, "1st_voicemail", cond=EC.presence_of_all_elements_located)
    if len(vm_list) < 1:
        raise AssertionError(f"{device}: Haven't received any voicemails yet")


def verify_vm_tab_status(device):
    common.sleep_with_msg(device, 2, "Wait until the voicemail tab loads")
    if common.is_element_present(device, voicemail_dict, "1st_voicemail"):
        return True
    return False


def refresh_for_voicemail_visibility(device):
    common.return_to_home_screen(device)
    if common.is_lcp(device):
        call_keywords.navigate_to_calls_tab(device)
        call_keywords.come_back_to_home_screen(device)
        navigate_to_voicemail_tab(device)
        call_keywords.come_back_to_home_screen(device)
    else:
        call_keywords.click_on_calls_tab(device)
        calendar_keywords.navigate_to_calendar_tab(device)


def refresh_for_voicemail_visibility_for_cap(device):
    call_keywords.click_on_calls_tab(device)
    navigate_to_voicemail_tab(device)
    settings_keywords.refresh_main_tab(device)
    common.return_to_home_screen(device)


def verify_1st_vm_presence_status(device):
    print("device :", device)
    common.wait_for_and_click(device, voicemail_dict, "1st_voicemail")
    print("Clicked on 1st Voicemail available in VM Tab")
    common.wait_for_and_click(device, voicemail_dict, "profile_action")
    print("Clicked on 1st Voicemail contact card button")
    common.wait_for_element(device, voicemail_dict, "user_presence_icon")
    print("User presence icon visible")


def verify_voicemail_status_while_in_call(device):
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")
    common.sleep_with_msg(device, 5, "Wait for active call ribbon to appear")
    common.wait_for_element(device, calls_dict, "call_action_bar")
    if verify_voicemail_navigation(device):
        common.wait_for_element(device, voicemail_dict, "1st_voicemail")
        common.wait_for_element(device, voicemail_dict, "voicemail_play_button")
        common.wait_for_and_click(device, calls_dict, "call_action_bar")
        return
    raise AssertionError(f"{device} : User is not on voicemail tab post answering the call")


def verify_voicemail_tab_empty(device):
    common.wait_for_element(device, voicemail_dict, "no_voicemail")


def verify_user_set_the_if_unanswered_to_voicemail(device):
    settings_keywords.open_settings_page(device)
    if not common.click_if_present(device, settings_dict, "Calling"):
        settings_keywords.swipe_till_end(device)
        settings_keywords.swipe_till_end(device)
        common.wait_for_and_click(device, settings_dict, "Device_Settings")
        device_settings_keywords.advance_calling_option_oem(device)
        common.wait_for_element(device, settings_dict, "call_forwarding")
    ele = common.wait_for_element(device, voicemail_dict, "if_unanswered_to_voicemail").text
    if ele != "Voicemail":
        raise AssertionError(f"{device} : User is not set to if unanswered to Voicemail")
    settings_keywords.device_setting_back(device)
    settings_keywords.device_setting_back(device)
    call_keywords.come_back_to_home_screen(device)


def verify_missed_voicemail_pill_in_app_bar(device, status):
    common.wait_for_element(device, common_dict, "more_tab")
    if status.lower() == "appear":
        common.wait_for_element(device, voicemail_dict, "missed_voicemail_pill_count_in_more")
    elif status.lower() == "disappear":
        if common.is_element_present(device, voicemail_dict, "missed_voicemail_pill_count_in_more"):
            raise AssertionError(f"{device} still pill count is shown in voicemail icon")


def verify_voicemail_forwarding_message_text_while_already_in_call(device, to_device):
    common.wait_for_and_click(device, calls_dict, "search")
    displayname = common.device_displayname(to_device)
    print(f"diaplay name: {displayname}")
    common.wait_for_element(device, calls_dict, "search_text").send_keys(displayname)
    common.hide_keyboard(device)
    tmp_dict = common.get_dict_copy(calls_dict, "search_result_item_container", "config_display", displayname)
    common.wait_for_and_click(device, tmp_dict, "search_result_item_container", "xpath")
    common.wait_for_and_click(device, calls_dict, "Make_an_audio_call")
    common.wait_for_element(device, voicemail_dict, "forwarding_voicemail")


def verify_and_click_send_to_voicemail_option_for_incoming_call(device, option="click"):
    if option.lower() not in ["click", "verify"]:
        raise AssertionError(f"Unexpected value for option : {option}")
    common.wait_for_element(device, calls_dict, "Accept_call_button")
    if option.lower() == "click":
        common.wait_for_and_click(device, calls_dict, "send_to_voicemail_button")
    else:
        common.wait_for_element(device, calls_dict, "send_to_voicemail_button")


def verify_voicemail_forwarding_message_text(device):
    common.wait_for_element(device, voicemail_dict, "forwarding_voicemail")
