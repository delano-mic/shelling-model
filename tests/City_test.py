import sys
import logging
sys.path.append('..')
from city import City
from diverse import DiverseAgent
from conform import ConformingAgent
from Logger import Logger
Logger()

logger = logging.getLogger("shelling-model-logger") 

def test_setup():
    city = City(4, 4, 1)
    city.setUp()
    assert len(city.grid) == 4
    assert len(city.grid[0]) == 4

def test_get_neighbors():
    grid = [
        [None, DiverseAgent("X"), DiverseAgent("X"), ConformingAgent("0")],
        [DiverseAgent("X"), ConformingAgent("0"), ConformingAgent("0"), None],
        [ConformingAgent("0"), DiverseAgent("X"), ConformingAgent("0"), DiverseAgent("X")],
        [DiverseAgent("X"), None, DiverseAgent("X"), DiverseAgent("X")],
    ]
    city = City(4, 4, 1, grid)

    # Check from a minimum x & y position 
    neighbors = city.get_neighbors(0, 0)
    assert len(neighbors) == 3
    assert neighbors[0] == DiverseAgent("X")
    assert neighbors[1] == DiverseAgent("X")
    assert neighbors[2] == ConformingAgent("0")

    # Check from a maximum x & y position 
    neighbors = city.get_neighbors(3, 3)
    assert len(neighbors) == 3
    assert neighbors[0] == ConformingAgent("0")
    assert neighbors[1] == DiverseAgent("X")
    assert neighbors[2] == DiverseAgent("X")

    # Check from a minimum y position 
    neighbors = city.get_neighbors(1, 0)
    assert len(neighbors) == 5
    assert neighbors[0] == None
    assert neighbors[1] == DiverseAgent("X")
    assert neighbors[2] == DiverseAgent("X")
    assert neighbors[3] == ConformingAgent("0")
    assert neighbors[4] == ConformingAgent("0")

    # # Check from a minimum x position 
    neighbors = city.get_neighbors(0, 1)
    assert len(neighbors) == 5
    assert neighbors[0] == None
    assert neighbors[1] == DiverseAgent("X")
    assert neighbors[2] == ConformingAgent("0")
    assert neighbors[3] == ConformingAgent("0")
    assert neighbors[4] == DiverseAgent("X")

    # Check from a maximum x position 
    neighbors = city.get_neighbors(3, 0)
    assert len(neighbors) == 3
    assert neighbors[0] == DiverseAgent("X")
    assert neighbors[1] == ConformingAgent("0")
    assert neighbors[2] == None

    # Check from a maximum y position 
    neighbors = city.get_neighbors(0, 3)
    assert len(neighbors) == 3
    assert neighbors[0] == ConformingAgent("0")
    assert neighbors[1] == DiverseAgent("X")
    assert neighbors[2] == None

    # Check from a landlocked position 
    neighbors = city.get_neighbors(1, 1)
    for neighbor in neighbors:
        print("Neighbor", neighbor)
    assert len(neighbors) == 8
    assert neighbors[0] == None
    assert neighbors[1] == DiverseAgent("X")
    assert neighbors[2] == DiverseAgent("X")
    assert neighbors[3] == DiverseAgent("X")
    assert neighbors[4] == ConformingAgent("0")
    assert neighbors[5] == ConformingAgent("0")
    assert neighbors[6] == DiverseAgent("X")
    assert neighbors[7] == ConformingAgent("0")
    
def test_move_agent():
    grid = [
        [None, DiverseAgent("X")]
    ]
    city = City(2, 1, 1, grid)

    # Test that the agent is moved and nothing is left in it's place
    city.move_agent(0, 1)
    assert len(city.grid) == 1
    assert len(city.grid[0]) == 2
    assert city.grid[0][0] == DiverseAgent("X")
    assert city.grid[0][1] == None

    # Test that empty spaces can't be moved
    city.move_agent(0, 0)
    assert len(city.grid) == 1
    assert len(city.grid[0]) == 2
    assert city.grid[0][0] == None
    assert city.grid[0][1] == DiverseAgent("X")


def test_simulate():
    city = City(5, 5, 5000) # Running a 5x5 simulation for 10 rounds per the instructions
    city.setUp()
    city.simulate()

# test_simulate()
    