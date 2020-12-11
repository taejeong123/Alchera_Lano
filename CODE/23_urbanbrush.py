import os
import func
import time
import re

from tqdm import tqdm

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/new_keywords.txt')

if __name__ == "__main__":
    save_root = r'D:\00_PTJ_crawl\23_urbanbrush'

    try:
        driver = chromedriver_settings(header=False, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        for keyword in keyword_list:
            url = r'https://www.urbanbrush.net/?s=' + keyword + r'&post_type=download'
            driver.get(url)

            try:
                h2 = driver.find_element_by_css_selector('#header_inner > h2').text
                total_cnt = int(''.join(re.findall('\d+', h2)))
                page = int(total_cnt / 24 + 1)
            except:
                print('[ERROR]: no search result ' + keyword)
                continue

            scroll_smooth(driver, 1, .5)

            idx = 0
            for p in range(page):
                try:
                    page_url = r'https://www.urbanbrush.net/page/' + str(p + 1) + r'/?s=' + keyword + r'&post_type=download'
                    driver.get(page_url)
                except:
                    continue

                time.sleep(1)

                img_list = driver.find_elements_by_css_selector('.masonry-brick > div > div > a > img')
                if img_list:
                    for img in tqdm(img_list, desc=keyword + ' (' + str(p + 1) + '/' + str(page) + ')'):
                        new_save_root = os.path.join(save_root, keyword)
                        os.makedirs(new_save_root, exist_ok=True)

                        split_src = img.get_attribute('src').split('-')
                        src = '-'.join(split_src[:3]) + split_src[-1][-4:]
                        download(src, new_save_root, idx, ext='.png')
                        idx += 1

    except Exception as e:
        print(e)
    finally:
        driver.quit()