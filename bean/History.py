class History:
    def __init__(self, history_id, book_id, user_id, action, action_date, support_message_id=None):
        self._history_id = history_id
        self._book_id = book_id
        self._user_id = user_id
        self._action = action
        self._action_date = action_date
        self._support_message_id = support_message_id

    def get_history_id(self):
        return self._history_id

    def set_history_id(self, history_id):
        self._history_id = history_id

    def get_book_id(self):
        return self._book_id

    def set_book_id(self, book_id):
        self._book_id = book_id

    def get_user_id(self):
        return self._user_id

    def set_user_id(self, user_id):
        self._user_id = user_id

    def get_action(self):
        return self._action

    def set_action(self, action):
        self._action = action

    def get_action_date(self):
        return self._action_date

    def set_action_date(self, action_date):
        self._action_date = action_date

    def get_support_message_id(self):
        return self._support_message_id

    def set_support_message_id(self, support_message_id):
        self._support_message_id = support_message_id
