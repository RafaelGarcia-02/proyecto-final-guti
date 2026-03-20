def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('cuadro_detalles', '/cuadros/{id}')
    config.add_route('cuadros_autor', '/autores/{id}/cuadros')
    
    config.add_route('admin', '/admin')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('register', '/register')

    config.add_route('edit_autor', '/edit_autor/{id}')
    config.add_route('delete_autor', '/delete_autor/{id}')
    config.add_route('add_cuadro', '/add_cuadro')
    config.add_route('edit_cuadro', '/edit_cuadro/{id}')
    config.add_route('delete_cuadro', '/delete_cuadro/{id}')
   