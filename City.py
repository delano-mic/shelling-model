import random
import logging
# This is imported because this python version doesn't support OR operators for function parameter typing.
from typing import Union, List
from Agent import Agent
from Logger import Logger

Logger()

class City():
    # The contructor allows for a grid to be passed in for testing purposes.
    def __init__(self, width: int, height: int, rounds: int, grid_override: List[List[Union['Agent', None]]] = []):
        self.width = width
        self.height = height
        self.rounds = rounds
        self.grid = grid_override
        self.logger = logging.getLogger("shelling-model-logger") 

    def __str__(self):
        grid_string = ""
        
        for _x, _y, _agent in self._grid_iterator():
            if(_agent is None):
                grid_string += "|_"
            else:
                grid_string += "|" +str(_agent)

            if(_y == self.width - 1):  # End of row when we reach the last column
                grid_string += "|"
                grid_string += "\n"

        return grid_string

    def _grid_iterator(self):
        for rowIndex in range(self.height): 
            for columnIndex in range(self.width): 
                yield rowIndex, columnIndex, self.grid[rowIndex][columnIndex]

    def _empty_locations(self):
        for _x, _y, _agent in self._grid_iterator():
            if(_agent is None):
                yield _x, _y

    def setUp(self):
        choices = ["X", "O", "_"]
        weights = [0.333, 0.333, 0.334]
        population = self.width * self.height
        def selectAgent():
            """
            Weighted random selection of X, O, or None
            """
            agentIdentification = random.choices(choices, weights=weights, k=population)[0]

            if agentIdentification == "_":
                return None
            
            return Agent(agentIdentification)

        if(len(self.grid) > 0):
            return ## Do not recreate the list if it's already set up. This is to support testing by allowing a grid to be passed into the constructor.

        for rowIndex in range(self.height): 
            self.grid.append([]) 
            for columnIndex in range(self.width): 
                agent = selectAgent()
                if agent is not None:
                    agent.set_location(rowIndex, columnIndex)  # Set agent's grid location
                self.grid[rowIndex].append(agent)  # Add agent to the current row

        self.logger.info(f"Grid created with {self.height} rows and {self.width} columns and a population of {population}")
        self.logger.info(f"Grid groups: {choices}")
        self.logger.info(f"Grid randomization weights: {weights}")

    def get_neighbors(self, x: int, y: int) -> List[Union['Agent', None]]:
        min_y = max(0, y-1)
        max_y = min(self.height-1, y+1)
        min_x= max(0, x-1)
        max_x = min(self.width-1, x+1)
        neighbors = []
        for _y in range(min_y, max_y + 1):  
            for _x in range(min_x, max_x + 1):  
                
                if(_x == x and _y == y):
                    continue
                neighbors.append(self.grid[_y][_x])
                self.logger.info(f"({x}, {y}) has a neighbor at ({_x}, {_y}): {self.grid[_y][_x]}")

        return neighbors

    def move_agent(self, x: int, y: int):
        if(self.grid[x][y] is None):
            return

        agent = self.grid[x][y];
        empty_locations = list(self._empty_locations())
        new_location_target = random.choice(empty_locations)
        
        # Update agent's location
        agent.set_location(new_location_target[0], new_location_target[1])
        
        # Move agent in grid
        self.grid[new_location_target[0]][new_location_target[1]] = agent
        self.grid[x][y] = None

        self.logger.info(f"Agent moved from ({x}, {y}) to ({new_location_target[0]}, {new_location_target[1]})")
        
    # This was added to support the expansion of the assignment which 
    # requires the calculation of the satisfaction percentage of an entire neighborhood.
    def neighborhood_satisfaction(self, centroid_x: int, centroid_y: int, simulation_candidate_x: int = -1, simulation_candidate_y: int = -1):
        neighbors_of_evaluation_location = self.get_neighbors(centroid_x, centroid_y)

        # Remove empty neighbors
        non_none_neighbors = [neighbor for neighbor in neighbors_of_evaluation_location if neighbor is not None]
        
        # Get thresholds and satisfaction percentages for current neighborhood
        current_neighborhood_satisfaction_target = [neighbor.threshold for neighbor in non_none_neighbors]
        current_neighborhood_satisfaction_actual = [neighbor.satisfaction_perc(self.get_neighbors(neighbor.x, neighbor.y)) for neighbor in non_none_neighbors]
        
        if(simulation_candidate_x == -1 and simulation_candidate_y == -1):
            if len(current_neighborhood_satisfaction_actual) == 0:
                return 0
            return sum(current_neighborhood_satisfaction_target) / sum(current_neighborhood_satisfaction_actual)

        # Simulate the neighbor in the new neighborhood
        neighbors_with_candidate = neighbors_of_evaluation_location.copy()
        candidate_agent = self.grid[simulation_candidate_x][simulation_candidate_y]
        if candidate_agent is not None:
            neighbors_with_candidate.append(candidate_agent)

        # Remove empty neighbors for potential scenario
        non_none_neighbors_potential = [neighbor for neighbor in neighbors_with_candidate if neighbor is not None]
        potential_new_location_satisfaction_target = [neighbor.threshold for neighbor in non_none_neighbors_potential]
        potential_new_location_satisfaction_actual = [neighbor.satisfaction_perc(self.get_neighbors(neighbor.x, neighbor.y)) for neighbor in non_none_neighbors_potential]
        
        # Calculate satisfaction ratios
        current_satisfaction = sum(current_neighborhood_satisfaction_target) / sum(current_neighborhood_satisfaction_actual) if len(current_neighborhood_satisfaction_actual) > 0 else 0
        potential_satisfaction = sum(potential_new_location_satisfaction_target) / sum(potential_new_location_satisfaction_actual) if len(potential_new_location_satisfaction_actual) > 0 else 0
        
        return potential_satisfaction > current_satisfaction

    def simulate(self):
        for simulation_round in range(self.rounds):
            self.logger.info(f"Simulation round {simulation_round}")
            for _x, _y, _agent in self._grid_iterator():
                if(_agent is None):
                    continue

                for empty_location in self._empty_locations():
                    current_neighborhood_satisfaction = self.neighborhood_satisfaction(_x, _y)
                    potential_new_location_satisfaction = self.neighborhood_satisfaction(empty_location[0], empty_location[1], _x, _y)
                    
                    if(potential_new_location_satisfaction > current_neighborhood_satisfaction):
                        self.move_agent(_x, _y)
                        self.logger.info(f"Grid mutated. New State:")
                        print(self)