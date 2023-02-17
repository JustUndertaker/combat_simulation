"""
战斗类
"""
from ..record import BattleRecord
from ..uint import Unit


class Battle:
    """
    战斗类，管理一场战斗
    """

    attacker: Unit
    """攻击方"""
    target: Unit
    """防守方"""
    battle_record: BattleRecord
    """战斗记录"""

    def __init__(self, attacker: Unit, target: Unit) -> None:
        self.attacker = attacker
        self.target = target

    def init(self) -> None:
        """初始化参数"""
        pass

    def run(self) -> None:
        """开始战斗"""
        pass
