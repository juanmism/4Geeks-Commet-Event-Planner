"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Events, Contacts, Event_Guests, Contact_Forms
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import json

api = Blueprint('api', __name__)

#USER

@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    results = [user.serialize() for user in users]
    response_body = {'message': 'OK',
                     'total_records': len(results),
                     'results': results}
    return jsonify(response_body), 200


@api.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    result = user.serialize()
    response_body = {'message': 'OK',
                     'result': result}
    return jsonify(response_body), 200


@api.route('/register', methods=['POST'])
def create_user():
    body = json.loads(request.data)
    user = User(email = body["email"],
                password= body["password"],
                name= body["name"],
                city= body["city"], 
                country=body["country"], 
                phone=body["phone"])
    db.session.add(user)
    db.session.commit()

    response_body = {
        "msg": " The new user has been created correctly "
    }

    return jsonify(response_body), 200


@api.route("/login", methods=["POST"])
def user_login():
    
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter(User.email == email, User.password == password).first()
    
    if not user :
        return jsonify({"msg": "Nombre de usuario o contraseña incorrectos"}), 401

    else:    
        access_token = create_access_token(identity=email)
        response_body = {"email": email,
                     "access_token": access_token}    
    return jsonify(response_body), 200

@api.route('/users/<int:user_id>', methods=['PUT'])
def modify_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=404)

    user.name = request.json.get('name', user.name)
    user.email = request.json.get('email', user.email)
    user.password = request.json.get('password', user.password)
    user.phone = request.json.get('phone', user.phone)
    user.city = request.json.get('city', user.city)
    user.country = request.json.get('country', user.country)
    db.session.commit()

    response_body = {'name': user.name,
                     'phone': user.phone,
                     'email': user.email,
                     'password': user.password,
                     'city': user.city,
                     'country': user.country}

    return jsonify(response_body), 200

@api.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(user)
    db.session.commit()
    response_body = {
        "message": "User deleted correctly"}    
    return jsonify(response_body), 200



    
# EVENTS

@api.route('events', methods=['GET'])
def get_all_events():
    events = Events.query.all()
    results = [event.serialize() for event in events]
    response_body = {'message': 'OK',
                     'total_records': len(results),
                     'results': results}
    return jsonify(response_body), 200

@api.route('/event/<event_id>', methods=['GET'])
def get_event_by_id(event_id):
    print(event_id)
    event = Events.query.get(event_id)
    print(event)
    return jsonify(event.serialize()), 200

@api.route('/event/register', methods=['POST'])
def create_event():
    body = request.get_json()
    new_event = Events(title=body["title"], date=body["date"], time=body["time"], description=body["description"], location=body["location"], image=body["image"], user_id=body["user_id"] )
    print(body)
    print(new_event)
    db.session.add(new_event)
    db.session.commit()
    return jsonify(new_event.serialize()), 200

@api.route('/events/<int:event_id>', methods=['PUT'])
def modify_event(event_id):
    event = Events.query.get(event_id)
    if event is None:
        raise APIException('Event not found', status_code=404)

    event.title = request.json.get('title', event.title)
    event.date = request.json.get('date', event.date)
    event.time = request.json.get('time', event.time)
    event.description = request.json.get('description', event.description)
    event.location = request.json.get('location', event.location)
    event.image = request.json.get('image', event.image)
    event.user_id = request.json.get('user_id', event.user_id)
    db.session.commit()

    response_body = {'title': event.title,
                     'date': event.date,
                     'time': event.time,
                     'description': event.description,
                     'location': event.location,
                     'image': event.image,
                     'user_id': event.user_id
                     }

    return jsonify(response_body), 200

@api.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Events.query.get(event_id)
    if event is None:
        raise APIException('Event not found', status_code=404)
    db.session.delete(event)
    db.session.commit()
    response_body = {
        "message": "Event deleted correctly"}    
    return jsonify(response_body), 200

# CONTACTS

@api.route('/contacts', methods=['GET'])
def get_all_contacts():
    contacts = Contacts.query.all()
    results = [contact.serialize() for contact in contacts]
    response_body = {'message': 'OK',
                     'total_records': len(results),
                     'results': results}
    return jsonify(response_body), 200

@api.route('/contact/<contact_id>', methods=['GET'])
def get_contacts_by_id(contact_id):
    print(contact_id)
    contact = Contacts.query.get(contact_id)
    print(contact)
    return jsonify(contact.serialize()), 200

@api.route('/contact/register', methods=['POST'])
def create_contact():
    body = request.get_json()
    new_contact = Contacts(name=body["name"], email=body["email"], user_id=body["user_id"])
    print(body)
    print(new_contact)
    db.session.add(new_contact)
    db.session.commit()
    return jsonify(new_contact.serialize()), 200

