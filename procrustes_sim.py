import Procrustes_API
import numpy as np
import pandas as pd
import argparse
import pickle

# 選擇要分析的檔案生成檔案路徑列表


def main():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument('-a', type=int, help='First number')
    parser.add_argument('-b', type=int, help='Second number')
    args = parser.parse_args()
    # args.a,args.b
    # 計算相似度
    contours_list_a = []
    contours_list_b = []
    patch_size = 4692

    with open(f'contours_part_{args.a}.pickle', 'rb') as f:
        part = pickle.load(f)
        contours_list_a.extend(part)
    with open(f'contours_part_{args.b}.pickle', 'rb') as f:
        part = pickle.load(f)
        contours_list_b.extend(part)
    fail_pic = []
    Similarity_list = np.zeros(shape=(len(contours_list_a), len(contours_list_b)), dtype=float)

    if args.a != args.b:
        for i in range(len(contours_list_a)):
            for j in range(len(contours_list_b)):
                a, b, similarity = Procrustes_API.Procrustes_analysis(contours_list_a[i], contours_list_b[j])
                if a == 2147:
                    break
                Similarity_list[i][j] = similarity
    else:
        for i in range(len(contours_list_a)):
            for j in range(i + 1, len(contours_list_b)):
                a, b, similarity = Procrustes_API.Procrustes_analysis(contours_list_a[i], contours_list_b[j])
                if a == 2147:
                    fail_pic.append(i)
                    break
                Similarity_list[i][j] = similarity
                Similarity_list[j][i] = similarity

    if args.a == args.b:
        print("%d," % (patch_size * args.a + i) for i in fail_pic)
    # 建立excel檔案
    out_name = './full_data_%d_%d,%d_%d.csv' % (args.a, args.b, len(contours_list_a), len(contours_list_b))
    (pd.DataFrame(Similarity_list)).to_csv(out_name, index=False, header=False)
if __name__ == "__main__":
    main()