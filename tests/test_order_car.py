import unittest
from appium import webdriver
import yaml
from time import sleep

def load_yaml(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

class OrderCarTest(unittest.TestCase):
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

    def test_order_car(self):
        self.driver.find_element_by_id(self.locators['login_button']).click()
        self.driver.find_element_by_id(self.locators['phone_input']).send_keys(self.testdata['user']['phone'])
        self.driver.find_element_by_id(self.locators['sms_code_input']).send_keys(self.testdata['user']['sms_code'])
        self.driver.find_element_by_id(self.locators['login_confirm_button']).click()

        self.driver.find_element_by_id(self.locators['start_point']).send_keys(self.testdata['order']['start_point'])
        self.driver.find_element_by_id(self.locators['end_point']).send_keys(self.testdata['order']['end_point'])
        self.driver.find_element_by_id(self.locators['price_input']).send_keys(self.testdata['order']['price'])
        self.driver.find_element_by_id(self.locators['order_confirm_button']).click()

        sleep(5)  # Подождем, чтобы элемент успел появиться
        order_confirmation_element = self.driver.find_element_by_id(self.locators['order_successful_message'])
        self.assertIsNotNone(order_confirmation_element, "Order failed!")

    def tearDown(self):
        if self.driver:
            self.driver.quit()

if __name__ == '__main__':
    unittest.main()
