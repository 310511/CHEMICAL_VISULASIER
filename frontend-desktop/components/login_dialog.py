"""
Login Dialog for PyQt5 Desktop Application
"""

import sys
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

from .api_client import APIClient

class LoginThread(QThread):
    """Thread for handling login to avoid UI freezing"""
    login_success = pyqtSignal(bool, str, str)  # success, token, error_message
    
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        self.api_client = APIClient()
    
    def run(self):
        success, token, error = self.api_client.login(self.username, self.password)
        self.login_success.emit(success, token, error)

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.token = None
        self.username = None
        self.login_thread = None
        
        self.setWindowTitle("Chemical Equipment Visualizer - Login")
        self.setFixedSize(400, 300)
        self.setWindowModality(Qt.ApplicationModal)
        
        # Center the dialog on screen
        self.center_on_screen()
        
        self.init_ui()
        self.apply_styles()
    
    def center_on_screen(self):
        """Center the dialog on the screen"""
        frame_geometry = self.frameGeometry()
        screen_center = self.screen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
    
    def init_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title_label = QLabel("Chemical Equipment Visualizer")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Please login to continue")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_font = QFont()
        subtitle_font.setPointSize(10)
        subtitle_label.setFont(subtitle_font)
        layout.addWidget(subtitle_label)
        
        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        
        # Username field
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        username_label.setFixedWidth(80)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)
        
        # Password field
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        password_label.setFixedWidth(80)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter password")
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)
        
        # Error message label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red; font-size: 12px;")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setWordWrap(True)
        layout.addWidget(self.error_label)
        
        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setFixedHeight(40)
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)
        
        # Test credentials info
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(10, 10, 10, 10)
        
        info_title = QLabel("Test Credentials:")
        info_title.setStyleSheet("font-weight: bold; color: #333;")
        info_layout.addWidget(info_title)
        
        info_user = QLabel("Username: admin")
        info_user.setStyleSheet("color: #666; font-size: 12px;")
        info_layout.addWidget(info_user)
        
        info_pass = QLabel("Password: admin123")
        info_pass.setStyleSheet("color: #666; font-size: 12px;")
        info_layout.addWidget(info_pass)
        
        info_frame.setLayout(info_layout)
        layout.addWidget(info_frame)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Connect return key to login
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
    
    def apply_styles(self):
        """Apply custom styles to the dialog"""
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: #333;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #007bff;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
            QPushButton:disabled {
                background-color: #ccc;
            }
        """)
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            self.error_label.setText("Please enter both username and password")
            return
        
        # Disable UI elements
        self.login_button.setEnabled(False)
        self.login_button.setText("Logging in...")
        self.username_input.setEnabled(False)
        self.password_input.setEnabled(False)
        self.error_label.setText("")
        
        # Start login thread
        self.login_thread = LoginThread(username, password)
        self.login_thread.login_success.connect(self.on_login_complete)
        self.login_thread.start()
    
    def on_login_complete(self, success, token, error_message):
        """Handle login completion"""
        # Re-enable UI elements
        self.login_button.setEnabled(True)
        self.login_button.setText("Login")
        self.username_input.setEnabled(True)
        self.password_input.setEnabled(True)
        
        if success:
            self.token = token
            self.username = self.username_input.text().strip()
            self.accept()
        else:
            self.error_label.setText(error_message)
            self.password_input.clear()
            self.password_input.setFocus()
    
    def get_token(self):
        """Get the authentication token"""
        return self.token
    
    def get_username(self):
        """Get the username"""
        return self.username
    
    def closeEvent(self, event):
        """Handle dialog close event"""
        if self.login_thread and self.login_thread.isRunning():
            self.login_thread.terminate()
            self.login_thread.wait()
        event.accept()
