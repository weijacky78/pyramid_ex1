from pyramid.config import Configurator
from pyramid.security import Authenticated


def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('photo', '/photo')
    config.add_route('add_photo', '/photo/add')
    config.add_route('edit_photo', '/photo/edit/{id}')
    config.add_route('delete_photo', '/photo/delete/{id}')
    config.add_route('add_page', '/add_page')
    config.scan()
