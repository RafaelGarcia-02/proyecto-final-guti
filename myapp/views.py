from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.security import remember, forget
from sqlalchemy.orm import joinedload, sessionmaker
from .models import Autor, Cuadro, Session

# Database session
session_factory = Session

@view_config(route_name='register', renderer='templates/register.jinja2')
def register(request):
    if request.method == 'POST':
        email = request.params.get('email')
        nombre = request.params.get('nombre')
        username = request.params.get('username')
        password = request.params.get('password')

        session = session_factory()
        try:
            existing = session.query(Autor).filter((Autor.email == email) | (Autor.username == username)).first()
            if existing:
                return {'error': 'Email o username ya registrado'}

            nuevo_autor = Autor(name=nombre, email=email, username=username, role='user')
            nuevo_autor.set_password(password)
            session.add(nuevo_autor)
            session.commit()

            headers = remember(request, str(nuevo_autor.id))
            return HTTPFound(location=request.route_url('home'), headers=headers)
        except Exception as e:
            session.rollback()
            return {'error': str(e)}
        finally:
            session.close()
    return {}

@view_config(route_name='login', renderer='templates/login.jinja2')
def login(request):
    if request.method == 'POST':
        username = request.params.get('username')
        password = request.params.get('password')

        session = session_factory()
        try:
            autor = session.query(Autor).filter_by(username=username).first()
            if autor and autor.check_password(password):
                headers = remember(request, str(autor.id))
                return HTTPFound(location=request.route_url('home'), headers=headers)
            return {'error': 'Credenciales incorrectas'}
        finally:
            session.close()
    return {}

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)

@view_config(route_name='home', renderer='templates/index.jinja2')
def home(request):
    session = session_factory()
    try:
        query_cuadros = request.params.get('a', '').strip()
        query_autores = request.params.get('q', '').strip()
        if query_cuadros:
            cuadros = session.query(Cuadro).options(joinedload(Cuadro.autor)).filter(Cuadro.name.ilike(f'%{query_cuadros}%')).all()
        else:
            cuadros = session.query(Cuadro).all()
        if query_autores:
            autores = session.query(Autor).options(joinedload(Autor.cuadros)).filter(Autor.name.ilike(f'%{query_autores}%')).all()
        else:
            autores = session.query(Autor).all()
        return {'cuadros': cuadros, 'autores': autores}
    finally:
        session.close()

@view_config(route_name='cuadro_detalles', renderer='templates/cuadro_detalles.jinja2')
def cuadro_detalles(request):
    cuadro_id = request.matchdict['id']
    session = session_factory()
    try:
        cuadro = session.query(Cuadro).options(joinedload(Cuadro.autor)).filter_by(id=cuadro_id).first()
        if cuadro:
            return {'cuadro': cuadro}
        return HTTPFound(location=request.route_url('home'))
    finally:
        session.close()

@view_config(route_name='cuadros_autor', renderer='templates/cuadros_autor.jinja2')
def cuadros_autor(request):
    autor_id = request.matchdict['id']
    session = session_factory()
    try:
        autor = session.query(Autor).options(joinedload(Autor.cuadros)).filter_by(id=autor_id).first()
        if autor:
            return {'autor': autor, 'cuadros': autor.cuadros}
        return HTTPFound(location=request.route_url('home'))
    finally:
        session.close()

# Admin views
@view_config(route_name='admin', renderer='templates/admin.jinja2')
def admin(request):
    if not request.user or request.user.role != 'admin':
        return HTTPForbidden()
    session = session_factory()
    try:
        autores = session.query(Autor).all()
        cuadros = session.query(Cuadro).all()
        return {'autores': autores, 'cuadros': cuadros}
    finally:
        session.close()

@view_config(route_name='edit_autor', renderer='templates/edit_autor.jinja2', request_method='GET')
def edit_autor_get(request):
    if not request.user:
        return HTTPFound(location=request.route_url('login'))
    autor_id = request.matchdict['id']
    if request.user.role != 'admin' and str(request.user.id) != autor_id:
        return HTTPForbidden()
    session = session_factory()
    try:
        autor = session.query(Autor).filter_by(id=autor_id).first()
        if autor:
            return {'autor': autor}
        return HTTPFound(location=request.route_url('home'))
    finally:
        session.close()

