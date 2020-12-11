import os
import func
import time

from tqdm import tqdm

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/new_keywords.txt')

if __name__ == "__main__":
    save_root = r'D:\00_PTJ_crawl\07_123freevectors'

    try:
        driver = chromedriver_settings(header=False, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        flag = False
        for keyword in keyword_list:
            if keyword == 'rainbow': flag = True
            if not flag: continue

            url = r'https://www.123freevectors.com/?s=' + keyword + r'&submit=Search'
            driver.get(url)

            page = 0
            page_doc = driver.find_elements_by_css_selector('.page-item .page-link:not(.next)')
            if page_doc:
                page = int(page_doc[-1].text)
            print(page)

            if page > 0:
                idx = 0
                for p in range(page):
                    url = r'https://www.123freevectors.com/page/' + str(p + 1) + r'/?s=' + keyword + r'&submit=Search'
                    driver.get(url)

                    new_save_root = os.path.join(save_root, keyword)
                    os.makedirs(new_save_root, exist_ok=True)

                    img_list = driver.find_elements_by_css_selector('#content div div.col-md-9 div.card-columns div div a img')
                    for img in tqdm(img_list, desc=keyword):
                        src = img.get_attribute('src').split('?')[0]
                        download(src, new_save_root, idx, ext='.png')
                        idx += 1

    except Exception as e:
        print(e)
    finally:
        driver.quit()