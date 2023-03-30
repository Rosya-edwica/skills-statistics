from csv_file import get_professions_from_csv
from mysql_file import move_professions_to_mysql

from pprint import pprint

import os

def main():
    directory = "files"
    for file in os.listdir(directory):
        if file == "Вариации написаний - Менеджер туризма.csv":
            area = "Туризм"
        elif file == "Вариации написаний - Автослесарь.csv":
            area = "Автомобилестроение"            
        if not file.endswith(".csv"): continue
        professions = get_professions_from_csv(csv_file=os.path.join(directory, file))
        move_professions_to_mysql(professions, area)

if __name__ == "__main__": 
    main()