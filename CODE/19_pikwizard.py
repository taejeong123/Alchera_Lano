import os
import func
import time

from tqdm import tqdm

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/new_keywords.txt')

if __name__ == "__main__":
    save_root = r'\\192.168.0.139\e\PTJ_crawl\19_pikwizard'
    # 하트 heart 곰돌이 곰인형 별 star 다이아몬드 Diamond 은하수 galaxy 벨벳 스판벨벳 velvet 젤리 jelly 무지개 rainbow
    page_list = [0, 1, 0, 0, 0, 5, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1]

    try:
        driver = chromedriver_settings(header=False, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        for x in range(len(keyword_list)):
            keyword = keyword_list[x]
            page = page_list[x]

            if page <= 0:
                print('no search result ' + keyword)
                continue

            idx = 0
            for p in range(page):
                try:
                    url = r'https://pikwizard.com/?q=' + keyword + r'&perpage=100&page=' + str(p + 1)
                    driver.get(url)
                    time.sleep(5)
                except:
                    continue

                scroll_smooth(driver, 5, 5)

                try:
                    img_list = driver.find_elements_by_css_selector('.photo-container img')
                except:
                    img_list = False
                if img_list:
                    for img in tqdm(img_list, desc=keyword + '(' + str(p + 1) + '/' + str(page) + ')'):
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