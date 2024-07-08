import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models, schemas
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.utils import verify_password, get_password_hash, create_access_token

def create_contact(db: Session, contact: schemas.ContactCreate):
    try:
        db_contact = models.Contact(**contact.model_dump())
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        logging.info(f"Contact created: {db_contact.id}, Name: {db_contact.first_name} {db_contact.last_name}")
        return db_contact
    except IntegrityError as e:
        db.rollback()
        logging.error(f"Error creating contact: {e.orig}")
        raise HTTPException(status_code=400, detail=f"Email {contact.email} already registered")
    except Exception as e:
        logging.error(f"Error creating contact: {e}")
        raise

def get_all_contacts(db: Session, skip: int = 0, limit: int = 10):
    try:
        contacts = db.query(models.Contact).offset(skip).limit(limit).all()
        logging.info(f"Retrieved {len(contacts)} contacts.")
        return contacts
    except Exception as e:
        logging.error(f"Error retrieving contacts: {e}")
        raise

def get_contact(db: Session, contact_id: int):
    try:
        contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
        if contact:
            logging.info(f"Contact retrieved: {contact.id}, Name: {contact.first_name} {contact.last_name}")
        else:
            logging.info(f"No contact found with ID: {contact_id}")
        return contact
    except Exception as e:
        logging.error(f"Error retrieving contact {contact_id}: {e}")
        raise

def update_contact(db: Session, contact_id: int, contact: schemas.ContactCreate):
    try:
        db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
        if db_contact:
            for key, value in contact.model_dump().items():
                setattr(db_contact, key, value)
            db.commit()
            db.refresh(db_contact)
            logging.info(f"Contact updated: {db_contact.id}, Name: {db_contact.first_name} {db_contact.last_name}")
            return db_contact
        else:
            logging.info(f"No contact found with ID: {contact_id}")
            return None
    except Exception as e:
        logging.error(f"Error updating contact {contact_id}: {e}")
        raise

def delete_contact(db: Session, contact_id: int):
    try:
        db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
        if db_contact:
            logging.info(f"Contact deleted: {db_contact.id}, Name: {db_contact.first_name} {db_contact.last_name}")
            db.delete(db_contact)
            db.commit()
            return db_contact
        else:
            logging.info(f"No contact found with ID: {contact_id}")
            return None
    except Exception as e:
        logging.error(f"Error deleting contact {contact_id}: {e}")
        raise

def search_contacts(db: Session, name: str = None, email: str = None):
    query = db.query(models.Contact)

    if name:
        query = query.filter((models.Contact.first_name.ilike(f"%{name}%")) | (models.Contact.last_name.ilike(f"%{name}%")))

    if email:
        query = query.filter(models.Contact.email.ilike(f"%{email}%"))

    contacts = query.all()
    logging.info(f"Found {len(contacts)} contacts matching criteria.")
    return contacts

def get_contacts_with_upcoming_birthdays(db: Session):
    today = datetime.today()
    upcoming = today + timedelta(days=7)

    contacts = db.query(models.Contact).filter(
        models.Contact.birthday.between(today, upcoming)
    ).all()

    logging.info(f"Found {len(contacts)} contacts with upcoming birthdays.")
    return contacts

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_user(db: Session, user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_access_token_for_user(user: models.User):
    access_token_expires = timedelta(minutes=30)  # You can set this value in a config file
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return access_token

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()