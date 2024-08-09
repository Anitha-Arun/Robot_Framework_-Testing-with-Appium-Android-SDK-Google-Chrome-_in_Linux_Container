from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import common
from Selectors import load_json_file
from initiate_driver import obj_dev as obj
from initiate_driver import config
import settings_keywords
import call_keywords
import calendar_keywords
import time


display_time = 2
action_time = 3

people_dict = load_json_file("resources/Page_objects/People.json")
calls_dict = load_json_file("resources/Page_objects/Calls.json")
common_dict = load_json_file("resources/Page_objects/Common.json")
app_bar_dict = load_json_file("resources/Page_objects/App_bar.json")
home_screen_dict = load_json_file("resources/Page_objects/Home_screen.json")
calendar_dict = load_json_file("resources/Page_objects/Calendar.json")
people_lcp_dict = load_json_file("resources/Page_objects/People_lcp.json")


def navigate_to_people_tab(device):
    if verify_people_navigation(device):
        return
    if common.click_if_present(device, common_dict, "back") or common.click_if_present(device, common_dict, "home_btn"):
        time.sleep(action_time)
    common.click_if_present(device, home_screen_dict, "home_bar_icon")
    if not (
        common.click_if_present(device, people_dict, "people_tab")
        or common.click_if_present(device, people_dict, "people_tab_cap")
    ):
        common.wait_for_and_click(device, app_bar_dict, "more_tab")
        common.wait_for_and_click(device, people_dict, "people_tab")
        people_text = common.wait_for_element(device, people_dict, "Header").text
        if people_text != "People":
            raise AssertionError(f"{device} is not on People tab")
    if verify_people_navigation(device):
        return
    raise AssertionError(f"{device}: Navigation to people tab failed")


def verify_people_navigation(device):
    common.sleep_with_msg(device, 2, "waiting for header on People tab")
    if common.is_element_present(device, people_dict, "Header", "id"):
        head_text = common.wait_for_element(device, people_dict, "Header").text
        print(f"Tab header is: {head_text}")
        if head_text == "People" or common.is_element_present(device, people_dict, "all_contacts_drop_down"):
            print(f"{device} is on People tab")
            return True
    elif common.is_element_present(device, people_dict, "all_contacts_drop_down"):
        print(f"{device} is on People tab now")
        return True
    elif common.is_element_present(device, people_dict, "people_view"):
        print(f"{device} is on People tab now")
        return True
    else:
        print(f"{device} is not on People tab")
        return False


def verify_plus_icon_on_people_tab(device):
    navigate_to_people_tab(device)
    if common.is_lcp(device):
        common.wait_for_element(device, people_dict, "people_more_lcp")
    else:
        common.wait_for_element(device, people_dict, "plus_icon")


def click_on_plus_icon_on_people_tab(device):
    common.wait_for_and_click(device, people_dict, "plus_icon")


def verify_plus_icon_two_options(device):
    common.wait_for_element(device, people_dict, "create_new_group")
    common.wait_for_element(device, people_dict, "add_from_directory")


def select_people_app_option_and_verify(device, option):
    if option.lower() not in ["create new group", "add from directory"]:
        raise AssertionError(f"Illegal value for 'option': '{option}'")
    if option.lower() == "create new group":
        common.wait_for_and_click(device, people_dict, "create_new_group")
        verify_create_new_group_page(device)
    elif option.lower() == "add from directory":
        common.wait_for_and_click(device, people_dict, "add_from_directory")
        verify_add_from_directory_page(device)


def verify_create_new_group_page(device):
    common.wait_for_element(device, people_dict, "name_your_group")


def verify_add_from_directory_page(device):
    common.wait_for_element(device, people_dict, "add_from_directory_text_view")


def click_drop_down_menu_and_verify_list_of_groups(device):
    common.sleep_with_msg(device, 3, "Waiting for contacts/group names to load")
    common.click_if_present(device, people_dict, "group_name_arrow")
    group_name_list = common.get_all_elements_texts(device, people_dict, "group_list")
    if len(group_name_list) < 5:
        raise AssertionError(f"{device}: All default groups aren't displayed: {group_name_list}")


def verify_default_group_name_from_drop_down(device):
    common.wait_for_element(device, people_dict, "favorites_group")
    common.wait_for_element(device, people_dict, "speed_dial_group")
    common.wait_for_element(device, people_dict, "other_contacts_group")


