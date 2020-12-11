import os
import func
import time

from tqdm import tqdm
from selenium.webdriver.common.keys import Keys

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/new_keywords.txt')

if __name__ == "__main__":
    save_root = r'D:\00_PTJ_crawl\10_freerangestock'

    try:
        driver = chromedriver_settings(header=False, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        flag = False
        for keyword in keyword_list:

            url = r'https://freerangestock.com/search/all/' + keyword + r'?perpage=100'
            driver.get(url)
            time.sleep(3)

            try: page = int(driver.find_element_by_css_selector('span.pag-results-num').text)
            except: continue

            idx = 0
            for p in range(page):
                try: page_input = driver.find_element_by_css_selector('input#pageNum')
                except: break
                page_input.clear()
                page_input.send_keys(p + 1)
                page_input.send_keys(Keys.RETURN)
                time.sleep(1)

                img_list = driver.find_elements_by_css_selector('#main-col-id div div.tabs_content div div a img')
                if img_list:
                    for img in tqdm(img_list, desc=keyword):
                        new_save_root = os.path.join(save_root, keyword)
                        os.makedirs(new_save_root, exist_ok=True)
                        src = img.get_attribute('src').replace('thumbnail', 'sample')
                        download(src, new_save_root, idx, ext='.png')
                        idx += 1

    except Exception as e:
        print(e)
    finally:
        driver.quit()