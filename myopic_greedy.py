import math
import datetime
from datetime import datetime as dt

from common import get_euclidean_distance, dis_to_time, dispatch


def myopic_greedy(driver_list, order_list, rate):
    for order in order_list:
        the_driver = None
        min_dis = 99999.0
        x1 = order.o_start_x
        y1 = order.o_start_y

        for driver in driver_list:
            dis = get_euclidean_distance(driver.d_pos_x, driver.d_pos_y, x1, y1)
            if driver.d_reward == 0.0:  # 司机如果是第一单 那么就没有上一单
                driver.d_ttime = order.o_stime  # 则把上一单的结束时间置为这个订单的下单时间

            if order.o_ttime < driver.d_ttime:  # 该订单的乘客没耐心等这个司机这么久
                continue

            if order.o_stime > driver.d_ttime:  # 司机上一单已经跑完 这个订单还没出现
                continue

            if min_dis > dis:  # 距离贪心
                min_dis = dis
                the_driver = driver


        if the_driver == None:
            # print(f'{order.o_id}号订单找不到司机接单')
            continue
        else:
            print(f'{order.o_id}号订单分派给{the_driver.d_id}号车 车和订单距离：{min_dis}')

        dispatch(order, the_driver, the_driver.d_ttime, rate)

    return driver_list, order_list