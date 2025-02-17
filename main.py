# === Qt widget ===
# Simple Qt python app
# Author: Otto Nilsson
# Created: 2024-08


### Imports ###
import sys
from dataclasses import dataclass
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QWidget, QMainWindow, QDialog, QMessageBox,
                                QFrame, QGridLayout, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy,
                                QLabel, QPushButton, QLineEdit, QTextEdit, QCheckBox, QRadioButton, QButtonGroup)
from PySide6.QtGui import QIcon, QFont
import logging


### Logging ###
logging.basicConfig(
    level=logging.INFO,
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%H:%M:%S"
    )


### Global settings ###
@dataclass
class Settings:
    enable_modifier: bool = False
    modifier_type: str = "None"


### Global variables ###
app_name = "Qt widget"
app_ver = "1.0"
author = "Otto Nilsson"
date = "2024-08"
app_icon = r'./assets/Qt_icon_256x256.png'
settings = Settings()


### Main window ###
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt widget")
        self.setMinimumSize(400, 500)


        ## Menu bar ##
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        self.about_menu = self.menu.addMenu("About")

        # Menu actions
        self.settings_action = self.file_menu.addAction("Settings", self.create_settings_win)
        self.exit_action = self.file_menu.addAction("Exit", self.close)
        self.about_action = self.about_menu.addAction(f"About {app_name}", self.create_about_win)


        ## Widgets ##
        # Input label
        self.input_label = QLabel()
        self.input_label.setText("Input")
        self.input_label.setStyleSheet("text-decoration: underline")

        # Input field
        self.input_field = QLineEdit()
        self.input_field.textChanged.connect(self.enable_enter_button)
        self.input_field.returnPressed.connect(self.enter)

        # Enter button
        self.enter_button = QPushButton()
        self.enter_button.setText("Enter")
        self.enter_button.clicked.connect(self.enter)
        self.enable_enter_button()

        # Horizontal line
        self.h_line = QFrame()
        self.h_line.setFrameShape(QFrame.Shape.HLine)
        self.h_line.setFrameShadow(QFrame.Shadow.Sunken)

        # Modifier status label
        self.modifier_status_label = QLabel()
        self.modifier_status_label.setText(f'Modifier: {self.modifier_status()}')

        # Output label
        self.output_label = QLabel()
        self.output_label.setText("Output")
        self.output_label.setStyleSheet("text-decoration: underline")

        # Output field
        self.output_field = QTextEdit()
        self.output_field.textChanged.connect(self.enable_clear_button)
        self.output_field.setReadOnly(True)
        
        # Clear button
        self.clear_button = QPushButton()
        self.clear_button.setText("Clear")
        self.clear_button.clicked.connect(self.clear)
        self.clear_button.setMinimumHeight(self.clear_button.sizeHint().height() * 2)
        self.enable_clear_button()


        ## Layout ##
        self.g_layout = QGridLayout()
        self.g_layout.addWidget(self.input_label, 0, 0)
        self.g_layout.addWidget(self.input_field, 1, 0)
        self.g_layout.addWidget(self.enter_button, 1, 1)
        self.g_layout.addWidget(self.h_line, 2, 0, 1, 2)
        self.g_layout.addWidget(self.modifier_status_label, 3, 0)
        self.g_layout.addWidget(self.output_label, 4, 0)
        self.g_layout.addWidget(self.output_field, 5, 0, 1, 2)
        self.g_layout.addWidget(self.clear_button, 6, 0, 1, 2)
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.g_layout)
        self.setCentralWidget(self.centralWidget)


    ## Main window methods ##
    def closeEvent(self, event):
        logging.info('App closed by user')
        event.accept()

    def enter(self):
        text = self.input_field.text()
        logging.debug(f'Text entered: {text}')

        if text:
            if settings.enable_modifier:
                match settings.modifier_type:
                    case "None":
                        self.output_field.append(text)
                    case "Uppercase":
                        text = self.uppercase(text)
                        self.output_field.append(text)
                    case "Togglecase":
                        text = self.togglecase(text)
                        self.output_field.append(text)
                    case "Reverse":
                        text = self.reverse(text)
                        self.output_field.append(text)
            else:
                self.output_field.append(text)

        self.input_field.clear()
    
    def enable_enter_button(self):
        self.enter_button.setEnabled(bool(self.input_field.text()))

    def modifier_status(self):
        if settings.enable_modifier:
            return settings.modifier_type
        else:
             return "Disabled"

    def clear(self):
        if not self.output_field.document().isEmpty():
            self.output_field.clear()
    
    def enable_clear_button(self):
        self.clear_button.setEnabled(not self.output_field.document().isEmpty())

    def create_settings_win(self):
        settings_win = SettingsWin(self)
        settings_win.setWindowTitle("Settings")
        settings_win.setFixedSize(300, 200)
        settings_win.exec()
        
    def create_about_win(self):
        about_win = AboutWin()
        about_win.setWindowTitle("About")
        about_win.setFixedSize(400, 250)
        about_win.exec()

    def settings_saved(self):
        logging.info('Settings saved')
        logging.debug(f'Modifiers enabled: {settings.enable_modifier}')
        logging.debug(f'Modifier selected: {settings.modifier_type}')
        self.modifier_status_label.setText(f'Modifier: {self.modifier_status()}')
    
    def popup(self):
        QMessageBox.information(self, "Popup", "Message")

    # Text modifiers
    def uppercase(self, text):
        return text.upper()
    
    def togglecase(self, text):
        return text.swapcase()
    
    def reverse(self, text):
        return text[::-1]


