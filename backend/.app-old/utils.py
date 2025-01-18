import random
from PIL import Image, ImageDraw, ImageFont
import qrcode
import segno
import io
import os
import requests


from datetime import datetime
#from ..app import db
from .models import db, Wheel, Creature
from flask import jsonify, send_from_directory
from openai import OpenAI
from config import Config  # Importar la clase Config
from flask import Blueprint, jsonify, request
from pathlib import Path

# Asegúrate de que la ruta "static/creatures" existe
STATIC_CREATURES_IMG_PATH = os.path.join(os.getcwd(), 'static', 'creatures')
os.makedirs(STATIC_CREATURES_IMG_PATH, exist_ok=True)

# Asegúrate de que la ruta "static/qr_codes" existe
STATIC_CREATURES_QR_CODE_PATH = os.path.join(os.getcwd(), 'static', 'qr_codes')
os.makedirs(STATIC_CREATURES_QR_CODE_PATH, exist_ok=True)

# Configurar la clave API de OpenAI desde las variables de configuración
client_openAI = OpenAI(
    organization=Config.OPENAI_ORG_ID,
    project=Config.OPENAI_PROJECT_ID,
)

# Crear un Blueprint para agrupar las rutas
main = Blueprint('main', __name__)

def calculate_life_number(birth_date):
    """Calcula el Número de Vida basado en la fecha de nacimiento."""
    digits = [int(digit) for digit in birth_date.replace('-', '') if digit.isdigit()]
    life_number = sum(digits)
    while life_number > 9:
        life_number = sum(int(digit) for digit in str(life_number))
    return life_number

