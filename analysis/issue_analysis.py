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
        #plt.show()

        #==========Find top 5 label of open or closed issues============
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
        plt.title("Top 5 Issue Label Counts("+self.state+")")
        plt.xlabel("Labels")
        plt.ylabel("Counts")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()  # Adjust layout for better spacing
        #plt.show() 

        #==========Find the ratio of assignee and no assignee for issues============
        no_assignee_in_issue = 0
        assignee_in_issue = 0
        for issue in issues:
            if issue.state == self.state:
                if not issue.assignees:
                    no_assignee_in_issue += 1
                else:
                    assignee_in_issue += 1
        # Plotting the pie chart for ratio of assignee and no assignee
        plt.figure(figsize=(8, 8))
        plt.pie([no_assignee_in_issue, assignee_in_issue], labels=["No Assignee", "Have assignee"], autopct='%1.1f%%', startangle=140)
        plt.title('Ratio of assignee and no assignee('+self.state+')')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        #plt.show()

        # temp = find the issues that do not have assignee and includes top 5 labels in it
        count_issue_assignee = ''
        high_priority_issue_list = []
        for issue in issues:
            if issue.state == self.state:
                for label in issue.labels:
                    if (label in label_title) and not issue.assignees:
                        high_priority_issue_list.append(issue)
        print(len(high_priority_issue_list))    

        count_of_events = []
        for high_priority_issue in high_priority_issue_list:
            if(len(high_priority_issue.events)) > 20:
                count_of_events.append(high_priority_issue)
        print(len(count_of_events)) 

        #==========Find the count of issues that have same number of events============
        event_count_dict = defaultdict(int)

        for high_priority_issue in high_priority_issue_list:
            event_count = len(high_priority_issue.events)
            event_count_dict[event_count] += 1

        # Sort event counts by the number of issues in descending order
        sorted_event_counts = sorted(event_count_dict.items(), key=lambda x: x[1], reverse=True)
        event_counts = [count for count, _ in sorted_event_counts]  # x-axis: event counts
        issue_counts = [issues for _, issues in sorted_event_counts]  # y-axis: number of issues

        # Plotting the bar chart
        plt.figure(figsize=(12, 8))
        plt.bar(event_counts, issue_counts, color='skyblue')
        plt.title('Number of Issues by Event Count in High-Priority Issues')
        plt.xlabel('Number of Events')
        plt.ylabel('Number of Issues')
        plt.xticks(rotation=45)
        plt.tight_layout()
        # plt.show()

        # Scatter Plot
        plt.figure(figsize=(10, 6))
        plt.scatter(event_counts, issue_counts, color='orange', s=100, alpha=0.7)
        plt.title('Scatter Plot of Issues by Event Count in High-Priority Issues')
        plt.xlabel('Number of Events')
        plt.ylabel('Number of Issues')
        plt.xticks(rotation=45)
        plt.grid(True)
        # plt.show()

        
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



# Priority scoring function
def calculate_issue_priority(issue):
    # Define scoring weights (can be tuned)
    LABEL_WEIGHTS = {
        "area/docs": 1,
        "status/triage": 2,
        "bug": 5,
        "feature-request": 3,
        "urgent": 10
    }
    COMMENT_WEIGHT = 1      # Points per comment
    ASSIGNEE_WEIGHT = 2     # Points if assigned to a team member
    RECENT_ACTIVITY_WEIGHT = 3  # Points if recently updated
    MAX_DAYS_FOR_ACTIVITY = 7   # Days within which an activity is considered "recent"
    score = 0

    # Add points for each label based on its importance
    for label in issue['labels']:
        score += LABEL_WEIGHTS.get(label, 0)  # Default weight of 0 if label not in weights

    # Add points for comments
    num_comments = sum(1 for event in issue['events'] if event['event_type'] == 'commented')
    score += num_comments * COMMENT_WEIGHT

    # Add points if issue is assigned
    if issue['assignees']:
        score += ASSIGNEE_WEIGHT

    # Add points if there is recent activity (within MAX_DAYS_FOR_ACTIVITY)
    last_updated = datetime.fromisoformat(issue['updated_date'].replace("Z", "+00:00"))
    days_since_update = (datetime.now() - last_updated).days
    if days_since_update <= MAX_DAYS_FOR_ACTIVITY:
        score += RECENT_ACTIVITY_WEIGHT

    return score

if __name__ == '__main__':
    # Invoke run method when running this module directly
    IssueAnalysis().run()