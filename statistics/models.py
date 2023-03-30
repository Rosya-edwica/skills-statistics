from typing import NamedTuple


class Profession(NamedTuple):
    PositionId:     int
    Name:           str
    Level:          int
    Skills:         str  # skill_1|skill_2|skill_3
    Experience:     str
    WeightInLevel:  int
    Area:           str

class WeightProfession(NamedTuple):
    Name:           str
    Level:          int
    Area:           str

class Skill(NamedTuple):
    Level:          int
    Name:           str
    Count:          int
    
class ProfessionStatistics(NamedTuple):
    Profession:     int
    Level:          int
    Skills:         list[Skill]


class SimilarSkills(NamedTuple):
    Name: str
    OtherNames: list[str]