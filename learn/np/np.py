import numpy as np

# 将列表转换为 np 数组
x = np.array([1.0, 2.0, 3.0])
print(x)
# 打印类型
print(type(x))

# numpy 的算术运算
# 当 x 和 y 的元素个数相同时，可以对各个元素进行运算
x = np.array([1.0, 2.0, 3.0])
y = np.array([2.0, 4.0, 6.0])
# 一维数组，对应元素相加
print(f"预期 [3., 6., 9.] 实际 {x + y}")
print(f"预期 [-1., -2., -3.] 实际 {x - y}")
print(f"预期 [2., 8., 18.] 实际 {x * y}")
print(f"预期 [0.5, 0.5, 0.5] 实际 {x / y}")

# numpy 数组和标量运算
x = np.array([1.0, 2.0, 3.0])
print(f"预期 [2., 3., 4.] 实际 {x + 1.0}")

# numpy 的 n 维数组
# 标量(scalar)，一个数，比如 5
# 向量(vector)，一维数组
# 矩阵(matrix)，二维数组
# 张量(tensor)，N 维数组(N>=0)，向量或矩阵，多维数组等统称为张量(tensor)

a = np.array([[1, 2], [3, 4]])
print(a)
# 打印形状
print(f"形状: {a.shape}")
print(f"类型: {a.dtype}")
print(f"大小: {a.size}")
print(f"维度: {a.ndim}")
# 矩阵的运算
b = np.array([[3, 0], [0, 6]])
print(f"预期 [[4, 2], [3, 10]] 实际 {a + b}")
print(f"预期 [[-2, 2], [3, -2]] 实际 {a - b}")
print(f"预期 [[3, 0], [0, 24]] 实际 {a * b}")

# 广播
# 标量，每个元素与标量操作
a = np.array([[1, 2, 3], [4, 5, 6]])
print(f"预期 [[10, 20, 30], [40, 50, 60]] 实际 {a * 10}")
# 向量，每行与向量操作
b = np.array([1, 2, 3])
print(a * b)

# 访问元素
X = np.array([[51, 55], [14, 19], [0, 4]], dtype=np.int32)
print(X)
print(f"预期 [51, 55] 实际 {X[0]}")
print(f"预期 55 实际 {X[0][1]}")
for row in X:
    print(f"{row}")

# 将 x 转换维 1 维数组
x = X.flatten()
print(x)

# 获取索引维 0,2,4 的元素
print(x[np.array([0, 2, 4])])
## 对 NumPy 数组使用不等号运算符，结果会得到一个布尔型的数组。
print(x > 15)
## 从 x 中抽取大于 15 的元素
print(x[x > 15])
