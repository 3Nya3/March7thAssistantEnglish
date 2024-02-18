
def subprocess_with_timeout(command, timeout, working_directory=None, env=None):
    import subprocess
    process = None
    try:
        process = subprocess.Popen(command, cwd=working_directory, env=env)
        process.communicate(timeout=timeout)
        if process.returncode == 0:
            return True
    except subprocess.TimeoutExpired:
        if process is not None:
            process.terminate()
            process.wait()
    return False


def subprocess_with_stdout(command):
    import subprocess
    try:
        # 使用subprocess运行命令并捕获标准输出
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # 检查命令是否成功执行
        if result.returncode == 0:
            # 返回标准输出的内容
            return result.stdout.strip()
        return None
    except Exception:
        return None


def start_task(command):
    # 为什么 Windows 这么难用呢
    import subprocess
    import sys
    import os
    # 检查是否是 PyInstaller 打包的可执行文件
    if getattr(sys, 'frozen', False):
        if subprocess_with_stdout(["where", "wt.exe"]) is not None:
            # 因为 https://github.com/microsoft/terminal/issues/10276 问题
            # 管理员模式下，始终优先使用控制台主机而不是新终端
            subprocess.Popen(["wt", os.path.abspath("./March7th Assistant.exe"), command], creationflags=subprocess.DETACHED_PROCESS)
        else:
            subprocess.Popen([os.path.abspath("./March7th Assistant.exe"), command], creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        if subprocess_with_stdout(["where", "wt.exe"]) is not None:
            subprocess.Popen(["wt", sys.executable, "main.py", command], creationflags=subprocess.DETACHED_PROCESS)
        else:
            subprocess.Popen([sys.executable, "main.py", command], creationflags=subprocess.CREATE_NEW_CONSOLE)
