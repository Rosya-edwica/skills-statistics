import pymysql
from pymysql.connections import Connection
from pymysql.cursors import DictCursor

from models import *
from config import SETTINGS, PROFESSION_TABLE, VACANCY_TABLE

def connection() -> Connection:
    try:
        connect = pymysql.connect(
            host=SETTINGS.Host,
            port=SETTINGS.Port,
            database=SETTINGS.Database,
            user=SETTINGS.User,
            password=SETTINGS.Password,
            cursorclass=DictCursor
        )
        return connect
    except BaseException as err:
        exit(err)


def get_professions_with_skills(area: str) -> list[Profession]:
    connect = connection()
    query = f"""SELECT {PROFESSION_TABLE}.id, {PROFESSION_TABLE}.name,
                {PROFESSION_TABLE}.level, {VACANCY_TABLE}.skills, {VACANCY_TABLE}.experience, {PROFESSION_TABLE}.weight_in_level, {PROFESSION_TABLE}.area
            FROM {VACANCY_TABLE}
            LEFT JOIN {PROFESSION_TABLE} ON {VACANCY_TABLE}.position_id={PROFESSION_TABLE}.id
            WHERE {VACANCY_TABLE}.skills != '' and area='{area}'
            """
    with connect.cursor() as cursor:
        cursor.execute(query)
        result = [Profession(*row.values()) for row in cursor.fetchall()]
    return result



def get_weight_professions(area: str) -> list[WeightProfession]:
    connect = connection()
    query = f"SELECT name, level, area FROM {PROFESSION_TABLE} WHERE weight_in_level = 1 AND area='{area}'"
    with connect.cursor() as cursor:    
        cursor.execute(query)
        result = [WeightProfession(*row.values()) for row in cursor.fetchall()]
    return result



def get_areas() -> list[str]:
    connect = connection()
    query = f"SELECT DISTINCT area FROM {PROFESSION_TABLE}"
    with connect.cursor() as cursor:
        cursor.execute(query)
        areas = [list(item.values())[0] for item in cursor.fetchall()]
    return areas