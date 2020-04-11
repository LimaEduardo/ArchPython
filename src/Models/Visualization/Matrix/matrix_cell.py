class MatrixCell:

    def __init__(self, from_module, to_module, status_module ):
        self.from_module = from_module
        self.to_module = to_module
        self.status_module = status_module
    
    def get_representation(self):
        return {
            "from" : self.from_module,
            "to" : self.to_module,
            "color" : self.status_module.value["Color"]
        }