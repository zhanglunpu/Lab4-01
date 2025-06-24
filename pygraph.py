from typing import Tuple, Union, Iterable, Set, Dict

Node = Union[str, int]
Edge = Tuple[Node, Node]


class Graph(object):
    """Graph data structure, undirected by default."""

    def __init__(self, edges: Iterable[Edge] = [], directed: bool = False):
        self.directed = directed
        self._nodes: Set[Node] = set()
        self._adj: Dict[Node, Set[Node]] = dict()
        for edge in edges:
            self.add_edge(edge)

    def has_node(self, node: Node):
        """Whether a node is in graph"""
        return node in self._nodes

    def has_edge(self, edge: Edge):
        """Whether an edge is in graph"""
        u, v = edge
        if u not in self._adj:
            return False
        if self.directed:
            return v in self._adj[u]
        else:
            return v in self._adj[u] or (u in self._adj.get(v, set()))

    def add_node(self, node: Node):
        """Add a node"""
        if node not in self._nodes:
            self._nodes.add(node)
            self._adj[node] = set()

    def add_edge(self, edge: Edge):
        """Add an edge (node1, node2). For directed graph, node1 -> node2"""
        u, v = edge
        self.add_node(u)
        self.add_node(v)
        self._adj[u].add(v)
        if not self.directed:
            self._adj[v].add(u)

    def remove_node(self, node: Node):
        """Remove all references to node"""
        if node not in self._nodes:
            raise ValueError(f"Node {node} not in graph")
        self._nodes.remove(node)
        self._adj.pop(node)
        for n in self._adj:
            if node in self._adj[n]:
                self._adj[n].remove(node)

    def remove_edge(self, edge: Edge):
        """Remove an edge from graph"""
        u, v = edge
        if u not in self._adj or v not in self._adj:
            raise ValueError(f"Edge {edge} not in graph")
        if self.directed:
            if v not in self._adj[u]:
                raise ValueError(f"Edge {edge} not in graph")
            self._adj[u].remove(v)
        else:
            if v not in self._adj[u] and u not in self._adj[v]:
                raise ValueError(f"Edge {edge} not in graph")
            if v in self._adj[u]:
                self._adj[u].remove(v)
            if u in self._adj[v]:
                self._adj[v].remove(u)

    def indegree(self, node: Node) -> int:
        """Compute indegree for a node"""
        if node not in self._nodes:
            raise ValueError(f"Node {node} not in graph")
        if self.directed:
            return sum(1 for n in self._nodes if node in self._adj[n])
        else:
            return len(self._adj[node])

    def outdegree(self, node: Node) -> int:
        """Compute outdegree for a node"""
        if node not in self._nodes:
            raise ValueError(f"Node {node} not in graph")
        return len(self._adj[node])

    def __str__(self):
        return f"Graph(nodes={list(self._nodes)}, edges={self.edges()}, directed={self.directed})"

    def __repr__(self):
        return self.__str__()

    def edges(self):
        result = set()
        for u in self._adj:
            for v in self._adj[u]:
                if self.directed or (v, u) not in result:
                    result.add((u, v))
        return list(result)
