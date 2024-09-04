import numpy as np
from selenium import webdriver
from Searchengines.Extract_Models import extract_model_name
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import undetected_chromedriver as uc
from Searchengines.AddVal import add_value_to_next_empty_cell_in_row
import time
from datetime import datetime
from selenium.webdriver.common.by import By
import os
import pandas as pd
import re
import uuid
def WildberriesSearch(e, path, lock, X, Y, positions):
    custom_dir = f"driver"
    unique_id = str(uuid.uuid4())
    # Создаем директорию, если она не существует
    os.makedirs(custom_dir, exist_ok=True)

    # Создаем патчер с указанием пользовательского пути для сохранения chromedriver
    patcher = uc.Patcher(executable_path=os.path.join(custom_dir, 'chromedriver.exe'))
    patcher.auto()  # Автоматическая настройка патчера

    # Опции для Chrome
    options = webdriver.ChromeOptions()
    # Используем уникальные пользовательские данные и профиль для каждого процесса
    options.add_argument(f"--user-data-dir=C:/Users/User/AppData/Local/Google/Chrome/User Data/{unique_id}")
    options.add_argument(f'--profile-directory=Profile_{unique_id}')

    # Создание экземпляра Chrome с патчером
    driver = uc.Chrome(options=options, patcher=patcher, driver_executable_path=fr"C:\Users\user\PycharmProjects\WildberriesFind\driver\chromedriver.exe")
    file_path = path.split("_")[0]
    file_path = rf'{file_path}_{e + 1}.xlsx'
    lock.release()
    df = pd.read_excel(file_path)
    def process_element(element):
        print("process_element начался")
        aoao = wait.until(EC.presence_of_all_elements_located((By.XPATH, ".//div/a")))
        link = element.find_element("xpath", ".//a")
        text = link.text
        our_text = row
        if our_text:
            text_extracted = extract_model_name(text.lower())
            our_text = extract_model_name(our_text.lower())
            # similarity_percentage1 = similarity_percentage(text_extracted.lower().replace(" ", ""),our_text.lower().replace(" ", ""))
            word = text.split()
            # price = element.find_element(By.XPATH, "./div/div[1]/div/span[1]").text
            # print(text + "   " + link.get_attribute("href") + "   " + str(price) +""+ str(similarity_percentage1))
            # print(text_extracted+" "+our_text+" "+str(similarity_percentage1))
            # text_lower = text.lower().replace(" ","").replace("-","").replace("brait","")
            # our_text_lower = our_text.lower().replace(" ","").replace("-","").replace("brait","")
            # print(our_text_lower +"   "+text_lower)
            print("da")
            add_value_to_next_empty_cell_in_row(df, index, link.get_attribute("href"))
            df.to_excel(file_path, index=False)
    for index, row in df.iloc[:, 1].items():
        try:
            driver.get("https://www.wildberries.ru/catalog/0/search.aspx?search="+"BRAIT "+df.iloc[index,1].split()[0]+" "+df.iloc[index, 3]+"&from_global=true")
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            wait = WebDriverWait(driver, 10)
        except:
            print("nea")
        try:
            driver.find_element(By.XPATH,"//h1[@class='not-found-search__title']")
            print("Ne naideno")
        except:
            try:
                driver.find_element(By.XPATH,"//p[@class='searching-results__text']")
                print("Найдено")
            except:
                try:
                    elementozs = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='product-card-overflow']//div[@class='product-card__wrapper']")))
                    elementozs = driver.find_elements(By.XPATH,"//div[@class='product-card-overflow']//div[@class='product-card__wrapper']")
                    for element in elementozs:
                        process_element(element)
                except:
                    print("Не нашлось")
    de = pd.read_excel(file_path)
    # time.sleep(30)
    for index, row in de.iterrows():
        for column, value in row[4:].items():
            print("AuoAu")
            if pd.notna(value) and pd.notnull(value):
                print("Work?")
                driver.get(value)
                wait = WebDriverWait(driver, 5)
                try:
                    w8 = wait.until(EC.presence_of_element_located(("xpath","//div[@class='product-page__aside']//div[@class='product-page__seller-wrap hide-mobile']//span[@class='seller-info__name']")))
                    magazin = driver.find_element("xpath","//div[@class='product-page__aside']//div[@class='product-page__seller-wrap hide-mobile']//span[@class='seller-info__name']").text
                    print("norm")
                except:
                    try:
                        w8 = wait.until(EC.presence_of_element_located(("xpath", "//div[@class='product-page__aside']//div[@class='product-page__seller-wrap hide-mobile']//span[@class='seller-info__name premium']")))
                        magazin = driver.find_element("xpath","//div[@class='product-page__aside']//div[@class='product-page__seller-wrap hide-mobile']//h3[@class='seller-info__default-name']").text
                    except:
                        magazin = "unknown"
                try:
                    w8 = wait.until(EC.presence_of_element_located(("xpath", "//div[@class='product-page__aside']//div[@class='product-page__price-block product-page__price-block--aside']//div[@class='price-block__content']//p[@class='price-block__price-wrap ']//del[@class='price-block__old-price']")))
                    price = driver.find_element("xpath", "//div[@class='product-page__aside']//div[@class='product-page__price-block product-page__price-block--aside']//div[@class='price-block__content']//p[@class='price-block__price-wrap ']//del[@class='price-block__old-price']").text
                except:
                    price = "Нет в наличии"
                # except:
                #     print("Произошла ошибка с ссылкой " + value)
                #     price = 0
                #     magazin = "none"
                print(f"Цена   {price}Магазин   {magazin} Валуе {value}")
                new_data = {
                    'Наименование': de.iloc[index, 3],
                    'Store Name': magazin,
                    'Price': str(price),
                    'Link': value
                }
                row_index = de.index[de['Наименование'] == new_data['Наименование']]
                if len(row_index) > 0:
                    store_col = f"{' '.join(new_data['Store Name'].split()).title()}"
                    if store_col in de.columns:
                        de.loc[row_index, store_col] = new_data['Price']
                        de.loc[row_index, f"{store_col} Link"] = new_data['Link']
                        # de.loc[row_index, f"{store_col} Article"] = new_data['Article']
                    else:
                        de[store_col] = np.nan
                        de.loc[row_index, store_col] = new_data['Price']
                        de.loc[row_index, f"{store_col} Link"] = new_data['Link']
                        # de.loc[row_index, f"{store_col} Article"] = new_data['Article']
                else:
                    new_row = {
                        'Наименование': new_data['Наименование'],
                        'Store A': np.nan,
                        'Store B': np.nan,
                        'Store C': np.nan
                    }
                    store_col = f"{' '.join(new_data['Store Name'].split()).title()}"
                    new_row[store_col] = new_data['Price']
                    new_row[f"{store_col} Link"] = new_data['Link']
                    # new_row[f"{store_col} Article"] = new_data['Article']
                    de = pd.concat([de,pd.DataFrame([new_row])],ignore_index=True)
                de.to_excel(file_path, index=False)
    print("Отправка файла")
    driver.close()
    driver.quit()