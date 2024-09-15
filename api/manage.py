from flask.cli import FlaskGroup
from app import flask_app
from db.sql_classes import (
    Base,
    Identification,
    Address,
    AddressList,
    AddEntrant,
    EntrantChoice
)
from db.database import Session, engine
import click

cli = FlaskGroup(flask_app)


@cli.command("create_db")
def create_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@cli.command("all_db")
def all_db():
    session = Session()
    response = session.query(EntrantChoice).all()
    list_of_object = []
    for obj in response:
        list_of_object.append(obj.__dict__)
    session.close()
    print("afhsijonv")
    print(*list_of_object, sep='\n')
    return list_of_object

@cli.command("all_db_id")
@click.argument('id', type=int)
def all_db_id(id):
    from sqlalchemy.orm import joinedload
    def get_entrant_choice_with_addresses(entrant_choice_id):
        session = Session()
        try:
            # Загрузка EntrantChoice вместе с AddEntrant и AddressList
            entrant_choice = session.query(EntrantChoice).options(
                joinedload(EntrantChoice.add_entrant).joinedload(AddEntrant.address_list).joinedload(
                    AddressList.addresses)
            ).get(entrant_choice_id)

            if not entrant_choice:
                print("EntrantChoice not found")
                return

            # Вывод информации о EntrantChoice
            print(f"EntrantChoice ID: {entrant_choice.id}")
            print(f"GUID: {entrant_choice.guid}")
            print(f'JSON: {entrant_choice.json_data}')
            print(f'XML: {entrant_choice.xml_data}')

            # Вывод информации о AddEntrant
            if entrant_choice.add_entrant:
                add_entrant = entrant_choice.add_entrant
                print(f"AddEntrant ID: {add_entrant.id}")
                print(f"SNILS: {add_entrant.snils}")
                print(f"Gender ID: {add_entrant.id_gender}")
                print(f"Birthday: {add_entrant.birthday}")
                print(f"Birthplace: {add_entrant.birthplace}")
                print(f"Phone: {add_entrant.phone}")
                print(f"Email: {add_entrant.email}")
                print(f"OKSM ID: {add_entrant.id_oksm}")

                # Вывод адресов
                for address_list in add_entrant.address_list:
                    for address in address_list.addresses:
                        print(f"Address ID: {address.id}")
                        print(f"Full Address: {address.full_addr}")
                        print(f"City: {address.city}")
                        print(f"Is Registration: {address.is_registration}")
                        print(f"Region ID: {address.id_region}")

        except Exception as e:
            print("Ошибка при получении данных:", e)
            return e
        finally:
            session.close()

    get_entrant_choice_with_addresses(id)


if __name__ == "__main__":
    cli()