def calculate_name_number(name):
    """Calcula el Número de Nombre basado en el nombre del usuario."""
    letter_to_number = {letter: index % 9 + 1 for index, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ", start=1)}
    name_number = sum(letter_to_number[letter.upper()] for letter in name if letter.isalpha())
    while name_number > 9:
        name_number = sum(int(digit) for digit in str(name_number))
    return name_number

# Función para generar la criatura usando OpenAI
def AI_description_creature_generator(client_name, birth_date, creature_details):
    birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d')

    life_number = calculate_life_number(birth_date)
    name_number = calculate_name_number(client_name)
   
    # Determinar rareza y poder basados en los números calculados
    rarity = "Legendaria" if life_number > 5 else "Común"
    power = "Alta" if name_number in [1, 3, 7] else "Media"

    # Crear el prompt para la API de OpenAI
    prompt = f"""
        Eres un creador de criaturas mágicas únicas, mitológicas, prehistóricas. Crea una criatura imaginativa basada en los siguientes detalles:

        - Relación con el usuario: El usuario {client_name} quiere una criatura que tenga una conexión especial con ellos.
        - Fecha de nacimiento del usuario: {birth_date} (Número de Vida: {life_number})
        - Detalles adicionales sobre la criatura: {creature_details}
        
        Si el usuario especifica múltiples criaturas o características en {creature_details}, combina sus rasgos para crear una nueva criatura híbrida. 
        Imagina que estás creando esta criatura genéticamente, mezclando las características de todas las criaturas mencionadas para crear 
        una entidad única que represente los deseos del usuario y que tenga una apariencia perfecta y no horrible.

        El nombre de la criatura, inventarlo, no uses el {client_name} para inventar el nombre.
        Proporciona una descripción detallada de la criatura resultante, incluyendo:
        - Apariencia física.
        - Habilidades especiales o mágicas.
        - Personalidad o comportamiento.
        - detalles astrológicos de la criatura en base a {birth_date} (eso no significa que nació en esa fecha pues las criaturas son muy antiguas).

        Proporciona la respuesta en formato:
        Nombre: [nombre de la criatura]
        Descripción: [descripción de la criatura] (no debe tener mas de 300 palabras).

        Que [descripción de la criatura] parezca que estas contando una historia a {client_name} quien puede tener entre 2 a 8 años de edad.

    """

    prompt2 = f"""
        Eres un creador de criaturas mágicas y míticas únicas. Crea una criatura imaginativa basada en los siguientes detalles:

        - Relación con el usuario: El usuario {client_name} quiere una criatura especial que sea su compañera mágica, alguien con quien pueda compartir secretos y aventuras.
        - Fecha de nacimiento del usuario: {birth_date} (Número de Vida: {life_number})
        - Detalles adicionales sobre la criatura: {creature_details}

        Si el usuario menciona múltiples criaturas o características en {creature_details}, fusiona sus rasgos para crear una criatura híbrida única. 
        Imagina que estás creando esta criatura especialmente para el usuario, dándole una apariencia encantadora y amistosa.

        El nombre de la criatura debe ser inventado por ti, pero que suene mágico y único, sin usar el nombre del usuario.

        Proporciona una descripción detallada de la criatura, incluyendo:
        - Cómo se ve (colores, forma, detalles únicos).
        - Habilidades mágicas o especiales que tiene.
        - Personalidad o cómo interactúa con el usuario {client_name}.
        - Conexión astrológica (basada en la fecha de nacimiento del usuario, pero recuerda que las criaturas pueden ser muy antiguas).

        Por favor, entrega la respuesta en este formato:
        Nombre: [nombre mágico de la criatura]
        Descripción: [Cuenta una historia detallada pero que no exceda de 300 palabras, como si estuvieras contándosela a {client_name}, quien puede tener entre 2 y 8 años 
        de edad. La historia debe ser mágica, suave, y emocionante, asegurándote de que la criatura sea amistosa y especial para el usuario].

    """

    prompt3 = f"""
        Eres un creador de criaturas mágicas, míticas y únicas. Tu misión es crear una criatura que sea mucho más que una compañera: una amiga mágica, alguien que siempre estará a tu lado, acompañándote en tus aventuras y compartiendo contigo secretos y sueños emocionantes. Esta criatura es especial para {client_name}.

        - Relación con el usuario: {client_name} desea una criatura mágica que le acompañe en todas sus aventuras, esté a su lado en los momentos de alegría y calma, y sea un amigo fiel en quien siempre pueda confiar.
        - Fecha de nacimiento del usuario: {birth_date} (Número de Vida: {life_number}).
        - Detalles adicionales sobre la criatura: {creature_details}.

        Si el usuario menciona varias criaturas o características en {creature_details}, toma esos rasgos y combínalos para crear una criatura híbrida increíble, con una apariencia mágica que fascine y emocione a {client_name}. Esta criatura debe ser hermosa y amigable, alguien con quien pueda soñar, jugar y sentir una conexión especial.

        El nombre de la criatura lo debes inventar tú, y debe sonar único, mágico y especial. No utilices el nombre del usuario para nombrar la criatura.

        Crea una descripción que capture la magia de esta criatura, contando su historia como si estuvieras hablándole directamente a {client_name}, que tiene entre 2 y 8 años. La criatura debe ser su compañera perfecta, con habilidades asombrosas, una personalidad encantadora, y un aspecto tan maravilloso que {client_name} quiera tenerla siempre a su lado.

        - Describe su apariencia de manera mágica y detallada: ¿Cómo se ve? (colores, forma, detalles únicos que la hagan especial).
        - Explica las habilidades mágicas o especiales que tiene: ¿Qué puede hacer que la hace tan increíble para {client_name}?
        - Describe su personalidad: ¿Es juguetona, protectora, curiosa? ¿Cómo interactúa con {client_name} en sus aventuras?
        - Incluye una conexión astrológica basada en la fecha de nacimiento del usuario, pero recuerda que las criaturas son antiguas y su sabiduría y magia han perdurado a lo largo del tiempo.

        Por favor, entrega la respuesta en el siguiente formato:

        Nombre: [nombre mágico de la criatura]
        Descripción: [Cuenta una historia mágica y emocionante de no más de 300 palabras, como si le estuvieras hablando a {client_name} directamente bajo el cielo estrellado. La narrativa debe ser suave y envolvente, asegurando que esta criatura se convierta en el amigo mágico y especial que {client_name} siempre ha soñado].
    """


    # Utiliza la nueva interfaz de la API GPT-4
    chat_completion = client_openAI.chat.completions.create(
        model="gpt-4",
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7,
        messages=[
            #{"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "content": 
             """Eres un experto creador experto de criaturas mágicas, mitologicas y fantásticas."""
            },
            {"role": "user", "content": prompt3}
        ]
    )

    # Extraer los detalles generados de la respuesta
    generated_text = chat_completion.choices[0].message.content.strip()
    print(f"Respuesta completa del modelo: {generated_text}")
    
    # Dividir el texto en nombre y descripción
    try:
        name_start = generated_text.index("Nombre: ") + len("Nombre: ")
        description_start = generated_text.index("Descripción: ")

        creature_name = generated_text[name_start:description_start].strip()
        creature_description = generated_text[description_start + len("Descripción: "):].strip()
    except ValueError:
        # Manejar el caso donde el formato no es como se esperaba
        creature_name = "Unknown Creature"
        creature_description = generated_text

    # Generar un número único para la criatura
    unique_number = spin_wheel()

    # Generar la imagen de la criatura
    try:
        image_url = AI_image_creature_generator(creature_description)
        

        if not image_url:
            return jsonify({'error': 'Error al generar la imagen: URL de imagen vacía o inválida.'}), 400
        
        # Descargar la imagen
        image_data = requests.get(image_url).content
        
        # Crear el nombre de la imagen basado en el nombre y número único de la criatura
        image_filename = f"{creature_name}_{unique_number}.png".replace(" ", "_")
        image_filepath = os.path.join(STATIC_CREATURES_IMG_PATH, image_filename)


        # Verificar que los espacios se hayan reemplazado correctamente
        print("Nombre image creature guiones bajos:", image_filename)

        # Guardar la imagen en el directorio "static/creatures"
        with open(image_filepath, 'wb') as image_file:
            image_file.write(image_data)

        # Construir la URL local para la imagen
        #relative_image_path = f"{STATIC_CREATURES_IMG_PATH}/{image_filename}"

    except Exception as e:
        print(f"Error al generar la imagen de la criatura: {str(e)}")
        return jsonify({'error': 'Ocurrió un error al generar la imagen de la criatura.'}), 500

    return {
        'name': creature_name,
        'description': creature_description,
        'unique_number': unique_number,
        'image_url': image_filename
        #'image_url': send_from_directory(STATIC_CREATURES_IMG_PATH, image_filename)
    }

