class User:
    def __init__(self, userid, username, password, useremail, userphone, role):
        self._username = username
        self._password = password
        self._userid = userid
        self._user_email = useremail
        self._user_phone = userphone
        self._role = role

    def get_userid(self):
        return self._userid

    def set_userid(self, userid):
        self._userid = userid

    def get_useremail(self):
        return self._user_email

    def set_username(self, username):
        self._username = username

    def get_username(self):
        return self._username

    def set_useremail(self, useremail):
        self._user_email = useremail

    def get_userphone(self):
        return self._user_phone

    def set_userphone(self, userphone):
        self._user_phone = userphone

    def get_role(self):
        return self._role

    def set_role(self, role):
        self._role = role
