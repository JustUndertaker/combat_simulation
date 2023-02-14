"""
人物属性
"""
from enum import Enum, auto

from pydantic import BaseModel


# 面板基础属性 = 基础属性+基础数字加成+基础百分比加成
# 面板百分比加成属性 = 面板基础属性*面板百分比加成
# 面板属性 = 面板基础属性+面板数字加成+面板百分比加成
# 人物最终结算时需要先计算基础属性，最后计算面板属性
class Attribute_t(BaseModel):
    """
    人物属性类
    """

    HP: int
    """生命值"""
    ATK: int
    """物攻"""
    DEF: int
    """物防"""
    MGK: int
    """魔攻"""
    RGS: int
    """魔防"""
    HIT: int
    """命中"""
    AVD: int
    """闪避"""

    def __add__(self, other: "Attribute_t") -> "Attribute_t":
        return Attribute_t(
            HP=self.HP + other.HP,
            ATK=self.ATK + other.ATK,
            DEF=self.DEF + other.DEF,
            MGK=self.MGK + other.MGK,
            RGS=self.RGS + other.RGS,
            HIT=self.HIT + other.HIT,
            AVD=self.AVD + other.AVD,
        )

    # 单乘，需要属性在前，加成在后，加成采用百分制加成
    def __mul__(self, other: "Attribute_t") -> "Attribute_t":
        return Attribute_t(
            HP=(int)(self.HP * (other.HP / 100)),
            ATK=(int)(self.ATK * (other.ATK / 100)),
            DEF=(int)(self.DEF * (other.DEF / 100)),
            MGK=(int)(self.MGK * (other.MGK / 100)),
            RGS=(int)(self.RGS * (other.RGS / 100)),
            HIT=(int)(self.HIT * (other.HIT / 100)),
            AVD=(int)(self.AVD * (other.AVD / 100)),
        )


class UnitAttribute_t(BaseModel):
    """人物属性"""

    BaseAttribute: Attribute_t
    """基础属性"""
    BaseNumAddAttribute: Attribute_t
    """基础数字加成属性"""
    BasePerAddAttribute: Attribute_t
    """基础百分比加成属性"""
    NumAddAttribute: Attribute_t
    """数字加成属性"""
    PerAddAttribute: Attribute_t
    """百分比加成属性"""

    @property
    def HP(self) -> int:
        """生命值"""
        return (
            self.BaseAttribute.HP
            + self.BaseNumAddAttribute.HP
            + self.BasePerAddAttribute.HP
            + self.NumAddAttribute.HP
            + self.PerAddAttribute.HP
        )

    @property
    def ATK(self) -> int:
        """物理攻击力"""
        return (
            self.BaseAttribute.ATK
            + self.BaseNumAddAttribute.ATK
            + self.BasePerAddAttribute.ATK
            + self.NumAddAttribute.ATK
            + self.PerAddAttribute.ATK
        )

    @property
    def DEF(self) -> int:
        """物理防御力"""
        return (
            self.BaseAttribute.DEF
            + self.BaseNumAddAttribute.DEF
            + self.BasePerAddAttribute.DEF
            + self.NumAddAttribute.DEF
            + self.PerAddAttribute.DEF
        )

    @property
    def MGK(self) -> int:
        """魔法攻击力"""
        return (
            self.BaseAttribute.MGK
            + self.BaseNumAddAttribute.MGK
            + self.BasePerAddAttribute.MGK
            + self.NumAddAttribute.MGK
            + self.PerAddAttribute.MGK
        )

    @property
    def RGS(self) -> int:
        """魔法防御力"""
        return (
            self.BaseAttribute.RGS
            + self.BaseNumAddAttribute.RGS
            + self.BasePerAddAttribute.RGS
            + self.NumAddAttribute.RGS
            + self.PerAddAttribute.RGS
        )

    @property
    def HIT(self) -> int:
        """命中"""
        return (
            self.BaseAttribute.HIT
            + self.BaseNumAddAttribute.HIT
            + self.BasePerAddAttribute.HIT
            + self.NumAddAttribute.HIT
            + self.PerAddAttribute.HIT
        )

    @property
    def AVD(self) -> int:
        """闪避"""
        return (
            self.BaseAttribute.AVD
            + self.BaseNumAddAttribute.AVD
            + self.BasePerAddAttribute.AVD
            + self.NumAddAttribute.AVD
            + self.PerAddAttribute.AVD
        )

    @property
    def BasePanelAttribute(self) -> Attribute_t:
        """基础面板攻击力"""
        return Attribute_t(
            HP=(
                self.BaseAttribute.HP
                + self.BaseNumAddAttribute.HP
                + self.BasePerAddAttribute.HP
            ),
            ATK=(
                self.BaseAttribute.ATK
                + self.BaseNumAddAttribute.ATK
                + self.BasePerAddAttribute.ATK
            ),
            DEF=(
                self.BaseAttribute.DEF
                + self.BaseNumAddAttribute.DEF
                + self.BasePerAddAttribute.DEF
            ),
            MGK=(
                self.BaseAttribute.MGK
                + self.BaseNumAddAttribute.MGK
                + self.BasePerAddAttribute.MGK
            ),
            RGS=(
                self.BaseAttribute.RGS
                + self.BaseNumAddAttribute.RGS
                + self.BasePerAddAttribute.RGS
            ),
            HIT=(
                self.BaseAttribute.HIT
                + self.BaseNumAddAttribute.HIT
                + self.BasePerAddAttribute.HIT
            ),
            AVD=(
                self.BaseAttribute.AVD
                + self.BaseNumAddAttribute.AVD
                + self.BasePerAddAttribute.AVD
            ),
        )

    @property
    def PanelAttribute(self) -> Attribute_t:
        """面板属性"""
        return Attribute_t(
            HP=self.HP,
            ATK=self.ATK,
            DEF=self.DEF,
            MGK=self.MGK,
            RGS=self.RGS,
            HIT=self.HIT,
            AVD=self.AVD,
        )


class AddAtrributeType_t(Enum):
    """加成类别"""

    BaseNum = auto()
    """基础数值加成"""
    BasePer = auto()
    """基础百分比加成"""
    Num = auto()
    """数值加成"""
    Per = auto()
    """百分比加成"""


class AddAtrribute_t(BaseModel):
    """加成属性"""

    AddAtrributeType: AddAtrributeType_t
    """加成类别"""
    AddAtrribute: Attribute_t
    """加成参数"""
    Added_atrribute: Attribute_t
    """实际加成的数值"""

    def caculate_nums(self, uint_atrribute: UnitAttribute_t) -> None:
        """计算加成属性"""
        match self.AddAtrributeType:
            case AddAtrributeType_t.BaseNum | AddAtrributeType_t.Num:
                self.Added_atrribute = self.AddAtrribute
            case AddAtrributeType_t.BasePer:
                self.Added_atrribute = uint_atrribute.BaseAttribute * self.AddAtrribute
            case AddAtrributeType_t.Per:
                self.Added_atrribute = (
                    uint_atrribute.BasePanelAttribute * self.AddAtrribute
                )
