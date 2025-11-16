import platform
import pyautogui
import subprocess
import time


# 检查 macos 是否获取了辅助功能权限
def check_accessibility_permission():
    """检查 macOS 辅助功能权限"""
    if platform.system() != "Darwin":  # 非 macOS 系统
        return True
    try:
        # 尝试获取辅助功能权限（通过尝试移动鼠标来测试）
        # 如果失败会抛出异常
        try:
            # 尝试获取鼠标位置（需要辅助功能权限）
            current_pos = pyautogui.position()
            print("✓ 辅助功能权限已授予")
            return True
        except Exception:
            pass

        # 使用 AppleScript 检查权限
        script = """
        tell application "System Events"
            try
                set UI elements enabled to true
                return "granted"
            on error
                return "denied"
            end try
        end tell
        """
        result = subprocess.run(
            ["osascript", "-e", script], capture_output=True, text=True, timeout=5
        )
        if "granted" in result.stdout.lower() or result.returncode == 0:
            print("✓ 辅助功能权限已授予")
            return True
        else:
            print("\n" + "=" * 60)
            print("⚠️  需要授予辅助功能权限才能执行点击操作！")
            print("=" * 60)
            print("\n正在打开系统设置页面...")
            # 打开系统设置的辅助功能页面
            open_settings_script = """
            tell application "System Settings"
                activate
            end tell
            delay 1
            tell application "System Events"
                tell process "System Settings"
                    click menu item "隐私与安全性" of menu "系统设置" of menu bar 1
                    delay 1
                    click button "辅助功能" of scroll area 1 of group 1 of split group 1 of group 2 of split group 1 of window "隐私与安全性"
                end tell
            end tell
            """
            # 或者直接使用 URL scheme
            try:
                subprocess.run(
                    [
                        "open",
                        "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility",
                    ],
                    timeout=5,
                )
                print("✓ 已打开系统设置页面")
                print("\n请按照以下步骤操作：")
                print("1. 在系统设置中找到 '辅助功能'")
                print("2. 找到 Terminal 或 Python（取决于您使用的终端）")
                print("3. 勾选复选框以授予权限")
                print("4. 如果找不到，点击 '+' 按钮添加应用程序")
                print("\n授权完成后，脚本将自动继续...")
                print("=" * 60 + "\n")
                # 等待用户授权（最多等待60秒）
                for i in range(60):
                    time.sleep(1)
                    try:
                        current_pos = pyautogui.position()
                        print("✓ 权限已授予！继续运行...")
                        return True
                    except:
                        if i % 10 == 0:
                            print(f"等待授权中... ({i}/60秒)")
                print("⚠️  等待超时，请手动授权后重新运行脚本")
                return False
            except Exception as e:
                print(f"无法自动打开设置页面: {e}")
                print("\n请手动打开：系统设置 → 隐私与安全性 → 辅助功能")
                print("然后添加 Terminal 或 Python 并授予权限")
                return False
    except Exception as e:
        print(f"检查权限时出错: {e}")
        print("请确保已授予辅助功能权限")
        return False


if __name__ == "__main__":
    check_accessibility_permission()
