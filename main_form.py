# -*- coding: utf-8 -*-

"""
Module implementing mydlg.
"""
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from Ui_main_form import Ui_Dialog 
import config 
from user.reprocess import execute
from user.myprocess import process
from PyQt5.QtNetwork import QUdpSocket, QHostAddress
import sys
from PyQt5.QtWidgets import QApplication
import os
from user.speaker import speak
from user.excelprocess import excel
class CustomProtocol:
    def __init__(self, dialog_instance):
        self.dialog = dialog_instance  # 保存对话框实例的引用
        path = "C:\\Users\\14676\\Desktop\\副本机房设备清单（正式版）.xlsx"
        self.data = excel.read(path)
        print(self.data)
    def custom_handle(self, message:str):
        if message == "success":
            self.dialog.que_label.setText("连接成功")
            self.dialog.ans_label.setText("连接成功")
        else:
            message = message.upper()
            message = message.replace("杠","-")
            self.dialog.que_label.setText(message)
            response = execute(message,self.data)
            self.dialog.ans_label.setText(response)
            speak(response)
            print(response)

class mydlg(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(mydlg, self).__init__(parent)

        config.ConfigManager.load_config()

        self.udp_socket = QUdpSocket()
        if not self.udp_socket.bind(QHostAddress(config.UDP.addr), config.UDP.cliport):
            print(f"绑定失败: {self.udp_socket.errorString()}")
        self.udp_socket.readyRead.connect(self.handle_udp_data)


        # 保存进程列表
        self.start_services()


        self.setupUi(self) 
        self.btn_start.clicked.connect(self.on_btn_start_cliked)
        self.btn_stop.clicked.connect(self.on_btn_stop_cliked)
        self.btn_update.clicked.connect(self.on_btn_update_cliked)
        self.btn_rest.clicked.connect(self.on_btn_rest_cliked)
        self.setWindowTitle('QMessageBox的使用')
        
    def show1(self):
        reply = QMessageBox.information(self,"消息对话框","消息对话框正文",QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
        print(reply)
    
    def start_services(self):
        """启动所有服务"""
        try:
            # 启动服务进程
            self.service_processes = process.start()
            if self.service_processes is None:
                print("服务启动失败或已在运行中")
                self.service_processes = []  # 初始化为空列表而不是None
            else:
                print("服务启动成功")
        except Exception as e:
            print(f"启动服务失败: {e}")
            self.service_processes = []  # 确保总是有可迭代对象

    def stop_services(self):
        """停止所有服务"""
        if not hasattr(self, 'service_processes') or self.service_processes is None:
            print("没有运行中的服务")
            return
        process.stop(self.service_processes)
        


    def handle_udp_data(self):
        while self.udp_socket.hasPendingDatagrams():
            datagram, _, _ = self.udp_socket.readDatagram(self.udp_socket.pendingDatagramSize())
            message = datagram.decode()
            # 将当前对话框实例传递给CustomProtocol
            CustomProtocol(self).custom_handle(message)

    def send(self, message, host, port):
        """封装UDP发送方法"""
        if isinstance(message, str):
            message = message.encode('utf-8')  # 转换为bytes
        self.udp_socket.writeDatagram(
            message,  # 直接使用bytes类型
            QHostAddress(host),
            port
        )

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "capswriter"))
        self.btn_start.setText(_translate("Dialog", "start"))
        self.btn_stop.setText(_translate("Dialog", "stop"))
        self.que_label.setText(_translate("Dialog", "等待连接"))
        self.ans_label.setText(_translate("Dialog", "等待连接"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "主页"))
        self.btn_update.setText(_translate("Dialog", "update"))
        
        # 设置表格垂直标题（行标题）
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "IP地址"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("Dialog", "标点引擎"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("Dialog", "UDP地址"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("Dialog", "快捷键"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("Dialog", "excel路径"))
        
        # 设置表格水平标题（列标题）
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "值"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "默认值"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "可用值"))
        
        # 填充表格数据
        self.fill_table_data()
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "配置"))
        self.btn_rest.setText(_translate("Dialog", "重启"))
        self.label_tip.setText(_translate("Dialog", "更新后重启以生效"))


    def fill_table_data(self):
        """填充表格数据"""
        # 确保表格有足够的行和列
        self.tableWidget.setRowCount(5)
        self.tableWidget.setColumnCount(3)
        
        # 第一行数据 (TCP端口)
        self.tableWidget.setItem(0, 0, QTableWidgetItem("待填入"))  # 当前值
        self.tableWidget.setItem(0, 1, QTableWidgetItem(str(config.ClientConfig.addr)))  # 默认值
        self.tableWidget.setItem(0, 2, QTableWidgetItem("ipconfig查询"))  # 可用值
        
        # 第二行数据 (标点引擎)
        self.tableWidget.setItem(1, 0, QTableWidgetItem("待填入"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem(str(config.ServerConfig.format_punc)))
        self.tableWidget.setItem(1, 2, QTableWidgetItem("True/False"))
        
        # 第三行数据 (UDP地址)
        self.tableWidget.setItem(2, 0, QTableWidgetItem("待填入"))
        self.tableWidget.setItem(2, 1, QTableWidgetItem(config.UDP.addr))
        self.tableWidget.setItem(2, 2, QTableWidgetItem("IP地址或域名"))
        
        # 第四行数据 (快捷键)
        self.tableWidget.setItem(3, 0, QTableWidgetItem("待填入"))
        self.tableWidget.setItem(3, 1, QTableWidgetItem(config.ClientConfig.shortcut))
        self.tableWidget.setItem(3, 2, QTableWidgetItem("任意键盘按键"))

        # 第五行数据 (excel路径)
        self.tableWidget.setItem(4, 0, QTableWidgetItem("待填入"))
        self.tableWidget.setItem(4, 1, QTableWidgetItem(str(config.ClientConfig.excedir)))
        self.tableWidget.setItem(4, 2, QTableWidgetItem("右键复制文件地址"))

        # 设置表格样式和调整列宽
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)


    def closeEvent(self, event):
        """重写关闭事件处理"""
        print("窗口即将关闭，执行清理操作...")
        self.stop_services()
        event.accept()  # 接受关闭事件
        event.accept()  # 接受关闭事件

    @pyqtSlot()
    def on_btn_start_cliked(self):
        if not hasattr(self, 'udp_socket'):
            print("UDP服务器未就绪!")
            return
        # 原有发送逻辑
        self.send("start", config.UDP.addr,config.UDP.serport)
        print("send:start")

    @pyqtSlot()
    def on_btn_stop_cliked(self):
        if not hasattr(self, 'udp_socket'):
            print("UDP服务器未就绪!")
            return
        # 原有发送逻辑
        self.send("stop", config.UDP.addr,config.UDP.serport)
        print("send:stop")

    @pyqtSlot()
    def on_btn_update_cliked(self):
        # 获取某一列的所有数据
        column_data = []
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 0)
            if item is not None:
                column_data.append(item.text())
                
            else:
                column_data.append("")
        if column_data[0] != "待填入":
            config.ClientConfig.addr = column_data[0]
        else :
            self.show1()
        if column_data[1] != "待填入":
            config.ServerConfig.format_punc = column_data[1]
        else :
            self.show1()
        if column_data[2] != "待填入":
            config.UDP.addr = column_data[2]
        else :
            self.show1()
        if column_data[3] != "待填入":
            config.ClientConfig.shortcut = column_data[3]
        else :
            self.show1()
        if column_data[4] != "待填入":
            config.ClientConfig.excedir = column_data[4]
        else :
            self.show1()
        
        config.ConfigManager.save_config()

    @pyqtSlot()
    def on_btn_rest_cliked(self):
        """实现重启功能"""
        print("正在重启应用程序...")
        self.stop_services()
        QApplication.instance().processEvents()
        QTimer.singleShot(100, self._restart_application)

    def _restart_application(self):
        """实际执行重启的逻辑"""
        python = sys.executable
        args = [python] + sys.argv
        os.execl(python, python, *sys.argv)
        # 退出当前进程
        QApplication.instance().quit()
        
    
def main():
    app = QApplication(sys.argv)
    window = mydlg()  # mydlg是main.py的上部的Class的名字
    window.show()
    ret = app.exec_()
    sys.exit(ret)

if __name__ == "__main__":
    path = "C:\\Users\\14676\\Desktop\\副本机房设备清单（正式版）.xlsx"
    excel.fix_excel(path)
    main()