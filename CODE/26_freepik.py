import os
import func
import time

from tqdm import tqdm

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/total_keywords.txt')

if __name__ == "__main__":
    save_root = r'D:\00_PTJ_crawl\26_freepik'

    try:
        driver = chromedriver_settings(header=False, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        flag = False
        for keyword in keyword_list:
            if keyword == 'heart': flag = True
            if not flag: continue

            try:
                url = r'https://kr.freepik.com/search?dates=any&format=search&page=1&query=' + keyword + r'&sort=popular'
                driver.get(url)
            except:
                continue

            # try:
            #     page = int(driver.execute_script('return document.querySelector("div.pagination__context.hide-phone span.pagination__pages").innerText.replaceAll(",", "")'))
            #     print(keyword, page)
            # except:
            #     print('[ERROR]: no search result ' + keyword)
            #     continue

            page = 1000

            idx = 0
            for p in range(page):
                try:
                    page_url = r'https://kr.freepik.com/search?dates=any&format=search&page=' + str(p + 1) + r'&query=' + keyword + r'&sort=popular'
                    driver.get(page_url)
                    time.sleep(1)
                except:
                    continue

                scroll_smooth_divided(driver, 10, 1, 10)

                img_list = driver.find_elements_by_css_selector('#main section.showcase div div figure div a img')
                if img_list:
                    for img in tqdm(img_list, desc=keyword + ' (' + str(p + 1) + '/' + str(page) + ')'):
                        new_save_root = os.path.join(save_root, keyword)
                        os.makedirs(new_save_root, exist_ok=True)

                        src = img.get_attribute('src')
                        if 'avatar' in src: continue
                        try:
                            download(src, new_save_root, idx, ext='.png')
                        except:
                            pass
                        idx += 1

    except Exception as e:
        print(e)
    finally:
        driver.quit()