import panels_homescreen_keywords
import common
from Selectors import load_json_file
import time
from initiate_driver import config
import settings_keywords

action_time = 3
max_attempt = 4

panels_home_screen_dict = load_json_file("resources/Page_objects/panels_homescreen.json")
panels_meeting_resrv_dict = load_json_file("resources/Page_objects/panels_meeting_reservation.json")
navigation_dict = load_json_file("resources/Page_objects/Navigation.json")


def verify_multiple_all_day_meetings_in_panel(device, meeting_list):
    # Verify the specified meeting names are in the 'All day' summary page, or in the main ('general calendar') list as All-day meetings.
    # Behavior: The 'All day' summary page is not offered if the actual 'All day' meeting count is > 2.
    # Behavior: The 'All day' meeting element structure is different for 'today' and 'non-today' meetings.
    # Note: Test is using _expected_meeting_names[0] as auto-scroll target, so the 'meeting_list' order is significant.

    _expected_meeting_names = meeting_list.split(",")
    _actual_meeting_name_list = []

    # If already on the 'All day' summary page, return to the 'general calendar' list:
    common.click_if_present(device, panels_home_screen_dict, "all_day_list_back_arrow")

    # If offered, verify the advertized all-day meeting count is at least what is expected
    if _advertized_meeting_count_element := common.is_element_present(
        device, panels_home_screen_dict, "all_day_list_meeting_count"
    ):
        _advertized_meeting_count = int(_advertized_meeting_count_element.text)
        if _advertized_meeting_count < len(_expected_meeting_names):
            raise AssertionError(
                f"{device}: Advertized all-day meeting count '{_advertized_meeting_count}' is less than expected meeting count '{len(_expected_meeting_names)}'"
            )
        print(
            f"{device}: Advertized 'All Day' meeting count is: '{_advertized_meeting_count}', expecting at least {len(_expected_meeting_names)}"
        )
    else:
        _expected_count = len(_expected_meeting_names)
        if _expected_count > 2:
            raise AssertionError(
                f"{device}: Expecting {_expected_count} names but Advertized 'All Day' meeting count was not offered"
            )
        print(f"{device}: Expecting only {_expected_count} meeting names - UI will not offer 'All day' list or count")

    # Gather names from either the 'main calendar' OR the 'All Day' list:
    if common.click_if_present(device, panels_home_screen_dict, "all_day_list_next_arrow"):
        print(f"{device}: Gathering meeting names from the 'All Day' list")
    else:
        print(f"{device}: Gathering meeting names from the main calendar")

    # Choose which today/not-today format to select with:
    if common.is_element_present(device, panels_home_screen_dict, "calendar_has_today_elements"):
        allday_meeting_selector = "calendar_all_day_meeting_elements_today"
    else:
        allday_meeting_selector = "calendar_all_day_meeting_elements_not_today"
    print(f"{device}: Using '{allday_meeting_selector}' format calendar selectors")

    _actual_meeting_name_list = common.get_all_elements_texts(device, panels_home_screen_dict, allday_meeting_selector)

    # -------------
    # Problematic/fragile:
    # This is attempting to reset the calendar and scroll to the 2nd(?) page to see more all-day names:
    settings_keywords.refresh_main_tab(device)
    panels_homescreen_keywords.scroll_agenda_view(device)
    panels_homescreen_keywords.scroll_agenda_view(device)
    panels_homescreen_keywords.scroll_agenda_view(device)
    #
    # If the scroll_agenda_view() is updated it may scroll too much, or not enough...
    # If the device has more/less display area, we may need to scroll more/less...
    # If Teams uses more/less display area, we may need to scroll more/less...
    # -------------

    # Accumulate more all-day meeting names revealed by the scroll:
    # Note that we are just doing this once, this will not work for long lists of meetings
    _actual_meeting_name_list = _actual_meeting_name_list + common.get_all_elements_texts(
        device,
        panels_home_screen_dict,
        allday_meeting_selector,
    )

    # Smash them into a unique-only list:
    _actual_meeting_name_list = [*set(_actual_meeting_name_list)]

    print("Expected meeting names:", _expected_meeting_names)
    print("Actual meeting names:", _actual_meeting_name_list)

    for meeting in _expected_meeting_names:
        if not meeting in _actual_meeting_name_list:
            raise AssertionError(f"{device}: '{meeting}' is not visible in All-Day events")
    print(f"{device}: All expected 'All day' events are visible in events list")

    # Validate auto-scroll back to the first All-day event:
    # Note: Even if we did not scroll, we are doing this anyway (an unnecessary wait).
    # Note: Assuming the main calendar and the 'All-day' summary list have the same behavior.
    # Note: Test is using _expected_meeting_names[0], so the specified order is important.
    _auto_scroll_wait_secs = 10
    common.sleep_with_msg(device, _auto_scroll_wait_secs, "Waiting for auto-scroll to occur")
    first_all_day_meeting = common.wait_for_element(device, panels_home_screen_dict, allday_meeting_selector).text
    if first_all_day_meeting != _expected_meeting_names[0]:
        raise AssertionError(
            f"{device}: '{first_all_day_meeting}' does not match '{_expected_meeting_names[0]}', even after timeout it didn't scroll back to "
            f"current scheduled All-Day events"
        )

    # Close the 'All-Day' summary list, if present:
    common.click_if_present(device, panels_home_screen_dict, "all_day_list_back_arrow")


