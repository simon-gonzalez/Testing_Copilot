from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='API de Ejemplo',
          description='Una API simple con Swagger')

# Modelo para la entrada de datos
entrada_model = api.model('Entrada', {
    'cadena': fields.String(required=True, description='Cadena de entrada')
})

@api.route('/agregar_hola')
class AgregarHola(Resource):
    @api.expect(entrada_model)
    def post(self):
        """Agrega 'hola' a la cadena de entrada"""
        data = request.json
        cadena_entrada = data.get('cadena', '')
        respuesta = f"hola {cadena_entrada} desde la api de python"
        return jsonify({"resultado": respuesta})

    @api.doc(params={'cadena': 'Cadena de entrada'})
    def get(self):
        """Agrega 'hola' a la cadena de entrada desde parámetros de URL"""
        cadena_entrada = request.args.get('cadena', '')
        respuesta = f"hola {cadena_entrada} desde la api de python"
        return jsonify({"resultado": respuesta})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
