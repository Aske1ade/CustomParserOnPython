import requests
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver import Firefox
from typing import List
import re
from configparser import ConfigParser
import psutil
import time
import pyautogui
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import os
from xml_editor import Creator


class BaseScraper:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('config.ini')
        self.service = FirefoxService(executable_path=self.config.get('main', 'driver_name'))
        self.driver = None

    def __start_browser(self):
        options = Options()
        options.headless = False
        self.driver = Firefox(service=self.service, options=options)

    def __navigate_to_website(self, url, city):
        self.driver.get(url=url)
        try:
            # Reduce implicit wait time
            location_popup = WebDriverWait(self.driver, 1).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'location-popup'))
            )

            # Replace XPath with a more concise expression
            city_li = location_popup.find_element(By.XPATH, city)
            city_li.click()
            # ...
        except TimeoutException:
            print('')

    def __solve_location_dialog(self, city):
        try:

            locate = self.driver.find_element(By.XPATH, '//*[@id="citySelector"]/span')
            locate.click()
            time.sleep(1)
        except:
            print('zaebosh')
        try:
            city_li = self.driver.find_element(By.XPATH, city)
            time.sleep(1)
            city_li.click()

        except Exception as e:
            print(f'Ошибка при решении диалогового окна выбора локации: {e}')
            raise Exception('Ошибка в solve_location_dialog')

    def navigate_pages(self, start_page=1, end_page=5):
        for page_number in range(start_page, end_page + 1):
            page_xpath = f'/html/body/div[1]/div[3]/div/div/div[3]/div/div/div[1]/div/div/div[2]/li[{page_number}]'
            try:
                # Ожидаем появления элемента навигации страницы
                page_element = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, page_xpath))
                )
                page_element.click()
                time.sleep(2)  # Подождите немного для загрузки содержимого страницы

                # Теперь вы можете вызвать функцию, которая получает информацию о товарах на странице
                self.get_product_info_from_current_page()

            except TimeoutException:
                print(f' {page_number} ')
            except Exception as e:
                print(f'Ошибка при попытке перейти на страницу {page_number}: {e}')

    def kill_firefox_processes(self):
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == 'firefox.exe':
                try:
                    process.kill()
                except psutil.NoSuchProcess:
                    pass

    def uploadXML(self):

        """self.kill_firefox_processes()
        self.driver.quit()"""

        self.driver.get('https://kaspi.kz/mc/')
        username = 'bigseosentr@gmail.com'
        password = 'Password1'
        time.sleep(4)
        try:
            wait = WebDriverWait(self.driver, 10)

            going_to_upload_items = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[1]/div/section/div/div[1]/div/ul[2]/li[2]/a")))
            going_to_upload_items.click()

        except TimeoutException:
            print("Next button not found or not clickable. End of the table.")

        file_path = r'D:\ZAKAZ\RETURN\kaspi_botRETURN (2)\kaspi_botRETURN\new_generated_xml.xml'

        input_element = self.driver.find_element(By.XPATH,
                                                 '//*[@id="app"]/div/section/div/div[2]/div/section[2]/div/section/div[1]/div[2]/label/input')

        # Очистите поле ввода (по желанию, в зависимости от ваших потребностей)
        input_element.clear()

        # Отправьте путь к файлу в поле ввода
        input_element.send_keys(file_path)

        # Используйте клавишу "Enter" на элементе ввода файла
        # input_element.send_keys(Keys.RETURN)

        print('Файл успешно загружен')
        self.driver.quit()

    def jointoCabinetInterface(self):

        self.__start_browser()
        self.driver.get('https://kaspi.kz/mc/#/login')

        username = 'zhdanov.meb@list.ru'
        password = 'Batonchik191288@'
        time.sleep(1)
        try:
            time.sleep(3)
            # Find the login button and click it using a more stable selector (e.g., ID)
            login_button = self.driver.find_element(By.ID, 'email_tab')
            login_button.click()

            # Find the email input field and enter your email using XPath
            email_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div/div/div/div/form/div[1]/div/div/section/div/section/div[2]/input")))
            email_field.send_keys(username)

            # Wait for the "Continue" button for the email step to be clickable
            wait = WebDriverWait(self.driver, 10)
            continue_button_email = wait.until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div/form/div[2]/div/button")))
            continue_button_email.click()

            # Find the password field and enter your password
            password_field = wait.until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div/div/div/div/form/div[1]/div/div/div[1]/input")))
            password_field.send_keys(password)

            # Find the "Continue" button for the password step and click it
            continue_button_password = wait.until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div/form/div[2]/div/button")))
            continue_button_password.click()

            time.sleep(5)

            going_to_controll_items = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[1]/div[2]/div/div/div/ul[2]/li[1]/a/div/div")))
            going_to_controll_items.click()
        except NoSuchElementException:
            self.close_browser()
            self.kill_firefox_processes()
            print("Next button not found or not clickable. End of the table.")

        item_names = []
        item_skus = []
        item_prices = []
        item_hrefs = []
        item_points = []

        #                       //*[@id="offers-table"]/div[2]/table/tbody/tr[2]/td[4]
        #                                                 //*[@id="offers-table"]/div[2]/table/tbody/tr[2]/td[2]/div/div/div[2]/p[1]/a



        # Get all rows in the table

        i = 0
        wait = WebDriverWait(self.driver, 10)


        # ... начало функции ...
        current_page = 1

        while True:
            time.sleep(3)
            # Получаем таблицу после каждого действия
            table = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="app"]/div[2]/section/div[2]/div/section/div[2]/div[2]/table'))
            )
            rows = table.find_elements(By.XPATH, '//tbody/tr')

            for index, row in enumerate(rows):
                # Обработка строки и извлечение данных
                name, sku, price, availability = self.extract_row_data(rows[index], index)
                item_names.append(name)
                item_skus.append(sku)
                item_prices.append(price)
                #item_hrefs.append(href)
                item_points.append(availability)
                rows = table.find_elements(By.XPATH, '//tbody/tr')
            # Проверяем, включена ли кнопка "Next"
            next_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="offers-table"]/div[2]/div/nav/a[2]')))
            disabled_value = next_button.get_attribute('disabled')
            if disabled_value == 'true':
                print("Next button is disabled. End of the table.")
                break

            # Нажимаем кнопку "Next"
            try:

                next_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="offers-table"]/div[2]/div/nav/a[2]')))
                next_button.click()
                #currentpage = currentpage + 1
            except TimeoutException:
                print("Next button not found or not clickable. End of the table.")
                break  # Break the loop if the "Next" button is not found or not clickable

            # Ждем обновления таблицы на новой странице
            WebDriverWait(self.driver, 10).until(
                EC.staleness_of(table)
            )

            # Увеличиваем текущую страницу
            current_page += 1

        # Закрываем браузер после завершения
        #self.close_browser()

        # Печатаем или возвращаем собранные данные
        collected_data =[
            {'name': name, 'sku': sku, 'price': price, 'points': points}
            for name, sku, price, href, points in zip(item_names, item_skus, item_prices, item_points)
        ]
        print(collected_data)
        return collected_data, item_names, item_skus, item_points

    def getterData(self, data):
        newdata = data[1], data[2], data[3], data[4]
        response = requests.get('http://127.0.0.1:5000/get_all_prices_python')
        if response.status_code == 200:
            prices_data = response.json()
        existing_data = newdata
        print(existing_data)
        minpricelist = []
        minpricelist = list(minpricelist)

        new_data_dict = {item["sku"]: item["min_prices"] for item in prices_data}

        # Добавляем минимальные цены к каждому товару в existing_data
        for i in range(len(existing_data[0])):
            sku = existing_data[2][i]  # SKU находится в третьем списке (индекс 2)
            if sku in new_data_dict:
                minpricelist.append(new_data_dict[sku])
                print(minpricelist)
            else:
                print("ne nashel s interface" + data[0][i]['price'])
                # Если SKU не найден в новых данных, добавляем пустую строку
                minpricelist.append(data[0][i]['price'])

        # Теперь existing_data содержит минимальные цены

        return minpricelist

    def everyItemgetNew(self, data):
        print('zashel v item')
        #data = self.jointoCabinet()
        newdata = data[1], data[2], data[3], data[4]
        minprices = self.getterData(data)
        hrefs = newdata[1]
        points = newdata[3]
        print(newdata)
        cityIDandPrices = []
        i = 0
        createXML = Creator()


        for i in range(len(hrefs)):
            print(points[i], hrefs[i], minprices[i])
            cityIDandPrices.append(self.GG(points[i], hrefs[i], minprices[i]))

        #self.close_browser()



        return newdata[0], newdata[1], newdata[2], newdata[3], cityIDandPrices

    def mainScript(self, data):
        print("pereshel v tempcop")
        createXML = Creator()
        createXML.create_xml_from_data(self.everyItemgetNew(data))

    def get_min_prices_list_from_db(self):
        # Вызываем endpoint '/get_min_prices' для получения данных
        response = requests.get(
            'http://localhost:5000/get_min_prices')  # Убедитесь, что ваш Flask сервер работает и доступен
        min_prices_list = response.json() if response.status_code == 200 else []
        return min_prices_list

    def extract_row_data(self, row, index):
        name_element = row.find_element(By.CLASS_NAME, 'is-5')
        name = name_element.text
        print(name)
        i = index % 10
        getsku_elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//p[@class='subtitle is-6']"))
        )
        sku = getsku_elements[i].text.split('\n')[1]
        print(sku)
        availability_element = row.find_element(By.XPATH, './/td[@data-label="Наличие в магазинах"]')
        availability = availability_element.text
        print(availability)
        price_element = row.find_element(By.XPATH, './/td[3]/p')
        price = price_element.text.replace('&nbsp;', '').replace(' ', '')
        print(price)
        """link_element = row.find_element(By.XPATH, ".//p[@class='is-5']/a")
        self.driver.execute_script("arguments[0].click();", link_element)"""

        # Ждем загрузки новой страницы и извлекаем нужный href
        """time.sleep(4)
        try:
            new_element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='master-product-info-fields__value']"))
            )
        except NoSuchElementException as e:
            print(f"Element not found: {e}")
        hrefik = new_element.find_element(By.XPATH, ".//div/a")
        print(hrefik.text)
        href = hrefik.get_attribute('href')
        # Возвращаемся обратно на предыдущую страницу
        self.driver.execute_script("window.history.go(-1)")

        # Обновляем страницу, чтобы обновить список строк
        self.driver.refresh()
        time.sleep(7)
        # Ждем, чтобы убедиться, что страница загружена после обновления
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="app"]/div/section/div/div[2]/div/section/div[2]/div[2]/table'))
        )
"""
        # Получаем таблицу после обновления


        print(name, sku, price, availability)
        return name, sku, price, availability

    def upload(self):

        current_directory = os.getcwd()
        file_path = os.path.join(current_directory, "new_generated_xml.xml")
        # geckodriver_path = r"C:\Users\snurm\PycharmProjects\pythonProject\sign_in_bot\geckodriver.exe"

        # Set the path to your Firefox executable
        # firefox_binary_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"

        # Set your Kaspi.kz credentials
        username = 'bigseosentr@gmail.com'
        password = 'Password1'

        # Configure Firefox options
        options = Options()
        # options.binary_location = firefox_binary_path

        driver = None

        try:
            # Set the path to GeckoDriver

            # Open the Kaspi.kz website
            self.driver.get('https://kaspi.kz/mc/#/login')

            time.sleep(2)

            # Find the login button and click it using a more stable selector (e.g., ID)
            login_button = self.driver.find_element(By.ID, "email_tab")
            login_button.click()

            # Find the email input field and enter your email using XPath
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                "/html/body/div[1]/div/div/div/div/form/div[1]/div/div/section/div/section/div[2]/input")))
            email_field.send_keys(username)

            # Wait for the "Continue" button for the email step to be clickable
            wait = WebDriverWait(self.driver, 10)
            continue_button_email = wait.until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div/form/div[2]/div/button")))
            continue_button_email.click()

            # Find the password field and enter your password
            password_field = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div/div/div/div/form/div[1]/div/div/div[1]/input")))
            password_field.send_keys(password)

            # Find the "Continue" button for the password step and click it
            continue_button_password = wait.until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div/form/div[2]/div/button")))
            continue_button_password.click()

            time.sleep(2)

            going_to_download_xml_file = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div/div/section/div/div[1]/div/ul[2]/li[2]/a/div/div")))
            going_to_download_xml_file.click()

            # Find and click the button to trigger the file dialog
            upload_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     "/html/body/div[1]/div/section/div/div[2]/div/section[2]/div/section/div[1]/div[2]/label/div/section"))
            )
            upload_button.click()

            # Wait for the file input element to be present
            file_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )

            # Send keys to the file input element
            file_input.send_keys(file_path)

            # Optionally, you can wait for a short time to ensure the file is processed
            time.sleep(1)

            pyautogui.hotkey('alt', 'f4')

            time.sleep(1)

            upload_xml_file = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div/div/section/div/div[2]/div/section/div/section/div[1]/button")))
            upload_xml_file.click()

            time.sleep(2)
            # Print a message indicating successful file upload
            print("File uploaded successfully!")

        except TimeoutException as e:
            print(f"Timeout Exception: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            # Close the browser window in the end
            if self.driver is not None:
                self.driver.quit()

        pass

    def getinfofromurl(self):
        try:
            self.driver.get('https://kaspi.kz/mc/#/login')
            elemen = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div/nav/div[1]/a[2]'))
            )
            return elemen.text.strip()
        except Exception as e:
            print(f'Ошибка при получении цены на товар: {e}')
            return None

    def __get_product_price(self, product_url):
        try:
            self.driver.get(product_url)
            price_element = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="offers"]/div/div/div[1]/table/tbody/tr[1]/td[4]/div'))
            )
            return price_element.text.strip()
        except Exception as e:
            print(f'Ошибка при получении цены на товар: {e}')
            return None

    def get_sku(self, product_url):
        try:
            self.driver.get(product_url)
            price_element = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="ItemView"]/div[2]/div/div[2]/div/div[1]/div[1]'))
            )
            return re.sub(r'\D', '', price_element.text.strip())
        except Exception as e:
            print(f'Ошибка при получении цены на товар: {e}')
            return None

    def browserStart(self, city):
        if not self.driver:
            self.__start_browser()

        self.__navigate_to_website('https://kaspi.kz/shop/', city)

        self.__solve_location_dialog(city)

    def browserStartwithHref(self, href, city):
        if not self.driver:
            self.__start_browser()
        self.__navigate_to_website(href, city)

        self.__solve_location_dialog(city)

    def get_product_info_from_url(self, product_url, city):
        # self.browserStartwithHref(product_url, city)
        self.driver.get(product_url)
        self.__solve_location_dialog(city)
        # self.__navigate_to_website(product_url, city)
        product_info_list = []
        total_products_required = 20
        current_page = 1
        # Optimize by using a single WebDriverWait instead of multiple calls
        wait = WebDriverWait(self.driver, 2)

        while len(product_info_list) < total_products_required:
            try:
                # Use explicit waits for critical elements
                price_elements = wait.until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, '//*[@id="offers"]/div/div/div[1]/table/tbody/tr/td[4]/div'))
                )
                seller_elements = wait.until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, '//*[@id="offers"]/div/div/div[1]/table/tbody/tr/td[1]/a'))
                )

                # Собираем данные о товарах на текущей странице
                for i in range(len(price_elements)):
                    price = price_elements[i].text.strip()
                    seller_name = seller_elements[i].text.strip()
                    seller_href = seller_elements[i].get_attribute("href")
                    product_info_list.append({'seller_name': seller_name, 'seller_href': seller_href, 'price': price})
                    if len(product_info_list) == total_products_required:
                        break

                if len(product_info_list) < total_products_required:
                    # Находим и кликаем по элементу "Следующая"
                    try:
                        next_page_element = WebDriverWait(self.driver, 2).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, '//li[contains(@class, "pagination__el") and text()="Следующая"]'))
                        )
                        next_page_element.click()
                        WebDriverWait(self.driver, 2).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="offers"]/div/div/div[1]/table/tbody'))
                        )
                    except TimeoutException:
                        print('Не удалось переключиться на следующую страницу')
                        break


            except Exception as e:

                print(f'Error occurred: {e}')

                break
        #print(product_info_list)
        return product_info_list

    def compare_prices(self, minimum_price, url, city):
        new_price = int(minimum_price)
        matching_products = []
        product_info_list = self.get_product_info_from_url(url, city)
        seller_name = 'DIGITAL HOME'
        for product in product_info_list:  # Iterating in reverse
            namesell = product['seller_name']
            #print(namesell)
            price_str = product['price'].replace(' ', '').replace('₸', '')  # Remove spaces and currency symbol
            if product['seller_name'] == seller_name:
                continue

            try:
                price = int(price_str)
                if price - 10 >= int(minimum_price):
                    new_price = price - 10
                    break

            except ValueError:
                print(f'Error converting price to integer: {price_str}')

        # print(self.get_sku(url))
        # url_sku = self.get_sku(url)
        # self.close_browser()
        return new_price

    def get_cityId(self, city):
        astana = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[1]/li[18]/a'
        karaganda = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[2]/li[20]/a'
        kostanai = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[2]/li[35]/a'
        ust_kaman = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[4]/li[15]/a'
        aktobe = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[1]/li[10]/a'
        aktau = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[1]/li[9]/a'
        atyrau = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[1]/li[20]/a'
        shymkent = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[4]/li[34]/a'
        pavlodar = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[3]/li[19]/a'
        almaty = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[1]/li[13]/a'
        # //*[@id="dialogService"]/div/div[1]/div[1]/div/ul[2]/li[21]/a
        # /html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[2]/li[21]/a
        # /html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[1]/li[18]/a
        almatyID = '750000000'
        astanaID = '710000000'
        karagandaID = '351010000'
        kostanaiID = '391010000'
        ust_kamanID = '271010000'
        aktobeID = '151010000'
        aktauID = '471010000'
        zhanaarkaID = '354430100'
        shymkentID = '511010000'
        pavlodarID = '551010000'

        if city == astana:
            currentID = astanaID
        elif city == karaganda:
            currentID = karagandaID
        elif city == kostanai:
            currentID = kostanaiID
        elif city == ust_kaman:
            currentID = ust_kamanID
        elif city == aktobe:
            currentID = aktobeID
        elif city == aktau:
            currentID = aktauID
        elif city == zhanaarkaID:
            currentID = zhanaarkaID
        elif city == shymkent:
            currentID = shymkentID
        elif city == pavlodar:
            currentID = pavlodarID
        else:
            currentID = ''

        return currentID

    def process_multiple_urls(self, urls: List[str], min_prices: List[str], city):
        self.browserStart(city)
        new_prices = []
        skus = []

        if len(urls) != len(min_prices):
            print("Error: Number of URLs must be equal to the number of minimum prices.")
            return

        for i, url in enumerate(urls):
            min_price = min_prices[i]

            # print(f"\nProcessing URL {i + 1}/{len(urls)}: {url}")
            result = self.compare_prices(min_price, url, city)
            new_price = result[0]
            sku = result[1]

            new_prices.append(new_price)
            skus.append(sku)

            # print(f"Minimum price for {url}: {new_price}")

        CurrentCityID = self.get_cityId(city)

        self.close_browser()
        return CurrentCityID, new_prices

    def close_browser(self):
        if self.driver:
            self.driver.quit()

    def getCityIDcityPrice(self, urls: List[str], cityids: List[str], min_prices: List[str]):
        new_prices = []

        self.__start_browser()
        self.driver.get()

        return None

    """astana = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[1]/li[18]/a'
        karaganda = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[2]/li[20]/a'
        kostanai = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[2]/li[35]/a'
        ust_kaman = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[4]/li[15]/a'
        aktobe = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[1]/li[10]/a'
        aktau = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[1]/li[9]/a'
        atyrau = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[1]/li[20]/a'
        shymkent = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[4]/li[34]/a'
        pavlodar = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[3]/li[19]/a'

        astanaID = '710000000'
        karagandaID = '351010000'
        kostanaiID = '391010000'
        ust_kamanID = '271010000'
        aktobeID = '151010000'
        aktauID = '471010000'
        zhanaarkaID = '354430100'
        shymkentID = '511010000'
        pavlodarID = '551010000'
        astanaPP = 'PP5'
        karagandaPP = 'PP4'
        zhanaarkaPP = 'PP13'
        shymkentPP = 'PP12'
        pavlodarPP = 'PP11'
        ust_kamanPP = 'PP7'
        aktobePP = 'PP6'
        kostanaiPP = 'PP9'
        aktauPP = 'PP10'
        """

    def process_pp3(self, href, prices):
        almaty = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[1]/li[13]/a'
        almatyID = '750000000'
        print("Обработка для PP5")
        return href, almatyID, self.compare_prices(prices, href, almaty)

    def process_pp5(self, href, prices):
        astana = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[1]/li[18]/a'
        astanaID = '710000000'
        print("Обработка для PP5")
        return href, astanaID, self.compare_prices(prices, href, astana)

    def process_pp4(self, href, prices):
        karaganda = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[2]/li[20]/a'
        karagandaID = '351010000'
        print("Обработка для PP4")
        return href, karagandaID, self.compare_prices(prices, href, karaganda)

    def process_pp13(self, href, prices):
        zhanaarka = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[4]/li[34]/a'
        zhanaarkaID = '354430100'
        print("Обработка для PP13")
        return href, zhanaarkaID, self.compare_prices(prices, href, zhanaarka)

    def process_pp12(self, href, prices):
        shymkent = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[4]/li[34]/a'
        shymkentID = '511010000'
        print("Обработка для PP12")
        return href, shymkentID, self.compare_prices(prices, href, shymkent)

    def process_pp11(self, href, prices):
        pavlodar = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[3]/li[19]/a'
        pavlodarID = '551010000'
        print("Обработка для PP11")
        return href, pavlodarID, self.compare_prices(prices, href, pavlodar)

    def process_pp7(self, href, prices):
        ust_kaman = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[4]/li[15]/a'
        ust_kamanID = '271010000'
        print("Обработка для PP7")
        return href, ust_kamanID, self.compare_prices(prices, href, ust_kaman)

    def process_pp6(self, href, prices):
        aktobe = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[1]/li[10]/a'
        aktobeID = '151010000'
        print("Обработка для PP6")
        return href, aktobeID, self.compare_prices(prices, href, aktobe)

    def process_pp9(self, href, prices):
        kostanai = '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/ul[2]/li[35]/a'
        kostanaiID = '391010000'
        print("Обработка для PP9")
        return href, kostanaiID, self.compare_prices(prices, href, kostanai)

    def process_pp10(self, href, prices):
        aktau = '/html/body/div[3]/div[1]/div/div/1/div[1]/div/ul[1]/li[9]/a'
        aktauID = '471010000'
        print("Обработка для PP10")
        return href, aktauID, self.compare_prices(prices, href, aktau)

    def GG(self, points, href, prices):
        try:
            self.__start_browser()
        except:
            pass
        pp_handlers = {
            'PP5': self.process_pp5,
            'PP4': self.process_pp4,
            'PP13': self.process_pp13,
            'PP12': self.process_pp12,
            'PP11': self.process_pp11,
            'PP7': self.process_pp7,
            'PP6': self.process_pp6,
            'PP9': self.process_pp9,
            'PP10': self.process_pp10,
        }

        # Обработка каждой строки входных данных
        out = []
        pps = points.split(', ')
        print(pps)
        prs = prices.split(',')
        print(prs)
        i = 0
        for pp in pps:

            if pp in pp_handlers:
                print(pp)
                print(prs[i])
                out.append(pp_handlers[pp](href, prs[i]))
                i = i + 1
        print(out)
        return out
