from sqlalchemy.sql import func
from app import db  # Importa la base de datos (db) de (backend/app/__init__.py)

# Modelo Creature (Criatura)
class Creature(db.Model):
    __tablename__ = 'creature'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(2000))
    unique_number = db.Column(db.Integer, unique=True, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)  # Debe ser nullable=False si siempre tiene un dueño
    image_url = db.Column(db.String(500), nullable=True)  # URL de la imagen
    QR_code_url = db.Column(db.String(500), nullable=True)  # URL del código QR generado
    created_at = db.Column(db.DateTime, default=func.now())

    # Relación con Client (1 cliente tiene muchas criaturas)
    owner = db.relationship('Client', back_populates='creatures')

    def __repr__(self):
        return f'<Creature id={self.id}, name={self.name}, unique_number={self.unique_number}>'


# Modelo Client (Cliente)
class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    birthdate = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=func.now())

    # Relación con Creature (1 cliente tiene muchas criaturas)
    creatures = db.relationship('Creature', back_populates='owner')

    # Relación con Book (1 cliente tiene muchos libros)
    books = db.relationship("Book", back_populates="client")

    def __repr__(self):
        return f'<Client id={self.id}, name={self.name}>'


# Modelo Wheel (Ruleta)
class Wheel(db.Model):
    __tablename__ = 'wheel'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    def __repr__(self):
        return f'<Wheel id={self.id}, numero={self.numero}>'


# Modelo Book (Libro)
class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)  # Clave foránea hacia Client
    scene_count = db.Column(db.Integer, default=20)
    completion_status = db.Column(db.Boolean, default=False)
    is_paid = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=func.now())

    # Relación con Client (muchos libros pertenecen a un cliente)
    client = db.relationship("Client", back_populates="books")

    # Relación con Scene (1 libro tiene muchas escenas)
    scenes = db.relationship("Scene", back_populates="book")

    def __repr__(self):
        return f'<Book id={self.id}, title={self.title}>'


# Modelo Scene (Escena)
class Scene(db.Model):
    __tablename__ = 'scene'
    id = db.Column(db.Integer, primary_key=True, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)  # Clave foránea hacia Book
    paragraph = db.Column(db.String, nullable=True)
    image_url = db.Column(db.String, nullable=True)
    scene_number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    # Relación con Book (muchas escenas pertenecen a un libro)
    book = db.relationship("Book", back_populates="scenes")

    def __repr__(self):
        return f'<Scene id={self.id}, book={self.book_id}>'
