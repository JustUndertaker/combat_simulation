"""
记录类，用来记录战斗过程
"""
from pydantic import BaseModel

from ..battle.damage import Damage_t


class Record(BaseModel):
    """
    一条战斗记录
    """

    attacker_name: str
    """攻击方名字"""
    target_name: str
    """被攻击方名字"""
    damage: Damage_t
    """伤害记录"""
    description: str
    """战斗描述"""


class BattleRecord(BaseModel):
    """战斗记录类"""

    records: list[Record]
    """战斗记录列表"""
