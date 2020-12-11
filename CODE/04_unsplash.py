import os
import time
import func

from tqdm import tqdm

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/new_keywords.txt')

if __name__ == "__main__":
    save_root = r'D:\00_PTJ_crawl\04_unsplash'

    prev_datas = []

    try:
        driver = chromedriver_settings(header=False, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        flag = False
        for keyword in keyword_list:
            if keyword == 'velvet': flag = True
            if not flag: continue

            try:
                url = r'https://unsplash.com/s/photos/' + keyword
                driver.get(url)
            except:
                continue

            idx = 0
            for x in range(1000):
                try:
                    driver.execute_script("window.scrollTo({top: document.querySelector('#app div').scrollHeight - 2000, behavior: 'smooth'});")
                    time.sleep(3)
                except:
                    continue

                try:
                    img_list = driver.find_elements_by_css_selector('#app div div div div div div div div div figure div div._3A74U div div a div div.c_6Je div img')
                    current_list = set(img_list) - set(prev_datas)
                    prev_datas = img_list
                except:
                    img_list = False

                if not current_list or len(current_list) <= 0:
                    print('[ERROR]: keyword "' + keyword + '" - no images')
                    break

                new_save_root = os.path.join(save_root, keyword)
                os.makedirs(new_save_root, exist_ok=True)

                for img in tqdm(current_list, desc=keyword + ' (' + str(x + 1) + '/1000)'):
                    src = img.get_attribute('src').split('?')[0]
                    try:
                        download(src, new_save_root, idx, ext='.png')
                    except:
                        pass
                    idx += 1

    except Exception as e:
        print(e)
    finally:
        driver.quit()