# Función para generar la imagen de la criatura usando DALL·E
def AI_image_creature_generator(description):

    # Ajusta el prompt para que la imagen se centre más en la criatura
    prompt=f"""
        Crea una imagen altamente detallada y fotorrealista de una criatura única basada únicamente en su ***apariencia física*** descrita en {description}. 
        Ignora cualquier información sobre habilidades, poderes, vida o aspectos astrológicos. Concéntrate solo en las características físicas de la criatura, 
        como su tamaño, forma, textura de la piel, escamas, pelaje, plumas, colores, y otras características fisicas visibles.
        
        No incluyas ningún texto, título, símbolo, gráfico adicional, ni detalles que no formen parte del aspecto físico de la criatura.

        La criatura debe estar representada en una vista de cuerpo completo, mostrando todo su cuerpo de cabeza a cola, con todos sus rasgos distintivos y 
        texturas claramente visibles. No incluyas ningún texto, símbolos, gráficos adicionales, ni detalles que no formen parte del aspecto físico de la criatura.

        La criatura debe estar ambientada en un hábitat natural adecuado a sus características físicas, como un bosque denso, la cima de una montaña, 
        un desierto abrasador, o un océano profundo, según corresponda. El fondo debe estar ligeramente desenfocado para proporcionar profundidad sin distraer 
        la atención de la criatura. Asegúrate de que el entorno natural complemente y realce la apariencia de la criatura.

        La imagen final debe transmitir una sensación de asombro e intriga, capturando la esencia física de la criatura en un entorno realista y vívido, 
        sin distracciones de texto, gráficos o elementos artificiales.
        **NO DEBE HABER NINGÚN TEXTO EN LA IMAGEN FINAL**.
        """
    
    prompt_no_text  =f"""
        NO TEXT. This image must contain NO TEXT, titles, symbols, or graphics of any kind.
        The creature is the ONLY focus of the image. There should be NO written language or characters anywhere in the image.
        """
                
    #image_size = os.getenv('IMAGE_SIZE', '512x512')  # Usa el valor de .env o un valor predeterminado
    image_response = client_openAI.images.generate(
        model="dall-e-3",
        prompt=prompt + prompt_no_text,
        quality="standard",
        n=1,
        size='1024x1024'    
    )
    image_url = image_response.data[0].url

    return image_url

