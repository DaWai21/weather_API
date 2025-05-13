import sys
from http.client import HTTPException

import requests
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout, QPushButton, QLineEdit, QVBoxLayout
from PyQt5.Qt import Qt
from requests import HTTPError


class Weatherapp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter the city",self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get weather",self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.discribe_label = QLabel(self)
        self.initui()

    def initui(self):
        self.setWindowTitle("Weather app")
        vbox = QVBoxLayout()

        vbox.addWidget(self.city_input)
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.discribe_label)
        self.setLayout(vbox)

        self.city_input.setAlignment(Qt.AlignCenter)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.discribe_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.discribe_label.setObjectName("discribe_label")

        self.setStyleSheet("""
        QLabel, QPushbutton{
        font-family: calibri;
        }
        QLineEdit#city_input{
        font-size : 40px;
        font-color: red;
        }
        QLabel#city_label{
        font-size: 40px;
        font-color: red;
        font-style: Italic;
        }
        QPushButton#get_weather_button{
        font-size : 30px;
        font-weight : bold;
        }
        QLabel#temperature_label{
        font-size: 50px;
        font-color: rgb(252, 186, 3);
        }
        QLabel#emoji_label{
        font-size: 100px;
        font-family: Segoe UI emoji;
        }
        QLabel#discribe_label{
        font-size: 50px;
        }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)


    def get_weather(self):
        api_key ="caf21758f6ca3caff09063f8944ed8b5"
        city = self.city_input.text()
        url =f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError:
                match response.status_code:
                    case 400:
                        self.display_error("Bad request")
                    case 401:
                        self.display_error("Unauthorized")
                    case 403:
                        self.display_error("Forbidden")
                    case 404:
                        self.display_error("Not Found")
                    case 500:
                        self.display_error("Internal Server Error")
                    case 502:
                        self.display_error("Bad Gateway")
                    case 503:
                        self.display_error("Service unavailable")
                    case 505:
                        self.display_error("Gateway Timeout ")
        except requests.exceptions.ConnectionError:
            self.display_error("Disconnected")
        except requests.exceptions.Timeout:
            self.display_error("Connection Time out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request error: {req_error}")


    def display_error(self,message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.discribe_label.clear()

    def display_weather(self,data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temp =  data["main"]["temp"]
        temp_c = temp - 273.15
        self.temperature_label.setText(f"{temp_c: .0f}°C")
        weather_des = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]
        self.discribe_label.setStyleSheet("font-size: 30px;")
        self.discribe_label.setText(f"{weather_des}")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))

    @staticmethod
    def get_weather_emoji(weather_id):

        if 200 <= weather_id <= 232:
            return"⛈️"
        elif 300 <= weather_id <=314:
            return"🌦️"
        elif 500 <= weather_id <=531:
            return"☔"
        elif 600 <= weather_id <=622:
            return"☃️"
        elif 701 <= weather_id <= 741:
            return"🌁"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "🌤️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    weatherapp = Weatherapp()
    weatherapp.show()
    sys.exit(app.exec_())