# --- Day 5: Binary Boarding ---


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
