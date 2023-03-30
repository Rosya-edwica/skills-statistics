package headhunter

import (
	"errors"
	"github.com/Rosya-edwica/skills-scraper/src/logger"
	"github.com/Rosya-edwica/skills-scraper/src/models"
	"github.com/Rosya-edwica/skills-scraper/src/mysql"
)

const GroupSize = 1

func Go() {
	defaultCity := models.City{
		HH_ID:        0,
		EDWICA_ID:    1,
		RABOTA_RU_ID: "russia",
		Name:         "Russia",
	}
	professions := mysql.GetProfessions()
	if len(professions) == 0 {
		checkErr(errors.New("Пустой список профессий. Нечего искать"))
	}
	for _, profession := range professions {
		// parseProfessionByCurrentCity(profession)
		logger.Log.Printf("Ищем профессию `%s`", profession.Title)
		GetVacanciesByQuery(defaultCity, profession)
		mysql.SetParsedStatusToProfession(profession.Id)
		logger.Log.Printf("Профессия %s спарсена", profession.Title)

	}
}
