from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPUnauthorized
from passlib.hash import sha256_crypt
from ..models import (
    Page,
    Photo,
    User,
)
from sqlalchemy.orm import Session, sessionmaker
import logging
from datetime import datetime

@view_config(route_name='home', renderer='ex1:templates/home.jinja2')
def home(request):
    engine = request.registry['sqlalchemy.engine']
    Session = sessionmaker(bind=engine)

    with Session() as session:
        # Get all the pages from the database
        pages = session.query(Page).order_by(Page.menu_order).all()
        # Get all the photos from the database
        photos = session.query(Photo).all()

        # Check if the user is logged in
        is_logged_in = False
        username = None
        if 'cookieHash' in request.cookies:
            cookie_hash = request.cookies['cookieHash']
            user = session.query(User).filter(
                User.cookieHash == cookie_hash).first()
            if user is not None:
                is_logged_in = True
                username = user.username
     
    # Render the template with the pages, photos, and login information
    return {'pages': pages, 'photos': photos, 'is_logged_in': is_logged_in, 'username': username}


@view_config(route_name='add_page', renderer='ex1:templates/add_page.pt')
def add_page(request):
    engine = request.registry['sqlalchemy.engine']
    Session = sessionmaker(bind=engine)

    with Session() as session:
        if request.method == 'POST':
            title = request.params['title']
            content = request.params['content']
            key = request.params['key']
            menu_order = request.params['menu_order']
            page = Page(title=title, content=content,
                        key=key, menu_order=menu_order)
            session.add(page)
            return HTTPFound(location=request.route_url('home'))
    return {}

@view_config(route_name='add_photo', renderer='ex1:templates/add_photo.jinja2')
def add_photo(request):
    logger = logging.getLogger()
    logger.info("Adding NEW Photo")
    engine = request.registry['sqlalchemy.engine']
    Session = sessionmaker(bind=engine)

    with Session() as session:
        if request.method == 'POST':
            picture = request.params['photo']
            description = request.params['description']
            
            photo = Photo()
            photo.photo= picture.file.read()
            photo.description=description
            photo.date_modified = datetime.now()
            
            session.add(photo)
            session.commit()
            return HTTPFound(location=request.route_url('home'))
    return {}


@view_config(route_name='delete_photo')
def delete_photo(request):
    print("Deleting photo")
    engine = request.registry['sqlalchemy.engine']
    Session = sessionmaker(bind=engine)

    with Session() as session:
        photo_id = request.matchdict['photo_id']
        photo = session.query(Photo).filter_by(photo_id=photo_id).one()
        session.delete(photo)
        return HTTPFound(location=request.route_url('photos'))
    


@view_config(route_name='login', renderer='ex1:templates/login.pt')
def login(request):
    
    engine = request.registry['sqlalchemy.engine']
    Session = sessionmaker(bind=engine)

    with Session() as session:
        if request.method == 'POST':
            username = request.params['username']
            password = request.params['password']
            user = session.query(User).filter_by(username=username).first()
            if user and password == user.passHash:
                response = HTTPFound(location=request.route_url('home'))
                response.set_cookie('username', user.username)
                return response
            else:
                return HTTPUnauthorized()
    return {}


@view_config(route_name='logout')
def logout(request):
    request.response.delete_cookie('username')
    return HTTPFound(location=request.route_url('home'))
