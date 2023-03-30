package headhunter

import (
	"fmt"
	"strings"
	"sync"

	"github.com/tidwall/gjson"

	"github.com/Rosya-edwica/skills-scraper/src/logger"
	"github.com/Rosya-edwica/skills-scraper/src/models"
	"github.com/Rosya-edwica/skills-scraper/src/mysql"
)

func scrapeVacancy(url string, city_edwica int, id_profession int, wg *sync.WaitGroup) {
	var vacancy models.VacancySkills
	checkCaptcha(url)
	json, err := GetJson(url)
	if err != nil {
		logger.Log.Printf("Ошибка при подключении к странице %s.\nТекст ошибки: %s", err, url)
		wg.Done()
		return
	}

	vacancy.CityId = city_edwica
	vacancy.ProfessionId = id_profession
	vacancy.Skills = getSkills(json)
	vacancy.Title = gjson.Get(json, "name").String()
	vacancy.Url = gjson.Get(json, "alternate_url").String()
	vacancy.Experience = gjson.Get(json, "experience.name").String()
	mysql.SaveOneVacancy(vacancy)
	wg.Done()
}

func getSkills(vacancyJson string) string {
	var skills []string
	for _, item := range gjson.Get(vacancyJson, "key_skills").Array() {
		skills = append(skills, item.Get("name").String())
	}
	languages := getLanguages(vacancyJson)
	skills = append(skills, languages...)
	return strings.Join(skills, "|")
}

func getLanguages(vacancyJson string) (languages []string) {
	for _, item := range gjson.Get(vacancyJson, "languages").Array() {
		lang := item.Get("name").String()
		level := item.Get("level.name").String()
		languages = append(languages, fmt.Sprintf("%s (%s)", lang, level))
	}
	return
}

func GetExperience(vacancyId string) (experience string) {
	url := "https://api.hh.ru/vacancies/" + vacancyId
	json, err := GetJson(url)
	if err != nil {
		logger.Log.Printf("Ошибка при подключении к странице %s.\nТекст ошибки: %s", err, url)
		return
	}
	experience = gjson.Get(json, "experience.name").String()
	return
}
