import os
import func
import time

from tqdm import tqdm

exec(func.get_cdn())
keyword_list = func.get_keyword()

if __name__ == "__main__":
    save_root = r'\\192.168.0.139\e\PTJ_crawl\13_imagebase'

    try:
        driver = chromedriver_settings(header=True, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        for keyword in keyword_list:
            url = r'https://imagebase.net/search/images/?q=' + keyword
            driver.get(url)

            # scroll_smooth_tqdm(driver, 5, 1)
            scroll_smooth(driver, 5, 1)

            idx = 0
            img_list = driver.find_elements_by_css_selector('#list-search-images div div div a img')
            if img_list:
                for img in tqdm(img_list, desc=keyword):
                    new_save_root = os.path.join(save_root, keyword)
                    os.makedirs(new_save_root, exist_ok=True)
                    src = img.get_attribute('src')
                    print(src)
                    # real_src = '/'.join(src.split('/')[0:-1]) + '/' + alt
                    download(src, new_save_root, idx, ext='.png')
                    idx += 1

    except Exception as e:
        print(e)
    finally:
        driver.quit()