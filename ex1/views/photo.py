from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.exc import DBAPIError

from ..models import Photo
from ..import create_session

db_err_msg = "An error occurred while accessing the database."


@view_config(route_name='photos', renderer='json')
def photo_list(request):
    session = create_session()
    try:
        photos = session.query(Photo).all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'photos': [p.to_dict() for p in photos]}


@view_config(route_name='photo', renderer='json')
def photo_detail(request):
    photo_id = request.matchdict['photo_id']
    session = create_session()
    try:
        photo = session.query(Photo).filter(Photo.photo_id == photo_id).one()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return photo.to_dict()


@view_config(route_name='add_photo', renderer='json', request_method='POST')
def add_photo(request):
    photo_data = request.json_body
    photo = Photo(filename=photo_data['filename'],
                  description=photo_data['description'])
    session = create_session()
    try:
        session.add(photo)
        session.flush()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return photo.to_dict()


@view_config(route_name='update_photo', renderer='json', request_method='PUT')
def update_photo(request):
    photo_id = request.matchdict['photo_id']
    photo_data = request.json_body
    session = create_session()
    try:
        photo = session.query(Photo).filter(Photo.photo_id == photo_id).one()
        photo.filename = photo_data['filename']
        photo.description = photo_data['description']
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return photo.to_dict()


@view_config(route_name='delete_photo', renderer='json', request_method='DELETE')
def delete_photo(request):
    photo_id = request.matchdict['photo_id']
    session = create_session()
    try:
        photo = session.query(Photo).filter(Photo.photo_id == photo_id).one()
        session.delete(photo)
        session.flush()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'message': f'Photo with ID {photo_id} has been deleted.'}
