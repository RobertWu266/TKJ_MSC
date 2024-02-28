from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import time
import create_excel
import cv2
import Procrustes_API
from tqdm import tqdm
import os
import numpy as np
import pandas as pd
import gc
from concurrent.futures import ProcessPoolExecutor, as_completed

# 選擇要分析的檔案生成檔案路徑列表
def select():
    FilePath_list = []
    root = tk.Tk()
    root.withdraw()
    FilePath_list = filedialog.askopenfilenames(parent=root, initialdir="/home/wu/PycharmProjects/TKJ_MSC",
                                                title='Select File')

    return FilePath_list


# need_arr=np.zeros(60000)
# 建立圖片路徑列表
# imgPath_list = select()
need_list = np.array([int(x) for x in pd.read_excel("data(3).xlsx")["id"]])
# for i in need_list: need_arr[i]=1
# 建立圖片列表與圖片名稱列表
contours_list = []
imgName_list=[]
imgPath_list = ["./images/"+str(need_list[i])+".jpg" for i in range(len(need_list))]
#imgPath_list = ["./medium_test/"+i for i in os.listdir("./medium_test")]

with tqdm(total=len(imgPath_list), desc='Processing Images', unit='image') as pbar:
    for img_path in imgPath_list:
        current_filename = Path(img_path).stem
        pbar.set_postfix(File=current_filename)
        contours_list.append(Procrustes_API.find_contours(cv2.resize(cv2.imread(img_path), (400, 400))))

        imgName_list.append(current_filename)
        pbar.update(1)

start = time.time()
# 計算相似度
Similarity = 0
#Similarity_list = [[0 for _ in range(len(contours_list))] for _ in range(len(contours_list))]
Similarity_list=np.zeros((len(contours_list),len(contours_list)),dtype=float)
total_iterations =  (len(contours_list)+1)*len(contours_list)/2
#pairs = [(np.int16(i), np.int16(j)) for i in range(len(contours_list)) for j in range(i+1, len(contours_list))]
iteration = 0
fail_pic=[]

for i in range(len(contours_list)):
        for j in range(i + 1, len(contours_list)):
            a, b, Similarity = Procrustes_API.Procrustes_analysis(contours_list[i], contours_list[j])
            if a==2147:
                fail_pic.append(i)
                break
            Similarity_list[i][j] = Similarity  # if Similarity < 0.005 else 10
            Similarity_list[j][i] = Similarity  # if Similarity < 0.005 else 10
            iteration += 1
            if(iteration % 200000 ==0):gc.collect()
            pbar.set_postfix(File=imgName_list[j])
            pbar.update(1)



end = time.time()

# 建立excel檔案
#create_excel.create_excel(imgName_list, Similarity_list)
(pd.DataFrame(Similarity_list)).to_csv('./full_data.csv', index=False, header=False)

print('time:', end - start)
print(fail_pic)