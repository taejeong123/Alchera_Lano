import os
import re
import func

from tqdm import tqdm

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/total_keywords.txt')

if __name__ == "__main__":
    save_root = r'D:\00_PTJ_crawl\03_shutterstock'

    try:
        driver = chromedriver_settings(header=False, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        flag = False
        for keyword in keyword_list:
            if keyword == '천사': flag = True
            if not flag: continue

            url = r'https://www.shutterstock.com/ko/search/' + keyword

            idx = 0
            for x in tqdm(range(2000), desc=keyword):
                current_page = str(x + 1)

                if keyword == 'hat' and int(current_page) <= 624:
                    idx = 13340
                    continue

                try:
                    driver.get(url + r'?page=' + current_page)
                except:
                    continue

                scroll_smooth(driver, 1, .5)

                new_save_root = os.path.join(save_root, keyword)
                os.makedirs(new_save_root, exist_ok=True)

                img_list = driver.find_elements_by_css_selector('#content div div div div main div div div div div a img')
                for img in tqdm(img_list, desc=keyword + ' (' + str(current_page) + '/2000)'):
                    src = img.get_attribute('src')
                    try:
                        download(src, new_save_root, idx, ext='.png')
                    except:
                        continue
                    idx += 1

    except Exception as e:
        print(e)
    finally:
        driver.quit()