# --- Day 7: Handy Haversacks ---
# You land at the regional airport in time for your next flight. In fact, it looks like you'll even have time to grab some food: all flights are currently delayed due to issues in luggage processing.
# 
# Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their contents; bags must be color-coded and must contain specific quantities of other color-coded bags. Apparently, nobody responsible for these regulations considered how long they would take to enforce!
# 
# For example, consider the following rules:
# 
# light red bags contain 1 bright white bag, 2 muted yellow bags.
# dark orange bags contain 3 bright white bags, 4 muted yellow bags.
# bright white bags contain 1 shiny gold bag.
# muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
# shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
# dark olive bags contain 3 faded blue bags, 4 dotted black bags.
# vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
# faded blue bags contain no other bags.
# dotted black bags contain no other bags.
# These rules specify the required contents for 9 bag types. In this example, every faded blue bag is empty, every vibrant plum bag contains 11 bags (5 faded blue and 6 dotted black), and so on.
# 
# You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors would be valid for the outermost bag? (In other words: how many colors can, eventually, contain at least one shiny gold bag?)
# 
# In the above rules, the following options would be available to you:
# 
# A bright white bag, which can hold your shiny gold bag directly.
# A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
# A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
# A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
# So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.
# 
# How many bag colors can eventually contain at least one shiny gold bag? (The list of rules is quite long; make sure you get all of it.)
#
# --- Part Two ---
# It's getting pretty expensive to fly these days - not because of ticket prices, but because of the ridiculous number of bags you need to buy!
# 
# Consider again your shiny gold bag and the rules from the above example:
# 
# faded blue bags contain 0 other bags.
# dotted black bags contain 0 other bags.
# vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black bags.
# dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black bags.
# So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags within it) plus 2 vibrant plum bags (and the 11 bags within each of those): 1 + 1*7 + 2 + 2*11 = 32 bags!
# 
# Of course, the actual rules have a small chance of going several levels deeper than this example; be sure to count all of the bags, even if the nesting becomes topologically impractical!
# 
# Here's another example:
# 
# shiny gold bags contain 2 dark red bags.
# dark red bags contain 2 dark orange bags.
# dark orange bags contain 2 dark yellow bags.
# dark yellow bags contain 2 dark green bags.
# dark green bags contain 2 dark blue bags.
# dark blue bags contain 2 dark violet bags.
# dark violet bags contain no other bags.
# In this example, a single shiny gold bag must contain 126 other bags.
# 
# How many individual bags are required inside your single shiny gold bag?

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