import sys
sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

def assult(state):
    #find strongest planet
    readyPlanets = max([planet for planet in state.my_planets() if planet.num_ships >= 100], key=lambda p: p.num_ships)

    #if we dont have a planet with enough forces we abort
    if not readyPlanets:
        return False

    # find a good weak target planet to attack
    weakPlanets = []
    for planet in state.not_my_planets():
        weakPlanets.append((planet, state.distance(readyPlanets.ID, planet.ID) + planet.num_ships))

    #fin the weakest 3 planets to attack
    weakPlanets = sorted(weakPlanets, key=lambda x: x[1])
    weakPlanets = weakPlanets[:3]

    #ATTACK
    for target in weakPlanets:
        issue_order(state, readyPlanets.ID, target[0].ID, (target[0].num_ships + 1) * target[0].growth_rate)



# like spreading to weakest planet, we do the same but target 4 of them at the same time
def expandToNeutrals (state):
    enemyTargets = []
    #planets that are being targeted by the enemy
    for fleet in state.enemy_fleets():
        enemyTargets.append(fleet.destination_planet)

    easyPickings = []
    # find neutral planets that are not the target of an enemy fleet to expand to
    for planet in state.neutral_planets():
        if planet.ID not in enemyTargets:
            #This needed to be a tupple or else game would crash
            easyPickings.append( (planet, state.distance(state.my_planets()[0].ID, planet.ID) + planet.num_ships) )  
    
    #sort to find the closest and weakest neutral planets          
    easyPickings = sorted(easyPickings, key=lambda x: x[1])
    neutralTargets = easyPickings[:4]

    #ATTACK!!!
    for target in neutralTargets:
        issue_order(state, state.my_planets()[0].ID, target[0].ID, (target[0].num_ships + 1)*target[0].growth_rate)

    return True