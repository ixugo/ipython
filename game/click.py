import pyautogui
import time


if __name__ == "__main__":
    # 在部分游戏比如小程序中，click 点击是无效的
    # pyautogui.click(366, 970)
    # 模拟鼠标点击
    pyautogui.mouseDown(366, 970)
    time.sleep(0.1)
    pyautogui.mouseUp(366, 970)
