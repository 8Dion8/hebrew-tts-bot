from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver import FirefoxOptions
from selenium.webdriver import FirefoxProfile

import os
import requests
from time import sleep
import telebot as tb

TOKEN = os.environ.get('TOKEN')
bot = tb.TeleBot(TOKEN)

opts = FirefoxOptions()
opts.add_argument("--headless")
bot.send_message(741069625, "Loading driver")
driver = webdriver.Firefox(executable_path='geckodriver', options=opts)
bot.send_message(741069625, "Installing addon")
driver.install_addon("./adblock_plus-3.16.2.xpi")
bot.send_message(741069625, "Loading page")
driver.get("https://ttsfree.com/text-to-speech")
sleep(2)
try:
    elem = driver.find_element("xpath", "//div[@class='qc-cmp-cleanslate css-cgzk6p']")
    driver.execute_script("arguments[0].style.visibility='hidden'", elem)
except:pass


bot.send_message(741069625, "Bot online.")

audio_link = ""


@bot.message_handler(func=lambda msg: True)
def main_react(message):
    global audio_link
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
    driver.execute_script("arguments[0].scrollIntoView();", start_button)
    while True:
        try:
            link = driver.find_element("xpath","/html/body/section[2]/div[2]/form/div[2]/div[2]/div[3]/div[2]/audio/source[1]").get_attribute("src")
            if link != audio_link:
                audio_link = link
            else:
                continue
            break
        except:sleep(1)

    #print(audio_link)

    r = requests.get(audio_link)

    with open(f"{word}.mp3", "wb") as f:
        f.write(r.content)

    
    bot.send_audio(message.chat.id, open(f"{word}.mp3", "rb"))

bot.infinity_polling()