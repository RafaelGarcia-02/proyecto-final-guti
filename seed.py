from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Importamos Base para poder resetear las tablas
from myapp.models import Base, Autor, Cuadro 

# 1. Conectar a la base de datos
engine = create_engine('sqlite:///myapp.db')

# --- ESTO ELIMINA LOS ERRORES DE COLUMNAS FALTANTES ---
print("Reseteando base de datos...")
Base.metadata.drop_all(engine)   # Borra las tablas viejas
Base.metadata.create_all(engine) # Crea las tablas nuevas con todos los campos
# -----------------------------------------------------

Session = sessionmaker(bind=engine)
session = Session()
# --- 1. Autores ---
# Van Gogh (Ya lo tenías)
v_gogh = Autor(name="Vincent van Gogh", prestigio="Muy Alto")
session.add(v_gogh)

# Nuevo Autor: Da Vinci
da_vinci = Autor(name="Leonardo da Vinci", prestigio="Legendario")
session.add(da_vinci)

# Usamos flush para que la base de datos nos asigne los IDs de ambos
session.flush() 

# --- 2. Cuadros ---

# Cuadro 1: Van Gogh (El que ya tenías)
cuadro1 = Cuadro(
    name="La noche estrellada",
    less_description="Óleo sobre lienzo",
    description="Una vista nocturna desde la ventana del asilo de Saint-Rémy.",
    precio=1000000,
    autor_id=v_gogh.id,
    url_imagen="/static/img/noche_estrellada.jpg"
)

# Cuadro 2: Segundo cuadro para Van Gogh
cuadro2 = Cuadro(
    name="Los Girasoles",
    less_description="Óleo sobre lienzo",
    description="Una de las famosas series de cuadros de girasoles pintados en Arlés.",
    precio=800000,
    autor_id=v_gogh.id,
    url_imagen="/static/img/girasoles.jpg"
    )

# Cuadro 3: Cuadro para Da Vinci
cuadro3 = Cuadro(
    name="La Gioconda",
    less_description="Óleo sobre tabla de álamo",
    description="También conocida como la Mona Lisa, el retrato más famoso del mundo.",
    precio=5000000,
    autor_id=da_vinci.id,
    url_imagen="/static/img/gioconda.jpg"
   )

# Añadimos todos los cuadros
session.add_all([cuadro1, cuadro2, cuadro3])

# Guardamos todo definitivamente
session.commit()

print(f"¡Éxito! Insertados 2 autores y 3 cuadros.")

print("¡Base de datos limpia y datos de prueba insertados con éxito!")