def select_group_from_drop_down(device, group_name):
    if group_name.lower() == "all contacts":
        common.wait_for_and_click(device, people_dict, "all_contacts_group")
    elif group_name.lower() == "speed dial":
        common.wait_for_and_click(device, people_dict, "speed_dial_group")
    elif group_name.lower() == "other contacts":
        common.wait_for_and_click(device, people_dict, "other_contacts_group")
    elif group_name.lower() == "favorites":
        common.wait_for_and_click(device, people_dict, "favorites_group")
    elif group_name.lower() == "tagged":
        common.wait_for_and_click(device, people_dict, "tagged_group")
    else:
        tmp_dict = common.get_dict_copy(people_dict, "group_name_xpath", "group_name", group_name)
        print(f"Group name: {group_name}")
        common.wait_for_and_click(device, tmp_dict, "group_name_xpath")


def verify_favorite_contacts_under_speed_dial_group(device):
    common.wait_for_element(device, people_dict, "speed_dial_group")
    user_title_elements = []
    user_list = common.wait_for_element(device, people_dict, "user_title", cond=EC.presence_of_all_elements_located)
    for i in user_list:
        user_title_elements.append(str(i.text))
    if len(user_title_elements) == 0:
        raise AssertionError("No favorite contacts added under speed dial group")
    print("list of favorite contacts : ", user_title_elements)


def close_add_contact_on_people_tab(device):
    common.wait_for_and_click(device, people_dict, "plus_icon")


def add_from_directory(from_device, to_device, group_name):
    verify_plus_icon_on_people_tab(from_device)
    click_on_plus_icon_on_people_tab(from_device)
    verify_plus_icon_two_options(from_device)
    select_people_app_option_and_verify(from_device, "Add from directory")
    displayname = config["devices"][to_device]["user"]["displayname"]

    common.kb_trigger_search(from_device, people_dict, "add_edit_text", displayname)

    tmp_dict = common.get_dict_copy(people_dict, "search_result_item_container", "config_display", displayname)
    common.wait_for_and_click(from_device, tmp_dict, "search_result_item_container", "xpath")

    group_name = group_name.lower().capitalize()
    tmp_dict1 = common.get_dict_copy(people_dict, "group_name_xpath", "group_name", group_name)
    common.wait_for_and_click(from_device, tmp_dict1, "group_name_xpath")

    print(f"{from_device} selected group name '{group_name}'")
    common.wait_for_and_click(from_device, people_dict, "action_submit")
    if not common.click_if_element_appears(from_device, people_dict, "group_name_arrow", max_attempts=5):
        common.wait_for_element(from_device, people_dict, "group_arrow")
    select_group_from_drop_down(from_device, group_name)
    time.sleep(display_time)
    verify_usergroup_name_on_people_tab(from_device, to_device, group_name)
    if common.is_portrait_mode_cnf_device(from_device):
        common.wait_for_and_click(from_device, calls_dict, "Call_Back_Button")
    # Tap on same group to contract the user list
    select_group_from_drop_down(from_device, group_name)


def verify_usergroup_name_on_people_tab(from_device, to_device, group_name):
    displayname = config["devices"][to_device]["user"]["displayname"]
    tmp_dict = common.get_dict_copy(people_dict, "search_result_item_container", "config_display", displayname)
    temp_dict1 = common.get_dict_copy(people_dict, "contact_title", "replace_username", displayname)
    time.sleep(10)
    if not common.click_if_present(from_device, tmp_dict, "search_result_item_container", "xpath"):
        common.wait_for_and_click(from_device, temp_dict1, "contact_title", "xpath")
    # wait for sometime and again tap on the contact for group name to be loaded
    time.sleep(5)
    if common.is_portrait_mode_cnf_device(from_device):
        common.wait_for_and_click(from_device, calls_dict, "Call_Back_Button")
        common.sleep_with_msg(from_device, 7, "React to back button click")
    settings_keywords.refresh_main_tab(from_device)
    time.sleep(3)
    if not common.click_if_present(from_device, tmp_dict, "search_result_item_container", "xpath"):
        common.wait_for_and_click(from_device, temp_dict1, "contact_title", "xpath")
    tmp_dict = common.get_dict_copy(people_dict, "appears_in_groups", "Change_Me", group_name)
    if not common.is_element_present(from_device, tmp_dict, "appears_in_groups"):
        if config["devices"][from_device]["model"].lower() == "gilbert":
            calendar_keywords.scroll_down_secondary_tab(from_device)
    group_name_fetched = common.wait_for_element(from_device, tmp_dict, "appears_in_groups").text
    verify_contact_card_details_on_people_app_page(from_device)

    print("Group name is : ", group_name_fetched)
    group_names = group_name_fetched.split(",")
    grp_list = []
    for names in group_names:
        grp_list.append(names.lower().strip())
    print("grp_list : ", grp_list)
    time.sleep(display_time)
    if not group_name.lower() in grp_list:
        raise AssertionError(f"User is not added to the {group_name} group")
    print(f"User is added to the {group_name} group")


