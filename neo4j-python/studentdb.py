from py2neo import Graph, Node, Relationship
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx


# Connect to the Neo4j database
graph = Graph("bolt://localhost:7687", auth=("neo4j", "2509"))

# Create a dataframe with student information
student_df = pd.DataFrame({
    "student_id": [1, 2, 3, 4, 5],
    "student_name": ["John", "Jane", "Jim", "Jessica", "Jake"],
    "student_age": [25, 27, 22, 21, 24]
})

# Loop through the rows in the dataframe and add each student as a node in the Neo4j database
for index, row in student_df.iterrows():
    student = Node("Student", student_id=row["student_id"], student_name=row["student_name"], student_age=row["student_age"])
    graph.create(student)
    if index > 0:
        graph.create(Relationship(student, "KNOWS", previous_student))
    previous_student = student
    course = Node("Course", course_name="Mathematics")
    graph.create(course)
    graph.create(Relationship(student, "STUDIES", course))

# Display Relationship 
query = """MATCH (s:Student)-[r]->(t:Student) RETURN s, r, t;"""
query2 =  """MATCH (c:Course) - [r]->(f:Course) RETURN c,r,f"""
results = graph.run(query)
results2 = graph.run(query2)

# Loop through the results and print the relationships
for result in results:
    start_node = result["s"]
    relationship = result["r"]
    end_node = result["t"]
    print("(%s) -[%s]-> (%s)" % (start_node, relationship, end_node))

print(results2)

for result in results2:
    start_node = result["c"]
    relationship = result["r"]
    end_node = result["f"]
    print("(%s) -[%s]-> (%s)" % (start_node, relationship, end_node))


# Create a NetworkX graph object
G = nx.DiGraph()

# Add nodes to the graph
for result in results:
    start_node = result["s"]
    end_node = result["t"]
    relationship = result["r"]
    G.add_node(start_node["name"], label=start_node["name"])
    G.add_node(end_node["name"], label=end_node["name"])
    G.add_edge(start_node["name"], end_node["name"], label=relationship["name"])

# Draw the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color="skyblue", edge_color="gray")

# Display the graph
plt.show()