### Settings window ###
class SettingsWin(QDialog):
    def __init__(self, parent):
        super().__init__()
        logging.info('Settings window opened')


        ## General ##
        self.parent = parent
        self.finished.connect(self.save)

        self.rb_group = QButtonGroup()


        ## Widgets ##
        self.label1 = QLabel()
        self.label1.setText("Output text modifiers")
        self.label1.setStyleSheet("text-decoration: underline")
        self.label1.setAlignment(Qt.AlignTop)

        # Activate modifiers
        self.cb_enable_modifier = QCheckBox("Activate modifiers")
        self.cb_enable_modifier.stateChanged.connect(self.toggle_rb_group)
        self.cb_enable_modifier.setChecked(settings.enable_modifier)
        
        # Output modifiers

        self.rb_default = QRadioButton("None")
        self.rb_group.addButton(self.rb_default)

        self.rb_uppercase = QRadioButton("Uppercase")
        self.rb_group.addButton(self.rb_uppercase)

        self.rb_togglecase = QRadioButton("Togglecase")
        self.rb_group.addButton(self.rb_togglecase)

        self.rb_reverse = QRadioButton("Reverse")
        self.rb_group.addButton(self.rb_reverse)

        self.check_rb()

        self.rb_group.buttonClicked.connect(self.rb_handler)
        self.toggle_rb_group()

    
        ## Layout ##
        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.label1)
        self.v_layout.addWidget(self.cb_enable_modifier)
        self.v_layout.addSpacerItem(QSpacerItem(0, 20))
        self.v_layout.addWidget(self.rb_default)
        self.v_layout.addWidget(self.rb_uppercase)
        self.v_layout.addWidget(self.rb_togglecase)
        self.v_layout.addWidget(self.rb_reverse)
        self.setLayout(self.v_layout)


    ## Settings window methods ##
    def check_rb(self):
        match settings.modifier_type:
            case "None":
                self.rb_default.setChecked(True)
            case "Uppercase":
                self.rb_uppercase.setChecked(True)
            case "Togglecase":
                self.rb_togglecase.setChecked(True)
            case "Reverse":
                self.rb_reverse.setChecked(True)

    def toggle_rb_group(self):
        settings.enable_modifier = self.cb_enable_modifier.isChecked()
        logging.debug(f'Modifiers enabled: {settings.enable_modifier}')
        for btn in self.rb_group.buttons():
            btn.setEnabled(settings.enable_modifier)
    
    def rb_handler(self, rb):
        settings.modifier_type = rb.text()
        logging.debug(settings.modifier_type)

    def save(self):
        logging.debug("Settings window closed")
        self.parent.settings_saved()


### About window ###
class AboutWin(QDialog):
    def __init__(self):
        super().__init__()
        logging.info('About window opened')


        ## Widgets ##
        # Heading
        self.label1 = QLabel()
        self.label1.setText(app_name)
        self.label1.setAlignment(Qt.AlignCenter)
        self.font = QFont()
        self.font.setPointSize(16)
        self.font.setBold(True)
        self.label1.setFont(self.font)

        # Version label
        self.label2 = QLabel()
        self.label2.setText(f'v {app_ver}')
        self.label2.setAlignment(Qt.AlignCenter)

        # Sub heading
        self.label3 = QLabel()
        self.label3.setText(f'{author}\n{date}')
        self.label3.setAlignment(Qt.AlignCenter)

        # Text field
        self.text_box = QLabel()
        self.text = open('./data/about.txt').read()
        self.text_box.setText(self.text)
        self.text_box.setWordWrap(True)
        self.text_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)


        ## Layout ##
        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.label1)
        self.v_layout.addWidget(self.label2)
        self.v_layout.addWidget(self.label3)
        self.v_layout.addSpacerItem(QSpacerItem(0, 20))
        self.h_layout = QHBoxLayout()
        self.h_layout.addSpacerItem(QSpacerItem(20, 0))
        self.h_layout.addWidget(self.text_box)
        self.h_layout.addSpacerItem(QSpacerItem(20, 0))
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addSpacerItem(QSpacerItem(0, 20))
        self.setLayout(self.v_layout)


### App entry point ###
if __name__ == "__main__":
    logging.info(f'{app_name} - v {app_ver}')
    logging.info('App started')
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(app_icon))
    window = MainWindow()
    window.resize(500, 500)
    window.show()

    sys.exit(app.exec())