# --- Day 6: Custom Customs ---


with open("input", "r") as input_data:
    # read entries; each entry is a separate line in input
    collective_declaration_forms = input_data.read().split("\n\n")

# count the number of answers that everyone responded "yes" to in each group
all_yes_answers = 0
for group_answers in collective_declaration_forms:

    # first create a list of all the answers given by one group
    # and count the number of people in a group
    group_answers_list = []
    n_people_in_group = 0
    for one_persons_answers in group_answers.split("\n"):
        if one_persons_answers:  # skip the empty lines left over from trailing newlines
            group_answers_list += one_persons_answers
            n_people_in_group += 1

    # if everyone in a group voted "yes" on a question, add it to the count
    for yes_answer in set(group_answers_list):
        if group_answers_list.count(yes_answer) == n_people_in_group:
            all_yes_answers += 1

print("Answer:", all_yes_answers)
