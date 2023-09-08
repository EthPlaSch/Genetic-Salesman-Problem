import random
from math import sqrt
from tkinter import *
cities = []

def generate():
    # Creating an inital city sizs of 10
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
    for i in range(200):
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
                
            print('Stuck at while 2')
        
        # Adding the route to our list of intial population routes    
        current_generation.append(route)    
        
        # resetting the city numbers       
        for i in range(len(cities)):
            city_numbers.append(i)
    
    return [current_generation, cities]

def calculateRouteDistance(group, cities):

    route_and_distance = []

    for route in group:
        distance = 0
        first_gen = []
        
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
    
    for route in route_and_distance:
        first_gen.append(route[0])
    
    return first_gen, route_and_distance
  
def crossOver(parent_1, parent_2):
    
    start = random.randint(0, len(parent_1) // 2)   
    end = random.randint(start + 1, len(parent_1))
    slicer = slice(start, end)     
    
    new_order = parent_1[slicer]
    
    for number in parent_2:
        if number not in new_order:
            new_order.append(number)
        
    return new_order

def repopulate(r_and_d):
    
    # Cutting the list in half, only keeping the top 50% of answers
    cut_list = r_and_d[:len(r_and_d) // 2]
    new_routes = []
    new_routes += cut_list
    
    for route in range((len(cut_list) // 2)):
        
        # Chosing 2 random parents
        parent_1 = cut_list[random.randint(0, len(cut_list) - 1)]
        parent_2 = cut_list[random.randint(0, len(cut_list) - 1)]
        
        i = 0
        # Preventing the parents from being the same
        while parent_2 == parent_1 and i < 100:
            parent_2 = cut_list[random.randint(0, len(cut_list) - 1)]
            print('Stuck at while 3')
            print(f'I: {i}')
            i += 1
        
        # Splicing the parents genes in half and crossing them over to form 2 new children
        child_1 = crossOver(parent_1, parent_2)
        child_2 = crossOver(parent_1, parent_2)
        
        # Adding the children to a list of new children
        new_routes.append(child_1)
        new_routes.append(child_2)
        
    for route in new_routes:
        if new_routes.index(route) != 0:
            # 10% change to randomly swap two cities in the route to add random mutatation to the gene pool
            for city in route:
                if 1 == random.randint(0, 4):
                    pos_1 = random.randint(0, len(route) - 1)
                    pos_2 = random.randint(0, len(route) - 1)
                    
                    route[pos_1], route[pos_2] = route[pos_2], route[pos_1]
        
    return new_routes

def displayResults(solution, cities):
    
    # Creating a window to show the algorithm's solution
    window = Tk()
    window.title("Algorithm's Solution to the TSP")
    window.configure(bg = '#46425e')
    window.resizable(False, False)
    
    print(solution)
    
    distance = int(solution[1])
    
    label = Label(window, text = f'Distance: {distance}', font = ('aharoni', 30), bg = '#46425e', fg = '#e5e5e5', borderwidth = 0)
    label.pack()
    
    canvas = Canvas(window, bg = '#46425e', height = 500, width = 500, highlightthickness = 0)
    canvas.pack()
    
    solution = solution[0]
    
    for city in solution:
        
        #print(f'City: {city[0]}')
        #print(f'Next City: {cities[cities.index(city) + 1][0]}')
        
        # Create a line between it and the next city
        if solution.index(city) + 1 < len(solution):
            canvas.create_line((cities[city][0] * 3.5) + 65, (cities[city][1] * 3.5) + 65, (cities[solution[solution.index(city) + 1]][0] * 3.5) + 65, (cities[solution[solution.index(city) + 1]][1] * 3.5) + 65, fill = '#00b9be', width = 3)
        else:
            canvas.create_line((cities[city][0] * 3.5) + 65, (cities[city][1] * 3.5) + 65, (cities[solution[0]][0] * 3.5) + 65, (cities[solution[0]][1] * 3.5) + 65, fill = '#00b9be', width = 3)

        canvas.create_oval((cities[city][0] * 3.5) + 60, (cities[city][1] * 3.5) + 60, (cities[city][0] * 3.5) + 70, (cities[city][1] * 3.5) + 70, fill = '#ff6973')
        canvas.create_text((cities[city][0] * 3.5) + 50, (cities[city][1] * 3.5) + 65, text = city, fill = '#e5e5e5', font = ('aharoni', 10))
    canvas.create_oval((cities[0][0] * 3.5) + 60, (cities[0][1] * 3.5) + 60, (cities[0][0] * 3.5) + 70, (cities[0][1] * 3.5) + 70, fill = '#ff6973')
    
    window.mainloop()
    
if __name__ == '__main__':
    group, cities = generate()
    generation, gen_plus_distances = calculateRouteDistance(group, cities)

    i = 0
    while i < 100:
        current_generation_distances, gen_plus_distances = calculateRouteDistance(generation, cities)
        generation = repopulate(current_generation_distances)
        i += 1

    displayResults(gen_plus_distances[0], cities)