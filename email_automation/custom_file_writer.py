# Writting a context manager class

class CustomFileWriter:
    def __init__(self, filename):
        self.filename = filename
        
    def __enter__(self):
        self.file = open(self.filename, 'w')
        return self.file
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()
        
        
with CustomFileWriter('sample4.txt') as file:
    file.write('Where is my CAT?')
    
    
    

