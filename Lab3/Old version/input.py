# Входные параметры

# Минимальное количество упражнений в тренировочный день
min_exercises_per_day = 3

# Максмальное количество упражнений в тренировочный день
max_exercises_per_day = 4

# Количество упражнений на КАЖДУЮ группу мышц за НЕДЕЛЮ
weekly_muscle_group_goals = {
    "Ноги": 3,
    "Грудь": 2,
    "Спина": 2,
    "Бицепс": 2,
    "Плечи": 2,
}


#### Проверки ####

# Проверка min_exercises_per_day и max_exercises_per_day
if min_exercises_per_day > max_exercises_per_day:
    raise ValueError("Минимальное количество упражнений в день не может быть больше максимального, проверьте файл input.py")
elif max_exercises_per_day < min_exercises_per_day:
    raise ValueError("Максимальное количество упражнений в день не может быть меньше минимального, проверьте файл input.py")

for muscle_group, exercises in weekly_muscle_group_goals.items():
    if exercises < 0 or exercises > 5:
        raise ValueError("Количество упражнений на каждую группу мышц должно быть в диапазоне от 0 до 5. Проверьте значения в файле input.py")
    
totalEX = sum(weekly_muscle_group_goals.values())
availableEX = max_exercises_per_day * 7
if totalEX > availableEX:
    raise ValueError(f"Вы пытаетесь распределить {totalEX} упражнений, когда возможно наличие только {availableEX} упражнений за неделю. Пересмотрите значение максимального возможного количества упражнений в тренировочный день или количество упражнений на каждую группу мышц. Файл input.py")

