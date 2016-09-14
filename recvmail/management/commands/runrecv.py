from abstractions.process_command import ProcessCommand
from recvmail.recv_server import Sh8MailProcess


class Command(ProcessCommand):
    help = 'Run mail receiving server.'
    process_class = Sh8MailProcess
    pid_file_name = 'runrecv.pid'
