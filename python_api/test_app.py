import unittest
import json
from app import app, db, User

class TestAuthAPI(unittest.TestCase):
    def setUp(self):
        """Configurar para las pruebas"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Limpiar después de las pruebas"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_user(self):
        """Prueba registro de usuario"""
        response = self.app.post('/auth/register', 
                                json={
                                    "username": "testuser",
                                    "email": "test@example.com",
                                    "password": "testpass123"
                                })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Usuario registrado exitosamente')

    def test_login_user(self):
        """Prueba login de usuario"""
        # Primero registrar usuario
        self.app.post('/auth/register', 
                     json={
                         "username": "testuser",
                         "email": "test@example.com",
                         "password": "testpass123"
                     })
        
        # Luego hacer login
        response = self.app.post('/auth/login',
                               json={
                                   "username": "testuser",
                                   "password": "testpass123"
                               })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)

    def test_protected_endpoint(self):
        """Prueba endpoint protegido"""
        # Registrar y hacer login
        self.app.post('/auth/register', 
                     json={
                         "username": "testuser",
                         "email": "test@example.com",
                         "password": "testpass123"
                     })
        
        login_response = self.app.post('/auth/login',
                                     json={
                                         "username": "testuser",
                                         "password": "testpass123"
                                     })
        token = json.loads(login_response.data)['access_token']
        
        # Probar endpoint protegido
        response = self.app.post('/api/agregar_hola',
                               json={"cadena": "mundo"},
                               headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("testuser", data['resultado'])

    def test_public_endpoint(self):
        """Prueba endpoint público"""
        response = self.app.get('/api/agregar_hola_publico?cadena=mundo')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['resultado'], "hola mundo desde la api de python (público)")

if __name__ == '__main__':
    unittest.main()
