class Answer:
    def __init__(self, row):
        self.id = int(row.get('Id'))
        self.parent_id = int(row.get('ParentId'))
        self.creation_date = row.get('CreationDate')
        self.score = int(row.get('Score'))
        self.comment_count = int(row.get('CommentCount'))
        self.body = row.get('Body')

    def to_dict(self):
        return {
            'id': self.id,
            'parent_id': self.parent_id,
            'creation_date': self.creation_date,
            'score': self.score,
            'comment_count': self.comment_count,
            'body': self.body
        }
