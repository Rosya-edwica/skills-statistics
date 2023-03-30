import logging
import csv

from models import SimilarSkills


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, filename="info.log", filemode="w")

class Cleaner:
    def __init__(self, stop_skills_path: str = "engine/data/stop_skills.csv", similar_skills_path: str = "engine/data/similar_skills.csv") -> list[str]:
        self.stop_skills_path = stop_skills_path
        self.similar_skills_path = similar_skills_path
        
        self.stop_skills = self.__load_stop_skills()
        self.similar_skills = self.__load_similar_skills()
        
    def run(self, skills: list[str]):
        self.skills = skills
        self.skills = self.__separate_by_comma()
        self.skills = self.__remove_prefixs()
        self.skills = self.__rename_similar()
        self.skills = self.__remove_stop_skills()

    def __separate_by_comma(self) -> list[str]:
        logging.info("Делим навыки по запятым")
        updated: list[str] = []
        for item in self.skills:
            separated = item.split(',')
            if len(separated) == 1:
                updated += item.split(';')
            else:
                updated += separated
                logging.info(f'Разбили навык по частям! "{item}"')
        
        return updated
    
    def __remove_prefixs(self) -> list[str]:
        logging.info("Удаляем лишние символы в приставке навыка")
        symbols = {
            "—",
            "-",
            "●",
            "*",
            " ",
        }
        updated: list[str] = []
        for item in self.skills:
            try: 
                skill = next(item.removeprefix(sym) for sym in symbols if sym in item)
            except StopIteration: 
                skill = item
            finally:
                updated.append(skill)
        return updated
    
    def __rename_similar(self):
        logging.info("Переименовываем навыки")
        updated: list[str] = []
        for skill in self.skills:
            new_name = skill
            for similar in self.similar_skills:
                if self.__is_foreign_language(skill):
                    new_name = "иностранный язык"  
                    logging.info(f'Переименовали навык "{skill}" -> "{new_name}" ')
                    break
                elif skill.lower() in similar.OtherNames:
                    new_name = similar.Name
                    logging.info(f'Переименовали навык "{skill}" -> "{new_name}" ')
                    break
            updated.append(new_name)
        return updated
    
    def __is_foreign_language(self, skill: str) -> str:
        foreign_languages = SimilarSkills(
            Name="иностранный язык",
            OtherNames=[
                "казахский",
                "итальянский",
                "испанский",
                "китайский",
                "японский",
                "турецкий",
            ]
        )
        for language in foreign_languages.OtherNames:
            if language in skill:
                return True
        return False
    
    def __remove_stop_skills(self) -> list[str]:
        logging.info("Удаляем стоп-навыки")
        updated: list[str] = []
        for skill in self.skills:
            if (skill.lower() not in self.stop_skills) and ("опыт" not in skill.lower()):
                updated.append(skill.lower())
            else:
                logging.info(f'Вырезали навык "{skill}"')
        return updated
    
    def __load_stop_skills(self) -> list[str]:
        stop_words: list[str] = []
        with open(self.stop_skills_path, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.reader(file, delimiter=",")
            for item in reader:
                stop_words.append(item[0].strip().lower())
        return stop_words

    def __load_similar_skills(self) -> list[SimilarSkills]:
        similar_skills: list[SimilarSkills] = [] 
        with open(self.similar_skills_path, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.reader(file, delimiter=";")
            for index, item in enumerate(reader):
                if index == 0: continue
                similar_skills.append(SimilarSkills(
                    Name=item[0].strip().lower(),
                    OtherNames=item[1].lower().split("|"),
                ))
        return similar_skills
        
