import os
import func
import time

from tqdm import tqdm

exec(func.get_cdn())
keyword_list = func.get_keyword()

if __name__ == "__main__":
    src = 'https://imagebase.net/images/2018/09/21/people024.md.jpg'
    save_root = r'C:\Users\Alchera\Desktop\crawl_img\CODE\ex'
    
    download(src, save_root, 1, ext='.png')
