import matplotlib.pyplot as plt
import numpy as np

x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])

# 将 x 的每个点画出来
plt.scatter(x[:, 0], x[:, 1], c="red")
# 在 x=0，y=0.5 和 x=0.5，y=0 的位置画一条线
plt.plot([0, 0.5], [0.5, 0], "b-")


plt.show()
# plt.savefig("perception.png")
