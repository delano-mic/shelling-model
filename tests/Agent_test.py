import sys
sys.path.append('..')
from Agent_og import Agent

def test_compare():
    agent1 = Agent("A")
    agent2 = Agent("A")
    agent3 = Agent("B")

    assert agent1.compare(agent2) == True
    assert agent1.compare(agent3) == False

def test_is_satisfied():
    evaluation_agent = Agent("A", 0.5)
    adjacent_agent_1 = Agent("A")
    adjacent_agent_2 = Agent("B")   

    assert evaluation_agent.is_satisfied([adjacent_agent_1]) == True
    assert evaluation_agent.is_satisfied([adjacent_agent_1, adjacent_agent_2]) == True
    assert evaluation_agent.is_satisfied([adjacent_agent_2]) == False
    assert evaluation_agent.is_satisfied([adjacent_agent_1, adjacent_agent_2, None]) == True
    assert evaluation_agent.is_satisfied([adjacent_agent_2, None]) == False
    