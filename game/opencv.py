import cv2
import os
import sys
import pyautogui

try:
    from . import capture_screen, screen
except ImportError:
    # 支持直接脚本运行：python game/opencv.py 或在 game 目录下 python opencv.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    from game import capture_screen, screen


# 比较图片相似度
def find_image(
    img1: cv2.typing.MatLike, img2: cv2.typing.MatLike, threshold: float = 0.8
):
    # 对图片进行预处理，提高匹配率
    # 转换为灰度图
    screen_gray = (
        cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY) if len(img1.shape) == 3 else img1
    )
    target_gray = (
        cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) if len(img2.shape) == 3 else img2
    )
    # 比较宽高，如果模板比屏幕大，直接返回
    if (
        target_gray.shape[0] > screen_gray.shape[0]
        or target_gray.shape[1] > screen_gray.shape[1]
    ):
        return None

    method = cv2.TM_CCOEFF_NORMED

    result = cv2.matchTemplate(screen_gray, target_gray, method)
    # 矩阵中的最小数值，最大数值，最小值所在坐标，最大值所在坐标
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 如果原始尺寸匹配度已经很高，直接返回
    if max_val >= threshold:
        h, w = target_gray.shape[:2]
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        return (center_x, center_y, max_loc, target_gray.shape[:2])

    # 如果匹配度接近阈值，尝试多尺度匹配
    # 可能因为缩放了界面，或不同分辨率的屏幕上运行，导致匹配度不高
    if max_val >= 0.5:
        scales = [0.95, 1.05, 0.9, 1.1]
        for scale in scales:
            h, w = target_gray.shape[:2]
            scaled_h = int(h * scale)
            scaled_w = int(w * scale)
            # 检查尺寸是否有效
            if (
                scaled_h <= 0
                or scaled_w <= 0
                or scaled_h > screen_gray.shape[0]
                or scaled_w > screen_gray.shape[1]
            ):
                continue
            # 缩放模板
            scaled_target = cv2.resize(
                target_gray, (scaled_w, scaled_h), interpolation=cv2.INTER_AREA
            )
            # 执行模板匹配
            result = cv2.matchTemplate(screen_gray, scaled_target, method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val >= threshold:
                # 计算中心点坐标,考虑缩放后的尺寸
                center_x = max_loc[0] + scaled_w // 2
                center_y = max_loc[1] + scaled_h // 2
                return (center_x, center_y, max_loc, target_gray.shape[:2])

    return None


# 画框
def draw_box(img: cv2.typing.MatLike, max_loc: cv2.typing.Point, size: tuple[int, int]):
    x, y = max_loc
    w, h = size
    x2 = x + w
    y2 = y + h
    center = (x + w // 2, y + h // 2)
    cv2.rectangle(img, (x, y), (x2, y2), (0, 255, 0), 2)
    cv2.putText(
        img,
        f"Match: ({center[0]},{center[1]})",
        (x, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 255, 0),
        2,
    )
    return img


# 标记匹配中心点
def mark_center(img: cv2.typing.MatLike, max_loc: cv2.typing.Point):
    x, y = max_loc
    w, h = size
    center = (x + w // 2, y + h // 2)
    cv2.circle(img, center, 5, (0, 255, 0), -1)
    return img


# 绘制点击位置(红色圆圈)
def draw_click_position(img: cv2.typing.MatLike, max_loc: cv2.typing.Point):
    x, y = max_loc
    w, h = size
    center = (x + w // 2, y + h // 2)

    cv2.circle(img, center, 10, (0, 0, 255), 3)
    cv2.putText(
        img,
        f"Click Screenshot: ({center[0]},{center[1]})",
        (center[0] + 15, center[1] - 15),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 0, 255),
        2,
    )
    return img


# 添加屏幕坐标信息
def add_screen_info(img: cv2.typing.MatLike, max_loc: cv2.typing.Point):
    cv2.putText(
        img,
        f"Screen: ({max_loc[0]},{max_loc[1]})",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 0),
        2,
    )


def save_image(
    screen: cv2.typing.MatLike, max_loc: cv2.typing.Point, size: tuple[int, int]
):
    img = screen.copy()

    draw_box(img, max_loc, size)
    mark_center(img, max_loc)
    draw_click_position(img, max_loc)
    add_screen_info(img, max_loc)
    # 保存图片
    cv2.imwrite("screenshot.png", img)


if __name__ == "__main__":
    frame1 = capture_screen.capture_screen()
    cv2.imwrite("screensho1t.png", frame1)
    frame1x = capture_screen.to_gray(frame1.copy())
    frame2 = capture_screen.capture_screen_range(frame1x, 300, 400, 300, 400)
    result = find_image(frame1x, frame2, 0.8)
    if result is not None:
        print("result: ", result)
        x, y, max_loc, size = result
        # 保存图片
        save_image(frame1, max_loc, size)
    else:
        print("未找到")
