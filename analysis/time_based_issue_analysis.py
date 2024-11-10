import datetime as time
from typing import List
from numpy import average
import pandas as pd
import plotly.express as px

import config as config
from data.data_loader import DataLoader
from models.model import Issue

class TimeBasedIssueAnalysis:
    """
    Implements time based issue analysis of closed
    GitHub issues and outputs the result of that analysis.
    """

    pd.options.mode.copy_on_write = True
    
    def __init__(self):
        """
        Constructor
        """
        # Parameter is passed in via command line (--user)
        self.user:str = config.get_parameter('user')
        self.label:str = config.get_parameter('label')
    
    def run(self):
        issues:List[Issue] = DataLoader().get_issues()
        open_issues = []
        closed_issues = []

        for issue in issues:
            if issue.state == 'open':
                open_issues.append(issue)
            elif issue.state == 'closed':
                closed_issues.append(issue)

        print('Number of closed issues: ', len(closed_issues))

        closed_issues_df = self.create_dataframe(closed_issues)

        if self.user != None:
            self.analyse_based_on_user(self.user, closed_issues_df)
        else:
            self.analyse_closed_issues(closed_issues_df)

    def create_dataframe(self, closed_issues):
        closed_issues_dict = dict()
        ids = []
        creators = []
        creation_times = []
        closed_times = []
        labels_list = []

        for issue in closed_issues:
            creation_time = issue.created_date
            closed_time = None
            events = issue.events
            labels = issue.labels
            for event in events:
                if event.event_type == 'closed':
                    closed_time = event.event_date
            if closed_time != None:
                ids.append(issue.number)
                creators.append(issue.creator)
                creation_times.append(creation_time)
                closed_times.append(closed_time)
                labels_list.append(str(labels))

        closed_issues_dict['issue_id'] = ids
        closed_issues_dict['creator'] = creators
        closed_issues_dict['labels'] = labels_list
        closed_issues_dict['creation_time'] = creation_times
        closed_issues_dict['closed_time'] = closed_times

        closed_issues_df = pd.DataFrame(closed_issues_dict)
        closed_issues_df['time_taken'] = closed_issues_df['closed_time'] - closed_issues_df['creation_time']

        # Calculate time difference in days
        closed_issues_df['time_diff_in_days'] = closed_issues_df['time_taken'].dt.days

        # Calculate the time difference in months
        closed_issues_df['time_diff_in_months'] = closed_issues_df['time_diff_in_days'].apply(self.get_approx_months)

        print(closed_issues_df.head())
        print()
        
        # Print the top 10 longest duration issues
        print(closed_issues_df['time_diff_in_days'].nlargest(10))

        # Print the top 10 highest number of issues assigned to a single user
        print(closed_issues_df['creator'].value_counts().nlargest(10))

        return closed_issues_df

    def analyse_closed_issues(self, closed_issues_df):
        fig = px.area(closed_issues_df[:100],
                x='creator',
                y='time_diff_in_months',
                color='time_diff_in_days',
                hover_data=['labels'],
                title='Time Taken to Close Issues')

        fig.show()

    def get_approx_months(self, time_diff):
        return int(round(time_diff / 30, 0))
    
    def analyse_based_on_user(self, user, closed_issues_df):
        # Create a dataframe with only information about the selected users
        user_df = closed_issues_df[closed_issues_df['creator'] == user]

        print(user_df)

        average_time_taken = average(user_df['time_diff_in_days'])
        print(f"The average time taken by user: {user} is {average_time_taken} days.")

        fig = px.bar(user_df,
            x='labels',
            y='time_diff_in_days',
            color='time_diff_in_days',
            title=f"Time Taken by '{user}' to Close Issues (in days)",
            labels={'time_diff_in_days':'Time Taken to Close Issues',
                    'labels': 'Issue Label'})

        fig.show()

if __name__ == '__main__':
    # Invoke run method when running this module directly
    TimeBasedIssueAnalysis().run()