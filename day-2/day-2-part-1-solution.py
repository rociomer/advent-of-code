# --- Day 2: Password Philosophy ---
# Your flight departs in a few days from the coastal airport; the easiest way down to the coast from here is via toboggan.
# 
# The shopkeeper at the North Pole Toboggan Rental Shop is having a bad day. "Something's wrong with our computers; we can't log in!" You ask if you can take a look.
# 
# Their password database seems to be a little corrupted: some of the passwords wouldn't have been allowed by the Official Toboggan Corporate Policy that was in effect when they were chosen.
# 
# To try to debug the problem, they have created a list (your puzzle input) of passwords (according to the corrupted database) and the corporate policy when that password was set.
# 
# For example, suppose you have the following list:
# 
# 1-3 a: abcde
# 1-3 b: cdefg
# 2-9 c: ccccccccc
# Each line gives the password policy and then the password. The password policy indicates the lowest and highest number of times a given letter must appear for the password to be valid. For example, 1-3 a means that the password must contain a at least 1 time and at most 3 times.
# 
# In the above example, 2 passwords are valid. The middle password, cdefg, is not; it contains no instances of b, but needs at least 1. The first and third passwords are valid: they contain one a or nine c, both within the limits of their respective policies.
# 
# How many passwords are valid according to their policies?

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