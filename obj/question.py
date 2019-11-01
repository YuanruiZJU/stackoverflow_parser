class Question:
    def __init__(self, row):
        self.id = int(row.get('Id'))
        self.creation_date = row.get('CreationDate')
        self.score = int(row.get('Score'))
        if row.get('AcceptedAnswerId') is not None:
            self.accepted_answer_id = int(row.get('AcceptedAnswerId'))
        else:
            self.accepted_answer_id = None
        self.view_count = row.get('ViewCount')
        self.tags = row.get('Tags')
        self.title = row.get('Title')
        self.body = row.get('Body')
        self.answer_count = int(row.get('AnswerCount'))
        self.comment_count = row.get('CommentCount')
        self.favorite_count = row.get('FavoriteCount')

    def to_dict(self):
        return {
            'id': self.id,
            'creation_date': self.creation_date,
            'score': self.score,
            'accepted_answer_id': self.accepted_answer_id,
            'view_count': self.view_count,
            'tags': self.tags,
            'title': self.title,
            'body': self.body,
            'answer_count': self.answer_count,
            'comment_count': self.comment_count,
            'favorite_count': self.favorite_count
        }
