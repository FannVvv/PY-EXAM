import random
import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QLabel, QDialog, QHBoxLayout, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('猜拳游戏')
        self.resize(520, 320)
        self.setWindowIcon(QIcon('pictures/Icon0.jpg'))

        background = QLabel(self)  # 设置主页面的背景
        background.setGeometry(0, 0, 520, 320)
        background.setPixmap(QPixmap("pictures/pic.png"))

        self.label1 = QLabel("欢迎来到猜拳游戏！", self)  # 设置标签名称
        self.label1.setGeometry(50, 20, 420, 50)  # 设置标签的位置
        self.label1.setAlignment(Qt.AlignCenter)  # 设置标签文本居中
        font = QFont("Arial", 20)
        font.setBold(True)  # 设置字体加粗
        self.label1.setFont(font)  # 设置字体格式
        self.label1.setStyleSheet("color:blue;")

        self.btn1 = QPushButton('START', self)
        self.btn1.setGeometry(30, 180, 200, 100)
        self.btn1.clicked.connect(self.open_second_window)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label1)
        layout.addWidget(self.btn1)

    def open_second_window(self):
        self.choose_window = ChooseWindow(self)
        self.choose_window.show()
        self.hide()


class ChooseWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("做出选择吧")
        self.resize(520, 320)

        self.label1 = QLabel("Round:")
        self.label2 = QLabel('玩家得分:')
        self.label3 = QLabel('电脑得分:')
        self.label4 = QLabel("")

        self.player_choice = ""  # 初始化玩家选择
        self.computer_choice = ""  # 初始化计算机选择
        self.max_rounds = 5  # 设置最大回合数为5
        self.round = 0
        self.player_score = 0
        self.computer_score = 0

        self.update_scores()

        self.btn1 = QPushButton('石头')
        self.btn1.setFixedSize(150, 100)
        self.btn1.clicked.connect(self.choose_rock)

        self.btn2 = QPushButton('剪刀')
        self.btn2.setFixedSize(150, 100)
        self.btn2.clicked.connect(self.choose_scissors)

        self.btn3 = QPushButton('布')
        self.btn3.setFixedSize(150, 100)
        self.btn3.clicked.connect(self.choose_paper)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn1)
        button_layout.addWidget(self.btn2)
        button_layout.addWidget(self.btn3)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label1)
        main_layout.addWidget(self.label2)
        main_layout.addWidget(self.label3)
        main_layout.addWidget(self.label4)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def choose_rock(self):
        self.make_choice('石头')

    def choose_scissors(self):
        self.make_choice('剪刀')

    def choose_paper(self):
        self.make_choice('布')

    def make_choice(self, player_choice):
        """判断双方的输赢"""
        self.player_choice = player_choice
        self.computer_choice = random.choice(['石头', '剪刀', '布'])

        if self.computer_choice == player_choice:
            pass
        elif self.computer_choice == '石头' and player_choice == '布':
            self.player_score += 1
        elif self.computer_choice == '石头' and player_choice == '剪刀':
            self.computer_score += 1
        elif self.computer_choice == '剪刀' and player_choice == '布':
            self.computer_score += 1
        elif self.computer_choice == '剪刀' and player_choice == '石头':
            self.player_score += 1
        elif self.computer_choice == '布' and player_choice == '石头':
            self.computer_score += 1
        elif self.computer_choice == '布' and player_choice == '剪刀':
            self.player_score += 1

        self.update_choice()
        self.update_scores()
        self.update_round()

    def update_choice(self):
        """显示双方的选择"""
        self.label4.setText(
            f"你选择 {self.player_choice}                  |                 计算机选择 {self.computer_choice}")

    def update_round(self):
        """更新回合数并检查"""

        self.round += 1
        self.label1.setText(f"Round: {self.round}")
        if self.round == self.max_rounds:  # 设置最大回合数为5,
            # 延迟结束游戏以便显示最后一回合的结果
            QTimer.singleShot(500, self.end_game)  # 延迟500毫秒

    def end_game(self):
        self.hide()
        ending = EndGame(self.player_score, self.computer_score)
        ending.exec_()

    def update_scores(self):
        """重新设置双方的分值"""
        self.label2.setText(f'Player Score: {self.player_score}')
        self.label3.setText(f'Computer Score: {self.computer_score}')


class EndGame(QDialog):
    def __init__(self, player_score, computer_score):
        super().__init__()
        self.setWindowTitle('结果')
        self.setGeometry(0, 0, 520, 320)
        self.player_score = player_score
        self.computer_score = computer_score
        background = QLabel(self)  # 设置页面的背景
        background.setGeometry(0, 0, 520, 320)
        background.setPixmap(QPixmap("pictures/pic_end.png"))

        result_text = "玩家分数: {}\n电脑分数: {}".format(player_score, computer_score)
        font = QFont("Arial", 32)
        font.setBold(True)  # 设置字体加粗
        
        
        self.label0 = QLabel(result_text, self)
        self.label0.setGeometry(50, 20, 400, 200)
        self.label0.setFont(font)  # 设置字体格式

        # 弹出消息框
        self.show_message(player_score, computer_score)

    def show_message(self, player_score, computer_score):
        msg = QMessageBox()
        msg.setWindowTitle("游戏结束")
        if player_score > computer_score:  # 根据游戏结果设置图标
            msg.setText("恭喜你，你赢了！")
            msg.setIcon(QMessageBox.Information)
            
            msg.setIconPixmap(QPixmap('pictures/pic_win.jpg').scaled(520, 320, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        elif player_score < self.computer_score:
            msg.setText("电脑赢了，再试一次吧！")
            msg.setIcon(QMessageBox.Warning)
            
            msg.setIconPixmap(QPixmap('pictures/pic_defeat.jpg').scaled(520, 320, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            msg.setText("平局！")
            msg.setIcon(QMessageBox.Information)
            
            msg.setIconPixmap(QPixmap('pictures/pic_draw.jpg').scaled(520, 320, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        msg.exec_()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
