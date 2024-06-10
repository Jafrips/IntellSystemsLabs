from collections import defaultdict
import random

from exercises import exercises
from input import min_exercises_per_day
from input import max_exercises_per_day
from input import weekly_muscle_group_goals


# Распределение упражнений по группам мышц
muscle_groups = defaultdict(list)
for exercise in exercises:
    muscle_groups[exercise["muscle_group"]].append(exercise["name"])

# Проверка целей и корректировка
for group, goal in weekly_muscle_group_goals.items():
    if goal > len(muscle_groups[group]):
        weekly_muscle_group_goals[group] = len(muscle_groups[group])

# Распределение по дням недели
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
schedule = defaultdict(list)

# Функция для распределения упражнений
def distribute_exercises():
    remaining_exercises = {group: random.sample(ex_list, k=weekly_muscle_group_goals[group])
                           for group, ex_list in muscle_groups.items() if group != "Кардио"}

    while any(remaining_exercises.values()):
        day_exercises = []

        for group, exercises in list(remaining_exercises.items()):
            if not exercises:
                continue

            if len(day_exercises) < min_exercises_per_day:
                day_exercises.append(exercises.pop())

        if day_exercises:
            available_days = [day for day in days_of_week if len(schedule[day]) + len(day_exercises) <= max_exercises_per_day]
            if available_days:
                chosen_day = random.choice(available_days)
                schedule[chosen_day].extend(day_exercises)

    # Проверка на минимальное количество упражнений в день и добавление кардио
    for day in days_of_week:
        if 0 < len(schedule[day]) < min_exercises_per_day:
            schedule[day].append(random.choice(muscle_groups["Кардио"]))

# Вызов функции распределения упражнений
distribute_exercises()

# Вывод расписания тренировок
for day in days_of_week:
    if day in schedule and schedule[day]:
        print(f"Тренировка на {day}:")
        for exercise in schedule[day]:
            for muscle_group, ex_list in muscle_groups.items():
                if exercise in ex_list:
                    print(f"{exercise} ({muscle_group})")
        print()
    else:
        print(f"{day} - отдых\n")
