# backend/routes.py
import requests
import stripe
from sqlalchemy.exc import SQLAlchemyError, OperationalError, ProgrammingError
from flask import Flask, request, jsonify, send_from_directory
from flask import Blueprint, jsonify, request
from .models import db, Creature, Client, Wheel
from .utils import AI_description_creature_generator, generate_qr_code
from config import Config  # Importar la clase Config
from .schemas import CreatureSchema
from pathlib import Path

# Instanciar el schema
creature_schema = CreatureSchema()

# Crear un Blueprint para agrupar las rutas
main = Blueprint('main', __name__)

# Configurar la clave secreta de la API de Stripe
stripe.api_key = Config.STRIPE_SECRET_KEY

# Endpoint de una ruta básica para probar la aplicación
@main.route('/')
def home():
    return "¡Bienvenido a tu proyecto Flask!"

# Endpoint para servir archivos estáticos
@main.route('/static/qr_codes/<path:filename>')
def serve_qr_code(filename):
    qr_file_path = f"/static/qr_codes"   
    print("Ruta completa:", qr_file_path)
    return send_from_directory(qr_file_path, filename)

@main.route('/api', methods=['GET', 'POST'])
def test_endpoint():
    if request.method == 'GET':
        return jsonify({"message": "Este es un endpoint de prueba para GET."})
    elif request.method == 'POST':
        return jsonify({"message": "Este es un endpoint de prueba para POST."})
    
# Endpoint para generar una criatura
@main.route('/api/generate_creature', methods=['POST'])
def generate_creature():
    try:
        message = request.json
        client_name = message.get('client_name')
        birth_date = message.get('birth_date')
        client_email = message.get('client_email')
        creature_details = message.get('creature_details')  # Asegúrate de recibir 'creature_details'

        # Validación básica de entrada

        if not client_name:
            return jsonify({'error': 'Se requiere el nombre.'}), 400

        if not birth_date:
            return jsonify({'error': 'Se requiere la fecha de nacimiento.'}), 400

        #if not client_email:
        #    return jsonify({'error': 'Se requiere el correo electrónico.'}), 400
        
        if not creature_details:
            return jsonify({'error': 'Se requieren los detalles de la criatura.'}), 400


        try:
            count = db.session.query(Wheel).count()            
            if count == 0:
                return jsonify({'error': 'No hay números disponibles en la ruleta.'}), 400
        except Exception as e:
            print(f"Error al consultar la base de datos: {str(e)}")
            return jsonify({'error': 'Ocurrió un error al verificar los números disponibles en la ruleta. Inténtalo de nuevo más tarde.'}), 500

        # Generar la criatura usando OpenAI
        try:
            creature = AI_description_creature_generator(client_name, birth_date, creature_details)
        except Exception as e:
            print(f"Error generating creature: {str(e)}")
            return jsonify({"error": "An error occurred while generating the creature description."}), 500

        return jsonify({
            'name': creature['name'],
            'description': creature['description'],
            'unique_number': creature['unique_number'],
            'image_url': creature['image_url']
        })
    except SQLAlchemyError as e:  
        db.session.rollback()
        return jsonify({'error': 'Error de base de datos: ' + str(e)}), 500

    except Exception as e:
        return jsonify({'error': 'Error inesperado: ' + str(e)}), 500

# Endpoint para comprar una criatura
@main.route('/api/buy_creature', methods=['POST'])
def buy_creature():    
    try:
        message = request.json
        client_name = message['client_name']
        client_email = message['client_email']
        birth_date = message['birth_date']
        creature_name = message['creature_name']
        creature_description = message['creature_description']
        wheel_number = message['wheel_number']
        image_url = message['image_url']
        
        # Verificar si el número aún está disponible en la ruleta
        wheel_entry = db.session.query(Wheel).filter_by(numero=wheel_number).first()

        if not wheel_entry:
            return jsonify({'error': 'Ya ha sido comprada esta imagen'}), 404
            
        # Buscar si el usuario ya existe en la base de datos, lo crea si no existe
        client = Client.query.filter_by(name=client_name, email=client_email).first()
        if not client:
            client = Client(name=client_name, email=client_email, birthdate=birth_date)
            db.session.add(client)
            db.session.commit()

        # Crear una nueva instancia de Creature y asociarla con el usuario    
        creature = Creature(
            name=creature_name,
            description=creature_description,
            unique_number=wheel_number,
            owner_id=client.id,
            image_url=image_url
        )      

        # Guardar la criatura en la base de datos
        db.session.add(creature)

        # Generar el código QR después de agregar la criatura
        QR_code_url = generate_qr_code(creature,client_name, birth_date)

        # Verificar si se ha generado correctamente o si existe un error
        if "Error:" in QR_code_url:
            return jsonify({'error': QR_code_url}), 400
        
        # Asignar el código QR a la criatura
        creature.QR_code_url = QR_code_url

        db.session.commit()

        # Eliminar la fila seleccionada de la tabla 'ruleta'
        db.session.delete(wheel_entry)
        db.session.commit()
        
        #return jsonify({
        #    'message': 'Creature purchased and QR code added successfully!',
        #    'QR_code_url': f'{creature.QR_code_url}'  # Usar la URL almacenada en la base de datos
        #})
    

        return jsonify({
            'message': 'Creature purchased and QR code added successfully!',
            'creature': creature_schema.dump(creature)  # Usar la URL almacenada en la base de datos
        })


    except SQLAlchemyError as e:
        # Captura de errores específicos de SQLAlchemy
        db.session.rollback()
        return jsonify({'error': 'Error de base de datos: ' + str(e)}), 500
    except Exception as e:
        # Captura de cualquier otro tipo de excepción
        db.session.rollback()
        return jsonify({'error': 'Error inesperado: ' + str(e)}), 500


@main.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        # Crear una sesión de pago de Stripe
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Donation',  # Aquí podrías personalizar el nombre según la criatura
                        },
                        'unit_amount': 299,  # El precio en centavos (ejemplo: $2.99)
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://localhost:3000/return?session_id={CHECKOUT_SESSION_ID}',  # Ajusta esto según tu frontend
            cancel_url='http://localhost:3000/cancel',
            automatic_tax={'enabled': True},
        )
        return jsonify({'url': checkout_session.url})  # Devuelve la URL de la sesión de pago
    except Exception as e:
        return jsonify(error=str(e)), 500

@main.route('/session-status', methods=['GET'])
def session_status():
    session_id = request.args.get('session_id')
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return jsonify(status=session.status, customer_email=session.customer_details.email)
    except Exception as e:
        return jsonify(error=str(e)), 500

