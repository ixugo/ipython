import sys
from typing import Optional, Tuple

Rect = Tuple[int, int, int, int]


# 为了统一入口并供后续截图/定位复用，集中获取完整窗口矩形。
def get_window_rect(window_name: str) -> Rect:
    """为了给调用方提供统一入口，同时保证上层能拿到完整坐标用于后续截图或定位。"""
    if not window_name:
        raise ValueError("window_name 不能为空")

    if sys.platform.startswith("win"):
        return _get_window_rect_windows(window_name)

    if sys.platform == "darwin":
        return _get_window_rect_mac(window_name)

    raise NotImplementedError("当前操作系统暂未支持窗口坐标获取")


# 为了避免多处重复计算尺寸，统一先取矩形再派生宽高。
def get_window_size(window_name: str) -> Tuple[int, int]:
    """为了避免重复计算尺寸，复用完整矩形坐标后再派生宽高。"""
    left, top, right, bottom = get_window_rect(window_name)
    return right - left, bottom - top


# 为了隔离 Windows 特有 API，便于后续维护和替换实现。
def _get_window_rect_windows(window_name: str) -> Rect:
    """为了重用 Win32 原生接口并保持返回值一致，单独封装 Windows 的窗口查询逻辑。"""
    try:
        import win32gui  # type: ignore
    except ImportError as exc:
        raise RuntimeError("缺少 pywin32，请先安装: pip install pywin32") from exc

    hwnd = win32gui.FindWindow(None, window_name)
    if not hwnd:
        raise ValueError(f"未找到窗口: {window_name}")

    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    return int(left), int(top), int(right), int(bottom)


# 为了在 macOS 复用 Quartz，无需额外脚本即可拿到窗口矩形。
def _get_window_rect_mac(window_name: str) -> Rect:
    """为了在 macOS 上保持无外部脚本依赖，使用 Quartz 直接读取窗口矩形。"""
    try:
        from Quartz import (  # type: ignore[attr-defined]
            CGWindowListCopyWindowInfo,
            kCGWindowListOptionOnScreenOnly,
            kCGNullWindowID,
        )
    except ImportError as exc:
        raise RuntimeError(
            "缺少 pyobjc-framework-Quartz，请先安装: pip install pyobjc-framework-Quartz"
        ) from exc

    window_list = CGWindowListCopyWindowInfo(
        kCGWindowListOptionOnScreenOnly, kCGNullWindowID
    )

    for win in window_list:
        title = win.get("kCGWindowName") or ""
        if title != window_name:
            continue

        bounds = win.get("kCGWindowBounds") or {}
        left = int(bounds.get("X", 0))
        top = int(bounds.get("Y", 0))
        width = int(bounds.get("Width", 0))
        height = int(bounds.get("Height", 0))
        if width > 0 and height > 0:
            return left, top, left + width, top + height

    raise ValueError(f"未找到窗口: {window_name}")


# 为了截图前确保目标窗口在前台，统一激活指定窗口。
def activate_window(window_name: str) -> None:
    """为了确保后续截图坐标与前台窗口一致，先激活目标窗口。"""
    if not window_name:
        raise ValueError("window_name 不能为空")

    if sys.platform.startswith("win"):
        _activate_window_windows(window_name)
        return

    if sys.platform == "darwin":
        _activate_window_mac(window_name)
        return

    raise NotImplementedError("当前操作系统暂未支持窗口激活")


# 为了在 Windows 通过原生接口把窗口置前，避免被遮挡。
def _activate_window_windows(window_name: str) -> None:
    """为了避免后台窗口遮挡，使用 Win32 将目标窗口置前并恢复。"""
    try:
        import win32con  # type: ignore
        import win32gui  # type: ignore
    except ImportError as exc:
        raise RuntimeError("缺少 pywin32，请先安装: pip install pywin32") from exc

    hwnd = win32gui.FindWindow(None, window_name)
    if not hwnd:
        raise ValueError(f"未找到窗口: {window_name}")

    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)


# 为了在 macOS 通过 PID 激活应用，确保截图捕捉前台窗口。
def _activate_window_mac(window_name: str) -> None:
    """为了与截图配合，先找到窗口并通过 PID 激活对应应用。"""
    try:
        from Quartz import (  # type: ignore
            CGWindowListCopyWindowInfo,
            kCGWindowListOptionOnScreenOnly,
            kCGNullWindowID,
        )
        from AppKit import NSRunningApplication, NSApplicationActivateIgnoringOtherApps  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "缺少 pyobjc-framework-Quartz 或 pyobjc，请先安装: pip install pyobjc-framework-Quartz pyobjc"
        ) from exc

    window_list = CGWindowListCopyWindowInfo(
        kCGWindowListOptionOnScreenOnly, kCGNullWindowID
    )

    target_pid = None
    for win in window_list:
        title = win.get("kCGWindowName") or ""
        if title != window_name:
            continue
        target_pid = win.get("kCGWindowOwnerPID")
        if target_pid:
            break

    if not target_pid:
        raise ValueError(f"未找到窗口: {window_name}")

    app = NSRunningApplication.runningApplicationWithProcessIdentifier_(target_pid)
    if not app:
        raise RuntimeError(f"未找到可激活的进程，PID: {target_pid}")

    app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)


# 为了提供最小依赖的矩形截图能力，可选激活窗口后再截图。
def screenshot_region(
    left: int,
    top: int,
    right: int,
    bottom: int,
    save_path: str,
    window_name: Optional[str] = None,
) -> str:
    """为了保证截图区域与窗口状态一致，可选先激活窗口再按坐标截图。"""
    if left >= right or top >= bottom:
        raise ValueError("截图坐标不合法")

    if window_name:
        activate_window(window_name)

    try:
        from PIL import ImageGrab  # type: ignore
    except ImportError as exc:
        raise RuntimeError("缺少 pillow，请先安装: pip install pillow") from exc

    image = ImageGrab.grab(bbox=(int(left), int(top), int(right), int(bottom)))
    image.save(save_path)
    return save_path


if __name__ == "__main__":
    name = "微信"
    rect = get_window_rect(name)
    print(f"{name} 窗口矩形: {rect}, 尺寸: {get_window_size(name)}")
    screenshot_region(*rect, save_path="screenshot.png", window_name=name)
