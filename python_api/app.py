from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import timedelta

app = Flask(__name__)

# Configuración
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'tu-clave-secreta-super-segura')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensiones
jwt = JWTManager(app)
db = SQLAlchemy(app)
api = Api(app, version='2.0', title='API con Autenticación JWT',
          description='API con sistema de usuarios y autenticación JWT',
          doc='/docs/')

# Modelo de Usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

# Modelos para la API
user_model = api.model('User', {
    'username': fields.String(required=True, description='Nombre de usuario'),
    'email': fields.String(required=True, description='Email del usuario'),
    'password': fields.String(required=True, description='Contraseña')
})

login_model = api.model('Login', {
    'username': fields.String(required=True, description='Nombre de usuario'),
    'password': fields.String(required=True, description='Contraseña')
})

entrada_model = api.model('Entrada', {
    'cadena': fields.String(required=True, description='Cadena de entrada')
})

# Namespace para autenticación
auth_ns = api.namespace('auth', description='Operaciones de autenticación')

@auth_ns.route('/register')
class Register(Resource):
    @api.expect(user_model)
    def post(self):
        """Registrar un nuevo usuario"""
        data = request.json
        
        # Verificar si el usuario ya existe
        if User.query.filter_by(username=data['username']).first():
            return {'message': 'El usuario ya existe'}, 400
        
        if User.query.filter_by(email=data['email']).first():
            return {'message': 'El email ya está registrado'}, 400
        
        # Crear nuevo usuario
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return {'message': 'Usuario registrado exitosamente', 'user': user.to_dict()}, 201

@auth_ns.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Iniciar sesión y obtener token JWT"""
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.id)
            return {
                'access_token': access_token,
                'user': user.to_dict(),
                'message': 'Login exitoso'
            }
        
        return {'message': 'Credenciales inválidas'}, 401

@auth_ns.route('/profile')
class Profile(Resource):
    @jwt_required()
    def get(self):
        """Obtener perfil del usuario autenticado"""
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        return user.to_dict()

# Namespace para funciones principales
main_ns = api.namespace('api', description='Funciones principales de la API')

@main_ns.route('/agregar_hola')
class AgregarHola(Resource):
    @api.expect(entrada_model)
    @jwt_required()
    def post(self):
        """Agrega 'hola' a la cadena de entrada (requiere autenticación)"""
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        data = request.json
        cadena_entrada = data.get('cadena', '')
        respuesta = f"hola {cadena_entrada} desde la api de python - Usuario: {user.username}"
        return jsonify({"resultado": respuesta})

    @api.doc(params={'cadena': 'Cadena de entrada'})
    @jwt_required()
    def get(self):
        """Agrega 'hola' a la cadena de entrada desde parámetros de URL (requiere autenticación)"""
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        cadena_entrada = request.args.get('cadena', '')
        respuesta = f"hola {cadena_entrada} desde la api de python - Usuario: {user.username}"
        return jsonify({"resultado": respuesta})

# Endpoint público (sin autenticación)
@main_ns.route('/agregar_hola_publico')
class AgregarHolaPublico(Resource):
    @api.expect(entrada_model)
    def post(self):
        """Agrega 'hola' a la cadena de entrada (público, sin autenticación)"""
        data = request.json
        cadena_entrada = data.get('cadena', '')
        respuesta = f"hola {cadena_entrada} desde la api de python (público)"
        return jsonify({"resultado": respuesta})

    @api.doc(params={'cadena': 'Cadena de entrada'})
    def get(self):
        """Agrega 'hola' a la cadena de entrada desde parámetros de URL (público)"""
        cadena_entrada = request.args.get('cadena', '')
        respuesta = f"hola {cadena_entrada} desde la api de python (público)"
        return jsonify({"resultado": respuesta})

# Crear tablas
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
