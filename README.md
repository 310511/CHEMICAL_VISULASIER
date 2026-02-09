# Chemical Equipment Parameter Visualizer

A complete hybrid web + desktop application for chemical equipment data visualization and analytics. This project demonstrates a full-stack solution with Django backend, React web frontend, and PyQt5 desktop application, all sharing the same REST API.

## 🚀 Features

### Backend Features
- **Django REST Framework API** with Token Authentication
- **CSV File Upload** with validation and processing using Pandas
- **Data Analytics** with automatic summary statistics calculation
- **PDF Report Generation** using ReportLab
- **Database Management** with SQLite (auto-cleanup of old datasets)
- **CORS Support** for cross-origin requests
- **Admin Interface** for data management

### Web Frontend Features
- **Modern React UI** with responsive design
- **User Authentication** with token-based login/logout
- **Drag & Drop File Upload** with progress indication
- **Interactive Charts** using Chart.js
- **Data Tables** with sorting capabilities
- **Real-time Data Updates** after uploads
- **PDF Download** functionality
- **Upload History** tracking

### Desktop Frontend Features
- **Native PyQt5 Application** with professional UI
- **Multi-tab Interface** (Data View, Analytics, History)
- **Matplotlib Integration** for interactive charts
- **Threaded Operations** to prevent UI freezing
- **File Dialog Integration** for CSV selection and PDF saving
- **Status Bar** with operation feedback
- **Menu System** with keyboard shortcuts

## 🛠 Tech Stack

### Backend
- **Python 3.8+**
- **Django 4.2.7**
- **Django REST Framework 3.14.0**
- **django-cors-headers 4.3.1**
- **pandas 2.1.3**
- **reportlab 4.0.7**
- **SQLite** (database)

### Web Frontend
- **React 18.2.0**
- **React Router 6.20.1**
- **Axios 1.6.2**
- **Chart.js 4.4.0**
- **react-chartjs-2 5.2.0**
- **Node.js 16+**

### Desktop Frontend
- **PyQt5 5.15.10**
- **matplotlib 3.8.2**
- **requests 2.31.0**
- **pandas 2.1.3**

### Deployment & CI/CD
- **GitHub Actions** for automated deployment
- **Netlify** for frontend hosting
- **Render** for backend hosting
- **Docker** support for containerization

## � Repository Structure

```
CHEMICAL_VISULASIER/
├── backend/                          # Django REST API
│   ├── config/                       # Django project configuration
│   │   ├── settings.py               # Main settings file
│   │   ├── urls.py                  # API URL routing
│   │   └── wsgi.py                  # WSGI configuration
│   ├── equipment/                    # Equipment data app
│   │   ├── models.py                 # Database models
│   │   ├── serializers.py            # API serializers
│   │   ├── views.py                  # API views
│   │   └── urls.py                  # App URL routing
│   ├── requirements.txt               # Python dependencies
│   └── manage.py                    # Django management script
├── frontend-web/                     # React web application
│   ├── public/                       # Static files
│   ├── src/                         # Source code
│   │   ├── components/               # React components
│   │   ├── pages/                   # Page components
│   │   ├── api.js                   # API client
│   │   └── index.css                # Global styles
│   ├── package.json                  # Node dependencies
│   └── package-lock.json             # Dependency lock file
├── frontend-desktop/                 # PyQt5 desktop application
│   ├── components/                   # Desktop UI components
│   │   ├── main_window.py           # Main application window
│   │   ├── data_view_tab.py        # Data view tab
│   │   ├── analytics_tab.py         # Analytics tab
│   │   ├── history_tab.py           # History tab
│   │   ├── login_dialog.py          # Login dialog
│   │   └── api_client.py           # API client
│   ├── main.py                      # Desktop app entry point
│   └── requirements.txt              # Python dependencies
├── .github/                         # GitHub workflows
│   └── workflows/                   # CI/CD configurations
│       ├── deploy.yml                 # GitHub Pages deployment
│       └── deploy-separate.yml        # Separate deployment workflow
├── netlify.toml                     # Netlify deployment config
├── render.yaml                      # Render deployment config
├── sample_equipment_data.csv          # Sample data file
├── README.md                        # This documentation
└── .gitignore                       # Git ignore rules
```

