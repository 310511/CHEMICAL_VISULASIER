#!/usr/bin/env python3
"""
Chemical Equipment Visualizer - Desktop Application
Main entry point for the PyQt5 desktop application
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

# Add current directory and components to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'components'))

from components.login_dialog import LoginDialog
from components.main_window import MainWindow

def main():
    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("Chemical Equipment Visualizer")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Chemical Equipment Visualizer")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Set application icon (if available)
    try:
        app.setWindowIcon(QIcon('icon.png'))
    except:
        pass  # Icon file not available, continue without it
    
    # Show login dialog first
    login_dialog = LoginDialog()
    
    if login_dialog.exec_() == LoginDialog.Accepted:
        # Login successful, show main window
        token = login_dialog.get_token()
        username = login_dialog.get_username()
        
        main_window = MainWindow(token, username)
        main_window.show()
        
        sys.exit(app.exec_())
    else:
        # Login cancelled or failed
        sys.exit(0)

if __name__ == '__main__':
    main()
