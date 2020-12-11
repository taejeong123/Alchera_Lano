import os
import func
import time

from tqdm import tqdm

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/new_keywords.txt')

if __name__ == "__main__":
    save_root = r'\\192.168.0.139\e\PTJ_crawl\05_picjumbo'

    try:
        driver = chromedriver_settings(header=True, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        for keyword in keyword_list:
            url = r'https://picjumbo.com/search/' + keyword
            driver.get(url)

            idx = 0
            keyword_cnt = 0
            while True:
                new_save_root = os.path.join(save_root, keyword)
                os.makedirs(new_save_root, exist_ok=True)

                img_list = driver.find_elements_by_css_selector('body div.tri_img_wrap div div a picture img')
                for img in tqdm(img_list, desc=keyword + '_' + str(keyword_cnt)):
                    src = img.get_attribute('src').split('?')[0]
                    download(src, new_save_root, idx, ext='.png')
                    idx += 1
                keyword_cnt += 1

                try:
                    time.sleep(1)
                    next_btn = driver.find_element_by_css_selector('body div div a.next.page-numbers')
                    driver.execute_script("arguments[0].click();", next_btn)
                except:
                    break

    except Exception as e:
        print(e)
    finally:
        driver.quit()