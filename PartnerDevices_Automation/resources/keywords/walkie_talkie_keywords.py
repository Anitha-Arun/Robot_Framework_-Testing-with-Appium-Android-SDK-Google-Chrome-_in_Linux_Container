import common
from Selectors import load_json_file
import time
from appium.webdriver.common.touch_action import TouchAction
from initiate_driver import obj_dev as obj
from selenium.webdriver.support import expected_conditions as EC
from initiate_driver import config
import app_bar_keywords

display_time = 3

app_bar_dict = load_json_file("resources/Page_objects/App_bar.json")
calls_dict = load_json_file("resources/Page_objects/Calls.json")
common_dict = load_json_file("resources/Page_objects/Common.json")
walkie_talkie_dict = load_json_file("resources/Page_objects/walkie_talkie.json")
calendar_dict = load_json_file("resources/Page_objects/Calendar.json")
home_screen_dict = load_json_file("resources/Page_objects/Home_screen.json")


def navigate_to_walkie_talkie_tab(device):
    devices = device.split(",")
    for device in devices:
        print("device :", device)
        time.sleep(display_time)
        common.click_if_present(device, common_dict, "back")
        time.sleep(display_time)
        common.click_if_present(device, home_screen_dict, "home_bar_icon")
        if not common.click_if_present(device, walkie_talkie_dict, "walkie_talkie_tab"):
            common.wait_for_and_click(device, app_bar_dict, "more_tab")
            common.wait_for_and_click(device, walkie_talkie_dict, "walkie_talkie_tab")
        common.wait_for_element(device, walkie_talkie_dict, "channel_option")
        common.wait_for_element(device, walkie_talkie_dict, "participants_icon")
        if not common.is_element_present(device, walkie_talkie_dict, "mic_disabled"):
            common.wait_for_element(device, walkie_talkie_dict, "mic_enabled")
        if not common.is_element_present(device, walkie_talkie_dict, "connect_button"):
            common.wait_for_element(device, walkie_talkie_dict, "disconnect_button")
        print("Navigation to walkie talkie tab is successful")


def verify_connect_when_no_channel_is_selected(device):
    devices = device.split(",")
    for device in devices:
        print("device :", device)
        common.wait_for_and_click(device, walkie_talkie_dict, "channel_option")
        time.sleep(display_time)
        if not common.is_element_present(device, walkie_talkie_dict, "select_channel"):
            common.wait_for_and_click(device, walkie_talkie_dict, "channel_back")
            common.wait_for_and_click(device, walkie_talkie_dict, "connect_button")
            if not common.is_element_present(device, walkie_talkie_dict, "disconnect_button"):
                print("Disconnect button not found. Hence, No channel is selected")
            else:
                raise AssertionError("Disconnect button found. Hence, a channel is selected")
        else:
            common.wait_for_and_click(device, walkie_talkie_dict, "channel_back")


def select_the_channel(device, channel="test_channel"):
    devices = device.split(",")
    for device in devices:
        print("device :", device)
        common.wait_for_and_click(device, walkie_talkie_dict, "channel_option")
        tmp_dict = common.get_dict_copy(walkie_talkie_dict, "channel_name", "channel_replace", channel)
        common.wait_for_and_click(device, tmp_dict, "channel_name")
        common.wait_for_element(device, tmp_dict, "channel_name")
        if common.is_element_present(device, walkie_talkie_dict, "connect_button"):
            common.wait_for_element(device, walkie_talkie_dict, "mic_disabled")
            print("Connect button is visible")
        else:
            common.wait_for_element(device, walkie_talkie_dict, "disconnect_button")


def click_on_connect_and_verify_mic(device):
    devices = device.split(",")
    for device in devices:
        print("device :", device)
        common.wait_for_element(device, walkie_talkie_dict, "channel_option")
        if not common.is_element_present(device, walkie_talkie_dict, "disconnect_button"):
            common.wait_for_and_click(device, walkie_talkie_dict, "connect_button")
        common.wait_for_element(device, walkie_talkie_dict, "mic_enabled")


def click_on_disconnect_and_verify_mic(device):
    devices = device.split(",")
    for device in devices:
        print("device :", device)
        common.wait_for_element(device, walkie_talkie_dict, "channel_option")
        if not common.is_element_present(device, walkie_talkie_dict, "connect_button"):
            common.wait_for_and_click(device, walkie_talkie_dict, "disconnect_button")
        common.wait_for_element(device, walkie_talkie_dict, "mic_disabled")


