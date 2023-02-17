from combat_simulation import Attribute_t, Battle, Unit, UnitAttribute_t

if __name__ == "__main__":
    attr_one = UnitAttribute_t(
        base_attribute=Attribute_t(),
        base_numadd_attribute=Attribute_t(),
        base_peradd_attribute=Attribute_t(),
        numadd_attribute=Attribute_t(),
        peradd_attribute=Attribute_t(),
    )
    unit_one = Unit("小明", attribute=attr_one)
    unit_two = Unit("小红", attribute=attr_one)

    battle = Battle(unit_one, unit_two)
    battle.run()
