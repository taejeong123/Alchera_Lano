import os
import time
import func

from tqdm import tqdm

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/new_keywords.txt')

if __name__ == "__main__":
    save_root = r'D:\00_PTJ_crawl\16_burst'

    try:
        driver = chromedriver_settings(header=False, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        for keyword in keyword_list:
            try:
                url = r'https://burst.shopify.com/photos/search?q=' + keyword
                driver.get(url)
            except:
                continue

            try:
                total_str = driver.find_element_by_css_selector('h1.section-heading__heading.heading--1').text
                total = total_str.split(' ')[0]
            except:
                continue

            if total == 'No':
                print(total_str)
                continue

            page = int(int(total) / 30 + 1)

            idx = 0
            for p in tqdm(range(page), desc=keyword):
                try:
                    url = r'https://burst.shopify.com/photos/search?page=' + str(p + 1) + '&q=' + keyword
                    driver.get(url)
                except:
                    continue

                try:
                    img_list = driver.find_elements_by_css_selector('#Main section div div div div div a div img')
                except:
                    func.err_msg('img_list not found')
                    continue
                for img in tqdm(img_list, desc=keyword + '(' + str(p + 1) + '/' + str(page) + ')'):
                    new_save_root = os.path.join(save_root, keyword)
                    os.makedirs(new_save_root, exist_ok=True)

                    src = img.get_attribute('src').split('?')[0]
                    download(src, new_save_root, idx, ext='.png')
                    idx += 1

    except Exception as e:
        print(e)
    finally:
        driver.quit()