def verify_contact_card_details_on_people_app_page(device):
    common.wait_for_element(device, people_dict, "user_profile_picture")
    common.wait_for_element(device, people_dict, "user_name")
    common.wait_for_element(device, people_dict, "make_an_audio_call")
    common.wait_for_element(device, people_dict, "email")
    if not common.is_element_present(device, people_dict, "appears_in"):
        print(f"{device}: The user is on not in any group, so group name is not displayed")


def verify_selected_usergroup_name(from_device, group_name):
    tmp_dict = common.get_dict_copy(people_dict, "appears_in_groups", "Change_Me", group_name)
    _group_names = common.wait_for_element(from_device, tmp_dict, "appears_in_groups").text
    print(f"{from_device}: Found group '{group_name}' in appears-in list: '{_group_names}'")


def verify_multiple_group_name_for_one_user(from_device, to_device, group_name):
    navigate_to_people_tab(from_device)
    displayname = config["devices"][to_device]["user"]["displayname"]
    tmp_dict = common.get_dict_copy(people_dict, "search_result_item_container", "config_display", displayname)
    common.wait_for_and_click(from_device, tmp_dict, "search_result_item_container", "xpath")
    time.sleep(action_time)
    common.click_if_present(from_device, common_dict, "back")
    # click on "search_result_item_container" twice because the group name reflects after the cache is refreshed
    common.wait_for_and_click(from_device, tmp_dict, "search_result_item_container", "xpath")
    tmp_dict = common.get_dict_copy(people_dict, "appears_in_groups", "Change_Me", group_name)
    if not common.is_element_present(from_device, tmp_dict, "appears_in_groups"):
        if config["devices"][from_device]["model"].lower() == "gilbert":
            calendar_keywords.scroll_down_secondary_tab(from_device)
    reflect_group_names = common.wait_for_element(from_device, tmp_dict, "appears_in_groups").text
    verify_contact_card_details_on_people_app_page(from_device)

    reflect_group_names = reflect_group_names.split(",")
    actual_group_names_list = []
    for names in reflect_group_names:
        actual_group_names_list.append(names.lower().strip())
    expected_group_names_list = group_name.split(",")
    for names in expected_group_names_list:
        name = names.lower().strip()
        if name not in actual_group_names_list:
            raise AssertionError(
                f"{from_device}: '{to_device}' user's expected group list: '{expected_group_names_list}', but found: '{actual_group_names_list}'"
            )
    if common.is_portrait_mode_cnf_device(from_device):
        common.wait_for_and_click(from_device, calls_dict, "Call_Back_Button")
    # Click on the group name again to shrink the user list in that group
    select_group_from_drop_down(from_device, group_name)


def create_new_group(device, group_name="test_group", group_creation_result="original"):
    if group_creation_result.lower() not in ["original", "duplicate"]:
        raise AssertionError(f"{device}: Illegal argument for 'group_creation_result': '{group_creation_result}'")
    verify_plus_icon_on_people_tab(device)
    click_on_plus_icon_on_people_tab(device)
    verify_plus_icon_two_options(device)
    select_people_app_option_and_verify(device, "Create new group")
    group_name_field = common.wait_for_element(device, people_dict, "name_your_group")
    group_name_field.send_keys(group_name)
    if config["devices"][device]["model"].lower() == "gilbert":
        common.hide_keyboard(device)
    common.wait_for_and_click(device, people_dict, "create_btn")
    common.sleep_with_msg(device, 3, "Wait post creating the group")
    if group_creation_result.lower() == "duplicate":
        validate_duplicate_group_name(device, group_name)
        return
    # If there is an existing group with same name, ignore the error message and access the existing group
    if common.is_element_present(device, people_dict, "error_msg", "xpath"):
        common.wait_for_and_click(device, people_dict, "ok_btn")
        common.wait_for_and_click(device, people_dict, "cancel_btn")
    time.sleep(display_time)
    click_drop_down_menu_and_verify_group_name(device, group_name)


