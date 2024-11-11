import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data.data_loader import DataLoader

from typing import List
import matplotlib.pyplot as plt
from data.data_loader import DataLoader
from models.model import Issue

class ReopenedIssueAnalysis:

#to analyze all the issues that were closed and then reopened

    def __init__(self):

        self.issues: List[Issue] = DataLoader().get_issues()
        self.reopened_issues_count = 0
        self.reopened_issues_details = []

    def analyze_issues_reopened(self):

    #to analyze reopened issues

        for issue in self.issues:
            closed = False
            reopened = False
            for event in issue.events:
                if event.event_type == 'closed':
                    closed = True
                elif event.event_type == 'reopened':
                    reopened = True
            
            #if issue was both closed and then has event type reopened as well, then we store the details of the issue

            if closed and reopened:
                self.reopened_issues_count += 1
                self.reopened_issues_details.append({
                    'issue_id' : issue.number,
                    'title': issue.title,
                    'labels': issue.labels
                })

    def display_summary(self):
        #to display analysis summary

        print(f"Total issues that were reopened after closing: {self.reopened_issues_count}")
        label_counts = {}
        for issue in self.reopened_issues_details:
            for label in issue['labels']:
                if label in label_counts:
                    label_counts[label] += 1
                else:
                    label_counts[label] = 1
        
        print("Reopened Issues by Label: ")
        for label, count in label_counts.items():
            print(f"{label}: {count}")

    def plot_reopened_issues(self):
        #to plot a bar chart of reopened issues against what label they have

        label_counts = {}
        for issue in self.reopened_issues_details:
            for label in issue['labels']:
                if label in label_counts:
                    label_counts[label] += 1
                else:
                    label_counts[label] = 1
        
        labels = list(label_counts.keys())
        counts = list(label_counts.values())

        
        # Sorting all labels by count to determine the top 5
        sorted_labels_counts = sorted(zip(labels, counts), key=lambda x: x[1], reverse=True)
        # Determine the threshold count for top 5 (including ties)
        threshold_count = sorted_labels_counts[4][1]  # Get the 5th highest count
        # Include all labels with counts greater than or equal to the threshold
        top_5_labels = [label for label, count in sorted_labels_counts if count >= threshold_count]

        plt.figure(figsize=(10,6))
        bars = plt.bar(labels, counts)
        plt.bar(labels, counts)
        plt.xlabel('Issue Labels')
        plt.ylabel('Number of Reopened Issues')
        plt.title('Reopened Isses by Their Label', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')


        # Adding value labels on top of each bar for readability
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval, int(yval), ha='center', va='bottom')

        # Making top 5 labels bold for readability
        ax = plt.gca()
        xtick_labels = ax.get_xticklabels()
        for label in xtick_labels:
            if label.get_text() in top_5_labels:
                label.set_fontweight('bold')

        plt.tight_layout()
        plt.show(block=False) #non-blocking show so that second plot can show too

    def plot_reopened_pichart(self):

        total_no_of_issues = len(self.issues)
        reopened_issues = self.reopened_issues_count
        non_reopened_issues = total_no_of_issues - reopened_issues

        labels = ['Issues that were Reopened', 'Issues that were never Reopened']
        sizes = [reopened_issues, non_reopened_issues]
        colors = ['#c999ff', '#2fe7f7']
        explode = (0.1, 0)  # explode the slice for reopened issues

        fig, ax = plt.subplots(figsize=(8, 6))

        plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, explode=explode, startangle=90)
        plt.title(
            'Percentage of Total Issues that Were Reopened',
            fontsize=14,  
            fontweight='bold',
            pad=30  # Move the title higher by adding padding
        )
        plt.axis('equal')  # Equal aspect ratio to ensure that the pie chart is drawn as a circle.
        plt.show()



    def run(self):
            """
            Run the full analysis and display results.
            """
            self.analyze_issues_reopened()
            self.display_summary()
            self.plot_reopened_issues()
            self.plot_reopened_pichart()

if __name__ == '__main__':
# Run the analysis when the script is executed
    ReopenedIssueAnalysis().run()



