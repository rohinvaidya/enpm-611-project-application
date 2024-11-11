from typing import List, Dict
import matplotlib.pyplot as plt
import pandas as pd

from data.data_loader import DataLoader
from models.model import Issue
import config

class UserSpecificIssueAnalysis:
    """
    Provides insights into a specific user's interactions with issues.
    Outputs the findings to standard out and generates a horizontal bar chart.
    """
    
    def run(self):
        user: str = config.get_parameter('user')
        if not user:
            print("No user specified. Please provide a user with the --user flag.")
            return
        
        issues: List[Issue] = DataLoader().get_issues()
        
        # Initialize counters
        created_count = 0
        commented_count = 0
        labeled_count = 0
        closed_count = 0
        
        # Dictionary to hold label-wise interaction counts
        label_interactions: Dict[str, int] = {}
        
        for issue in issues:
            # Check if user created the issue
            if issue.creator == user:
                created_count += 1
            
            # Iterate through events
            for event in issue.events:
                if event.author == user:
                    if event.event_type == 'commented':
                        commented_count += 1
                    elif event.event_type == 'labeled':
                        labeled_count += 1
                    elif event.event_type == 'closed':
                        closed_count += 1
                
                # Count label interactions
                if event.author == user and event.label:
                    label_interactions[event.label] = label_interactions.get(event.label, 0) + 1
        
        # Output to standard out
        print(f"Insights for User: {user}")
        print(f"Issues Created: {created_count}")
        print(f"Comments Made: {commented_count}")
        print(f"Issues Labeled: {labeled_count}")
        print(f"Issues Closed: {closed_count}")
        
        if label_interactions:
            print("\nLabel Interactions:")
            df_labels = pd.DataFrame(list(label_interactions.items()), columns=['Label', 'Interactions']).sort_values(by='Interactions', ascending=True)
            print(df_labels.to_string(index=False))
            
            # Generate Horizontal Bar Chart
            plt.figure(figsize=(14, 10))
            plt.barh(df_labels['Label'], df_labels['Interactions'], color='coral')
            plt.xlabel('Number of Interactions')
            plt.title(f"Label Interactions by User '{user}'")
            plt.yticks(fontsize=9)
            plt.tight_layout()
            plt.show()
            
            
if __name__ == '__main__':
    # Invoke run method when running this module directly
    UserSpecificIssueAnalysis().run()