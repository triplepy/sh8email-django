import os.path
import smtplib
import sys

if len(sys.argv) <= 2:
    print('Usage:')
    print('  $ python ' + sys.argv[0] + ' mailfrom rcptto <emlfile>')
    print
    print('Parameter:')
    print('  mailfrom: MAIL FROM address.')
    print('  rcptto:   RCPT TO address.')
    print('  emlfile:  Message file in eml format. When emlfile is not specified, an empty message will be send.')
    print('  port:     Port of SMTP server that would recieve the email. Optional. Default is 25.')
    print
    print('Example:')
    print('  $ python ' + sys.argv[0] + ' mailfrom@example.com rcptto@example.com mail.eml 2525')
    sys.exit(0)

server = 'localhost'
mailfrom = sys.argv[1]
rcptto = sys.argv[2].split(',')
try:
    port = sys.argv[3]
except IndexError:
    port = 25

message = ''
if len(sys.argv) >= 5:
    filename = sys.argv[4]
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
