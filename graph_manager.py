import networkx as nx
import matplotlib.pyplot as plt
from flight_data import import_real_routes_to_graph

class GraphManager:
    def __init__(self):
        self.flight_graph = {}
        self.highlighted_nodes = []
        self.highlighted_edges = []

    #Demo graph nodes and edges
    def load_demo_graph(self):
        self.flight_graph = {
            'JFK': [('ORD', 150), ('ATL', 200), ('BOS', 120)],
            'ORD': [('DEN', 180), ('DFW', 160)],
            'ATL': [('MIA', 140), ('DFW', 150), ('CLT', 130)],
            'DFW': [('LAX', 170), ('SEA', 210)],
            'MIA': [('JFK', 300), ('CLT', 190)],
            'BOS': [('JFK', 120), ('MIA', 220)],
            'SEA': [('DEN', 200), ('LAX', 140)],
            'DEN': [('ATL', 190), ('SEA', 200)],
            'CLT': [('JFK', 160), ('DFW', 170)],
            'LAX': [('SEA', 150)]
        }

    def load_live_graph(self):
        airports = ['JFK', 'BOS', 'DCA', 'MIA', 'ORD', 'DTW', 'ATL', 'CLT', 'DFW', 'PHX', 'LAS']
        self.flight_graph.clear()
        for airport in airports:
            try:
                import_real_routes_to_graph(self.flight_graph, airport)
            except Exception as e:
                print(f"Failed to import flights for {airport}: {e}")

    def add_flight(self, from_city, to_city, price):
        if from_city in self.flight_graph:
            self.flight_graph[from_city].append((to_city, price))
        else:
            self.flight_graph[from_city] = [(to_city, price)]

        if to_city not in self.flight_graph:
            self.flight_graph[to_city] = []

    def remove_flight(self, from_city, to_city):
        if from_city in self.flight_graph:
            original = self.flight_graph[from_city]
            self.flight_graph[from_city] = [tup for tup in original if tup[0] != to_city]

    def draw_graph(self):
        G = nx.DiGraph()
        for from_city, connections in self.flight_graph.items():
            for to_city, price in connections:
                G.add_edge(from_city, to_city, weight=price)

        pos = nx.kamada_kawai_layout(G)

        fig, ax = plt.subplots(figsize=(6, 5))
        ax.set_facecolor('#1e1e1e')
        fig.patch.set_facecolor('#1e1e1e')

        node_colors = []
        for node in G.nodes():
            if node in self.highlighted_nodes:
                node_colors.append('limegreen')
            else:
                node_colors.append('lightblue')

        edge_colors = []
        for u, v in G.edges():
            if (u, v) in self.highlighted_edges:
                edge_colors.append('limegreen')
            else:
                edge_colors.append('black')

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color=node_colors,
            edge_color=edge_colors,
            node_size=2500,
            font_size=10,
            arrows=True,
            edgecolors='black',
            linewidths=1,
            ax=ax
        )

        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, ax=ax)

        ax.set_title("Current Flight Graph", fontsize=16, color='white')
        ax.axis('off')

        return fig