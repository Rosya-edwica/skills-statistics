package mysql

import (
	"fmt"

	"github.com/Rosya-edwica/skills-scraper/src/logger"
	"github.com/Rosya-edwica/skills-scraper/src/models"
)

func SaveOneVacancy(v models.VacancySkills) (err error) {
	db := connect()
	defer db.Close()

	columns := buildPatternInsertValues(6)
	smt := fmt.Sprintf(`INSERT INTO %s (title, city_id, position_id, skills, url, experience) VALUES %s`, TableVacancy, columns)
	tx, _ := db.Begin()
	_, err = db.Exec(smt, v.Title, v.CityId, v.ProfessionId, v.Skills, v.Url, v.Experience)
	if err != nil {
		logger.Log.Printf("Ошибка: Вакансия %s не была добавлена в базу - %s", v.Title, err)
		err = tx.Commit()
		checkErr(err)
		db.Close()
		return
	}
	err = tx.Commit()
	checkErr(err)
	logger.Log.Printf("Успех: Вакансия %s была добавлена в базу", v.Title)
	return nil
}
