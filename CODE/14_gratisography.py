import os
import func
import time

from tqdm import tqdm

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/new_keywords.txt')

if __name__ == "__main__":
    save_root = r'D:\00_PTJ_crawl\14_gratisgraphy'

    try:
        driver = chromedriver_settings(header=True, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        for keyword in keyword_list:
            try:
                url = r'https://gratisography.com/?s=' + keyword
                driver.get(url)
            except:
                continue

            scroll_smooth(driver, 1, 1)

            idx = 0
            try:
                img_list = driver.find_elements_by_css_selector('div.thumb a.download')
            except:
                func.err_msg('img_list not found')
                img_list = False

            if img_list:
                for img in tqdm(img_list, desc=keyword):
                    new_save_root = os.path.join(save_root, keyword)
                    os.makedirs(new_save_root, exist_ok=True)

                    src = img.get_attribute('href')
                    if src:
                        try:
                            download(src, new_save_root, idx, ext='.png')
                        except:
                            continue
                    idx += 1

    except Exception as e:
        print(e)
    finally:
        driver.quit()