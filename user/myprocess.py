import subprocess
import os
import sys
import time
import psutil

class process():
    @staticmethod
    def get_script_path(script_name):
        """获取父目录中的脚本路径"""
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        script_path = os.path.join(parent_dir, script_name)
        
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"无法找到 {script_name} 文件，查找路径: {script_path}")
        
        return script_path

    @staticmethod
    def start():
        """启动服务进程和客户端进程（完全无控制台）"""
        try:
            # 使用pythonw.exe而不是python.exe来避免控制台窗口
            #python = sys.executable.lower().replace("python.exe", "pythonw.exe")
            python = sys.executable.lower()

            try:
                server_script = process.get_script_path('core_server.py')
                client_script = process.get_script_path('core_client.py')
            except FileNotFoundError as e:
                print(f"找不到执行的文件: {e}")
                return None

            print(f"服务器脚本路径: {server_script}")
            print(f"客户端脚本路径: {client_script}")

            processes = []
            
            
            # Windows 平台
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                #startupinfo.wShowWindow = subprocess.SW_HIDE
                
                
                # 启动服务器进程
                if 'core_server.py':
                    server_process = subprocess.Popen(
                        [python, server_script],
                        #creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                        startupinfo=startupinfo,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        stdin=subprocess.DEVNULL,
                        #shell=False
                    )
                    processes.append(server_process)
                    print(f"服务器启动成功，PID: {server_process.pid}")
                else:
                    print("服务器已在运行中")
                
                # 启动客户端进程
                if 'core_client.py':
                    client_process = subprocess.Popen(
                        [python, client_script],
                        #creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                        startupinfo=startupinfo,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        stdin=subprocess.DEVNULL,
                        #shell=False
                    )
                    processes.append(client_process)
                    print(f"客户端启动成功，PID: {client_process.pid}")
                else:
                    print("客户端已在运行中")
            
            
            # 等待进程启动
            time.sleep(1)
            for p in processes[:]:
                if p.poll() is not None:
                    print(f"进程启动失败，PID: {p.pid}")
                    processes.remove(p)
                    
            return processes if processes else None

        except Exception as e:
            print(f"启动服务时出错: {e}")
            return None

    @staticmethod
    def stop(processes):
        """停止服务进程和客户端进程，包括子进程和异步任务"""
        if not processes:
            return

        for p in processes:
            try:
                if p.poll() is None:  # 进程仍在运行
                    # 获取进程树
                    parent = psutil.Process(p.pid)
                    children = parent.children(recursive=True)  # 获取所有子进程

                    # 先终止子进程
                    for child in children:
                        try:
                            if child.is_running():
                                child.terminate()  # 先尝试优雅终止
                        except psutil.NoSuchProcess:
                            pass

                    # 给主进程发送终止信号
                    try:
                        p.terminate()  # 先尝试优雅终止
                        
                        # 等待进程结束
                        for _ in range(10):
                            if p.poll() is not None:
                                break
                            time.sleep(0.1)
                            
                        # 如果进程仍未终止，强制终止
                        if p.poll() is None:
                            # Windows平台特殊处理
                            if os.name == 'nt':
                                import ctypes
                                PROCESS_TERMINATE = 1
                                handle = ctypes.windll.kernel32.OpenProcess(
                                    PROCESS_TERMINATE, False, p.pid)
                                ctypes.windll.kernel32.TerminateProcess(handle, -1)
                                ctypes.windll.kernel32.CloseHandle(handle)
                            else:
                                p.kill()  # Unix-like系统使用kill
                                
                        print(f"进程已停止，PID: {p.pid}")
                        
                    except Exception as e:
                        print(f"终止进程 {p.pid} 时出错: {e}")

            except Exception as e:
                print(f"处理进程 {p.pid if hasattr(p, 'pid') else 'unknown'} 时出错: {e}")
                
        # 确保所有进程都已终止
        for p in processes:
            try:
                if p.poll() is None:
                    p.kill()
            except:
                pass

if __name__ == "__main__":
    p = process.start()
    time.sleep(15)
    process.stop(p)