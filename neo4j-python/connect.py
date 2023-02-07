from neo4j import GraphDatabase

class StudentDB:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def add_student(self, message):
        with self.driver.session() as session:
            greeting = session.execute_write(self.add_student_to_db, message)
            print(greeting)

    @staticmethod
    def add_student_to_db(tx, message):
        result = tx.run("""// create a database 
        CREATE (a:Student {name: $message})
        WITH a
        match (n) return n;
        """, message=message)
        return result.single()[0]

# Create a student database table using neo4j 



if __name__ == "__main__":
    greeter = StudentDB("bolt://localhost:7687", "neo4j", "2509")
    # Print Database name
    while True:
        print("Enter the name of the student")
        name = input()
        greeter.add_student(name)
        print("Do you want to add another student? (y/n)")
        if input() == "n":
            break
    greeter.close()