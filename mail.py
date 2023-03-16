import imaplib
import parserBody

def imap_connect(host, email, password):
    imap = imaplib.IMAP4_SSL(host)
    imap.login(email, password)
    return imap

def messages_list(imap):
    messages_list = []
    status, messages = imap.select("INBOX")
    retcode, messages = imap.search(None, '(UNSEEN)')

    if status != "OK": exit("Incorrect mail box")
    for num in str(messages[0]).split(' '):
        if (num != "b''"):
            f = filter(str.isdecimal, num)
            number = "".join(f)
            res, msg = imap.fetch(number, '(RFC822)')
            for response in msg:
                if isinstance(response, tuple):
                    messages_list.append(parserBody.email2Text(response[1]))

    return messages_list