import datetime
from datetime import datetime as dt
import time
from solve import solve
from csv_operation import get_driver_list, get_order_list, save_scheduling_results

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

    print()
    print(f'订单分配量：              {num}')
    print(f'订单总收益：              {reward}')
    print(f'司机空载距离：            {vain_dis}')
    print(f'乘客等待时间(等接单+等接驾)：{times}')

    return num, reward, vain_dis


def order_scheduling():
    driver_list, order_list = get_datasets(driver_pos_dir, order_list_dir) # 获取司机和订单的数据

    algorithm_type = "base_distance"    # 基于 司机接驾距离
    # algorithm_type = "base_distance2"   # 基于 司机接驾距离+订单出发地到目的地的距离
    # algorithm_type = "base_rate"        # 基于 收益/司机接驾距离
    # algorithm_type = "myopic_greedy"    # 基于 收益

    time_slot = 0   # 0 - 理想状态：一有订单来或者司机跑单结束就立即发起一轮调度
                    # t - 实际情况：按照一定的时间间隔t(>0)秒发起每轮调度

    st = time.time()
    driver_list, order_list = solve(driver_list, order_list, rate, algorithm_type, time_slot)
    ed = time.time()
    print(f'{algorithm_type} 耗时 {"%.4f" % (ed - st)} 秒')

    evaluation(driver_list, order_list) # 评估调度算法的效果

    save_scheduling_results(driver_list, order_list, algorithm_type) # 保存调度结果

    pass

if __name__=="__main__":

    order_scheduling()

    pass