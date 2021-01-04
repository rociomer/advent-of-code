# --- Day 4: Passport Processing ---


with open("input", "r") as input_data:
    # read entries; each entry is a separate line in input
    passports = input_data.read().split("\n\n")

# define the required fields
required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

# add ":" too all the required fields to search for them in each passport entry
required_fields = [i + ":" for i in required_fields]

# count the valid passports
n_valid_passports = 0
n_required_fields = len(required_fields)
for passport_entry in passports:
    if all(i in passport_entry for i in required_fields):
        n_valid_passports += 1

print("Answer:", n_valid_passports)