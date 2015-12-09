from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_adventure(self):
        #Daniel is a single parent who has heard about this
        #new game that he can play with his daughter. So he
        #picks a day and they open the site together.
        self.browser.get('https://adventuregame.herokuapp.com')

        #Daniel and his daughter see that the page title
        #mentions adventures.
        assert 'Adventure' in self.browser.title, "Browser title was " + self.browser.title
        header_text = self.browser.find_element_by_tag_name('h2'.text)
        self.assertIn('Check out some of our adventures!',header_text)

        #They are asked to login to continue but they are new
        #and must click register.