def click_drop_down_menu_and_verify_group_name(device, group_name):
    if not common.click_if_element_appears(device, people_dict, "group_name_arrow", max_attempts=3):
        common.wait_for_element(device, people_dict, "group_arrow")
    tmp_dict = common.get_dict_copy(people_dict, "group_name_xpath", "group_name", group_name)
    common.wait_for_element(device, tmp_dict, "group_name_xpath")
    time.sleep(display_time)
    select_group_from_drop_down(device, group_name)


def delete_group(device, group_name):
    navigate_to_people_tab(device)
    select_group_from_drop_down(device, group_name)
    temp_dict = common.get_dict_copy(people_dict, "more_option", "group_name", group_name)
    common.wait_for_and_click(device, temp_dict, "more_option", "xpath")
    common.wait_for_and_click(device, people_dict, "edit_group")
    temp_dict = common.get_dict_copy(people_dict, "name_your_group", "Name your group", group_name)
    common.wait_for_element(device, temp_dict, "name_your_group", "xpath")
    common.wait_for_and_click(device, people_dict, "delete_group")
    common.wait_for_and_click(device, home_screen_dict, "home_bar_icon")
    tmp_dict = common.get_dict_copy(people_dict, "group_name_xpath", "group_name", group_name)
    common.wait_while_present(device, tmp_dict, "group_name_xpath")


def edit_group_name(device, old_group_name, new_group_name):
    if not common.click_if_element_appears(device, people_dict, "group_name_arrow", max_attempts=3):
        common.wait_for_element(device, people_dict, "group_arrow")
    time.sleep(display_time)
    select_group_from_drop_down(device, old_group_name)
    temp_dict = common.get_dict_copy(people_dict, "more_option", "group_name", old_group_name)
    time.sleep(3)
    if not common.click_if_present(device, temp_dict, "more_option", "xpath"):
        common.wait_for_and_click(device, people_dict, "more_option", "xpath1")
    common.wait_for_and_click(device, people_dict, "edit_group")
    tmp_dict = common.get_dict_copy(people_dict, "group_name_xpath", "group_name", old_group_name)
    temp_dict1 = common.get_dict_copy(people_dict, "name_your_group", "Name your group", old_group_name)
    time.sleep(display_time)
    if not common.click_if_element_appears(device, tmp_dict, "group_name_xpath", max_attempts=3):
        common.wait_for_and_click(device, temp_dict1, "name_your_group", "xpath")
    elem = common.wait_for_element(device, people_dict, "name_your_group").clear()
    elem.send_keys(new_group_name)
    common.wait_for_and_click(device, people_dict, "save_btn")
    time.sleep(display_time)
    if common.is_element_present(device, people_dict, "error_msg"):
        common.wait_for_and_click(device, people_dict, "ok_btn")
        common.wait_for_and_click(device, people_dict, "cancel_btn")
    click_drop_down_menu_and_verify_group_name(device, new_group_name)


def clicked_first_contact(device):
    common.wait_for_and_click(device, people_dict, "contact_title")


def validate_global_search_and_call_park_icon(device):
    common.wait_for_and_click(device, calls_dict, "search")
    common.wait_for_element(device, calls_dict, "search_text")
    common.wait_for_and_click(device, calls_dict, "Call_Back_Button")
    common.wait_for_and_click(device, people_dict, "people_more_tab")
    common.wait_for_element(device, people_dict, "people_tab_unpark_call")
    call_keywords.dismiss_call_more_options(device)


def validate_create_new_group_with_empty_name(device):
    verify_plus_icon_on_people_tab(device)
    click_on_plus_icon_on_people_tab(device)
    verify_plus_icon_two_options(device)
    select_people_app_option_and_verify(device, "Create new group")
    common.wait_for_element(device, people_dict, "name_your_group").send_keys("")
    common.wait_for_and_click(device, people_dict, "create_btn")
    common.wait_for_element(device, people_dict, "empty_group_error_msg")
    common.wait_for_and_click(device, people_dict, "ok_btn")
    common.wait_for_and_click(device, people_dict, "cancel_btn")


