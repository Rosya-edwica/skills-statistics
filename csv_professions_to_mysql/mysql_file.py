import pymysql

from config import SETTINGS, CsvProfession

def connect_to_mysql() -> pymysql.Connection:
    try:
        connect = pymysql.connect(
            host=SETTINGS.Host,
            port=int(SETTINGS.Port),
            database=SETTINGS.Database,
            user=SETTINGS.User,
            password=SETTINGS.Password,
        )
        return connect
    except BaseException as err:
        exit(err)

def move_professions_to_mysql(data: list[CsvProfession], area: str):
    connect = connect_to_mysql()
    with connect.cursor() as cursor:
        for item in data:
            try:
                cursor.execute(f"INSERT INTO h_skills_position(name, level, area, weight_in_level) VALUES('{item.Name}', {item.Level}, '{area}', {item.Weigth})")
                connect.commit()
            except BaseException as err:
                print(err)