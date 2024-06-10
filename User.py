class User:
    def __init__(self, user_id, username, first_name, last_name):
        self.user_id = user_id
        self.username = username
        self.name = (first_name + ' ' + last_name).strip()
        self.num_of_comments = 0
        self.num_of_reactions = 0
        self.num_of_all_activities = 0

    def display_info(self):
        return [self.user_id, self.username, self.name, str(self.num_of_comments), str(self.num_of_reactions)]


