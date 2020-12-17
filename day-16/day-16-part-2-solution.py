# --- Day 16: Ticket Translation ---
# As you're walking to yet another connecting flight, you realize that one of the legs of your re-routed trip coming up is on a high-speed train. However, the train ticket you were given is in a language you don't understand. You should probably figure out what it says before you get to the train station after the next flight.
# 
# Unfortunately, you can't actually read the words on the ticket. You can, however, read the numbers, and so you figure out the fields these tickets must have and the valid ranges for values in those fields.
# 
# You collect the rules for ticket fields, the numbers on your ticket, and the numbers on other nearby tickets for the same train service (via the airport security cameras) together into a single document you can reference (your puzzle input).
# 
# The rules for ticket fields specify a list of fields that exist somewhere on the ticket and the valid ranges of values for each field. For example, a rule like class: 1-3 or 5-7 means that one of the fields in every ticket is named class and can be any value in the ranges 1-3 or 5-7 (inclusive, such that 3 and 5 are both valid in this field, but 4 is not).
# 
# Each ticket is represented by a single line of comma-separated values. The values are the numbers on the ticket in the order they appear; every ticket has the same format. For example, consider this ticket:
# 
# .--------------------------------------------------------.
# | ????: 101    ?????: 102   ??????????: 103     ???: 104 |
# |                                                        |
# | ??: 301  ??: 302             ???????: 303      ??????? |
# | ??: 401  ??: 402           ???? ????: 403    ????????? |
# '--------------------------------------------------------'
# Here, ? represents text in a language you don't understand. This ticket might be represented as 101,102,103,104,301,302,303,401,402,403; of course, the actual train tickets you're looking at are much more complicated. In any case, you've extracted just the numbers in such a way that the first number is always the same specific field, the second number is always a different specific field, and so on - you just don't know what each position actually means!
# 
# Start by determining which tickets are completely invalid; these are tickets that contain values which aren't valid for any field. Ignore your ticket for now.
# 
# For example, suppose you have the following notes:
# 
# class: 1-3 or 5-7
# row: 6-11 or 33-44
# seat: 13-40 or 45-50
# 
# your ticket:
# 7,1,14
# 
# nearby tickets:
# 7,3,47
# 40,4,50
# 55,2,20
# 38,6,12
# It doesn't matter which position corresponds to which field; you can identify invalid nearby tickets by considering only whether tickets contain values that are not valid for any field. In this example, the values on the first nearby ticket are all valid for at least one field. This is not true of the other three nearby tickets: the values 4, 55, and 12 are are not valid for any field. Adding together all of the invalid values produces your ticket scanning error rate: 4 + 55 + 12 = 71.
# 
# Consider the validity of the nearby tickets you scanned. What is your ticket scanning error rate?
#
# --- Part Two ---
# Now that you've identified which tickets contain invalid values, discard those tickets entirely. Use the remaining valid tickets to determine which field is which.
# 
# Using the valid ranges for each field, determine what order the fields appear on the tickets. The order is consistent between all tickets: if seat is the third field, it is the third field on every ticket, including your ticket.
# 
# For example, suppose you have the following notes:
# 
# class: 0-1 or 4-19
# row: 0-5 or 8-19
# seat: 0-13 or 16-19
# 
# your ticket:
# 11,12,13
# 
# nearby tickets:
# 3,9,18
# 15,1,5
# 5,14,9
# Based on the nearby tickets in the above example, the first position must be row, the second position must be class, and the third position must be seat; you can conclude that in your ticket, class is 12, row is 11, and seat is 13.
# 
# Once you work out which field is which, look for the six fields on your ticket that start with the word departure. What do you get if you multiply those six values together?
import itertools
from functools import reduce

def parse_rules(raw_rules : list) -> dict:
    """Parse the rules from the train ticket document. Each rule is encoded in a 
    dict as a list of all the possible values the items in each field can take.
    """
    parsed_rules = {}  # initialize (we will fill it in as we parse each rule)

    rules = raw_rules.split("\n")[:-1]  # skip the last item of `raw_rules`, which is empty
    for rule in rules:
        rule_items = rule.split(":")      # the ":" separates the keys from the values
        parsed_rules[rule_items[0]] = []  # initialize a value for each key to an empty list
        ranges = rule_items[1].split("or")

        # we care only about the ranges, which we will append to `parsed_rules`
        for range_item in ranges:
            integers = range_item.split("-")
            parsed_rules[rule_items[0]] += [n for n in range(int(integers[0]), int(integers[1]) + 1)]
    return parsed_rules


