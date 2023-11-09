import math
import sys

'''
ARCHERS EMBRACE

Ranged weapons with attack speed 4 or above have this stat halved, rounded down

Ranged weapons with attack speed 3 or below have this stat halved, rounded up

10% chance that the weapon will fire an extra projectile

Ranged accuracy is increased by 100%
'''

ranged_level = 99
prayer_bonus = 1.2 # rigour 1.2
potion_bonus = 1.15 # super ranging potion 1.15
other_bonus = 1.0

ammo = {
    'dragon_arrow': {'ranged_attack_bonus': 0, 'ranged_strength_bonus': 60},
    'rune_arrow': {'ranged_attack_bonus': 0, 'ranged_strength_bonus': 49},
    'amethyst_arrow': {'ranged_attack_bonus': 0, 'ranged_strength_bonus': 55},
    'diamond_bolts_e': {'ranged_attack_bonus': 0, 'ranged_strength_bonus': 105},
    'diamond_dragon_bolts_e': {'ranged_attack_bonus': 0, 'ranged_strength_bonus': 122},
    'ruby_bolts_e': {'ranged_attack_bonus': 0, 'ranged_strength_bonus': 103},
    'ruby_dragon_bolts_e': {'ranged_attack_bonus': 0, 'ranged_strength_bonus': 122},
    'none': {'ranged_attack_bonus': 0, 'ranged_strength_bonus': 0},

}

weapons = {
    'rune_crossbow': {'ranged_attack_bonus': 90, 'ranged_strength_bonus': 0, 'speed': 6},
    'armadyl_crossbow': {'ranged_attack_bonus': 100, 'ranged_strength_bonus': 0, 'speed': 6},
    'zaryte_crossbow': {'ranged_attack_bonus': 110, 'ranged_strength_bonus': 0, 'speed': 6},
    'twisted_bow': {'ranged_attack_bonus': 70, 'ranged_strength_bonus': 20, 'speed': 5},
    'armadyl_crossbow_buckler': {'ranged_attack_bonus': 108, 'ranged_strength_bonus': 10, 'speed': 6},
    'zaryte_crossbow_buckler': {'ranged_attack_bonus': 118, 'ranged_strength_bonus': 10, 'speed': 6},
    'rune_crossbow_buckler': {'ranged_attack_bonus': 128, 'ranged_strength_bonus': 10, 'speed': 6},
}

gear = {
    'zaryte_vambs': {'ranged_attack_bonus': 18, 'ranged_strength_bonus': 2},
    'masori_hat': {'ranged_attack_bonus': 12, 'ranged_strength_bonus': 2},
    'masori_top': {'ranged_attack_bonus': 43, 'ranged_strength_bonus': 4},
    'masori_bottom': {'ranged_attack_bonus': 27, 'ranged_strength_bonus': 2},
    'void_gloves': {'ranged_attack_bonus': 0, 'ranged_strength_bonus': 0},
    'void_hat': {'ranged_attack_bonus': 0, 'ranged_strength_bonus': 0},
    'void_top': {'ranged_attack_bonus': 0, 'ranged_strength_bonus': 0},
    'void_bottom': {'ranged_attack_bonus': 0, 'ranged_strength_bonus': 0},
    'pegasian_boots': {'ranged_attack_bonus': 12, 'ranged_strength_bonus': 0},
    'archers_ring': {'ranged_attack_bonus': 8, 'ranged_strength_bonus': 8},
    'avas_attractor': {'ranged_attack_bonus': 8, 'ranged_strength_bonus': 2},
}

monsters = {
    'nex': {'defence_level': 260, 'ranged_defence_bonus': 190},
    'vorkath': {'defence_level': 214, 'ranged_defence_bonus': 26},
    'olm': {'defence_level': 250, 'ranged_defence_bonus': 50},
    'warden': {'defence_level': 150, 'ranged_defence_bonus': 20},
    'zebak': {'defence_level': 70, 'ranged_defence_bonus': 110},
}

def calculate_hit_chance(attack_roll, defence_roll):
    """
    Calculate the probability of hitting the target based on attack and defense rolls.
    """
    if attack_roll > defence_roll:
        return 1 - ((defence_roll + 2) / (2 * (attack_roll + 1)))
    else:
        return attack_roll / (2 * (defence_roll + 1))


