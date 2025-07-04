import sys
import os
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QSpinBox,
    QPushButton, QVBoxLayout, QHBoxLayout, QCheckBox,
    QGroupBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
print("Testing git integration")


class LargeStepSpinBox(QSpinBox):
    def __init__(self):
        super().__init__()
        self.setSingleStep(100)
        self.setStyleSheet("""
            QSpinBox {
                font-size: 16px;
                height: 30px;
                width: 100px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 30px;
                height: 20px;
            }
            QSpinBox::up-arrow, QSpinBox::down-arrow {
                width: 15px;
                height: 15px;
            }
        """)


class UnitSection(QGroupBox):
    def __init__(self, unit_names):
        super().__init__("Enemy Unit")
        self.setStyleSheet("""
            QGroupBox {
                border: 2px solid #66fcf1;
                border-radius: 5px;
                margin-top: 10px;
                padding: 10px;
                font-weight: bold;
            }
        """)
        layout = QHBoxLayout()

        self.unit_dropdown = QComboBox()
        self.unit_dropdown.addItems(sorted(unit_names))
        self.unit_dropdown.setStyleSheet("font-size: 14px;")
        self.unit_dropdown.setMinimumWidth(150)

        self.credits_label = QLabel("Credits Invested:")
        self.credits_label.setStyleSheet("font-size: 14px;")

        self.credits_input = LargeStepSpinBox()
        self.credits_input.setRange(0, 100000)
        self.credits_input.setValue(1000)

        layout.addWidget(self.unit_dropdown)
        layout.addWidget(self.credits_label)
        layout.addWidget(self.credits_input)
        self.setLayout(layout)


class TechThemeUI(QWidget):
    def __init__(self):
        super().__init__()

        self.unit_names = [
            "Abyss", "Hound", "Phantom Ray", "Raiden", "Farseer", "Fire Badger", "Tarantula", "Sandworm",
            "Sabertooth", "Scorpion", "Wraith", "War Factory", "Phoenix", "Arclight",
            "Hacker", "Sledgehammer", "Stormcaller", "Overlord", "Crawler", "Fang",
            "Steel Ball", "Mustang", "Wasp", "Rhino", "Melting Point", "Marksman",
            "Fortress", "Vulcan", "Mountain", "Typhoon"
        ]

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Unit Counter Tool")
        self.setStyleSheet("background-color: #0b0c10; color: #66fcf1; font-size: 16px;")

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Directly add unit sections to main layout
        self.unit_sections_container = QVBoxLayout()
        self.main_layout.addLayout(self.unit_sections_container)

        self.add_unit_section()  # Add first section

        # Add button below unit sections
        add_button = QPushButton("+ Add Unit")
        add_button.setStyleSheet("background-color: #1f2833; color: #66fcf1; font-size: 16px;")
        add_button.clicked.connect(self.add_unit_section)
        self.main_layout.addWidget(add_button)

        # Checkboxes
        fire_badger_checkbox = QCheckBox("Fire Badger")
        fire_badger_checkbox.setStyleSheet("color: #66fcf1; font-size: 16px;")
        typhoon_checkbox = QCheckBox("Typhoon")
        typhoon_checkbox.setStyleSheet("color: #66fcf1; font-size: 16px;")

        checkbox_frame = QGroupBox("Spec Unlocks")
        checkbox_layout = QVBoxLayout()
        checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        checkbox_layout.addWidget(fire_badger_checkbox)
        checkbox_layout.addWidget(typhoon_checkbox)
        checkbox_frame.setLayout(checkbox_layout)
        checkbox_frame.setStyleSheet("""
            QGroupBox {
                border: 2px solid #45a29e;
                padding: 10px;
                font-weight: bold;
            }
        """)
        self.main_layout.addWidget(checkbox_frame)

        # Analysis section
        self.counter_button = QPushButton("Counter")
        self.counter_button.setStyleSheet("background-color: #1f2833; color: #66fcf1; font-size: 16px;")
        self.counter_button.setFixedHeight(40)
        self.counter_button.clicked.connect(self.handle_counter_click)

        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("font-size: 16px; font-weight: bold; min-height: 30px;")

        self.image_label = QLabel()
        self.image_label.setFixedSize(151, 230)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: #1f2833; border: 2px solid #66fcf1;")

        analysis_frame = QGroupBox("Counter Calculator")
        analysis_layout = QVBoxLayout()
        analysis_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        analysis_layout.addWidget(self.counter_button, alignment=Qt.AlignmentFlag.AlignCenter)
        analysis_layout.addSpacing(10)
        analysis_layout.addWidget(self.result_label, alignment=Qt.AlignmentFlag.AlignCenter)
        analysis_layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        analysis_frame.setLayout(analysis_layout)
        analysis_frame.setStyleSheet("""
            QGroupBox {
                border: 2px solid #45a29e;
                padding: 10px;
                font-weight: bold;
            }
        """)
        self.main_layout.addWidget(analysis_frame)

    def add_unit_section(self):
        section = UnitSection(self.unit_names)
        self.unit_sections_container.addWidget(section)
        self.adjustSize()  # Dynamically grow the window height

    def handle_counter_click(self):
        unit_name = random.choice(self.unit_names)
        self.result_label.setText(f"Suggested Unit: {unit_name}")

        image_path = f"./mechabellum units/{unit_name}.jpg"
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path).scaled(
                self.image_label.width(),
                self.image_label.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(pixmap)
            self.image_label.setText("")
        else:
            self.image_label.setPixmap(QPixmap())  # Clear old image
            self.image_label.setText("Image not found")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TechThemeUI()
    window.show()
    sys.exit(app.exec())
