from rgbmatrix import RGBMatrix, RGBMatrixOptions

class Display(object):
    def __init__(self, brightness: int):
        options = RGBMatrixOptions()
        options.brightness = brightness
        options.rows = 32
        options.cols = 64
        options.chain_length = 1
        options.parallel = 1
        options.pwm_bits = 11
        options.hardware_mapping = 'regular'
        options.pwm_lsb_nanoseconds = 130
        options.gpio_slowdown = 1
        options.led_rgb_sequence = 'RGB'
        options.pixel_mapper_config = ''
        options.row_address_type = 0
        options.multiplexing = 0
        self.matrix = RGBMatrix(options=options)