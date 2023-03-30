package main

import (
	"fmt"
	"time"

	"github.com/Rosya-edwica/skills-scraper/src/platform/headhunter"
	"github.com/Rosya-edwica/skills-scraper/src/telegram"
)

func main() {
	start := time.Now().Unix()
	headhunter.Go()
	telegram.Mailing(fmt.Sprintf("Время выполнения программы: %d секунд", time.Now().Unix()-start))
}