def verify_added_group_name_for_user(from_device, to_device, group_name):
    navigate_to_people_tab(from_device)
    click_drop_down_menu_and_verify_list_of_groups(from_device)
    select_group_from_drop_down(from_device, group_name)
    verify_usergroup_name_on_people_tab(from_device, to_device, group_name)

    # Back button only expected in portrait mode:
    if common.is_portrait_mode_cnf_device(from_device):
        common.wait_for_and_click(from_device, calls_dict, "Call_Back_Button")

    # tap again on the same group to contract the user list
    select_group_from_drop_down(from_device, group_name)


def add_contact_to_group_by_global_contact_search_icon(from_device, to_device, group_name):
    driver = obj.device_store.get(alias=from_device)
    displayname = config["devices"][to_device]["user"]["displayname"]
    username = config["devices"][to_device]["user"]["username"].split("@")[0]
    print("search text :", username)
    try:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((MobileBy.ID, calls_dict["search"]["id"]))).click()
        element = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, calls_dict["search_text"]["id"]))
        )
        element.send_keys(username)
        time.sleep(display_time)
        try:
            driver.hide_keyboard()
        except Exception as e:
            print("Cannot hide keyboard : ", e)
        search_result_xpath = (calls_dict["search_result_item_container"]["xpath"]).replace(
            "config_display", displayname
        )
        print("Search result xpath : ", search_result_xpath)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((MobileBy.XPATH, search_result_xpath))).click()
        time.sleep(display_time)
        print("We are in User contact card page")
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((MobileBy.ID, people_dict["ppl_more_options_button"]["id"]))
            ).click()
            print("Clicked on more_options_button id.")
        except Exception as e:
            try:
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((MobileBy.ID, people_dict["ppl_more_options_button"]["id1"]))
                ).click()
                print("Clicked on more_options_button id1")
            except Exception as e:
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, people_dict["ppl_more_options_button"]["xpath"]))
                ).click()
                print("Clicked on more_options_button xpath")
        print("Clicked on MORE button")
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, people_dict["add_to_contacts"]["xpath"]))
        ).click()
        print("Clicked on ADD TO CONTACT button")
        group_name = group_name.lower().capitalize()
        group_name_xpath = (people_dict["group_name_xpath"]["xpath"]).replace("group_name", group_name)
        print("Search group_name_xpath xpath : ", group_name_xpath)
        group_name_xpath1 = (people_dict["group_name_xpath"]["xpath1"]).replace("group_name", group_name)
        print("Search group_name_xpath xpath1 : ", group_name_xpath1)
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((MobileBy.XPATH, group_name_xpath))).click()
        except Exception as e:
            settings_keywords.swipe_till_end(from_device)
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((MobileBy.XPATH, group_name_xpath1))).click()
        time.sleep(display_time)
        print("selected ", group_name, " group name")
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.ID, people_dict["action_submit"]["id"]))
        ).click()
        print("Clicked on Save button")
        call_keywords.come_back_to_home_screen(from_device)
        verify_added_group_name_for_user(from_device, to_device, group_name)
    except Exception as e:
        raise AssertionError("Xpath not found")


def validate_duplicate_group_name(device, group_name):
    common.wait_for_element(device, people_dict, "error_msg")
    common.wait_for_and_click(device, people_dict, "ok_btn")
    groupname = common.wait_for_element(device, people_dict, "name_your_group", "id").text
    if groupname != group_name:
        raise AssertionError(
            f"{device}: Duplicate group pop-up is displayed for group: '{groupname}', but expected pop-up for: '{group_name}'"
        )
    common.wait_for_and_click(device, people_dict, "cancel_btn")


def click_cancel_btn(device):
    if config["devices"][device]["model"].lower() == "gilbert":
        common.hide_keyboard(device)
    common.wait_for_and_click(device, people_dict, "cancel_btn")


