import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageLabelingTool(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_index = 0
        self.json_data = self.load_json_data('./PyQt/qr_data.json')
        self.temp_coordinates = None  # 임시 좌표 저장을 위한 변수

        # 버튼 멤버 변수 추가
        self.prev_button = QPushButton('Previous')
        self.next_button = QPushButton('Next')

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Labeling Tool')

        # Main widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        # self.setFocusPolicy(Qt.StrongFocus)
        
        # Left and right image viewers
        self.left_image_label = QLabel()
        self.right_image_label = QLabel()
        self.left_scroll_area = self.create_scrollable_area(self.left_image_label)
        self.right_scroll_area = self.create_scrollable_area(self.right_image_label)
        main_layout.addWidget(self.left_scroll_area)
        main_layout.addWidget(self.right_scroll_area)

        # Navigation buttons
        nav_layout = QVBoxLayout()
        # 멤버 변수로 생성된 버튼 사용
        self.prev_button.clicked.connect(self.load_previous_image)
        self.next_button.clicked.connect(self.load_next_image)
        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.next_button)
        main_layout.addLayout(nav_layout)

        # Load initial images
        self.load_images()

        # 클릭 이벤트 연결
        self.left_image_label.mousePressEvent = self.on_left_image_clicked

        # 키보드 이벤트 연결
        self.left_image_label.setFocusPolicy(Qt.StrongFocus)
        self.left_image_label.keyPressEvent = self.on_key_pressed

        # # 이미지 이름을 표시할 QLabel 위젯 추가
        # self.left_image_name_label = QLabel()
        # self.right_image_name_label = QLabel()
        # nav_layout.addWidget(self.left_image_name_label)
        # nav_layout.addWidget(self.right_image_name_label)


    def create_scrollable_area(self, widget):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(widget)
        return scroll_area

    def load_json_data(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def load_images(self):
        data = self.json_data[str(self.current_index)]
        self.left_image_label.setPixmap(QPixmap(data['prev_path']))
        self.right_image_label.setPixmap(QPixmap(data['image_path']))

        # 스크롤 위치 조정
        self.left_scroll_area.verticalScrollBar().setValue(data['y_pixel'])
        self.right_scroll_area.verticalScrollBar().setValue(data['y_pixel'])
        print(data['y_pixel'])

        # # # 이미지 이름 표시
        # self.left_image_label.setText(data['image_path'])
        # self.right_image_label.setText(data['prev_path'])


    def on_left_image_clicked(self, event):
        self.temp_coordinates = (event.pos().x(), event.pos().y())

    def on_key_pressed(self, event):
        # 엔터 키 또는 리턴 키를 누를 때 좌표 저장
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            if self.temp_coordinates:
                self.save_click_coordinates(*self.temp_coordinates)
                self.temp_coordinates = None
        # 스페이스바를 누를 때 창 닫기
        elif event.key() == Qt.Key_Space:
            self.close()
            #######
        elif event.key() == Qt.Key_Left:
            self.prev_button.click()  # 'a' 키를 누르면 'Previous' 버튼 클릭 시뮬레이션
        elif event.key() == Qt.Key_Right:
            self.next_button.click()  # 'd' 키를 누르면 'Next' 버튼 클릭 시뮬레이션
        

    def save_click_coordinates(self, x, y):
        # 클릭된 좌표를 JSON 파일로 저장
        qr_id = self.json_data[str(self.current_index)]['qr_ID']
        json_file_name = f"{qr_id}_coordinates.json"

        # 클릭된 좌표 데이터 생성
        data = {"prev_location": {"x": x, "y": y}}

        # JSON 파일로 저장
        with open(json_file_name, 'w') as file:
            json.dump(data, file, indent=4)

        print(f'json file saved at {json_file_name}')

    def load_previous_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_images()

    def load_next_image(self):
        if self.current_index < len(self.json_data) - 1:
            self.current_index += 1
            self.load_images()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ex = ImageLabelingTool()
    ex.show()
    sys.exit(app.exec_())
