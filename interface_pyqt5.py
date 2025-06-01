import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QWidget, QScrollArea, QTableWidget, QTableWidgetItem
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import pandas as pd

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Performance Interactive Dashboard")
        self.setGeometry(100, 100, 1200, 800)

        # Main layout
        main_layout = QVBoxLayout()

        # Button layout
        button_layout = QHBoxLayout()
        buttons = {
            "Attendance by Classroom": "visual/attendance_by_classroom_boxplot.png",
            "Clustering Heatmap": "visual/boxplocluster_heatmap.png",
            "Student by Class": "visual/student_by_class.png",
            "Association Rules Table": "visual/association_rules.png"
        }

        for label, path in buttons.items():
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked, p=path: self.display_content(p))
            button_layout.addWidget(btn)

        # Image/Table display area
        self.display_area = QScrollArea()
        self.display_area.setWidgetResizable(True)

        # Set layout
        container = QWidget()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.display_area)
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def display_content(self, path):
        if path.endswith(".csv"):
            widget = self.create_table_widget(path)
        else:
            widget = self.create_image_widget(path)

        self.display_area.setWidget(widget)

    def create_image_widget(self, image_path):
        label = QLabel()
        pixmap = QPixmap(image_path)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
        return label

    def create_table_widget(self, csv_path):
        df = pd.read_csv(csv_path)
        table = QTableWidget()
        table.setRowCount(len(df))
        table.setColumnCount(len(df.columns))
        table.setHorizontalHeaderLabels(df.columns)

        for i in range(len(df)):
            for j in range(len(df.columns)):
                table.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))

        table.resizeColumnsToContents()
        return table

def main():
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
