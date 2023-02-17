"""
记录类，用来记录战斗过程
"""
from pydantic import BaseModel

from ..battle.damage import Damage_t, DamageStatus, DamageType


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
    remain_hp: int
    """目标剩余血量"""

    def get_description(self) -> str:
        """获取战斗描述"""
        match self.damage.status:
            case DamageStatus.Normal:
                status = "命中了"
            case DamageStatus.CriticalBlow:
                status = "暴击了"
            case DamageStatus.Missed:
                status = "打偏了"
            case DamageStatus.Withstanded:
                status = "被抵消了"
        match self.damage.type:
            case DamageType.Physical:
                _type = "物理伤害"
            case DamageType.Magic:
                _type = "魔法伤害"
            case DamageType.Real:
                _type = "真实伤害"
            case DamageType.Custom:
                _type = "未知伤害"
        return f"{self.attacker_name} 对 {self.target_name} {status} {self.damage.value}点的 {_type}，剩余生命值：{self.remain_hp}\n"


class BattleRecord(BaseModel):
    """战斗记录类"""

    records: list[Record]
    """战斗记录列表"""

    def add(self, record: Record) -> None:
        """添加一条记录"""
        self.records.append(record)
