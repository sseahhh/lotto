import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QTimer

class LottoGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("now it's your turn!")
        self.setWindowIcon(QIcon(r'C:\Users\SBA\github\pyqt5\lotto_make\ball.png'))
        self.resize(600, 450)

        main_vbox = QVBoxLayout()

        title_label = QLabel("now it's your turn!", self)
        title_label.setFont(QFont('Arial', 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_vbox.addWidget(title_label)

        number_frame = QFrame(self)
        number_frame.setFrameShape(QFrame.StyledPanel)
        number_frame.setFrameShadow(QFrame.Raised)
        main_vbox.addWidget(number_frame)

        number_hbox = QHBoxLayout()
        number_frame.setLayout(number_hbox)

        self.number_labels = []
        for _ in range(6):
            label = QLabel("?", self)
            label.setFont(QFont('Arial', 30, QFont.Bold))
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(80, 80)
            label.setStyleSheet("""
                border: 3px solid #d3d3d3;
                border-radius: 40px;
                background-color: white;
            """)
            self.number_labels.append(label)
            number_hbox.addWidget(label)

        self.lotto_button = QPushButton("lotto", self)
        self.lotto_button.setFont(QFont('Arial', 16, QFont.Bold))
        self.lotto_button.setFixedSize(150, 50)
        self.lotto_button.setStyleSheet("""
            QPushButton {
                background-color: #FFC0CB; /* 파스텔 핑크 */
                color: white;
                border-radius: 25px;
                border: 2px solid #FFB6C1;
            }
            QPushButton:hover {
                background-color: #FFB6C1;
            }
            QPushButton:pressed {
                background-color: #FF69B4;
            }
        """)
        self.lotto_button.clicked.connect(self.start_lotto_animation)
        
        button_hbox = QHBoxLayout()
        button_hbox.addStretch(1)
        button_hbox.addWidget(self.lotto_button)
        button_hbox.addStretch(1)
        main_vbox.addLayout(button_hbox)

        # --- 지난주 당첨번호 ---
        last_week_vbox = QVBoxLayout()
        last_week_label = QLabel("--- 지난주 당첨번호 (1178회) ---", self)
        last_week_label.setFont(QFont('Arial', 12))
        last_week_label.setAlignment(Qt.AlignCenter)
        last_week_vbox.addWidget(last_week_label)

        last_week_hbox = QHBoxLayout()
        last_week_numbers = [5, 6, 11, 27, 43, 44]
        bonus_number = 17
        
        for num in last_week_numbers:
            label = QLabel(str(num), self)
            label.setFont(QFont('Arial', 16, QFont.Bold))
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(50, 50)
            label.setStyleSheet(self.get_ball_style(num, is_small=True))
            last_week_hbox.addWidget(label)

        plus_label = QLabel("+", self)
        plus_label.setFont(QFont('Arial', 16, QFont.Bold))
        plus_label.setAlignment(Qt.AlignCenter)
        last_week_hbox.addWidget(plus_label)

        bonus_label = QLabel(str(bonus_number), self)
        bonus_label.setFont(QFont('Arial', 16, QFont.Bold))
        bonus_label.setAlignment(Qt.AlignCenter)
        bonus_label.setFixedSize(50, 50)
        bonus_label.setStyleSheet(self.get_ball_style(bonus_number, is_small=True))
        last_week_hbox.addWidget(bonus_label)
        
        last_week_container = QWidget()
        last_week_container.setLayout(last_week_hbox)
        last_week_vbox.addWidget(last_week_container)
        main_vbox.addLayout(last_week_vbox)

        self.setLayout(main_vbox)

        # --- 애니메이션 타이머 ---
        self.spin_timer = QTimer(self)
        self.spin_timer.timeout.connect(self.update_spinning_balls)
        self.reveal_timer = QTimer(self)
        self.reveal_timer.timeout.connect(self.reveal_next_ball)
        
        self.generated_numbers = []
        self.revealed_indices = set()
        self.reveal_step = 0

        self.show()

    def start_lotto_animation(self):
        self.lotto_button.setEnabled(False)
        self.revealed_indices.clear()
        self.reveal_step = 0

        for label in self.number_labels:
            label.setText("?")
            label.setStyleSheet("""
                border: 3px solid #d3d3d3;
                border-radius: 40px;
                background-color: white;
                color: black;
            """)

        weighted_numbers = list(range(1, 46))
        most_common_numbers = [6, 14, 27, 38, 40]
        for num in most_common_numbers:
            weighted_numbers.extend([num] * 5)

        numbers = set()
        while len(numbers) < 6:
            number = random.choice(weighted_numbers)
            numbers.add(number)
        
        self.generated_numbers = sorted(list(numbers))
        
        self.spin_timer.start(30)       # 0.03초 간격으로 회전 (더 빠르게)
        self.reveal_timer.start(600)    # 0.6초 간격으로 번호 공개

    def update_spinning_balls(self):
        # 아직 공개되지 않은 공들만 회전시킴
        for i in range(6):
            if i not in self.revealed_indices:
                random_num = random.randint(1, 45)
                self.number_labels[i].setText(str(random_num))

    def reveal_next_ball(self):
        if self.reveal_step < 6:
            # 이번에 멈출 공의 인덱스를 공개된 인덱스 집합에 추가
            self.revealed_indices.add(self.reveal_step)
            
            # 해당 공의 최종 번호 설정
            num = self.generated_numbers[self.reveal_step]
            self.number_labels[self.reveal_step].setText(str(num))
            self.number_labels[self.reveal_step].setStyleSheet(self.get_ball_style(num))
            
            self.reveal_step += 1
        else:
            # 모든 번호가 공개되면 모든 타이머를 멈춤
            self.spin_timer.stop()
            self.reveal_timer.stop()
            self.lotto_button.setEnabled(True)

    def get_ball_style(self, number, is_small=False):
        if number <= 10:
            color = "#FBC400" # 노란색
        elif number <= 20:
            color = "#69C8F2" # 파란색
        elif number <= 30:
            color = "#FF7272" # 빨간색
        elif number <= 40:
            color = "#AAAAAA" # 회색
        else:
            color = "#B0D840" # 녹색
        
        radius = 25 if is_small else 40

        return f"""
            border: 3px solid {color};
            border-radius: {radius}px;
            background-color: {color};
            color: white;
            font-weight: bold;
        """

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LottoGenerator()
    sys.exit(app.exec_())