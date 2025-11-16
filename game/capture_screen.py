import os
import pyautogui
import numpy as np
import cv2


# 截取屏幕
def capture_screen() -> cv2.typing.MatLike:
    screenshot = pyautogui.screenshot()
    # 转换为 OpenCV 格式
    frame = np.array(screenshot)  # PIL: RGB
    # 统一使用 OpenCV 的 BGR 色彩空间
    return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)


def to_gray(frame: cv2.typing.MatLike) -> cv2.typing.MatLike:
    # 输入已统一为 BGR
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


# 截取范围
def capture_screen_range(
    frame: cv2.typing.MatLike, x1: int, x2: int, y1: int, y2: int
) -> cv2.typing.MatLike:
    size = pyautogui.size()
    # 考虑 retina 高分辨率
    scale = frame.shape[1] / size.width
    x1 = int(x1 * scale)
    x2 = int(x2 * scale)
    y1 = int(y1 * scale)
    y2 = int(y2 * scale)
    return frame[y1:y2, x1:x2]


if __name__ == "__main__":
    name = "screenshot.png"
    os.remove(name)
    frame = to_gray(capture_screen())
    frame = capture_screen_range(frame, 0, 100, 0, 100)
    # 保存图片
    cv2.imwrite(name, frame)
