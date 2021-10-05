from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFit


class BrandLogoListingImageSpec(ImageSpec):
    processors = [ResizeToFit(100, 50)]
    format = "PNG"
    options = {"quality": 80}


register.generator("recorders:brand_logo_listing", BrandLogoListingImageSpec)
