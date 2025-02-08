import unittest
from appium import webdriver
import yaml
from time import sleep

def load_yaml(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

class RegistrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.locators = load_yaml("locators.yaml")
        cls.testdata = load_yaml("testdata.yaml")

    def setUp(self):
        desired_caps = {
            'platformName': 'Android',
            'deviceName': 'Android Emulator',
            'app': '<path>',
            'automationName': 'UiAutomator2'
        }
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(30)

    def test_registration(self):
        self.driver.find_element_by_id(self.locators['register_button']).click()
        self.driver.find_element_by_id(self.locators['name_input']).send_keys(self.testdata['user']['name'])
        self.driver.find_element_by_id(self.locators['phone_input']).send_keys(self.testdata['user']['phone'])
        self.driver.find_element_by_id(self.locators['sms_code_input']).send_keys(self.testdata['user']['sms_code'])
        self.driver.find_element_by_id(self.locators['register_confirm_button']).click()

        sleep(5)  # Подождем, чтобы элемент успел появиться
        registered_element = self.driver.find_element_by_id(self.locators['registration_successful_message'])
        self.assertIsNotNone(registered_element, "Registration failed!")

    def tearDown(self):
        if self.driver:
            self.driver.quit()

if __name__ == '__main__':
    unittest.main()

