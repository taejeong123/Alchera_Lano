import os
import func
import time

from tqdm import tqdm

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/total_keywords.txt')

if __name__ == "__main__":
    save_root = r'D:\00_PTJ_crawl\37_fotosearch'

    try:
        driver = chromedriver_settings(header=False, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        flag = False
        for keyword in keyword_list:
            if keyword == 'cap': flag = True
            if not flag: continue

            keyword = keyword.replace(' ', '-')
            try:
                url = r'https://www.fotosearch.co.kr/photos-images/' + keyword + r'.html'
                driver.get(url)
            except:
                continue

            time.sleep(2)
            try:
                driver.execute_script('document.querySelector("div.result_header div.col-sm-3").classList = document.querySelector("div.result_header div.col-sm-3").classList.value.replace("hidden-xs","")')
                driver.execute_script('document.querySelector("div.result_header div.col-sm-3 form").classList += " open"')
                click(driver, 'form ul li div select[name="ipp"]')
                click(driver, 'form ul li div select[name="ipp"] option[value="200"]')
            except:
                continue
            time.sleep(5)

            page = 50

            idx = 0
            for p in range(page):
                try:
                    page_url = r'https://www.fotosearch.co.kr/photos-images/' + keyword + r'_' + str(p + 1) + r'.html'
                    driver.get(page_url)
                except:
                    continue

                scroll_smooth(driver, 1, 1)

                try:
                    img_list = driver.find_elements_by_css_selector('#image_results div div a div div img')
                except:
                    time.sleep(300)
                    img_list = False
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