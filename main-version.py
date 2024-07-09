import random
import math

def generate_vrp_instance(num_clients, num_vehicles, seed):
    random.seed(seed)
    base = (50, 50)
    points = [(random.randint(1, 100), random.randint(1, 100)) for _ in range(num_clients)]
    return base, points, num_vehicles

def distance(point1, point2):
    return round(math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2))

def total_distance(routes):
    return sum(distance(route[i], route[i+1]) for route in routes for i in range(len(route) - 1))

def initial_solution(base, points, num_vehicles):
    routes = [[] for _ in range(num_vehicles)]
    # Sort points by distance from the base
    sorted_points = sorted(points, key=lambda x: distance(base, x))
    for i, point in enumerate(sorted_points):
        routes[i % num_vehicles].append(point)
    for route in routes:
        route.insert(0, base)
        route.append(base)
    return routes

def neighbor_solution(routes):
    return swap(routes)

def swap(routes):
    r1, r2 = random.sample(range(len(routes)), 2)
    if len(routes[r1]) > 2 and len(routes[r2]) > 2:
        i1, i2 = random.randint(1, len(routes[r1]) - 2), random.randint(1, len(routes[r2]) - 2)
        routes[r1][i1], routes[r2][i2] = routes[r2][i2], routes[r1][i1]
    return routes

def sa_algorithm(base, points, num_vehicles, max_iter, temp_init, cooling_rate, stagnation_threshold, seed, epochs):
    random.seed(seed)
    routes = initial_solution(base, points, num_vehicles)
    best_routes = routes
    best_distance = total_distance(routes)
    temp = temp_init
    epoch_length = max_iter // epochs
    print(f"Initial total distance: {best_distance}")

    for iter in range(max_iter):
        if iter % epoch_length == 0 and iter > 0:
            temp *= cooling_rate
            print(f"Epoch {iter // epoch_length}: Temperature reduced to {temp:.2f}")

        new_routes = neighbor_solution([route[:] for route in routes])
        new_distance = total_distance(new_routes)
        delta_distance = new_distance - best_distance

        if delta_distance < 0 or random.random() < math.exp(-delta_distance / temp):
            routes = new_routes
            if new_distance < best_distance:
                best_routes = [route[:] for route in routes]
                best_distance = new_distance
                print(f"{iter + 1} {best_distance}")

    return best_routes

# Parameters for the SA
num_clients = 10
num_vehicles = 5
seed = 40
max_iter = 1000
temp_init = 1000
cooling_rate = 0.95
stagnation_threshold = 100
epochs = 10  # Adjust the number of epochs as needed

base, points, num_vehicles = generate_vrp_instance(num_clients, num_vehicles, seed)
best_routes = sa_algorithm(base, points, num_vehicles, max_iter, temp_init, cooling_rate, stagnation_threshold, seed, epochs)

print("Best routes:")
for idx, route in enumerate(best_routes):
    print(f"Vehicle {idx + 1} Route = {route}")
