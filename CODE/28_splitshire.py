import os
import func
import time

from tqdm import tqdm

exec(func.get_cdn())
# keyword_list = ['tree', 'winter tree', 'bountiful tree']
keyword_list = func.get_keyword('keywords/new_keywords.txt')

if __name__ == "__main__":
    save_root = r'\\192.168.0.139\e\PTJ_crawl\28_splitshire'

    try:
        driver = chromedriver_settings(header=False, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        for keyword in keyword_list:
            url = r'https://www.splitshire.com/?s=' + keyword
            driver.get(url)

            for x in range(15):
                try:
                    next_btn = driver.find_element_by_css_selector('#index-1 div.isotope-footer.style-light.single-gutter div nav a')
                    driver.execute_script("arguments[0].click();", next_btn)
                    scroll_smooth(driver, 1, 3)
                except:
                    break

            idx = 0
            img_list = driver.find_elements_by_css_selector('#index-1 div.isotope-wrapper div div.tmb div div.t-entry-visual div div a img')
            if img_list:
                for img in tqdm(img_list, desc=keyword):
                    new_save_root = os.path.join(save_root, keyword)
                    os.makedirs(new_save_root, exist_ok=True)

                    src = img.get_attribute('src')
                    download(src, new_save_root, idx, ext='.png')
                    idx += 1

    except Exception as e:
        print(e)
    finally:
        driver.quit()