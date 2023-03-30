import db
from engine import Statistics

def main():
    areas = db.get_areas()
    way = input("\n".join((
        "Построить статистику по всем профотраслям или по какой-то конкретной?",
        "0. Построить по всем профобластям",
        "1. Построить по одной профобласти",
        "2. Выйти",
        ">>> ",
    )))
    match way:
        case "0":
            for area in areas:
                run(area)
        case "1":
            print("Для какой профобласти построить статистику? (Выбери число)")
            for index, area in enumerate(areas):
                print(f"{index}. {area}")
            print(f"{index+1}. Выйти")
            area = input(">>> ")
            try:
                run(prof_area=areas[int(area)])
            except:
                exit("Пока!")
        case _:
            exit("Пока!")
                
    
def run(prof_area: int):
    print(f"Строим статистику по: {prof_area}")
    filename = f"result/{prof_area}.xlsx"
    professions = db.get_professions_with_skills(area=prof_area)
    if len(professions) == 0:
        print(f"Для профобласти '{prof_area}' не нашлось ни одной профессии")
        return 
    
    weight_professions = db.get_weight_professions(area=prof_area)
    statistics = Statistics(professions, weight_professions)
    result = statistics.build()
    db.save_statistics(result, filename)
    print(f"Закончили строить статистику! Результат здесь: {filename}")


if __name__ == "__main__":
    main()
