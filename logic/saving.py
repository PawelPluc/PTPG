import numpy as np
from PIL import Image

# colors - pokolorowane punkty
# Convert the plotted image to a bitmap (BMP) using PIL
img = Image.fromarray((colors * 255).astype(np.uint8))  # Convert to uint8 for PIL
img.save('colored_image.bmp')  # Save the image as a BMP file