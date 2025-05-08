# Define movement probabilities
probabilities = {
    'F': 0.6,
    'S': 0.2,
    'L': 0.1,
    'R': 0.1
}

# Dictionary to store total probability per cell
cell_probs = {}

# Process the file
with open("cellMotion.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        movement, cell = line.strip().split("=")
        movement = movement.strip()
        cell = cell.strip()
        
        if len(movement) == 2:
            first, second = movement[0], movement[1]
            prob = probabilities.get(first, 0) * probabilities.get(second, 0)
            
            # Add or update the total probability for the cell
            if cell in cell_probs:
                cell_probs[cell] += prob
            else:
                cell_probs[cell] = prob

# Sort the list by converting the number after the C to an int 
sortedList = sorted(cell_probs.items(), key=lambda x:int(x[0][1:]))

# Print the summed probabilities per cell
for cell, total_prob in sortedList:
    print(f"{cell}: {total_prob:.4f}")
