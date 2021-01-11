# --- Day 8: Space Image Format ---


def decode_picture(picture : str, width : int, height : int) -> list:
    """Decodes the input picture from Space Image Format into normal encoding.
    As per the problem statement: Digits fill row of image left-to-right,
    then downward to next row, then onwards to the next layer (e.g. 3D image).
    """
    n_digits_per_layer = width * height

    # split the `picture` string into multiple substrings, one for each layer, and
    # convert each substring into a list of integers
    layers = [list(int(j) for j in picture[i:i+n_digits_per_layer]) for i in range(0, len(picture), n_digits_per_layer)]

    # the image is rendered by stacking the layers and aligning the pixels with
    # the same positions in each layer, where 0:black, 1:white, 2:transparent
    top_visible_layer = layers[0]
    for pixel_idx, pixel in enumerate(top_visible_layer):
        if pixel == 2:
            layer_idx = 0
            while pixel == 2:
                layer_idx += 1
                pixel = layers[layer_idx][pixel_idx]
            top_visible_layer[pixel_idx] = pixel

    # reshape the top visible layer into a square
    image = [top_visible_layer[i:i+width] for i in range(0, len(top_visible_layer), width)]

    return image


def enhance_picture(picture : list) -> list:
    """Enhances the picture by replacing the black pixels (0) with a black unicode
    square and the white pixels (1) with a white unicode square.
    """
    picture = ["".join(str(j) for j in row) for row in picture]
    picture_enhanced = ""
    for row in picture:
        picture_enhanced += row.replace("0", "⬛").replace("1", "⬜") + "\n"
    return picture_enhanced


def main():
    with open("input", "r") as input_data:
        # load the input password
        password_picture = input_data.read().split("\n")[0]

    image_width = 25
    image_height = 6

    # decode password picture, sent in Space Image Format, into normal encoding
    decoded_picture = decode_picture(picture=password_picture, width=image_width, height=image_height)

    # "enhance" the image a bit to better see the message
    picture_enhanced = enhance_picture(picture=decoded_picture)

    # the answer to the puzzle is the message hidden inside the picture
    print("Answer:")
    print(picture_enhanced)


if __name__ == "__main__":
    main()
