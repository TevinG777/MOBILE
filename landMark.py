import math
import numpy as np

# ———— Configuration ————

# Sensor landmarks (always hard‑coded)
L1 = (-2,  -2)
L2 = ( -2,  2)
L3 = (2, 2)
L4 = ( 2, -2)

# Particle coordinates (always given as x,y)
particle = (-0.5, -0.5)

# Mode flag: if True, we use explicit robot coords; if False, we use pre‑measured distances
USE_ROBOT_COORDS = True

# If USE_ROBOT_COORDS == True, fill in:
robot = (1.0, 0.0)

# If USE_ROBOT_COORDS == False, fill in robot_distances:
robot_distances = [4.0, 5.0, 4.0, 2.0]

def trilaterate(p1, r1, p2, r2, p3, r3):
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3
    A = np.array([
        [2*(x2 - x1), 2*(y2 - y1)],
        [2*(x3 - x1), 2*(y3 - y1)]
    ])
    b = np.array([
        (r1**2 - x1**2 - y1**2) - (r2**2 - x2**2 - y2**2),
        (r1**2 - x1**2 - y1**2) - (r3**2 - x3**2 - y3**2),
    ])
    return tuple(np.linalg.solve(A, b))

def calculate_normdist(s, mu, sigma = 1):
    coefficient = 1/ (math.sqrt(2*math.pi*sigma**2))
    exponent = -((s-mu)**2) / (2*sigma**2)
    probability = coefficient * math.exp(exponent)
    return probability


def euclidean(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def gaussian_pdf(x, mu, sigma=1.0):
    coeff = 1.0 / (math.sqrt(2 * math.pi) * sigma)
    exponent = -0.5 * ((x - mu) / sigma) ** 2
    return coeff * math.exp(exponent)

def main():
    landmarks = [("L1", L1), ("L2", L2), ("L3", L3), ("L4", L4)]

    # Part 1: particle → landmarks
    print("Distances from PARTICLE to each landmark:")
    d_particle = {}
    for name, coord in landmarks:
        d = euclidean(particle, coord)
        d_particle[name] = d
        print(f"  {name}: {d:.3f} m")

    # Part 2: robot → landmarks (either via coords or via given distances)
    print("\nDistances from ROBOT to each landmark:")
    d_robot = {}
    if USE_ROBOT_COORDS:
        for name, coord in landmarks:
            d = euclidean(robot, coord)
            d_robot[name] = d
            print(f"  {name}: {d:.3f} m")
    else:
        for (name, _), dist in zip(landmarks, robot_distances):
            d_robot[name] = dist
            print(f"  {name}: {dist:.3f} m")
        
    importances = []

    # Part 3: normal distribution probabilities σ=1
    print("\nGaussian probabilities p(particle_dist | robot_dist, o=1):")
    for name in [n for n, _ in landmarks]:
        mu = d_robot[name]
        x  = d_particle[name]
        p  = calculate_normdist(x, mu, sigma=1.0)
    
        
        print(f"  {name}: {p:.5f}")
        importances.append(p)
        
        
    # Part 4: Weighted normal distribution for C7 (P7)
    product = 1.0
    for i in importances:
        product *= i
    print(f"\nWeighted normal distribution for C7 (P7): {product:.9f}")
    
    x_est, y_est = trilaterate(
        L2, d_robot["L2"],  # (2.5,  2.5), distance = 5.0
        L3, d_robot["L3"],  # (-2.5, -2.5), distance = 4.0
        L4, d_robot["L4"]   # (2.5, -2.5), distance = 2.0
    )
    
    print("\nTrilateration estimate of robot position:")
    print(f"  x = {x_est:.3f}, y = {y_est:.3f}")

    


if __name__ == "__main__":
    main()
