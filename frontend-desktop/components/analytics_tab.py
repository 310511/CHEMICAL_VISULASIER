"""
Analytics Tab for PyQt5 Desktop Application
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox,
    QComboBox, QLabel, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class AnalyticsTab(QWidget):
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
        
        # Chart controls
        controls_group = QGroupBox("Chart Controls")
        controls_layout = QHBoxLayout()
        
        # Chart type selector
        chart_type_layout = QHBoxLayout()
        chart_type_label = QLabel("Chart Type:")
        chart_type_label.setStyleSheet("color: #2c3e50; font-size: 12px; font-weight: bold;")
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(["Bar Chart", "Line Chart"])
        self.chart_type_combo.currentTextChanged.connect(self.update_charts)
        
        chart_type_layout.addWidget(chart_type_label)
        chart_type_layout.addWidget(self.chart_type_combo)
        chart_type_layout.addStretch()
        
        # Download PDF button
        self.pdf_button = QPushButton("Download PDF Report")
        self.pdf_button.clicked.connect(self.download_pdf)
        
        controls_layout.addLayout(chart_type_layout)
        controls_layout.addWidget(self.pdf_button)
        controls_group.setLayout(controls_layout)
        layout.addWidget(controls_group)
        
        # Charts area
        charts_group = QGroupBox("Data Visualization")
        charts_layout = QVBoxLayout()
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(12, 8))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        charts_layout.addWidget(self.toolbar)
        charts_layout.addWidget(self.canvas)
        charts_group.setLayout(charts_layout)
        layout.addWidget(charts_group)
        
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
                background-color: #28a745;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
            QComboBox {
                border: 2px solid #dee2e6;
                border-radius: 6px;
                padding: 6px 12px;
                background-color: white;
                color: #2c3e50;
                font-size: 12px;
            }
            QComboBox:hover {
                border-color: #667eea;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #667eea;
                margin-right: 4px;
            }
        """)
    
    def update_data(self, summary, equipment):
        """Update the tab with new data"""
        self.current_summary = summary
        self.current_equipment = equipment
        self.update_charts()
    
    def update_charts(self):
        """Update the charts with current data"""
        if not self.current_summary or not self.current_equipment:
            self.figure.clear()
            self.canvas.draw()
            return
        
        self.figure.clear()
        
        chart_type = self.chart_type_combo.currentText()
        
        # Create subplots
        fig = self.figure
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        
        # Chart 1: Equipment Type Distribution
        type_dist = self.current_summary.get('type_distribution', {})
        if type_dist:
            types = list(type_dist.keys())
            counts = list(type_dist.values())
            
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
            
            if chart_type == "Bar Chart":
                ax1.bar(types, counts, color=colors[:len(types)])
                ax1.set_title('Equipment Type Distribution', fontweight='bold', fontsize=12)
                ax1.set_xlabel('Equipment Type')
                ax1.set_ylabel('Count')
                ax1.tick_params(axis='x', rotation=45)
            else:  # Line Chart
                ax1.plot(types, counts, marker='o', linewidth=2, markersize=8, color='#007bff')
                ax1.set_title('Equipment Type Distribution', fontweight='bold', fontsize=12)
                ax1.set_xlabel('Equipment Type')
                ax1.set_ylabel('Count')
                ax1.tick_params(axis='x', rotation=45)
                ax1.grid(True, alpha=0.3)
        
        # Chart 2: Average Parameters Comparison
        params = ['Flowrate', 'Pressure', 'Temperature']
        values = [
            self.current_summary.get('avg_flowrate', 0),
            self.current_summary.get('avg_pressure', 0),
            self.current_summary.get('avg_temperature', 0)
        ]
        
        if chart_type == "Bar Chart":
            bars = ax2.bar(params, values, color=['#007bff', '#28a745', '#dc3545'])
            ax2.set_title('Average Parameters', fontweight='bold', fontsize=12)
            ax2.set_ylabel('Average Value')
            
            # Add value labels on bars
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{value:.1f}', ha='center', va='bottom')
        else:  # Line Chart
            ax2.plot(params, values, marker='s', linewidth=2, markersize=8, color='#28a745')
            ax2.set_title('Average Parameters', fontweight='bold', fontsize=12)
            ax2.set_ylabel('Average Value')
            ax2.grid(True, alpha=0.3)
            
            # Add value labels
            for i, (param, value) in enumerate(zip(params, values)):
                ax2.annotate(f'{value:.1f}', (i, value), textcoords="offset points", 
                           xytext=(0,10), ha='center')
        
        # Adjust layout
        self.figure.tight_layout()
        self.canvas.draw()
    
    def download_pdf(self):
        """Download PDF report"""
        if not self.current_summary:
            QMessageBox.warning(self, "No Data", "No data available to generate report.")
            return
        
        # Ask for save location
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF Report",
            f"equipment_report.pdf",
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
                success, error = self.api_client.download_pdf(save_path=file_path)
                
                progress.close()
                
                if success:
                    QMessageBox.information(self, "Success", f"PDF report saved to:\n{file_path}")
                else:
                    QMessageBox.critical(self, "Error", f"Failed to generate PDF:\n{error}")
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred:\n{str(e)}")
