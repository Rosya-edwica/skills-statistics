import csv
from config import *


def get_professions_from_csv(csv_file: str):
    professions: list[CsvProfession] = []
    with open(csv_file, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file, delimiter=",")
        for index, row in enumerate(reader):
            if index == 0: continue
            profession = CsvProfession(Name=row[COLUMN_PROFESSION].lower(), Level=row[COLUMN_LEVEL], Weigth=int(row[COLUMN_WEIGHT]))
            if profession not in professions:
                professions.append(profession)
    return professions