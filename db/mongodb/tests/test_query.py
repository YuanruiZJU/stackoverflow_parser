from db.mongodb import posts

db_api = posts.PostDB('answer', 'java')


def test_query():
    db_api.get_all_ids()


def test_get_one_post(id):
    post = db_api.get_post_by_id(id)
    print post['body']


def get_answers_for_question(question_id):
    question_lists = list()
    question_lists.append(question_id)
    posts = db_api.get_posts_by_question_ids(question_lists)
    for p in posts:
        print p['body']
        print '---------------------------------------------'


