import math
import datetime
from datetime import datetime as dt


from csv_operation import get_driver_list, get_order_list

driver_pos_dir = r"./datasets/driver_pos.csv"
order_list_dir = r"./datasets/order_list.csv"

rate = 0.35
now_time = dt(2022, 6, 29, 18, 0)

def get_euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 -y2) ** 2)

def dis_to_time(dis):
    s = int(math.ceil(dis / rate * 60))
    return datetime.timedelta(seconds=s)


def myopic_greedy_order():
    driver_list = get_driver_list(driver_pos_dir)
    order_list = get_order_list(order_list_dir)

    for i, order in enumerate(order_list):
        number = -1
        min_dis = 99999.0
        x1 = order.o_start_x
        y1 = order.o_start_y
        x2 = order.o_dest_x
        y2 = order.o_dest_y
        for j, driver in enumerate(driver_list):
            dis = get_euclidean_distance(driver.d_pos_x, driver.d_pos_y, x1, y1)
            if driver.d_reward == 0.0:  # 司机如果是第一单 那么就没有上一单
                driver_list[j].d_ttime = order.o_stime  # 则把上一单的结束时间置为这个订单的下单时间

            if order.o_ttime < driver.d_ttime:  # 该订单的乘客没耐心等这个司机这么久
                continue

            # if order.o_stime > driver.d_ttime:  # 司机上一单已经跑完 这个订单还没出现
            #     continue

            if min_dis > dis:  # 距离贪心
                min_dis = dis
                number = j

        if number == -1:
            # print(f'{order.o_id}号订单找不到司机接单')
            continue

        driver_list[number].d_pos_x = x2
        driver_list[number].d_pos_y = y2
        driver_list[number].d_ttime += dis_to_time(min_dis + order.o_dis)
        driver_list[number].d_reward += order.o_reward
        driver_list[number].d_vain_dis += min_dis
        order_list[i].o_status = 1
        order_list[i].o_wait = (driver_list[number].d_ttime - order.o_stime) + dis_to_time(
            min_dis)  # 该订单的乘客等待时间 = 等待接单的时间 + 司机赶来的时间

    return driver_list, order_list


def myopic_greedy_driver():
    driver_list = get_driver_list(driver_pos_dir)
    order_list = get_order_list(order_list_dir)

    # for i, driver in enumerate(driver_list):

    pass

def order_scheduling():

    driver_list, order_list = myopic_greedy_order()


    num = 0
    for order in order_list:
        if order.o_status == 1:
            num += 1

    reward = 0.0
    vain_dis = 0.0
    for driver in driver_list:
        reward += driver.d_reward
        vain_dis += driver.d_vain_dis

    print(f'订单分配量：{num}')
    print(f'订单收益：{reward}')
    print(f'司机空载距离：{vain_dis}')

    pass

if __name__=="__main__":

    order_scheduling()

    pass