import os
import time
import func

from tqdm import tqdm

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/new_keywords.txt')

if __name__ == "__main__":
    save_root = r'D:\00_PTJ_crawl\06_flickr'
    prev_datas = []

    try:
        driver = chromedriver_settings(header=False, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        for keyword in keyword_list:
            url = r'https://www.flickr.com/search/?text=' + keyword
            driver.get(url)

            idx = 0
            time.sleep(10)

            new_save_root = os.path.join(save_root, keyword)
            os.makedirs(new_save_root, exist_ok=True)

            for x in tqdm(range(100)):
                scroll_smooth(driver, 1, 1)
                try:
                    driver.find_element_by_css_selector('div.infinite-scroll-load-more button').click()
                    time.sleep(1)
                except:
                    pass
                href_list = driver.find_elements_by_css_selector('.interaction-view a.overlay')
                current_list = set(href_list) - set(prev_datas)
                prev_datas = href_list

                for href_doc in tqdm(list(current_list), desc=keyword):
                    href = href_doc.get_attribute('href')
                    new_tab_open(driver, href, .5)

                    try:
                        src = driver.find_element_by_css_selector('img.main-photo').get_attribute('src')
                    except:
                        src = False

                    if src: download(src, new_save_root, idx, ext='.png')

                    new_tab_close(driver, .5)
                    idx += 1

    except Exception as e:
        print(e)
    finally:
        driver.quit()