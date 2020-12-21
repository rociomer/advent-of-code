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


def get_re(rules_dict : dict) -> dict:
    """Returns the rules (dictionary of lists) as a dictionary of regular expressions
    (in string format, not yet converted into regex objects).
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

    return re_dict


def main():
    # load data
    with open("input", "r") as input_data:
        valid_message_rules, received_messages = input_data.read().split("\n\n")

    valid_message_rules = valid_message_rules.split("\n")
    received_messages = received_messages.split("\n")[:-1]  # last line is empty

    # first put the valid message rules into a dictionary which can be more easily worked with
    rules_dict = parse_message_rules(rules=valid_message_rules)

    # then, convert the rules into regular expressions (regex strings, to compile later)
    re_dict = get_re(rules_dict=rules_dict)

    # the answer to the puzzle is the number of messages that completely match rule 0
    # i.e. the entire line must match, from start ("^") to finish ("$")
    answer = 0
    regex = re.compile("^" + re_dict["0"] + "$")  # add the constraints of "^" and "$" to rule 0
    for message in received_messages:
        if re.search(regex, message): # check if message matches rule 0
             answer += 1

    print("Answer:", answer)


if __name__ == "__main__":
    main()
