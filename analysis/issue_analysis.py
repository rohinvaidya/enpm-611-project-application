import config as config
from datetime import datetime
from collections import defaultdict
from data.data_loader import DataLoader
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
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
        issues:List[Issue] = DataLoader().get_issues()
        
        #==========Find the ratio of open and closed issues============
        # analysis_open_closed_ratio(self,issues)

        #==========Find top 5 labels in issues============
        # top_labels(self,issues)

        #==========Find the ratio of assignee and no assignee for issues============
        # assignee_ratio(self,issues)

        if self.label is None:
            time_to_assign_user(self,issues)
        else:
            time_to_assign_user_label(self,issues)

        
            


def time_to_assign_user_label(self,issues):
    assignedtime = []
    for issue in issues:
        for label in issue.labels:
            if label == self.label and issue.assignees:
                for event in issue.events:
                    if event.event_type== "assigned":
                        assignedtime.append((event.event_date - issue.created_date).total_seconds()/(86400*30))
    print("IN IF COND = ",len(assignedtime))
    plt.figure(figsize=(10, 6))  # Set figure size for better visibility
    plt.hist(assignedtime, bins=40, color='skyblue', edgecolor='black')
    plt.xlabel('Time to Assign (Months)')
    plt.ylabel('Number of Issues')
    plt.title('Distribution of Time to Assign Issues (Label = '+self.label+')')
    plt.show()

def time_to_assign_user(self,issues):
    assignedtime = []
    for issue in issues:
        if issue.assignees:
            for event in issue.events:
                if event.event_type== "assigned":
                    assignedtime.append((event.event_date - issue.created_date).total_seconds()/(86400*30))
    print(len(assignedtime))

    plt.figure(figsize=(10, 6))  # Set figure size for better visibility

    # Create a histogram to show the distribution of assignment times
    plt.hist(assignedtime, bins=40, color='skyblue', edgecolor='black')

    # Labels and title
    plt.xlabel('Time to Assign a User (Months)')
    plt.ylabel('Number of Issues')
    plt.title('Distribution of Time to Assign Issues')
    plt.show()      

def analysis_open_closed_ratio(self,issues):
    open_issue_count = 0
    closed_issue_count = 0
    notknown_count = 0
    for issue in issues:
        if issue.state == "open":
            open_issue_count += 1
        elif issue.state == "closed":
            closed_issue_count += 1
        else:
            notknown_count += 1
    # Plotting the pie chart for open/closed issue i.e. status
    plt.figure(figsize=(8, 8))
    plt.pie([open_issue_count, closed_issue_count], labels=["open issue","closed issue"], autopct='%1.1f%%', startangle=140)
    plt.title('Status of Issues')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

def top_labels(self,issues):
    all_labels = find_labels(self,issues)
    label_title:List[str] = []
    label_count:List[int]= []
    for label,count in all_labels[0:5]:
        label_title.append(label)
        label_count.append(count)
    #Combining all other issues in one category i.e. others
    others_count = 0
    for label,count in all_labels[5:]:
        others_count += count
    
    label_title.append("all other labels")
    label_count.append(others_count)

    # Plotting the bar chart for top labels in issues
    plt.figure(figsize=(12, 8))  # Set a larger figure size for readability
    plt.bar(label_title, label_count, color='skyblue')
    plt.title("Top 5 Labels in Issues")
    plt.xlabel("Labels")
    plt.ylabel("Counts")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()  # Adjust layout for better spacing
    plt.show() 

def assignee_ratio(self,issues):
    no_assignee_in_issue = 0
    assignee_in_issue = 0
    for issue in issues:
        if not issue.assignees:
            no_assignee_in_issue += 1
        else:
            assignee_in_issue += 1
    # Plotting the pie chart for ratio of assignee and no assignee
    plt.figure(figsize=(8, 8))
    plt.pie([no_assignee_in_issue, assignee_in_issue], labels=["No Assignee", "Have assignee"], autopct='%1.1f%%', startangle=140)
    plt.title('Ratio of assignee and no assignee')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()
        
def find_labels(self,issues):
    label_counts = defaultdict(int)
    # Iterate over each Issue object in the list
    for issue in issues:
        # Assuming `labels` is a list attribute on the Issue object
        if issue.state == self.state:
            for label in issue.labels:
                label_counts[label] += 1
    sorted_labels = sorted(label_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_labels

if __name__ == '__main__':
    # Invoke run method when running this module directly
    IssueAnalysis().run()