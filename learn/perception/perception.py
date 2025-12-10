import numpy as np


def AND(x1: int, x2: int) -> int:
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    b = -0.7
    if np.sum(x * w) + b > 0:
        return 1
    return 0


def OR(x1: int, x2: int) -> int:
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    b = -0.2
    if np.sum(x * w) + b > 0:
        return 1
    return 0


def NAND(x1: int, x2: int) -> int:
    x = np.array([x1, x2])
    w = np.array([-0.5, -0.5])
    b = 0.7
    if np.sum(x * w) + b > 0:
        return 1
    return 0


def XOR(x1: int, x2: int) -> int:
    s1 = NAND(x1, x2)
    s2 = OR(x1, x2)
    return AND(s1, s2)


print(AND(0, 0), False and False)
print(AND(0, 1), False and True)
print(AND(1, 0), True and False)
print(AND(1, 1), True and True)

print(OR(0, 0), False or False)
print(OR(0, 1), False or True)
print(OR(1, 0), True or False)
print(OR(1, 1), True or True)

print(NAND(0, 0), False and False)
print(NAND(0, 1), False and True)
print(NAND(1, 0), True and False)
print(NAND(1, 1), True and True)

print(XOR(0, 0), False ^ False)
print(XOR(0, 1), False ^ True)
print(XOR(1, 0), True ^ False)
print(XOR(1, 1), True ^ True)
