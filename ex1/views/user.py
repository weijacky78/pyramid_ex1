from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import forget, remember
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from ..models.user import User


@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    return {'title': 'Home'}


@view_config(route_name='login', renderer='templates/login.pt')
def login(request):
    if request.method == 'POST':
        username = request.params.get('username')
        password = request.params.get('password')

        user = request.dbsession.query(
            User).filter_by(username=username).first()

        if user is None:
            message = "Invalid username or password"
            return {'message': message}

        if user.validate_password(password):
            headers = remember(request, user.cookieHash)
            return HTTPFound(location=request.route_url('home'), headers=headers)

        message = "Invalid username or password"
        return {'message': message}

    return {}


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)
