
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

class CombinedCategory():
    def __init__(self, name, mean1, mean2, std1, std2, size1, size2):
        self.mean1 = mean1
        self.mean2 = mean2
        self.std1 = std1
        self.std2 = std2
        self.size1 = size1
        self.size2 = size2
        self.name = name
    
    def get_mean(self):
        return (self.mean1 + self.mean2) / 2
    
    def get_std(self):
        return (self.std1**2 + self.std2**2)**(1/2)/2
    
    def get_size(self):
        return self.size1 + self.size2
    
    def get_name(self):
        return self.name

category = Category(name="Q3", mean=2, std=1, size=10)
#print(category.get_samples(5))