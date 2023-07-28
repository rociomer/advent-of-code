# --- Day 2: I Was Told There Would Be No Math ---

# load the input data
with open("input", "r") as input_data:
    # read entries; each entry is a separate line in input (lxwxh)
    box_dimensions_raw = input_data.read().split("\n")[:-1]
    box_dimensions     = [boxdims.split("x") for boxdims in box_dimensions_raw]

# calculate the ribbon required to wrap a present: this is the shortest distance around its sides
# each present also requires a bow made out of ribbon, equal to the cubic feet of volume of the present
ribbon = 0
for boxdims in box_dimensions:
    l = int(boxdims[0])
    w = int(boxdims[1])
    h = int(boxdims[2])
    perimeter_lw = 2*(l+w)
    perimeter_lh = 2*(l+h)
    perimeter_wh = 2*(w+h)
    ribbon += min(perimeter_wh, perimeter_lh, perimeter_lw) + l*w*h

# the answer to the puzzle is amount of ribbon needed
answer = ribbon

print("Answer:", answer)
