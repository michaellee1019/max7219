# michaellee1019:led_matrix:max7219
A VIAM module to support led matrices with a max7219 chip. The module is a wrapper of the [luma.led-matrix](https://luma-led-matrix.readthedocs.io/en/latest/python-usage.html#x8-led-matrices) python library.

The module was tested with a 3 pack of [EC Buying MAX7219 Dot Matrix Modules](https://www.amazon.com/dp/B0BXDKHZL6)

The first module should be wired to a raspberry pi in the following way:

| Max Pin    | RPI Pin               |
| --------   | -------               |
| VCC        | Any 5v Pin            |
| GND        | Any Ground Pin        |
| DIN        | MOSI Pin 19 / GPIO 10 |
| CS         | CE0 Pin 24 / GPIO 8   |
| CLK        | SCLK Pin 23 / GPIO 11 |

Based on the [official pinout diagram](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html) provided by Raspberry Pi

## Attribute Examples
The following config is used to control a single [HiLetgo MAX7219 Dot Matrix Module](https://www.amazon.com/dp/B07FFV537V).
```
{
    "spi_bus":"0",
    "device":"0",
    "block_orientation": 0,
    "width": 32,
    "height": 24,
    "rotate": 0
}
```

## DoCommand Examples
A single DoCommand call will erase the display and draw a new canvas from scratch. Each DoCommand call can contain a list of drawings to be performed in a single frame, where the screen will not be cleared between each drawing.

### Border
Draws a border around the display using the provided width + height in the attributes of the component. This type has no options available to it.
```
{
    "drawings": [
        {
            "type": "border"
        }
    ]
}
```

### Rectangle
Draw a rectangle on the display. Options:
- `pixels`: An array of integers representing the start and end pixels to draw the rectangle. Provide the coordinates a list of four integers like `[start_x, start_y, end_x, end_y]`.
```
{
    "drawings": [
        {
            "type": "rectangle",
            "pixels": [
                0,
                0,
                4,
                5
            ]
        }
    ]
}
```

### Text
Write text to the display. Options:
- `message`: The text to display
- `start_pixel`: The xy coordinates to start the text. Helpful to center text visually. Provide the coordinates a list of two integers like `[x, y]`.
- `font`: The font to use, defaults to `LCD_FONT` if not provided. The other option is `CP437_FONT` which provides thicker "bold" letters.
```
{
    "drawings": [
        {
            "type": "text",
            "message": "VIAM",
            "start_pixel": [
                3,
                0
            ],
            "font": "CP437_FONT"
        }
    ]
}
```

### Point
Light up a single pixel on the display. Options:
- `pixel` The xy coordinates of the pixel. Provide the coordinates a list of two integers like `[x, y]`.
```
{
    "drawings": [
        {
            "type": "point",
            "pixel": [
                3,
                0
            ]
        }
    ]
}
```

### Line
Draw a line of pixels on the display. Options:
- `pixels`: An array of integers representing the start and end pixels to draw the line. Provide the coordinates a list of four integers like `[start_x, start_y, end_x, end_y]`.
```
{
    "drawings": [
        {
            "type": "line",
            "pixels": [
                0,
                0,
                0,
                5
            ]
        }
    ]
}
```

### Clear
Erases all pixels on the display to show a blank screen.
```
{
    "drawings": [
        {
            "type": "clear"
        }
    ]
}
```

### Multiple drawings.
Provide a list of drawings to place multiple elements on to the screen. The next DoCommand will erase the screen
```
{
    "drawings": [
        {
            "type": "point",
            "pixel": [
                0,
                0
            ]
        },
        {
            "type": "text",
            "message": "VIAM",
            "start_pixel": [
                3,
                0
            ]
        },
        {
            "type": "line",
            "pixels": [
                31,
                0,
                31,
                7
            ]
        }
    ]
}
```