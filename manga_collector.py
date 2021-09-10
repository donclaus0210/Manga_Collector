from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
import urllib

def CollectManga(url:str, manga_name:str):
    try:
        chrome_options = Options()
        # chrome_options.headless = True
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@id="reader-wrapper"]/div[9]/div[2]/div/div[2]/span/em[2]')
            )
        )



        current_chapter = driver.find_element_by_xpath('//*[@id="reader-wrapper"]/div[2]/div[3]/div[2]/span[1]').text
        number_of_pages = int(driver.find_element_by_xpath('//*[@id="reader-wrapper"]/div[9]/div[2]/div/div[2]/span/em[2]').text)

        for count in range(number_of_pages-1):
            WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "page-next")
                )
            )
            img = driver.find_element_by_xpath('//*[@id="reader-wrapper"]/div[4]/div[2]/div[1]/img').get_attribute('src')
            urllib.request.urlretrieve(img, f'{current_chapter}_{count+1}.png')
            elem = driver.find_element_by_class_name('page-next')
            elem.click()
            sleep(1)
        current_chapter = driver.find_element_by_xpath('//*[@id="reader-wrapper"]/div[2]/div[3]/div[2]/span[1]').text


        driver.find_element_by_xpath('//*[@id="reader-wrapper"]/div[2]/div[3]/div[3]').click()
        sleep(5)
        url = driver.current_url
    except:
        url = None
    finally:
        driver.close()
        return url

if __name__ == '__main__':
    new_url = ''
    url = input("Digite a url do mangá: ")
    nome = input("Digite o nome do mangá: ")

    while True:
        new_url = CollectManga(url, nome)
        if new_url == None:
            new_url = url
        elif new_url == url:
            break
        else:
            url = new_url