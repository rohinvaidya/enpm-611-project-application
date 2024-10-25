import config as config

class IssueAnalysis:
    """
    Implements issue analysis of GitHub
    issues and outputs the result of that analysis.
    """
    
    def __init__(self, state:str):
        """
        Constructor
        """
        # Parameter is passed in via command line (--user)
        self.user:str = config.get_parameter('user')
        self.label:str = config.get_parameter('label')
        self.state:str = state
    
    def run(self):
        if self.state == 'open':
            print('You chose open!')
            print(f'Found {self.user} events across {len(self.label)}')
        elif self.state == 'closed':
            print('You chose closed!')
            print(f'Found {self.user} events across {len(self.label)}')

if __name__ == '__main__':
    # Invoke run method when running this module directly
    IssueAnalysis().run()