package models

type VacancySkills struct {
	Title        string
	Url          string
	ProfessionId int
	CityId       int
	Skills       string
	Experience   string
}

type City struct {
	HH_ID        int
	EDWICA_ID    int
	RABOTA_RU_ID string
	Name         string
}

type Profession struct {
	Id    int
	Title string
	Level int
}
