from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Boolean,
    ForeignKey,
    JSON,
    TEXT
)
from .database import Base


class EntrantChoice(Base):
    __tablename__ = 'entrant_choices'
    id = Column(Integer, primary_key=True)
    guid = Column(String(36), nullable=True)
    json_data = Column(JSON, nullable=True)
    xml_data = Column(TEXT, nullable=True)
    add_entrant_id = Column(Integer, ForeignKey('add_entrants.id'))
    add_entrant = relationship("AddEntrant", back_populates="entrant_choice")


class AddEntrant(Base):
    __tablename__ = 'add_entrants'
    id = Column(Integer, primary_key=True)
    snils = Column(String(11), nullable=True)
    id_gender = Column(Integer, nullable=False)
    birthday = Column(Date, nullable=False)
    birthplace = Column(String(500), nullable=False)
    phone = Column(String(120), nullable=True)
    email = Column(String(150), nullable=True)
    id_oksm = Column(Integer, nullable=False)

    identification_id = Column(Integer, ForeignKey('identifications.id'))
    identification = relationship("Identification", back_populates="add_entrant")

    address_list = relationship("AddressList", back_populates="add_entrant", cascade="all, delete-orphan", uselist=True)

    entrant_choice = relationship("EntrantChoice", back_populates="add_entrant")


class AddressList(Base):
    __tablename__ = 'address_lists'
    id = Column(Integer, primary_key=True)

    add_entrant_id = Column(Integer, ForeignKey('add_entrants.id'))
    add_entrant = relationship("AddEntrant", back_populates="address_list")

    addresses = relationship("Address", back_populates="address_list", cascade="all, delete-orphan")


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)

    is_registration = Column(Boolean, nullable=True)
    full_addr = Column(String(1024), nullable=False)
    id_region = Column(Integer, nullable=True)
    city = Column(String(255), nullable=True)

    # Внешний ключ на AddressList
    address_list_id = Column(Integer, ForeignKey('address_lists.id'))
    address_list = relationship("AddressList", back_populates="addresses")


class Identification(Base):
    __tablename__ = 'identifications'
    id = Column(Integer, primary_key=True)
    id_document_type = Column(Integer, nullable=False)
    doc_name = Column(String(255), nullable=True)
    doc_series = Column(String(20), nullable=True)
    doc_number = Column(String(50), nullable=False)
    issue_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    passport_uuid = Column(String(500), nullable=True)
    doc_organization = Column(String(500), nullable=False)
    passport_org_code = Column(String(500), nullable=True)
    passport_type_id = Column(Integer, nullable=True)
    user_id = Column(Integer, nullable=False)
    first_name = Column(String(500), nullable=False)
    second_name = Column(String(500), nullable=False)
    middle_name = Column(String(500), nullable=True)
    add_entrant = relationship("AddEntrant", back_populates="identification")