## �📋 Prerequisites

- **Python 3.8 or higher**
- **Node.js 16 or higher**
- **npm or yarn**
- **Git**

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd chemical-equipment-visualizer
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (use admin/admin123 for testing)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

### 3. Web Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend-web

# Install dependencies
npm install

# Configure API base URL (optional, defaults to localhost:8000)
# Create .env file if needed:
echo "REACT_APP_API_URL=http://localhost:8000/api" > .env

# Start development server
npm start
```

The web frontend will be available at `http://localhost:3000`

### 4. Desktop Frontend Setup

```bash
# Navigate to desktop frontend directory (from project root)
cd frontend-desktop

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the desktop application
python main.py
```

## 📊 Sample Data Format

The application expects CSV files with the following columns:

| Column | Type | Range | Example |
|--------|------|-------|---------|
| Equipment Name | String | - | "Reactor A-101" |
| Type | String | Fixed values | "Reactor", "Pump", "Heat Exchanger", "Compressor", "Valve" |
| Flowrate | Float | 10.5 - 500.0 | 125.5 |
| Pressure | Float | 1.0 - 150.0 | 45.2 |
| Temperature | Float | 20.0 - 350.0 | 180.5 |

A sample CSV file (`sample_equipment_data.csv`) is included in the project root.

## 🔐 Authentication

### Test Credentials
- **Username:** `admin`
- **Password:** `admin123`

### Authentication Flow
1. Both frontends require authentication before accessing data
2. Login sends credentials to `/api/auth/login/`
3. Server returns a token that's stored locally
4. All subsequent API calls include the token in the `Authorization` header
5. Logout clears the token and returns to login screen

## 📡 API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/login/ | User login | No |
| POST | `/api/auth/logout/ | User logout | Yes |
| POST | `/api/upload/ | Upload CSV file | Yes |
| GET | `/api/equipment/ | Get equipment list | Yes |
| GET | `/api/summary/ | Get summary statistics | Yes |
| GET | `/api/history/ | Get upload history | Yes |
| GET | `/api/report/pdf/ | Download PDF report | Yes |

### API Usage Examples

#### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

#### Upload CSV
```bash
curl -X POST http://localhost:8000/api/upload/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -F "file=@sample_equipment_data.csv"
```

#### Get Equipment Data
```bash
curl -X GET http://localhost:8000/api/equipment/ \
  -H "Authorization: Token YOUR_TOKEN"
```

## 🖥 Application Screenshots

### Web Application
- **Login Page:** Clean authentication interface
- **Dashboard:** Comprehensive data visualization
- **Upload Section:** Drag-and-drop file upload
- **Analytics:** Interactive charts and graphs
- **History:** Upload tracking and management

### Desktop Application
- **Login Dialog:** Native authentication window
- **Data View Tab:** Table view with statistics
- **Analytics Tab:** Matplotlib charts with controls
- **History Tab:** Upload history with actions

## 🔧 Configuration

### Backend Configuration
Edit `backend/config/settings.py` for:
- Database settings
- CORS origins
- File upload limits
- Debug mode

### Frontend Configuration
Edit `frontend-web/src/api.js` for:
- API base URL
- Request/response interceptors
- Error handling

### Desktop Configuration
Edit `frontend-desktop/components/api_client.py` for:
- API base URL
- Timeout settings
- Request headers

## 🧪 Testing

### Backend Testing
```bash
cd backend
python manage.py test
```

### Web Frontend Testing
```bash
cd frontend-web
npm test
```

### Manual Testing Checklist
- [ ] Login with valid credentials
- [ ] Login with invalid credentials
- [ ] Upload valid CSV file
- [ ] Upload invalid CSV file
- [ ] View equipment data
- [ ] Sort table columns
- [ ] Generate PDF report
- [ ] View upload history
- [ ] Load historical dataset
- [ ] Logout functionality

## 🐛 Troubleshooting

