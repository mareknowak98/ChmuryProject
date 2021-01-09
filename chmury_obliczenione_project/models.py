from neo4jrestclient.client import GraphDatabase

graph = GraphDatabase("https://db-vhct3wzga2erpkbqxsqi.graphenedb.com:24780", username="neo4j",
                      password="newprojectpass")


def execute(query):
    return graph.query(query)


class Location:
    def __init__(self, city, state):
        self.city = city
        self.state = state

    def find(self):
        query = "MATCH (n:Location {city:'" + self.city + "', state:'" + self.state + "'}) RETURN n"
        result = execute(query)
        return (result)

    def add_dist(self, city1, dist):
        query = "MATCH (a:Location {city: '" + self.city + "', state: '" + self.state + "'}),(b:Location {city: '" + city1.city + "', state: '" + city1.state + "'}) MERGE(a)-[r:DIST {dist: '" + dist +"'}]->(b) RETURN a,b"
        result = execute(query)
        return result

    def get_dist(self):
        query = "OPTIONAL MATCH a= (Location {city: '" + self.city + "', state: '" + self.state + "'}) -[:DIST]-(city) RETURN relationships(a) as relations, city.city as city"
        result = execute(query)
        return result

    def add(self):
        if not self.find():
            query = "CREATE (n:Location {city:'" + self.city + "', state:'" + self.state + "'}) RETURN n"
            execute(query)
            return True
        else:
            return False

    def delete(self):
        if not self.find():
            return False
        else:
            query = "MATCH (n:Location {city:'" + self.city + "', state:'" + self.state + "'}) DETACH DELETE n"
            execute(query)
            return True

    def get_people_live_in(self, city):
        query = "OPTIONAL MATCH (a:Person)-[r:LIVE_IN]-(b:Location {city:'" + self.city + "'}) RETURN a.name as name, b.city as city"
        result = execute(query)
        return result



class Person:
    def __init__(self, name):
        self.name = name

    def find(self):
        query = "MATCH (n:Person {name: '" + self.name + "'}) RETURN n"
        result = execute(query)
        return (result)

    def add(self):
        if not self.find():
            query = "CREATE(n:Person {name:'" + self.name + "'})"
            execute(query)
            return True
        else:
            return False

    def delete(self):
        if not self.find():
            return False
        else:
            query = "MATCH (p:Person {name: '" + self.name + "'}) DETACH DELETE p "
            execute(query)
            return True

    def add_friend(self, person):
        if self.find() and person.find():
            query = "MATCH(a:Person {name:'" + self.name + "'}),(b:Person {name:'" + person.name + "'}) MERGE(a)-[r:FRIENDS]->(b) RETURN a,b"
            execute(query)
            return True
        else:
            return False

    def add_birthplace(self, place):
        if self.find() and place.find():
            query = "MATCH(a:Person {name:'" + self.name + "'}),(b:Location {city:'" + place.city + "', state:'" + place.state + "'}) MERGE(a)-[r:LIVE_IN]->(b) RETURN a,b"
            execute(query)
            return True
        else:
            return False

    def get_friends(self):
        query = "OPTIONAL MATCH (a:Person {name:'" + self.name + "'})-[r:FRIENDS]-(b:Person) RETURN b"
        result = execute(query)
        return (result)

    def get_birthplace(self):
        query = "OPTIONAL MATCH (a:Person {name:'" + self.name + "'})-[r:LIVE_IN]-(b:Location) RETURN b.city as city, b.state as state"
        result = execute(query)
        return (result)


def list_all_persons():
    query = "MATCH (p:Person) RETURN (p)"
    return execute(query)


def list_all_locations():
    query = "MATCH (n:Location) RETURN (n)"
    return execute(query)
