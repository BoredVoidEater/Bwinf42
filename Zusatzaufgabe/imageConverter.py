from PIL import Image

# Define the color mapping
color_mapping = {
    0: "X",
    1: "L",
    2: "B",
    3: "W",
    4: "R",
}

# Load the input image
input_image = Image.open("input.png")
input_image = input_image.rotate(-90)
width, height = input_image.size
input_image = input_image.resize((width*2,height*2),Image.Resampling.NEAREST)

# Get the width and height of the image
width, height = input_image.size
print(width,height)

# Create an empty 2D array to store the color strings
color_array = [[""] * width for _ in range(height)]

# Iterate through each pixel and map its color to a string
for y in range(0,height):
    for x in range(0,width):
        pixel_color = input_image.getpixel((x, y))
        color_array[y][x] = color_mapping.get(pixel_color, "!")

# Print the 2D array of color strings
for row in color_array:
    print(" ".join(row))
