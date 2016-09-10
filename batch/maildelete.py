import multiprocessing
import time

import schedule

from sh8core.models import Mail


class MailDeleteBatch(multiprocessing.Process):
    def run(self):
        def delete_job():
            Mail.delete_one_day_ago()

        schedule.every().hour.do(delete_job)

        while True:
            schedule.run_pending()
            time.sleep(1)
