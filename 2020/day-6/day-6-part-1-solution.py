# --- Day 6: Custom Customs ---


with open("input", "r") as input_data:
    # read entries; each entry is a separate line in input
    collective_declaration_forms = input_data.read().split("\n\n")

# count the number of "yes" answers in the declaration forms
yes_answers = 0
for group_answers in collective_declaration_forms:
    group_answers_list = []
    for one_persons_answers in group_answers.split("\n"):
        group_answers_list += one_persons_answers

    yes_answers += len(set(group_answers_list))

print("Answer:", yes_answers)
