from Models.Visualization.Graph.graph import Graph
from Models.Visualization.Graph.node import Node
from Models.Visualization.Graph.edge import Edge
from Enums.edge_status_enum import EdgeStatusEnum

class InferenceGraphCreator:

    def __init__(self, inferences):
        self.inferences = inferences
        self.graph = Graph("Inference Graph")

        self.__nodes_cache = {}

    
    def create_graph_from_inference(self):
        self.create_nodes()
        self.create_edges()
        return self.graph
    
    def create_nodes(self):
        for inference in self.inferences:
            
            origin_module = inference.origin_module
            inferred_module = inference.inferred_module_name

            if not origin_module in self.__nodes_cache.keys():
                if "builtins" in origin_module:
                    continue
                new_node = self.graph.add_node(origin_module)
                self.__nodes_cache[origin_module] = new_node
            
            if not inferred_module in self.__nodes_cache.keys():
                if "builtins" in inferred_module:
                    continue
                new_node = self.graph.add_node(inferred_module)
                self.__nodes_cache[inferred_module] = new_node
    
    def create_edges(self):
        for inference in self.inferences:

            if "builtins" in inference.origin_module or "builtins" in inference.inferred_module_name:
                continue

            origin_node = self.__nodes_cache[inference.origin_module] 
            final_node = self.__nodes_cache[inference.inferred_module_name]

            if origin_node.name == final_node.name:
                continue

            new_edge = Edge(origin_node, final_node, EdgeStatusEnum.ALLOWED.value)
            self.graph.add_edge(new_edge)