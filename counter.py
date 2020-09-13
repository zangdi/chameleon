class Counter():
    def __init__(self):
        self.val = 0
    
    def next(self):
        self.val += 1
        return self.val