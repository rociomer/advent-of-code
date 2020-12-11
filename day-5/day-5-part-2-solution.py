# --- Day 5: Binary Boarding ---
# You board your plane only to discover a new problem: you dropped your boarding pass! You aren't sure which seat is yours, and all of the flight attendants are busy with the flood of people that suddenly made it through passport control.
# 
# You write a quick program to use your phone's camera to scan all of the nearby boarding passes (your puzzle input); perhaps you can find your seat through process of elimination.
# 
# Instead of zones or groups, this airline uses binary space partitioning to seat people. A seat might be specified like FBFBBFFRLR, where F means "front", B means "back", L means "left", and R means "right".
# 
# The first 7 characters will either be F or B; these specify exactly one of the 128 rows on the plane (numbered 0 through 127). Each letter tells you which half of a region the given seat is in. Start with the whole list of rows; the first letter indicates whether the seat is in the front (0 through 63) or the back (64 through 127). The next letter indicates which half of that region the seat is in, and so on until you're left with exactly one row.
# 
# For example, consider just the first seven characters of FBFBBFFRLR:
# 
# Start by considering the whole range, rows 0 through 127.
# F means to take the lower half, keeping rows 0 through 63.
# B means to take the upper half, keeping rows 32 through 63.
# F means to take the lower half, keeping rows 32 through 47.
# B means to take the upper half, keeping rows 40 through 47.
# B keeps rows 44 through 47.
# F keeps rows 44 through 45.
# The final F keeps the lower of the two, row 44.
# The last three characters will be either L or R; these specify exactly one of the 8 columns of seats on the plane (numbered 0 through 7). The same process as above proceeds again, this time with only three steps. L means to keep the lower half, while R means to keep the upper half.
# 
# For example, consider just the last 3 characters of FBFBBFFRLR:
# 
# Start by considering the whole range, columns 0 through 7.
# R means to take the upper half, keeping columns 4 through 7.
# L means to take the lower half, keeping columns 4 through 5.
# The final R keeps the upper of the two, column 5.
# So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5.
# 
# Every seat also has a unique seat ID: multiply the row by 8, then add the column. In this example, the seat has ID 44 * 8 + 5 = 357.
# 
# Here are some other boarding passes:
# 
# BFFFBBFRRR: row 70, column 7, seat ID 567.
# FFFBBBFRRR: row 14, column 7, seat ID 119.
# BBFFBBFRLL: row 102, column 4, seat ID 820.
# As a sanity check, look through your list of boarding passes. What is the highest seat ID on a boarding pass?
#
# --- Part Two ---
# Ding! The "fasten seat belt" signs have turned on. Time to find your seat.
# 
# It's a completely full flight, so your seat should be the only missing boarding pass in your list. However, there's a catch: some of the seats at the very front and back of the plane don't exist on this aircraft, so they'll be missing from your list as well.
# 
# Your seat wasn't at the very front or back, though; the seats with IDs +1 and -1 from yours will be in your list.
# 
# What is the ID of your seat?

def get_row(boarding_pass):

    # get first 7 characters of boarding pass
    row_encoding = boarding_pass[:7]
    
    # start with all rows
    rows = range(0,128)

    # F means to take the lower half, B means to take the upper half
    for letter in row_encoding:
        idx = int(len(rows)/2)
        if letter == "F":
            rows = rows[:idx]
        elif letter == "B":
            rows = rows[idx:]

    # there will be only one row left
    rows = [int(i) for i in rows]
    row = rows[0]
    return row
    

def get_column(boarding_pass):

    # get last 3 characters of boarding pass
    column_encoding = boarding_pass[7:] 
    
    # start with all columns
    columns = range(0,8)

    # L means to take the lower half, R means to take the upper half
    for letter in column_encoding:
        idx = int(len(columns)/2)
        if letter == "L":
            columns = columns[:idx]
        elif letter == "R":
            columns = columns[idx:]

    # there will be only one column left
    columns = [int(i) for i in columns]
    column = columns[0]
    return column


def get_seat_id(row, column):
    return row * 8 + column


def get_missing_seat(max_seat_id, seat_ids):

    # start with all the seat IDs
    all_seat_ids = list(range(0,max_seat_id + 1))
    
    # remove the ones that are already taken, as per the boarding passes
    for seat_id in seat_ids:
        all_seat_ids.remove(seat_id)

    # of the leftover seat IDs, the correct assignment must have a +1 and -1 in `seat_ids`
    for leftover_seat_id in all_seat_ids:
        seat_id_plus_one = leftover_seat_id + 1
        seat_id_minus_one = leftover_seat_id - 1
        if seat_id_plus_one in seat_ids and seat_id_minus_one in seat_ids:
            return leftover_seat_id  # this is the missing seat

    return None


with open("input", "r") as input_data:
    # read entries; each entry is a separate line in input
    boarding_passes = input_data.read().split("\n")[:-1]  # remove the last entry, just a blank due to the last \n

# create list of all the seat IDs in the boarding passes
seat_ids = []
for seat in boarding_passes:
    # get the seat ID
    row = get_row(boarding_pass=seat)
    column = get_column(boarding_pass=seat)
    seat_id = get_seat_id(row=row, column=column)

    # append
    seat_ids.append(seat_id)

# get the largest seat ID
largest_seat_id = max(seat_ids)

# get the missing seat ID
missing_seat = get_missing_seat(max_seat_id=largest_seat_id, seat_ids=seat_ids)

print("Answer:", missing_seat)
