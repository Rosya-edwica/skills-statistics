package headhunter

import (
	"fmt"
	"sync"

	"github.com/Rosya-edwica/skills-scraper/src/logger"
	"github.com/Rosya-edwica/skills-scraper/src/models"
	"github.com/Rosya-edwica/skills-scraper/src/mysql"
	"github.com/tidwall/gjson"
)

func GetVacanciesByQuery(city models.City, profession models.Profession) {
	url := CreateLink(profession.Title, city.HH_ID)
	checkCaptcha(url)
	json, err := GetJson(url)
	if err != nil {
		logger.Log.Printf("Ошибка при подключении к странице с вакансиями: %s. Error: %s", err, url)
		return
	}
	pagesCount := gjson.Get(json, "pages").Int()
	found := gjson.Get(json, "found").Int()
	if found > 2000 && city.Name == "Russia" {
		logger.Log.Printf("Профессия: %s | Город: %s | Найдено: %d", profession.Title, city.Name, found)
		logger.Log.Printf("Найдено вакансий свыше 2000. Поэтому будет вестись поиск по отдельным городам для этой профессии")
		parseProfessionByCurrentCity(profession)
		return
	} else {
		logger.Log.Printf("Профессия: %s | Город: %s | Найдено: %d", profession.Title, city.Name, found)
		for page := 0; page < int(pagesCount); page++ {
			ParseVacanciesFromPage(fmt.Sprintf("%s&page=%d", url, page), city.EDWICA_ID, profession.Id)
		}
		return
	}

}

func ParseVacanciesFromPage(url string, city_edwica int, id_profession int) {
	json, err := GetJson(url)
	if err != nil {
		logger.Log.Printf("Не удалось подключиться к странице %s.\nТекст ошибки: %s", err, url)
		return
	}

	items := gjson.Get(json, "items").Array()
	var wg sync.WaitGroup
	wg.Add(int(len(items)))
	for _, item := range items {
		go scrapeVacancy(item.Get("url").String(), city_edwica, id_profession, &wg)
	}
	wg.Wait()
	return
}

func parseProfessionByCurrentCity(profession models.Profession) {
	logger.Log.Printf("Ищем профессию `%s`", profession.Title)
	groups := groupCities()
	for _, group := range groups {
		var wg sync.WaitGroup
		wg.Add(len(group))
		for _, city := range group {
			go parseProfessionInCity(city, profession, &wg)
		}
		wg.Wait()
	}
	mysql.SetParsedStatusToProfession(profession.Id)
	logger.Log.Printf("Профессия %s спарсена", profession.Title)

}

func groupCities() (groups [][]models.City) {
	cities := mysql.GetCities()
	citiesCount := len(cities)
	var limit int
	for i := 0; i < citiesCount; i += GroupSize {
		limit += GroupSize
		if limit > citiesCount {
			limit = citiesCount
		}
		group := cities[i:limit]
		groups = append(groups, group)
	}
	logger.Log.Printf("Ведем поиск профессии в  %d городах одновременно", GroupSize)
	return
}

func parseProfessionInCity(city models.City, profession models.Profession, wg *sync.WaitGroup) {
	defer wg.Done()
	GetVacanciesByQuery(city, profession)
}
