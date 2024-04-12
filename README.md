# michaellee1019:led_matrix:max7219
A VIAM module to support led matrices with a max7219 chip. The module is a wrapper of the [luma.led-matrix](https://luma-led-matrix.readthedocs.io/en/latest/python-usage.html#x8-led-matrices) python library

## Attribute Examples
The following config is used to control a single [HiLetgo MAX7219 Dot Matrix Module](https://www.amazon.com/dp/B07FFV537V).
```
{
    "spi_bus":"0",
    "chip_select":"0",
    "block_orientation": 0,
    "width": 8,
    "height": 32,
    "rotate": true
}
```

## DoCommand Examples
A single DoCommand call will erase the display and draw a new canvas from scratch. Each DoCommand call can contain a list of drawings to be performed in a single frame, where the screen will not be cleared between each drawing.

```
{
    "drawings": [
        {
            "type": "border"
        }
    ]
}
```