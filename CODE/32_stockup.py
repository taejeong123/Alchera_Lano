import os
import func
import time

from tqdm import tqdm
from selenium.webdriver.common.keys import Keys

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/new_keywords.txt')

if __name__ == "__main__":
    save_root = r'\\192.168.0.139\e\PTJ_crawl\32_stockup'

    try:
        driver = chromedriver_settings(header=True, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        for keyword in keyword_list:
            url = r'https://stockup.sitebuilderreport.com'
            driver.get(url)
            time.sleep(1)

            search_box = driver.find_element_by_css_selector('.search-box form #q')
            search_box.clear()
            search_box.send_keys(keyword)
            search_box.send_keys(Keys.ENTER)
            time.sleep(3)

            idx = 0
            page_cnt = 0
            while True:
                scroll_smooth(driver, 1, 1)
                time.sleep(3)
                try:
                    img_list = driver.find_elements_by_css_selector('#hits ul li a img')
                except:
                    img_list = False
                if img_list:
                    for img in tqdm(img_list, desc=keyword + '_' + str(page_cnt + 1)):
                        new_save_root = os.path.join(save_root, keyword)
                        os.makedirs(new_save_root, exist_ok=True)

                        src = img.get_attribute('src').replace('small', 'original')
                        download(src, new_save_root, idx, ext='.png')
                        idx += 1

                try:
                    driver.find_element_by_css_selector('#pagination li a[title="Go to next page"]').click()
                    page_cnt += 1
                except:
                    break

    except Exception as e:
        print(e)
    finally:
        driver.quit()