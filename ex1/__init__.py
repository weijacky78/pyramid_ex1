from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .models.user import User


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_chameleon')
        config.include('.routes')
        config.include('.models')
        config.scan()
    return config.make_wsgi_app()
    # Set up authentication and authorization policies
    authn_policy = AuthTktAuthenticationPolicy('supersecret')
    authz_policy = ACLAuthorizationPolicy()

    # Add authentication and authorization policies to the configuration
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    # Add a callback function to the authentication policy to retrieve user info
    def get_user(request):
        user_id = request.authenticated_userid
        if user_id is not None:
            user = request.dbsession.query(User).get(user_id)
            return user

    authn_policy.callback = get_user
