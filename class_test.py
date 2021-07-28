########################################################################
class Dict2Obj():
    """
    Turns a dictionary into a class
    """

    #----------------------------------------------------------------------
    def __init__(self, dictionary):
        """Constructor"""
        for key in dictionary:
            setattr(self, key, dictionary[key])
        
    
#----------------------------------------------------------------------
if __name__ == "__main__":
    ball_dict = {"color":"blue",
                 "size":"8 inches",
                 "material":"rubber"}
    ball = Dict2Obj(ball_dict)
    print(ball.color)