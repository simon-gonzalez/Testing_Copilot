import unittest
from app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_post_agregar_hola(self):
        """Prueba el endpoint POST /agregar_hola"""
        response = self.app.post('/agregar_hola', json={"cadena": "mundo"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"resultado": "hola mundo desde la api de python"})

    def test_get_agregar_hola(self):
        """Prueba el endpoint GET /agregar_hola"""
        response = self.app.get('/agregar_hola?cadena=mundo')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"resultado": "hola mundo desde la api de python"})

if __name__ == '__main__':
    unittest.main()
