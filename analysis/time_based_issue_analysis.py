import datetime as time
from typing import List
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
    
    def __init__(self):
        """
        Constructor
        """
        # Parameter is passed in via command line (--user)
        self.user:str = config.get_parameter('user')
        self.label:str = config.get_parameter('label')
    
    def run(self):
        issues:List[Issue] = DataLoader().get_issues()
        no_of_issues = len(issues)
        open_issues = []
        closed_issues = []

        for issue in issues:
            if issue.state == 'open':
                open_issues.append(issue)
            elif issue.state == 'closed':
                closed_issues.append(issue)

        if self.state == 'open':
            print('Number of open issues: ', len(open_issues))
        elif self.state == 'closed':
            print('Number of closed issues: ', len(closed_issues))
            self.track_closed_issues(closed_issues)
        else:
            print('Number of open issues: ', len(open_issues))
            print('Number of closed issues: ', len(closed_issues))


    def track_closed_issues(self, closed_issues):
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
        closed_issues_df['time_diff'] = (closed_issues_df['closed_time'] - closed_issues_df['creation_time']).dt.days

        # closed_issues_df['unique_id'] = list(pd.concat(closed_issues_df['creator'], closed_issues_df['issue_id']))

        print(closed_issues_df.head())
        print()

        closed_issues_sorted = closed_issues_df.sort_values(by='time_taken', ascending=False)

        print(closed_issues_sorted.head())
        print(closed_issues_sorted.tail())

        # scaled_df = closed_issues_df.groupby(closed_issues_df["time_taken"]).value_counts().nlargest(10)

        # print(scaled_df.head())

        # Scatter plot for danceability vs streams
        # fig = px.area(closed_issues_df,
        #                 x='creator',
        #                 y='time_taken',
        #                 color='time_diff',
        #                 hover_data=['issue_id', 'creator'],
        #                 title='Time Taken to Close Issues',
        #                 labels={'time_taken':'Time Taken'}
        # )

        # fig = px.bar(closed_issues_sorted[:100],
        #                 x='unique_id',
        #                 y='time_taken',
        #                 color='time_taken',
        #                 hover_data=['issue_id', 'creator', 'time_diff'],
        #                 title='Time Taken to Close Issues',
        #                 color_continuous_scale='Plasma',
        #                 labels={'time_taken':'Time Taken'}
        # )

        # fig.show()

        # Identify duplicates
        duplicates = closed_issues_sorted.duplicated(keep=False)

        # Create new dataframe with duplicates
        df_duplicates = closed_issues_sorted[duplicates].copy()

        df = closed_issues_sorted.drop_duplicates(subset=['creator'], keep='first')

        print(df['time_diff'].value_counts().nlargest(10))

        df['time_diff_in_months'] = df['time_diff'] / 30

        # print(df_duplicates)

        # fig = px.bar(df,
        #         x='creator',
        #         y='time_taken',
        #         color='time_diff',
        #         hover_data=['issue_id', 'creator', 'time_diff'],
        #         title='Time Taken to Close Issues',
        #         color_continuous_scale='Plasma')

        # fig.show()

        # fig = px.scatter(closed_issues_df,
        #         x='creator',
        #         y='time_taken',
        #         color='time_diff',
        #         hover_data=['issue_id', 'creator'],
        #         title='Time Taken to Close Issues',
        #         color_continuous_scale='Plasma')

        # fig.show()

        fig = px.area(df,
                x='creator',
                y='time_diff_in_months',
                color='time_diff_in_months',
                hover_data=['labels'],
                title='Time Taken to Close Issues')

        fig.show()

if __name__ == '__main__':
    # Invoke run method when running this module directly
    TimeBasedIssueAnalysis().run()