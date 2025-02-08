import unittest
from appium import webdriver
import yaml
from time import sleep

def load_yaml(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

class ChangeLanguageTest(unittest.TestCase):
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
        self.login()

    def login(self):
        self.driver.find_element_by_id(self.locators['login_button']).click()
        self.driver.find_element_by_id(self.locators['phone_input']).send_keys(self.testdata['user']['phone'])
        self.driver.find_element_by_id(self.locators['sms_code_input']).send_keys(self.testdata['user']['sms_code'])
        self.driver.find_element_by_id(self.locators['login_confirm_button']).click()
        sleep(5)  # Подождем, чтобы элемент успел появиться

    def test_change_language(self):
        self.driver.find_element_by_id(self.locators['settings_button']).click()
        self.driver.find_element_by_id(self.locators['language_option']).click()

        # Смена языка с английского на французский
        self.driver.find_element_by_id(self.locators['language_french']).click()
        self.driver.find_element_by_id(self.locators['save_button']).click()
        self.driver.find_element_by_id(self.locators['confirm_language_change_button']).click()

        sleep(5)

        # Повторное открытие приложения
        desired_caps = {
            'platformName': 'Android',
            'deviceName': 'Android Emulator',
            'app': '<path>',
            'automationName': 'UiAutomator2'
        }
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(30)

        # Проверка, что текст изменился на французский
        self.driver.find_element_by_id(self.locators['settings_button']).click()
        language_text_element = self.driver.find_element_by_id(self.locators['language_option'])
        self.assertEqual(language_text_element.text, self.testdata['languages']['language_text'], "Language change failed!")


    def tearDown(self):
        if self.driver:
            self.driver.quit()

if __name__ == '__main__':
    unittest.main()
