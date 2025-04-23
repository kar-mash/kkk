import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QTableWidgetItem,
    QDialog, QLineEdit, QPushButton, QTableWidget
)
from PyQt5 import uic
from db import get_connection, get_products, add_product, edit_product, delete_product


# --- Окно авторизации ---
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/login.ui", self)

        self.loginButton.clicked.connect(self.handle_login)

    def handle_login(self):
        username = self.loginInput.text()
        password = self.passwordInput.text()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")


# --- Окно для редактирования записи ---
class EditProductWindow(QDialog):
    def __init__(self, product_id, name, price):
        super().__init__()
        uic.loadUi("ui/edit_product.ui", self)

        self.product_id = product_id
        self.nameInput.setText(name)
        self.priceInput.setText(str(price))

        self.saveButton.clicked.connect(self.save_changes)

    def save_changes(self):
        name = self.nameInput.text().strip()
        price = self.priceInput.text().strip()

        if not name or not price.replace('.', '', 1).isdigit():
            QMessageBox.warning(self, "Ошибка", "Введите корректные данные")
            return

        try:
            edit_product(self.product_id, name, float(price))
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при изменении: {e}")


# --- Главное окно приложения ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/main.ui", self)

        self.nameInput = self.findChild(QLineEdit, "nameInput")
        self.priceInput = self.findChild(QLineEdit, "priceInput")
        self.tableWidget = self.findChild(QTableWidget, "tableWidget")

        self.addButton = self.findChild(QPushButton, "addButton")
        self.editButton = self.findChild(QPushButton, "editButton")
        self.deleteButton = self.findChild(QPushButton, "deleteButton")

        self.addButton.clicked.connect(self.add_record)
        self.editButton.clicked.connect(self.edit_record)
        self.deleteButton.clicked.connect(self.delete_record)

        self.load_data()

    def load_data(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Название', 'Цена'])

        for i, (id_, name, price) in enumerate(get_products()):
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(id_)))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(name))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(price)))

    def add_record(self):
        name = self.nameInput.text().strip()
        price = self.priceInput.text().strip()

        if not name or not price.replace('.', '', 1).isdigit():
            QMessageBox.warning(self, "Ошибка", "Введите корректные данные")
            return

        try:
            add_product(name, float(price))
            self.nameInput.clear()
            self.priceInput.clear()
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении: {e}")

    def edit_record(self):
        selected = self.tableWidget.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите строку для изменения")
            return

        row_id = int(self.tableWidget.item(selected, 0).text())
        name = self.tableWidget.item(selected, 1).text()
        price = float(self.tableWidget.item(selected, 2).text())

        dialog = EditProductWindow(row_id, name, price)
        if dialog.exec_():
            self.load_data()

    def delete_record(self):
        selected = self.tableWidget.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите строку для удаления")
            return

        row_id = int(self.tableWidget.item(selected, 0).text())

        try:
            delete_product(row_id)
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении: {e}")


# --- Запуск программы ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