def spin_wheel():
    # Obtener el tamaño actual de la tabla 'ruleta'
    count = db.session.query(Wheel).count()
    
    if count == 0:
        raise ValueError("Sorry there are not creatures available NOW")

    # Generar un índice aleatorio basado en el tamaño de la tabla
    random_index = random.randint(0, count - 1)

    # Seleccionar la fila en la posición aleatoria
    wheel_entry = db.session.query(Wheel).offset(random_index).first()

    # Obtener el número de la ruleta
    wheel_number = wheel_entry.numero

    # Retornar el número de la ruleta
    return wheel_number

# Método para generar y guardar el código QR
def generate_qr_code(Creature, client_name, birth_date):
    # Create a shorter data string for the QR code
    qr_data = f"No escanees mis secretos"  # Replace with your actual URL

    # Generate the QR code
    qr = segno.make(qr_data, error='h')

    # Create a larger image to contain both QR code and text
    img_size = (300, 300)  # Adjust size as needed
    img = Image.new('RGB', img_size, color='white')

    # Convert QR code to PIL Image
    buffer = io.BytesIO()
    qr.save(buffer, kind='png', scale=5)
    buffer.seek(0)
    qr_img = Image.open(buffer)

    # Resize the QR code to fit the entire white space
    qr_size = 250  # Desired size of the QR code
    qr_img = qr_img.resize((qr_size, qr_size), Image.LANCZOS)

    # Calculate position to center the QR code
    qr_position = ((img_size[0] - qr_size) // 2, (img_size[1] - qr_size) // 2)

    # Paste the resized QR code into the white image at the calculated position
    img.paste(qr_img, qr_position)

    # Add text information
    #draw = ImageDraw.Draw(img)
    #font = ImageFont.load_default()  # You may want to use a custom font
    #text_data = f"Yo Soy: {client_name}\n" \
    #            f"Naci el: {birth_date}\n" \
    #            f"Mi Criatura fantastica es: {self.name}\n" \
    #            f"Sus habilidades son:\n" \
    #            f"{self.description[:100]}..."  # Truncate description if too long

    # Draw text on image
    #draw.multiline_text((50, 750), text_data, font=font, fill='black')

    # Construir una ruta relativa    
    image_filename = f"QR_Code_{Creature.name}.png".replace(" ", "_")
    qr_file_path = os.path.join(STATIC_CREATURES_QR_CODE_PATH, image_filename)

    # Verificar que los espacios se hayan reemplazado correctamente
    print("QR Code image name:", image_filename)
    print("Ruta QR Code image:", qr_file_path)

    # Guardar la imagen en el directorio "static/creatures"
    #with open(qr_file_path, 'wb') as image_file:
    #    image_file.write(img)

    img.save(qr_file_path)

    # Construir la URL local para la imagen
    #relative_image_path = f"{STATIC_CREATURES_QR_CODE_PATH}/{image_filename}"

#################################################################################
    # Assign the generated URL to the creature's attribute
    Creature.QR_code_url = qr_file_path
    return qr_file_path
