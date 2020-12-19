# --- Day 7: Handy Haversacks ---


def load_bag_rules(file : str) -> dict:
    with open(file, "r") as input_data:
        # read entries; each entry is a separate line in input
        bag_rules = input_data.read().split(".\n")[:-1]  # remove the last entry, just a blank due to the last \n
    
        # convert bag rules to a dictionary where the values for each key (i.e. bag)
        # are a tuple of lists: one list for the bag types and one list for the number
        # of said bag type in the "main" (i.e. key) bag
        bag_rules_dict = {}
        for rule in bag_rules:
            main_bags, contained_bags = rule.split("contain")
            
            key = main_bags[:-5].replace(" ", "")  # description of bag only, without spaces
    
            contained_bag_types_list = []
            contained_bag_numbers_list = []
            for contained_bag in contained_bags.split(","):
                # first get the type of bags and append (after minor preprocessing for empty bags)
                bag_type = contained_bag[3:-4].replace(" ", "")  # description of bag only, without spaces
                if bag_type == "other":  # just for readability, replace the "other" from "no other bags" with "empty"
                    bag_type = "empty"
                contained_bag_types_list.append(bag_type)
    
                # then get the number of bags and append (after minor preprocessing for empty bags)
                number = contained_bag[:3].replace(" ", "")  # number of bags only, without spaces
                if number == "no":  # for empty bags, replace the "no" from "no other bags" with "0"
                    number = "0"
                contained_bag_numbers_list.append(number)
    
            # define the dictionary
            bag_rules_dict[key] = (contained_bag_types_list, contained_bag_numbers_list)

    return bag_rules_dict


def count_bags_inside_shiny_gold(bag_rules : dict) -> int:
    """To count bags, we will start by keeping track of the bags (and number of
    bags) in the shiny gold bag using a list which indicates the number of bags 
    in a given "layer".
    """
    
    # below is the first layer:
    type_bags_in_shiny_gold = list(bag_rules["shinygold"][0])
    n_bags_in_shiny_gold = list(bag_rules["shinygold"][1])
    
    # start keeping track of how many bags we have "opened"
    sum_of_bags_in_shiny_gold = sum([int(n) for n in n_bags_in_shiny_gold])
    
    while type_bags_in_shiny_gold:  # while there are still keys to check
    
        bags_in_bag = []
        n_bags_in_bag = []
        for idx, bag in enumerate(type_bags_in_shiny_gold):
            multiplier = int(n_bags_in_shiny_gold[idx])
    
            # add the bags to the running count if they have reached the end of the line
            if "empty" in bag_rules[bag][0]:
                sum_of_bags_in_shiny_gold += multiplier * (bag_rules[bag][0].count("empty") - 1)
            
            # keep track of any remaining, non-empty bags
            bags_in_bag += [bag for bag in bag_rules[bag][0]]
            n_bags_in_bag += [int(n) * multiplier for n in bag_rules[bag][1]]
    
        # exclude empty bags
        type_bags_in_shiny_gold = [bag for bag in bags_in_bag if bag != "empty"]
        n_bags_in_shiny_gold = [n for n in n_bags_in_bag if n != 0]
    
        sum_of_bags_in_shiny_gold += sum(n_bags_in_shiny_gold)

    return sum_of_bags_in_shiny_gold


def main():
    bag_rules_dict = load_bag_rules(file="input")
    bags_in_shiny_gold = count_bags_inside_shiny_gold(bag_rules=bag_rules_dict)

    print("Answer:", bags_in_shiny_gold)


if __name__ == "__main__":
    main()