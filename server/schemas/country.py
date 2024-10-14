from datetime import date

from pydantic import BaseModel


class CountryBase(BaseModel):
    name: str
    official_name: str
    wiki: str
    md_file: str

    class Config:
        from_attributes = True


class CountryDisplay(BaseModel):
    id: int
    name: str
    official_name: str

    class Config:
        from_attributes = True


# Country Schema
class DayCountryBase(BaseModel):
    country_id: int

    class Config:
        from_attributes = True


class DayCountryDisplay(DayCountryBase):
    id: int
    country: CountryDisplay | None
    date: date

    class Config:
        from_attributes = True


class CountryCount(BaseModel):
    id: int
    name: str
    count: int
    last: date | None

    class Config:
        from_attributes = True
