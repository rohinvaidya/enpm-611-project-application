# status_event_analysis.py

from typing import List, Dict
import matplotlib.pyplot as plt
import pandas as pd

from data.data_loader import DataLoader
from models.model import Issue

class StatusEventAnalysis:
    """
    Analyzes the number of status-related label events in GitHub issues.
    Outputs the findings to standard out and generates a bar chart with annotations.
    """
    
    def run(self):
        # Load all issues using the DataLoader
        issues: List[Issue] = DataLoader().get_issues()
        
        # Dictionary to hold status label event counts
        status_event_counts: Dict[str, int] = {}
        
        # Iterate through each issue
        for issue in issues:
            # Iterate through each event in the issue
            for event in issue.events:
                # Check if the event is a label addition event
                if event.event_type == 'labeled' and event.label:
                    label = event.label.lower()  # Normalize label to lowercase for consistency
                    # Check if the label starts with 'status/'
                    if label.startswith('status/'):
                        # Remove the 'status/' prefix
                        label_clean = label.replace('status/', '')
                        # Increment the count for the cleaned label
                        status_event_counts[label_clean] = status_event_counts.get(label_clean, 0) + 1
        
        if not status_event_counts:
            print("No status-related label events found in the issues data.")
            return
        
        # Convert the status_event_counts dictionary to a DataFrame for easier manipulation
        df = pd.DataFrame(list(status_event_counts.items()), columns=['Status Label', 'Event Count'])
        
        # Sort the DataFrame in descending order of event counts
        df_sorted = df.sort_values(by='Event Count', ascending=False)
        
        # Output the results to standard out
        print("Status Event Analysis:")
        print(df_sorted.to_string(index=False))
        
        # Generate a Bar Chart
        plt.figure(figsize=(12, 8))
        bars = plt.bar(df_sorted['Status Label'], df_sorted['Event Count'], color='skyblue')
        plt.xlabel('Status Labels')
        plt.ylabel('Number of Events')
        plt.title('Distribution of Status Label Events in GitHub Issues')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Annotate each bar with the event count
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{height}',
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),  # 3 points vertical offset
                         textcoords="offset points",
                         ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        plt.show()

        
if __name__ == '__main__':
    # Invoke run method when running this module directly
    StatusEventAnalysis().run()
