# --- Day 4: Passport Processing ---
import re  # regular expressions


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

        valid_passport = True  # assume True until at least one condition proves False

        # loop over fields, check if condition is met for each field
        for field in re.split(" |\n", passport_entry):
            # byr (Birth Year) - four digits; at least 1920 and at most 2002.
            if "byr:" in field:
                valid_field = bool(1920 <= int(field[4:]) <= 2002)
            # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
            elif "iyr:" in field:
                valid_field = bool(2010 <= int(field[4:]) <= 2020)
            # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
            elif "eyr:" in field:
                valid_field = bool(2020 <= int(field[4:]) <= 2030)
            # hgt (Height) - a number followed by either cm or in:
            # If cm, the number must be at least 150 and at most 193.
            elif "hgt:" in field and "cm" in field:
                valid_field = bool(150 <= int(field[4:-2]) <= 193)
            # If in, the number must be at least 59 and at most 76.
            elif "hgt:" in field and "in" in field:
                valid_field = bool(59 <= int(field[4:-2]) <= 76)
            # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
            elif "hcl:#" in field:
                valid_field = bool(re.match("[0-9, a-z]{6}\s", field[5:] + " "))
            # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
            elif "ecl:" in field:
                valid_field = bool(any(i in field for i in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]))
            # pid (Passport ID) - a nine-digit number, including leading zeroes.
            elif "pid:" in field:
                valid_field = bool(re.match("[0-9]{9}\s", field[4:] + " "))
            # cid (Country ID) - ignored, missing or not.
            elif "cid:" in field:
                valid_field = True
            # otherwise, this is an invalid field
            else:
                valid_field = False

            if not valid_field:
                valid_passport = False
                break 

        # if all conditions are met, we still have a valid passport
        if valid_passport:
            n_valid_passports += 1

print("Answer:", n_valid_passports)