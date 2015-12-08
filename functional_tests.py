from selenium import webdriver
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
        assert 'Adventure' in browser.title, "Browser title was " + browser.title

if __name__ == '__main__':
    unittest.main(warnings = 'ignore')
