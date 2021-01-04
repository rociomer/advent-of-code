# --- Day 7: Handy Haversacks ---


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