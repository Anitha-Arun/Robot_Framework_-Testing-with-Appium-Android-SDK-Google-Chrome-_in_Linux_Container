import common
from Selectors import load_json_file
from initiate_driver import obj_dev as obj

display_time = 2
action_time = 3


calls_dict = load_json_file("resources/Page_objects/Calls.json")
calendar_dict = load_json_file("resources/Page_objects/Calendar.json")
home_screen_dict = load_json_file("resources/Page_objects/Home_screen.json")
sign_dict = load_json_file("resources/Page_objects/Signin.json")


def verify_that_sign_in_is_successful(device_list, state):
    if state.lower() not in ["sign in", "sign out"]:
        raise AssertionError(f"Unexpected value for state: {state}")
    devices = device_list.split(",")
    print("Devices : ", devices)
    for device in devices:
        print("device : ", device)
        driver = obj.device_store.get(alias=device)
        if state.lower() == "sign in":
            if (
                common.is_element_present(device, calendar_dict, "calendar_tab")
                or common.is_element_present(device, calls_dict, "call_park")
                or common.is_element_present(device, calls_dict, "calls_tab")
                or common.is_element_present(device, home_screen_dict, "more_option")
            ):
                print("Sign in is successfully completed")
                return
            elif not common.is_portrait_mode_cnf_device(device):
                raise AssertionError(f"Sign in is not completed on {device}")
            common.wait_for_element(device, calendar_dict, "app_bar_dialpad_icon")
            common.wait_for_element(device, calendar_dict, "app_bar_meet_now")
            common.wait_for_element(device, calendar_dict, "app_bar_more")
        elif state.lower() == "sign out":
            common.wait_for_element(device, sign_dict, "sign_in_on_the_device")
