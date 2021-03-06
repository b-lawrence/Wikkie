import unittest
from selenium import webdriver

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()


    def tearDown(self):
        self.browser.quit()


    def test_creating_a_new_list(self):

        # Edith has heard about a cool new to-do app. She goes to
        # check it out its homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention to-do lists.
        self.assertIn('To-Do', self.browser.title)


# Run tests
if __name__ == "__main__":
    unittest.main()
