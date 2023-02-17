"""
单位
"""

from .attribute import UnitAttribute_t


class Unit:
    """单位类"""

    unit_attribute: UnitAttribute_t
    """单位属性"""

    def __init__(self, attribute: UnitAttribute_t) -> None:
        self.unit_attribute = attribute

    def ResetHP(self) -> None:
        """重置生命值"""
        self.unit_attribute.ResetHP()
