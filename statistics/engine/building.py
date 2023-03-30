from models import Profession, Skill, ProfessionStatistics, WeightProfession
from collections import Counter
from .cleaning import Cleaner

from typing import NamedTuple
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

class LevelSeparation(NamedTuple):
    Level: int
    Professions: list[Profession]

class Statistics:
    def __init__(self, professionsList: list[Profession], weightProfessionsList: list[WeightProfession], clear_skills: bool = True):
        self.ProfessionsList = professionsList
        self.WeightProfessionsList = weightProfessionsList
        self.clear_skills = clear_skills
        logging.info("Подготовили профессии для обработки")
        self.cleaner = Cleaner()
        
        

    def build(self) -> list[ProfessionStatistics]:
        result: list[ProfessionStatistics] = []
        self.ProfessionsList = self.__update_level_for_zero_professions()
        separation_by_levels = self.__separate_professions_by_levels(self.ProfessionsList)
        for separation in separation_by_levels:
            skills = self.__count_the_skills_of_the_level(separation)
            main_profession_in_level = next(prof.Name for prof in self.WeightProfessionsList if prof.Level==separation.Level)
            result.append(ProfessionStatistics(
                Level=separation.Level,
                Skills=skills,
                Profession=main_profession_in_level
            ))
        return result
    
    def __update_level_for_zero_professions(self) -> list[Profession]:
        professions_without_zero_level: list[Profession] = []
        for profession in self.ProfessionsList:
            if profession.Level == 0:
                updated_profession = self.__set_level_by_experience(zero_profession=profession)
                professions_without_zero_level.append(updated_profession)
            else:
                professions_without_zero_level.append(profession)
                
        logging.info("Переименовали нулевые профессии согласно их опыту")
        return professions_without_zero_level
    
    def __separate_professions_by_levels(self, professions: list[Profession]) -> list[LevelSeparation]:
        separation: list[LevelSeparation] = []

        for profession in professions:
            added = False
            for item in separation:
                if item.Level == profession.Level:
                    item.Professions.append(profession)
                    added = True
                    break
            if not added:
                separation.append(LevelSeparation(Level=profession.Level, Professions=[profession, ]))
                
        logging.info("Разделили профессии на группы по уровням")
        return separation                  
    
    def __count_the_skills_of_the_level(self, separation:LevelSeparation) -> list[Skill]:
        result: list[Skill] = []
        if self.clear_skills:
            profession_skills = self.cleaner.run(self.__get_skills(separation.Professions))
        else:
            profession_skills = self.__get_skills(separation.Professions)
        
        counter = Counter(profession_skills).most_common()
        skills = [item[0] for item in counter]
        count = [item[1] for item in counter]
        
        for index in range(len(skills)):
            if self.clear_skills:
                if count[index] <= 3: continue
            result.append(Skill(
                Level=separation.Level,
                Name=skills[index],
                Count=count[index]
            ))
            
        logging.info(f"Подсчитали навыки для уровня {separation.Level}")            
        return result
        
    def __set_level_by_experience(self, zero_profession: Profession) -> Profession:
        match zero_profession.Experience:
            case "Нет опыта": level = 1
            case "От 1 года до 3 лет": level = 2
            case "От 3 до 6 лет": level = 3
            case "Более 6 лет": level = 4

        return Profession(
            Name=next(profession.Name for profession in self.WeightProfessionsList if profession.Level == level and profession.Area == zero_profession.Area),
            Level=level,
            Area=zero_profession.Area,
            Skills=zero_profession.Skills,
            PositionId=zero_profession.PositionId,
            Experience=zero_profession.Experience,
            WeightInLevel=zero_profession.WeightInLevel,
        )
        
    def __get_skills(self, professions: list[Profession]) -> list[str]:
        skills: list[str] = []
        for item in professions:
            item_skills = item.Skills.lower().strip().removeprefix(" ").removesuffix(" ").split("|")
            skills += item_skills
        return skills
