"""
绘制 sin 和 cos 函数
"""

from cProfile import label
from matplotlib.lines import lineStyles
import numpy as np
import matplotlib.pyplot as plt

## 使用 NumPy 的 arange方法生成了 [0, 0.1, 0.2, ..., 5.8, 5.9]的数据
x = np.arange(0, 6, 0.1)
print(x)
## 使用 NumPy 的 sin方法生成了 [0, 0.1, 0.2, ..., 5.8, 5.9]的正弦值
y = np.sin(x)
y2 = np.cos(x)

plt.plot(x, y, label="sin")
# 设置虚线
plt.plot(
    x,
    y2,
    linestyle="--",
    label="cos",
)
## 设置 x 轴标签
plt.xlabel("x")
## 设置 y 轴标签
plt.ylabel("y")
## 设置图表标题
plt.title("sin & cos")
## legend 的作用是显示图例
plt.legend()
plt.show()
