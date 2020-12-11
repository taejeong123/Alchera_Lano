import os
import func
import time

from tqdm import tqdm

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/new_keywords.txt')

if __name__ == "__main__":
    save_root = r'D:\00_PTJ_crawl\08_stocksnap'

    try:
        driver = chromedriver_settings(header=False, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        for keyword in keyword_list:
            url = r'https://stocksnap.io/search/' + keyword
            driver.get(url)

            scroll_smooth_tqdm(driver, 50, 1)

            idx = 0
            img_list = driver.find_elements_by_css_selector('#main div.photo-grid-item a img')
            if img_list:
                for img in tqdm(img_list, desc=keyword):
                    new_save_root = os.path.join(save_root, keyword)
                    os.makedirs(new_save_root, exist_ok=True)

                    src = img.get_attribute('src').replace('280h', '960w')
                    if '.svg' in src: continue
                    
                    download(src, new_save_root, idx, ext='.png')
                    idx += 1

    except Exception as e:
        print(e)
    finally:
        driver.quit()