def verify_group_page_when_no_user_added(device, group_name):
    common.sleep_with_msg(device, 10, "Waiting for group users to load")
    if common.is_element_present(device, people_dict, "contacts_are_out_msg"):
        common.wait_for_element(device, people_dict, "lets_bring_them_it_msg")
        return
    temp_dict = common.get_dict_copy(people_dict, "more_option_for_group_participant", "group_name", group_name)
    common.wait_while_present(device, temp_dict, "more_option_for_group_participant", "xpath1")


def validate_selected_group_users_name_on_people_tab(device, participant_device, group_name):
    expected_username = common.device_displayname(participant_device)
    temp_dict = common.get_dict_copy(people_dict, "more_option_for_group_participant", "group_name", group_name)
    actual_username = common.wait_for_element(device, temp_dict, "more_option_for_group_participant", "xpath1").text
    if expected_username != actual_username:
        raise AssertionError(f"{device}: Expected user: {expected_username}, but found: {actual_username}")


def verify_presence_in_contact_card_page(device):
    driver = obj.device_store.get(alias=device)
    try:
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((MobileBy.XPATH, people_dict["presence_xpath"]["xpath"]))
        )
        print("Participant Presence available")
    except Exception as e:
        raise AssertionError("Xpath not found")
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((MobileBy.XPATH, common_dict["back"]["xpath"]))
        ).click()
        print("Clicked on BACK button")
    except Exception as e:
        pass


def validate_when_user_search_for_its_own_name_in_search_result(device):
    verify_plus_icon_on_people_tab(device)
    click_on_plus_icon_on_people_tab(device)
    verify_plus_icon_two_options(device)
    select_people_app_option_and_verify(device, "Add from directory")
    displayname = common.device_displayname(device)
    print(f"{device}: User displayname: {displayname}")
    common.kb_trigger_search(device, people_dict, "add_edit_text", displayname)
    tmp_dict = common.get_dict_copy(people_dict, "search_result_item_container", "config_display", displayname)
    temp_dict1 = common.get_dict_copy(people_dict, "contact_title", "replace_username", displayname)
    if not common.is_element_present(device, tmp_dict, "search_result_item_container", "xpath"):
        common.wait_for_and_click(device, temp_dict1, "contact_title", "xpath")
    common.return_to_home_screen(device)


def remove_user_from_group(from_device, to_device, group_names, select_contact="group"):
    if not select_contact.lower() in ["group", "all_contacts"]:
        raise AssertionError(f"Illegal option specified: '{select_contact}'")
    navigate_to_people_tab(from_device)
    group_names = group_names.split(",")
    for group_name in group_names:
        if not common.click_if_element_appears(from_device, people_dict, "group_name_arrow", max_attempts=3):
            common.wait_for_element(from_device, people_dict, "group_arrow")
        time.sleep(action_time)
        # select contact from all contact page
        if select_contact.lower() == "all_contacts":
            select_group_from_drop_down(from_device, group_name="all contacts")
        elif select_contact.lower() == "group":
            select_group_from_drop_down(from_device, group_name)
        displayname = common.device_displayname(to_device)
        group_name = group_name.lower().capitalize()
        print("group_name : ", group_name)
        tmp_dict = common.get_dict_copy(people_dict, "search_result_item_container", "config_display", displayname)
        # In case, if double tapping on the group name has shrunk the user name, tap on group name again to get username
        time.sleep(display_time)
        if not common.common.click_if_present(from_device, tmp_dict, "search_result_item_container", "xpath"):
            if select_contact.lower() == "all_contacts":
                select_group_from_drop_down(from_device, group_name="all contacts")
            elif select_contact.lower() == "group":
                select_group_from_drop_down(from_device, group_name)
        common.wait_for_and_click(from_device, tmp_dict, "search_result_item_container", "xpath")
        time.sleep(display_time)
        verify_contact_card_details_on_people_app_page(from_device)
        if common.is_portrait_mode_cnf_device(from_device):
            common.wait_for_and_click(from_device, common_dict, "back")
        temp_dict = common.get_dict_copy(people_dict, "more_option_for_group_participant", "group_name", group_name)
        temp_dict1 = common.get_dict_copy(temp_dict, "more_option_for_group_participant", "user_name", displayname)
        common.wait_for_element(from_device, temp_dict1, "more_option_for_group_participant", "xpath")
        common.wait_for_element(from_device, people_dict, "add_to_group")
        common.wait_for_and_click(from_device, people_dict, "remove_from_group")
        common.wait_while_present(from_device, temp_dict1, "more_option_for_group_participant")


