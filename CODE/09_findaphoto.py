import os
import func
import time

from tqdm import tqdm
from selenium.common.exceptions import NoSuchElementException

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/new_keywords.txt')

if __name__ == "__main__":
    save_root = r'D:\00_PTJ_crawl\09_findaphoto'

    try:
        driver = chromedriver_settings(header=False, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        flag = False
        for keyword in keyword_list:
            url = r'https://www.chamberofcommerce.org/findaphoto/search?q=' + keyword
            driver.get(url)

            idx = 0
            while True:
                try:
                    scroll_smooth(driver, 1, 5)

                    try:
                        img_list = driver.find_elements_by_css_selector('#container a div.real-image-wrapper img')
                    except:
                        img_list = False
                    if img_list:
                        for img in tqdm(img_list, desc=keyword):
                            new_save_root = os.path.join(save_root, keyword)
                            os.makedirs(new_save_root, exist_ok=True)

                            src = img.get_attribute('src').replace('280h', '960w')
                            if '.svg' in src: continue
                            
                            download(src, new_save_root, idx, ext='.png')
                            idx += 1

                    next_btn = driver.find_element_by_css_selector('body div.search-results-header div:nth-child(4) div div div:nth-child(2) a')
                    next_btn_classlist = next_btn.get_attribute('class')
                    if 'disabled' in next_btn_classlist:
                        break
                    driver.get(next_btn.get_attribute('href'))
                except NoSuchElementException:
                    break

    except Exception as e:
        print(e)
    finally:
        driver.quit()