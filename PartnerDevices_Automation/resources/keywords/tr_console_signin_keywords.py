from Libraries.Selectors import load_json_file
import common

display_time = 2
action_time = 3

calls_dict = load_json_file("resources/Page_objects/Calls.json")
tr_console_signin_dict = load_json_file("resources/Page_objects/rooms_console_signin.json")
signin_dict = load_json_file("resources/Page_objects/Signin.json")


def verify_signin_is_successful(console_list, state):
    consoles = console_list.split(",")
    print("Consoles : ", consoles)
    for console in consoles:
        print("Console : ", console)
        if state.lower() == "sign in":
            common.wait_for_element(console, tr_console_signin_dict, "more_option")
            common.wait_for_element(console, tr_console_signin_dict, "meet_now_icon")
            print("Sign in is Successfully Completed")
        elif state.lower() == "sign out":
            common.wait_for_element(console, signin_dict, "sign_in_on_the_device", "id")
            print("Sign out is Successfully Completed")
