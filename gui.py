from miio import AirPurifier
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

ip_address = "192.168.1.141"
token = "9669b15db6364ad79a76e9b9fc051b09"

purifier = AirPurifier(ip_address, token)

class App:
    def __init__(self, master):
        # 윈도우 생성
        self.master = master
        self.master.title("미세먼지 측정기")

        # 라벨 생성
        self.air_quality_label = tk.Label(master, text="미세먼지: ", font=("Helvetica", 16))
        self.temperature_label = tk.Label(master, text="온도: ", font=("Helvetica", 16))
        self.humidity_label = tk.Label(master, text="습도: ", font=("Helvetica", 16))

        # 라벨 위치 설정
        self.air_quality_label.grid(row=0, column=0, sticky="W")
        self.temperature_label.grid(row=1, column=0, sticky="W")
        self.humidity_label.grid(row=2, column=0, sticky="W")

        # 그래프 생성
        self.figure = plt.figure(figsize=(5, 4), dpi=100)
        self.subplot = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master)
        self.canvas.get_tk_widget().grid(row=3, columnspan=2)

        # 그래프 타이틀 설정
        self.subplot.set_title("미세먼지 추이")

        # 그래프 축 라벨 설정
        self.subplot.set_xlabel("시간")
        self.subplot.set_ylabel("미세먼지 농도 (ug/m3)")

        # 그래프 데이터 초기화
        self.x_data = [time.time()]
        self.y_data = [0]

        # 그래프 설정
        self.line, = self.subplot.plot(self.x_data, self.y_data)

        # 업데이트 버튼 생성
        self.update_button = tk.Button(master, text="업데이트", command=self.update)
        self.update_button.grid(row=4, column=0, sticky="W")

        # 종료 버튼 생성
        self.quit_button = tk.Button(master, text="종료", command=master.quit)
        self.quit_button.grid(row=4, column=1, sticky="E")

    def update(self):
        # 미세먼지 측정기에서 데이터 가져오기
        status = purifier.status()
        air_quality = status.aqi
        temperature = status.temperature
        humidity = status.humidity

        # 라벨 텍스트 업데이트
        self.air_quality_label.config(text="미세먼지: {} ug/m3".format(air_quality))
        self.temperature_label.config(text="온도: {}°C".format(temperature))
        self.humidity_label.config(text="습도: {}%".format(humidity))

        # 그래프 데이터 업데이트
        self.x_data.append(time.time())
        self.y_data.append(air_quality)
        self.line.set_xdata(self.x_data)
        self.line.set_ydata(self.y_data)
        self.subplot.relim()
        self.subplot.autoscale_view()

        # 그래프 캔버스 업데이트
        self.canvas.draw()

    def update_graph(self):
        # 업데이트 함수를 1초마다 호출하면서 그래프 업데이트
        self.update()
        self.master.after(1000, self.update_graph)
