import logging
import multiprocessing
import time

import schedule

from sh8core.models import Mail


logger = logging.getLogger(__name__)


class MailDeleteBatch(multiprocessing.Process):
    def run(self):
        def delete_job():
            try:
                Mail.delete_one_day_ago()
            except:
                logger.exception("Exception raised in MailDeleteBatch#run()#delete_job()")
                raise

        schedule.every().hour.do(delete_job)

        while True:
            schedule.run_pending()
            time.sleep(1)
