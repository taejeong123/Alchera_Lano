import os
import func
import time

from tqdm import tqdm

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/new_keywords.txt')

if __name__ == "__main__":
    save_root = r'\\192.168.0.139\e\PTJ_crawl\20_rawpixel'

    try:
        driver = chromedriver_settings(header=False, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        for keyword in keyword_list:            
            try:
                url = r'https://www.rawpixel.com/search/' + keyword
                driver.get(url)
                time.sleep(3)
            except:
                continue

            try:
                page = driver.find_element_by_css_selector('#page > div.content-wrapper > main > div > div.search-wrapper > div > nav > div.search-pager-cell > span > div > span')
                page = int(page.text)
            except:
                print('[ERROR]: no search result ' + keyword)
                continue

            idx = 0
            for p in range(page):
                try:
                    page_url = r'https://www.rawpixel.com/search/' + keyword + r'?sort=curated&page=' + str(p + 1)
                    driver.get(page_url)
                except:
                    continue

                scroll_smooth_divided(driver, 10, .5, 10)

                try:
                    img_list = driver.find_elements_by_css_selector('#page div.content-wrapper main div div div div.container-full figure div img')
                except:
                    img_list = False
                if img_list:
                    for img in tqdm(img_list, desc=keyword):
                        new_save_root = os.path.join(save_root, keyword)
                        os.makedirs(new_save_root, exist_ok=True)

                        src = img.get_attribute('srcset').split(' ')[0]
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