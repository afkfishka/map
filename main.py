import os
import sys
import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi

WINDOW_WIDTH = 650
WINDOW_HEIGHT = 550
z = 10


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('untitled.ui', self)
        self.ll = '37.530887,55.703118'
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.getImage()
        self.initUI()


    def getImage(self):
        server_address = 'https://static-maps.yandex.ru/1.x/'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        size = '650,450'
        params = {
            'll': self.ll,
            'z': z,
            'size': size,
            'l': 'map',
            'apikey': api_key
        }

        response = requests.get(server_address, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(response.url)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.pixmap = QPixmap(self.map_file)
        self.map.setPixmap(self.pixmap)
        self.map.setFixedSize(650, 450)
        self.pushButton1.clicked.connect(self.new_loc)

    def new_loc(self):
        server_address = 'http://geocode-maps.yandex.ru/1.x/?'
        api_key = "1f9c9d43-845e-4888-a31f-6c1539fb2794"
        geocode = self.lineEdit1.text()
        geocoder_request = f'{server_address}apikey={api_key}&geocode={geocode}&format=json'
        response = requests.get(geocoder_request)
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = ','.join(toponym["Point"]["pos"].split())
        self.ll = toponym_coodrinates
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.map.setPixmap(self.pixmap)


    def keyPressEvent(self, event):
        global z
        if event.key() == Qt.Key.Key_PageUp and z < 21:
            z += 1
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.map.setPixmap(self.pixmap)

        elif event.key() == Qt.Key.Key_PageDown and z > 0:
            z -= 1
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.map.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
