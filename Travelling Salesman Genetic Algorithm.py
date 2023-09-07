import random
from math import sqrt
cities = []

def generate():
    # Creating an inital city sizs of 50
    for i in range(10):
        city = [random.randint(1, 100), random.randint(1, 100)]
        
        # Making sure we have unique set of cities
        while city in cities:
            print('Repeat city, trying again')
            city = [random.randint(1, 100), random.randint(1, 100)]
            
        cities.append(city)
        
    city_numbers = []

    # Creating the list of city numbers (1 to the number of cities)
    for i in range(len(cities)):
        city_numbers.append(i)

    current_generation = []

    # Generating a bunch of random solutions (the intial population)
    for i in range(100):
        route = []

        # Generating a route
        for i in range(len(city_numbers)):
            val = random.choice(city_numbers)
            route.append(val)
            city_numbers.remove(val)
        
        # Avoiding any repeat routes when creating the inital population
        while route in current_generation:

            # Generating a route
            for i in range(len(city_numbers)):
                val = random.choice(city_numbers)
                route.append(val)
                city_numbers.remove(val)
        
        # Adding the route to our list of intial population routes    
        current_generation.append(route)    
        
        # resetting the city numbers       
        for i in range(len(cities)):
            city_numbers.append(i)
    
    return [current_generation, cities]

def routeDistance(group, cities):

    route_and_distance = []

    for route in group:
        distance = 0
        
        for city in route:
            
            # Find the current city and next cities position
            city_1 = cities[city]
            # If you are at the last item in the list, make the next city the starting city
            if route.index(city) + 1 != len(route):
                city_2 = cities[route[(route.index(city)) + 1]]
            else:
                city_2 = cities[0]
                
            distance += sqrt(((city_2[0] - city_1[0]) ** 2) + ((city_2[1] - city_1[1]) ** 2))
            
        route_and_distance.append([route, distance])
        
    route_and_distance.sort(key = lambda x: x[1])
        
    return route_and_distance

def repopulate(r_and_d):
    
    # Cutting the list in half, only keeping the top 50% of answers
    cut_list = r_and_d[:len(r_and_d)//2]
    new_routes = []
    
    for route in range((len(r_and_d) // 2)):
        
        # Chosing 2 random parents
        parent_1 = cut_list[random.randint(0, len(cut_list) - 1)][0]
        parent_2 = cut_list[random.randint(0, len(cut_list) - 1)][0]
        
        # Preventing the parents from being the same
        while parent_2 == parent_1:
            parent_2 = cut_list[random.randint(0, len(cut_list) - 1)][0]
        
        # Splicing the parents genes in half and crossing them over to form 2 new children
        child_1 = []
        child_2 = []
        child_1 += (parent_1[:len(parent_1)//2])
        child_1 += (parent_2[len(parent_2)//2:])
        child_2 += (parent_2[:len(parent_2)//2])
        child_2 += (parent_1[len(parent_1)//2:])
        
        # Adding the children to a list of new children
        new_routes.append(child_1)
        new_routes.append(child_2)
        
    new_generation = []
    for routes in r_and_d:
        new_generation.append(routes[0])
        
    new_generation += new_routes
    
    for route in new_generation:
        
        # 10% change to randomly swap two cities in the route to add random mutatation to the gene pool
        for city in route:
            if 1 == random.randint(0, 10):
                pos_1 = random.randint(0, len(route) - 1)
                pos_2 = random.randint(0, len(route) - 1)
                
                route[pos_1], route[pos_2] = route[pos_2], route[pos_1]
        
    return new_generation

if __name__ == '__main__':
    group, cities = generate()
    current_generation = routeDistance(group, cities)
    
    i = 0
    while i < 200:
        
        repopulate(current_generation)
        current_generation = repopulate(current_generation)
        
        i += 1