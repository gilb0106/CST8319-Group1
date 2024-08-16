class Branch:
    def __init__(self, branch_id, branch_name, email_address):
        self._branch_id = branch_id
        self._branch_name = branch_name
        self._email_address = email_address


    def get_branch_id(self):
        return self.branch_id

    def set_branch_id(self, branch_id):
        self._branch_id = branch_id

    def branch_name(self):
        return self._branch_name

    def set_branch_name(self, branch_name):
        self._branch_name = branch_name

    def get_email_address(self):
        return self._email_address

    def set_useremail(self, email_address):
        self._email_address = email_address
