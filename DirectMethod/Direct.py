from utils.tree import generate_Tree


class Direct(object):
    """Direct

    Args:
        regular_expression (_string_): This is the regular 
            expression that the Thomson algorythm will evaluate
    """
    def __init__(self, regular_expression):
        super(Direct, self).__init__()
        self.tree = generate_Tree(regular_expression)
        
    
            