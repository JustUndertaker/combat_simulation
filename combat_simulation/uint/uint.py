"""
单位
"""

from ..base.attribute import UnitAttribute_t
from ..base.damage import Damage_t, DamageStatus


class Unit:
    """单位类"""

    name: str
    """名称"""
    HP: int
    """当前生命"""
    unit_attribute: UnitAttribute_t
    """单位属性"""

    def __init__(self, name: str, attribute: UnitAttribute_t) -> None:
        self.name = name
        self.unit_attribute = attribute

    @property
    def alive(self) -> bool:
        """存活状态"""
        return self.HP > 0

    def reset_HP(self) -> None:
        """重置生命值"""
        self.HP = self.unit_attribute.HP

    def get_hurt(self, damage: Damage_t) -> None:
        """单位受伤"""
        if damage.status == DamageStatus.Missed:
            return

        if damage.value > self.HP:
            self.HP = 0
        else:
            self.HP -= damage.value
