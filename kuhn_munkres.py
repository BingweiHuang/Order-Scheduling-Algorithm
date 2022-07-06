import queue
import numpy as np
import datetime
from datetime import datetime as dt

from scipy.optimize import linear_sum_assignment

from common import get_euclidean_distance, dispatch


def fun(driver_work, order_work, now, rate):
    mat = np.zeros([len(order_work), len(driver_work)], dtype=float)  # 订单分派给司机的分派矩阵
    for i, order in enumerate(order_work):
        for j, driver in enumerate(driver_work):
            # 权值取订单出发点与司机的距离
            dis = get_euclidean_distance(order.o_start_x, order.o_start_y, driver.d_pos_x, driver.d_pos_y)
            mat[i][j] = dis

    row_ind, col_ind = linear_sum_assignment(mat)
    # print('row_ind:', row_ind)  # 开销矩阵对应的行索引
    # print('col_ind:', col_ind)  # 对应行索引的最优指派的列索引
    # print('cost:', mat[row_ind, col_ind])  # 提取每个行索引的最优指派列索引所在的元素，形成数组
    # print('cost_sum:', mat[row_ind, col_ind].sum())  # 最小开销

    k = min(len(order_work), len(driver_work))
    for i in range(k):  # 分派处理
        order = order_work[row_ind[i]]  # 订单
        driver = driver_work[col_ind[i]]  # 该订单分派给对应的司机
        # print(f'{order.o_id}号订单分派给{driver.d_id}号车 车和订单距离：{mat[row_ind[i], col_ind[i]]}')
        dispatch(order, driver, now, rate)  # 分派

    s = set(row_ind)
    back_order = []
    for i, order in enumerate(order_work):
        if i in s:
            continue
        back_order.append(order)

    return back_order


# 基于距离的匈牙利算法
def kuhn_munkres(driver_list, order_list, rate):

    driver_pq = queue.PriorityQueue() # 司机的优先队列 上一单结束时间越早 优先级越高
    order_pq = queue.PriorityQueue() # 订单的优先队列 订单取消时刻越早 优先级越高

    for driver in driver_list: # 初始化司机的优先队列
        driver_pq.put(driver)

    timestamp = set()
    for order in order_list:
        timestamp.add(order.o_stime)
        timestamp.add(order.o_ttime)

    timestamp_pq = queue.PriorityQueue()

    for ts in timestamp:
        timestamp_pq.put(ts)

    idx = 0 # 按下单时刻顺序访问订单列表 模拟订单按时下达
    last_time = order_list[-1].o_ttime # 最后一单的取消时刻
    while not timestamp_pq.empty(): # 时间戳遍历
        now = timestamp_pq.get() # 更新当前时间
        if now > last_time:
            break
        if idx < len(order_list):
            while order_list[idx].o_stime <= now: # 下单
                order_pq.put(order_list[idx])
                idx += 1
                if idx >= len(order_list):
                    break

        driver_work = []  # 可接单的司机列表
        while not driver_pq.empty(): # 遍历司机
            driver = driver_pq.get()
            if driver.d_ttime > now: # 没有待接单的司机
                driver_pq.put(driver)
                break
            driver_work.append(driver) # 司机可接单 加入driver_work

        n = len(driver_work) # 当前可接单的司机数量

        order_work = [] # 待调度的订单
        while not order_pq.empty(): # 遍历订单
            order = order_pq.get()
            if order.o_ttime < now: # 订单超过乘客可忍耐等待时间范围 取消了
                pass
            else:
                # if len(order_work) == n: # 这一批次的订单数量已经和可接单司机数量相等了 该待调度订单等下一批
                #     order_pq.put(order)
                #     break
                # else:
                #     order_work.append(order)
                order_work.append(order)

        m = len(order_work)
        # print(f'当前时间{now} 当前可接单的司机数量{n} 正在跑单的司机数量{driver_pq.qsize()} 当前待调度的订单{m}')
        back_order = []
        if m > 0:
            back_order = fun(driver_work, order_work, now, rate)

        for order in back_order:
            order_pq.put(order)

        timestamp = set()
        for driver in driver_work: # 司机不是一次性的 用完还可以再用 得重新回到优先队列
            driver_pq.put(driver)
            if driver.d_ttime > now: # 司机的跑单结束的时刻可以引发订单调度
                timestamp.add(driver.d_ttime) # 如果还有订单的话 把每个司机跑单结束的时刻加入时间戳队列

        for ts in timestamp:
            timestamp_pq.put(ts)
    return driver_list, order_list


if __name__=="__main__":

    pass