

def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())


#check if we have any planets that have 100 or more ships to fight with. 100 is the magic number it seems
def checkForces(state):
    readyPlanets = []
    for planet in state.my_planets():
        if planet.num_ships >= 100:
            readyPlanets.append(planet)

    return len(readyPlanets) > 0

# Check if our little empire has less than 4 planets
def homeBase(state):
    home = state.my_planets()
    return len(home) < 4

#check if we actually have any ships at all to fightt
def readyShips(state):
    battleFleets = []
    for ship in state.my_fleets():
        battleFleets.append(ship)

    if battleFleets:
        return False
    else:
        return True
