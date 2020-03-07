# Adapted from https://github.com/aimacode/aima-python/blob/master/search.py
from .node import Node
from collections import deque
from timeit import default_timer as timer
from datetime import timedelta
from .utils import (PriorityQueue, memoize)
import sys

def depth_first_graph_search(problem):
    # Return variables
    goal = None
    explored_ordered = []
    # Problem Solving
    start = timer()
    frontier = [(Node(problem.initial))]  # Stack
    explored = set()
    while frontier:
        node = frontier.pop()
        explored_ordered.insert(len(explored_ordered), node.state)
        if problem.goal_test(node.state):
            goal = node
        explored.add(node.state)
        frontier.extend(child for child in node.expand(problem)
                        if child.state not in explored and
                        child not in frontier)
    # 
    end = timer()
    return [goal, explored_ordered, timedelta(seconds=end-start).total_seconds() * 1000]


def breadth_first_graph_search(problem):
    # Return variables
    goal = None
    explored_ordered = []
    # Problem Solving
    start = timer()
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node
    frontier = deque([node])
    explored = set()
    should_end = False
    while frontier and not should_end:
        node = frontier.popleft()
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                explored_ordered.insert(len(explored_ordered), child)
                if problem.goal_test(child.state):
                    goal = child
                    should_end = True
                    break
                frontier.append(child)
    # 
    end = timer()
    return [goal, explored_ordered, timedelta(seconds=end-start).total_seconds() * 1000]

def depth_limited_search(problem, limit=50):
    # Return variables
    explored_ordered = []
    # Problem Solving
    def recursive_dls(node, problem, limit):
        explored_ordered.insert(len(explored_ordered), node)
        if problem.goal_test(node.state):
            return node
        elif limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand(problem):
                result = recursive_dls(child, problem, limit - 1)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return 'cutoff' if cutoff_occurred else None

    # Body of depth_limited_search:
    return [recursive_dls(Node(problem.initial), problem, limit), explored_ordered]


def iterative_deepening_search(problem):
    # Return variables
    goal = None
    explored_ordered = []
    # Problem Solving
    start = timer()
    for depth in range(13):
        [result, explored_ordered_ins] = depth_limited_search(problem, depth)
        explored_ordered.extend(explored_ordered_ins)
        if result != 'cutoff':
            goal = result
            break
    
    end = timer()
    return [goal, explored_ordered, timedelta(seconds=end-start).total_seconds() * 1000]

def best_first_graph_search(problem, f):
    # Return variables
    goal = None
    explored_ordered = []
    # Problem Solving
    start = timer()
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        explored_ordered.insert(len(explored_ordered), node)
        if problem.goal_test(node.state):
            goal = node
            break
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    end = timer()
    return [goal, explored_ordered, timedelta(seconds=end-start).total_seconds() * 1000]


def uniform_cost_search(problem):
    return best_first_graph_search(problem, lambda node: node.path_cost)

infinity = float('inf')

def bidirectional_search(problem):
    # Return variables
    goal = None
    explored_ordered = []
    start = timer()
    #
    e = 1 #problem.find_min_edge() -> All edge costs are 1.
    gF, gB = {problem.initial : 0}, {problem.goal : 0}
    final = gB
    openF, openB = [problem.initial], [problem.goal]
    closedF, closedB = [], []
    U = infinity


    def extend(U, open_dir, open_other, g_dir, g_other, closed_dir):
        """Extend search in given direction"""
        n = find_key(C, open_dir, g_dir)

        open_dir.remove(n)
        closed_dir.append(n)

        for c in node.expand(problem):
            if c in open_dir or c in closed_dir:
                if g_dir[c] <= problem.path_cost(g_dir[n], n, None, c):
                    continue

                open_dir.remove(c)

            g_dir[c] = problem.path_cost(g_dir[n], n, None, c)
            open_dir.append(c)

            if c in open_other:
                U = min(U, g_dir[c] + g_other[c])

        return U, open_dir, closed_dir, g_dir


    def find_min(open_dir, g):
        """Finds minimum priority, g and f values in open_dir"""
        m, m_f = infinity, infinity
        for n in open_dir:
            f = g[n] + problem.h(n)
            pr = max(f, 2*g[n])
            m = min(m, pr)
            m_f = min(m_f, f)

        return m, m_f, min(g.values())


    def find_key(pr_min, open_dir, g):
        """Finds key in open_dir with value equal to pr_min
        and minimum g value."""
        m = infinity
        state = -1
        for n in open_dir:
            pr = max(g[n] + problem.h(n), 2*g[n])
            if pr == pr_min:
                if g[n] < m:
                    m = g[n]
                    state = n

        return state


    while openF and openB:
        pr_min_f, f_min_f, g_min_f = find_min(openF, gF)
        pr_min_b, f_min_b, g_min_b = find_min(openB, gB)
        C = min(pr_min_f, pr_min_b)

        if U <= max(C, f_min_f, f_min_b, g_min_f + g_min_b + e):
            goal = U
            break

        if C == pr_min_f:
            # Extend forward
            U, openF, closedF, gF = extend(U, openF, openB, gF, gB, closedF)
        else:
            # Extend backward
            U, openB, closedB, gB = extend(U, openB, openF, gB, gF, closedB)

    end = timer()
    return [openB[0], explored_ordered, timedelta(seconds=end-start).microseconds / 1000]

def astar_search(problem, h):
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))
