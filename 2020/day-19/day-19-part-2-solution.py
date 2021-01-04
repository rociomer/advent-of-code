# --- Day 19: Monster Messages ---
import re
from copy import deepcopy


def parse_message_rules(rules : list) -> dict:
    """Takes the valid message rules in `rules` and puts them into a dictionary,
    where the keys are the rule numbers and the values are the rules (strings).
    Manipulates the rules a bit to make them easier to work with later e.g. adds
    "o"s around the digits, removes spaces, and adds parentheses to all rules
    except the two which contain "a" and "b".
    """
    # first convert the input list into a dictionary
    rules_dict = {}
    for rule in rules:
        rule_split = rule.split(":")
        rules_dict[rule_split[0]] = rule_split[1][1:]

    # put the values in the dictionary into regex strings
    for key, value in rules_dict.items():
        if value == '"a"':
            rules_dict[key] = "a"  # remove the double parentheses
        elif value == '"b"':
            rules_dict[key] = "b"  # remove the double parentheses
        else:
            # add "o"s around the remaining digits, delete the spaces, and add
            # parentheses to make it a regex
            # for example:
            # "1 2" --> "(o1oo2o)"
            # "1 2 | 3 4" --> "(o1oo3o|o2oo4o)"
            split_value = value.split(" ")
            parsed_values = []
            for item in split_value:
                # remove any spaces
                i = item.replace(" ", "")
                # lets put "o"s around each number to make them easier to replace later
                i_delimited = "o" + i + "o"
                if i_delimited == "o|o":  # but no "o"s around the | operator
                    parsed_values.append("|")
                else:
                    parsed_values.append(i_delimited)
            # adds parentheses (this makes it a regex that matches the meaning of
            # the rule i.e. anything inside the () must be exactly matched
            rules_dict[key] = "(" + "".join(parsed_values) + ")"

    return rules_dict


def get_n_cycles(rules_dict : dict) -> int:
    """Returns the number of cycles it takes to convert the input rules
    (dictionary of lists) into a dictionary of regular expressions (in string
    format, not yet converted into regex objects). Careful here to  only input
    the "unmodified" rules, without loops.
    """
    re_dict = deepcopy(rules_dict)

    # initialize the list of patterns to replace (initially just "a" and "b",
    # but later this list will expand to include more complex regex)
    patterns_to_replace = {}
    for key, value in rules_dict.items():
        if "a" in value:
            patterns_to_replace[re.compile("o"+key+"o")] = value
        elif "b" in value:
            patterns_to_replace[re.compile("o"+key+"o")] = value
        else:
            pass

    # then go through and replace the values which still contain digits with the
    # regex patterns in `patterns_to_replace`; every iteration we will update
    # the patterns to replace based on the "complete" regex expressions
    previous_patterns_to_replace = {}
    n_cycles = 0
    while patterns_to_replace:

        # we will keep track of the new patterns to replace next round
        new_patterns_to_replace = {}
        # as well as the "previous" patterns to replace (so we avoid searching for them once
        # they've been replaced)
        previous_patterns_to_replace.update(patterns_to_replace)

        # go through all the values in the rules and replace them using the patterns in `patterns_to_replace`
        for key, regex in re_dict.items():
            for pattern in patterns_to_replace.keys():
                if re.search(pattern, regex):
                    # replace the pattern (e.g. replace "o1o" with the regex for rule 1)
                    regex = re.sub(pattern, patterns_to_replace[pattern], regex)

            re_dict[key] = regex

            # if there are no digits left in the new values (the regex), then
            # these will become the new patterns to replace in the next cycle
            digits = re.compile("[\d]")
            if not re.search(digits, str(re_dict[key])) and re.compile("o"+key+"o") not in previous_patterns_to_replace.keys():
                new_patterns_to_replace[re.compile("o"+key+"o")] = re_dict[key]

        # update the dict of patterns which we will replace in the next cycle
        patterns_to_replace = deepcopy(new_patterns_to_replace)
        n_cycles += 1

    return n_cycles


