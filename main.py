import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.cor = sqlite3.connect('coffee.sqlite')
        self.cur = self.cor.cursor()
        self.see.clicked.connect(self.load_table)
        self.add_update_btn.clicked.connect(self.add_update)

    def load_table(self):
        self.tableWidget.verticalHeader().setVisible(False)
        self.data = self.cur.execute("Select * from coffee").fetchall()
        self.tableWidget.setColumnCount(len(self.data[0]))
        names = [description[0] for description in self.cur.description]
        self.tableWidget.setHorizontalHeaderLabels(names)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(self.data):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def add_update(self):
        self.add_update_window = AddUpdateBtn(self)
        self.add_update_window.show()


class AddUpdateBtn(QMainWindow):
    def __init__(self, parrent):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.parrent = parrent
        self.add_btn.clicked.connect(self.add_data)
        self.update_btn.clicked.connect(self.update_data)

    def add_data(self):
        self.statusBar().showMessage("")
        try:
            if not self.add_lineedit.text():
                raise
            text = self.add_lineedit.text().split(";")
            if len(text) != 7:
                raise
            if not text[0].isdigit() or not text[-1].isdigit() or not text[-2].isdigit():
                raise
            text[0], text[-1], text[-2] = int(text[0]), int(text[-1]), int(text[-2])
            text = tuple(text)
            self.parrent.cur.execute(
                f"Insert Into coffee VALUES ({int(text[0])}, '{text[1]}', '{text[2]}', "
                f"'{text[3]}', '{text[4]}', {int(text[5])}, {int(text[6])})")
            self.parrent.cor.commit()
            self.parrent.load_table()
        except RuntimeError:
            self.statusBar().showMessage('Некорректный ввод')
        except Exception:  # непредвиденные ошибки при записи в бд
            self.statusBar().showMessage("Error")

    def update_data(self):
        pass


def except_hook(cls, exception, traceback):
    sys.excepthook(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffee()
    sys.excepthook = except_hook
    ex.show()
    sys.exit(app.exec())
