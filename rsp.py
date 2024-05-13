import random
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QLabel, QDialog, QHBoxLayout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('猜拳游戏')
        self.resize(520, 320)
        self.setWindowIcon(QIcon('Icon0.jpg'))

        background = QLabel(self)  # 设置主页面的背景
        background.setGeometry(0, 0, 520, 320)
        background.setPixmap(QPixmap("pic.png"))

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


class ChooseWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.parent.setVisible(False)  # 将初始界面设置为不可见
        self.setWindowTitle("做出选择吧")
        self.resize(520, 320)

        self.label1 = QLabel("Round:")
        self.label2 = QLabel('Player Score:')
        self.label3 = QLabel('Computer Score:')
        self.label4 = QLabel("")

        self.player_choice = ""  # 初始化玩家选择
        self.computer_choice = ""  # 初始化计算机选择
        self.max_rounds = 7  # 设置最大回合数为7
        self.round = 1
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

        score_dict = {'石头': 1, '剪刀': 2, '布': 3}

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
        self.label1.setText(f"Round: {self.round}")
        self.round += 1
        if self.round >= self.max_rounds:  # 设置最大回合数为7
            self.endgame()

    def end_game(self):
        self.accept()

    def update_scores(self):
        """重新设置双方的分值"""
        self.label2.setText(f'Player Score: {self.player_score}')
        self.label3.setText(f'Computer Score: {self.computer_score}')


class EndGame(QDialog):
    def __init__(self, player_score, computer_score):
        super().__init__()
        self.setWindowTitle('结果')

        result_text = "玩家分数: {}\n电脑分数: {}".format(player_score, computer_score)
        if player_score > computer_score:
            result_text += "\n恭喜你，你赢了！"
        elif player_score < computer_score:
            result_text += "\n电脑赢了，再试一次吧！"
        else:
            result_text += "\n平局！"

        self.label0 = QLabel(result_text, self)
        self.label0.setGeometry(50, 20, 400, 200)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