def calculate_attack_roll(ranged_level, weapon, ammo_type, gear_selected, prayer_bonus, potion_bonus, other_bonus, attack_style):
    void_items = {'void_hat', 'void_top', 'void_bottom', 'void_gloves'}
    void_modifier = 1.125 if void_items.issubset(gear_selected) else 1.0
    # Apply the attack style bonus to the base ranged level
    attack_style_bonus = 3 if attack_style == 'accurate' else 0
    
    # Calculate the effective ranged level
    effective_ranged_level = math.floor(ranged_level + attack_style_bonus + 8)
    
    # Apply the other bonuses and round down
    effective_ranged_level = math.floor(effective_ranged_level * prayer_bonus * potion_bonus * other_bonus)
    
    # Calculate the total ranged attack bonus from equipment
    ranged_attack_bonus = sum(gear[item]['ranged_attack_bonus'] for item in gear_selected) \
                          + weapons[weapon]['ranged_attack_bonus'] \
                          + ammo[ammo_type]['ranged_attack_bonus']
    
    ranged_attack_bonus *= 2
    
    # Apply the formula according to the documentation provided
    return effective_ranged_level * (ranged_attack_bonus + 64)


def calculate_max_ranged_hit(ranged_level, weapon, ammo_type, gear_selected, prayer_bonus, potion_bonus, other_bonus, attack_style):
    # Apply the attack style bonus to the base ranged level
    attack_style_bonus = 3 if attack_style == 'accurate' else 0

    # Calculate the effective ranged level
    effective_ranged_level = math.floor((math.floor(ranged_level * prayer_bonus * potion_bonus) + attack_style_bonus + 8))

    # Calculate the total ranged strength bonus from equipment
    ranged_strength_bonus = sum(gear[item]['ranged_strength_bonus'] for item in gear_selected) \
                            + weapons[weapon]['ranged_strength_bonus'] \
                            + ammo[ammo_type]['ranged_strength_bonus']
    
    # Calculate the max hit using the effective ranged level and strength bonus
    max_hit = math.floor(0.5 + effective_ranged_level * (ranged_strength_bonus + 64) / 640)
    
    return max_hit


def get_attack_speed(weapon, attack_style):
    """
    Get the attack speed of the weapon, modified by the attack style if necessary.
    Now also modifies based on new rules for attack speed adjustments.
    """
    base_speed = weapons[weapon]['speed']
    # Modify the attack speed based on the new rules
    if base_speed >= 4:
        base_speed = math.floor(base_speed / 2)  # halve and round down for speed 4 or above
    else:
        base_speed = math.ceil(base_speed / 2)   # halve and round up for speed 3 or below

    return base_speed

def calculate_defence_roll(monster_name):
    """
    Calculate the target's total defense roll for ranged attacks based on the monster's stats.
    """
    monster_stats = monsters.get(monster_name, {'defence_level': 0, 'ranged_defence_bonus': 0})
    return (monster_stats['defence_level'] + 9) * (monster_stats['ranged_defence_bonus'] + 64)

def final_calcs(weapon_input, gear_setup_input, ammo_input, monster_input, attack_style_input):
    print("\033[92m")

    if gear_setup_input.lower() == 'masori':
        gear_selected = ['masori_top', 'masori_bottom', 'masori_hat', 'zaryte_vambs', 'pegasian_boots', 'archers_ring', 'avas_attractor']
    elif gear_setup_input.lower() == 'void':
        gear_selected = ['void_top', 'void_bottom', 'void_hat', 'void_gloves', 'pegasian_boots', 'archers_ring', 'avas_attractor']
    else:
        print("Invalid gear setup.")
        return

    if ammo_input.lower() == 'none':
        gear_selected.remove('avas_attractor')

    player_attack_roll = calculate_attack_roll(ranged_level, weapon_input, ammo_input, gear_selected, prayer_bonus, potion_bonus, other_bonus, attack_style_input)
    opponent_defence_roll = calculate_defence_roll(monster_input)
    hit_chance = calculate_hit_chance(player_attack_roll, opponent_defence_roll)
    max_hit = calculate_max_ranged_hit(ranged_level, weapon_input, ammo_input, gear_selected, prayer_bonus, potion_bonus, other_bonus, attack_style_input)
    attack_speed = get_attack_speed(weapon_input, attack_style_input)
    damage_per_hit = max_hit * hit_chance
    attack_speed_seconds = attack_speed * 0.6
    extra_projectile_chance = 0.10
    dps = damage_per_hit / attack_speed_seconds
    dps += dps * extra_projectile_chance

    print(f"Attack Style: {attack_style_input}")
    print(f"Hit Chance: {hit_chance:.2%}")
    print(f"Max Hit: {max_hit}")
    print(f"Attack Speed (ticks): {attack_speed}")
    print(f"\033[93mRanged DPS: {dps:.2f}\033[0m")

print(f'\033[95mvalues:\033[96m \n weapon_input \n gear_setup_input \n ammo_input \n monster_input \n attack_style_input')
print(f'\033[95mexample:\033[96m \n zaryte_crossbow_buckler \n masori \n ruby_dragon_bolts_e \n warden \n rapid')

if __name__ == "__main__":
    if len(sys.argv) != 6:
        sys.exit(1)
    
    _, weapon_input, gear_setup_input, ammo_input, monster_input, attack_style_input = sys.argv
    final_calcs(weapon_input, gear_setup_input, ammo_input, monster_input, attack_style_input)
