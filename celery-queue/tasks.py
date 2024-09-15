import os
import time
from xml.parsers.expat import ExpatError
from celery import Celery, chain
from db.sql_classes import (
    Base,
    Identification,
    Address,
    AddressList,
    AddEntrant,
    EntrantChoice
)
from db.pydantic_classes import DataJsonXml
from db.database import Session, engine
import json
import logging
from pydantic import ValidationError
from sqlalchemy.orm import joinedload

import xmltodict
import xml.etree.ElementTree as ET
from datetime import datetime, date


CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
RESULT_BACKEND = os.environ.get("RESULT_BACKEND")

celery = Celery("tasks", broker=CELERY_BROKER_URL, backend=RESULT_BACKEND)
celery.conf.update(imports=["tasks"])
celery.conf.update(
    worker_hijack_root_logger=False,
    task_send_sent_event=True
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


@celery.task(name="tasks.run_chair")
def run_chair(data):
    try:
        return process_file(data)
    except Exception as e:
        return {"status": "error", "message": str(e)}


def convert_dates(data):
    date_fields = ["birthday", "passport_begda", "passport_endda", 'BeginDate', 'EndDate', 'Birthday']
    for field in date_fields:
        if data.get(field):
            try:
                data[field] = datetime.strptime(data[field], "%d.%m.%Y").date().isoformat()
            except ValueError:
                raise ValueError(f"Неверный формат даты в поле {field}: {data[field]}")
    return data


def sql_model_to_dict(obj, seen=None):
    """Преобразует sql модель в словарь"""
    if seen is None:
        seen = set()
    # Предотвращение циклической зависимости
    if obj in seen:
        return None
    seen.add(obj)

    result = {}
    for column in obj.__table__.columns:
        try:
            # Исключаем поле json_data
            if column.name == 'json_data' or column.name == 'xml_data':
                continue
            value = getattr(obj, column.name)
            if isinstance(value, (datetime, date)):
                result[column.name] = value.isoformat()
            else:
                result[column.name] = value
        except Exception as e:
            raise Exception(f"Ошибка при конвертации поля {column.name}: {e}")

    for relationship in obj.__mapper__.relationships:
        related_obj = getattr(obj, relationship.key)
        if related_obj is None:
            result[relationship.key] = None
        elif isinstance(related_obj, list):  # Если это список связанных объектов
            result[relationship.key] = [sql_model_to_dict(item, seen) for item in related_obj]
        else:
            # Если это один связанный объект
            result[relationship.key] = sql_model_to_dict(related_obj, seen)
    return result


def dict_to_xml(tag, d):
    """Преобразует словарь в XML"""
    elem = ET.Element(tag)
    if not isinstance(d, dict):
        raise ValueError(f"Ожидался словарь, но получен {type(d).__name__}")

    for key, val in d.items():
        try:
            if isinstance(val, dict):
                child = dict_to_xml(key, val)
                if child is not None:
                    elem.append(child)
            elif isinstance(val, list):
                for sub_elem in val:
                    if sub_elem is None:
                        continue
                    if isinstance(sub_elem, dict):
                        child = dict_to_xml(key, sub_elem)
                        if child is not None:
                            elem.append(child)
                    else:
                        raise ValueError(f"Ожидался словарь в списке, но получен {type(sub_elem).__name__}")
            elif val is not None:
                child = ET.Element(key)
                child.text = str(val)
                elem.append(child)
        except Exception as e:
            raise Exception(f"Ошибка при создании XML элемента {key}: {e}")
    return elem


@celery.task(name="tasks.save_file", soft_time_limit=10, time_limit=60)
def save_file(data):
    session = Session()
    try:
        converted_data, file_format, entrant_choice_id = data['converted_data'], data['file_format'], data[
            'entrant_choice_id']
        entrant_choice = session.query(EntrantChoice).get(entrant_choice_id)
        if file_format == 'xml':
            entrant_choice.xml_data = converted_data
        else:
            entrant_choice.json_data = converted_data
        session.add(entrant_choice)
        session.commit()
    except ValidationError as e:
        print(f'Ошибка при валидации данных: {e}')
        session.rollback()  # Откат транзакции в случае ошибки

    except ValueError as e:
        print(f'Ошибка при сохранении данных: {e}')
        session.rollback()

    except TypeError as e:
        print(f'Ошибка типа данных: {e}')

    except ExpatError as e:
        print(e)
        session.rollback()
    except Exception as e:
        print(f'Ошибка при сохранении файла в базу данных: {e}')
        session.rollback()
    finally:
        session.close()


@celery.task(name="tasks.convert_file", soft_time_limit=10, time_limit=60)
def convert_file(data):
    try:
        if data is Exception:
            raise
        entrant_choice_id, file_format = data["entrant_choice_id"], data["file_format"]
        if file_format == 'json':
            new_file_format = 'xml'
        else:
            new_file_format = 'json'
        session = Session()
        file_record = session.query(EntrantChoice).options(
            joinedload(EntrantChoice.add_entrant).joinedload(AddEntrant.address_list).joinedload(
                AddressList.addresses)
        ).get(entrant_choice_id)
        data = sql_model_to_dict(file_record.add_entrant)
        if new_file_format == 'xml':
            xml_elem = dict_to_xml('root', data)
            # Convert XML to string
            converted_data = ET.tostring(xml_elem, encoding='utf-8').decode('utf-8')
        else:
            converted_data = json.dumps(data, ensure_ascii=False)
        session.close()
        return {"converted_data": converted_data, "file_format": new_file_format,
                'entrant_choice_id': entrant_choice_id}
    except Exception as e:
        raise Exception(f'Ошибка при конвертации данных: {e}')


@celery.task
def error_handler(request, exc, traceback):
    logger.error(f'Task {request.id} raised exception: {exc}', exc_info=True)


def process_file(data):
    try:
        task_chain = chain(
            first_save.s(data).set(soft_time_limit=10, time_limit=60) |  # Первая задача: сохранение файла
            convert_file.s().set(soft_time_limit=10, time_limit=60) |  # Вторая задача: конвертация файла
            save_file.s().set(soft_time_limit=10, time_limit=60)  # Третья задача: сохранение конвертированного файла
        )
        task_chain.apply_async(link_error=error_handler.s())
        return {"status": "running", "message": "Цепочка задач запущена"}

    except Exception as e:
        print(f'Ошибка при запуске цепочки задач: {e}')
        return {"status": "error", "message": str(e)}


@celery.task(name="tasks.first_save", soft_time_limit=10, time_limit=60)
def first_save(data):
    time.sleep(2)
    session = Session()
    try:
        file_data, file_format = data["data"], data["format"]

        if file_format == 'xml':
            file_data = xmltodict.parse(file_data)
            file_data = convert_dates(file_data['Document'])
        else:
            file_data = convert_dates(file_data)
        try:
            data = DataJsonXml(**file_data)
            data = data.dict()
        except ValidationError:
            raise
        identification = Identification(
            id_document_type=data.get('id_document_type'),
            doc_name=data.get('doc_name'),
            doc_series=data.get('doc_series'),
            doc_number=data.get('doc_number'),
            issue_date=data.get('issue_date'),
            end_date=data.get('end_date'),
            passport_uuid=data.get('passport_uuid'),
            doc_organization=data.get('doc_organization'),
            passport_org_code=data.get('passport_org_code'),
            passport_type_id=data.get('passport_type_id'),
            user_id=data.get('user_id'),
            first_name=data.get('first_name'),
            second_name=data.get('second_name'),
            middle_name=data.get('middle_name')
        )
        session.add(identification)
        session.flush()

        addresses = [
            data.get('full_addr_1'),
            data.get('full_addr_2'),
            data.get('full_addr_3'),
            data.get('full_addr_4'),
            data.get('second_full_addr_1'),
            data.get('second_full_addr_2'),
            data.get('second_full_addr_3'),
            data.get('second_full_addr_4')
        ]
        add_entrant = AddEntrant(
            snils=data.get('snils'),
            id_gender=data.get('id_gender'),
            birthday=data.get('birthday'),
            birthplace=data.get('birthplace'),
            phone=data.get('phone'),
            email=data.get('email'),
            id_oksm=data.get('id_oksm'),
            identification_id=identification.id
        )

        session.add(add_entrant)
        session.flush()
        address_list = AddressList()
        session.add(address_list)
        session.flush()
        for i, addr in enumerate(addresses):
            if addr is not None:
                address = Address(
                    is_registration=i == 0 and not data.get('has_another_living_address'),
                    full_addr=addr,
                    address_list_id=address_list.id
                )
                session.add(address)
                session.flush()
                address_list.addresses.append(address)

        add_entrant.address_list.append(address_list)

        dict_data = sql_model_to_dict(add_entrant)
        if file_format == 'xml':
            xml_elem = dict_to_xml('root', dict_data)
            xml_str = ET.tostring(xml_elem, encoding='unicode')
            entrant_choice = EntrantChoice(
                add_entrant_id=add_entrant.id,
                xml_data=xml_str
            )
        else:
            json_data = json.dumps(dict_data, ensure_ascii=False)
            entrant_choice = EntrantChoice(
                add_entrant_id=add_entrant.id,
                json_data=json_data
            )

        session.add(entrant_choice)
        session.commit()
        entrant_choice_id = entrant_choice.id

        return {'entrant_choice_id': entrant_choice_id, 'file_format': file_format}
    except ExpatError:
        session.rollback()
        raise
    except ValidationError:
        session.rollback()
        raise
    except ValueError:
        session.rollback()
        raise
    except TypeError:
        session.rollback()
        raise
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()