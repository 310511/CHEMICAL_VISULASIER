"""
Main Window for PyQt5 Desktop Application
"""

import sys
import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QMenuBar, QMenu, QAction, QStatusBar, QMessageBox, QFileDialog,
    QProgressDialog, QApplication
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QFont

from .api_client import APIClient
from .data_view_tab import DataViewTab
from .analytics_tab import AnalyticsTab
from .history_tab import HistoryTab

class DataRefreshThread(QThread):
    """Thread for refreshing data to avoid UI freezing"""
    data_ready = pyqtSignal(dict, list, list)  # summary, equipment, history
    error_occurred = pyqtSignal(str)
    
    def __init__(self, api_client, dataset_id=None):
        super().__init__()
        self.api_client = api_client
        self.dataset_id = dataset_id
    
    def run(self):
        try:
            success, summary, error = self.api_client.get_summary(self.dataset_id)
            if not success:
                self.error_occurred.emit(error)
                return
            
            success, equipment, error = self.api_client.get_equipment(self.dataset_id)
            if not success:
                self.error_occurred.emit(error)
                return
            
            success, history, error = self.api_client.get_history()
            if not success:
                self.error_occurred.emit(error)
                return
            
            self.data_ready.emit(summary, equipment, history)
            
        except Exception as e:
            self.error_occurred.emit(f"Unexpected error: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self, token: str, username: str, parent=None):
        super().__init__(parent)
        self.token = token
        self.username = username
        self.api_client = APIClient()
        self.api_client.set_token(token)
        
        self.current_dataset_id = None
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_data)
        
        self.init_ui()
        self.apply_styles()
        self.refresh_data()
        
        # Auto-refresh every 30 seconds
        self.refresh_timer.start(30000)
    
    def init_ui(self):
        """Initialize UI components with modern styling"""
        self.setWindowTitle(" Chemical Equipment Visualizer v2.0")
        self.setGeometry(100, 100, 1400, 900)
        
        # Set modern application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                background-color: #ffffff;
                border-top: none;
            }
            
            QTabWidget::tab-bar {
                background: linear-gradient(135deg, #667eea, #764ba2);
                border: none;
                border-bottom: 2px solid #667eea;
            }
            
            QTabWidget::tab {
                background-color: transparent;
                color: rgba(255, 255, 255, 0.7);
                padding: 12px 24px;
                margin-right: 2px;
                border: none;
                font-weight: 600;
                min-width: 120px;
            }
            
            QTabWidget::tab:selected {
                background-color: #667eea;
                color: white;
                border-radius: 8px 8px 0 0;
            }
            
            QTabWidget::tab:hover {
                background-color: rgba(102, 126, 234, 0.1);
                color: white;
            }
            
            QMenuBar {
                background: linear-gradient(135deg, #2c3e50, #343a40);
                color: white;
                border: none;
                font-weight: 600;
                padding: 4px 0px;
            }
            
            QMenuBar::item {
                background-color: transparent;
                padding: 8px 16px;
                border-radius: 4px;
                margin: 2px;
            }
            
            QMenuBar::item:selected {
                background-color: #667eea;
                color: white;
            }
            
            QMenuBar::item:hover {
                background-color: rgba(102, 126, 234, 0.2);
                color: white;
            }
            
            QStatusBar {
                background: linear-gradient(135deg, #2c3e50, #343a40);
                color: white;
                border: none;
                font-weight: 500;
                padding: 8px 16px;
            }
            
            QStatusBar::item {
                background-color: transparent;
                border: none;
                padding: 4px 8px;
                border-radius: 4px;
            }
            
            QPushButton {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: 600;
                font-size: 13px;
                min-width: 100px;
            }
            
            QPushButton:hover {
                background: linear-gradient(135deg, #5a67d8, #667eea);
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            }
            
            QPushButton:pressed {
                background: linear-gradient(135deg, #764ba2, #5a67d8);
                transform: translateY(1px);
            }
            
            QPushButton:disabled {
                background-color: #6c757d;
                color: rgba(255, 255, 255, 0.5);
            }
            
            QGroupBox {
                font-weight: 600;
                color: #2c3e50;
                border: 2px solid #dee2e6;
                border-radius: 12px;
                margin-top: 16px;
                padding-top: 16px;
                background-color: white;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px;
                border-bottom: 2px solid #dee2e6;
            }
            
            QTableWidget {
                gridline-color: #e9ecef;
                background-color: white;
                alternate-background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 12px;
                selection-background-color: #667eea;
            }
            
            QTableWidget::item {
                padding: 8px;
                border: none;
                color: #2c3e50;
            }
            
            QTableWidget::item:selected {
                background-color: #667eea;
                color: white;
            }
            
            QHeaderView::section {
                background-color: #667eea;
                color: white;
                padding: 12px 8px;
                border: none;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            QProgressDialog {
                background-color: white;
                border: 2px solid #667eea;
                border-radius: 12px;
                padding: 20px;
            }
            
            QMessageBox {
                background-color: white;
                border: 2px solid #667eea;
                border-radius: 12px;
                padding: 20px;
            }
            
            QMessageBox QPushButton {
                background-color: #667eea;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
            }
            
            QMessageBox QPushButton:hover {
                background-color: #5a67d8;
            }
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(False)
        
        # Create tabs with enhanced styling
        self.data_view_tab = DataViewTab(self.api_client)
        self.analytics_tab = AnalyticsTab(self.api_client)
        self.history_tab = HistoryTab(self.api_client)
        
        # Add tabs to widget with icons
        self.tab_widget.addTab(self.data_view_tab, " Data View")
        self.tab_widget.addTab(self.analytics_tab, " Analytics")
        self.tab_widget.addTab(self.history_tab, " History")
        
        # Add tab widget to main layout
        main_layout.addWidget(self.tab_widget)
        
        # Connect tab signals
        self.data_view_tab.data_updated.connect(self.on_data_updated)
        self.history_tab.dataset_selected.connect(self.on_dataset_selected)
        
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(f"Logged in as: {self.username}")
    
    def create_menu_bar(self):
        """Create the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        upload_action = QAction('Upload CSV', self)
        upload_action.setShortcut('Ctrl+U')
        upload_action.triggered.connect(self.upload_csv)
        file_menu.addAction(upload_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu('View')
        
        refresh_action = QAction('Refresh', self)
        refresh_action.setShortcut('F5')
        refresh_action.triggered.connect(self.refresh_data)
        view_menu.addAction(refresh_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def apply_styles(self):
        """Apply custom styles to the main window"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #c0c0c0;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #007bff;
            }
            QTabBar::tab:hover {
                background-color: #d0d0d0;
            }
        """)
    
    def upload_csv(self):
        """Handle CSV file upload"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv)"
        )
        
        if file_path:
            self.status_bar.showMessage("Uploading file...")
            
            # Show progress dialog
            progress = QProgressDialog("Uploading and processing file...", "Cancel", 0, 0, self)
            progress.setWindowModality(Qt.WindowModal)
            progress.show()
            
            # Upload file in a separate thread
            class UploadThread(QThread):
                upload_complete = pyqtSignal(bool, dict, str)
                
                def __init__(self, api_client, file_path):
                    super().__init__()
                    self.api_client = api_client
                    self.file_path = file_path
                
                def run(self):
                    success, data, error = self.api_client.upload_csv(self.file_path)
                    self.upload_complete.emit(success, data, error)
            
            upload_thread = UploadThread(self.api_client, file_path)
            upload_thread.upload_complete.connect(lambda success, data, error: self.on_upload_complete(success, data, error, progress))
            upload_thread.start()
    
    def on_upload_complete(self, success, data, error, progress_dialog):
        """Handle upload completion"""
        progress_dialog.close()
        
        if success:
            self.current_dataset_id = data.get('dataset_id')
            self.refresh_data()
            self.status_bar.showMessage("File uploaded successfully!")
            QMessageBox.information(self, "Upload Success", data.get('message', 'File uploaded successfully!'))
        else:
            self.status_bar.showMessage("Upload failed")
            QMessageBox.critical(self, "Upload Error", error)
    
    def refresh_data(self):
        """Refresh all data"""
        self.status_bar.showMessage("Refreshing data...")
        
        self.refresh_thread = DataRefreshThread(self.api_client, self.current_dataset_id)
        self.refresh_thread.data_ready.connect(self.on_data_refreshed)
        self.refresh_thread.error_occurred.connect(self.on_refresh_error)
        self.refresh_thread.start()
    
    def on_data_refreshed(self, summary, equipment, history):
        """Handle data refresh completion"""
        self.status_bar.showMessage("Data refreshed successfully")
        
        # Update all tabs with new data
        self.data_view_tab.update_data(summary, equipment)
        self.analytics_tab.update_data(summary, equipment)
        self.history_tab.update_history(history)
    
    def on_refresh_error(self, error):
        """Handle data refresh error"""
        self.status_bar.showMessage("Data refresh failed")
        QMessageBox.warning(self, "Refresh Error", f"Failed to refresh data: {error}")
    
    def on_data_updated(self):
        """Handle data update from data view tab"""
        self.refresh_data()
    
    def on_dataset_selected(self, dataset_id):
        """Handle dataset selection from history tab"""
        self.current_dataset_id = dataset_id
        self.refresh_data()
        self.tab_widget.setCurrentIndex(0)  # Switch to Data View tab
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
        <h3>Chemical Equipment Visualizer</h3>
        <p>Version 1.0</p>
        <p>A desktop application for visualizing and analyzing chemical equipment data.</p>
        <p><b>Features:</b></p>
        <ul>
            <li>CSV file upload and processing</li>
            <li>Interactive data visualization</li>
            <li>Statistical analysis</li>
            <li>PDF report generation</li>
            <li>Upload history tracking</li>
        </ul>
        <p><b>Tech Stack:</b></p>
        <ul>
            <li>PyQt5 for GUI</li>
            <li>Matplotlib for charts</li>
            <li>Requests for API communication</li>
            <li>Pandas for data processing</li>
        </ul>
        """
        
        QMessageBox.about(self, "About", about_text)
    
    def closeEvent(self, event):
        """Handle application close event"""
        # Stop refresh timer
        self.refresh_timer.stop()
        
        # Logout from server
        try:
            self.api_client.logout()
        except:
            pass  # Ignore logout errors
        
        event.accept()
