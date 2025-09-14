import sys
sys.path.append('..')
from agent import ParentAgent

def test_compare():
    agent1 = ParentAgent("A")
    agent2 = ParentAgent("A")
    agent3 = ParentAgent("B")

    assert agent1.compare(agent2) == True
    assert agent1.compare(agent3) == False

def test_is_satisfied():
    evaluation_agent = ParentAgent("A", 0.5)
    adjacent_agent_1 = ParentAgent("A")
    adjacent_agent_2 = ParentAgent("B")   

    assert evaluation_agent.is_satisfied([adjacent_agent_1]) == True
    assert evaluation_agent.is_satisfied([adjacent_agent_1, adjacent_agent_2]) == True
    assert evaluation_agent.is_satisfied([adjacent_agent_2]) == False
    assert evaluation_agent.is_satisfied([adjacent_agent_1, adjacent_agent_2, None]) == True
    assert evaluation_agent.is_satisfied([adjacent_agent_2, None]) == False
    