def verify_connected_paricipant_list(device, connected_device_list):
    print("device :", device)
    expected_participants = []
    for device_name in connected_device_list.split(","):
        expected_participants.append(str(config["devices"][device_name]["user"]["displayname"]))
    common.wait_for_and_click(device, walkie_talkie_dict, "participants_icon")
    time.sleep(display_time)
    actual_participants = common.get_all_elements_texts(device, walkie_talkie_dict, "connected_participants_name")
    expected_participants.sort()
    actual_participants.sort()
    for participant_name in expected_participants:
        if participant_name not in actual_participants:
            raise AssertionError(
                f"{device}: Expected name: {participant_name} not found in connected participants list: {actual_participants}"
            )
    common.wait_for_and_click(device, common_dict, "back")


def press_and_hold_the_mic_button(from_device, to_device):
    driver = obj.device_store.get(alias=from_device)
    elem = common.wait_for_element(from_device, walkie_talkie_dict, "mic_enabled", cond=EC.element_to_be_clickable)
    actions = TouchAction(driver)
    actions.long_press(elem, duration=5000).perform()
    if not common.is_element_present(from_device, walkie_talkie_dict, "live"):
        raise AssertionError(f"{from_device} is not able to talk")
    print(f"{from_device} is able to talk")
    verify_press_and_hold(from_device, to_device)
    elem = common.wait_for_element(
        from_device, walkie_talkie_dict, "mic_while_speaking", cond=EC.element_to_be_clickable
    )
    actions.press(elem).release().perform()


def verify_press_and_hold(from_device, to_device):
    user_displayname = config["devices"][from_device]["user"]["displayname"]
    print("user_displayname : ", user_displayname)
    tmp_dict = common.get_dict_copy(walkie_talkie_dict, "speaker_name", "speaker_replace", user_displayname)
    if common.is_element_present(to_device, calls_dict, "call_action_bar"):
        if common.is_element_present(to_device, tmp_dict, "speaker_name"):
            raise AssertionError(f"{to_device} is able to hear incoming voice message")
        print(f"{to_device} is not able to hear incoming voice message while in a call")
    else:
        speaker = common.wait_for_element(to_device, tmp_dict, "speaker_name").text
        if user_displayname.lower() == speaker.lower():
            print(f"{to_device} is able to hear the voice")
        else:
            raise AssertionError(f"Expected {user_displayname}, found {speaker}")


def verify_call_park_icon_should_not_present_in_walkie_talkie_tab(device):
    print("device :", device)
    time.sleep(display_time)
    if common.is_element_present(device, calls_dict, "call_park"):
        raise AssertionError(f"{device} contains call park icon in walkie-talkie tab")


def verify_walkie_talkie_is_not_present_on_home_screen(device):
    print("device :", device)
    if common.is_element_present(device, walkie_talkie_dict, "walkie_talkie_tab"):
        raise AssertionError("Walkie talkie app is present on home screen")
    print("Walkie talkie app is not present on home screen")


def verify_channel_connection_from_notification_banner(device):
    print("device :", device)
    driver = obj.device_store.get(alias=device)
    window_size = driver.get_window_size()
    print("Window size: ", window_size)
    height = window_size["height"]
    print("Window Height :", height)
    width = window_size["width"]
    print("Window Width :", width)
    if height > width:
        print("Swiping co-ordinates : ", width / 2, 0, width / 2, 3 * (height / 5))
        driver.swipe(width / 2, 0, width / 2, 3 * (height / 5))
    else:
        print("Swiping co-ordinates : ", width / 8, 4 * (height / 5), width / 8, 3 * (height / 5))
        driver.swipe(width / 8, 0, width / 8, 3 * (height / 5))
    common.wait_for_element(device, walkie_talkie_dict, "teams_icon")
    common.wait_for_and_click(device, walkie_talkie_dict, "expand_teams")
    common.wait_for_element(device, walkie_talkie_dict, "connected_teams_channel_name")
    common.wait_for_element(device, walkie_talkie_dict, "connected_people")
    common.wait_for_element(device, walkie_talkie_dict, "disconnect_banner")
    app_bar_keywords.swipe_page_up(device)


def verify_walikie_talkie_option_in_shared_accounts(device):
    if common.is_portrait_mode_cnf_device(device):
        common.wait_for_and_click(device, app_bar_dict, "more_tab")
    time.sleep(display_time)
    if common.is_element_present(device, walkie_talkie_dict, "walkie_talkie_tab"):
        raise AssertionError(f"{device} contains walkie talkie tab")


def verify_error_pop_up_when_double_tap_on_mic_button(device):
    common.wait_for_element(device, walkie_talkie_dict, "disconnect_button")
    driver = obj.device_store.get(alias=device)
    elem = common.wait_for_element(device, walkie_talkie_dict, "mic_enabled", cond=EC.element_to_be_clickable)
    actions = TouchAction(driver)
    max_attempts = 5
    for _attempt in range(max_attempts):
        actions.tap(element=elem, count=2).perform()
        if common.is_element_present(device, walkie_talkie_dict, "mic_double_tap_error_pop"):
            print("You need to wait a bit before you tap and hold to talk.")
            break
        if _attempt == max_attempts - 1:
            raise AssertionError("{device}: error message not founded")


