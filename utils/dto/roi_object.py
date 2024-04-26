import json


class RoiObject:
    """A Data Transfer Object to encapsulate the data of a ROI (Angle, CenterX, CenterY, Height, Identifier & Width).

    Used by the Vision App Classes to manage the attributes of a ROI.

    Can be converted from / to json. """

    def __init__(self, angle: int, center_x: int = None, center_y: int = None, height: int = None,
                 identifier: str = None, width: int = None):
        self.angle = angle
        self.center_x = center_x
        self.center_y = center_y
        self.height = height
        self.identifier = identifier
        self.width = width

    def __str__(self):
        return (f" Angle:{self.angle} CenterX:{self.center_x} CenterY:{self.center_y} Height:{self.height} "
                f"Identifier:{self.identifier} Width:{self.width}")

    @classmethod
    def from_json(cls, data: json):
        check_ident = "Identifier"
        check_angle = "Angle"
        if check_ident not in data:
            identifier = None
        else:
            identifier = data["Identifier"]
        if check_angle not in data:
            angle = None
        else:
            angle = data["Angle"]
        return RoiObject(angle, data["CenterX"], data["CenterY"], data["Height"], identifier,
                         data["Width"])

    def to_json(self) -> json:
        json_str = {"CenterX": self.center_x,
                    "CenterY": self.center_y,
                    "Height": self.height,
                    "Width": self.width}

        if self.identifier is not None:
            json_str = {"CenterX": self.center_x,
                        "CenterY": self.center_y,
                        "Height": self.height,
                        "Identifier": self.identifier,
                        "Width": self.width}
        if self.angle is not None:
            insert_angle = {"Angle": self.angle}
            json_str.update(insert_angle)

        return json_str
