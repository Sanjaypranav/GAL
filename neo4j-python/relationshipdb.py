import matplotlib.pyplot as plt
import networkx as nx
from py2neo import Graph

# Connect to the Neo4j database
graph = Graph("bolt://localhost:7687", auth=("neo4j", "2509"))

# Create the Student and Course nodes in the database
graph.run("CREATE (s1:Student {name: 'Student 1'})")
graph.run("CREATE (s2:Student {name: 'Student 2'})")
graph.run("CREATE (c1:Course {name: 'Math'})")
graph.run("CREATE (c2:Course {name: 'Science'})")

# Create relationships between the Student and Course nodes
graph.run("MATCH (s1:Student {name: 'Student 1'}), (c1:Course {name: 'Math'}) CREATE (s1)-[r:TAKES]->(c1)")
graph.run("MATCH (s2:Student {name: 'Student 2'}), (c2:Course {name: 'Science'}) CREATE (s2)-[r:TAKES]->(c2)")

# Run a Cypher query to retrieve the nodes and relationships you want to visualize
query = "MATCH (s:Student)-[r]->(c:Course) RETURN s, r, c"
results = graph.run(query)

# Create a NetworkX graph object
G = nx.DiGraph()

# Add nodes to the graph
for result in results:
    start_node = result["s"]
    end_node = result["c"]
    relationship = result["r"]
    
    if start_node and end_node and start_node["name"] and end_node["name"]:
        G.add_node(start_node["name"], label=start_node["name"], shape="circle")
        G.add_node(end_node["name"], label=end_node["name"], shape="rectangle")
        G.add_edge(start_node["name"], end_node["name"], label=relationship.type("Friends"))

# Draw the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color="skyblue", edge_color="gray")

# Display the graph
plt.show()
