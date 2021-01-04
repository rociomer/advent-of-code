# --- Day 16: Ticket Translation ---


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