@view_config(route_name='edit_autor', request_method='POST')
def edit_autor_post(request):
    if not request.user:
        return HTTPFound(location=request.route_url('login'))
    autor_id = request.matchdict['id']
    if request.user.role != 'admin' and str(request.user.id) != autor_id:
        return HTTPForbidden()
    name = request.params.get('name')
    prestigio = request.params.get('prestigio')
    role = request.params.get('role') if request.user.role == 'admin' else None
    session = session_factory()
    try:
        autor = session.query(Autor).filter_by(id=autor_id).first()
        if autor:
            autor.name = name
            autor.prestigio = prestigio
            if role:
                autor.role = role
            session.commit()
        return HTTPFound(location=request.route_url('admin') if request.user.role == 'admin' else request.route_url('home'))
    finally:
        session.close()

@view_config(route_name='delete_autor', request_method='POST')
def delete_autor(request):
    if not request.user or request.user.role != 'admin':
        return HTTPForbidden()
    autor_id = request.matchdict['id']
    session = session_factory()
    try:
        autor = session.query(Autor).filter_by(id=autor_id).first()
        if autor:
            session.query(Cuadro).filter_by(autor_id=autor_id).delete()
            session.delete(autor)
            session.commit()
        return HTTPFound(location=request.route_url('admin'))
    finally:
        session.close()

@view_config(route_name='delete_cuadro', request_method='POST')
def delete_cuadro(request):
    if not request.user:
        return HTTPFound(location=request.route_url('login'))
    cuadro_id = request.matchdict['id']
    session = session_factory()
    try:
        cuadro = session.query(Cuadro).filter_by(id=cuadro_id).first()
        if cuadro and (request.user.role == 'admin' or cuadro.autor_id == request.user.id):
            session.delete(cuadro)
            session.commit()
        return HTTPFound(location=request.route_url('admin') if request.user.role == 'admin' else request.route_url('home'))
    finally:
        session.close()

# User views for cuadros
@view_config(route_name='add_cuadro', renderer='templates/nuevo_cuadro.jinja2', request_method='GET')
def add_cuadro_get(request):
    if not request.user:
        return HTTPFound(location=request.route_url('login'))
    return {}

@view_config(route_name='add_cuadro', request_method='POST')
def add_cuadro_post(request):
    if not request.user:
        return HTTPFound(location=request.route_url('login'))
    name = request.params.get('name')
    less_description = request.params.get('less_description')
    description = request.params.get('description')
    precio = request.params.get('precio')
    url_imagen = request.params.get('url_imagen')
    enVenta = request.params.get('enVenta') == 'true'
    session = session_factory()
    try:
        nuevo_cuadro = Cuadro(
            name=name,
            less_description=less_description,
            description=description,
            precio=int(precio) if precio else None,
            autor_id=request.user.id,
            url_imagen=url_imagen,
            enVenta=enVenta
        )
        session.add(nuevo_cuadro)
        session.commit()
        return HTTPFound(location=request.route_url('home'))
    finally:
        session.close()

@view_config(route_name='edit_cuadro', renderer='templates/edit_cuadro.jinja2', request_method='GET')
def edit_cuadro_get(request):
    if not request.user:
        return HTTPFound(location=request.route_url('login'))
    cuadro_id = request.matchdict['id']
    session = session_factory()
    try:
        cuadro = session.query(Cuadro).filter_by(id=cuadro_id).first()
        if cuadro and (request.user.role == 'admin' or cuadro.autor_id == request.user.id):
            return {'cuadro': cuadro}
        return HTTPForbidden()
    finally:
        session.close()

@view_config(route_name='edit_cuadro', request_method='POST')
def edit_cuadro_post(request):
    if not request.user:
        return HTTPFound(location=request.route_url('login'))
    cuadro_id = request.matchdict['id']
    name = request.params.get('name')
    less_description = request.params.get('less_description')
    description = request.params.get('description')
    precio = request.params.get('precio')
    url_imagen = request.params.get('url_imagen')
    enVenta = request.params.get('enVenta') == 'true'
    session = session_factory()
    try:
        cuadro = session.query(Cuadro).filter_by(id=cuadro_id).first()
        if cuadro and (request.user.role == 'admin' or cuadro.autor_id == request.user.id):
            cuadro.name = name
            cuadro.less_description = less_description
            cuadro.description = description
            cuadro.precio = int(precio) if precio else None
            cuadro.url_imagen = url_imagen
            cuadro.enVenta = enVenta
            session.commit()
        return HTTPFound(location=request.route_url('admin') if request.user.role == 'admin' else request.route_url('home'))
    finally:
        session.close()
