import numpy as np
from time import time
from scipy.optimize import linear_sum_assignment

from My_KM import My_KM

def my_kuhn_munkres(mat, maximize):

    n = np.size(mat, 0)
    m = np.size(mat, 1)

    flag = False
    if n <= m:
        flag = True

    num = -1
    if maximize:
        num = 1

    mat = mat.ravel()
    mat = (num * mat).tolist()
    km = My_KM(mat, n, m)
    km.compute()
    matches = km.getMatch(flag)

    if n <= m:
        row_ind = np.array(range(n))
        return row_ind, np.array(matches)
    else:
        col_ind = np.array(range(m))
        return np.array(matches), col_ind

if __name__ == "__main__":
    # print(windll.kernel32)
    # print(platform.architecture())

    w = np.array([11.2472, 0.229506, 0.0382638, 0.0381432, 0.0397027, 0.0313909,
                  0.224794, 8.14484, 0.0458661, 0.0453376, 0.0466399, 0.0367264,
                  0.0299137, 0.0354885, 0.163514, 0.149832, 0.138921, 0.0995749,
                  0.0395173, 0.0463618, 21.4613, 0.963952, 0.436966, 0.255043,
                  0.041079, 0.0473524, 0.46014, 0.818429, 15.3917, 0.8489,
                  0.0330598, 0.0378731, 0.264884, 0.380127, 0.944165, 26.4972,
                  0.0391057, 0.0455497, 1.07156, 9.93479, 0.726293, 0.35456,
                  0.0355863, 0.0427534, 0.317523, 0.236992, 0.185949, 0.124624], np.float32).tolist()

    w = np.array([94.72742649, 98.15901842, 23.17530884, 72.82023363, 77.80301925, 112.4354889, 158.1281655, 75.92693992, 114.1252596, 23.44355586, 110.0611357, 114.5370204, 69.42635549, 14.39993735, 78.83025886, 13.0, 96.08826036, 102.8120997, 13.0]).tolist()
    tic = time()
    km = My_KM(w, 19, 1)
    km.compute()
    toc = time()

    print('KM costs {}s'.format(toc - tic))
    # print(km)   #print the weight matrix

    # match = km.getMatch(False) # False 返回列
    match = km.getMatch(True) # True 返回行
    print('Kuhn Munkres match:')
    print(match)

    max_w = km.maxWeight()
    print('Max matching weights: {}'.format(max_w))

    pass