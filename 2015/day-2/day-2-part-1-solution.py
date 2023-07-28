# --- Day 2: I Was Told There Would Be No Math ---

# load the input data
with open("input", "r") as input_data:
    # read entries; each entry is a separate line in input (lxwxh)
    box_dimensions_raw = input_data.read().split("\n")[:-1]
    box_dimensions     = [boxdims.split("x") for boxdims in box_dimensions_raw]

# calculate the size of each face, along with the wrapping paper needed to cover
# the box + extra wrapping paper corresponding to the smallest face
wrapping_paper = 0
for boxdims in box_dimensions:
    l = int(boxdims[0])
    w = int(boxdims[1])
    h = int(boxdims[2])
    face_lw = l*w
    face_lh = l*h
    face_wh = w*h
    wrapping_paper += 2*face_lw + 2*face_lh + 2*face_wh + min(face_wh, face_lh, face_lw)

# the answer to the puzzle is amount of wrapping paper needed
answer = wrapping_paper

print("Answer:", answer)
