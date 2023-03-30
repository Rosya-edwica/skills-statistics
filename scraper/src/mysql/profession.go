package mysql

import (
	"fmt"
	"github.com/Rosya-edwica/skills-scraper/src/models"
)

func SetParsedStatusToProfession(id int) {
	db := connect()
	defer db.Close()

	query := fmt.Sprintf(`update %s set parsed=true where id=%d`, TableProfessions, id)
	fmt.Println(query)
	tx, _ := db.Begin()
	_, err := db.Exec(query)
	checkErr(err)
	tx.Commit()
}

func GetProfessions() (professions []models.Profession) {
	db := connect()
	defer db.Close()

	query := fmt.Sprintf("SELECT id, name, level FROM %s WHERE parsed = false", TableProfessions)
	rows, err := db.Query(query)
	checkErr(err)
	defer rows.Close()
	for rows.Next() {
		var (
			name      string
			id, level int
		)
		err = rows.Scan(&id, &name, &level)
		checkErr(err)
		prof := models.Profession{
			Id:    id,
			Title: name,
			Level: level,
		}
		professions = append(professions, prof)

	}
	return
}
