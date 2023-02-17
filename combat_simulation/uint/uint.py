"""
单位
"""

from .attribute import UnitAttribute_t


class Unit:
    """单位类"""

    UnitAttribute: UnitAttribute_t
    """单位属性"""

    def __init__(self, attribute: UnitAttribute_t) -> None:
        self.UnitAttribute = attribute
