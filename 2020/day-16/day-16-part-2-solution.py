# --- Day 16: Ticket Translation ---
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
