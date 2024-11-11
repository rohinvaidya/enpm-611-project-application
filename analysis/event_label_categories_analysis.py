from typing import List, Dict
import matplotlib.pyplot as plt
import pandas as pd

from data.data_loader import DataLoader
from models.model import Issue
import config

class EventLabelCategoriesAnalysis:
    """
    Analyzes the number of label events for a specified label prefix in GitHub issues.
    Outputs the findings to standard out and generates a bar chart with annotations.
    
    The label prefix is specified via the --label command-line argument.
    For example:
        --label status        -> Analyzes labels starting with 'status/'
        --label area          -> Analyzes labels starting with 'area/'
    """
    
    def run(self):
        # Retrieve the label prefix from the config (set via --label)
        label_prefix = config.get_parameter('label') 
        
        if not label_prefix:
            print("Error: No label prefix provided. Please specify a label with the --label flag.")
            return
        
        # Ensure the label_prefix ends with '/' for accurate matching
        if not label_prefix.endswith('/'):
            label_prefix += '/'
        
        # Load all issues using the DataLoader
        issues: List[Issue] = DataLoader().get_issues()
        
        # Dictionary to hold label event counts
        label_event_counts: Dict[str, int] = {}
        
        # Iterate through each event in each issue
        for issue in issues:
            for event in issue.events:
                if event.event_type == 'labeled' and event.label:
                    label = event.label.lower()
                    # Check if the label starts with the specified prefix
                    if label.startswith(label_prefix):
                        label_clean = label.replace(label_prefix, '')
                        label_event_counts[label_clean] = label_event_counts.get(label_clean, 0) + 1
        
        if not label_event_counts:
            print(f"No label events found with prefix '{label_prefix}' in the issues data.")
            return
        
        # Convert the label_event_counts dictionary to a DataFrame for easier manipulation
        df = pd.DataFrame(list(label_event_counts.items()), columns=['Label', 'Event Count'])
        df_sorted = df.sort_values(by='Event Count', ascending=False)
        
        # Output the results to standard out
        print(f"Status Event Analysis for label prefix '{label_prefix}':")
        print(df_sorted.to_string(index=False))
        
        # Generate a Bar Chart
        plt.figure(figsize=(12, 8))
        bars = plt.bar(df_sorted['Label'], df_sorted['Event Count'], color='skyblue')
        plt.xlabel('Labels')
        plt.ylabel('Number of Events')
        plt.title(f"Distribution of '{label_prefix[:-1]}' Label Events in GitHub Issues")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Annotate each bar with the event count
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{height}',
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        plt.show()

if __name__ == '__main__':
    # Invoke run method when running this module directly
    EventLabelCategoriesAnalysis().run()