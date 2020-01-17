import tkinter
from core import FractalGenerator
from PIL import ImageTk
from configparser import ConfigParser
from cmath import *


class GeneratorUI:
    def __init__(self, master):
        self.master = master

        self.config = config = ConfigParser()
        config.read('config.cfg')
        self.c_point_radius = int(config['Appearance']['c_point_radius'])

        master.title('Fractal generator')
        master.resizable(False, False)
        master.geometry(str(int(config['General']['pixel_width']) + 202) + 'x'
                        + str(max(int(config['General']['pixel_height']), 500)))

        tkinter.Label(master, text='Escape boundary:').place(x=45, y=0)
        self.escape_boundary = tkinter.Entry(root, width=10)
        self.escape_boundary.insert(0, config['General']['default_escape_boundary'])
        self.escape_boundary.place(x=60, y=25)

        tkinter.Label(master, text='Max iteration:').place(x=55, y=60)
        self.max_iteration = tkinter.Entry(root, width=10)
        self.max_iteration.insert(0, config['General']['default_max_iteration'])
        self.max_iteration.place(x=60, y=85)

        tkinter.Label(master, text='Iteration function:').place(x=40, y=120)
        self.iteration_function = tkinter.Entry(root, width=25)
        self.iteration_function.insert(0, config['General']['default_iteration_function'])
        self.iteration_function.place(x=20, y=145)

        self.c = complex(config['General']['default_c'].replace('i', 'j'))
        tkinter.Label(master, text='Complex value:').place(x=50, y=180)
        self.c_entry = tkinter.Canvas(width=177, height=177, bg='azure3')
        self.c_entry.place(x=8, y=210)
        self.c_entry.create_line(90, 0, 90, 182)
        self.c_entry.create_line(0, 90, 182, 90)
        oval_x = round((self.c.real + 1) * 90)
        oval_y = 180 - round((self.c.imag + 1) * 90)
        self.c_entry.create_oval(oval_x - self.c_point_radius, oval_y - self.c_point_radius,
                                 oval_x + self.c_point_radius, oval_y + self.c_point_radius,
                                 outline='', fill='red3', tag='circle')
        self.c_text = tkinter.StringVar()
        self.c_print = tkinter.Label(root, textvariable=self.c_text)
        self.c_text.set(str(round(self.c.real, 3)) + ' + ' + str(round(self.c.imag, 3)) + 'i')
        self.c_print.place(x=55, y=400)
        self.c_entry.bind("<Button-1>", self.update_c)

        self.render_button = tkinter.Button(master, text="Render", width=10, height=3, command=self.draw)
        self.render_button.place(x=100, y=430)

        self.save_button = tkinter.Button(master, text="Save", width=10, height=3, command=self.save)
        self.save_button.place(x=10, y=430)

        self.canvas = tkinter.Canvas(master, width=int(config['General']['pixel_width']),
                                     height=int(config['General']['pixel_height']))
        self.canvas.place(x=200, y=-2)

        self.generator = FractalGenerator(config)
        self.save_generator = FractalGenerator(config, render=True)
        self.image_pos_x = int(config['General']['pixel_width']) // 2 + 2
        self.image_pos_y = int(config['General']['pixel_height']) // 2 + 2

        if config['General']['render_at_start'] == 'True':
            self.image = self.generator.render_image(self.c, float(self.escape_boundary.get()),
                                                     int(self.max_iteration.get()),
                                                     eval('lambda z, c: ' + self.iteration_function.get()))
            self.image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image((self.image_pos_x, self.image_pos_y), image=self.image)

    def update_c(self, event):
        self.c_entry.delete('circle')
        self.c_entry.create_oval(event.x - self.c_point_radius, event.y - self.c_point_radius,
                                 event.x + self.c_point_radius, event.y + self.c_point_radius,
                                 outline='', fill='red3', tag='circle')
        c_real = (event.x / 180 * 2) - 1
        c_imaginary = -((event.y / 180 * 2) - 1)
        self.c = c_real + c_imaginary * 1j
        self.c_text.set(str(round(self.c.real, 3)) + ' + ' + str(round(self.c.imag, 3)) + 'i')

    def draw(self):
        self.canvas.delete('ALL')
        self.image = self.generator.render_image(self.c, float(self.escape_boundary.get()),
                                                 int(self.max_iteration.get()),
                                                 eval('lambda z, c: ' + self.iteration_function.get()))
        self.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image((self.image_pos_x, self.image_pos_y), image=self.image)
        self.canvas.update()

    def save(self):
        img = self.save_generator.render_image(self.c, float(self.escape_boundary.get()),
                                               int(self.max_iteration.get()),
                                               eval('lambda z, c: ' + self.iteration_function.get()))
        img.save(self.config['Save']['filename'] + '.png', 'PNG')


root = tkinter.Tk()
ui = GeneratorUI(root)
root.mainloop()
