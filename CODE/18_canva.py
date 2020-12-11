import os
import func
import time

from tqdm import tqdm
from selenium.common.exceptions import NoSuchElementException

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/new_keywords.txt')

if __name__ == "__main__":
    save_root = r'D:\00_PTJ_crawl\18_canva'

    try:
        driver = chromedriver_settings(header=True, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        for keyword in keyword_list:
            url = r'https://www.canva.com/photos/search/' + keyword
            driver.get(url)

            driver.find_element_by_css_selector('#root div div div div div div div div div div div div div button').click()
            time.sleep(1)
            driver.find_element_by_css_selector('body div:nth-child(1) div div div div div div ul li:nth-child(3) button').click()
            time.sleep(5)

            try:
                msg = driver.find_element_by_css_selector('#root div div._D528A div div div.xNkxdA div div._2gt19g div div.yAe4gg p').text
                if '죄송합니다' in msg or 'Sorry' in msg:
                    print('no search result ' + keyword)
                    continue
            except NoSuchElementException:
                pass

            scroll_smooth_tqdm(driver, 200, 3)

            idx = 0
            img_list = driver.find_elements_by_css_selector('#root div div div div div div div div div div div div div a div div div div img')
            if img_list:
                for img in tqdm(img_list, desc=keyword):
                    new_save_root = os.path.join(save_root, keyword)
                    os.makedirs(new_save_root, exist_ok=True)

                    src = img.get_attribute('src')
                    if src and '/tl/' in src:
                        real_src = src.replace('/tl/', '/s2/')
                    elif src and '/thumbnail_large/' in src:
                        real_src = src.replace('thumbnail_large', 'screen_2x')
                    else:
                        continue

                    download(src, new_save_root, idx, ext='.png')
                    idx += 1

    except Exception as e:
        print(e)
    finally:
        driver.quit()