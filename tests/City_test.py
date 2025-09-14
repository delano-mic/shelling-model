import sys
import logging
sys.path.append('..')
from City_og import City
from Agent_og import Agent
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
        [None, Agent("X"), Agent("X"), Agent("0")],
        [Agent("X"), Agent("0"), Agent("0"), None],
        [Agent("0"), Agent("X"), Agent("0"), Agent("X")],
        [Agent("X"), None, Agent("X"), Agent("X")],
    ]
    city = City(4, 4, 1, grid)

    # Check from a minimum x & y position 
    neighbors = city.get_neighbors(0, 0)
    assert len(neighbors) == 3
    assert neighbors[0] == Agent("X")
    assert neighbors[1] == Agent("X")
    assert neighbors[2] == Agent("0")

    # Check from a maximum x & y position 
    neighbors = city.get_neighbors(3, 3)
    assert len(neighbors) == 3
    assert neighbors[0] == Agent("0")
    assert neighbors[1] == Agent("X")
    assert neighbors[2] == Agent("X")

    # Check from a minimum y position 
    neighbors = city.get_neighbors(1, 0)
    assert len(neighbors) == 5
    assert neighbors[0] == None
    assert neighbors[1] == Agent("X")
    assert neighbors[2] == Agent("X")
    assert neighbors[3] == Agent("0")
    assert neighbors[4] == Agent("0")

    # # Check from a minimum x position 
    neighbors = city.get_neighbors(0, 1)
    assert len(neighbors) == 5
    assert neighbors[0] == None
    assert neighbors[1] == Agent("X")
    assert neighbors[2] == Agent("0")
    assert neighbors[3] == Agent("0")
    assert neighbors[4] == Agent("X")

    # Check from a maximum x position 
    neighbors = city.get_neighbors(3, 0)
    assert len(neighbors) == 3
    assert neighbors[0] == Agent("X")
    assert neighbors[1] == Agent("0")
    assert neighbors[2] == None

    # Check from a maximum y position 
    neighbors = city.get_neighbors(0, 3)
    assert len(neighbors) == 3
    assert neighbors[0] == Agent("0")
    assert neighbors[1] == Agent("X")
    assert neighbors[2] == None

    # Check from a landlocked position 
    neighbors = city.get_neighbors(1, 1)
    for neighbor in neighbors:
        print("Neighbor", neighbor)
    assert len(neighbors) == 8
    assert neighbors[0] == None
    assert neighbors[1] == Agent("X")
    assert neighbors[2] == Agent("X")
    assert neighbors[3] == Agent("X")
    assert neighbors[4] == Agent("0")
    assert neighbors[5] == Agent("0")
    assert neighbors[6] == Agent("X")
    assert neighbors[7] == Agent("0")
    
def test_move_agent():
    grid = [
        [None, Agent("X")]
    ]
    city = City(2, 1, 1, grid)

    # Test that the agent is moved and nothing is left in it's place
    city.move_agent(0, 1)
    assert len(city.grid) == 1
    assert len(city.grid[0]) == 2
    assert city.grid[0][0] == Agent("X")
    assert city.grid[0][1] == None

    # Test that empty spaces can't be moved
    city.move_agent(0, 0)
    assert len(city.grid) == 1
    assert len(city.grid[0]) == 2
    assert city.grid[0][0] == None
    assert city.grid[0][1] == Agent("X")

def test_simulate():
    city = City(4, 4, 2)
    city.simulate()

    