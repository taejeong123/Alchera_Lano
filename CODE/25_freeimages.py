# import os
# import func
# import time

# from tqdm import tqdm

# exec(func.get_cdn())
# keyword_list = func.get_keyword()

# if __name__ == "__main__":
#     save_root = r'\\192.168.0.139\e\PTJ_crawl\25_freeimages'
#     page = 10

#     try:
#         driver = chromedriver_settings(header=True, gpu=False, log=False, driver_root='bin/chromedriver.exe')

#         for keyword in keyword_list:
#             idx = 0
#             for p in range(page):
#                 url = r'https://www.freeimages.com/kr/search/' + keyword + r'/' + str(p + 1)
#                 driver.get(url)
#                 time.sleep(1)
#                 scroll_smooth(driver, 1, 1)

#                 try:
#                     img_list = driver.find_elements_by_css_selector('.thumbnail-rowgrid .item a img')
#                 except:
#                     img_list = False
#                 if img_list:
#                     for img in tqdm(img_list, desc=keyword + ' (' + str(p + 1) + '/' + str(page) + ')'):
#                         new_save_root = os.path.join(save_root, keyword)
#                         os.makedirs(new_save_root, exist_ok=True)

#                         src = img.get_attribute('src').replace('small', 'large')
#                         download(src, new_save_root, idx, ext='.png')
#                         idx += 1

#     except Exception as e:
#         print(e)
#     finally:
#         driver.quit()

# FUCKING CAPTCHA
# FUCKING CAPTCHA
# FUCKING CAPTCHA
# FUCKING CAPTCHA
# FUCKING CAPTCHA
# FUCKING CAPTCHA
# FUCKING CAPTCHA
# FUCKING CAPTCHA
# FUCKING CAPTCHA
# FUCKING CAPTCHA