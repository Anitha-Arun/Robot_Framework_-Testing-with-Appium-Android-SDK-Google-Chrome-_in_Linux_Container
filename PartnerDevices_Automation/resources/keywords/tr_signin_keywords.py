import common
import tr_home_screen_keywords
from Selectors import load_json_file

tr_Signin_dict = load_json_file("resources/Page_objects/tr_Signin.json")
signin_dict = load_json_file("resources/Page_objects/Signin.json")


def validate_that_signin_successful(device_list, state):
    if state.lower() not in ["sign in", "sign out"]:
        raise AssertionError(f"Illegal 'state' specified: {state}")

    devices = device_list.split(",")
    print("Devices : ", devices)
    for device in devices:
        print("device : ", device)
        if state.lower() == "sign in":
            common.wait_for_element(device, tr_Signin_dict, "more_button", "xpath")

            _dict, _dict_key = tr_home_screen_keywords.tr_get_username_selector(device)
            common.wait_for_element(device, _dict, _dict_key)

        elif state.lower() == "sign out":
            common.wait_for_element(device, signin_dict, "sign_in_on_the_device")

        print(f"{device}: '{state}' successfully completed")
