import itertools
import re


def get_all_pairs_in_list(my_list: list[str]) -> list[tuple[str, str]]:
    return_list = list()
    for i in range(len(my_list)):
        first = my_list[i]
        for j in range(i + 1, len(my_list)):
            second = my_list[j]
            pair = (first, second)
            return_list.append(pair)
    return return_list


def get_all_combinations(my_list: list[str]) -> list[list[str]]:
    combinations = list()
    for size in range(1, len(my_list)):
        combs_with_size = itertools.combinations(my_list, size)
        combinations.extend(combs_with_size)
    combinations.append(tuple(my_list))
    return combinations


# https://stackoverflow.com/questions/19366517/how-to-sort-a-list-containing-alphanumeric-values
def natural_sort_key(s):
    nsre = re.compile("([0-9]+)")
    return [int(text) if text.isdigit() else text.lower() for text in re.split(nsre, s)]


def natural_sort(values: list[str]) -> list[str]:
    return sorted(values, key=natural_sort_key)
