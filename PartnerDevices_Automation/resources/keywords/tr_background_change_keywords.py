from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Selectors import load_json_file
from initiate_driver import obj_dev as obj
import settings_keywords
import common
import time
import call_keywords

display_time = 2
action_time = 3
refresh_time = 5

tr_background_change_dict = load_json_file("resources/Page_objects/tr_background_change.json")
tr_calls_dict = load_json_file("resources/Page_objects/tr_calls.json")
calls_dict = load_json_file("resources/Page_objects/Calls.json")


def choose_background_change(device, option):
    print("Option: ", option)
    devices = device.split(",")
    for device in devices:
        driver = obj.device_store.get(alias=device)
        print("device :", device)
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((MobileBy.ID, calls_dict["Hang_up_button"]["id"]))
            )
            print("Call control visible on screen")
        except Exception as e:
            settings_keywords.click_device_center_point(device)
            print("Call control is not visible on screen ,so clicking on center point")
        try:
            elem = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((MobileBy.ID, calls_dict["call_more_options"]["id"]))
            )
            elem.click()
            print("Clicked on call more option")
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (MobileBy.XPATH, tr_background_change_dict["change_background_btn"]["xpath"])
                )
            ).click()
            print("Clicked on change_background_btn")
            WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((MobileBy.ID, tr_background_change_dict["select_background_button"]["id"]))
            )
            print("Select background text is visible on the screen")
            time.sleep(refresh_time)
            if option.lower() in [
                "no_background",
                "blur_background",
                "teams_contemporary_background",
                "teams_beach_background",
                "teams_traditional_office_background",
                "teams_home_background",
                "fluent_spaces_three_background",
                "fluent_spaces_four_background",
                "teams_contemporary_office_one_background",
                "fluent_Sphere_four_background",
                "fluent_Sphere_two_background",
                "edu_bridge_background",
                "edu_space_background",
                "edu_classroom_background",
                "edu_lab_background",
                "mini_craft_green_background",
                "mini_craft_dark_background",
                "halo_valley_trailer_background",
                "halo_hstill_background",
                "worlds_edge_background",
                "helo_zenith_vista_background",
                "edu_galaxy_background",
                "obsidian_background",
                "obsidian_roseway_background",
                "obsidian_color_cryo_background",
            ]:
                try:
                    WebDriverWait(driver, 30).until(
                        EC.element_to_be_clickable((MobileBy.XPATH, tr_background_change_dict[option.lower()]["xpath"]))
                    ).click()
                    print("Selected background option is: ", option)
                    time.sleep(display_time)
                    swipe_till_last_background_change_option(device)
                except Exception as e:
                    raise Exception("Xpath not found")
            else:
                raise AssertionError("Please select proper background change option.")
        except Exception as e:
            raise AssertionError("Xpath not match")


def get_background_effect(device):
    if not common.click_if_present(device, tr_background_change_dict, "cancel_background_btn"):
        call_keywords.device_right_corner_click(device)


def swipe_till_last_background_change_option(device):
    driver = obj.device_store.get(alias=device)
    window_size = driver.get_window_size()
    print("Window size: ", window_size)
    height = window_size["height"]
    width = window_size["width"]
    print("Swiping co-ordinates : ", (2 * (width / 3), 3 * (height / 4), 2 * (width / 3), 2 * (height / 5)))
    driver.swipe(2 * (width / 3), 3 * (height / 4), 2 * (width / 3), 2 * (height / 5))


def select_no_background_option(device):
    devices = device.split(",")
    for device in devices:
        driver = obj.device_store.get(alias=device)
        print("device :", device)
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((MobileBy.ID, calls_dict["Hang_up_button"]["id"]))
            )
            print("Call control visible on screen")
        except Exception as e:
            settings_keywords.click_device_center_point(device)
            print("Call control is not visible on screen ,so clicking on center point")
        try:
            elem = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((MobileBy.ID, calls_dict["call_more_options"]["id"]))
            )
            elem.click()
            print("Clicked on call more option")
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (MobileBy.XPATH, tr_background_change_dict["change_background_btn"]["xpath"])
                )
            ).click()
            print("Clicked on change background btn")
            time.sleep(refresh_time)
            try:
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((MobileBy.XPATH, tr_background_change_dict["no_background"]["xpath"]))
                ).click()
                print("Clicked On 'No Background' option")
            except Exception as e:
                print("No background option is already selected")
        except Exception as e:
            raise AssertionError("Xpath not found")


def verify_background_change_support_device(device):
    devices = device.split(",")
    for device in devices:
        driver = obj.device_store.get(alias=device)
        print("device :", device)
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((MobileBy.ID, calls_dict["Hang_up_button"]["id"]))
            )
            print("Call control is visible")
        except Exception as e:
            settings_keywords.click_device_center_point(device)
            print("Call Control is not visible so clicking on center point")
        elem = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((MobileBy.ID, calls_dict["call_more_options"]["id"]))
        )
        elem.click()
        print("Clicked on call more option")
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (MobileBy.XPATH, tr_background_change_dict["change_background_btn"]["xpath"])
                )
            )
            status = "pass"
            print("Background change option is present under more option")
        except Exception as e:
            status = "fail"
            print("Background change option is not present under more option")
        call_keywords.device_right_corner_click(device)
        return status
