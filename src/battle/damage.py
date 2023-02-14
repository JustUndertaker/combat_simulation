"""
伤害计算，战斗计算在这里
"""
from abc import ABC, abstractmethod
from enum import Enum, auto
from random import randint

from pydantic import BaseModel

from ..uint.attribute import Attribute_t


class DamageType(Enum):
    """伤害类型"""

    Physical = auto()
    """物理伤害"""
    Magic = auto()
    """魔法伤害"""
    Real = auto()
    """真实伤害"""
    Custom = auto()
    """自定义伤害，自己计算"""


class DamageStatus(Enum):
    """伤害状态"""

    Normal = auto()
    """正常造成伤害"""
    CriticalBlow = auto()
    """暴击"""
    Missed = auto()
    """未命中"""
    Withstanded = auto()
    """抵消"""


class Damage_t(BaseModel):
    """单次伤害类"""

    damage: int
    """伤害值"""
    damage_type: DamageType
    """伤害类型"""
    damage_status: DamageStatus
    """伤害状态"""


class DamageBase(ABC):
    """伤害类基础"""

    @abstractmethod
    def get_damagetype(self) -> DamageType:
        """获取伤害类型"""
        raise NotImplementedError

    @abstractmethod
    def caculate_damage(self, attacker: Attribute_t, target: Attribute_t) -> Damage_t:
        """
        说明:
            计算伤害值，给出初始的伤害

        参数:
            * `attacker`：攻击者的最终属性
            * `target`：目标的最终属性

        返回:
            * `Damage_t`：计算出的伤害
        """
        raise NotImplementedError


class DamagePhysical(DamageBase):
    """物理伤害"""

    def get_damagetype(self) -> DamageType:
        return DamageType.Physical

    def caculate_damage(self, attacker: Attribute_t, target: Attribute_t) -> Damage_t:
        # 计算命中
        hit = attacker.HIT - target.AVD
        if hit < 0:
            hit = 0
        if randint(0, 100) > hit:
            # 未命中
            return Damage_t(
                damage=0,
                damage_type=self.get_damagetype(),
                damage_status=DamageStatus.Missed,
            )

        # 计算
        damage = attacker.ATK - target.DEF
        if damage < 0:
            damage = 0

        return Damage_t(
            damage=damage,
            damage_type=self.get_damagetype(),
            damage_status=DamageStatus.Normal,
        )


class DamageMagic(DamageBase):
    """魔法伤害"""

    def get_damagetype(self) -> DamageType:
        return DamageType.Magic

    def caculate_damage(self, attacker: Attribute_t, target: Attribute_t) -> Damage_t:
        damage = attacker.MGK - target.RGS
        if damage < 0:
            damage = 0

        return Damage_t(
            damage=damage,
            damage_type=self.get_damagetype(),
            damage_status=DamageStatus.Normal,
        )


class DamageReal(DamageBase):
    """真实伤害"""

    def get_damagetype(self) -> DamageType:
        return DamageType.Real

    def caculate_damage(self, attacker: Attribute_t, target: Attribute_t) -> Damage_t:
        return Damage_t(
            damage=attacker.ATK,
            damage_type=self.get_damagetype(),
            damage_status=DamageStatus.Normal,
        )
