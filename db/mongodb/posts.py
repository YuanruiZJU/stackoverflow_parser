from db.mongodb import client
from config import conf


class PostDB:
    """
    For questions, there are five attributes:
    * id
    * answer_count
    * tags
    * title
    * body
    For answers, there are four attributes:
    * id
    * question_id
    * body
    """

    def __init__(self, post_type, topic=None):
        if topic is not None:
            db = getattr(client, conf.db_name(topic))
        else:
            db = getattr(client, conf.clean_db_name)
        self.post_type = post_type
        self.table = db[post_type]
        print post_type

    def insert(self, qa_dicts):
        assert(isinstance(qa_dicts, list))
        self.table.insert(qa_dicts)

    def get_post_by_id(self, idx):
        return self.table.find_one({'id': idx})

    def get_all_ids(self):
        ret_ids = list()
        for idx in self.table.find({}, {'id': 1, '_id': 0}):
            ret_ids.append(idx['id'])
        return ret_ids

    def get_posts_from_ids(self, ids):
        posts = self.table.find({'id': {'$in': ids}})
        return posts

    def get_posts_by_question_ids(self, ids):
        assert(self.post_type == 'answer')
        posts = self.table.find({'question_id': {'$in': ids}})
        return posts

