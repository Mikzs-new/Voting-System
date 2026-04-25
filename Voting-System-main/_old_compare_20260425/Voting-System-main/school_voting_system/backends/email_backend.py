import ssl

from django.core.mail.backends.smtp import EmailBackend as SMTPBackend
from django.utils.functional import cached_property

class EmailBackend(SMTPBackend):
    @cached_property
    def ssl_context(self):
        if self.ssl_certfile or self.ssl_keyfile:
            self.ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
            self.ssl_context.load_cert_chain(self.ssl_certfile, self.ssl_keyfile)
            return self.ssl_context
        else:
            self.ssl_context = ssl.create_default_context()
            self.ssl_context.check_hostname = False
            self.ssl_context.verify_mode = ssl.CERT_NONE
            return self.ssl_context