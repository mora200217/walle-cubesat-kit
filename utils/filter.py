class LowPassFilter:
    def __init__(self, alpha):
        self.alpha = alpha
        self.prev_y = 0  # Initial previous output

    def update(self, x):
        self.prev_y = self.alpha * x + (1 - self.alpha) * self.prev_y
        return self.prev_y

def apply_low_pass(data, alpha=0.4):
    filter = LowPassFilter(alpha)
    for x in data:
        filtered_value = filter.update(x)
    return filtered_value  # Return the final filtered value