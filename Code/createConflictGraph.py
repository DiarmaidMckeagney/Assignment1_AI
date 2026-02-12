#IMPORTANT NOTE: This File is written by AI. It is just used to analyse the input file small.txt to see if a perfect solution is possible to achieve.

import networkx as nx
import itertools
import matplotlib.pyplot as plt

def read_instance(filename):
    with open(filename, 'r') as f:
        lines = f.read().strip().splitlines()

    n_exams, n_slots, n_students = map(int, lines[0].split())
    matrix = [list(map(int, line.split())) for line in lines[1:]]

    return n_exams, n_slots, n_students, matrix


def build_conflict_graph(n_exams, matrix):
    G = nx.Graph()
    G.add_nodes_from(range(n_exams))

    for student in matrix:
        exams = [i for i, v in enumerate(student) if v == 1]
        for i, j in itertools.combinations(exams, 2):
            G.add_edge(i, j)

    return G


# ---- Exact chromatic number (backtracking) ----
def chromatic_number_exact(G):
    nodes = list(G.nodes())
    n = len(nodes)
    best = n
    colors = {}

    def valid(node, c):
        for neighbor in G.neighbors(node):
            if neighbor in colors and colors[neighbor] == c:
                return False
        return True

    def backtrack(i, used_colors):
        nonlocal best
        if i == n:
            best = min(best, used_colors)
            return

        if used_colors >= best:
            return

        node = nodes[i]

        for c in range(used_colors):
            if valid(node, c):
                colors[node] = c
                backtrack(i + 1, used_colors)
                del colors[node]

        colors[node] = used_colors
        backtrack(i + 1, used_colors + 1)
        del colors[node]

    backtrack(0, 0)
    return best


# ---- Greedy coloring (fast upper bound) ----
def greedy_coloring(G):
    coloring = nx.coloring.greedy_color(G, strategy="largest_first")
    return max(coloring.values()) + 1

def plot_colored_graph(G):
    plt.figure(figsize=(8, 6))

    pos = nx.spring_layout(G, seed=42)

    # Get greedy coloring
    coloring = nx.coloring.greedy_color(G, strategy="largest_first")

    # Extract colors in node order
    node_colors = [coloring[node] for node in G.nodes()]

    nx.draw_networkx_nodes(G, pos, node_size=500, node_color=node_colors, cmap=plt.cm.tab10)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, font_size=10)

    plt.title("Exam Conflict Graph (Greedy Coloring)")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    filename = "../InputFiles/small.txt"

    n_exams, n_slots, n_students, matrix = read_instance(filename)
    G = build_conflict_graph(n_exams, matrix)

    print("Nodes:", G.number_of_nodes())
    print("Edges:", G.number_of_edges())

    exact = chromatic_number_exact(G)
    greedy = greedy_coloring(G)
    plot_colored_graph(G)
    print("Exact chromatic number:", exact)
    print("Greedy coloring uses:", greedy, "colors")
