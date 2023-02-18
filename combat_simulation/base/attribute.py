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

    HP: int = 0
    """生命值"""
    ATK: int = 0
    """物攻"""
    DEF: int = 0
    """物防"""
    MGK: int = 0
    """魔攻"""
    RGS: int = 0
    """魔防"""
    HIT: int = 0
    """命中"""
    AVD: int = 0
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

    base_attribute: Attribute_t = Attribute_t()
    """基础属性"""
    base_numadd_attribute: Attribute_t = Attribute_t()
    """基础数字加成属性"""
    base_peradd_attribute: Attribute_t = Attribute_t()
    """基础百分比加成属性"""
    numadd_attribute: Attribute_t = Attribute_t()
    """数字加成属性"""
    peradd_attribute: Attribute_t = Attribute_t()
    """百分比加成属性"""

    @property
    def HP(self) -> int:
        """最大生命值"""
        return (
            self.base_attribute.HP
            + self.base_numadd_attribute.HP
            + self.base_peradd_attribute.HP
            + self.numadd_attribute.HP
            + self.peradd_attribute.HP
        )

    @property
    def ATK(self) -> int:
        """物理攻击力"""
        return (
            self.base_attribute.ATK
            + self.base_numadd_attribute.ATK
            + self.base_peradd_attribute.ATK
            + self.numadd_attribute.ATK
            + self.peradd_attribute.ATK
        )

    @property
    def DEF(self) -> int:
        """物理防御力"""
        return (
            self.base_attribute.DEF
            + self.base_numadd_attribute.DEF
            + self.base_peradd_attribute.DEF
            + self.numadd_attribute.DEF
            + self.peradd_attribute.DEF
        )

    @property
    def MGK(self) -> int:
        """魔法攻击力"""
        return (
            self.base_attribute.MGK
            + self.base_numadd_attribute.MGK
            + self.base_peradd_attribute.MGK
            + self.numadd_attribute.MGK
            + self.peradd_attribute.MGK
        )

    @property
    def RGS(self) -> int:
        """魔法防御力"""
        return (
            self.base_attribute.RGS
            + self.base_numadd_attribute.RGS
            + self.base_peradd_attribute.RGS
            + self.numadd_attribute.RGS
            + self.peradd_attribute.RGS
        )

    @property
    def HIT(self) -> int:
        """命中"""
        return (
            self.base_attribute.HIT
            + self.base_numadd_attribute.HIT
            + self.base_peradd_attribute.HIT
            + self.numadd_attribute.HIT
            + self.peradd_attribute.HIT
        )

    @property
    def AVD(self) -> int:
        """闪避"""
        return (
            self.base_attribute.AVD
            + self.base_numadd_attribute.AVD
            + self.base_peradd_attribute.AVD
            + self.numadd_attribute.AVD
            + self.peradd_attribute.AVD
        )

    @property
    def base_panel_attribute(self) -> Attribute_t:
        """基础面板攻击力"""
        return Attribute_t(
            HP=(
                self.base_attribute.HP
                + self.base_numadd_attribute.HP
                + self.base_peradd_attribute.HP
            ),
            ATK=(
                self.base_attribute.ATK
                + self.base_numadd_attribute.ATK
                + self.base_peradd_attribute.ATK
            ),
            DEF=(
                self.base_attribute.DEF
                + self.base_numadd_attribute.DEF
                + self.base_peradd_attribute.DEF
            ),
            MGK=(
                self.base_attribute.MGK
                + self.base_numadd_attribute.MGK
                + self.base_peradd_attribute.MGK
            ),
            RGS=(
                self.base_attribute.RGS
                + self.base_numadd_attribute.RGS
                + self.base_peradd_attribute.RGS
            ),
            HIT=(
                self.base_attribute.HIT
                + self.base_numadd_attribute.HIT
                + self.base_peradd_attribute.HIT
            ),
            AVD=(
                self.base_attribute.AVD
                + self.base_numadd_attribute.AVD
                + self.base_peradd_attribute.AVD
            ),
        )

    @property
    def panel_attribute(self) -> Attribute_t:
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

    add_atrribute_type: AddAtrributeType_t
    """加成类别"""
    add_atrribute: Attribute_t
    """加成参数"""
    added_atrribute: Attribute_t
    """实际加成的数值"""

    def caculate_nums(self, uint_atrribute: UnitAttribute_t) -> None:
        """计算加成属性"""
        match self.add_atrribute_type:
            case AddAtrributeType_t.BaseNum | AddAtrributeType_t.Num:
                self.added_atrribute = self.add_atrribute
            case AddAtrributeType_t.BasePer:
                self.added_atrribute = (
                    uint_atrribute.base_attribute * self.add_atrribute
                )
            case AddAtrributeType_t.Per:
                self.added_atrribute = (
                    uint_atrribute.base_panel_attribute * self.add_atrribute
                )
