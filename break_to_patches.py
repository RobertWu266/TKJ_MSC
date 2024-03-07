import cv2
from pathlib import Path
import Procrustes_API
import numpy as np
import pandas as pd
import pickle
need_list = np.array([int(x) for x in pd.read_excel("data(3).xlsx")["id"]])
contours_list = []
imgName_list=[]
imgPath_list = ["./images/"+str(need_list[i])+".jpg" for i in range(len(need_list))]

for img_path in imgPath_list:
    current_filename = Path(img_path).stem
    contours_list.append(Procrustes_API.find_contours(cv2.resize(cv2.imread(img_path), (400, 400))))

total_files = 5
split_size = len(contours_list) // total_files

for i in range(total_files):
    start_index = i * split_size
    # For the last file, make sure to include any remaining elements
    end_index = (i + 1) * split_size if i < total_files - 1 else len(contours_list)
    part = contours_list[start_index:end_index]
    with open(f'contours_part_{i}.pickle', 'wb') as f:
        pickle.dump(part, f)
