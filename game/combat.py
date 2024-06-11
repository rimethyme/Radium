def combat(player, monster, previous_location):
    player_health = player.health
    monster_health = monster.health

    while player_health > 0 and monster_health > 0:
        print("Player Health:", player_health)
        print("Monster Health:", monster_health)
        print("Options:")
        print("1. Attack")
        print("2. Use Health Potion")
        print("3. Flee")
        choice = input("Choose your action: ").strip().lower()

        if choice in ["1", "attack"]:
            print("Choose your weapon:")
            for i, item in enumerate(player.inventory):
                if item.damage > 0:
                    print(f"{i+1}. {item.name} - Damage: {item.damage}")
            weapon_choice = input("Choose a weapon: ").strip().lower()
            selected_weapon = player.has_item(weapon_choice)
            if selected_weapon and selected_weapon.damage > 0:
                player_damage = selected_weapon.damage
                monster_health -= player_damage
                print("You attacked the", monster.name + "!")
                if monster_health <= 0:
                    return {"result": "win"}
            else:
                print("Invalid weapon choice.")

        elif choice in ["2", "use health potion"]:
            if player.health < player.max_health:
                use_health_potion(player)
            else:
                print("You already have full health!")

        elif choice in ["3", "flee"]:
            print("You fled from the", monster.name + "!")
            return {"result": "flee", "previous_location": previous_location}

        player_health -= monster.damage
        if player_health <= 0:
            return {"result": "lose"}

    return {"result": "draw"}

def use_health_potion(player):
    health_potion = player.has_item("health potion")
    if health_potion:
        if player.health < player.max_health:
            player.health += health_potion.heal
            if player.health > player.max_health:
                player.health = player.max_health
            player.inventory.remove(health_potion)
            print(f"You used a Health Potion and restored {health_potion.heal} health!")
        else:
            print("You already have full health!")
    else:
        print("You don't have any Health Potions!")
