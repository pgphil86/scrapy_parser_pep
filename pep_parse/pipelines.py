import csv
import datetime as dt
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:
    """
    PEP documents with different statuses are summarized.
    At the end, a csv file is created.
    """
    def open_spider(self, spider):
        """
        Creating a dictionary.
        """
        self.status_count = defaultdict(int)

    def process_item(self, item, spider):
        """
        PEP account in different statuses.
        """
        self.status_count[item['status']] += 1
        return item

    def close_spider(self, spider):
        """
        Creating a csv file.
        """
        time_now = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = BASE_DIR / 'results' / f'status_summary_{time_now}.csv'
        heading = ('Статус', 'Количество')
        total = 'Total'
        with open(filename, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows([
                heading,
                *self.status_count.items(),
                [total, sum(self.status_count.values())]
            ])
