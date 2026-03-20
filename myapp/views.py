from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from sqlalchemy import create_engine
from sqlalchemy.orm import joinedload, sessionmaker
from .models import Cuadro, Item, Base, Autor

# Database setup
engine = create_engine('sqlite:///myapp.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


@view_config(route_name='home', renderer='templates/index.jinja2')
def home(request):
    session = Session()
    cuadros = session.query(Cuadro).all()
    autores = session.query(Autor).all()
    session.close()
    return {'cuadros': cuadros, 'autores': autores}


@view_config(route_name='add', renderer='templates/add.jinja2', request_method='GET')
def add_get(request):
    return {}


@view_config(route_name='add', request_method='POST')
def add_post(request):
    name = request.params.get('name')
    description = request.params.get('description')
    if name:
        session = Session()
        item = Item(name=name, description=description)
        session.add(item)
        session.commit()
        session.close()
    return HTTPFound(location=request.route_url('home'))


@view_config(route_name='edit', renderer='templates/edit.jinja2', request_method='GET')
def edit_get(request):
    item_id = request.matchdict['id']
    session = Session()
    item = session.query(Item).filter_by(id=item_id).first()
    session.close()
    if item:
        return {'item': item}
    return HTTPFound(location=request.route_url('home'))


@view_config(route_name='edit', request_method='POST')
def edit_post(request):
    item_id = request.matchdict['id']
    name = request.params.get('name')
    description = request.params.get('description')
    if name:
        session = Session()
        item = session.query(Item).filter_by(id=item_id).first()
        if item:
            item.name = name
            item.description = description
            session.commit()
        session.close()
    return HTTPFound(location=request.route_url('home'))


@view_config(route_name='delete')
def delete(request):
    item_id = request.matchdict['id']
    session = Session()
    item = session.query(Item).filter_by(id=item_id).first()
    if item:
        session.delete(item)
        session.commit()
    session.close()
    return HTTPFound(location=request.route_url('home'))
@view_config(route_name='cuadro_detalles', renderer='templates/cuadro_detalles.jinja2')
def cuadro_detalles(request):
    cuadro_id = request.matchdict['id']
    session = Session()
    cuadro = session.query(Cuadro).options(joinedload(Cuadro.autor)).filter_by(id=cuadro_id).first()
    session.close()
    if cuadro:
        return {'cuadro': cuadro}
    return HTTPFound(location=request.route_url('home')) 
@view_config(route_name='cuadros_autor', renderer='templates/cuadros_autor.jinja2')
def cuadros_autor(request):
    autor_id = request.matchdict['id']
    session = Session()
    autor = session.query(Autor).options(joinedload(Autor.cuadros)).filter_by(id=autor_id).first()
    session.close()
    if autor:
        return {'autor': autor, 'cuadros': autor.cuadros}
    return HTTPFound(location=request.route_url('home'))