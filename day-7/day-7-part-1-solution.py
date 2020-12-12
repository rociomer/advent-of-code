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

with open("input", "r") as input_data:
    # read entries; each entry is a separate line in input
    bag_rules = input_data.read().split(".\n")[:-1]  # remove the last entry, just a blank due to the last \n

    # convert bag rules to a dictionary
    bag_rules_dict = {}
    for rule in bag_rules:
        main_bags, contained_bags = rule.split("contain")
        
        key = main_bags[:-5].replace(" ", "")  # description of bag only, without spaces
        
        contained_bags_list = []
        for contained_bag in contained_bags.split(","):
            contained_bags_list.append(contained_bag[3:-4].replace(" ", ""))  # description of bag only, without spaces

        # define the dictionary
        bag_rules_dict[key] = contained_bags_list


# we will keep track of bags that can hold a shiny gold bag here:
can_hold_gold = []

keys_to_check = list(bag_rules_dict.keys())
should_contain = ["shinygold"]
checked_all_bags = False
while not checked_all_bags:  # while there are still keys to check

    # keep track of the number of keys checked, if stop changing then exit loop
    len_keys_to_check_start = len(keys_to_check)

    for key in keys_to_check:
        contains_gold = [i in bag_rules_dict[key] for i in should_contain]
        if 1 in contains_gold:
            # we can remove this `key` from the list as we have verified it can hold gold
            can_hold_gold.append(key)
            keys_to_check.remove(key)
    
    # if the length of the list of bags that cannot hold gold has not changed, exit loop
    if len(keys_to_check) == len_keys_to_check_start:
        checked_all_bags = True

    # replace the keys of bags that can hold gold
    should_contain = can_hold_gold

print("Answer:", len(can_hold_gold))