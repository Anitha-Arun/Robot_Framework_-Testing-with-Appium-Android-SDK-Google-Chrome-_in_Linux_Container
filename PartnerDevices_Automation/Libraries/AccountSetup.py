import collections
from appium import webdriver
from Store import Store
import subprocess
import time
import traceback
from device_control import ping_device, connect_device, clear_app_caches


class AccountSetup(object):
    __instance = None

    @staticmethod
    def getInstance():
        if AccountSetup.__instance is None:
            AccountSetup()
        return AccountSetup.__instance

    def __init__(self):
        if AccountSetup.__instance is not None:
            raise Exception("This class is singleton.")
        AccountSetup.__instance = self
        self.device_store = Store()

    def setup_device_driver(self, device, config):
        desired_cap = collections.OrderedDict(
            list(config["common_desired_caps"].items()) + list(config["devices"][device]["desired_caps"].items())
        )
        driver = webdriver.Remote(
            command_executor="http://127.0.0.1:" + str(config["devices"][device]["port"]) + "/wd/hub",
            desired_capabilities=desired_cap,
        )
        time.sleep(2)
        print("Setting alias Name as : ", device)
        self.device_store.add(driver, alias=device)
        print("Added alias with name : ", device)

    def re_setup_device_driver(self, device, config):
        """
        Tear-down and re-establish automation with the specified device.
        """
        print(f"{device}: re_setup_device_driver")
        self.teardown_device_driver(device)

        if self.device_store.has_alias(device):
            self.device_store.remove(device)

        udid_ = str(config["devices"][device]["desired_caps"]["udid"])
        _is_ip = udid_.count(".") == 3
        print(f"{device}: UDID '{udid_}' is_ip={_is_ip}")

        #
        # IP-connected device may be restarting or unplugged - verify/re-do EVERYTHING.
        #
        if _is_ip:
            try:
                ping_device(device, config)
                connect_device(device, config)
            except Exception as e:
                print(f"{device}: Cannot re-connect - '{type(e).__name__}': {e}")
                raise

        clear_app_caches(device, config, [config["companyPortal_Package"], config["common_desired_caps"]["appPackage"]])

        attached_devices = subprocess.check_output("adb devices", shell=True).decode("utf-8")
        print(f"Info: adb devices reports: {attached_devices}")

        for i in range(0, 2):
            try:
                self.setup_device_driver(device, config)
                break
            except Exception:
                print(traceback.format_exc())
                print(f"Unable to add driver for {device} on attempt {i}")
                continue
        print("Added alias with name AGAIN : ", device)

    def teardown_device_driver(self, device):
        """
        If 'device' has a Webdriver, ask it to quit
        """
        if not self.device_store.has_alias(device):
            print(f"teardown_device_driver: No driver for'{device}'")
            return
        driver = self.device_store.get(device)
        try:
            driver.quit()
            print(f"teardown_device_driver: terminated driver for'{device}'")
        except Exception as e:
            print(f"{device}: WARN teardown_device_driver: caught {type(e).__name__}: {e}")

    def setup_console_driver(self, console, config):
        desired_cap = collections.OrderedDict(
            list(config["common_desired_caps"].items()) + list(config["consoles"][console]["desired_caps"].items())
        )
        driver = webdriver.Remote(
            command_executor="http://127.0.0.1:" + str(config["consoles"][console]["port"]) + "/wd/hub",
            desired_capabilities=desired_cap,
        )
        time.sleep(2)
        print("Setting alias Name as : ", console)
        self.device_store.add(driver, alias=console)
        print("Added alias with name : ", console)

    def re_setup_console_driver(self, console, config, root_console):
        self.teardown_console_driver(console)
        self.device_store.remove(alias=console)
        udid_ = config["consoles"][console]["desired_caps"]["udid"]
        root_console(console, config)
        clear_app_caches(
            console, config, [config["companyPortal_Package"], config["common_desired_caps"]["appPackage"]]
        )
        attached_devices = subprocess.check_output("adb devices", shell=True).decode("utf-8")
        print(attached_devices)
        self.setup_console_driver(console, config)
        print("Added alias with name AGAIN : ", console)

    def teardown_console_driver(self, console):
        """
        If 'console device' has a Webdriver, ask it to quit
        """
        if not self.device_store.has_alias(console):
            print(f"teardown_device_driver: No driver for'{console}'")
            return
        driver = self.device_store.get(console)
        driver.quit()
        print(f"teardown_device_driver: terminated driver for'{console}'")
