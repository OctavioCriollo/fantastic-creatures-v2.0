# app/models.py
from sqlalchemy.sql import func
from app import db     # Importa la base de datos (db) de (backend/app/__init__.py)

class Creature(db.Model):
    __tablename__ = 'creature'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(2000))
    unique_number = db.Column(db.Integer, unique=True, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)  # Campo para la URL de la imagen
    QR_code_url = db.Column(db.String(500), nullable=True)  # URL del código QR generado
    created_at = db.Column(db.DateTime, default=func.now()) 
    client = db.relationship('Client', back_populates='creatures')
   
    def __repr__(self):
        return f'<Creature id={self.id}, name={self.name}, unique_number={self.unique_number}>'    
    
class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    birthdate = db.Column(db.Date, nullable=True)
    #creatures = db.relationship('Creature', backref='client', lazy=True)
    #books = db.relationship('Book', backref='client', lazy=True)
    creatures = db.relationship('Creature', back_populates='client')
    books = db.relationship("Book", back_populates="client")
    created_at = db.Column(db.DateTime, default=func.now()) 

    def __repr__(self):
        return f'<Client id={self.id}, name={self.name}>'

class Wheel(db.Model):
    __tablename__ = 'wheel'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    #created_at = db.Column(db.DateTime, default=func.now())

    def __repr__(self):
        return f'<Wheel id={self.id}, numero={self.numero}>'
    
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))  # Asegúrate de que el nombre de la tabla es 'client'
    scene_count = db.Column(db.Integer, default=20)
    completion_status = db.Column(db.Boolean, default=False)
    is_paid = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=func.now())
    client = db.relationship("Client", back_populates="books")
    scenes = db.relationship("Scene", back_populates="book")

    def __repr__(self):
        return f'<Book id={self.id}, title={self.title}>'

class Scene(db.Model):
    __tablename__ = 'scenes'
    id = db.Column(db.Integer, primary_key=True, index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    paragraph = db.Column(db.String, nullable=True)
    image_url = db.Column(db.String, nullable=True)
    scene_number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    book = db.relationship("Book", back_populates="scenes")
    
    def __repr__(self):
        return f'<Scene id={self.id}, book={self.book}>'  
