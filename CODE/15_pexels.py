import os
import time
import func

from tqdm import tqdm

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/new_keywords.txt')

if __name__ == "__main__":
    save_root = r'D:\00_PTJ_crawl\15_pexels'

    try:
        driver = chromedriver_settings(header=True, gpu=False, log=False, driver_root='bin/chromedriver.exe')
        
        for keyword in keyword_list:
            url = r'https://www.pexels.com/ko-kr/search/' + keyword
            driver.get(url)

            scroll_smooth(driver, 1, 1)
            # scroll_smooth_tqdm(driver, 1000, 1)

            # idx = 0
            # img_list = driver.find_elements_by_css_selector('article a.js-photo-link.photo-item__link img.photo-item__img')
            # if img_list:
            #     for img in tqdm(img_list, desc=keyword):
            #         new_save_root = os.path.join(save_root, keyword)
            #         os.makedirs(new_save_root, exist_ok=True)

            #         src = img.get_attribute('src').split('?')[0]
            #         download(src, new_save_root, idx, ext='.png')
            #         idx += 1

    except Exception as e:
        print(e)
    finally:
        driver.quit()