def validate_username_and_designation_on_people_tab(device):
    first_group_participant = common.wait_for_element(device, people_dict, "user_title").text
    if common.is_element_present(device, people_dict, "user_designation"):
        designation = common.wait_for_element(device, people_dict, "user_designation").text
        print(f"{device}: first group participant is: {first_group_participant}, designation is: {designation}")


def add_user_to_newly_created_group_from_add_contact_page(from_device, to_device, group_name):
    verify_plus_icon_on_people_tab(from_device)
    click_on_plus_icon_on_people_tab(from_device)
    verify_plus_icon_two_options(from_device)
    select_people_app_option_and_verify(from_device, "Add from directory")
    displayname = config["devices"][to_device]["user"]["displayname"]

    common.kb_trigger_search(from_device, people_dict, "add_edit_text", displayname)

    tmp_dict = common.get_dict_copy(people_dict, "search_result_item_container", "config_display", displayname)
    common.wait_for_and_click(from_device, tmp_dict, "search_result_item_container", "xpath")
    common.wait_for_and_click(from_device, people_dict, "create_group_text")
    common.wait_for_element(from_device, people_dict, "name_your_group").send_keys(group_name)
    common.wait_for_and_click(from_device, people_dict, "create_btn")
    if common.is_element_present(from_device, people_dict, "error_msg"):
        common.wait_for_and_click(from_device, people_dict, "ok_btn")
        common.wait_for_and_click(from_device, people_dict, "cancel_btn")
    tmp_dict1 = common.get_dict_copy(people_dict, "group_name_xpath", "group_name", group_name)
    common.wait_for_and_click(from_device, tmp_dict1, "group_name_xpath")
    print("selected ", group_name, " group name")
    common.wait_for_and_click(from_device, people_dict, "action_submit")
    common.click_if_present(from_device, calls_dict, "Call_Back_Button")


def verify_user_in_all_contacts(from_device, to_device):
    users_list = common.get_all_elements_texts(from_device, people_dict, "group_list")
    display_name = config["devices"][to_device]["user"]["displayname"]
    if display_name not in users_list:
        raise AssertionError(f"{from_device}: {display_name} not found in all contacts list")


def verify_user_profile_avatar(device):
    people_text = common.wait_for_element(device, people_dict, "Header").text
    if not people_text == "People":
        raise AssertionError(f"{device} is not on People tab")
    common.wait_for_element(device, people_dict, "user_profile_picture")


def click_on_people_tab(device):
    time.sleep(display_time)
    if not common.click_if_present(device, people_dict, "people_tab"):
        if common.is_element_present(device, app_bar_dict, "more_tab"):
            common.wait_for_and_click(device, app_bar_dict, "more_tab")
            common.wait_for_and_click(device, people_dict, "people_tab")
        else:
            common.wait_for_and_click(device, people_dict, "people_tab_cap")
    time.sleep(display_time)
    if common.is_lcp(device):
        common.wait_for_element(device, calls_dict, "search_icon")
    else:
        common.wait_for_element(device, calls_dict, "search")


def check_and_close_create_new_group_window(device):
    if common.is_element_present(device, people_dict, "name_your_group"):
        common.wait_for_and_click(device, people_dict, "cancel_btn")


def verify_error_message_after_removing_group_name(device, group_name):
    if not common.click_if_element_appears(device, people_dict, "group_name_arrow", max_attempts=3):
        common.wait_for_element(device, people_dict, "group_arrow")
    select_group_from_drop_down(device, group_name)
    temp_dict = common.get_dict_copy(people_dict, "more_option", "group_name", group_name)
    common.wait_for_and_click(device, temp_dict, "more_option", "xpath")
    common.wait_for_and_click(device, people_dict, "edit_group")
    tmp_dict = common.get_dict_copy(people_dict, "group_name_xpath", "group_name", group_name)
    temp_dict1 = common.get_dict_copy(people_dict, "name_your_group", "Name your group", group_name)
    if not common.click_if_element_appears(device, tmp_dict, "group_name_xpath", max_attempts=3):
        common.wait_for_and_click(device, temp_dict1, "name_your_group", "xpath")
    elem = common.wait_for_element(device, people_dict, "name_your_group")
    elem.clear()
    common.wait_for_and_click(device, people_dict, "save_btn")
    common.wait_for_element(device, people_dict, "invalid_input")
    common.wait_for_and_click(device, people_dict, "ok_btn")
    common.wait_for_element(device, people_dict, "cancel_btn")
    elem.send_keys(group_name)
    common.wait_for_and_click(device, people_dict, "save_btn")
    click_drop_down_menu_and_verify_group_name(device, group_name)


