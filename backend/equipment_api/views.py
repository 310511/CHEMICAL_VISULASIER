import os
import csv
import io
from datetime import datetime
from django.http import HttpResponse
from django.db import transaction
from django.db.models import Avg, Count
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.files.uploadedfile import InMemoryUploadedFile
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import pandas as pd

from .models import Equipment, DatasetUpload
from .serializers import EquipmentSerializer, DatasetUploadSerializer


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """Login endpoint to authenticate user and return token"""
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Username and password are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': user.username
            })
        else:
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """Logout endpoint to delete user token"""
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Logged out successfully'})
    except Token.DoesNotExist:
        return Response({'message': 'Logged out successfully'})
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def upload_csv(request):
    """Upload CSV file and process equipment data"""
    try:
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        file = request.FILES['file']
        
        if not file.name.endswith('.csv'):
            return Response(
                {'error': 'File must be a CSV'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Read and validate CSV content
        try:
            # Read file content
            if isinstance(file, InMemoryUploadedFile):
                file.seek(0)
                content = file.read().decode('utf-8')
                file.seek(0)
            else:
                content = file.read().decode('utf-8')
            
            # Parse with pandas
            df = pd.read_csv(io.StringIO(content))
            
            # Validate required columns
            required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return Response(
                    {'error': f'Missing required columns: {", ".join(missing_columns)}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate equipment types (extract base type from names with suffixes)
            valid_types = ['Reactor', 'Pump', 'Heat Exchanger', 'HeatExchanger', 'Compressor', 'Valve', 'Condenser']
            
            def extract_base_type(equipment_name):
                """Extract base equipment type by removing common suffixes"""
                for valid_type in valid_types:
                    if equipment_name.startswith(valid_type):
                        return valid_type
                    # Also check for no-space version
                    if valid_type == 'Heat Exchanger' and equipment_name.startswith('HeatExchanger'):
                        return 'HeatExchanger'
                return equipment_name
            
            # Apply extraction to all equipment types
            df['BaseType'] = df['Type'].apply(extract_base_type)
            invalid_types = df[~df['BaseType'].isin(valid_types)]['Type'].unique()
            
            if len(invalid_types) > 0:
                return Response(
                    {'error': f'Invalid equipment types: {", ".join(invalid_types)}. Valid base types: {", ".join(valid_types)}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate data ranges
            if df['Flowrate'].min() < 10.5 or df['Flowrate'].max() > 500.0:
                return Response(
                    {'error': 'Flowrate values must be between 10.5 and 500.0 L/min'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if df['Pressure'].min() < 1.0 or df['Pressure'].max() > 150.0:
                return Response(
                    {'error': 'Pressure values must be between 1.0 and 150.0 bar'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if df['Temperature'].min() < 20.0 or df['Temperature'].max() > 350.0:
                return Response(
                    {'error': 'Temperature values must be between 20.0 and 350.0 °C'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        except Exception as e:
            return Response(
                {'error': f'Error parsing CSV: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            # Delete oldest dataset if more than 5 exist
            datasets = DatasetUpload.objects.all().order_by('upload_timestamp')
            if datasets.count() >= 5:
                oldest_dataset = datasets.first()
                Equipment.objects.filter(dataset=oldest_dataset).delete()
                oldest_dataset.delete()
            
            # Create dataset record
            type_counts = df['Type'].value_counts().to_dict()
            dataset = DatasetUpload.objects.create(
                filename=file.name,
                total_count=len(df),
                avg_flowrate=float(df['Flowrate'].mean()),
                avg_pressure=float(df['Pressure'].mean()),
                avg_temperature=float(df['Temperature'].mean()),
                type_distribution=type_counts
            )
            
            # Create equipment records
            equipment_list = []
            for _, row in df.iterrows():
                equipment_list.append(Equipment(
                    equipment_name=row['Equipment Name'],
                    type=row['BaseType'],  # Use extracted base type
                    flowrate=float(row['Flowrate']),
                    pressure=float(row['Pressure']),
                    temperature=float(row['Temperature']),
                    dataset=dataset
                ))
            
            Equipment.objects.bulk_create(equipment_list)
        
        # Return summary
        summary = {
            'total_count': dataset.total_count,
            'avg_flowrate': dataset.avg_flowrate,
            'avg_pressure': dataset.avg_pressure,
            'avg_temperature': dataset.avg_temperature,
            'type_distribution': dataset.type_distribution
        }
        
        return Response({
            'message': 'Upload successful',
            'dataset_id': dataset.id,
            'summary': summary
        })
        
    except Exception as e:
        return Response(
            {'error': f'Upload failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def equipment_list(request):
    """Get equipment list for a specific dataset or latest dataset"""
    try:
        dataset_id = request.GET.get('dataset_id')
        
        if dataset_id:
            try:
                dataset = DatasetUpload.objects.get(id=dataset_id)
                equipment = Equipment.objects.filter(dataset=dataset)
            except DatasetUpload.DoesNotExist:
                return Response(
                    {'error': 'Dataset not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Get latest dataset
            latest_dataset = DatasetUpload.objects.order_by('-upload_timestamp').first()
            if not latest_dataset:
                return Response([])
            equipment = Equipment.objects.filter(dataset=latest_dataset)
        
        serializer = EquipmentSerializer(equipment, many=True)
        return Response(serializer.data)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def summary_view(request):
    """Get analytics summary for a specific dataset or latest dataset"""
    try:
        dataset_id = request.GET.get('dataset_id')
        
        if dataset_id:
            try:
                dataset = DatasetUpload.objects.get(id=dataset_id)
            except DatasetUpload.DoesNotExist:
                return Response(
                    {'error': 'Dataset not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Get latest dataset
            dataset = DatasetUpload.objects.order_by('-upload_timestamp').first()
            if not dataset:
                return Response({
                    'total_count': 0,
                    'avg_flowrate': 0.0,
                    'avg_pressure': 0.0,
                    'avg_temperature': 0.0,
                    'type_distribution': {}
                })
        
        response_data = {
            'total_count': dataset.total_count,
            'avg_flowrate': dataset.avg_flowrate,
            'avg_pressure': dataset.avg_pressure,
            'avg_temperature': dataset.avg_temperature,
            'type_distribution': dataset.type_distribution
        }
        
        return Response(response_data)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def history_view(request):
    """Get last 5 upload records"""
    try:
        datasets = DatasetUpload.objects.order_by('-upload_timestamp')[:5]
        serializer = DatasetUploadSerializer(datasets, many=True)
        return Response(serializer.data)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def generate_pdf_report(request):
    """Generate PDF report for a specific dataset or latest dataset"""
    try:
        dataset_id = request.GET.get('dataset_id')
        
        if dataset_id:
            try:
                dataset = DatasetUpload.objects.get(id=dataset_id)
                equipment = Equipment.objects.filter(dataset=dataset)
            except DatasetUpload.DoesNotExist:
                return Response(
                    {'error': 'Dataset not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Get latest dataset
            latest_dataset = DatasetUpload.objects.order_by('-upload_timestamp').first()
            if not latest_dataset:
                return Response(
                    {'error': 'No data available'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            dataset = latest_dataset
            equipment = Equipment.objects.filter(dataset=dataset)
        
        # Create PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="equipment_report_{dataset.id}.pdf"'
        
        # Create PDF document
        doc = SimpleDocTemplate(response, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1  # Center
        )
        story.append(Paragraph("Chemical Equipment Analysis Report", title_style))
        story.append(Spacer(1, 12))
        
        # Metadata section
        metadata_style = styles['Normal']
        story.append(Paragraph(f"<b>Report Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", metadata_style))
        story.append(Paragraph(f"<b>Dataset Filename:</b> {dataset.filename}", metadata_style))
        story.append(Paragraph(f"<b>Upload Timestamp:</b> {dataset.upload_timestamp.strftime('%Y-%m-%d %H:%M:%S')}", metadata_style))
        story.append(Spacer(1, 20))
        
        # Summary Statistics Table
        story.append(Paragraph("Summary Statistics", styles['Heading2']))
        summary_data = [
            ['Metric', 'Value'],
            ['Total Equipment Count', str(dataset.total_count)],
            ['Average Flowrate', f"{dataset.avg_flowrate:.2f} L/min"],
            ['Average Pressure', f"{dataset.avg_pressure:.2f} bar"],
            ['Average Temperature', f"{dataset.avg_temperature:.2f} °C"],
        ]
        
        summary_table = Table(summary_data)
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Equipment Type Distribution
        story.append(Paragraph("Equipment Type Distribution", styles['Heading2']))
        type_data = [['Equipment Type', 'Count']]
        for eq_type, count in dataset.type_distribution.items():
            type_data.append([eq_type, str(count)])
        
        type_table = Table(type_data)
        type_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(type_table)
        story.append(Spacer(1, 20))
        
        # Complete Equipment List
        story.append(Paragraph("Complete Equipment List", styles['Heading2']))
        equipment_data = [['Name', 'Type', 'Flowrate (L/min)', 'Pressure (bar)', 'Temperature (°C)']]
        
        for eq in equipment:
            equipment_data.append([
                eq.equipment_name,
                eq.type,
                f"{eq.flowrate:.1f}",
                f"{eq.pressure:.1f}",
                f"{eq.temperature:.1f}"
            ])
        
        equipment_table = Table(equipment_data)
        equipment_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8)
        ]))
        story.append(equipment_table)
        
        # Build PDF
        doc.build(story)
        return response
        
    except Exception as e:
        return Response(
            {'error': f'PDF generation failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
