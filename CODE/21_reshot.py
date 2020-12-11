import os
import func
import time

from tqdm import tqdm

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/new_keywords.txt')

def scroll(driver, n, t):
    for i in tqdm(range(n), desc=keyword + '_scroll'):
        driver.execute_script("window.scrollTo({top: document.body.scrollHeight - 1000, behavior: 'smooth'});")
        time.sleep(t)

def get_img_list(driver):
    try:
        img_list = driver.find_elements_by_css_selector('.photo-grid-item .grid-photo a img')
    except:
        img_list = False
    return img_list

if __name__ == "__main__":
    save_root = r'\\192.168.0.139\e\PTJ_crawl\21_reshot'

    try:
        driver = chromedriver_settings(header=False, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        for keyword in keyword_list:
            try:
                url = r'https://www.reshot.com/search/' + keyword
                driver.get(url)
            except:
                continue

            if not get_img_list(driver):
                print('[ERROR]: no search result ' + keyword)
                continue

            scroll(driver, 500, 1)

            idx = 0
            img_list = get_img_list(driver)
            if img_list:
                for img in tqdm(img_list, desc=keyword + '_download'):
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