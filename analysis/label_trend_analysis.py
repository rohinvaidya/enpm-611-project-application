from typing import List, Dict
import matplotlib.pyplot as plt
import pandas as pd
import math

from data.data_loader import DataLoader
from models.model import Issue

class LabelTrendAnalysis:
    """
    Analyzes the trend of label usage over time.
    Outputs the findings to standard out and generates a line chart for top labels.
    """

    def run(self):
        issues: List[Issue] = DataLoader().get_issues()

        # Dictionary to hold label usage per month
        label_trend: Dict[str, Dict[str, int]] = {}

        for issue in issues:
            created_month = issue.created_date.strftime('%Y-%m') if issue.created_date else None
            if not created_month:
                continue  # Skip if creation date is missing

            for label in issue.labels:
                if label not in label_trend:
                    label_trend[label] = {}
                if created_month not in label_trend[label]:
                    label_trend[label][created_month] = 0
                label_trend[label][created_month] += 1

        # Calculate total label usage to identify top labels
        total_label_usage = {label: sum(months.values()) for label, months in label_trend.items()}
        top_labels = sorted(total_label_usage, key=total_label_usage.get, reverse=True)[:5]  # Top 5 labels

        # Filtering label_trend to include only top labels
        top_label_trend = {label: label_trend[label] for label in top_labels}

        # Converting the nested dictionary to a DataFrame
        df_dict = {}
        for label, months in top_label_trend.items():
            df_dict[label] = months
        df = pd.DataFrame(df_dict).fillna(0)
        df_sorted = df.sort_index()

        # Output to standard out
        print("Label Trend Over Time (Top 5 Labels):")
        print(df_sorted.to_string())

        # Prepare for plotting
        months = df_sorted.index.tolist()
        num_months = len(months)

        # Determine the step for displaying labels to reduce clutter
        step = max(1, math.ceil(num_months / 24))  # max is there to insure that the step is never less than 1

        # Generate Line Chart for Top Labels
        plt.figure(figsize=(16, 9))
        for label in df_sorted.columns:
            plt.plot(df_sorted.index, df_sorted[label], label=label)

        plt.xlabel('Month')
        plt.ylabel('Number of Labels Added')
        plt.title('Trend of Top 5 Label Usage Over Time')

        plt.xticks(ticks=range(0, num_months, step), labels=[months[i] for i in range(0, num_months, step)], rotation=45, ha='right')

        plt.legend(title='Labels', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()



if __name__ == '__main__':
    # Invoke run method when running this module directly
    LabelTrendAnalysis().run()