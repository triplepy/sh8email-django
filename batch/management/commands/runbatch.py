from abstractions.process_command import ProcessCommand
from batch.maildelete import MailDeleteBatch


class Command(ProcessCommand):
    help = 'Run mail delete batch server.'
    process_class = MailDeleteBatch
    pid_file_name = 'runbatch.pid'
