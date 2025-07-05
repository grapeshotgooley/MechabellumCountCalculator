import sys
import os
import random
import pandas as pd

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QSpinBox,
    QPushButton, QVBoxLayout, QHBoxLayout, QCheckBox,
    QGroupBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

print("program init")

matchup_matrix = pd.read_csv('./Unit_Matchup_Matrix.csv', index_col=0)

def evaluate_best_counter(unit_credits, matchup_matrix):
    results = {}
    print("\n---- Running evaluate_best_counter ----")
    print("Enemy units and credits:")
    for unit, credits in unit_credits:
        print(f"  {unit}: {credits} credits")

    for candidate_unit in matchup_matrix.index:
        total = 0
        print(f"\nEvaluating {candidate_unit} against enemy units:")
        for enemy_unit, credits in unit_credits:
            try:
                matchup_value = int(matchup_matrix.loc[candidate_unit, enemy_unit])
                print(f"  vs {enemy_unit}: matchup value = {matchup_value}, weighted = {matchup_value * credits}")
                total += matchup_value * credits
            except KeyError:
                print(f"  [!] KeyError: {candidate_unit} vs {enemy_unit} not found in matrix.")
                continue
        results[candidate_unit] = total
        print(f"  Total score for {candidate_unit}: {total}")

    best_unit = max(results, key=results.get)
    print(f"\n>> Best unit: {best_unit} with score: {results[best_unit]}")
    return best_unit, results[best_unit]


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

        self.unit_sections = []  # ✅ Declare this list to track UnitSection objects
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Unit Counter Tool")
        self.setStyleSheet("background-color: #0b0c10; color: #66fcf1; font-size: 16px;")

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.unit_sections_container = QVBoxLayout()
        self.main_layout.addLayout(self.unit_sections_container)

        self.add_unit_section()

        add_button = QPushButton("+ Add Unit")
        add_button.setStyleSheet("background-color: #1f2833; color: #66fcf1; font-size: 16px;")
        add_button.clicked.connect(self.add_unit_section)
        self.main_layout.addWidget(add_button)

        remove_button = QPushButton("- Remove Unit")
        remove_button.setStyleSheet("background-color: #1f2833; color: #66fcf1; font-size: 16px;")
        remove_button.clicked.connect(self.remove_unit_section)
        self.main_layout.addWidget(remove_button)

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
        self.unit_sections.append(section)
        self.adjustSize()

    def remove_unit_section(self):
        if self.unit_sections:
            section = self.unit_sections.pop()
            section.setParent(None)  # This removes the widget from the layout
            self.adjustSize()

    def handle_counter_click(self):
        unit_credits = []
        print("---- Evaluating Counter ----")
        for section in self.unit_sections:
            unit = section.unit_dropdown.currentText()
            credits = section.credits_input.value()
            unit_credits.append((unit, credits))
            print(f"Unit: {unit}, Credits: {credits}")

        if not unit_credits:
            print("No units to evaluate.")
            self.result_label.setText("Please add units to evaluate.")
            return

        print("Running evaluate_best_counter...")
        best_unit, total_score = evaluate_best_counter(unit_credits, matchup_matrix)
        print(f"Best Unit: {best_unit}, Score: {total_score}")

        self.result_label.setText(f"Suggested Unit: {best_unit}")

        image_path = f"./mechabellum units/{best_unit}.jpg"
        print(f"Looking for image at: {image_path}")

        if os.path.exists(image_path):
            print("Image found.")
            pixmap = QPixmap(image_path).scaled(
                self.image_label.width(),
                self.image_label.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(pixmap)
            self.image_label.setText("")
        else:
            print("Image not found.")
            self.image_label.setPixmap(QPixmap())  # Clear old image
            self.image_label.setText("Image not found")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TechThemeUI()
    window.show()
    sys.exit(app.exec())
