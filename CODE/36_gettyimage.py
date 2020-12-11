import os
import func
import time

from tqdm import tqdm

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/total_keywords.txt')

if __name__ == "__main__":
    save_root = r'D:\00_PTJ_crawl\36_gettyimage'

    try:
        driver = chromedriver_settings(header=False, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        flag = False
        for keyword in keyword_list:
            if keyword == 'rainbow': flag = True
            if not flag: continue

            try:
                url = r'https://mbdrive.gettyimageskorea.com/creative/?q=' + keyword + r'&rows=100#page=1'
                driver.get(url)
                time.sleep(3)
            except:
                continue

            # try:
            #     page = int(driver.execute_script('return document.querySelector("#search_total_page_top").innerText.replaceAll(",","")'))
            # except:
            #     print('[ERROR]: no search result ' + keyword)

            page = 2000

            idx = 0
            for p in range(page):
                try:
                    page_url = r'https://mbdrive.gettyimageskorea.com/creative/?q=' + keyword + r'&rows=100#page=' + str(p + 1)
                    driver.get(page_url)
                except:
                    continue

                time.sleep(3)
                scroll_smooth(driver, 1, 1)

                try:
                    img_list = driver.find_elements_by_css_selector('.thumbinsp .image .thumbnail')
                except:
                    break
                if img_list:
                    for img in tqdm(img_list, desc=keyword + ' (' + str(p + 1) + '/' + str(page) + ')'):
                        new_save_root = os.path.join(save_root, keyword)
                        os.makedirs(new_save_root, exist_ok=True)

                        src = img.get_attribute('src')
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