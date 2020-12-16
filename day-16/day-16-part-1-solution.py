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


def parse_rules(raw_rules : list) -> list:
    """Parse the rules from the train ticket document. The rules are encoded as 
    a list of all the possible values the items in each field can take.
    """
    parsed_rules = []  # initialize (we will fill it in as we parse each rule)

    rules = raw_rules.split("\n")[:-1]  # skip the last item of `raw_rules`, which is empty
    for rule in rules:
        rule_items = rule.split(":")  # we will discard everything before the ":"
        ranges = rule_items[1].split("or")

        # we care only about the ranges, which we will append to `parsed_rules`
        for range_item in ranges:
            integers = range_item.split("-")
            parsed_rules += [n for n in range(int(integers[0]), int(integers[1]) + 1)]
    return set(parsed_rules)  # we only need one occurrence


def get_invalid_fields(nearby_tickets : list, parsed_rules : list) -> list:
    """Returns a list of the fields that are invalid in the nearby tickets for 
    *any* criterion in the parsed rules.
    """
    invalid_fields = []  # initialize (we will fill it in as we find invalid fields)

    for ticket in nearby_tickets.split("\n")[1:-1]:  # skip the header of `nearby_tickets` and skip the last item, which is empty
        for n in ticket.split(","):
            if int(n) not in parsed_rules:
                invalid_fields.append(int(n))

    return invalid_fields

def main():
    # load data
    with open("input", "r") as input_data:
        # read entries; each entry is a separate line in input
        train_ticket_document = input_data.read().split("\n\n")

    rules, my_ticket, nearby_tickets = train_ticket_document

    # we will ignore `my_ticket` for now

    # parse the rules
    parsed_rules = parse_rules(raw_rules=rules)

    # check the invalid fields in the nearby tickets
    invalid_fields = get_invalid_fields(nearby_tickets=nearby_tickets,
                                        parsed_rules=parsed_rules)

    # the ticket scanning error rate is the sum of all the invalid fields
    ticket_scanning_error_rate = sum(invalid_fields)

    print("Answer:", ticket_scanning_error_rate)


if __name__ == "__main__":
    main()
