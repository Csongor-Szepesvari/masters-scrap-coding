
import numpy as np
class Category():
    def __init__(self, name, mean, std, size):
        self.mean = mean
        self.std = std
        self.size = size
        self.name = name
    
    def get_samples(self, n:int):
        if n > self.size:
            raise ValueError("Error: we can't sample more than there are elements in this category.")
        else:
            rng = np.random.default_rng()
            return rng.normal(loc=self.mean, scale=self.std, size=n)
        
    def get_mean(self):
        return self.mean
    
    def get_std(self):
        return self.std
    
    def get_size(self):
        return self.size
    
    def get_name(self):
        return self.name



category = Category(name="Q3", mean=2, std=1, size=10)
#print(category.get_samples(5))