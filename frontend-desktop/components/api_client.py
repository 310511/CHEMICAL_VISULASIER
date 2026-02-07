"""
API Client for communicating with the Django backend
"""

import requests
import json
from typing import Dict, List, Optional, Tuple

class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url
        self.token = None
        self.session = requests.Session()
        
    def set_token(self, token: str):
        """Set authentication token"""
        self.token = token
        self.session.headers.update({
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        })
    
    def login(self, username: str, password: str) -> Tuple[bool, str, str]:
        """Login and return (success, token, error_message)"""
        try:
            response = requests.post(
                f"{self.base_url}/auth/login/",
                json={"username": username, "password": password},
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.set_token(data['token'])
                return True, data['token'], ""
            else:
                error_msg = response.json().get('error', 'Login failed')
                return False, "", error_msg
                
        except requests.exceptions.RequestException as e:
            return False, "", f"Network error: {str(e)}"
    
    def logout(self) -> Tuple[bool, str]:
        """Logout and return (success, error_message)"""
        try:
            response = self.session.post(f"{self.base_url}/auth/logout/")
            if response.status_code == 200:
                self.token = None
                self.session.headers.pop('Authorization', None)
                return True, ""
            else:
                error_msg = response.json().get('error', 'Logout failed')
                return False, error_msg
                
        except requests.exceptions.RequestException as e:
            return False, f"Network error: {str(e)}"
    
    def upload_csv(self, file_path: str) -> Tuple[bool, Dict, str]:
        """Upload CSV file and return (success, data, error_message)"""
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                # Remove Content-Type for file upload
                headers = {'Authorization': f'Token {self.token}'}
                response = requests.post(
                    f"{self.base_url}/upload/",
                    files=files,
                    headers=headers
                )
            
            if response.status_code == 200:
                return True, response.json(), ""
            else:
                error_msg = response.json().get('error', 'Upload failed')
                return False, {}, error_msg
                
        except requests.exceptions.RequestException as e:
            return False, {}, f"Network error: {str(e)}"
        except Exception as e:
            return False, {}, f"File error: {str(e)}"
    
    def get_equipment(self, dataset_id: Optional[int] = None) -> Tuple[bool, List, str]:
        """Get equipment list and return (success, data, error_message)"""
        try:
            params = {}
            if dataset_id:
                params['dataset_id'] = dataset_id
                
            response = self.session.get(
                f"{self.base_url}/equipment/",
                params=params
            )
            
            if response.status_code == 200:
                return True, response.json(), ""
            else:
                error_msg = response.json().get('error', 'Failed to get equipment')
                return False, [], error_msg
                
        except requests.exceptions.RequestException as e:
            return False, [], f"Network error: {str(e)}"
    
    def get_summary(self, dataset_id: Optional[int] = None) -> Tuple[bool, Dict, str]:
        """Get summary statistics and return (success, data, error_message)"""
        try:
            params = {}
            if dataset_id:
                params['dataset_id'] = dataset_id
                
            response = self.session.get(
                f"{self.base_url}/summary/",
                params=params
            )
            
            if response.status_code == 200:
                return True, response.json(), ""
            else:
                error_msg = response.json().get('error', 'Failed to get summary')
                return False, {}, error_msg
                
        except requests.exceptions.RequestException as e:
            return False, {}, f"Network error: {str(e)}"
    
    def get_history(self) -> Tuple[bool, List, str]:
        """Get upload history and return (success, data, error_message)"""
        try:
            response = self.session.get(f"{self.base_url}/history/")
            
            if response.status_code == 200:
                return True, response.json(), ""
            else:
                error_msg = response.json().get('error', 'Failed to get history')
                return False, [], error_msg
                
        except requests.exceptions.RequestException as e:
            return False, [], f"Network error: {str(e)}"
    
    def download_pdf(self, dataset_id: Optional[int] = None, save_path: str = "report.pdf") -> Tuple[bool, str]:
        """Download PDF report and return (success, error_message)"""
        try:
            params = {}
            if dataset_id:
                params['dataset_id'] = dataset_id
                
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get(
                f"{self.base_url}/report/pdf/",
                params=params,
                headers=headers,
                stream=True
            )
            
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True, ""
            else:
                return False, "Failed to download PDF"
                
        except requests.exceptions.RequestException as e:
            return False, f"Network error: {str(e)}"
        except Exception as e:
            return False, f"File error: {str(e)}"
