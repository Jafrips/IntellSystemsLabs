import random
import time
from exercises import exercises, cardio_exercises
from input import min_exercises_per_day, max_exercises_per_day, weekly_exercise_plan
from input import generations, pop_size

# Окрашивание элементов в консоли
from colorama import init, Fore
init()

# Проверка наличия ключей в exercises
def check_exercises_keys(muscle_groups):
    missing_keys = [key for key in muscle_groups if key not in exercises]
    if missing_keys:
        raise KeyError(f"Missing keys in exercises: {', '.join(missing_keys)}")

# Оценка пригодности распределения
def fitness(days):
    score = 0
    for day, exs in days.items():
        unique_exs = set(exs)
        if len(exs) < min_exercises_per_day and len(exs) > 0:
            score -= (min_exercises_per_day - len(exs)) * 2  # штраф за недостаток упражнений
        elif len(exs) > max_exercises_per_day:
            score -= (len(exs) - max_exercises_per_day) * 2  # штраф за избыток упражнений
        score -= (len(exs) - len(unique_exs)) * 2  # штраф за дублирование упражнений
    return score

# Создание начальной популяции
def create_initial_population(pop_size, muscle_groups):
    check_exercises_keys(muscle_groups)
    population = []
    for _ in range(pop_size):
        days = {i: [] for i in range(1, 8)}
        for muscle_group in muscle_groups:
            exercises_for_group = exercises[muscle_group]
            num_exercises = weekly_exercise_plan[muscle_group]
            for _ in range(num_exercises):
                while True:
                    day = random.choice(list(days.keys()))
                    if len(days[day]) < max_exercises_per_day:
                        days[day].append(random.choice(exercises_for_group))
                        break
        # Проверка и корректировка количества упражнений в каждом дне
        for day in days:
            while 0 < len(days[day]) < min_exercises_per_day:
                muscle_group = random.choice(list(exercises.keys()))
                new_exercise = random.choice(exercises[muscle_group])
                if new_exercise not in days[day]:
                    days[day].append(new_exercise)
        population.append(days)
    return population

