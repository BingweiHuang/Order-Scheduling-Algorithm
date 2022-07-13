import csv
import datetime
import os
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

def save_scheduling_results(driver_list, order_list, algorithm_type):

    num = 0
    reward = 0.0
    vain_dis = 0.0
    times = datetime.timedelta(seconds=0)
    write_driver_list = []
    write_order_list = []
    for driver in driver_list:
        reward += driver.d_reward
        vain_dis += driver.d_vain_dis
        write_driver_list.append([driver.d_id, driver.d_reward, driver.d_orders_num, driver.d_vain_dis, driver.d_ttime])
        pass

    for order in order_list:
        if order.o_status == 1:
            num += 1
        times += order.o_wait
        write_order_list.append([order.o_id, order.o_status, order.o_driver_id, order.o_stime, f'[{order.o_start_x} {order.o_start_y}]', \
                                 f'[{order.o_dest_x} {order.o_dest_y}]', order.o_dis, order.o_reward, order.o_wtime, order.o_dispatch_time, order.o_wait])
        pass


    dir = rf'./results/{algorithm_type}'
    if not os.path.exists(dir): # 目录是否存在
        os.makedirs(dir)

    with open(rf"{dir}/driver_results.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["司机id", "总收益", "总跑单量", "总空载距离", "完成最后一单的时刻"])  # 先写入columns_name
        writer.writerows(write_driver_list)  # 写入多行用writerows

    with open(rf"{dir}/order_results.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["订单id", "是否被司机接单", "接单司机id", "下单时间", "乘客位置", "目的地位置", "订单距离", "订单收益", "乘客最长等待接单时间", "接单时刻",
                         "乘客实际等待时间"])  # 先写入columns_name
        writer.writerows(write_order_list)  # 写入多行用writerows

    with open(rf"{dir}/scheduling_result.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["订单分配量", "司机总收益", "司机空载距离", "乘客等待时间(等接单+等接驾)"])  # 先写入columns_name
        writer.writerow([num, reward, vain_dis, times])

    pass