import datetime
import queue
import numpy as np
from common import get_euclidean_distance, dispatch
from kuhn_munkres import my_kuhn_munkres

# 每一轮的司机与订单的匹配
def match(driver_work, order_work, now, rate, algorithm_type):
    mat = np.zeros([len(order_work), len(driver_work)], dtype=float)  # 订单分派给司机的分派矩阵
    maximize = False # 求权值最大还是最小

    if algorithm_type == "myopic_greedy":
        maximize = True
        for i, order in enumerate(order_work):
            for j, driver in enumerate(driver_work):
                # 权值取 订单收益
                mat[i][j] = order.o_reward

    elif algorithm_type == "base_rate":
        maximize = True
        for i, order in enumerate(order_work):
            for j, driver in enumerate(driver_work):
                # 权值取 收益/司机接驾距离
                mat[i][j] = order.o_reward / get_euclidean_distance(order.o_start_x, order.o_start_y, driver.d_pos_x, driver.d_pos_y)

    elif algorithm_type == "base_distance2":
        for i, order in enumerate(order_work):
            for j, driver in enumerate(driver_work):
                # 权值取 司机接驾距离+订单出发地到目的地的距离
                mat[i][j] = get_euclidean_distance(order.o_start_x, order.o_start_y, driver.d_pos_x,
                                                   driver.d_pos_y) + order.o_dis

    else: # algorithm_type == "base_distance"
        for i, order in enumerate(order_work):
            for j, driver in enumerate(driver_work):
                # 权值取 司机接驾距离
                mat[i][j] = get_euclidean_distance(order.o_start_x, order.o_start_y, driver.d_pos_x, driver.d_pos_y)

    n = len(order_work)
    m = len(driver_work)

    row_ind, col_ind = my_kuhn_munkres(mat, maximize) # 用自己C++写的kuhn_munkres

    k = min(n, m)
    back_order = []
    for i in range(k):  # 分派处理
        order = order_work[row_ind[i]]  # 订单
        driver = driver_work[col_ind[i]]  # 该订单分派给对应的司机
        # print(f'{order.o_id}号订单分派给{driver.d_id}号车 车和订单距离：{mat[i, matches[i]]}')
        dispatch(order, driver, now, rate)  # 分派

    s = set(row_ind)  # 已经派单的order_work序号
    for i, order in enumerate(order_work):  # 没派完的订单放到下一轮
        if i in s:
            continue
        back_order.append(order)  # 本轮没派完的订单

    return back_order


# 开始系统的整个调度过程
def solve(driver_list, order_list, rate, algorithm_type, time_slot):

    # 第一步 初始化数据
    driver_pq = queue.PriorityQueue() # 司机的优先队列 上一单结束时间越早 优先级越高
    order_pq = queue.PriorityQueue() # 订单的优先队列 订单取消时刻越早 优先级越高
    for driver in driver_list: # 初始化司机的优先队列
        driver_pq.put(driver)

    timestamp = set() # 时间戳
    time = order_list[0].o_stime  # 第一单的下单时刻
    last_time = order_list[-1].o_ttime  # 最后一单的取消时刻

    if time_slot == 0: # 0 - 理想情况 每当有订单发起或者司机跑单结束 就触发调度
        for order in order_list:
            timestamp.add(order.o_stime) # 订单下单时间戳
            # timestamp.add(order.o_ttime) # 订单结束时间戳

    else: # t - 实际情况 每隔t秒调度一次
        while time <= last_time:
            timestamp.add(time)
            time += datetime.timedelta(seconds=time_slot) # 每隔time_slot秒进行一次订单匹配
        timestamp.add(time)

    timestamp_pq = queue.PriorityQueue() # 时间戳
    for ts in timestamp:
        timestamp_pq.put(ts)


    # 第二步 模拟调度
    idx = 0 # 按下单时刻顺序访问订单列表 模拟订单按时下达
    while not timestamp_pq.empty(): # 时间戳遍历
        now = timestamp_pq.get() # 更新当前时间
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
                order_work.append(order) # 订单已经下单且未取消 加入order_work

        m = len(order_work) # 待调度的订单数量
        # print(f'当前时间{now} 当前可接单的司机数量{n} 正在跑单的司机数量{driver_pq.qsize()} 当前待调度的订单{m}')

        if m > 0: # 这一轮有待分配的订单
            back_order = match(driver_work, order_work, now, rate, algorithm_type) # 开启这一轮的分配吧
            for order in back_order:  # 这轮分配没轮到的订单进入下一轮
                order_pq.put(order)

        timestamp = set()
        for driver in driver_work: # 司机不是一次性的 用完还可以再用 得重新回到队列
            driver_pq.put(driver)
            if time_slot == 0 and driver.d_ttime > now and driver.d_ttime < last_time: # 在理想情况下 司机跑单结束的时刻也可以触发订单调度
                timestamp.add(driver.d_ttime)

        for ts in timestamp: # 如果是理想情况下 把这些司机跑单结束的时刻加入时间戳队列
            timestamp_pq.put(ts)

    return driver_list, order_list