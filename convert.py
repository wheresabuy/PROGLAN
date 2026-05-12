from PIL import Image

# Open the image and the mask
img = Image.open('ninjarildo_Image.bmp').convert('RGB')
mask = Image.open('ninjarildo_mask.bmp').convert('L')

# Ensure they have the same size
if img.size != mask.size:
    mask = mask.resize(img.size)

# Create an RGBA version of the image
# We use the mask as the alpha channel
img.putalpha(mask)

# Save as PNG
img.save('ninja.png')
print("Successfully created ninja.png")
