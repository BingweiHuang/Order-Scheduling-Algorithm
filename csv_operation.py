import csv
import numpy as np

order_list_dir = r"./datasets/order_list.csv"
driver_pos_dir = r"./datasets/driver_pos.csv"


driver_csv = csv.reader(open(driver_pos_dir))
driver_csv = list(driver_csv)
driver_pos = [[0] * 2 for i in range(len(driver_csv) - 1)]
for i, row in enumerate(driver_csv):
    if i == 0:
        continue
    for j, col in enumerate(row):
        if j == 0:
            continue
        else:
            driver_pos[i - 1][j - 1] = float(col)

driver_pos = np.array(driver_pos)
print(driver_pos)
print(np.size(driver_pos, 0))
print(np.size(driver_pos, 1))
print(driver_pos[299][1])


order_csv = csv.reader(open(order_list_dir))
order_csv = list(order_csv)