def remove_invalid_tickets(nearby_tickets : list, parsed_rules : dict) -> list:
    """Returns a list of the valid nearby tickets only, which are tickets for which
    each field matches *any* criterion in the parsed rules.
    """
    valid_tickets = []  # initialize (we will fill it in as we find valid tickets)
    # aggregate all the possible values for the fields in the line below
    possible_values_for_all_fields = set(list(itertools.chain.from_iterable(parsed_rules.values())))

    for ticket in nearby_tickets.split("\n")[1:-1]:  # skip the header of `nearby_tickets` and skip the last item, which is empty
        for n in ticket.split(","):
            if int(n) not in possible_values_for_all_fields:
                break  # ticket is invalid (will not reach lines below)
        else:
            valid_tickets.append(ticket.split(","))

    return valid_tickets


def determine_order_of_fields(valid_tickets : list, parsed_rules : dict) -> dict:
    """Determines the order of the fields in the valid tickets and returns a 
    dictionary where each key is the name of the field and each value corresponds
    to its index in the tickets.
    """
    potential_field_idc = {}
    n_fields = len(valid_tickets[0])
    
    # we will loop over the different fields to see how many ticket entries match
    for field_name in parsed_rules.keys():

        # create a list where we keep track of the number of fields matched
        potential_field_idc[field_name] = [0] * n_fields
 
        # then we check which fields in the tickets match the valid range of each field
        for ticket in valid_tickets:
            for idx, field_value in enumerate(ticket):
                if int(field_value) in parsed_rules[field_name]:
                    potential_field_idc[field_name][idx] += 1
                
    # assign the field names based on how many matches were found for each field,
    # starting from the field which got the fewest matches
    field_idc = {}  # for storing the true values

    while potential_field_idc.keys():
        # find the total number of matches for each field
        field_matches_sum = [sum(matches_list) for matches_list in potential_field_idc.values()]
        # identify the minimum values (i.e. the least matches)
        fewest_matches = min(field_matches_sum)
        for field_key, field_matches in potential_field_idc.items():
            if sum(field_matches) == fewest_matches:
                # add the field to the dictionary
                field_with_most_matches = max(field_matches)
                field_with_most_matches_idx = field_matches.index(field_with_most_matches)
                field_idc[field_key] = field_with_most_matches_idx

                break
        # remove the entry from the `potential_field_idc`
        del potential_field_idc[field_key]

        # remove the index from the list of potential matches
        for field_key, field_matches in potential_field_idc.items():
            potential_field_idc[field_key][field_with_most_matches_idx] = 0
                
    return field_idc


def main():
    # load data
    with open("input", "r") as input_data:
        # read entries; each entry is a separate line in input
        train_ticket_document = input_data.read().split("\n\n")

    rules, my_ticket, nearby_tickets = train_ticket_document

    # we will ignore `my_ticket` for now

    # parse the rules
    parsed_rules = parse_rules(raw_rules=rules)

    # check for invalid fields in the nearby tickets, and remove them
    valid_tickets = remove_invalid_tickets(nearby_tickets=nearby_tickets,
                                           parsed_rules=parsed_rules)
    
    # figure out the fields
    field_idc = determine_order_of_fields(valid_tickets=valid_tickets,
                                          parsed_rules=parsed_rules)

    # the answer to the puzzle is the product of all the fields in `my_ticket` 
    # that start with the name "departure"
    departure_field_idc = [field_idc[key] for key in field_idc.keys() if key[:9] == "departure"]
    departure_field_values_in_my_ticket = [int(my_ticket.split(",")[i]) for i in departure_field_idc]
    answer = reduce((lambda x, y: x * y), departure_field_values_in_my_ticket)  # product of all items in list

    print("Answer:", answer)


if __name__ == "__main__":
    main()
