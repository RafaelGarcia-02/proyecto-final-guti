from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

def get_user(request):
        user_id = request.authenticated_userid
        if user_id is not None:
            from .models import Session, Autor
            session = Session()
            user = session.query(Autor).get(user_id)
            session.close()
            return user
        return None

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        # 1. Configuración de Seguridad (¡Añade esto!)
        # 'secret_key' es una frase secreta para cifrar la cookie. Cámbiala por algo único.
        authn_policy = AuthTktAuthenticationPolicy('mi_clave_secreta_777', hashalg='sha512')
        authz_policy = ACLAuthorizationPolicy()
        
        config.set_authentication_policy(authn_policy)
        config.set_authorization_policy(authz_policy)

        # 2. Configuración estándar
        config.include('pyramid_jinja2')
       # config.include('.models') # Asegúrate de incluir tus modelos para la DB
        config.include('.routes')
        
        config.scan()
        config.add_request_method(get_user, 'user', reify=True)
    
    
    return config.make_wsgi_app()