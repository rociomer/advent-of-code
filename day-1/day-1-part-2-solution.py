# --- Day 1: Report Repair ---


with open("input", "r") as input_data:
    # read entries; each entry is a separate line in input
    expense_report_entries = input_data.read().split("\n")[:-1]  # remove the last entry, just a blank due to the last \n

    # convert to integers
    expense_report_entries = [int(i) for i in expense_report_entries]

for idx_1, entry_1 in enumerate(expense_report_entries):
    for idx_2, entry_2 in enumerate(expense_report_entries[idx_1+1:]):
        for idx_3, entry_3 in enumerate(expense_report_entries[idx_1 + idx_2 + 1:]):
            if entry_1 + entry_2 + entry_3 == 2020:
                product = entry_1 * entry_2 * entry_3
                print("Answer:", product)
                exit(0)