import common
from Selectors import load_json_file
import tr_settings_keywords

max_attempt = 5

panels_meeting_resrv_dict = load_json_file("resources/Page_objects/panels_meeting_reservation.json")
home_screen_dict = load_json_file("resources/Page_objects/Home_screen.json")
panels_home_screen_dict = load_json_file("resources/Page_objects/panels_homescreen.json")
panels_device_settings_dict = load_json_file("resources/Page_objects/panels_device_settings.json")


def verify_presence_of_QR_room_reservation_option_in_meetings(device):
    for i in range(max_attempt):
        if common.is_element_present(device, panels_device_settings_dict, "allow_QR_room_reserve_txt"):
            break
        tr_settings_keywords.swipe_screen_page(device)
    common.wait_for_element(device, panels_device_settings_dict, "room_reservation_toggle_qrCode")


def enable_or_disable_QR_code_toggle_button_in_meetings(device, status):
    verify_presence_of_QR_room_reservation_option_in_meetings(device)
    return common.change_toggle_button(device, panels_device_settings_dict, "room_reservation_toggle_qrCode", status)


def verify_QR_Code_on_homescreen(device, state):
    if state.lower() not in ["present", "absent"]:
        raise AssertionError(f"{device}: Unexpected value for  QR code toggle state: {state}")
    if state.lower() == "present":
        common.wait_for_element(device, home_screen_dict, "qr_code_container")
    elif state.lower() == "absent":
        if common.is_element_present(device, home_screen_dict, "qr_code_container") and not common.is_element_present(
            device, panels_home_screen_dict, "reserve_btn"
        ):
            raise AssertionError(
                f"{device} QR Code is still present after disabling QR toggle or reserve button is missing"
            )
