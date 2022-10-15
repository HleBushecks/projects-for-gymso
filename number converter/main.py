import sys
from functools import partial

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.font_size = 30
        self.font = QFont()
        self.font.setPixelSize(self.font_size)
        self.numbers = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        systems = list(range(2, 37))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.grid = QGridLayout(central_widget)

        self.combo_box1 = QComboBox()
        self.combo_box1.addItems(list(map(lambda x: str(x), systems)))
        self.combo_box1.currentIndexChanged.connect(self.change)
        self.combo_box2 = QComboBox()
        self.combo_box2.addItems(list(map(lambda x: str(x), systems)))
        self.combo_box2.currentIndexChanged.connect(self.keyboard)

        self.grid.addWidget(self.combo_box1, 0, 0)
        self.grid.addWidget(self.combo_box2, 0, 1)

        self.horizontal_layout1 = QHBoxLayout()
        self.horizontal_layout2 = QHBoxLayout()
        self.grid_layout = QGridLayout()

        self.grid.addLayout(self.horizontal_layout1, 1, 0, 1, 2)
        self.grid.addLayout(self.horizontal_layout2, 2, 0, 1, 2)
        self.grid.addLayout(self.grid_layout, 3, 0, 1, 2)

        btn_font_minus = QPushButton("-")
        btn_backspace = QPushButton('<--')
        btn_font_plus = QPushButton("+")

        btn_font_minus.clicked.connect(self.font_minus)
        btn_backspace.clicked.connect(self.backspace)
        btn_font_plus.clicked.connect(self.font_plus)

        self.horizontal_layout2.addWidget(btn_font_minus)
        self.horizontal_layout2.addWidget(btn_backspace)
        self.horizontal_layout2.addWidget(btn_font_plus)

        self.line_edit1 = QLineEdit()
        self.line_edit1.setReadOnly(True)
        self.line_edit1.setFont(self.font)
        self.line_edit1.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))

        self.line_edit2 = QLineEdit()
        self.line_edit2.setReadOnly(True)
        self.line_edit2.setFont(self.font)
        self.line_edit2.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))

        self.horizontal_layout1.addWidget(self.line_edit1)
        self.horizontal_layout1.addWidget(self.line_edit2)

        self.keyboard()

    def change(self):
        self.line_edit1.clear()
        self.line_edit2.clear()
        self.keyboard()

    def keyboard(self):
        self.conversion()
        for i in range(self.grid_layout.count()):
            self.grid_layout.itemAt(i).widget().deleteLater()
        keys = self.numbers[:self.combo_box1.currentIndex() + 2]
        x = 0
        y = 0
        for i in keys:
            btn = QPushButton(i)
            btn.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
            btn.setFont(self.font)
            btn.clicked.connect(partial(self.add_number, i))
            self.grid_layout.addWidget(btn, y, x)
            x += 1
            if x == 10:
                x = 0
                y += 1

    def add_number(self, number):
        self.line_edit1.setText(self.line_edit1.text() + number)
        self.conversion()

    def conversion(self):
        if self.line_edit1.text():
            number_from = int(self.line_edit1.text(), (self.combo_box1.currentIndex() + 2))

            number_to = ''
            while number_from > 0:
                number_to = self.numbers[number_from % (self.combo_box2.currentIndex() + 2)] + number_to
                number_from = number_from // (self.combo_box2.currentIndex() + 2)
            self.line_edit2.setText(f'{number_to}')
            if number_to == '':
                self.line_edit2.setText(self.line_edit1.text())

    def font_minus(self):
        self.font_size -= 1
        self.font.setPixelSize(self.font_size)
        self.line_edit1.setFont(self.font)
        self.line_edit2.setFont(self.font)
        self.keyboard()

    def backspace(self):
        self.line_edit1.setText(self.line_edit1.text()[0:-1])
        self.line_edit2.clear()
        self.conversion()

    def font_plus(self):
        self.font_size += 1
        self.font.setPixelSize(self.font_size)
        self.line_edit1.setFont(self.font)
        self.line_edit2.setFont(self.font)
        self.keyboard()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
