import queue

import numpy as np

from common import get_euclidean_distance, dispatch
from kuhn_munkres import kuhn_munkres



def match(driver_work, order_work, now, rate, algorithm_type):
    # print(len(order_work), len(driver_work))
    mat = np.zeros([len(order_work), len(driver_work)], dtype=float)  # 订单分派给司机的分派矩阵
    maximize = False # 求权值最大还是最小
    if algorithm_type == "base_distance":
        for i, order in enumerate(order_work):
            for j, driver in enumerate(driver_work):
                # 权值取订单出发点与司机的距离
                mat[i][j] = get_euclidean_distance(order.o_start_x, order.o_start_y, driver.d_pos_x, driver.d_pos_y)

    elif algorithm_type == "myopic_greedy":
        maximize = True
        for i, order in enumerate(order_work):
            for j, driver in enumerate(driver_work):
                # 权值取订单收益
                mat[i][j] = order.o_reward

    # row_ind, col_ind = kuhn_munkres(mat, maximize)
    # print(np.size(mat, 0), np.size(mat, 1))
    # print()
    # print()

    matches = kuhn_munkres(mat, maximize)


    n = len(order_work)
    m = len(driver_work)


    # print(len(matches))
    back_order = []  # 这次分配没轮到的订单
    if n <= m:
        for i in range(n): # 分派处理
            order = order_work[i] # 订单
            driver = driver_work[matches[i]] # 该订单分派给对应的司机
            # print(f'{order.o_id}号订单分派给{driver.d_id}号车 车和订单距离：{mat[i, matches[i]]}')
            dispatch(order, driver, now, rate)  # 分派
            pass
    else:
        for i in range(m):  # 分派处理
            order = order_work[matches[i]]  # 订单
            driver = driver_work[i]  # 该订单分派给对应的司机
            # print(f'{order.o_id}号订单分派给{driver.d_id}号车 车和订单距离：{mat[matches[i], i]}')
            dispatch(order, driver, now, rate)  # 分派

        s = set(matches)
        for i, order in enumerate(order_work):
            if i in s:
                continue
            back_order.append(order) # 本轮没派完的订单

    # for i in range(k):  # 分派处理
    #     order = order_work[row_ind[i]]  # 订单
    #     driver = driver_work[col_ind[i]]  # 该订单分派给对应的司机
    #     # print(f'{order.o_id}号订单分派给{driver.d_id}号车 车和订单距离：{mat[row_ind[i], col_ind[i]]}')
    #     dispatch(order, driver, now, rate)  # 分派
    #
    # s = set(row_ind)
    #
    # for i, order in enumerate(order_work):
    #     if i in s:
    #         continue
    #     back_order.append(order)

    return back_order

def solve(driver_list, order_list, rate, algorithm_type):

    driver_pq = queue.PriorityQueue() # 司机的优先队列 上一单结束时间越早 优先级越高
    order_pq = queue.PriorityQueue() # 订单的优先队列 订单取消时刻越早 优先级越高

    for driver in driver_list: # 初始化司机的优先队列
        driver_pq.put(driver)

    timestamp = set()
    for order in order_list:
        timestamp.add(order.o_stime)
        timestamp.add(order.o_ttime)


    # time = order_list[0].o_stime # 第一单的下单时刻
    # last_time = order_list[-1].o_ttime  # 最后一单的取消时刻
    # timestamp.clear()
    # while time <= last_time:
    #     timestamp.add(time)
    #     time += datetime.timedelta(minutes=1)
    # timestamp.add(time)


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
                order_work.append(order)

        m = len(order_work)
        # print(f'当前时间{now} 当前可接单的司机数量{n} 正在跑单的司机数量{driver_pq.qsize()} 当前待调度的订单{m}')


        # if m > 0:
        #     if algorithm_type == "base_distance":
        #         back_order = base_distance(driver_work, order_work, now, rate)
        #     elif algorithm_type == "myopic_greedy":
        #         back_order = myopic_greedy(driver_work, order_work, now, rate)
        if m > 0: # 这一轮有待分配的订单
            back_order = match(driver_work, order_work, now, rate, algorithm_type)
            for order in back_order:  # 这轮分配没轮到的订单进入下一轮
                order_pq.put(order)


        for driver in driver_work: # 司机不是一次性的 用完还可以再用 得重新回到优先队列
            driver_pq.put(driver)


    return driver_list, order_list