import datetime
from datetime import datetime as dt

# 将表示位置坐标的字符串转换成浮点数x y坐标
def get_xy(str):
    pos = str.strip('[ ]')  # 去除首尾的'[' 和 ']' 和 ' '
    pos = ' '.join(pos.split())  # 字符间只保留一个空格
    x, y = pos.split(' ', 2)  # 分割x y坐标
    return float(x), float(y)

class Order:
    def __init__(self, line):
        self.o_id = int(line[0]) # 订单id
        self.o_stime = dt.strptime(line[1], '%Y/%m/%d %H:%M') # 下单时刻
        self.o_wtime = datetime.timedelta(minutes=int(line[6]))  # 乘客最长等待接单时间(分钟)
        self.o_ttime = self.o_stime + self.o_wtime  # 订单结束时刻
        x, y = get_xy(line[2])
        self.o_start_x = x # 乘客位置x坐标
        self.o_start_y = y # 乘客位置y坐标
        x, y = get_xy(line[3])
        self.o_dest_x = x # 目的地x坐标
        self.o_dest_y = y # 目的地y坐标
        self.o_dis = float(line[4]) # 乘客位置到目的地的欧氏距离
        self.o_reward = float(line[5]) # 订单收益
        self.o_status = 0 # 订单是否完成
        self.o_driver_id = -1 # 哪个司机id接的单
        self.o_dispatch_time = datetime.timedelta(0) # 接单时刻
        self.o_wait = datetime.timedelta(0) # 实际等了多久

    def __lt__(self, other):
        if self.o_ttime == other.o_ttime:
            # return self.o_rate > other.o_rate
            return self.o_dis < other.o_dis
        return self.o_ttime < other.o_ttime
