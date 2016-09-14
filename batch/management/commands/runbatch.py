from batch.maildelete import MailDeleteBatch
from abstractions.process_command import ProcessCommand


class Command(ProcessCommand):
    help = 'Run mail delete batch server.'
    process_class = MailDeleteBatch
    pid_file_name = 'runbatch.pid'
