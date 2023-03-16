import configparser

def createConfig(path, imap_host, email, password, token_telegram, chat_id, db, domain):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("accounts")
    config.set("accounts", "imap", imap_host)
    config.set("accounts", "email", email)
    config.set("accounts", "password", password)
    config.set("accounts", "token_telegram", token_telegram)
    config.set("accounts", "chat_id", chat_id)
    config.set("accounts", "db", db)
    config.set("accounts", "domain", domain)
    
    with open(path, "w") as config_file:
        config.write(config_file)
