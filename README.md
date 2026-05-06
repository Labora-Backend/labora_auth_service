# Auth Service

 **Labora Backend** — A secure, scalable Django authentication microservice for the freelancing platform.



![Django](https://img.shields.io/badge/Django-4.2+-092E20?style=flat-square&logo=django)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python)
![JWT](https://img.shields.io/badge/JWT-RS256-000000?style=flat-square)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=flat-square&logo=mysql)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat-square&logo=docker)



---

## Overview

Auth Service is a production-ready authentication microservice built with Django and Django REST Framework. It handles user registration, secure login, JWT token generation, password recovery, and profile management for the Labora freelancing platform.

**Key Highlights:**
- 🔐 **RS256 JWT Authentication** with asymmetric cryptography
- 📧 **Secure OTP-based Password Reset** via email
- 👥 **Role-based Access Control** (Client, Freelancer, Admin)
- 🚀 **Fully Containerized** with Docker
- ⚡ **Microservice Ready** with clean API design
- 🛡️ **Environment-based Configuration** for multiple deployments

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Runtime** | Python 3.10+ |
| **Framework** | Django 4.2+, Django REST Framework |
| **Authentication** | JWT (RS256 with RSA keys) |
| **Database** | MySQL 8.0+ |
| **Email** | SMTP (Gmail/custom) |
| **Containerization** | Docker & Docker Compose |
| **Key Libraries** | python-decouple, cryptography, Pillow |

---

## Project Structure

```
labora-freelancing_platform_AuthService/
│
├── 📂 authservice/              # Django project configuration
│   ├── settings.py              # Project settings & database config
│   ├── urls.py                  # Main URL router
│   └── wsgi.py                  # WSGI application
│
├── 📂 myapp/                    # Core authentication application
│   ├── models.py                # User & PasswordResetOTP models
│   ├── views.py                 # REST API endpoints
│   ├── serializers.py           # Request/response serialization
│   ├── authentication.py        # JWT token logic
│   ├── urls.py                  # App-level routing
│   └── admin.py                 # Django admin configuration
│
├── 📂 jwt_keys/                 # RSA key pair (git-ignored)
│   ├── private.pem              # Private key (SECURE)
│   └── public.pem               # Public key
│
├── 📄 manage.py                 # Django CLI
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env                      # Environment variables (git-ignored)
├── 📄 .gitignore                # Git exclusions
├── 📄 Dockerfile                # Container configuration
├── 📄 entrypoint.sh             # Docker entrypoint script
└── 📄 README.md                 # This file

```

---

## Getting Started

### Prerequisites

- **Python** 3.10 or higher
- **MySQL** 8.0 or higher
- **pip** (Python package manager)
- **Git**

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/labora-freelancing_platform_AuthService.git
cd labora-freelancing_platform_AuthService
```

### 2. Create & Activate Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Django Configuration
DJANGO_SECRET_KEY=your-super-secret-key-here-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_ENGINE=django.db.backends.mysql
DB_NAME=labora_auth_db
DB_USER=root
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306

# Email Configuration (Gmail SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password

# JWT Configuration
JWT_ALGORITHM=RS256
JWT_ACCESS_TOKEN_MINUTES=15
JWT_REFRESH_TOKEN_DAYS=7

# OTP Configuration
OTP_EXPIRY_MINUTES=5
OTP_LENGTH=6
```

> **⚠️ Security Note:** Never commit `.env` files. Add to `.gitignore` before pushing code.

### 5. Setup JWT Keys

Generate RSA key pair for JWT signing:

```bash
# Create jwt_keys directory (one level above the project)
mkdir -p ../jwt_keys

# Generate private key (4096-bit)
openssl genrsa -out ../jwt_keys/private.pem 4096

# Extract public key from private key
openssl rsa -in ../jwt_keys/private.pem -pubout -out ../jwt_keys/public.pem
```

### 6. Setup Database

```bash
# Run migrations
python manage.py migrate

# Create superuser (optional, for Django admin)
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Server will be available at `http://localhost:8000`

---

## Docker Deployment

### Build & Run with Docker

```bash
# Build the image
docker build -t labora-auth-service:latest .

# Run the container
docker run -d \
  -p 8000:8000 \
  --name auth-service \
  --env-file .env \
  labora-auth-service:latest
```

### Using Docker Compose (Recommended)

Create `docker-compose.yml`:

```yaml
version: '3.9'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: labora_auth_db
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  auth-service:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - mysql
    environment:
      DB_HOST: mysql
      DB_USER: root
      DB_PASSWORD: rootpassword
    volumes:
      - ./jwt_keys:/app/jwt_keys

volumes:
  mysql_data:
```

Run with:
```bash
docker-compose up -d
```

---

## API Endpoints

### Authentication Endpoints

#### 1. **User Registration**
```http
POST /api/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "first_name": "John",
  "last_name": "Doe",
  "role": "freelancer"  # or "client", "admin"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user_id": 1,
  "email": "user@example.com"
}
```

---

#### 2. **User Login**
```http
POST /api/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJSUzI1NiIs...",
  "expires_in": 900,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "role": "freelancer"
  }
}
```

---

#### 3. **Get User Profile** *(Authenticated)*
```http
GET /api/profile/
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "freelancer",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

#### 4. **Send Password Reset OTP**
```http
POST /api/send-reset-otp/
Content-Type: application/json

{
  "email": "user@example.com"
}
```

**Response (200 OK):**
```json
{
  "message": "OTP sent to your email",
  "expires_in": 300
}
```

---

#### 5. **Reset Password with OTP**
```http
POST /api/reset-password/
Content-Type: application/json

{
  "email": "user@example.com",
  "otp": "123456",
  "new_password": "NewSecurePassword456!"
}
```

**Response (200 OK):**
```json
{
  "message": "Password reset successfully"
}
```

---

#### 6. **Logout** *(Authenticated)*
```http
POST /api/logout/
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "message": "Logged out successfully"
}
```

---

## Security Best Practices

### Environment & Secrets
- ✅ Never commit `.env` files, private keys, or secrets
- ✅ Use strong `DJANGO_SECRET_KEY` (minimum 50 characters)
- ✅ Rotate JWT keys periodically in production
- ✅ Use environment-specific configurations

### JWT Security
- ✅ RS256 algorithm provides asymmetric cryptography
- ✅ Access tokens expire in 15 minutes (configurable)
- ✅ Refresh tokens expire in 7 days
- ✅ Public key safely exposed to clients; private key kept secure

### OTP & Password Reset
- ✅ OTP expires after 5 minutes
- ✅ OTP can only be used once
- ✅ One-way hashing for password storage
- ✅ Email verification for account recovery

### Database
- ✅ Use strong MySQL passwords
- ✅ Enable SSL/TLS for database connections in production
- ✅ Regular backups and monitoring

---

## Configuration Guide

### Email Setup (Gmail)

1. Enable 2-Factor Authentication on your Google Account
2. Generate an **App Password**: https://myaccount.google.com/apppasswords
3. Use the app password in `.env`:
   ```env
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=generated-app-password
   ```

### Database Setup

**For MySQL 8.0+:**
```bash
mysql -u root -p
CREATE DATABASE labora_auth_db;
CREATE USER 'labora_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON labora_auth_db.* TO 'labora_user'@'localhost';
FLUSH PRIVILEGES;
```

---

## Troubleshooting

### Common Issues

**1. "No module named 'django'"**
```bash
pip install -r requirements.txt
```

**2. "Can't connect to MySQL server"**
- Verify MySQL is running: `mysql -u root -p`
- Check `DB_HOST`, `DB_USER`, `DB_PASSWORD` in `.env`
- Ensure database exists: `CREATE DATABASE labora_auth_db;`

**3. "JWT key not found"**
- Generate keys in `../jwt_keys/` directory (see Setup Step 5)
- Verify file paths match in Django settings

**4. "Email sending fails"**
- Enable Less Secure Apps (if not using App Passwords)
- Check Gmail SMTP settings are correct
- Verify network allows SMTP on port 587

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "Add feature: description"`
4. Push to branch: `git push origin feature/your-feature`
5. Submit a Pull Request

---

## Roadmap

- [ ] PostgreSQL support
- [ ] Refresh token rotation
- [ ] Rate limiting for OTP/login attempts
- [ ] Email verification on signup
- [ ] Two-factor authentication (2FA)
- [ ] OAuth2 integration (Google, GitHub)
- [ ] API Gateway integration
- [ ] Deployment automation (AWS, GCP)
- [ ] Comprehensive API documentation (Swagger/OpenAPI)

---



**Built with ❤️ for the Labora Freelancing Platform**

</div>
