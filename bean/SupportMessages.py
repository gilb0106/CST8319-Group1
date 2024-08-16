class SupportMessages:
    def __init__(self, subject, message_text, message_date):
        self._subject = subject
        self._message_text = message_text
        self._message_date = message_date
        self._support_message_id = None

    def get_subject(self):
        return self._subject

    def set_subject(self, subject):
        self._subject = subject

    def get_message_text(self):
        return self._message_text

    def set_message_text(self, message_text):
        self._message_text = message_text

    def get_message_date(self):
        return self._message_date

    def set_message_date(self, message_date):
        self._message_date = message_date

    def get_support_message_id(self):
        return self._support_message_id

    def set_support_message_id(self, support_message_id):
        self._support_message_id = support_message_id
