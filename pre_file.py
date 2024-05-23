import random
import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QLabel, QDialog, QHBoxLayout, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置主窗口的标题、尺寸和图标
        self.setWindowTitle('猜拳游戏')
        self.resize(520, 320)
        self.setWindowIcon(QIcon('pictures/Icon0.jpg'))
        
        # 设置主窗口的背景图片
        background = QLabel(self)
        background.setGeometry(0, 0, 520, 320)
        background.setPixmap(QPixmap("pictures/pic.png"))

        # 设置标签的文本、字体和位置
        self.label1 = QLabel("欢迎来到猜拳游戏！", self)
        self.label1.setGeometry(50, 20, 420, 50)
        self.label1.setAlignment(Qt.AlignCenter)
        font = QFont("Arial", 20)
        font.setBold(True)
        self.label1.setFont(font)
        self.label1.setStyleSheet("color:blue;")

        # 设置开始按钮及其位置，并连接到打开选择窗口的槽函数
        self.btn1 = QPushButton('START', self)
        self.btn1.setGeometry(30, 180, 200, 100)
        self.btn1.clicked.connect(self.open_second_window)

    def open_second_window(self):
        """槽函数，在按钮发出信号时被调用，打开选择窗口并隐藏主窗口"""
        self.choose_window = ChooseWindow(self)
        self.choose_window.show()
        self.hide()


class ChooseWindow(QDialog):
    def __init__(self, parent=None):
        """在构造函数里设置所有的内容"""
        super().__init__(parent)

        # 设置选择窗口的标题和尺寸
        self.setWindowTitle("做出选择吧")
        self.resize(520, 320)

        # 初始化标签和游戏参数
        self.label1 = QLabel("Round:")
        self.label2 = QLabel('玩家得分:')
        self.label3 = QLabel('电脑得分:')
        self.label4 = QLabel("")
        self.player_choice = ""
        self.computer_choice = ""
        self.max_rounds = 5
        self.round = 0
        self.player_score = 0
        self.computer_score = 0

        # 初始化显示双方的得分标签
        self.update_scores()

        # 创建选择按钮并设置其尺寸和点击事件
        self.btn1 = QPushButton('石头')
        self.btn1.setFixedSize(150, 100)
        self.btn1.clicked.connect(self.choose_rock)

        self.btn2 = QPushButton('剪刀')
        self.btn2.setFixedSize(150, 100)
        self.btn2.clicked.connect(self.choose_scissors)

        self.btn3 = QPushButton('布')
        self.btn3.setFixedSize(150, 100)
        self.btn3.clicked.connect(self.choose_paper)

        # 把三个按钮设置为水平布局
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn1)
        button_layout.addWidget(self.btn2)
        button_layout.addWidget(self.btn3)

        # 把所有的展示结果的标签设置为垂直布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label1)
        main_layout.addWidget(self.label2)
        main_layout.addWidget(self.label3)
        main_layout.addWidget(self.label4)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def choose_rock(self):
        """玩家选择石头"""
        self.make_choice('石头')

    def choose_scissors(self):
        """玩家选择剪刀"""
        self.make_choice('剪刀')

    def choose_paper(self):
        """玩家选择布"""
        self.make_choice('布')

    def make_choice(self, player_choice):
        """判断双方的输赢并更新分数和回合"""
        self.player_choice = player_choice
        self.computer_choice = random.choice(['石头', '剪刀', '布'])

        # 定义所有可能的输赢情况
        outcomes = {
            ('石头', '布'): 'player',
            ('石头', '剪刀'): 'computer',
            ('剪刀', '布'): 'computer',
            ('剪刀', '石头'): 'player',
            ('布', '石头'): 'computer',
            ('布', '剪刀'): 'player',
        }

        if self.computer_choice != player_choice:
            winner = outcomes.get((self.computer_choice, player_choice))
            if winner == 'player':
                self.player_score += 1
            elif winner == 'computer':
                self.computer_score += 1

        # 更新显示双方选择的标签、分数和回合数
        self.update_choice()
        self.update_scores()
        self.update_round()

    def update_choice(self):
        """显示双方的选择"""
        self.label4.setText(
            f"你选择 {self.player_choice}                  |||                 计算机选择 {self.computer_choice}")

    def update_round(self):
        """更新回合数并检查是否达到最大回合数"""
        self.round += 1
        self.label1.setText(f"Round: {self.round}")
        if self.round == self.max_rounds:
            # 延迟结束游戏以便显示最后一回合的结果
            QTimer.singleShot(500, self.end_game)

    def end_game(self):
        """结束游戏并显示结果窗口"""
        self.hide()
        ending = EndGame(self.player_score, self.computer_score)
        ending.exec_()

    def update_scores(self):
        """重新设置并显示双方的分数"""
        self.label2.setText(f'Player Score: {self.player_score}')
        self.label3.setText(f'Computer Score: {self.computer_score}')


class EndGame(QDialog):
    def __init__(self, player_score, computer_score):
        """初始化结果窗口"""
        super().__init__()
        self.setWindowTitle('结果')
        self.setGeometry(0, 0, 520, 320)
        self.player_score = player_score
        self.computer_score = computer_score

        # 设置结果窗口的背景图片
        background = QLabel(self)
        background.setGeometry(0, 0, 520, 320)
        background.setPixmap(QPixmap("pictures/pic_end.png"))

        # 显示最终分数
        result_text = "玩家分数: {}\n电脑分数: {}".format(player_score, computer_score)
        font = QFont("Arial", 32)
        font.setBold(True)

        self.label0 = QLabel(result_text, self)
        self.label0.setGeometry(50, 20, 400, 200)
        self.label0.setFont(font)

        # 弹出消息框显示比赛结果
        self.show_message(player_score, computer_score)

    def show_message(self, player_score, computer_score):
        """根据最终分数显示不同的结果信息"""
        msg = QMessageBox()
        msg.setWindowTitle("游戏结束")
        if player_score > computer_score:
            msg.setText("恭喜你，你赢了！")
            msg.setIcon(QMessageBox.Information)
            msg.setIconPixmap(QPixmap('pictures/pic_win.jpg').scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        elif player_score < self.computer_score:
            msg.setText("电脑赢了，再试一次吧！")
            msg.setIcon(QMessageBox.Warning)
            msg.setIconPixmap(QPixmap('pictures/pic_defeat.jpg').scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            msg.setText("平局！")
            msg.setIcon(QMessageBox.Information)
            msg.setIconPixmap(QPixmap('pictures/pic_draw.jpg').scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        msg.exec_()


app = QApplication(sys.argv)  # 创建应用程序实例并运行
main_window = MainWindow()  # 创建窗口的实例对象
main_window.show()  # 进行第一步，展示主窗口
sys.exit(app.exec())  # app.exec()启动事件循环并返回状态码，如果成功则为0，程序正常退出 
