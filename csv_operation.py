import csv
import numpy as np
import datetime
from datetime import datetime as dt
from operator import itemgetter
from Order import Order
from Driver import Driver

driver_pos_dir = r"./datasets/driver_pos.csv"
order_list_dir = r"./datasets/order_list.csv"

def get_driver_list(dir):
    driver_csv = csv.reader(open(dir))
    driver_csv = list(driver_csv)
    del driver_csv[0]
    driver_list = []

    for line in driver_csv:
        driver_list.append(Driver(line))

    return driver_list



def get_order_list(dir):
    order_csv = csv.reader(open(dir))
    order_csv = list(order_csv)
    del order_csv[0]
    order_list = []

    for line in order_csv:
        order_list.append(Order(line))

    order_list.sort(key=lambda x: (x.o_stime, x.o_ttime))

    return order_list


if __name__=="__main__":
    order_list = get_order_list(order_list_dir)
    for order in order_list:
        print(order.o_id, order.o_stime, order.o_wtime, order.o_ttime)

    driver_list = get_driver_list(driver_pos_dir)

    for driver in driver_list:
        print(driver.d_id, driver.d_pos_x, driver.d_pos_y, driver.d_ttime)


    pass