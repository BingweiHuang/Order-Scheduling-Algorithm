import datetime
from datetime import datetime as dt
import time
from solve import solve
from csv_operation import get_driver_list, get_order_list


driver_pos_dir = r"./datasets/driver_pos.csv"
order_list_dir = r"./datasets/order_list.csv"

rate = 0.35 # 司机开车的平均速率

# 获取司机和订单的数据
def get_datasets(driver_pos_dir, order_list_dir):
    driver_list = get_driver_list(driver_pos_dir)
    order_list = get_order_list(order_list_dir)

    return driver_list, order_list

# 评估调度算法
def evaluation(driver_list, order_list):
    num = 0
    reward = 0.0
    vain_dis = 0.0
    times = datetime.timedelta(seconds=0)
    for order in order_list:
        if order.o_status == 1:
            num += 1
            times += order.o_wait

    for driver in driver_list:
        reward += driver.d_reward
        vain_dis += driver.d_vain_dis

    print(f'订单分配量：{num}')
    print(f'订单总收益：{reward}')
    print(f'司机空载距离：{vain_dis}')
    print(f'乘客等待时间（等接单 + 接单后等司机赶来）：{times}')
    pass

def order_scheduling():
    driver_list, order_list = get_datasets(driver_pos_dir, order_list_dir) # 获取司机和订单的数据

    st = time.time()

    driver_list, order_list = solve(driver_list, order_list, rate, "base_distance") # 基于距离的匈牙利算法
    # driver_list, order_list = solve(driver_list, order_list, rate, "myopic_greedy") #

    ed = time.time()
    print(f'time consuming is {"%.4f" % (ed - st)} seconds')

    evaluation(driver_list, order_list) # 评估调度算法

    pass

if __name__=="__main__":

    order_scheduling()

    pass