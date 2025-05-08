# Sensor models
left_model = {
    (0, 0): 0.7,
    (0, 1): 0.1,
    (1, 0): 0.3,
    (1, 1): 0.9
}
front_model = {
    (0, 0): 0.7,
    (0, 1): 0.1,
    (1, 0): 0.3,
    (1, 1): 0.9
}
right_model = {
    (0, 0): 0.7,
    (0, 1): 0.1,
    (1, 0): 0.3,
    (1, 1): 0.9
}

# Observation z = [L, F, R] = [1, 0, 1]
z = [1, 1, 0]

# Cell wall configurations: s = [L, F, R]
cell_configs = {
    "C1":  [1, 1, 1],
    "C2":  [1, 1, 0],
    "C3":  [0, 0, 1],
    "C4":  [0, 0, 0],
    "C5":  [0, 1, 1],
    "C6":  [0, 1, 0],
    "C7":  [1, 1, 0],
    "C8":  [1, 0, 1],
    "C9":  [0, 0, 1],
}

# Step (a): Compute unnormalized probabilities
raw_probs = {}
print("Step (a): Unnormalized p(z|s) for each cell:\n")
for cell, s in cell_configs.items():
    l_prob = left_model[(z[0], s[0])]
    f_prob = front_model[(z[1], s[1])]
    r_prob = right_model[(z[2], s[2])]
    total_prob = l_prob * f_prob * r_prob
    raw_probs[cell] = total_prob
    print(f"{cell}: L={l_prob}, F={f_prob}, R={r_prob} → Total={total_prob:.6f}")

# Step (b): Normalize the probabilities
total_sum = sum(raw_probs.values())
normalized = {cell: prob / total_sum for cell, prob in raw_probs.items()}

print(f"\nNormalization factor: {total_sum:.6f}")

print("\nStep (b): Normalized probabilities:\n")
for cell, prob in normalized.items():
    print(f"{cell}: {prob:.3f}")

