class FractalGenerator:
    from PIL import Image

    def __init__(self, config, render=False):
        category = 'Save' if render else 'General'

        self.pixel_height = int(config[category]['pixel_height'])
        self.pixel_width = int(config[category]['pixel_width'])
        self.real_max_value = float(config[category]['real_max_value'])
        self.real_min_value = float(config[category]['real_min_value'])
        self.imaginary_max_value = float(config[category]['imaginary_max_value'])
        self.imaginary_min_value = float(config[category]['imaginary_min_value'])

        self.escaped_color_1 = eval(config['Appearance']['escaped_color_1'])
        self.escaped_color_2 = eval(config['Appearance']['escaped_color_2'])
        self.not_escaped_color = eval(config['Appearance']['not_escaped_color'])

        self.dy = (self.imaginary_max_value - self.imaginary_min_value) / (self.pixel_height - 1)
        self.dx = (self.real_max_value - self.real_min_value) / (self.pixel_width - 1)

    def render_image(self, c, escape_boundary, max_iteration, iteration_function):

        arr = []
        for y in range(self.pixel_height - 1, -1, -1):
            for x in range(self.pixel_width):
                z = ((x * self.dx) + self.real_min_value) + (((y * self.dy) + self.imaginary_min_value) * 1j)
                for _ in range(max_iteration):
                    z = iteration_function(z, c)
                    if abs(z) >= escape_boundary:
                        arr.append(self.__get_color(z))
                        break
                else:
                    arr.append(self.not_escaped_color)

        img = self.Image.new('RGB', (self.pixel_width, self.pixel_height))
        img.putdata(tuple(arr))
        return img

    def __get_color(self, z):
        if (z.real > 0 and z.imag > 0) or (z.real < 0 and z.imag < 0):
            return self.escaped_color_1
        else:
            return self.escaped_color_2
