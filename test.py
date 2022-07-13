from matplotlib.colors import LogNorm
from matplotlib import pyplot as plt
import matplotlib
import matplotlib.dates as mdates

from csv_operation import get_order_list, get_driver_list


driver_pos_dir = r"./datasets/driver_pos.csv"
order_list_dir = r"./datasets/order_list.csv"


order_list = get_order_list(order_list_dir)
driver_list = get_driver_list(driver_pos_dir)

order_list_start_x = [order.o_start_x for order in order_list]
order_list_start_y = [order.o_start_y for order in order_list]
order_list_reward = [order.o_reward for order in order_list]
order_list_time = [order.o_stime for order in order_list]
driver_list_start_x = [driver.d_pos_x for driver in driver_list]
driver_list_start_y = [driver.d_pos_y for driver in driver_list]



plt.rc('font', family='SimHei', size='16')
plt.figure(figsize=(12, 10))

ax = plt.subplot(2, 2, 1)
#指定X轴的以日期格式（带小时）显示
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
#X轴的间隔为小时
ax.xaxis.set_major_locator(mdates.HourLocator())
plt.hist(order_list_time, bins=50)
plt.gcf().autofmt_xdate()
plt.title('订单数量的时间维度分布')
plt.xlabel('时间段')
plt.ylabel('订单数')


plt.subplot(2, 2, 2)
plt.hist2d(order_list_start_x, order_list_start_y, bins=30, norm=LogNorm())
plt.colorbar()
plt.title('订单数量的空间维度分布')
plt.xlabel('x坐标')
plt.ylabel('y坐标')


plt.subplot(2, 2, 3)
plt.hist2d(order_list_start_x, order_list_start_y, bins=30, weights=order_list_reward, norm=LogNorm())
plt.colorbar()
plt.title('订单总收益的空间维度分布')
plt.xlabel('x坐标')
plt.ylabel('y坐标')



plt.subplot(2, 2, 4)
plt.hist2d(driver_list_start_x, driver_list_start_y, bins=10, norm=LogNorm())
plt.colorbar()
plt.title('司机数量的空间维度分布')
plt.xlabel('x坐标')
plt.ylabel('y坐标')

plt.tight_layout()
plt.savefig("space-time_dimension_distribution.jpg", dpi=300)
plt.show()

if __name__ == "__main__":
    import numpy as np
    from scipy.optimize import linear_sum_assignment

    # 代价矩阵
    cost = np.array([[4, 1, 3], [2, 0, 5], [3, 6, 5], [3, 5, 3]])
    # print(cost)
    r, c = linear_sum_assignment(cost)  # 得到最佳分配下的行列索引值
    # print(cost[r, c])

    print(r)
    print(c)
    print("最小成本：", cost[r, c].sum())
