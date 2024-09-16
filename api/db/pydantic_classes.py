from pydantic import BaseModel, Field, AliasChoices, SkipValidation
from typing import List, Optional
from datetime import date


# ИСПОЛЬЗОВАТЬ validation_alias=AliasChoices('name1', 'name2') для первичной и вторичной валидации.
# Также исправить все классы ниже по прототипу из sql_classes


class DataJsonXml(BaseModel):
    id_document_type: int = Field(None, validation_alias=AliasChoices("IdDocumentType", "id_document_type", 'DocumentTypeID'))
    doc_name: Optional[str] = Field(None, validation_alias=AliasChoices("DocName", "passport_name_text", 'PassportNameText'), min_length=1,
                                    max_length=255)
    doc_series: Optional[str] = Field(None, validation_alias=AliasChoices("DocSeries", "passport_series", 'Series'), min_length=1,
                                      max_length=20)
    doc_number: str = Field(..., validation_alias=AliasChoices("DocNumber", "passport_number", 'Number'), min_length=1,
                            max_length=50)
    issue_date: date = Field(..., validation_alias=AliasChoices("passport_begda", "IssueDate", 'BeginDate'))
    end_date: Optional[date] = Field(None, validation_alias=AliasChoices("EndDate", "passport_endda", 'EndDate'))
    passport_uuid: Optional[str] = Field(None, validation_alias=AliasChoices("PassportUUID", "passport_uuid"),
                                         max_length=500)
    doc_organization: str = Field(..., validation_alias=AliasChoices("passport_issued_by", "DocOrganization", 'IssuedBy'), min_length=1,
                                  max_length=500)
    passport_org_code: Optional[str] = Field(None,
                                             validation_alias=AliasChoices("PassportOrgCode", "passport_org_code", 'OrgCode'))
    passport_type_id: int = Field(..., validation_alias=AliasChoices("passport_type_id", "PassportTypeId", 'PassportTypeID'))
    user_id: int = Field(..., validation_alias=AliasChoices("user_id", "UserId", 'UserID'))
    first_name: str = Field(..., validation_alias=AliasChoices("first_name", "FirstName"))
    second_name: str = Field(..., validation_alias=AliasChoices("second_name", "SecondName"))
    middle_name: Optional[str] = Field(None, validation_alias=AliasChoices("MiddleName", "middle_name"))

    # AddEntrantSchema
    snils: Optional[str] = Field(None, validation_alias=AliasChoices("Snils", "snils", 'SNILS'), length=11, pattern=r"\d{11}")
    id_gender: int = Field(..., validation_alias=AliasChoices('IdGender', 'dict_sex_id', 'SexID'))
    birthday: date = Field(..., validation_alias=AliasChoices('birthday', 'Birthday'))
    birthplace: str = Field(..., validation_alias=AliasChoices('birthplace', 'motherland', "Birthplace", 'Motherland'), min_length=1,
                            max_length=500)
    phone: Optional[str] = Field(None, validation_alias=AliasChoices("Phone", "tel_mobile", 'MobileTel'), min_length=1,
                                 max_length=120)
    email: Optional[str] = Field(None, validation_alias=AliasChoices("Email", "email"), min_length=1, max_length=150)
    id_oksm: int = Field(..., validation_alias=AliasChoices('citizenship_id', 'IdOksm', 'CitizenshipID'))

    is_registration_1: bool = Field(None, validation_alias=AliasChoices("IsRegistration1", "has_another_living_address"))
    full_addr_1: str = Field(..., validation_alias=AliasChoices('address_txt1', 'FullAddr1', 'AddressLine1'), min_length=1, max_length=1024)
    id_region_1: Optional[str] = Field(None, validation_alias=AliasChoices("IdRegion1"))
    city_1: Optional[str] = Field(None, validation_alias=AliasChoices("City1"), min_length=1, max_length=255)

    is_registration_2: bool = Field(None, validation_alias=AliasChoices("IsRegistration2", "has_another_living_address"))
    full_addr_2: Optional[str] = Field(None, validation_alias=AliasChoices('address_txt2', 'FullAddr2', 'AddressLine2'), min_length=1, max_length=1024)
    id_region_2: Optional[str] = Field(None, validation_alias=AliasChoices("IdRegion2"))
    city_2: Optional[str] = Field(None, validation_alias=AliasChoices("City2"), min_length=1, max_length=255)

    is_registration_3: bool = Field(None, validation_alias=AliasChoices("IsRegistration3", "has_another_living_address"))
    full_addr_3: Optional[str] = Field(None, validation_alias=AliasChoices('address_txt3', 'FullAddr3', 'AddressLine3'), min_length=1, max_length=1024)
    id_region_3: Optional[str] = Field(None, validation_alias=AliasChoices("IdRegion3"))
    city_3: Optional[str] = Field(None, validation_alias=AliasChoices("City3"), min_length=1, max_length=255)

    is_registration_4: bool = Field(None, validation_alias=AliasChoices("IsRegistration_4", "has_another_living_address"))
    full_addr_4: Optional[str] = Field(None, validation_alias=AliasChoices('address_txt4', 'FullAddr4', 'AddressLine4'), min_length=1, max_length=1024)
    id_region_4: Optional[str] = Field(None, validation_alias=AliasChoices("IdRegion4"))
    city_4: Optional[str] = Field(None, validation_alias=AliasChoices("City4"), min_length=1, max_length=255)

    second_is_registration_1: bool = Field(None, validation_alias=AliasChoices("SecondIsRegistration1", "has_another_living_address"))
    second_full_addr_1: Optional[str] = Field(None, validation_alias=AliasChoices('second_address_txt1', 'SecondFullAddr1', 'SecondAddressLine1'), min_length=1, max_length=1024)
    second_id_region_1: Optional[str] = Field(None, validation_alias=AliasChoices("SecondIdRegion1"))
    second_city_1: Optional[str] = Field(None, validation_alias=AliasChoices("SecondCity1"), min_length=1, max_length=255)

    second_is_registration_2: bool = Field(None, validation_alias=AliasChoices("SecondIsRegistration2", "has_another_living_address"))
    second_full_addr_2: Optional[str] = Field(None, validation_alias=AliasChoices('second_address_txt2', 'SecondFullAddr2', 'SecondAddressLine2'), min_length=1, max_length=1024)
    second_id_region_2: Optional[str] = Field(None, validation_alias=AliasChoices("SecondIdRegion2"))
    second_city_2: Optional[str] = Field(None, validation_alias=AliasChoices("SecondCity2"), min_length=1, max_length=255)

    second_is_registration_3: bool = Field(None, validation_alias=AliasChoices("SecondIsRegistration3", "has_another_living_address"))
    second_full_addr_3: Optional[str] = Field(None, validation_alias=AliasChoices('second_address_txt3', 'SecondFullAddr3', 'SecondAddressLine3'), min_length=1, max_length=1024)
    second_id_region_3: Optional[str] = Field(None, validation_alias=AliasChoices("SecondIdRegion3"))
    second_city_3: Optional[str] = Field(None, validation_alias=AliasChoices("SecondCity3"), min_length=1, max_length=255)

    second_is_registration_4: bool = Field(None, validation_alias=AliasChoices("SecondIsRegistration4", "has_another_living_address"))
    second_full_addr_4: Optional[str] = Field(None, validation_alias=AliasChoices('second_address_txt4', 'SecondFullAddr4', 'SecondAddressLine4'), min_length=1, max_length=1024)
    second_id_region_4: Optional[str] = Field(None, validation_alias=AliasChoices("SecondIdRegion4"))
    second_city_4: Optional[str] = Field(None, validation_alias=AliasChoices("SecondCity4"), min_length=1, max_length=255)

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