@api.route('/contacts/<int:contact_id>', methods=['PUT'])
def modify_contact(contact_id):
    contact = Contacts.query.get(contact_id)
    if contact is None:
        raise APIException('Contact not found', status_code=404)

    contact.name = request.json.get('name', contact.name)
    contact.email = request.json.get('email', contact.email)
    contact.user_id = request.json.get('user_id', contact.user_id)
    db.session.commit()

    response_body = {'name': contact.name,
                    'email': contact.email,
                     'user_id': contact.user_id}

    return jsonify(response_body), 200

@api.route('/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    contact = Contacts.query.get(contact_id)
    if contact is None:
        raise APIException('Contact not found', status_code=404)
    db.session.delete(contact)
    db.session.commit()
    response_body = {
        "message": "Contact deleted correctly"}    
    return jsonify(response_body), 200

# EVENTS_GUESTS

@api.route('/events_guests', methods=['GET'])
def get_all_events_guests():
    events_guests = Event_Guests.query.all()
    results = [events_guest.serialize() for events_guest in events_guests]
    response_body = {'message': 'OK',
                     'total_records': len(results),
                     'results': results}
    return jsonify(response_body), 200

@api.route('/events_guest/<events_guest_id>', methods=['GET'])
def get_events_guests_by_id(events_guest_id):
    events_guest = Event_Guests.query.get(events_guest_id)
    return jsonify(events_guest.serialize()), 200

@api.route('/events_guest/register', methods=['POST'])
def create_events_guests():
    body = request.get_json()
    new_events_guest = Event_Guests(contact_id=body["contact_id"], event_id=body["event_id"], user_id=body["user_id"])
    db.session.add(new_events_guest)
    db.session.commit()
    return jsonify(new_events_guest.serialize()), 200

@api.route('/events_guests/<int:events_guest_id>', methods=['PUT'])
def modify_events_guests(events_guest_id):
    events_guests = Event_Guests.query.get(events_guest_id)
    if events_guests is None:
        raise APIException('Event_Guest not found', status_code=404)

    events_guests.contact_id = request.json.get('contact_id', events_guests.contact_id)
    events_guests.event_id = request.json.get('event_id', events_guests.event_id)
    events_guests.user_id = request.json.get('user_id', events_guests.user_id)
    db.session.commit()

    response_body = {'contact_id': events_guests.contact_id,
                     'event_id': events_guests.event_id,
                     'user_id': events_guests.user_id}

    return jsonify(response_body), 200

@api.route('/events_guests/<int:events_guest_id>', methods=['DELETE'])
def delete_events_guests(events_guest_id):
    events_guest = Event_Guests.query.get(events_guest_id)
    if events_guest is None:
        raise APIException('Events_guest not found', status_code=404)
    db.session.delete(events_guest)
    db.session.commit()
    response_body = {
        "message": "Events_guest deleted correctly"}    
    return jsonify(response_body), 200

# CONTACT_FORMS

@api.route('/contact_forms', methods=['GET'])
def get_all_contact_forms():
    contacts_forms = Contact_Forms.query.all()
    results = [contacts_form.serialize() for contacts_form in contacts_forms]
    response_body = {'message': 'OK',
                     'total_records': len(results),
                     'results': results}
    return jsonify(response_body), 200


@api.route('/contact_forms/<contact_forms_id>', methods=['GET'])
def get_contact_forms_by_id(contact_forms_id):
    print(contact_forms_id)
    contact_form = Contact_Forms.query.get(contact_forms_id)
    print(contact_form)
    return jsonify(contact_form.serialize()), 200


@api.route('/contact_forms/register', methods=['POST'])
def create_contact_forms():
    body = request.get_json()
    new_contact_forms = Contact_Forms(email=body["email"], name=body["name"], message=body["message"],  user_id=body["user_id"])
    print(body)
    print(new_contact_forms)
    db.session.add(new_contact_forms)
    db.session.commit()
    return jsonify(new_contact_forms.serialize()), 200


@api.route('/contact_forms/<int:contact_forms_id>', methods=['PUT'])
def modify_contact_forms(contact_forms_id):
    contact_forms = Contact_Forms.query.get(contact_forms_id)
    if contact_forms is None:
        raise APIException('Contact not found', status_code=404)

    contact_forms.email = request.json.get('email', contact_forms.email)
    contact_forms.name = request.json.get('name', contact_forms.name)
    contact_forms.user_id = request.json.get('user_id', contact_forms.user_id)
    db.session.commit()

    response_body = {'email': contact_forms.email,
                     'name': contact_forms.name,   
                     'user_id': contact_forms.user_id}

    return jsonify(response_body), 200


@api.route('/contact_forms/<int:contact_forms_id>', methods=['DELETE'])
def delete_contact_forms(contact_forms_id):
    contact_form = Contact_Forms.query.get(contact_forms_id)
    if contact_form is None:
        raise APIException('Contact not found', status_code=404)
    db.session.delete(contact_form)
    db.session.commit()
    response_body = {
        "message": "Contact deleted correctly"}    
    return jsonify(response_body), 200
