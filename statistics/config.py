from dotenv import load_dotenv
import os
from typing import NamedTuple

loaded_env = load_dotenv('.env')
if not load_dotenv:
    exit("Пустые переменные окружения")

    
class __Settings(NamedTuple):
    Host:       str
    Port:       str
    Database:   str
    User:       str
    Password:   str
    
SETTINGS = __Settings(
    Host=os.getenv('HOST_MYSQL'),
    Port=int(os.getenv('PORT_MYSQL')),
    Database=os.getenv('DATABASE_MYSQL'),
    User=os.getenv('USER_MYSQL'),
    Password=os.getenv('PASSWORD_MYSQL'),
    )

PROFESSION_TABLE = 'h_skills_position'
VACANCY_TABLE = 'h_skills_vacancy'
