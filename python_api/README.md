# API Python con Autenticación JWT 🔐

Una API completa con sistema de autenticación JWT, registro de usuarios y endpoints protegidos.

## 🚀 Características

- **Autenticación JWT**: Login/registro seguro
- **Base de datos**: SQLite integrada
- **Swagger UI**: Documentación interactiva
- **Endpoints protegidos**: Requieren token de autenticación
- **Endpoints públicos**: Acceso libre

## 📋 Endpoints Disponibles

### 🔓 Autenticación (`/auth/`)
- `POST /auth/register` - Registrar nuevo usuario
- `POST /auth/login` - Iniciar sesión (obtener token)
- `GET /auth/profile` - Ver perfil (requiere token)

### 🛡️ API Principal (`/api/`)
- `GET/POST /api/agregar_hola` - Endpoint protegido (requiere token)
- `GET/POST /api/agregar_hola_publico` - Endpoint público

## 🔧 Uso

### 1. Registrar usuario
```bash
curl -X POST https://testing-copilot.onrender.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "mi_usuario", "email": "mi@email.com", "password": "mi_password"}'
```

### 2. Hacer login
```bash
curl -X POST https://testing-copilot.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "mi_usuario", "password": "mi_password"}'
```

### 3. Usar endpoint protegido
```bash
curl -X POST https://testing-copilot.onrender.com/api/agregar_hola \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -d '{"cadena": "mundo"}'
```

## 🧪 Testing

```bash
python -m unittest test_app.py
```

## 📖 Documentación

Visita: https://testing-copilot.onrender.com/docs/
