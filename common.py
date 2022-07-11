import math
import datetime
from datetime import datetime as dt


def get_euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def dis_to_time(dis, rate):
    s = int(math.ceil(dis / rate * 60))
    return datetime.timedelta(seconds=s)

def dispatch(order, driver, time, rate):
    order.o_status = 1  # 该订单被成功分派
    dis = get_euclidean_distance(order.o_start_x, order.o_start_y, driver.d_pos_x, driver.d_pos_y)  # 空载距离
    driver.d_pos_x = order.o_dest_x
    driver.d_pos_y = order.o_dest_y
    driver.d_ttime = time + dis_to_time(dis + order.o_dis, rate)  # 这单结束时刻 = 接单时刻 + 乘客等司机的时间（司机空载时间） + 跑单时间
    driver.d_reward += order.o_reward  # 更新司机收益
    driver.d_vain_dis += dis  # 更新司机空载距离
    order.o_wait = (time - order.o_stime) + dis_to_time(dis, rate)  # 该订单的乘客等待时间 = 等待接单的时间（接单时刻 - 下单时刻） + 乘客等司机的时间（司机空载时间）
    pass
