import os
import func
import time

from tqdm import tqdm

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/new_keywords.txt')

if __name__ == "__main__":
    save_root = r'D:\00_PTJ_crawl\11_morguefile'
    prev_datas = []

    try:
        driver = chromedriver_settings(header=True, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        for keyword in keyword_list:
            idx = 0
            for x in range(500):
                url = r'https://morguefile.com/photos/morguefile/' + str(x + 1) + r'/' + keyword + r'/pop'
                driver.get(url)
                time.sleep(3)

                if 'Try searching' in driver.find_element_by_css_selector('body').text:
                    break

                try:
                    img_list = driver.find_elements_by_css_selector('#imgScrllPage div.scrolld-item.thumb')
                    # current_list = list(set(img_list) - set(prev_datas))
                    # prev_datas = img_list
                except:
                    continue
                if img_list:
                    for img in tqdm(img_list, desc=keyword + ' (' + str(x) + '/500)'):
                        new_save_root = os.path.join(save_root, keyword)
                        os.makedirs(new_save_root, exist_ok=True)

                        src = img.get_attribute('data-jpg')
                        try:
                            download(src, new_save_root, idx, ext='.png')
                        except:
                            pass
                        idx += 1

    except Exception as e:
        print(e)
    finally:
        driver.quit()