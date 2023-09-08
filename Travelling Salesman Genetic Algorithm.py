import random
from math import sqrt
from tkinter import *
cities = []

num_gen = int(input('Number of Generations: '))
population_size = int(input('Population Size: '))
num_cities = int(input('Number of Cities (10 to 20): '))

def generate(pop_size, num_cities):
    # Creating an inital city sizs of 10
    for i in range(num_cities):
        city = [random.randint(1, 100), random.randint(1, 100)]
        
        # Making sure we have unique set of cities
        while city in cities:
            city = [random.randint(1, 100), random.randint(1, 100)]
            
        cities.append(city)
        
    city_numbers = []

    # Creating the list of city numbers (1 to the number of cities)
    for i in range(len(cities)):
        city_numbers.append(i)

    current_generation = []

    # Generating a bunch of random solutions (the intial population)
    for i in range(pop_size):
        route = []

        # Generating a route
        for i in range(len(city_numbers)):
            val = random.choice(city_numbers)
            route.append(val)
            city_numbers.remove(val)
        
        # # Avoiding any repeat routes when creating the inital population
        # while route in current_generation:

        #     # Generating a route
        #     for i in range(len(city_numbers)):
        #         val = random.choice(city_numbers)
        #         route.append(val)
        #         city_numbers.remove(val)

        
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
        average_line_len = 0
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
            average_line_len += sqrt(((city_2[0] - city_1[0]) ** 2) + ((city_2[1] - city_1[1]) ** 2))
         
        average_line_len = average_line_len / len(route)
            
        route_and_distance.append([route, average_line_len, distance])
        
    route_and_distance.sort(key = lambda x: x[1])
    route_and_distance.sort(key = lambda x: x[2])
    
    #print(f'Route, Score and Distance: {route_and_distance}\n')
    
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
    
    parent_1 = cut_list[0]
    parent_2 = cut_list[1]
    
    # Splicing the parents genes in half and crossing them over to form 2 new children
    child_1 = crossOver(parent_1, parent_2)
    child_2 = crossOver(parent_1, parent_2)
        
    # Adding the children to a list of new children
    new_routes.append(child_1)
    new_routes.append(child_2)
    
    for route in range(((len(cut_list) // 2) - 1)):
        
        # Chosing 2 random parents
        len_cut_list = len(cut_list)
        p1_num = random.randint(0, len_cut_list - 1)
        p2_num = random.randint(0, len_cut_list - 1)
        count = 0
        while p1_num == p2_num and count < 10:
            p2_num = random.randint(0, len_cut_list - 1)
            count += 1
        parent_1 = cut_list[p1_num]
        parent_2 = cut_list[p2_num]
        
        # Splicing the parents genes in half and crossing them over to form 2 new children
        child_1 = crossOver(parent_1, parent_2)
        child_2 = crossOver(parent_1, parent_2)
        
        # Adding the children to a list of new children
        new_routes.append(child_1)
        new_routes.append(child_2)
        
    for idx, route in enumerate(new_routes):
        if idx == 0:
            continue
        # 10% change to randomly swap two cities in the route to add random mutatation to the gene pool
        for city in route:
            if 1 == random.randint(0, 10):
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
    
    route = str(solution[0][0])
    
    for i in range(1, len(solution[0])):
        route += f', {str(solution[0][i])}'
    
    print(f"Route: {route.strip()} | Distance: {int(solution[2])}")
    
    distance = int(solution[2])
    
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
    group, cities = generate(population_size, num_cities)
    
    print('Simulating Evolution...')
    generation, route_score_distance = calculateRouteDistance(group, cities)

    i = 0
    while i < num_gen:
        current_generation_distances, route_score_distance = calculateRouteDistance(generation, cities)
        generation = repopulate(current_generation_distances)
        i += 1

    print('Done!')
    displayResults(route_score_distance[0], cities)