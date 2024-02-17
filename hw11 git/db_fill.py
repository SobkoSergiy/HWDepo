from datetime import timedelta, datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import faker
from db_models import Contact


fake_data: faker.Faker = faker.Faker()
TOTAL_CONTACTS = 100


def create_contacts(count: int, session):
    for i in range(count):
        c = Contact(
            first_name = fake_data.first_name(),
            last_name = fake_data.last_name(),
            email = fake_data.email(),
            birthday = fake_data.date(end_datetime=datetime.now() - timedelta(days=5*365)),
            phone = fake_data.msisdn(),
            inform = f"<{i+1}> {fake_data.paragraph(nb_sentences=1)}"
        )
        session.add(c)
    session.commit()   

    
def main():
    engine = create_engine('sqlite:///hw11.db', echo=False)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    create_contacts(TOTAL_CONTACTS, session)
    
    session.close()
    print("Data created")


if __name__ == "__main__":
    main()