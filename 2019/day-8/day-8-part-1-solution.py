# --- Day 8: Space Image Format ---


def get_picture_layers(picture : str, width : int, height : int) -> list:
    """Splits the input picture from Space Image Format into its corresponding layers.
    """
    n_digits_per_layer = width * height
    # split the `picture` string into multiple substrings, one for each layer
    layers = [picture[i:i+n_digits_per_layer] for i in range(0, len(picture), n_digits_per_layer)]
    return layers


def main():
    with open("input", "r") as input_data:
        # load the input password
        password_picture = input_data.read().split("\n")[0]

    image_width = 25
    image_height = 6

    # get the layers of the password picture
    picture_layers = get_picture_layers(picture=password_picture, width=image_width, height=image_height)

    # find the layer that contains the fewest 0 digits
    layer_0_count = []
    for layer in picture_layers:
        layer_0_count.append(layer.count("0"))

    layer_with_fewest_0s = picture_layers[layer_0_count.index(min(layer_0_count))]

    # the answer to the puzzle is the number of 1 digits multiplied by the number
    # of 2 digits in the layer with the fewest 0 digits
    answer = layer_with_fewest_0s.count("1") * layer_with_fewest_0s.count("2")

    print("Answer:", answer)


if __name__ == "__main__":
    main()
