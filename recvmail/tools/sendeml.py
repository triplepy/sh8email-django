import sys
import os.path
import smtplib

if len(sys.argv) <= 2:
    print('Usage:')
    print('  $ python ' + sys.argv[0] + ' mailfrom rcptto <emlfile>')
    print
    print('Parameter:')
    print('  mailfrom: MAIL FROM address.')
    print('  rcptto:   RCPT TO address.')
    print('  emlfile:  Message file in eml format. When emlfile is not specified, an empty message will be send.')
    print
    print('Example:')
    print('  $ python ' + sys.argv[0] + ' mailfrom@example.com rcptto@example.com mail.eml')
    sys.exit(0)

server = 'localhost'
port = 25
mailfrom = sys.argv[0]
rcptto = sys.argv[1].split(',')

message = ''
if len(sys.argv) >= 4:
    filename = sys.argv[3]
    if not os.path.isfile(filename):
        print('File "' + filename + '" not found.')
        sys.exit(0)
    with open(filename) as f:
        message = f.read()

smtp = None
try:
    smtp = smtplib.SMTP(server, port)
    smtp.sendmail(mailfrom, rcptto, message)
except Exception as e:
    print('Failed to send mail.')
    print(str(e))
else:
    print('Succeeded to send mail.')
finally:
    if smtp is not None:
        smtp.close()
