def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('add', '/add')
    config.add_route('edit', '/edit/{id}')
    config.add_route('delete', '/delete/{id}')
    config.add_route('cuadro_detalles', '/cuadros/{id}')
    config.add_route('cuadros_autor', '/autores/{id}/cuadros')
    