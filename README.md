# Fractals
This is a simple tool written in python, that allows you to generate fractals and save them in high resolution.

## Installation
You can download this repo and then install required libraries by running this command in the project directory:
```
pip3 install -r requirements.txt
```

## Usage
After launching `main.pyw` file you should see this interface:

![](https://i.imgur.com/sHhHur3.png)
There are four parameters that you can change:
1. `Escape boundary` - determines how far should point go from the origin to be considered as escaped.
2. `Max iteration` - maximum number of iteration function calls, after which point is considered as not escaped.
3. `Iteration function` - consists of `c` (constant value) and `z` (iterable value).
4. `Complex value` - constant value, selected by clicking on complex plane.

After changing parameteres, press `Render` button to see the results. To save fractal press `Save` button. You can change the resolution of saved fractals (and other parameters, like window size) in `config.cfg` file.

## Fractal example
Example of generated 10000x10000 image of fractal:

![](https://i.redd.it/r563uzyx8bv31.png)
