import platform
import pyautogui

# 获取屏幕尺寸，判断系统类型


def IsWindows() -> bool:
    return platform.system() == "Windows"


def IsLinux() -> bool:
    return platform.system() == "Linux"


def IsMac() -> bool:
    return platform.system() == "Darwin"


def GetScreenSize():
    return pyautogui.size()


if __name__ == "__main__":
    print("isWindows: ", IsWindows())
    print("isLinux: ", IsLinux())
    print("isMac: ", IsMac())
    print("system: ", platform.system())
    print("screen size: ", GetScreenSize())
