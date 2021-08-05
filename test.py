class test():
    def __init__(self, dict):
        self.name = 0
        self.set_attributes(dict)
        print(self.name)
    def set_attributes(self, plant_model):
        for key in plant_model:
            setattr(self, key, plant_model[key])

a = test({'name': 'My_Name'})