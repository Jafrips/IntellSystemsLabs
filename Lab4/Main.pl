
series("Breaking Bad", crime_drama, netflix, 9.5).
series("Stranger Things", sci_fi, netflix, 8.9).
series("The Crown", historical_drama, netflix, 8.7).
series("The Mandalorian", sci_fi, disney_plus, 8.8).
series("Game of Thrones", fantasy, hbo, 9.3).
series("Friends", comedy, hbo_max, 8.9).
series("The Office", comedy, peacock, 8.8).
series("The Witcher", fantasy, netflix, 8.2).
series("Westworld", sci_fi, hbo, 8.6).
series("The Boys", superhero, amazon_prime, 8.7).
series("The Marvelous Mrs. Maisel", comedy, amazon_prime, 8.7).
series("The Handmaid's Tale", dystopian, hulu, 8.4).
series("Dark", sci_fi, netflix, 8.8).
series("Fargo", crime_drama, hulu, 9.0).
series("Black Mirror", sci_fi, netflix, 8.8).
series("Better Call Saul", crime_drama, amc, 8.7).
series("The Sopranos", crime_drama, hbo, 9.2).
series("Sherlock", mystery, bbc, 9.1).
series("Mindhunter", crime_drama, netflix, 8.6).
series("Brooklyn Nine-Nine", comedy, hulu, 8.4).

% Рекомендация по жанру
recommend_by_genre(Genre, Series) :-
    series(Series, Genre, _, _).

% Рекомендация по платформе
recommend_by_platform(Platform, Series) :-
    series(Series, _, Platform, _).

% Рекомендация по платформе и жанру
recommendation(Genre, Platform, Series) :-
    recommend_by_genre(Genre, Series),
    recommend_by_platform(Platform, Series).

% Рекомендация по рейтингу (выведется равный или больше указанному)
recommend_by_rating(Rating, Series) :-
    series(Series, _, _, SeriesRating),
    SeriesRating >= Rating.

% Последняя рекомендация по всем критериям
final_recommendation(Genre, Platform, Rating, Series) :-
    recommendation(Genre, Platform, Series),
    recommend_by_rating(Rating, Series).

% Интерфейс для пользователя
recommend_by_genre_interface :-
    write('Enter the genre: '),
    read(Genre),
    nl,
    write('Series list of genre '), write(Genre), write(':'), nl,
    findall(Series, recommend_by_genre(Genre, Series), SeriesList),
    print_series(SeriesList),
    start.

recommend_by_platform_interface :-
    write('Enter the platform: '),
    read(Platform),
    nl,
    write('Series list for platform '), write(Platform), write(':'), nl,
    findall(Series, recommend_by_platform(Platform, Series), SeriesList),
    print_series(SeriesList),
    start.

recommendation_interface :-
    write('Enter the genre: '),
    read(Genre),
    nl,
    write('Enter the platform: '),
    read(Platform),
    nl,
    write('Series list of genre '), write(Genre), write(' for platform '), write(Platform), write(':'), nl,
    findall(Series, recommendation(Genre, Platform, Series), SeriesList),
    print_series(SeriesList),
    start.

final_recommendation_interface :-
    write('Enter the genre: '),
    read(Genre),
    nl,
    write('Enter the platform: '),
    read(Platform),
    nl,
    write('Enter the minimum rating: '),
    read(Rating),
    nl,
    write('Result:'), nl,
    findall(Series, final_recommendation(Genre, Platform, Rating, Series), SeriesList),
    print_series(SeriesList),
    start.

print_series([]).
print_series([Series|SeriesList]) :-
    write('- '), write(Series), nl,
    print_series(SeriesList).

% Флаг для отслеживания необходимости завершения программы
:- dynamic should_exit/0.

% Запуска интерфейса
start :-
    \+ should_exit,
    write('Welcome to the Series Base System!'), nl,
    write('Choose an option:'), nl,
    write('1. Sort series by genre'), nl,
    write('2. Sort series by publishing platform'), nl,
    write('3. Sort series by genre and platform'), nl,
    write('4. Search for certain series (all parametres)'), nl,
    write('5. Exit'), nl,
    read(Choice),
    process_choice(Choice).

% Обработка выбора пользователя
process_choice(1) :-
    recommend_by_genre_interface.
process_choice(2) :-
    recommend_by_platform_interface.
process_choice(3) :-
    recommendation_interface.
process_choice(4) :-
    final_recommendation_interface.
process_choice(5) :-
    quit.

quit :-
    write('See ya!'), nl,
    assert(should_exit).

% Запуск интерфейса
:- start.