def verify_options_inside_people_tab_for_lcp(device):
    common.wait_for_element(device, calls_dict, "search_icon")
    common.wait_for_element(device, people_dict, "all_contacts_group_lcp")
    common.wait_for_element(device, people_lcp_dict, "favorites_group")
    common.wait_for_element(device, people_lcp_dict, "other_contacts_group")
    common.wait_for_element(device, people_lcp_dict, "speed_dial_group")
    calendar_keywords.scroll_only_once(device)
    common.wait_for_element(device, people_dict, "tagged_group")
    common.wait_for_element(device, people_dict, "people_more_lcp")
    # common.get_all_elements_texts(device, people_dict, "group_list")
    # call_keywords.dismiss_the_popup_screen(device)
    common.wait_for_element(device, people_dict, "people_tab_cap")
    common.wait_for_and_click(device, common_dict, "home_btn")


def verify_list_of_group_names_in_people_tab(device):
    group_names = common.wait_for_element(
        device, people_dict, "group_list", "xpath1", cond=EC.presence_of_all_elements_located
    )
    group_names_list = []
    for ele in group_names:
        ele1 = ele.get_attribute("content-desc")
        group_names_list.append(ele1)
    print(f"{device}: List of groups on People Tab are {group_names_list}")


def verify_all_contacts_group_name_is_in_first_group(device):
    group_names = common.wait_for_element(
        device, people_dict, "group_list", "xpath1", cond=EC.presence_of_all_elements_located
    )
    group_names_list = []
    for ele in group_names:
        ele1 = ele.get_attribute("content-desc")
        group_names_list.append(ele1)
    print(f"{device}: List of groups on People Tab are {group_names_list}")
    if "All Contacts" != group_names_list[0]:
        raise AssertionError(f"{device}: 'All contacts' is not the first group name in people tab")


def verify_search_icon_in_people_tab(device):
    if not verify_people_navigation(device):
        navigate_to_people_tab(device)
    if common.is_lcp(device):
        common.wait_for_element(device, calls_dict, "search_icon")
    else:
        common.wait_for_element(device, calls_dict, "search")


def validate_when_user_search_for_a_contact_in_search_result(from_device, to_device):
    verify_search_icon_in_people_tab(from_device)
    displayname = common.device_displayname(to_device)
    if common.is_lcp(from_device):
        common.kb_trigger_search(from_device, calls_dict, "search_icon", displayname)
    else:
        common.kb_trigger_search(from_device, calls_dict, "search", displayname)
    tmp_dict = common.get_dict_copy(people_dict, "search_result_item_container", "config_display", displayname)
    common.wait_for_and_click(from_device, tmp_dict, "search_result_item_container", "xpath")
    verify_contact_card_details_on_people_app_page(from_device)
    common.wait_for_element(from_device, people_dict, "contact_card_full_view")
    common.return_to_home_screen(from_device)


def unpark_call_from_people_tab(park_code, device):
    if not common.is_element_present(device, people_dict, "people_more_tab"):
        for i in range(2):
            common.click_if_present(device, calls_dict, "Call_Back_Button")
        time.sleep(display_time)
        if not common.is_element_present(device, people_dict, "people_more_tab"):
            navigate_to_people_tab(device)
    if common.is_lcp(device):
        common.wait_for_and_click(device, people_dict, "people_more_lcp")
    else:
        common.wait_for_and_click(device, people_dict, "people_more_tab")
    common.wait_for_and_click(device, people_dict, "people_tab_unpark_call")
    unpark_code_input = common.wait_for_element(device, calls_dict, "unpark_code_edit_text")
    print("park_code : ", park_code)
    unpark_code_input.send_keys(park_code)
    if not common.is_lcp(device):
        common.wait_for_and_click(device, calls_dict, "unpark_call_ok_button")
    _max_attempt = 5
    for _attempt in range(_max_attempt):
        if common.is_element_present(device, calls_dict, "Hang_up_button"):
            return
