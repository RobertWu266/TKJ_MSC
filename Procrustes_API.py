# 引入所需的模組
import argparse
import numpy as np
from scipy.spatial import procrustes
import matplotlib.pyplot as plt
from scipy.interpolate import splprep, splev
import cv2

# 定義一個函數來調整圖像的對比度和亮度
def adjust_contrast_brightness(img, contrast, brightness):
    output = img * (contrast/127 + 1) - contrast + brightness    # 轉換公式
    output = np.clip(output, 0, 255)
    output = np.uint8(output)

    return output
def show_contour(shape,contour):
    return#commentable
    blk=np.zeros(shape)
    cv2.drawContours(blk,contour,-1, (0, 255, 0), 2)
    plt.imshow(cv2.cvtColor(np.uint8(blk), cv2.COLOR_BGR2RGB))
    plt.title("Image with Contours")
    plt.axis('off')  # Hide the axis
    plt.show()


# 定義一個函數來找出圖像的輪廓
def find_contours(img):
    # 調整圖像的對比度和亮度
    img = adjust_contrast_brightness(img, contrast=100, brightness=-100)
    
    # 將圖像轉換為灰度圖
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 使用Canny邊緣檢測來找出圖像的邊緣
    edges = cv2.Canny(gray_img, 25, 125)

    # 建立一個3x3的核並進行膨脹操作來強化邊緣
    kernel = np.ones((3, 3), np.uint8)
    dilated_edges = cv2.dilate(edges, kernel, iterations=4)

    # 找出輪廓
    contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 建立一個與灰度圖像大小相同的空圖像並在上面填充輪廓
    contour_img = np.zeros_like(gray_img)
    cv2.fillPoly(contour_img, pts=contours, color=(255, 255, 255))
    
    # 再次進行Canny邊緣檢測和膨脹操作
    contour_edges = cv2.Canny(contour_img, 25, 125)
    dilated_contour_edges = cv2.dilate(contour_edges, kernel, iterations=4)
    
    # 再次找出輪廓
    contours, _ = cv2.findContours(dilated_contour_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    show_contour(img.shape,contours)
    return contours  # 返回輪廓

# 定義一個函數進行Procrustes分析
def Procrustes_analysis(contours1, contours2):
    # 壓縮的第一個元素的第二個維度
    try:
        contours1 = np.squeeze(contours1[0], axis=1)
    except:
        return 2147,2147,2147

    try:
        contours2 = np.squeeze(contours2[0], axis=1)
    except:
        return 2148,2148,2148
    # 獲取兩個輪廓中的最大長度
    new_size = max(len(contours1), len(contours2))
    
    # 對兩個輪廓進行參數化
    tck1, _ = splprep(contours1.T, k=2, s=0)
    tck2, _ = splprep(contours2.T, k=2, s=0)
    
    # 建立一個新的均勻分布的參數向量
    u_new = np.linspace(0, 1, new_size)
    
    # 對兩個輪廓進行插值
    contours1_interp = np.column_stack(splev(u_new, tck1))
    contours2_interp = np.column_stack(splev(u_new, tck2))
    
    # 進行Procrustes分析並計算Procrustes距離
    mtx1, mtx2, disparity = procrustes(contours1_interp, contours2_interp)
    procrustes_distance = round(disparity**2, 6)
    
    # 使用分數變換來將 Procrustes 距離映射到 [0, 1] 範圍
    # normalized_procrustes_distance = round(1 - 1 / (1 + procrustes_distance), 6)
    
    return 0,0, procrustes_distance  # 返回對齊後的輪廓和正規化後的Procrustes距離


def main():
    # 建立命令列參數解析器
    parser = argparse.ArgumentParser(description='Procrustes Analysis of Images')
    
    # 添加兩個命令列參數
    parser.add_argument('image1', type=str, help='Path to the first image')
    parser.add_argument('image2', type=str, help='Path to the second image')
    
    # 解析命令列參數
    args = parser.parse_args()

    # 讀取並調整圖片的大小
    image1 = cv2.resize(cv2.imread(args.image1), (416, 416))
    image2 = cv2.resize(cv2.imread(args.image2), (416, 416))

    # 使用findContours獲取輪廓
    contours1 = find_contours(image1)
    contours2 = find_contours(image2)

    cont1 = np.zeros_like(image1)
    cont2 = np.zeros_like(image2)

    cv2.drawContours(cont1, contours1, -1, (255, 255, 255), 2)
    cv2.drawContours(cont2, contours2, -1, (255, 255, 255), 2)

    cv2.imshow('cont1', cont1)
    cv2.imshow('cont2', cont2)

    # 進行Procrustes分析
    aligned_contours1, aligned_contours2, procrustes_distance = Procrustes_analysis(contours1, contours2)

    # 打印對齊後的輪廓和Procrustes距離
    print("Aligned Contour 1:\n", aligned_contours1)
    print("Aligned Contour 2:\n", aligned_contours2)
    print("Procrustes Distance (Squared):", procrustes_distance)
    
    # 壓縮的第一個元素的第二個維度
    contours1 = np.squeeze(contours1[0], axis=1)
    contours2 = np.squeeze(contours2[0], axis=1)

    # 可視化對齊後的輪廓
    plt.figure()
    plt.plot(contours1[:, 0], contours1[:, 1], label='Contour 1', marker='o')
    plt.plot(contours2[:, 0], contours2[:, 1], label='Contour 2', marker='o')
    plt.plot(aligned_contours1[:, 0], aligned_contours1[:, 1], label='Aligned Contour 1', linestyle='--', marker='x')
    plt.legend()
    plt.title('Procrustes Analysis')
    plt.show()
    cv2.waitKey(5000)
    
# 當此程式作為主程式執行時，呼叫main函數
if __name__ == "__main__":
    main()
