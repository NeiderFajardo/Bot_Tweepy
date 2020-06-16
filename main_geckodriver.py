#!/bin/python3


from selenium import webdriver
from decouple import config
import time
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


USER_NAME = config('USER_TWITTER')
PASSWORD = config('PASSWORD')

class Bot:
    def __init__(self, user, passwd, busquedas):
        self.user = user
        self.passwd = passwd
        self.bot = webdriver.Firefox()
        self.a_buscar = busquedas


    def login(self):
        bot = self.bot
        bot.get('https://twitter.com/explore')
        time.sleep(3)
        email = bot.find_element_by_name('session[username_or_email]')
        password = bot.find_element_by_name('session[password]')
        email.clear()
        password.clear()
        email.send_keys(self.user)
        password.send_keys(self.passwd)
        password.submit()
        time.sleep(5)


    def like_tweet(self, nums):
        bot = self.bot
        for b in self.a_buscar:
            bot.get('https://twitter.com/search?q='+b+'&src=typeahead_click')
            time.sleep(3)
            for i in range(nums):
                bot.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(2)
                x = WebDriverWait(bot, 20).until(EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "div[data-testid='like'][role='button']"))).click()

busqueda = sys.argv[1:]
prueba = Bot(USER_NAME, PASSWORD, busqueda)
prueba.login()
prueba.like_tweet(3)