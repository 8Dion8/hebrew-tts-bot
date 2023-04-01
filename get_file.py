from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver import FirefoxOptions
from selenium.webdriver import FirefoxProfile

import os
import requests
from time import sleep
import telebot as tb

opts = FirefoxOptions()

opts.add_argument("--headless")

driver = webdriver.Firefox(executable_path='geckodriver', options=opts)
driver.install_addon("./adblock_plus-3.16.2.xpi")
driver.get("https://ttsfree.com/text-to-speech")


TOKEN = os.environ.get('TOKEN')

bot = tb.TeleBot(TOKEN)

bot.send_message(741069625, "Bot online.")


@bot.message_handler(func=lambda msg: True)
def main_react(message):
    word = message.text

    select_click = driver.find_element("xpath","/html/body/section[2]/div[2]/form/div[2]/div[1]/div[1]/div[2]/span[1]")
    driver.execute_script("arguments[0].scrollIntoView();", select_click)
    select_click.click()
    input_lang  = driver.find_element("xpath","/html/body/span/span/span[1]/input")
    input_lang.send_keys("hebrew")
    select_lang = driver.find_element("id","select2-select_lang_bin-results")
    driver.execute_script("arguments[0].scrollIntoView();", select_lang)
    select_lang.click()

    word_input = driver.find_element("id","input_text")
    driver.execute_script("arguments[0].scrollIntoView();", word_input)
    word_input.clear()
    word_input.send_keys(word)

    start_button = driver.find_element("xpath","/html/body/section[2]/div[2]/form/div[2]/div[2]/a")
    driver.execute_script("arguments[0].scrollIntoView();", start_button)

    start_button.click()
    sleep(10)
    driver.execute_script("arguments[0].scrollIntoView();", start_button)
    audio_link = driver.find_element("xpath","/html/body/section[2]/div[2]/form/div[2]/div[2]/div[3]/div[2]/audio/source[1]").get_attribute("src")
    print(audio_link)

    r = requests.get(audio_link)

    with open(f"{word}.mp3", "wb") as f:
        f.write(r.content)

    
    bot.send_audio(message.chat.id, open(f"{word}.mp3", "rb"))

bot.infinity_polling()