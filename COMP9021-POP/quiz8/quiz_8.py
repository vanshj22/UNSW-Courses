# Written by *** for COMP9021

# Defines a class Building that defines a few special methods,
# as well as the two methods:
# - go_to_floor_from_entry()
# - leave_floor_from_entry()
# and an atribute, number_created, to keep track of
# the number of Building objects that have been created.
#
# Also defines a function compare_occupancies() meant to take
# as arguments two Building objects.
#
# Building objects are created with statements of the form
# Building(height, entries) where height is a positive integer
# (possibly equal to 0) and entries is a nonempty string that
# denotes all access doors to the building, with at least
# one space within the string to separate entries.
# You can assume that height and entries are as expected.
#
# If building denotes a Building object, then
# building.go_to_floor_from_entry(floor, entry, nb_of_people)
# takes as argument an integer, a string, and an integer.
# An error of type BuildingError is raised,
# all with the same message, if:
# - floor is not between 0 and the building's height, or
# - entry is not one of the building's entries, or
# - nb_of_people is not strictly positive.
# If the lift at that entry has to go down,
# then by how many floors it has to go down is printed out.
#
# If building denotes a Building object, then
# building.leave_floor_from_entry(floor, entry, nb_of_people)
# takes as argument an integer, a string, and an integer.
# An error of type BuildingError is raised if:
# - floor is not between 0 and the building's height, or
# - entry is not one of the building's entries, or
# - nb_of_people is not strictly positive, or
# - there are not at least nb_of_people on that floor.
# The same error message is used for the first 3 issues,
# and another error message is used for the last issue.
# If the lift at that entry has to go up or down, then
# by how many floors it has to go up or down is printed out.
#
# For the number of floors to go up or down, use
# "1 floor..." or "n floors..." for n > 1.

class BuildingError(Exception):
    pass

class Building:
    number_created = 0
    
    def __init__(self, height, entries):
        self.height = height
        self.entries = entries.split()
        self.lift_positions = {entry: 0 for entry in self.entries}
        self.occupants = {}
        
        Building.number_created += 1
    
    def __str__(self):
        return f"Building with {self.height + 1} floors accessible from entries: {', '.join(self.entries)}"

    def __repr__(self):
        return f"Building({self.height}, '{' '.join(self.entries)}')"

    def go_to_floor_from_entry(self, floor, entry, nb_of_people):
        if not (0 <= floor <= self.height) or entry not in self.entries or nb_of_people <= 0:
            raise BuildingError("That makes no sense!")

        current_position = self.lift_positions[entry]
        floors_to_move = abs(current_position - 0)
        if floors_to_move > 0:
            direction = "down"
            floors_text = "1 floor" if floors_to_move == 1 else f"{floors_to_move} floors"
            print(f"Wait, lift has to go {direction} {floors_text}...")
        key = (floor, entry)
        if key in self.occupants:
            self.occupants[key] += nb_of_people
        else:
            self.occupants[key] = nb_of_people

        self.lift_positions[entry] = floor

    
    def leave_floor_from_entry(self, floor, entry, nb_of_people):
        if not (0 <= floor <= self.height) or entry not in self.entries or nb_of_people <= 0:
            raise BuildingError("That makes no sense!")

        key = (floor, entry)
        if key not in self.occupants or self.occupants[key] < nb_of_people:
            raise BuildingError("There aren't that many people on that floor!")
        current_position = self.lift_positions[entry]
        floors_to_move = abs(current_position - floor)
        if floors_to_move > 0:
            direction = "down" if current_position > floor else "up"
            floors_text = "1 floor" if floors_to_move == 1 else f"{floors_to_move} floors"
            print(f"Wait, lift has to go {direction} {floors_text}...")
        
        self.occupants[key] -= nb_of_people
        if self.occupants[key] == 0:
            del self.occupants[key]
        
        self.lift_positions[entry] = 0
    

def compare_occupancies(building_1, building_2):
    occupants_1 = sum(building_1.occupants.values())
    occupants_2 = sum(building_2.occupants.values())
    
    if occupants_1 > occupants_2:
        print("There are more occupants in the first building.")
    elif occupants_1 < occupants_2:
        print("There are more occupants in the second building.")
    else:
        print("There is the same number of occupants in both buildings.")



the_horizons = Building(10, 'A B C D')
the_horizons
print(the_horizons)
Building.number_created
the_spike = Building(37, '1')
the_spike
print(the_spike)
Building.number_created
the_seaside = Building(6, 'A B Z')
the_seaside
print(the_seaside)
Building.number_created
# the_horizons.go_to_floor_from_entry(-1, 'A', 4)
# the_horizons.go_to_floor_from_entry(11, 'A', 4)
# the_horizons.go_to_floor_from_entry(0, 'Z', 4)
# the_horizons.go_to_floor_from_entry(0, 'B', 0)
the_horizons.go_to_floor_from_entry(0, 'B', 4)
compare_occupancies(the_horizons, the_spike)
the_spike.go_to_floor_from_entry(17, '1', 4)
compare_occupancies(the_horizons, the_spike)
# the_spike.leave_floor_from_entry(17, '1', 0)
# the_spike.leave_floor_from_entry(17, '1', 5)
the_spike.leave_floor_from_entry(17, '1', 3)
# the_horizons.leave_floor_from_entry(0, 'A', 1)
the_horizons.leave_floor_from_entry(0, 'B', 1)
the_horizons.leave_floor_from_entry(0, 'B', 1)
the_horizons.leave_floor_from_entry(0, 'B', 1)
compare_occupancies(the_horizons, the_spike)
the_horizons.leave_floor_from_entry(0, 'B', 1)
compare_occupancies(the_horizons, the_spike)
the_seaside.go_to_floor_from_entry(3, 'B', 1)
the_seaside.go_to_floor_from_entry(3, 'B', 1)
the_seaside.go_to_floor_from_entry(3, 'B', 1)
the_seaside.go_to_floor_from_entry(3, 'B', 1)
the_seaside.leave_floor_from_entry(3, 'B', 2)
the_seaside.leave_floor_from_entry(3, 'B', 2)
the_seaside.go_to_floor_from_entry(4, 'A', 10)
the_seaside.go_to_floor_from_entry(5, 'A', 10)
the_seaside.go_to_floor_from_entry(2, 'A', 10)
the_seaside.leave_floor_from_entry(4, 'A', 2)
the_seaside.go_to_floor_from_entry(1, 'A', 10)
the_seaside.leave_floor_from_entry(5, 'A', 2)
the_seaside.go_to_floor_from_entry(5, 'A', 10)
the_seaside.leave_floor_from_entry(3, 'B', 2)
the_seaside.leave_floor_from_entry(2, 'A', 2)
