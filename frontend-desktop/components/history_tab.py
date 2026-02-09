"""
History Tab for PyQt5 Desktop Application
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, 
    QTableWidgetItem, QGroupBox, QHeaderView, QMessageBox, QFileDialog, QLabel
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor
from datetime import datetime

class HistoryTab(QWidget):
    dataset_selected = pyqtSignal(int)
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.current_history = []
        self.selected_dataset_id = None
        
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        """Initialize the UI components"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # History table
        history_group = QGroupBox("Upload History")
        history_layout = QVBoxLayout()
        
        # Create table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(7)
        self.history_table.setHorizontalHeaderLabels([
            "Filename", "Upload Date", "Equipment Count", 
            "Avg Flowrate", "Avg Pressure", "Avg Temperature", "Actions"
        ])
        
        # Configure table
        header = self.history_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.history_table.setSortingEnabled(True)
        self.history_table.itemSelectionChanged.connect(self.on_selection_changed)
        
        history_layout.addWidget(self.history_table)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        
        self.load_button = QPushButton("Load Dataset")
        self.load_button.clicked.connect(self.load_selected_dataset)
        self.load_button.setEnabled(False)
        
        self.pdf_button = QPushButton("Download PDF")
        self.pdf_button.clicked.connect(self.download_pdf)
        self.pdf_button.setEnabled(False)
        
        buttons_layout.addWidget(self.load_button)
        buttons_layout.addWidget(self.pdf_button)
        buttons_layout.addStretch()
        
        history_layout.addLayout(buttons_layout)
        history_group.setLayout(history_layout)
        layout.addWidget(history_group)
        
        # Info label
        self.info_label = QLabel("Select a dataset from the history to load it or generate a PDF report.")
        self.info_label.setStyleSheet("color: #666; font-style: italic; padding: 10px;")
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def apply_styles(self):
        """Apply custom styles to the tab"""
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #2c3e50;
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
                color: #2c3e50;
                background-color: white;
            }
            QTableWidget::item:selected {
                background-color: #007bff;
                color: white;
            }
            QHeaderView::section {
                background-color: #667eea;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QHeaderView::section:horizontal {
                background-color: #667eea;
                color: white;
                border: 1px solid #5a67d8;
            }
            QHeaderView::section:vertical {
                background-color: #f8f9fa;
                color: #2c3e50;
                border: 1px solid #dee2e6;
                width: 30px;
            }
        """)
    
    def update_history(self, history):
        """Update the history table with new data"""
        self.current_history = history
        
        self.history_table.setRowCount(len(history))
        
        for row, item in enumerate(history):
            # Filename
            filename_item = QTableWidgetItem(item.get('filename', ''))
            self.history_table.setItem(row, 0, filename_item)
            
            # Upload Date
            upload_date = item.get('upload_timestamp', '')
            if upload_date:
                try:
                    # Parse ISO datetime and format
                    dt = datetime.fromisoformat(upload_date.replace('Z', '+00:00'))
                    formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    formatted_date = upload_date
            else:
                formatted_date = ''
            
            date_item = QTableWidgetItem(formatted_date)
            self.history_table.setItem(row, 1, date_item)
            
            # Equipment Count
            count_item = QTableWidgetItem(str(item.get('total_count', 0)))
            count_item.setTextAlignment(Qt.AlignCenter)
            self.history_table.setItem(row, 2, count_item)
            
            # Average Flowrate
            flowrate_item = QTableWidgetItem(f"{item.get('avg_flowrate', 0):.2f}")
            flowrate_item.setTextAlignment(Qt.AlignCenter)
            self.history_table.setItem(row, 3, flowrate_item)
            
            # Average Pressure
            pressure_item = QTableWidgetItem(f"{item.get('avg_pressure', 0):.2f}")
            pressure_item.setTextAlignment(Qt.AlignCenter)
            self.history_table.setItem(row, 4, pressure_item)
            
            # Average Temperature
            temp_item = QTableWidgetItem(f"{item.get('avg_temperature', 0):.2f}")
            temp_item.setTextAlignment(Qt.AlignCenter)
            self.history_table.setItem(row, 5, temp_item)
            
            # Actions button
            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(5, 2, 5, 2)
            
            load_btn = QPushButton("Load")
            load_btn.setStyleSheet("""
                QPushButton {
                    background-color: #28a745;
                    color: white;
                    border: none;
                    padding: 4px 8px;
                    border-radius: 3px;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #218838;
                }
            """)
            load_btn.clicked.connect(lambda checked, rid=item.get('id'): self.load_dataset(rid))
            
            pdf_btn = QPushButton("PDF")
            pdf_btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    border: none;
                    padding: 4px 8px;
                    border-radius: 3px;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #c82333;
                }
            """)
            pdf_btn.clicked.connect(lambda checked, rid=item.get('id'): self.generate_pdf(rid))
            
            actions_layout.addWidget(load_btn)
            actions_layout.addWidget(pdf_btn)
            actions_widget.setLayout(actions_layout)
            
            self.history_table.setCellWidget(row, 6, actions_widget)
        
        # Adjust row heights
        self.history_table.resizeRowsToContents()
        
        # Update info label
        if len(history) == 0:
            self.info_label.setText("No upload history available.")
        else:
            self.info_label.setText(f"Showing {len(history)} recent uploads. Click 'Load' to view a dataset or 'PDF' to download a report.")
    
    def on_selection_changed(self):
        """Handle table selection change"""
        selected_items = self.history_table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            if row < len(self.current_history):
                self.selected_dataset_id = self.current_history[row].get('id')
                self.load_button.setEnabled(True)
                self.pdf_button.setEnabled(True)
            else:
                self.load_button.setEnabled(False)
                self.pdf_button.setEnabled(False)
        else:
            self.selected_dataset_id = None
            self.load_button.setEnabled(False)
            self.pdf_button.setEnabled(False)
    
    def load_selected_dataset(self):
        """Load the currently selected dataset"""
        if self.selected_dataset_id:
            self.load_dataset(self.selected_dataset_id)
    
    def load_dataset(self, dataset_id):
        """Load a specific dataset"""
        self.dataset_selected.emit(dataset_id)
        QMessageBox.information(self, "Dataset Loaded", f"Dataset {dataset_id} has been loaded.")
    
    def download_pdf(self):
        """Download PDF for selected dataset"""
        if self.selected_dataset_id:
            self.generate_pdf(self.selected_dataset_id)
    
    def generate_pdf(self, dataset_id):
        """Generate PDF for a specific dataset"""
        # Ask for save location
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF Report",
            f"equipment_report_{dataset_id}.pdf",
            "PDF Files (*.pdf)"
        )
        
        if file_path:
            try:
                # Show progress dialog
                from PyQt5.QtWidgets import QProgressDialog
                progress = QProgressDialog("Generating PDF report...", None, 0, 0, self)
                progress.setWindowModality(Qt.WindowModal)
                progress.show()
                
                # Download PDF
                success, error = self.api_client.download_pdf(dataset_id, file_path)
                
                progress.close()
                
                if success:
                    QMessageBox.information(self, "Success", f"PDF report saved to:\n{file_path}")
                else:
                    QMessageBox.critical(self, "Error", f"Failed to generate PDF:\n{error}")
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred:\n{str(e)}")
