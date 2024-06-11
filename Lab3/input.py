# Входные параметры

# Минимальное количество упражнений в тренировочный день
min_exercises_per_day = 3

# Максмальное количество упражнений в тренировочный день
max_exercises_per_day = 4

# Количество упражнений на КАЖДУЮ группу мышц за НЕДЕЛЮ
weekly_exercise_plan = {
    "Ноги": 3,
    "Грудь": 2,
    "Спина": 2,
    "Бицепс": 2,
    "Плечи": 2,
}

pop_size = 10  # размер популяции
generations = 50  # количество поколений

#### Проверки ####

# Окрашивание текста ошибок в консоли красным
from colorama import init, Fore
init()

# Проверка min_exercises_per_day и max_exercises_per_day
if min_exercises_per_day > max_exercises_per_day:
    raise ValueError(Fore.RED + "Минимальное количество упражнений в день не может быть больше максимального, проверьте файл input.py")
elif max_exercises_per_day < min_exercises_per_day:
    raise ValueError(Fore.RED + "Максимальное количество упражнений в день не может быть меньше минимального, проверьте файл input.py")

for muscle_group, exercises in weekly_exercise_plan.items():
    if exercises < 0 or exercises > 5:
        raise ValueError(Fore.RED + "Количество упражнений на каждую группу мышц должно быть в диапазоне от 0 до 5. Проверьте значения в файле input.py")
    
totalEX = sum(weekly_exercise_plan.values())
availableEX = max_exercises_per_day * 7
if totalEX > availableEX:
    raise ValueError(Fore.RED + f"Вы пытаетесь распределить {totalEX} упражнений, когда возможно наличие только {availableEX} упражнений за неделю. Пересмотрите значение максимального возможного количества упражнений в тренировочный день или количество упражнений на каждую группу мышц. Файл input.py")