def verify_selected_channel_name_in_walkie_talkie_tab(device, channel):
    common.wait_for_element(device, walkie_talkie_dict, "walkie_talkie_tab")
    channel_name = common.wait_for_element(
        device, walkie_talkie_dict, "selected_channel_name_in_walkie_talkie_tab"
    ).text
    if channel != channel_name:
        raise AssertionError("{device}: Channel Name is not Shown in Walkie Talkie Tab")


def verify_walkie_talkie_tab_header(device):
    common.wait_for_element(device, walkie_talkie_dict, "walkie_talkie_tab")


def verify_participant_icon_in_disconnected_state(device):
    common.wait_for_element(device, walkie_talkie_dict, "connect_button")
    common.wait_for_element(device, walkie_talkie_dict, "mic_disabled")
    elem = common.wait_for_element(device, walkie_talkie_dict, "participants_icon")
    temp = elem.get_attribute("clickable")
    if temp == "true":
        raise AssertionError(f"{device} : Participant icon in disconnected state is enabled")


def verify_search_option_is_disabled_in_walkie_talkie_tab(device):
    time.sleep(display_time)
    if common.is_element_present(device, calls_dict, "search"):
        raise AssertionError("Search option is present")


def verify_suggested_channels_and_your_channels(device, channel):
    devices = device.split(",")
    for device in devices:
        print("device :", device)
        common.wait_for_element(device, walkie_talkie_dict, "channel_option")
        if not common.is_portrait_mode_cnf_device(device):
            common.wait_for_and_click(device, walkie_talkie_dict, "suggested_channels")
            common.wait_for_element(device, walkie_talkie_dict, "your_teams")
        common.wait_for_and_click(device, walkie_talkie_dict, "channel_option")
        common.wait_for_element(device, walkie_talkie_dict, "choose_a_channel")

        channel_names = channel.split(",")
        for channel in channel_names:
            tmp_dict = common.get_dict_copy(walkie_talkie_dict, "channel_name", "channel_replace", channel)
            common.wait_for_element(device, tmp_dict, "channel_name")
    common.wait_for_and_click(device, walkie_talkie_dict, "channel_back")


def verify_user_send_voice_message_when_no_participant_is_connected(device):
    common.wait_for_element(device, walkie_talkie_dict, "disconnect_button")
    common.wait_for_element(device, walkie_talkie_dict, "mic_enabled")
    common.wait_for_element(device, walkie_talkie_dict, "no_one_is_connected")


def press_and_hold_the_mic_button_when_no_one_else_connected(from_device, to_device):
    driver = obj.device_store.get(alias=from_device)
    elem = common.wait_for_element(from_device, walkie_talkie_dict, "mic_enabled", cond=EC.element_to_be_clickable)
    actions = TouchAction(driver)
    actions.long_press(elem, duration=5000).perform()
    if not common.is_element_present(from_device, walkie_talkie_dict, "live"):
        raise AssertionError(f"{from_device} is not able to talk")
    user_displayname = config["devices"][from_device]["user"]["displayname"]
    print("user_displayname : ", user_displayname)
    tmp_dict = common.get_dict_copy(walkie_talkie_dict, "speaker_name", "speaker_replace", user_displayname)
    time.sleep(2)
    if common.is_element_present(to_device, tmp_dict, "speaker_name"):
        raise AssertionError(f"Expected {user_displayname}, found in {to_device}")
    elem = common.wait_for_element(
        from_device, walkie_talkie_dict, "mic_while_speaking", cond=EC.element_to_be_clickable
    )
    actions.press(elem).release().perform()


def verify_user_can_not_use_the_walikie_talkie_app_error_message_while_in_a_call_or_meeting(device):
    max_attempt = 5
    for _attempt in range(max_attempt):
        common.wait_for_and_click(device, walkie_talkie_dict, "mic_enabled")
        if common.is_element_present(device, walkie_talkie_dict, "can_not_use_the_app_while_in_call"):
            return print("can not use error message while in call is found")

        if _attempt == max_attempt - 1:
            raise AssertionError(f"{device}: After clicking on  {_attempt} times error message did not appear")
        time.sleep(2)


def verify_walikie_talkie_error_message_when_user_in_DND_state(from_device, to_device):
    max_attempt = 5
    for _attempt in range(max_attempt):
        common.wait_for_and_click(to_device, walkie_talkie_dict, "mic_enabled")
        if common.is_element_present(from_device, walkie_talkie_dict, "DND_error_message"):
            return print("DND error message is found")

        if _attempt == max_attempt - 1:
            raise AssertionError(f"{from_device}: After clicking on  {_attempt} times error message did not appear")
        time.sleep(2)
