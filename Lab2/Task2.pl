%Опpеделить, является ли один список подсписком дpугого
%Если список пустой

sublist([], _).

% Подсписок - это список, который начинается с некоторого префикса списка.
sublist(SubList, List) :-
    append(_, SubListWithSuffix, List), % Находим какой-то префикс списка List
    append(SubList, _, SubListWithSuffix). % Проверка того, что SubList - это суффикс найденного префикса.

% Проверка, является ли SubList подсписком List.
is_sublist(SubList, List) :-
    sublist(SubList, List),
    SubList \= []. % Проверка, что SubList не пустой список, иначе это был бы любой подсписок.

% ?-is_sublist([1, 3], [1, 2, 3, 4, 5]).
