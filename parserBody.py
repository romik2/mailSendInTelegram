import email, email.parser, email.policy

def header_decode(header):
    hdr = ""
    for text, encoding in email.header.decode_header(header):
        if isinstance(text, bytes):
            text = text.decode(encoding or "us-ascii")
        hdr += text
    return hdr

def msg2bodyText(msg):
    if msg.get_content_maintype() != "text":
        return None

    ddd = msg.get_content()

    if msg.get_content_subtype() == "html":
        ddd = msg.get_payload(decode=True)

    return ddd

def email2Text(rfc822mail):
        msg_data = email.message_from_bytes(rfc822mail, policy=email.policy.default)
        
        mail_value = {}

        mail_value["from"] = header_decode(msg_data.get('From'))
        mail_value["date"] = header_decode(msg_data.get('Date'))
        mail_value["subject"] = header_decode(msg_data.get('Subject'))
        
        mail_value["body"] = ""
        if msg_data.is_multipart():
            for part in msg_data.walk():
                ddd = msg2bodyText(part)
                if ddd is not None:
                    mail_value["body"] = mail_value["body"] + ddd
        else:
            ddd = msg2bodyText(msg_data)
            mail_value["body"] = ddd

        return mail_value