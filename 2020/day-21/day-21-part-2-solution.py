# --- Day 21: Allergen Assessment ---
from typing import Tuple


def intersection(list1 : list, list2 : list) -> list:
    """Returns the intersection of two lists using the set() method.
    """
    return list(set(list1) & set(list2))


def parse_ingredients_list(ingredients_list : list) -> Tuple[list, list]:
    """Parses the raw input (list of ingredients and allergens) into separate
    lists of ingredients and allergens, where the indices of both lists belong to
    the same line in the input.
    """
    ingredients = []
    allergens = []
    for line in ingredients_list:
        if "contains" in line:
            ingredients_split, allergens_split = line.split(" (contains ")
            ingredients.append([ingredient for ingredient in ingredients_split.split(" ")])
            allergens.append([allergen for allergen in allergens_split[:-1].split(", ")])
        else:
            ingredients.append([ingredient for ingredient in line.split(" ")])
            allergens.append(None)

    return ingredients, allergens


def match_allergens(ingredients : list, allergens : list) -> Tuple[list, list, list]:
    """Matches the input allergens to the ingredients which contains them. Outputs
    three lists, the indices of the matched ingredients and allergens correspond
    to each other, whereas all the ingredients which contain no allergens are returned
    in the third list.
    """
    matched_ingredients, matched_allergens = [], []  # initialize

    # determine all the possible matches by looping through the list of ingredients and allergens
    possible_matches = {}  # key: allergen (str), value: possible ingredients (list)
    for idx, row in enumerate(ingredients):
        # if there are no allergens in the product, then this does not necessarily
        # mean the ingredients have no allergens, as they could simply be unlabeled
        if allergens[idx] is None:
            pass

        # if there is an equal number of allergens and ingredients in a row, then we
        # know that these are possible matches
        else:
            for allergen in allergens[idx]:
                if allergen in possible_matches:
                    possible_matches[allergen] = intersection(row, possible_matches[allergen])
                else:
                    possible_matches[allergen] = row

    # go through process of elimination to match allergens
    while possible_matches.keys():
        # loop over all the possible matches, checking for allergens which match
        # to a single ingredient
        for allergen, ingredient in possible_matches.items():
            if len(ingredient) == 1:
                matched_ingredients += ingredient
                matched_allergens.append(allergen)

        # remove any previously matched ingredients/allergens from raw input/allergens
        for allergen in matched_allergens:
            if allergen in possible_matches.keys():
                del possible_matches[allergen]  # remove from dictionary
        for ingredient in matched_ingredients:
            for key, value in possible_matches.items():
                if ingredient in value:
                    value.remove(ingredient)    # remove from dictionary

    # the ingredients without any allergens are those left over
    ingredients_without_allergens = []
    for row in ingredients:
        for ingredient in row:
            if ingredient not in matched_ingredients:
                ingredients_without_allergens.append(ingredient)

    return matched_ingredients, matched_allergens, ingredients_without_allergens


def main():
    # load data
    with open("input", "r") as input_data:
        ingredients_list = input_data.read().split("\n")[:-1]  # discard the last empty item

    # parse the ingredients list into separate lists of ingredients and allergens
    ingredients, allergens = parse_ingredients_list(ingredients_list=ingredients_list)

    # find the ingredients which do not contain any allergens
    matched_ingredients, matched_allergens, _ = match_allergens(ingredients=ingredients,
                                                                allergens=allergens)

    # combine the matched allergens and ingredients to sort them
    combined_list = []
    for idx, ingredient in enumerate(matched_ingredients):
        combined_list.append(matched_allergens[idx] + "," + ingredient)

    combined_list.sort()

    # the answer to the puzzle is the canonical dangerous ingredients list
    canonical_dangerous_ingredients = [i.split(",")[1] for i in combined_list]
    answer = ",".join(canonical_dangerous_ingredients)

    print("Answer:", answer)


if __name__ == "__main__":
    main()
