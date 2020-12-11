import os
import func
import time

from tqdm import tqdm

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/new_keywords.txt')

if __name__ == "__main__":
    save_root = r'\\192.168.0.139\e\PTJ_crawl\12_papersco'

    try:
        driver = chromedriver_settings(header=True, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        flag = False
        for keyword in keyword_list:
            if keyword == 'galaxy': flag = True
            if not flag: continue

            try:
                url = r'https://papers.co/?cat=1&s=' + keyword
                driver.get(url)
            except:
                continue

            idx = 0
            while True:
                time.sleep(3)
                try:
                    img_list = driver.find_elements_by_css_selector('li .category-all a img')
                except:
                    img_list = False
                if img_list:
                    for img in tqdm(img_list, desc=keyword):
                        new_save_root = os.path.join(save_root, keyword)
                        os.makedirs(new_save_root, exist_ok=True)

                        src_thumbnail = img.get_attribute('src')
                        src_image = src_thumbnail.split('/')[-1]
                        src_ori = src_image.replace('-1-wallpaper-300x300.jpg', '-36-3840x2400-4k-wallpaper.jpg')
                        src = r'https://papers.co/wallpaper/' + src_ori
                        if src:
                            try:
                                download(src, new_save_root, idx, ext='.png')
                            except:
                                continue
                        idx += 1

                try:
                    click_arg(driver, 'body div.container div.postcontainer div div.navigation a.next.page-numbers')
                    time.sleep(1)
                except:
                    break

    except Exception as e:
        print(e)
    finally:
        driver.quit()