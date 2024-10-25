import config as config

class EventAnalysis:
    """
    Implements event analysis of GitHub
    issues and outputs the result of that analysis.
    """
    
    def __init__(self):
        """
        Constructor
        """
        # Parameter is passed in via command line (--user)
        self.user:str = config.get_parameter('user')
        self.label:str = config.get_parameter('label')
    
    def run(self):
        pass

if __name__ == '__main__':
    # Invoke run method when running this module directly
    EventAnalysis().run()