# --- Day 2: Password Philosophy ---


with open("input", "r") as input_data:
    # read entries; each entry is a separate line in input
    policies_and_passwords = input_data.read().split("\n")[:-1]  # remove the last entry, just a blank due to the last \n

    # preprocess the data a bit
    policy_rules = []
    policy_letters = []
    passwords = []
    for entry in policies_and_passwords:
        # split each entry into the three components
        rule, letter, pwd = entry.split(" ")

        policy_rules.append(rule)
        policy_letters.append(letter[:-1])
        passwords.append(pwd)

# loop over passwords
n_valid_passwords = 0
for idx, pwd in enumerate(passwords):
    # get the policy requirements for this password
    rule_min, rule_max = policy_rules[idx].split("-")
    letter = policy_letters[idx]

    # check if password satisfies requirement
    if int(rule_min) <= pwd.count(letter) <= int(rule_max):
        n_valid_passwords +=1

print("Answer:", n_valid_passwords)