# Селекция
def select(population, fitnesses):
    sorted_population = sorted(zip(fitnesses, population), key=lambda x: x[0], reverse=True)
    return [x[1] for x in sorted_population[:len(population)//2]]

# Скрещивание
def crossover(parent1, parent2):
    child = {i: [] for i in range(1, 8)}
    for day in child.keys():
        if random.random() > 0.5:
            child[day] = parent1[day][:]
        else:
            child[day] = parent2[day][:]
    return child

# Мутация
def mutate(days, mutation_rate=0.1):
    for day in days.keys():
        if random.random() < mutation_rate:
            if days[day]:
                days[day].pop(random.randint(0, len(days[day]) - 1))  # Удаление случайного упражнения
            # Убедимся, что новое упражнение не дублируется и соблюдается лимит
            while len(days[day]) < min_exercises_per_day or len(days[day]) > max_exercises_per_day:
                muscle_group = random.choice(list(exercises.keys()))
                new_exercise = random.choice(exercises[muscle_group])
                if new_exercise not in days[day]:
                    days[day].append(new_exercise)
    return days

# Проверка количества упражнений на каждую группу мышц за неделю
def validate_exercise_plan(days):
    weekly_plan = {muscle: 0 for muscle in weekly_exercise_plan.keys()}
    for exs in days.values():
        for ex in exs:
            for muscle_group, ex_list in exercises.items():
                if ex in ex_list:
                    if muscle_group in weekly_plan:
                        weekly_plan[muscle_group] += 1
    for muscle_group, count in weekly_plan.items():
        if count != weekly_exercise_plan[muscle_group]:
            return False
    return True

# Корректировка количества упражнений на каждую группу мышц за неделю
def adjust_exercise_plan(days):
    while not validate_exercise_plan(days):
        muscle_group_counts = count_exercises_per_muscle_group(days)
        for muscle_group, required_count in weekly_exercise_plan.items():
            current_count = muscle_group_counts[muscle_group]
            if current_count < required_count:
                while current_count < required_count:
                    day = random.choice(list(days.keys()))
                    if len(days[day]) < max_exercises_per_day:
                        new_exercise = random.choice(exercises[muscle_group])
                        if new_exercise not in days[day]:
                            days[day].append(new_exercise)
                            current_count += 1
            elif current_count > required_count:
                while current_count > required_count:
                    for day in days:
                        for ex in days[day]:
                            if ex in exercises[muscle_group]:
                                days[day].remove(ex)
                                current_count -= 1
                                break
                        if current_count <= required_count:
                            break
    return days

# Подсчет количества упражнений на каждую группу мышц за неделю
def count_exercises_per_muscle_group(days):
    muscle_group_counts = {muscle: 0 for muscle in weekly_exercise_plan.keys()}
    for day_exercises in days.values():
        for exercise in day_exercises:
            for muscle_group, ex_list in exercises.items():
                if exercise in ex_list and muscle_group in muscle_group_counts:
                    muscle_group_counts[muscle_group] += 1
    return muscle_group_counts

# Добавление кардио-упражнений в дни с недостаточным количеством упражнений
def add_cardio_exercises(days):
    for day in days:
        if 0 < len(days[day]) < min_exercises_per_day:
            cardio_exercise = random.choice(cardio_exercises)
            if cardio_exercise not in days[day]:
                days[day].append(cardio_exercise)
    return days

def check_min_exercises_per_day(days):
    for day, exercises in days.items():
        non_cardio_exercises = [ex for ex in exercises if ex not in cardio_exercises]
        if len(non_cardio_exercises) < min_exercises_per_day:
            return False
    return True

def check_single_exercise_days(days):
    for day, exercises in days.items():
        non_cardio_exercises = [ex for ex in exercises if ex not in cardio_exercises]
        if len(non_cardio_exercises) == 1:
            return False
    return True

def main():
    muscle_groups = list(weekly_exercise_plan.keys())

    # Инициализация популяции
    population = create_initial_population(pop_size, muscle_groups)
    population = [adjust_exercise_plan(individual) for individual in population]

    for generation in range(generations):
        fitnesses = [fitness(individual) for individual in population]

        # Селекция
        selected_population = select(population, fitnesses)

        # Скрещивание и мутация
        new_population = []
        while len(new_population) < pop_size:
            parent1, parent2 = random.sample(selected_population, 2)
            child = crossover(parent1, parent2)
            child = mutate(child)
            child = adjust_exercise_plan(child)
            new_population.append(child)

        population = new_population

        # Проверка выполнения всех условий
        if all(validate_exercise_plan(individual) for individual in population):
            best_solution = max(population, key=fitness)
            if check_min_exercises_per_day(best_solution) and check_single_exercise_days(best_solution):
                break

    # Выбор лучшего решения
    final_fitnesses = [fitness(individual) for individual in population]
    best_solution = population[final_fitnesses.index(max(final_fitnesses))]

    # Добавление кардио-упражнений в дни с недостаточным количеством упражнений
    best_solution = add_cardio_exercises(best_solution)

    # Вывод результата
    for day, exs in best_solution.items():
        if exs:
            # Подсчет количества упражнений в день без учета кардио упражнений
            ExCount = 0
            for ex in exs:
                if ex in cardio_exercises:
                    ExCount = ExCount
                else:
                    ExCount += 1
            
            print(f"Day {day}: ({ExCount}) {', '.join(exs)}")
        else:
            print(f"Day {day}: {Fore.GREEN} Выходной", Fore.RESET)

    print("Численность популяции:", Fore.CYAN, len(population), Fore.RESET)
    print("Количество поколений:", Fore.CYAN, generation + 1, Fore.RESET)

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("Время выполнения: %s секунд" % (time.time() - start_time))
