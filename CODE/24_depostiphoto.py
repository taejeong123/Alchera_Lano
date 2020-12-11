import os
import func
import time

from tqdm import tqdm

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/total_keywords.txt')

if __name__ == "__main__":
    save_root = r'D:\00_PTJ_crawl\24_depostiphoto'

    try:
        driver = chromedriver_settings(header=False, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        flag = False
        for keyword in keyword_list:
            if keyword == 'seraph': flag = True
            if not flag: continue

            url = r'https://ko.depositphotos.com/stock-photos/' + keyword + r'.html?filter=all'
            driver.get(url)
            time.sleep(3)

            # try:
            #     total_cnt = driver.execute_script('return document.querySelector("._search-count-info div span span:nth-child(2)").innerText.replaceAll(",", "")')
            #     page = int(int(total_cnt) / 100)
            #     print(keyword, page)
            # except:
            #     print('[ERROR]: no search result ' + keyword)
            #     continue

            page = 200

            idx = 0
            for p in range(page):
                try:
                    url = r'https://ko.depositphotos.com/stock-photos/' + keyword + r'.html?offset=' + str(p * 100) + r'&filter=all'
                    driver.get(url)
                except:
                    continue

                scroll_smooth_divided(driver, 5, .5, 5)

                try:
                    img_list = driver.find_elements_by_css_selector('#root div section div section section div div div div div div div a img')
                except:
                    img_list = False

                if img_list:
                    for img in tqdm(img_list, desc=keyword + ' (' + str(p + 1) + '/' + str(page) + ')'):
                        new_save_root = os.path.join(save_root, keyword)
                        os.makedirs(new_save_root, exist_ok=True)
                        try:
                            src = img.get_attribute('src')
                            download(src, new_save_root, idx, ext='.png')
                        except:
                            pass
                        idx += 1

    except Exception as e:
        print(e)
    finally:
        driver.quit()