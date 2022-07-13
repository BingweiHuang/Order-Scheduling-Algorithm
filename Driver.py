import datetime
from datetime import datetime as dt

class Driver:
    def __init__(self, line):
        self.d_id = int(line[0]) # 司机id
        self.d_pos_x = float(line[1]) # 司机位置x坐标
        self.d_pos_y = float(line[2]) # 司机位置y坐标
        self.d_ttime = dt.strptime("2022/06/29 18:00", '%Y/%m/%d %H:%M') # 完成上一个订单的时刻
        self.d_reward = 0.0 # 司机获得的收益
        self.d_vain_dis = 0.0 # 司机的空载距离
        self.d_orders_num = 0.0 # 司机跑单数量

    def __lt__(self, other):
        return self.d_ttime < other.d_ttime