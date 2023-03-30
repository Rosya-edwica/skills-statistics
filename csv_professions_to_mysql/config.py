from typing import NamedTuple
from dotenv import load_dotenv
import os

env_is_loaded = load_dotenv("../.env")

COLUMN_LEVEL = 1
COLUMN_PROFESSION = 3
COLUMN_WEIGHT = 2

class CsvProfession(NamedTuple):
    Name:   str
    Level:  int
    Weigth: int

class __Settings(NamedTuple):
    Host: str
    Port: str
    Database: str
    User: str
    Password: str


SETTINGS = __Settings(
    Host=os.getenv("MYSQL_HOST"),
    Port=os.getenv("MYSQL_PORT"),
    Database=os.getenv("MYSQL_DATABASE"),
    User=os.getenv("MYSQL_USER"),
    Password=os.getenv("MYSQL_PASSWORD"),
)