#-1. делаем запрос на сайт с выбранным товаром
#-2.Готовим суп и выбираем цену
#-3. Формируем условие
#4. Отправляемс смс

import requests
from bs4 import BeautifulSoup
import smtplib

SMTP_ADDRESS = "outlook.office365.com"
MY_EMAIL = "Aleshichevigor@outlook.com"
PASSWORD = "45rhfy7853rt"

url = "https://www.amazon.com/dp/B0053WRWX8/ref=sbl_dpx_kitchen-electric-cookware_B07NSTN2R4_0?th=1"
header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8"
}
response = requests.get(url, headers=header)     #создаём запрос на сайт адрес + язык
# print(response.text)

soup = BeautifulSoup(response.content, 'lxml')       # суп с контентом

price = soup.find("span", class_="a-offscreen").get_text()    # достаём текст из html
price_without_currency = price.split("$")[1]     #редактируем текст
price_as_float = float(price_without_currency)      # тип Float
print(price_as_float)
title = soup.find("h1", class_="a-size-large a-spacing-none").get_text().strip()
print(title)

if price_as_float < 200:     # формируем условие
        message = f"{title} is now {price}"        #  формируем смс

        with smtplib.SMTP("outlook.office365.com") as connection:
                connection.starttls()       # защита письма
                result = connection.login(MY_EMAIL, PASSWORD)     # подключаемся к почте
                connection.sendmail(
                        from_addr=MY_EMAIL,
                        to_addrs=MY_EMAIL,
                        msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}"
                )                                 # отправляем письмо