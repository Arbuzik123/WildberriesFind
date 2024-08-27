from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium import webdriver
import re
from selenium.webdriver.support.ui import WebDriverWait
import time
import undetected_chromedriver as uc
import requests
def updateWildberries(e, path, lock,X,Y,positions):
    options = webdriver.ChromeOptions()
    # options.add_argument("--user-data-dir=C:/Users/User/AppData/Local/Google/Chrome/User Data")
    # options.add_argument(f'--profile-directory=Profile 1')
    # options.add_argument(rf"--load-extension=C:\Users\Dimulka\Downloads\Spp12")
    driver = uc.Chrome(options=options)
    lock.release()
    driver.set_window_size(X, Y)
    driver.set_window_position(*positions, windowHandle='current')
    file_path = path.split("_")[0]
    file_path = rf'{file_path}_{e + 1}.xlsx'
    df = pd.read_excel(file_path)
    print("UpdateWB rabotaet")
    for col_name in df.columns[4:]:
        for index, value in df[col_name].items():
            if str(value) != "nan" and pd.api.types.is_numeric_dtype(value) == False and str(value).startswith('http'):
                driver.get(value)
                time.sleep(1)
                wait = WebDriverWait(driver, 15)
                # try:
                #     w8 = wait.until(EC.presence_of_element_located(("xpath", "//div[@class='product-page__seller-wrap section-border hide-desktop']//span[@class='seller-info__name']")))
                #     magazin = driver.find_element("xpath","//div[@class='product-page__seller-wrap section-border hide-desktop']//span[@class='seller-info__name']").text
                #     print("norm")
                # except:
                #     try:
                #         # w8 = wait.until(EC.presence_of_element_located(("xpath", "//a[@class='seller-info__name seller-info__name--link']")))
                #         magazin = "unknown"
                #     except:
                #         continue
                # try:

                try:
                    w8 = wait.until(EC.presence_of_element_located(("xpath",
                                                                    "//div[@class='product-page__aside']//div[@class='product-page__price-block product-page__price-block--aside']//div[@class='price-block__content']//p[@class='price-block__price-wrap ']//ins[@class='price-block__final-price wallet']")))
                    price = driver.find_element("xpath",
                                                "//div[@class='product-page__aside']//div[@class='product-page__price-block product-page__price-block--aside']//div[@class='price-block__content']//p[@class='price-block__price-wrap ']//ins[@class='price-block__final-price wallet']").text
                except:
                    try:
                        w8 = wait.until(EC.presence_of_element_located(("xpath",
                                                                        "//div[@class='product-page__aside']//div[@class='product-page__price-block product-page__price-block--aside']//div[@class='price-block__content']//p[@class='price-block__price-wrap ']//span[@class='price-block__wallet-price']")))
                        price = driver.find_element("xpath",
                                                    "//div[@class='product-page__aside']//div[@class='product-page__price-block product-page__price-block--aside']//div[@class='price-block__content']//p[@class='price-block__price-wrap ']//span[@class='price-block__wallet-price']").text
                    except:
                        price = "Нет в наличии"
                # except:
                # w8 = wait.until(EC.presence_of_element_located(("xpath", "//div[@class='wbcon__check-prices-second wbcon__check-prices-cell']")))
                # price = driver.find_element("xpath","//div[@class='wbcon__check-prices-second wbcon__check-prices-cell']").text
                # except:
                #     price = "Нет в наличии"
                print(f"Цена   {price} Валуе {value}")
                price1 = re.sub(r"\D", "", price)
                # current_date = datetime.datetime.now().strftime('%d-%m-%Y')
                # new_column_name = f'Цена за {current_date}'
                # # df[new_column_name] = current_date
                # df.loc[index, new_column_name] = price1
                prev_col_index = df.columns.get_loc(col_name) - 1
                prev_col_name = df.columns[prev_col_index]
                # df[new_column_name] = current_date
                df.loc[index, prev_col_name] = price1
                # result_file_path = os.path.join(result_directoryWB, "" + file)
                df.to_excel("wb.xlsx", index=False)
    driver.quit()
    lock.release()
    file_path = path.split("_")[0]
    file_path = rf'{file_path}_{e + 1}.xlsx'
    df = pd.read_excel(file_path)
    print("UpdateWB rabotaet")
    regex_pattern = r"https://www.wildberries.ru/catalog/(\d+)/detail.aspx"
    # Применяем регулярное выражение
    for col_name in df.columns[4:]:
        for index, value in df[col_name].items():
            if str(value) != "nan" and pd.api.types.is_numeric_dtype(value) == False and str(value).startswith('http'):
                match = re.search(regex_pattern, value)
                if match:
                    article = match.group(1)
                    response1 = requests.get('http://92.63.192.39:371/spp')
                    if response1.status_code == 200:
                        data = response1.json()
                        spp = int(data['spp'])
                        print(spp)
                        url = "https://card.wb.ru/cards/detail?appType=2&curr=rub&dest=-1257786&spp=" + str(
                            spp) + "&nm=" + article
                        print(url)
                        response = requests.get(url)
                        if response.status_code == 200:
                            data = response.json()
                            try:
                                price = float(data['data']['products'][0]['extended']['basicPriceU']) / 100
                            except:
                                try:
                                    price = float(data['data']['products'][0]['priceU']) / 100
                                except:
                                    price = 0
                        print(str(price))
                        prev_col_index = df.columns.get_loc(col_name) - 1
                        prev_col_name = df.columns[prev_col_index]
                        # df[new_column_name] = current_date
                        df.loc[index, prev_col_name] = price
                        # result_file_path = os.path.join(result_directoryWB, "" + file)
                        df.to_excel(file_path, index=False)

