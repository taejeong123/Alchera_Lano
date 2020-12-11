import os
import time
import func

from tqdm import tqdm

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/new_keywords.txt')

if __name__ == "__main__":
    save_root = r'D:\00_PTJ_crawl\17_kaboompics'

    try:
        driver = chromedriver_settings(header=False, gpu=False, log=False, driver_root='bin/chromedriver.exe')
        
        for keyword in keyword_list:
            try:
                url = r'https://kaboompics.com/gallery?search=' + keyword
                driver.get(url)
            except:
                continue

            scroll_smooth(driver, 1, 1)

            try:
                next_btn = driver.find_element_by_css_selector('#top div.pagination span.last a')
                next_href = next_btn.get_attribute('href')
                page = int(next_href.split('page=')[-1])
            except:
                page = 1
                print(keyword + ' no search result')

            idx = 0
            for p in tqdm(range(page), desc=keyword):
                page_url = url + r'&page=' + str(p + 1)
                driver.get(page_url)

                try:
                    img_list = driver.find_elements_by_css_selector('#work-grid li div.work-img a img')
                except:
                    continue
                if img_list:
                    for img in tqdm(img_list, desc=keyword + '(' + str(p + 1) + '/' + str(page) + ')'):
                        new_save_root = os.path.join(save_root, keyword)
                        os.makedirs(new_save_root, exist_ok=True)

                        src = img.get_attribute('data-srcset')
                        real_src = src.split(' ')
                        src_list = []
                        for x in real_src:
                            if 'http' in x: src_list.append(x)
                        if len(src_list) > 0: final_src = src_list[-1]
                        try:
                            download(final_src, new_save_root, idx, ext='.png')
                        except:
                            continue
                        idx += 1

    except Exception as e:
        print(e)
    finally:
        driver.quit()