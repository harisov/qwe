import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Paint(QMainWindow):
    lastPoint: QPoint

    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 900, 900)
        self.setWindowTitle("Paint Lite")
        self.setWindowIcon(QIcon("Pic\paint.png"))
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.background = Qt.white
        self.penSize = 2  # размер кисти
        self.penColor = Qt.black  # цвет пера
        self.drawing = False  # флаг рисования

        self.typeLine = Qt.SolidLine  # тип линии(сплошная, перрывистая, точечная)
        self.typeEnd = Qt.RoundCap  # тип окнчания линии(округлое, прямое)
        self.typeCorner = Qt.RoundJoin  # вид угла сгиба(острый, тупой, округлый)

        menu = self.menuBar()

        file_menu = menu.addMenu("Файл")  # создаем ферхнюю менюшку под названием "Файл"

        saveAction = QAction(QIcon("Pic\сохранить.png"), "Сохранить",
                             self)  # добавляем подраздел "сохранить" в менюшку "Файл"
        file_menu.addAction(saveAction)
        saveAction.triggered.connect(self.save)

        clearAction = QAction(QIcon("Pic\метелка.png"), "Очистить",
                              self)  # добавляем подраздел "очистить" в менюшку "Файл
        file_menu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)

        pen_size = menu.addMenu("Pic\Размер Кисти")  # создаем ферхнюю менюшку под названием "Размер кисти"

        pen_2 = QAction(QIcon("Pic\ 5 px.png"), "2 px", self)  # добавляем подраздел "5 рх" в менюшку "Размер кисти"
        pen_size.addAction(pen_2)
        pen_2.triggered.connect(self.two_px)

        pen_5 = QAction(QIcon("Pic\ 2 px.png"), "5 px", self)  # добавляем подраздел "5 рх" в менюшку "Размер кисти"
        pen_size.addAction(pen_5)
        pen_5.triggered.connect(self.five_px)

        pen_7 = QAction(QIcon("Pic\ 7 px.png"), "7 px", self)  # добавляем подраздел "7 рх" в менюшку "Размер кисти"
        pen_size.addAction(pen_7)
        pen_7.triggered.connect(self.seven_px)

        pen_9 = QAction(QIcon("Pic\9 px.png"), "9 px", self)  # добавляем подраздел "9 рх" в менюшку "Размер кисти"
        pen_size.addAction(pen_9)
        pen_9.triggered.connect(self.nine_px)

        pen_12 = QAction(QIcon("Pic\9 px.png"), "12 px", self)  # добавляем подраздел "12 рх" в менюшку "Размер кисти"
        pen_size.addAction(pen_12)
        pen_12.triggered.connect(self.tw_px)

        pen_color = menu.addMenu("Цвет кисти")  # создаем верхнюю менюшку под названием "Цвет кисти"

        black_act = QAction(QIcon("Pic\черный.png"), "Черный",
                            self)  # добавляем подраздел "Черный" в менюшку "Цвет кисти"
        pen_color.addAction(black_act)
        black_act.triggered.connect(self.black)

        red_act = QAction(QIcon("Pic\красный.png"), "Красный",
                          self)  # добавляем подраздел "красный" в менюшку "Цвет кисти"
        pen_color.addAction(red_act)
        red_act.triggered.connect(self.red)

        green_act = QAction(QIcon("Pic\зеленый.png"), "Зеленый",
                            self)  # добавляем подраздел "красный" в менюшку "Цвет кисти"
        pen_color.addAction(green_act)
        green_act.triggered.connect(self.green)

        yellow_act = QAction(QIcon("Pic\желтый.png"), "Желтый",
                             self)  # добавляем подраздел "желтый" в менюшку "Цвет кисти"
        pen_color.addAction(yellow_act)
        yellow_act.triggered.connect(self.yellow)

        palette = QAction(QIcon("Pic\palette.png"), "Палитра",
                          self)  # добавляем подраздел "палитра" в менюшку "Цвет кисти"
        pen_color.addAction(palette)
        palette.triggered.connect(self.palette)

        background = menu.addMenu("Цвет заднего фона")  # создаем верхнюю менюшку под названием "Цвет заднего фона"

        white_back = QAction("Белый", self)  # добавляем подраздел "белый" в менюшку "Цвет фона"
        background.addAction(white_back)
        white_back.triggered.connect(self.white_back)

        black_back = QAction("Черный", self)
        background.addAction(black_back)
        black_back.triggered.connect(self.black_back)

        green_back = QAction("Зеленый", self)
        background.addAction(green_back)
        green_back.triggered.connect(self.green_back)

        another = QAction("Дргуой...", self)
        background.addAction(another)
        another.triggered.connect(self.another)

        pen_line = menu.addMenu("Тип линии")

        solidAction = QAction(QIcon("Pic\сплошная.png"), "Сплошная линия", self)
        pen_line.addAction(solidAction)
        solidAction.triggered.connect(self.solid)

        dashAction = QAction(QIcon("Pic\пе.png"), "Прерывистая линия", self)
        pen_line.addAction(dashAction)
        dashAction.triggered.connect(self.dash)

        dotAction = QAction(QIcon("Pic\точечная.png"), "Точечная линия", self)
        pen_line.addAction(dotAction)
        dotAction.triggered.connect(self.dot)

        end_line = menu.addMenu("Окончание линии")

        squareAction = QAction("Квадратное", self)
        end_line.addAction(squareAction)
        squareAction.triggered.connect(self.square)

        roundAction = QAction("Круглое", self)
        end_line.addAction(roundAction)
        roundAction.triggered.connect(self.round)

        corner_line = menu.addMenu("Угол сгиба")

        miter_corner = QAction(QIcon("Pic\уголок.PNG"), "Острый", self)
        corner_line.addAction(miter_corner)
        miter_corner.triggered.connect(self.miter)

        round_join_corner = QAction(QIcon("Pic\уг.PNG"), "Круглый", self)
        corner_line.addAction(round_join_corner)
        round_join_corner.triggered.connect(self.round_join)

        eraser = menu.addMenu("Стерка")

        eraser_5 = QAction(QIcon("Pic\стерка.png"), "5 px", self)
        eraser.addAction(eraser_5)
        eraser_5.triggered.connect(self.eraser_5)

        eraser_7 = QAction(QIcon("Pic\стерка.png"), "7 px", self)
        eraser.addAction(eraser_7)
        eraser_7.triggered.connect(self.eraser_7)

        eraser_9 = QAction(QIcon("Pic\стерка.png"), "9 px", self)
        eraser.addAction(eraser_9)
        eraser_9.triggered.connect(self.eraser_9)

        eraser_12 = QAction(QIcon("Pic\стерка.png"), "12 px", self)
        eraser.addAction(eraser_12)
        eraser_12.triggered.connect(self.eraser_12)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() and Qt.LeftButton) and self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.penColor, self.penSize, self.typeLine, self.typeEnd))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()
        else:
            pass

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.image, self.image.rect())

    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG(*.png);; JPEG(*.jpg)")
        if filePath == "":
            return
        self.image.save(filePath)

    def clear(self):
        self.image.fill(self.background)
        self.update()

    def two_px(self):
        self.penSize = 2
        self.update()

    def five_px(self):
        self.penSize = 5
        self.update()

    def seven_px(self):
        self.penSize = 7
        self.update()

    def nine_px(self):
        self.penSize = 9
        self.update()

    def tw_px(self):
        self.penSize = 12
        self.update()

    def black(self):
        self.penColor = Qt.black
        self.update()

    def red(self):
        self.penColor = Qt.red
        self.update()

    def green(self):
        self.penColor = Qt.green
        self.update()

    def yellow(self):
        self.penColor = Qt.yellow
        self.update()

    def palette(self):
        self.penColor = QColorDialog.getColor()

    def white_back(self):
        self.background = Qt.white
        self.image.fill(self.background)
        self.update()

    def green_back(self):
        self.background = Qt.green
        self.image.fill(self.background)
        self.update()

    def black_back(self):
        self.background = Qt.black
        self.image.fill(self.background)
        self.update()

    def another(self):
        self.background = QColorDialog.getColor()
        self.image.fill(self.background)
        self.update()

    def solid(self):
        self.typeLine = Qt.SolidLine
        self.update()

    def dot(self):
        self.typeLine = Qt.DotLine
        self.update()

    def dash(self):
        self.typeLine = Qt.DashLine
        self.update()

    def square(self):
        self.typeEnd = Qt.SquareCap
        self.update()

    def round(self):
        self.typeEnd = Qt.RoundCap
        self.update()

    def miter(self):
        self.typeCorner = Qt.MiterJoin
        self.update()

    def round_join(self):
        self.typeCorner = Qt.RoundJoin
        self.update()

    def eraser_5(self):
        self.penColor = self.background
        self.penSize = 5
        self.update()

    def eraser_7(self):
        self.penColor = self.background
        self.penSize = 7
        self.update()

    def eraser_9(self):
        self.penColor = self.background
        self.penSize = 9
        self.update()

    def eraser_12(self):
        self.penColor = self.background
        self.penSize = 12
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Paint()
    window.show()
    app.exec()