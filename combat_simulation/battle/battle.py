"""
战斗类
"""
import random

from ..base.damage import Damage_t, DamageMagic, DamagePhysical, DamageReal, DamageType
from ..record import BattleRecord, Record
from ..uint import Unit


class BattleRound:
    """战斗回合"""

    @classmethod
    def battle_get_damage(cls, attacker: Unit, target: Unit) -> Damage_t:
        """战斗一回合，获取伤害"""
        damage_type = random.choice(
            [DamageType.Physical, DamageType.Magic, DamageType.Real]
        )
        damage_cal = DamagePhysical()
        match damage_type:
            case DamageType.Physical:
                damage_cal = DamagePhysical()
            case DamageType.Magic:
                damage_cal = DamageMagic()
            case DamageType.Real:
                damage_cal = DamageReal()
        return damage_cal.caculate_damage(
            attacker.unit_attribute.panel_attribute,
            target.unit_attribute.panel_attribute,
        )

    @classmethod
    def checkout_damage(cls, attacker: Unit, target: Unit, damage: Damage_t) -> Record:
        """结算伤害，生成记录"""
        target.get_hurt(damage)
        return Record(
            attacker_name=attacker.name,
            target_name=target.name,
            damage=damage,
            remain_hp=target.HP,
        )


class Battle:
    """
    战斗类，管理一场战斗
    """

    attacker: Unit
    """攻击方"""
    target: Unit
    """防守方"""
    winner: Unit
    """获胜方"""
    loser: Unit
    """失败方"""
    battle_record: BattleRecord
    """战斗记录"""

    def __init__(self, attacker: Unit, target: Unit) -> None:
        self.attacker = attacker
        self.target = target
        self.battle_record = BattleRecord()

    def init(self) -> None:
        """初始化参数"""
        pass

    def run(self) -> None:
        """开始战斗"""
        self.attacker.reset_HP()
        self.target.reset_HP()
        self.print_battle_open()
        flag = True
        while self.check_battle_is_in_progress():
            self.battle_one_round(flag)
            flag = not flag

        self.print_battle_end()

    def print_battle_open(self) -> None:
        """开场台词！"""
        print(f"{self.attacker.name} 对 {self.target.name} 发起挑战，战斗开始！\n")

    def print_battle_end(self) -> None:
        """结束台词"""
        msg = "------战斗结束！！！！-----\n" f"胜者是 {self.winner.name} ！让我们恭喜他！"
        print(msg)

    def check_battle_is_in_progress(self) -> bool:
        """
        检测战斗是否继续进行，当有一方未存活时结束战斗
        """
        if not self.attacker.alive:
            self.winner = self.target
            self.loser = self.attacker
            return False

        if not self.target.alive:
            self.winner = self.attacker
            self.loser = self.target
            return False
        return True

    def battle_one_round(self, flag: bool) -> None:
        """战斗一回合"""
        if flag:
            damage = BattleRound.battle_get_damage(self.attacker, self.target)
            record = BattleRound.checkout_damage(self.attacker, self.target, damage)
        else:
            damage = BattleRound.battle_get_damage(self.target, self.attacker)
            record = BattleRound.checkout_damage(self.target, self.attacker, damage)
        print(record.get_description())
        self.battle_record.add(record)