### Common Issues

#### Backend Issues
**Problem:** `ModuleNotFoundError: No module named 'django'`
**Solution:** Activate virtual environment and install requirements

**Problem:** CORS errors in browser
**Solution:** Check `CORS_ALLOWED_ORIGINS` in settings.py

**Problem:** Database migration errors
**Solution:** Delete `db.sqlite3` and re-run migrations

#### Web Frontend Issues
**Problem:** `npm install` fails
**Solution:** Clear npm cache: `npm cache clean --force`

**Problem:** API connection refused
**Solution:** Ensure backend server is running on localhost:8000

**Problem:** Charts not displaying
**Solution:** Check browser console for JavaScript errors

#### Desktop Application Issues
**Problem:** PyQt5 import errors
**Solution:** Install PyQt5 in virtual environment

**Problem:** API connection errors
**Solution:** Check network connectivity and backend server status

**Problem:** UI freezing during operations
**Solution:** Ensure all API calls are made in separate threads

## 🚀 Deployment Options

### 🌐 Automated Deployment (Recommended)

#### GitHub Actions + Netlify + Render
The repository includes automated deployment workflows:

1. **Frontend to Netlify:**
   - Push to `main` branch triggers automatic deployment
   - URL: `https://chemical-equipment-visualizer.netlify.app`
   - Environment variables configured in `netlify.toml`

2. **Backend to Render:**
   - Push to `main` branch triggers automatic deployment
   - URL: `https://chemical-equipment-backend.onrender.com`
   - Configuration in `render.yaml`

3. **CI/CD Workflow:**
   - Located in `.github/workflows/deploy-separate.yml`
   - Automatic testing and deployment
   - Separate frontend and backend deployment

### 🛠️ Manual Deployment

#### Backend Deployment Options
1. **Render (Recommended):**
   - Connect GitHub repository
   - Use `render.yaml` configuration
   - Auto-deploy on push

2. **Heroku:**
   ```bash
   # Install Heroku CLI
   heroku create your-app-name
   heroku buildpacks:add heroku/python
   git push heroku main
   ```

3. **DigitalOcean/AWS:**
   - Set up server with Docker
   - Configure nginx reverse proxy
   - Use gunicorn WSGI server

#### Frontend Deployment Options
1. **Netlify (Recommended):**
   - Drag and drop build folder
   - Or connect GitHub repository
   - Configure redirects in `netlify.toml`

2. **Vercel:**
   ```bash
   npm install -g vercel
   vercel --prod
   ```

3. **GitHub Pages:**
   ```bash
   npm run build
   # Deploy dist folder to gh-pages branch
   ```

#### Desktop Application Distribution
1. **PyInstaller:**
   ```bash
   cd frontend-desktop
   pip install pyinstaller
   pyinstaller --onefile --windowed main.py
   ```

2. **Create Installers:**
   - Windows: Use Inno Setup or NSIS
   - macOS: Use create-dmg
   - Linux: Use AppImage or Snap

### 📋 Environment Variables

#### Production Environment
```bash
# Backend (.env)
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com

# Frontend (.env)
REACT_APP_API_URL=https://your-backend-domain.com/api
```

#### Local Development
```bash
# Backend uses SQLite by default
# Frontend connects to http://localhost:8000/api
```

## 🔮 Future Enhancements

- [ ] Real-time data streaming with WebSockets
- [ ] Advanced filtering and search capabilities
- [ ] Data export in multiple formats (Excel, JSON)
- [ ] User roles and permissions
- [ ] Email notifications for uploads
- [ ] Mobile application (React Native)
- [ ] Cloud deployment (AWS/Azure)
- [ ] Machine learning analytics
- [ ] Equipment performance predictions
- [ ] Multi-language support

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the API documentation

## 🙏 Acknowledgments

- Django REST Framework for robust API development
- React team for excellent frontend framework
- PyQt5 community for desktop GUI toolkit
- Chart.js for beautiful data visualization
- ReportLab for PDF generation capabilities

---

**Built with ❤️ for the chemical engineering community**
