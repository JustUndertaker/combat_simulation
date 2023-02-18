from combat_simulation import Attribute_t, Battle, Unit, UnitAttribute_t

if __name__ == "__main__":
    base_attr = Attribute_t(HP=1000, ATK=50, DEF=10, MGK=10, RGS=20, HIT=80)
    base_attr2 = Attribute_t(HP=1000, ATK=10, DEF=20, MGK=50, RGS=10, HIT=80)

    unit_one = Unit("小明", attribute=UnitAttribute_t(base_attribute=base_attr))
    unit_two = Unit("小红", attribute=UnitAttribute_t(base_attribute=base_attr2))

    battle = Battle(unit_one, unit_two)
    battle.run()
