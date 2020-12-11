import os
import func

from tqdm import tqdm

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/new_keywords.txt')

if __name__ == "__main__":
    save_root = r'\\192.168.0.139\e\PTJ_crawl\02_picsart'

    try:
        driver = chromedriver_settings(header=False, gpu=False, log=False, driver_root='bin/chromedriver.exe')
        flag = False
        for keyword in keyword_list:
            if keyword == 'heart': flag = True
            if not flag: continue

            url = r'https://picsart.com/search/stickers?q=' + keyword
            driver.get(url)

            while True:
                try:
                    btn = driver.find_element_by_css_selector('div.load-more-btn-container div a')
                    if not btn.get_attribute('href'): break
                    driver.execute_script("arguments[0].click();", btn)
                    scroll_smooth(driver, 1, 3)
                except Exception as e:
                    print(e)
                    break

            new_save_root = os.path.join(save_root, keyword)
            os.makedirs(new_save_root, exist_ok=True)

            img_list = driver.find_elements_by_css_selector('div.c-preview-container figure a div img')
            idx = 0
            for img in tqdm(img_list, desc=keyword):
                src = img.get_attribute('src').split('?')[0]
                download(src, new_save_root, idx, ext='.png')
                idx += 1

    except Exception as e:
        print(e)
    finally:
        driver.quit()