def get_re(rules_dict : dict, n_max_cycles : int) -> dict:
    """Returns the rules (dictionary of lists) as a dictionary of regular expressions
    (in string format, not yet converted into regex objects), by doing search
    and replace in the input rules for the specified number of cycles.
    """
    re_dict = deepcopy(rules_dict)

    # initialize the list of patterns to replace (initially just "a" and "b",
    # but later this list will expand to include more complex regex)
    patterns_to_replace = {}
    for key, value in rules_dict.items():
        if "a" in value:
            patterns_to_replace[re.compile("o"+key+"o")] = value
        elif "b" in value:
            patterns_to_replace[re.compile("o"+key+"o")] = value
        else:
            pass

    # then go through and replace the values which still contain digits with the
    # regex patterns in `patterns_to_replace`; every iteration we will update
    # the patterns to replace based on the "complete" regex expressions
    previous_patterns_to_replace = {}
    n_cycles = 0
    while n_cycles < n_max_cycles:

        # we will keep track of the new patterns to replace next round
        new_patterns_to_replace = {}
        # as well as the "previous" patterns to replace (so we avoid searching for them once
        # they've been replaced)
        previous_patterns_to_replace.update(patterns_to_replace)

        # go through all the values in the rules and replace them using the patterns in `patterns_to_replace`
        for key, regex in re_dict.items():
            for pattern in patterns_to_replace.keys():
                if re.search(pattern, regex):
                    # replace the pattern (e.g. replace "o1o" with the regex for rule 1)
                    regex = re.sub(pattern, patterns_to_replace[pattern], regex)

            re_dict[key] = regex

            # if there are no digits left in the new values (the regex), then
            # these will become the new patterns to replace in the next cycle
            digits = re.compile("[\d]")
            if not re.search(digits, str(re_dict[key])) and re.compile("o"+key+"o") not in previous_patterns_to_replace.keys():
                new_patterns_to_replace[re.compile("o"+key+"o")] = re_dict[key]

        # update the dict of patterns which we will replace in the next cycle
        patterns_to_replace = deepcopy(new_patterns_to_replace)
        n_cycles += 1

    return re_dict


def main():
    # 1) first, we will get the number of search and replace cycles used for the
    # "unmodified" input:
    with open("input", "r") as input_data:
        unmodified_message_rules, _ = input_data.read().split("\n\n")

    unmodified_message_rules = unmodified_message_rules.split("\n")

    # put the valid message rules into a dictionary which can be more easily worked with
    unmodified_rules_dict = parse_message_rules(rules=unmodified_message_rules)

    # get the number of cycles to use in the next part; this is the number of
    # search and replace cycles it takes to convert the "unmodified" rules (without
    # loops) into complete regular expressions
    n_cycles = get_n_cycles(rules_dict=unmodified_rules_dict)

    # 2) then, we will work with the new input data, using the `n_cycles` obtained
    # above as a starting point:
    with open("input2", "r") as input_data:
        valid_message_rules, received_messages = input_data.read().split("\n\n")

    valid_message_rules = valid_message_rules.split("\n")
    received_messages = received_messages.split("\n")[:-1]  # last line is empty

    # put the valid message rules into a dictionary which can be more easily worked with
    rules_dict = parse_message_rules(rules=valid_message_rules)

    # convert the rules into regular expressions (regex strings, to compile later)
    re_dict = get_re(rules_dict=rules_dict, n_max_cycles=n_cycles)

    # get any rules in rule 0, recursively
    rules_in_rule_0 = re.findall("\d+", re_dict["0"])
    condition = False
    while not condition:
        condition = True
        new_rules = []
        for i in rules_in_rule_0:
            rules_in_rule_i = re.findall("\d+", re_dict[i])
        for i in rules_in_rule_i:
            if i not in rules_in_rule_0:
                rules_in_rule_0.append(i)
                condition = False

    # replace rule 0 with those rules, and their recursive counterparts, until
    # the number of matches stops changing
    prev_n_matches = -1
    n_matches = 0
    n = 1
    while n_matches != prev_n_matches:

        prev_n_matches = n_matches

        rule_0 = re_dict["0"]
        # replace the recursive rules "n" times
        for _ in range(n):
            for rule in rules_in_rule_0:
                  rule_0 = re.sub(f"o{rule}o", re_dict[rule], rule_0)

        # replace the last "o\do"s with .
        rule_0 = re.sub("o\do", ".", rule_0)

        # get the number of messages that completely match rule 0
        n_matches = 0
        regex = re.compile("^" + rule_0 + "$")
        for message in received_messages:
            if re.search(regex, message): # check if message matches rule 0
                 n_matches += 1

        n += 1

    print("Answer:", n_matches)


if __name__ == "__main__":
    main()
