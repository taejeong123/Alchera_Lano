import os
import func
import time

from tqdm import tqdm

exec(func.get_cdn())
keyword_list = func.get_keyword('keywords/total_keywords.txt')

if __name__ == "__main__":
    save_root = r'\\192.168.0.139\e\PTJ_crawl\35_canstockphoto'

    try:
        driver = chromedriver_settings(header=False, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        flag = False
        for keyword in keyword_list:
            if keyword == '은하수': flag = True
            if not flag: continue

            keyword = keyword.replace(' ', '-')
            url = r'https://www.canstockphoto.co.kr/images-photos/' + keyword + r'.html'
            driver.get(url)

            # try:
            #     page = int(driver.execute_script('return document.querySelector("body main div.search-view div div div nav div.row div span span span").innerText.replaceAll(",","")'))
            # except:
            #     print('[ERROR]: no search result ' + keyword)

            time.sleep(2)
            driver.execute_script('document.querySelector("nav:nth-child(4) div.row div.nav.navbar-nav").classList = document.querySelector("nav:nth-child(4) div.row div.nav.navbar-nav").classList.value.replace("d-none","")')
            click(driver, 'nav:nth-child(4) div.row div.nav.navbar-nav div span')
            click(driver, '#_fg select[name="display_rows"]')
            click(driver, '#_fg select[name="display_rows"] option[value="200"]')
            time.sleep(5)

            page = 50

            idx = 0
            for p in range(page):
                page_url = r'https://www.canstockphoto.co.kr/images-photos/' + keyword + r'_' + str(p + 1) + r'.html'
                driver.get(page_url)

                scroll_smooth(driver, 1, 1)

                try:
                    img_list = driver.find_elements_by_css_selector('.search-view div div div div section article a span img')
                except:
                    time.sleep(300)
                    img_list = False
                if img_list:
                    for img in tqdm(img_list, desc=keyword + ' (' + str(p + 1) + '/' + str(page) + ')'):
                        new_save_root = os.path.join(save_root, keyword)
                        os.makedirs(new_save_root, exist_ok=True)

                        src = img.get_attribute('src')
                        download(src, new_save_root, idx, ext='.png')
                        idx += 1

    except Exception as e:
        print(e)
    finally:
        driver.quit()