from PIL import Image
from PIL import ImageFilter
import os

class ImageLib:

    BLUR_LEVEL  = 100
    EDGE_REMOVAL_FACTOR = 0.08

    def __init__(self, path):
        abs_path = os.path.abspath(path)
        self.img = Image.open(abs_path)

    def get_width(self):
        return self.img.width
    
    def get_height(self):
        return self.img.height

    def get_max_dimension(self):
        if(self.img.height > self.img.width):
            return self.img.height
        return self.img.width
    
    def get_min_dimension(self):
        if(self.img.height < self.img.width):
            return self.img.height
        return self.img.width

    def get_image(self):
        return self.img

    def get_blurred_image(self, level):
        self.blur_image = self.img
        for i in range(level):
            self.blur_image = self.blur_image.filter(ImageFilter.BLUR)
        #To remove edges which is not perfectly blurred
        crop_factor = self.get_max_dimension() * ImageLib.EDGE_REMOVAL_FACTOR
        self.blur_image = self.blur_image.crop((crop_factor, crop_factor, self.blur_image.width - crop_factor, self.blur_image.height - crop_factor))

        #As we have removed Edges, we need to resize the image to original size
        self.blur_image = self.blur_image.resize((int(self.blur_image.width + (crop_factor * 2)), int(self.blur_image.height + (crop_factor * 2))))
        return self.blur_image

    def show(self):
        self.img.show()

    def crop_to_square(src_img: Image):
        if(src_img.width > src_img.height):
            width = src_img.height
            margin = (src_img.width - width) / 2
            left = margin
            top = 0
            right = src_img.width - margin
            bottom = src_img.height
        else:
            height = src_img.width
            margin = (src_img.height - height) / 2
            left = 0
            top = margin
            right = src_img.width
            bottom = src_img.height - margin
        return src_img.crop((left, top, right, bottom))

    def get_cropped_square_image(src_img: Image):
        height = src_img.height
        width = src_img.width
        if(src_img.width < src_img.height):
            high_dimension = src_img.height
            low_dimension = src_img.width
        else:
            high_dimension = src_img.width
            low_dimension = src_img.height
        diff = high_dimension - low_dimension
        width = width + (width * (diff / src_img.width))
        height = height + (height * (diff / src_img.height))
        #print(f"Original Width: {src_img.width}\nOriginal Height: {src_img.height}\nNew Width: {width}\nNew Height: {height}\n")
        resized_img = src_img.resize((int(width), int(height)))
        return ImageLib.crop_to_square(resized_img)
    
    def __create_blurry_square_background(self) -> None:
        self.blurry_bg = ImageLib.get_cropped_square_image(self.get_blurred_image(ImageLib.BLUR_LEVEL))

    def get_squared_image(self) -> Image:
        self.__create_blurry_square_background()
        src_img = self.img
        if(src_img.width < src_img.height):
            margin = (self.blurry_bg.width - src_img.width) / 2
            left = 0
            top = margin
        else:
            margin = (self.blurry_bg.height - src_img.height) / 2
            left = margin
            top = 0

        coordinate = (int(top), int(left))
        self.blurry_bg.paste(self.img, coordinate)
        return self.blurry_bg
        