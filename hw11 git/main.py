from typing import List
from datetime import datetime, date,  timedelta 
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import or_
from sqlalchemy.orm import Session
from db_session import get_db, Contact
import uvicorn


app = FastAPI()


class ContactModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    birthday: str
    inform: str


class ResponseContactModel(BaseModel):
    id: int = Field(default=1, ge=1)
    first_name: str
    last_name: str
    email: str
    phone: str
    birthday: str
    inform: str


@app.get("/")
def read_root():
    return {"root message": "Contact OK !"}


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.query(Contact).limit(3).all()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"healthchecker message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


@app.post("/contacts")
async def create_cont(cont: ContactModel, db: Session = Depends(get_db)):
    new_cont = Contact(first_name=cont.first_name, last_name=cont.last_name, email=cont.email, 
                        phone=cont.phone, birthday=cont.birthday, inform=cont.inform)
    db.add(new_cont)
    db.commit()
    db.refresh(new_cont)
    return new_cont


@app.get("/contacts")
async def contacts_all(db: Session = Depends(get_db)):
    return db.query(Contact).all()


@app.get('/contacts/birthdays', response_model=List[ResponseContactModel])
async def soon_birthdays(days: int = 7, db: Session = Depends(get_db)):
    res = []
    now = date.today()
    end = now + timedelta(days)
    for i in db.query(Contact).all():
        bd = datetime.strptime(i.birthday, '%Y-%m-%d')
        bd = date(now.year, bd.month, bd.day)
        if (now < bd < end):
            res.append(i)
    return res


@app.get("/contacts/find")
async def find_contacts(q: str, db: Session = Depends(get_db)):
    query = db.query(Contact)
    if q:
        query = query.filter(or_(Contact.first_name.like(f'{q}%'), Contact.last_name.like(f'{q}%'), Contact.email.like(f'{q}%')))
    return query.all()


@app.get("/contacts/{contact_id}", response_model=ResponseContactModel)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    cont = db.query(Contact).filter(Contact.id == contact_id).first()
    if cont is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return cont


@app.put('/contacts/{contact_id}', response_model=ResponseContactModel)
async def update_contact(contact_id: int, body: ContactModel, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        for key, value in body.model_dump().items():
            setattr(contact, key, value)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    return contact


@app.delete('/contacts/{contact_id}', response_model=ResponseContactModel)
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    return contact
    

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)