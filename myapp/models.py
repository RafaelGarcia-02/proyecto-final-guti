from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
class Autor(Base):
    __tablename__="autores"
    id= Column(Integer,primary_key=True)
    name= Column(String(100), nullable=False)
    prestigio= Column(Text)
    cuadros=relationship("Cuadro", back_populates="autor")
    
class Cuadro(Base):
    __tablename__="cuadros"
    id= Column(Integer,primary_key=True)
    name= Column(String(100), nullable=False)
    less_description= Column(String(200), nullable=True)
    description= Column(Text)
    enVenta= Column(Boolean, default=True)
    precio= Column(Integer, nullable=True)
    autor_id= Column(Integer, ForeignKey("autores.id"))
    autor= relationship("Autor", back_populates="cuadros")
    url_imagen= Column(String(200),nullable=True)
    
    





