"""
Data View Tab for PyQt5 Desktop Application
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QTableWidget, QTableWidgetItem, QGroupBox, QFileDialog,
    QMessageBox, QProgressDialog, QHeaderView, QApplication
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor

class UploadThread(QThread):
    """Thread for handling file upload to avoid UI freezing"""
    upload_complete = pyqtSignal(bool, dict, str)
    
    def __init__(self, api_client, file_path):
        super().__init__()
        self.api_client = api_client
        self.file_path = file_path
    
    def run(self):
        success, data, error = self.api_client.upload_csv(self.file_path)
        self.upload_complete.emit(success, data, error)

class DataViewTab(QWidget):
    data_updated = pyqtSignal()
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.current_summary = {}
        self.current_equipment = []
        
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Upload section
        upload_group = QGroupBox("File Upload")
        upload_layout = QVBoxLayout()
        
        upload_button_layout = QHBoxLayout()
        self.upload_button = QPushButton("Upload CSV File")
        self.upload_button.clicked.connect(self.upload_csv)
        upload_button_layout.addWidget(self.upload_button)
        upload_button_layout.addStretch()
        
        upload_layout.addLayout(upload_button_layout)
        upload_group.setLayout(upload_layout)
        layout.addWidget(upload_group)
        
        # Summary statistics section
        self.summary_group = QGroupBox("Summary Statistics")
        summary_layout = QVBoxLayout()
        
        self.summary_labels = {}
        summary_items = [
            ("Total Equipment:", "total_count", "items"),
            ("Average Flowrate:", "avg_flowrate", "L/min"),
            ("Average Pressure:", "avg_pressure", "bar"),
            ("Average Temperature:", "avg_temperature", "°C")
        ]
        
        for label_text, key, unit in summary_items:
            item_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setFont(QFont("Arial", 10, QFont.Bold))
            value_label = QLabel("0")
            value_label.setStyleSheet("color: #007bff; font-size: 14px; font-weight: bold;")
            unit_label = QLabel(unit)
            unit_label.setStyleSheet("color: #666; font-size: 12px;")
            
            item_layout.addWidget(label)
            item_layout.addWidget(value_label)
            item_layout.addWidget(unit_label)
            item_layout.addStretch()
            
            self.summary_labels[key] = value_label
            summary_layout.addLayout(item_layout)
        
        self.summary_group.setLayout(summary_layout)
        layout.addWidget(self.summary_group)
        
        # Equipment table
        table_group = QGroupBox("Equipment Data")
        table_layout = QVBoxLayout()
        
        self.equipment_table = QTableWidget()
        self.equipment_table.setColumnCount(5)
        self.equipment_table.setHorizontalHeaderLabels([
            "Equipment Name", "Type", "Flowrate (L/min)", 
            "Pressure (bar)", "Temperature (°C)"
        ])
        
        # Configure table
        header = self.equipment_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        self.equipment_table.setAlternatingRowColors(True)
        self.equipment_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.equipment_table.setSortingEnabled(True)
        
        table_layout.addWidget(self.equipment_table)
        table_group.setLayout(table_layout)
        layout.addWidget(table_group)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def apply_styles(self):
        """Apply custom styles to the tab"""
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QTableWidget {
                gridline-color: #d0d0d0;
                background-color: white;
                alternate-background-color: #f9f9f9;
            }
            QTableWidget::item {
                padding: 5px;
                color: black;  /* Force black text for all items */
            }
            QTableWidget::item:selected {
                background-color: #007bff;
                color: white;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 5px;
                border: 1px solid #d0d0d0;
                font-weight: bold;
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
            self.upload_button.setEnabled(False)
            self.upload_button.setText("Uploading...")
            
            # Show progress dialog
            progress = QProgressDialog("Uploading and processing file...", None, 0, 0, self)
            progress.setWindowModality(Qt.WindowModal)
            progress.show()
            
            # Start upload thread
            self.upload_thread = UploadThread(self.api_client, file_path)
            self.upload_thread.upload_complete.connect(
                lambda success, data, error: self.on_upload_complete(success, data, error, progress)
            )
            self.upload_thread.start()
    
    def on_upload_complete(self, success, data, error, progress_dialog):
        """Handle upload completion"""
        progress_dialog.close()
        self.upload_button.setEnabled(True)
        self.upload_button.setText("Upload CSV File")
        
        if success:
            QMessageBox.information(self, "Upload Success", data.get('message', 'File uploaded successfully!'))
            self.data_updated.emit()
        else:
            QMessageBox.critical(self, "Upload Error", error)
    
    def update_data(self, summary, equipment):
        """Update the tab with new data"""
        self.current_summary = summary
        self.current_equipment = equipment
        
        # Update summary labels
        if summary:
            self.summary_labels['total_count'].setText(str(summary.get('total_count', 0)))
            self.summary_labels['avg_flowrate'].setText(f"{summary.get('avg_flowrate', 0):.2f}")
            self.summary_labels['avg_pressure'].setText(f"{summary.get('avg_pressure', 0):.2f}")
            self.summary_labels['avg_temperature'].setText(f"{summary.get('avg_temperature', 0):.2f}")
        else:
            for label in self.summary_labels.values():
                label.setText("0")
        
        # Update equipment table
        self.equipment_table.setRowCount(len(equipment))
        
        for row, item in enumerate(equipment):
            # Equipment Name
            self.equipment_table.setItem(row, 0, QTableWidgetItem(item.get('equipment_name', '')))
            
            # Type
            type_item = QTableWidgetItem(item.get('type', ''))
            type_item.setBackground(self.get_type_color(item.get('type', '')))
            type_item.setForeground(QColor(0, 0, 0, 0))  # Black text for colored background
            self.equipment_table.setItem(row, 1, type_item)
            
            # Flowrate
            flowrate_item = QTableWidgetItem(f"{item.get('flowrate', 0):.1f}")
            self.equipment_table.setItem(row, 2, flowrate_item)
            
            # Pressure
            pressure_item = QTableWidgetItem(f"{item.get('pressure', 0):.1f}")
            self.equipment_table.setItem(row, 3, pressure_item)
            
            # Temperature
            temp_item = QTableWidgetItem(f"{item.get('temperature', 0):.1f}")
            self.equipment_table.setItem(row, 4, temp_item)
        
        # Adjust row heights
        self.equipment_table.resizeRowsToContents()
    
    def get_type_color(self, equipment_type):
        """Get background color for equipment type"""
        
        colors = {
            'Reactor': QColor(0, 123, 255, 50),      # Blue
            'Pump': QColor(40, 167, 69, 50),        # Green
            'Heat Exchanger': QColor(255, 193, 7, 50), # Yellow
            'Compressor': QColor(220, 53, 69, 50),   # Red
            'Valve': QColor(108, 117, 125, 50)       # Gray
        }
        return colors.get(equipment_type, QColor(200, 200, 200, 50))
