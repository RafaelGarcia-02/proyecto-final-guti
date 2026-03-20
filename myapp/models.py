import bcrypt
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Autor(Base):
    __tablename__ = "autores"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    prestigio = Column(Text)
    email = Column(String(100), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    role = Column(String(20), default='user')  # 'user' or 'admin'
    cuadros = relationship("Cuadro", back_populates="autor")

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
class Cuadro(Base):
    __tablename__ = "cuadros"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    less_description = Column(String(200), nullable=True)
    description = Column(Text)
    enVenta = Column(Boolean, default=True)
    precio = Column(Integer, nullable=True)
    autor_id = Column(Integer, ForeignKey("autores.id"))
    autor = relationship("Autor", back_populates="cuadros")
    url_imagen = Column(String(200), nullable=True)
    
engine = create_engine('sqlite:///myapp.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)





