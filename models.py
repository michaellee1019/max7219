#!/usr/bin/env viam-wrap
import codecs
import sys
from typing import Mapping, Optional
from typing_extensions import Self
import viam_wrap
from viam.components.generic import Generic
from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.utils import ValueTypes
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily
from viam.components.generic import Generic
from google.protobuf import json_format
from viam.services.service_base import ServiceBase
from viam import logging
from viam.components.camera import Camera

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT, CP437_FONT
from luma.led_matrix.device import max7219

class MAX7219(Generic):
    MODEL = 'michaellee1019:led_matrix:max7219'

    serial = None
    device = None

    @classmethod
    def new(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        output = self(config.name)
        output.reconfigure(config, dependencies)
        return output

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        result = {key: False for key in command.keys()}
        drawings = command.get("drawings")
        with canvas(self.device) as draw:
            for drawing in drawings:
                match drawing["type"]:
                    case "border":
                        self.border(draw)
                    case "rectangle":
                        pixels = drawing["pixels"]
                        self.rectangle(draw, pixels)
                    case "text":
                        message = drawing["message"]
                        start_pixel = drawing["start_pixel"]
                        font = drawing.get("font")
                        self.text(draw, start_pixel, message, font)
                    case "point":
                        pixel = drawing["pixel"]
                        self.point(draw, pixel)
                    case "line":
                        pixels = drawing["pixels"]
                        width = drawing.get("width")
                        self.line(draw, pixels, width)
                    case "clear":
                        self.clear()
        result["drawings"] = True
        return result

    def border(self, draw):
        draw.rectangle(self.device.bounding_box, outline="white")

    def rectangle(self, draw, pixels: list[int]):
        draw.rectangle(pixels, outline="white")

    def text(self, draw, start_pixel: list[int], message: str, font):
        font_cls = LCD_FONT
        if font == "CP437_FONT":
            font_cls = CP437_FONT
        text(draw, start_pixel, message, fill="white", font=proportional(font_cls))

    def point(self, draw, pixel: list[int]):
        draw.point(pixel, fill="white")

    def line(self, draw, pixels: list[int], width):
        if not width:
            width=1
        draw.line(pixels, fill="white", width=width)

    def clear(self):
        self.device.clear()

    def reconfigure(self,
                    config: ComponentConfig,
                    dependencies: Mapping[ResourceName, ResourceBase]):
        
        #Cleanup the screen and previous drawings on reconfigure
        if self.device is not None:
            self.device.cleanup()

        spi_bus = int(config.attributes.fields["spi_bus"].string_value)
        chip_select = int(config.attributes.fields["chip_select"].string_value)
        block_orientation = int(config.attributes.fields["block_orientation"].number_value)
        width = int(config.attributes.fields["width"].number_value)
        height = int(config.attributes.fields["height"].number_value)
        rotate = config.attributes.fields["rotate"].bool_value
        if rotate:
            rotate=1

        self.serial = spi(port=spi_bus, device=chip_select, gpio=noop(), block_orientation=block_orientation)
        self.device = max7219(self.serial, width=width, height=height, rotate=rotate)

    @classmethod
    def validate_config(self, config: ComponentConfig) -> None:
        # Custom validation can be done by specifiying a validate function like this one. Validate functions
        # can raise errors that will be returned to the parent through gRPC. Validate functions can
        # also return a sequence of strings representing the implicit dependencies of the resource.
        return None

if __name__ == '__main__':
    # necessary for pyinstaller to see it
    # build this with: 
    # pyinstaller --onefile --hidden-import viam-wrap --paths $VIRTUAL_ENV/lib/python3.10/site-packages installable.py 
    # `--paths` arg may no longer be necessary once viam-wrap is published somewhere
    # todo: utility to append this stanza automatically at build time
    viam_wrap.main(sys.modules.get(__name__))