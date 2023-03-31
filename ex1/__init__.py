from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from sqlalchemy import create_engine
from .models.user import User


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:

        config.include('pyramid_chameleon')
        config.include('.routes')
        config.include('.models')
        config.include('pyramid_jinja2')
        config.scan()

        my_session_factory = SignedCookieSessionFactory('my_secret_key')
        config.set_session_factory(my_session_factory)
        # Set up authentication and authorization policies
        authn_policy = AuthTktAuthenticationPolicy('supersecret')
        authz_policy = ACLAuthorizationPolicy()

        # Add authentication and authorization policies to the configuration
        config.set_authentication_policy(authn_policy)
        config.set_authorization_policy(authz_policy)

        #Create SQLAlchemy engine and adding it to the config registry
        engine = create_engine(settings['sqlalchemy.url'])
        config.registry['sqlalchemy.engine'] = engine
        
        # Add a callback function to the authentication policy to retrieve user info
        def get_user(request):
            user_id = request.authenticated_userid
            if user_id is not None:
                user = request.dbsession.query(User).get(user_id)
                return user

        authn_policy.callback = get_user

    return config.make_wsgi_app()