def verify_one_all_day_meeting_in_panel(device, meeting):
    print("verifying available meeting slot for the next day")
    common.wait_for_element(device, panels_home_screen_dict, "available_room")
    common.wait_for_element(device, panels_home_screen_dict, "agenda_view_time_range")
    common.wait_for_element(device, panels_home_screen_dict, "next_day_text")
    print("verifying all day meeting slot")
    all_day_meeting = common.wait_for_element(device, panels_home_screen_dict, "all_day_meeting", "id1").text
    all_day_time_range = common.wait_for_element(device, panels_home_screen_dict, "all_day_time_range").text
    if all_day_meeting != meeting or all_day_time_range != "All-day":
        raise AssertionError(f"{all_day_meeting} or {all_day_time_range} is not visible in current events")


def verify_all_all_day_reserved_meeting_parameters_in_panel(
    device, organizer, all_day_meeting_list, count_of_all_day_meetings
):
    common.wait_for_element(device, panels_home_screen_dict, "all_day_list_title")
    all_day_count = common.wait_for_element(device, panels_home_screen_dict, "all_day_list_meeting_count").text
    if all_day_count != count_of_all_day_meetings:
        raise AssertionError(f"{all_day_count} count from panel is not same as {count_of_all_day_meetings}")
    if common.click_if_present(device, panels_home_screen_dict, "all_day_list_next_arrow"):
        print(f"{device}: Gathering meeting names from the 'All Day' list")
    else:
        print(f"{device}: Gathering meeting names from the main calendar")
    all_day_meeting_name = common.get_all_elements_texts(device, panels_home_screen_dict, "all_day_meeting")
    for meeting in all_day_meeting_list.split(","):
        print("meeting :", meeting)
        if not meeting in all_day_meeting_name:
            raise AssertionError(f"{meeting} is not visible inside All-Day events tab.")
    all_day_meeting_time = common.get_all_elements_texts(device, panels_home_screen_dict, "all_day_time_range")
    for meeting_time in all_day_meeting_time:
        if meeting_time != "All day":
            raise AssertionError(f" Meeting time is not all-day")
    all_day_meeting_organizer_name = common.get_all_elements_texts(
        device, panels_home_screen_dict, "all_day_organizer_name"
    )
    organizer_name = config["devices"][organizer]["user"]["displayname"]
    for organizer in all_day_meeting_organizer_name:
        if organizer != organizer_name:
            raise AssertionError(f"{organizer_name} is not matched with organizer on homescreen:{organizer}")
    common.wait_for_element(device, panels_home_screen_dict, "teams_logo")


def verify_all_normal_reserved_meeting_parameters_in_panel(device, other_meeting_list, count_of_other_meetings):
    other_meeting_list_from_panel = common.get_all_elements_texts(
        device, panels_home_screen_dict, "agenda_view_meeting_name"
    )
    panels_homescreen_keywords.scroll_agenda_view(device)
    panels_homescreen_keywords.scroll_agenda_view(device)
    panels_homescreen_keywords.scroll_agenda_view(device)
    other_meeting_list_from_panel1 = common.get_all_elements_texts(
        device, panels_home_screen_dict, "agenda_view_meeting_name"
    )
    other_meeting_list_from_panel = other_meeting_list_from_panel + other_meeting_list_from_panel1
    other_meeting_list_from_panel = [*set(other_meeting_list_from_panel)]
    if common.is_element_present(device, panels_home_screen_dict, "next_day_text"):
        common.wait_for_element(device, panels_home_screen_dict, "next_day_available_tile")
    else:
        raise AssertionError(f"No Available meeting is present in calendar tab for next day")
    available_meeting = "Available"
    while available_meeting in other_meeting_list_from_panel:
        other_meeting_list_from_panel.remove(available_meeting)
    print(other_meeting_list_from_panel)
    count = len(other_meeting_list_from_panel)
    if count != int(count_of_other_meetings):
        raise AssertionError(f"{count} is not matched with count_of_other_meetings:{count_of_other_meetings}")
    for meeting in other_meeting_list.split(","):
        print("meeting :", meeting)
        if not meeting in other_meeting_list_from_panel:
            raise AssertionError(f"{meeting} is not visible inside Calendar tab.")


def verify_truncated_meeting_title_in_panel(device, meeting):
    title = common.wait_for_element(device, panels_home_screen_dict, "agenda_view_meeting_name", "xpath").text
    print("title : ", title)
    compare_length = len(title)
    if title.endswith("...") and compare_length >= 250:
        compare_length = compare_length - 3
    if not title.endswith("..."):
        raise AssertionError(f"{title} is not truncated")
    if not title[0:compare_length] == meeting[0:compare_length]:
        raise AssertionError(
            f"{device}: meeting title: expected {meeting[0:compare_length]}, found {title[0:compare_length]}"
        )


def verify_presence_of_single_meeting_in_panel(device, state, meeting):
    if state.lower() not in ["present", "absent"]:
        raise AssertionError(f"{device}: Unexpected value for state: {state}")
    for i in range(max_attempt):
        if common.is_element_present(device, panels_home_screen_dict, "teams_logo"):
            break
        settings_keywords.refresh_calls_main_tab(device)
    title = common.wait_for_element(device, panels_home_screen_dict, "agenda_view_meeting_name", "xpath").text
    print("title : ", title)
    if state.lower() == "present":
        if title != meeting:
            raise AssertionError(f"{device}: meeting title: expected: {meeting} but, found {title}")
    else:
        if title.lower() != "available":
            raise AssertionError(f"{device}: meeting title: expected: Available but, found {title}")


def verify_presence_of_upcoming_single_meeting_in_panel(device, meeting):
    settings_keywords.refresh_calls_main_tab(device)
    meeting_list = common.get_all_elements_texts(device, panels_home_screen_dict, "agenda_view_meeting_name")
    print("meeting_list : ", meeting_list)
    if meeting not in meeting_list:
        raise AssertionError(f"{device}: meeting title: {meeting}, not found  in calendar {meeting_list}")
