import random

# Функция для ввода пользовательских предпочтений
def get_user_preferences():
    min_exercises_per_day = int(input("Введите минимальное число упражнений в тренировочный день: "))
    max_exercises_per_day = int(input("Введите максимальное число упражнений в тренировочный день: "))
    muscle_group_frequencies = {}
    for muscle_group in set(exercises.values()):
        if muscle_group == 'Кардио':
            continue
        frequency = int(input(f"Введите частоту упражнений на '{muscle_group}' в неделю: "))
        muscle_group_frequencies[muscle_group] = frequency
    return min_exercises_per_day, max_exercises_per_day, muscle_group_frequencies

# Функция для генерации программы тренировок
def generate_workout(exercises, week_days, min_exercises_per_day, max_exercises_per_day, muscle_group_frequencies):
    workout_program = {day: [] for day in week_days}
    available_exercises = exercises.copy()
    total_exercises_needed = sum(muscle_group_frequencies.values())

    # Добавление кардио, если в день меньше трех упражнений
    def add_cardio(day):
        if len(workout_program[day]) < 3:
            cardio_exercises = [exercise for exercise, group in available_exercises.items() if group == 'Кардио']
            chosen_cardio = random.choice(cardio_exercises)
            workout_program[day].append((chosen_cardio, 'Кардио'))

    # Распределение упражнений по дням на основе предпочтений пользователя
    for muscle_group, frequency in muscle_group_frequencies.items():
        for _ in range(frequency):
            day = random.choice(week_days)
            while len(workout_program[day]) >= max_exercises_per_day:
                day = random.choice(week_days)
            workout_program[day].append((random.choice([exercise for exercise, group in available_exercises.items() if group == muscle_group]), muscle_group))
            add_cardio(day)  # Добавление кардио, если необходимо

    return workout_program

# Набор упражнений и групп мышц
exercises = {
    'Жим штанги лежа': 'Грудь',
    'Сведение в бабочке': 'Грудь',
    'Жим на наклонной скамье': 'Грудь',
    'Жим гантелей': 'Грудь',
    'Отжимания': 'Грудь',
    
    'Приседания': 'Ноги',
    'Разгиб сидя': 'Ноги',
    
    'Подтягивания': 'Спина',
    'Вертикальный хаммер': 'Спина',
    'Горизонтальная тяга блока': 'Спина',
    
    'Подъем штанги стоя': 'Бицепс',
    'Молоты': 'Бицепс',
    
    'Жим гантелей сидя': 'Плечи',
    'Бабочка на заднюю дельту': 'Плечи',
    'Махи в стороны с гантелями': 'Плечи',
    
    'Беговая дорожка': 'Кардио',
    'Велосипед': 'Кардио',
    'Эллипсоид': 'Кардио',
}

# Дни недели
week_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

# Получение предпочтений пользователя
min_exercises_per_day, max_exercises_per_day, muscle_group_frequencies = get_user_preferences()

# Генерация программы тренировок
workout_program = generate_workout(exercises, week_days, min_exercises_per_day, max_exercises_per_day, muscle_group_frequencies)

# Вывод программы тренировок
for day, workout in workout_program.items():
    if workout:
        print(f'Тренировка на {day}:')
        for exercise, muscle_group in workout:
            print(f'- {exercise} ({muscle_group})')
        print()
    else:
        print(f'{day} - Отдых')
