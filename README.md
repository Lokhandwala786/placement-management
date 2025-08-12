# 🎓 Placement Management System

A comprehensive Django-based web application for managing student placements, internships, and industry collaborations between universities and companies.

## 🌟 Features

### 🔐 **User Management & Authentication**
- **Multi-role System**: Students, Tutors, Providers, and Administrators
- **Secure Login/Registration**: Role-based access control
- **Profile Management**: Complete user profiles with relevant information

### 📍 **Interactive Maps & Location Services**
- **Google Maps Integration**: Visual placement locations with markers
- **Geolocation Support**: Latitude/longitude tracking for placements
- **Interactive Interface**: Click to view placement details

### 📅 **Advanced Calendar Management**
- **FullCalendar Integration**: Professional calendar interface
- **Visit Scheduling**: Schedule and manage site visits
- **Drag & Drop**: Easy event management
- **Real-time Updates**: Live calendar synchronization

### 💬 **Communication System**
- **Internal Messaging**: Built-in communication between users
- **Category-based Recipients**: Organized by role (Student/Tutor/Provider)
- **Message Management**: Send, receive, delete, and organize messages
- **Real-time Notifications**: Unread message counters

### 📊 **Data Management & Export**
- **Excel Export**: Download placement data in Excel format
- **CSV Support**: Alternative export formats
- **Advanced Filtering**: Search and filter placements
- **Data Analytics**: Placement statistics and reports

### 📧 **Automated Email System**
- **Smart Notifications**: Automatic emails for status changes
- **Professional Templates**: HTML-formatted emails
- **Status Updates**: Placement approval, rejection, completion notifications

### 🚀 **Modern Web Technologies**
- **Django 4.2.7**: Latest stable Django framework
- **RESTful APIs**: Complete API endpoints for mobile apps
- **Bootstrap 5**: Modern, responsive UI design
- **AJAX Integration**: Smooth user experience

## 🛠️ Technology Stack

### **Backend**
- **Python 3.13**: Latest Python version
- **Django 4.2.7**: Web framework
- **Django REST Framework**: API development
- **SQLite**: Database (easily configurable for production)

### **Frontend**
- **HTML5 & CSS3**: Modern web standards
- **Bootstrap 5**: Responsive design framework
- **JavaScript (ES6+)**: Interactive functionality
- **FullCalendar.io**: Professional calendar component

### **APIs & Services**
- **Google Maps JavaScript API**: Location services
- **SMTP Email Backend**: Automated notifications
- **RESTful APIs**: Complete backend API system

### **Development Tools**
- **Git Version Control**: Source code management
- **Virtual Environment**: Isolated Python environment
- **Requirements Management**: Dependency tracking

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8+
- pip (Python package installer)
- Git

### **Installation Steps**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Lokhandwala786/placement-management.git
   cd placement-management
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   - Copy `.env.example` to `.env`
   - Add your Google Maps API key
   - Configure email settings

5. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run the Application**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   - Open browser: `http://127.0.0.1:8000`
   - Login with your superuser credentials

## 🔑 Configuration

### **Google Maps API**
```python
# settings.py
GOOGLE_MAPS_API_KEY = 'your_api_key_here'
GOOGLE_MAPS_ENABLED = True
```

### **Email Configuration**
```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
```

## 👥 User Roles & Permissions

### **🎓 Students**
- Create placement requests
- Upload documents
- Submit reports
- Communicate with tutors and providers
- View placement status

### **👨‍🏫 Tutors**
- Approve/reject placement requests
- Schedule site visits
- Monitor student progress
- Access calendar and scheduling tools
- Export placement data

### **🏢 Providers**
- Publish placement opportunities
- Review student applications
- Approve/reject requests
- Communicate with students and tutors

### **👨‍💼 Administrators**
- Manage all users
- System configuration
- Data backup and maintenance
- Analytics and reporting

## 📱 API Endpoints

### **Authentication**
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/logout/` - User logout

### **Placements**
- `GET /api/v1/placements/` - List all placements
- `POST /api/v1/placements/` - Create new placement
- `GET /api/v1/placements/{id}/` - Get placement details
- `PUT /api/v1/placements/{id}/` - Update placement
- `DELETE /api/v1/placements/{id}/` - Delete placement

### **Messages**
- `GET /api/v1/messages/inbox/` - Get inbox messages
- `GET /api/v1/messages/sent/` - Get sent messages
- `POST /api/v1/messages/` - Send new message
- `DELETE /api/v1/messages/{id}/` - Delete message

### **Users**
- `GET /api/v1/users/` - List all users
- `GET /api/v1/users/{id}/` - Get user details

## 🗂️ Project Structure

```
placement-management/
├── accounts/                 # User authentication & profiles
├── core/                    # Core application views & URLs
├── placements/              # Main placement management
├── providers/               # Provider-specific functionality
├── students/                # Student-specific functionality
├── tutors/                  # Tutor-specific functionality
├── templates/               # HTML templates
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User-uploaded files
├── placement_management/    # Project settings & configuration
├── requirements.txt         # Python dependencies
└── manage.py               # Django management script
```

## 🌐 Live Demo

- **GitLab Repository**: [https://campus.cs.le.ac.uk/gitlab/pgt_project/24_25_summer/imil1.git](https://campus.cs.le.ac.uk/gitlab/pgt_project/24_25_summer/imil1.git)
- **GitHub Repository**: [https://github.com/Lokhandwala786/placement-management.git](https://github.com/Lokhandwala786/placement-management.git)

## 📊 Features Overview

| Feature | Status | Description |
|---------|--------|-------------|
| User Authentication | ✅ Complete | Multi-role login system |
| Google Maps | ✅ Complete | Interactive location services |
| FullCalendar | ✅ Complete | Professional scheduling |
| Messaging System | ✅ Complete | Internal communication |
| Excel Export | ✅ Complete | Data export functionality |
| Email Notifications | ✅ Complete | Automated alerts |
| REST APIs | ✅ Complete | Full backend API |
| Responsive UI | ✅ Complete | Mobile-friendly design |

## 🚀 Deployment

### **Production Setup**
1. Configure production database (PostgreSQL/MySQL)
2. Set up static file serving (Nginx/Apache)
3. Configure environment variables
4. Set up SSL certificates
5. Configure backup systems

### **Docker Support**
```bash
# Build and run with Docker
docker build -t placement-management .
docker run -p 8000:8000 placement-management
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Lokhandwala786**
- GitHub: [@Lokhandwala786](https://github.com/Lokhandwala786)
- Project: [Placement Management System](https://github.com/Lokhandwala786/placement-management)

## 🙏 Acknowledgments

- Django Framework Team
- Bootstrap Team
- FullCalendar.io
- Google Maps API
- Open Source Community

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Contact: [Your Email]
- Documentation: [Project Wiki]

---

⭐ **Star this repository if you find it helpful!** ⭐

**Made with ❤️ by Lokhandwala786**
