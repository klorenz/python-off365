

class IMAP_Account:
    def __init__(self, host, username, password, port=993, use_ssl=True):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.use_ssl = use_ssl

    def __getattr__(self, name):
        if name == 'imap':
            if self.use_ssl:
            #    self.imap = imaplib.
                pass



def sync_imap_accounts(src, dest, ):
    """Sync a source imap account with a destination account.

    This is a one-way sync.
    """
