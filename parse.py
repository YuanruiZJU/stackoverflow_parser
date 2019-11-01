from config import conf
from lxml import etree
import serialize
import os
from obj import question
from obj import answer
from db.mongodb import posts


path = conf.posts_file_path


def get_all_tags():
    context = etree.iterparse(path, events=('end',), tag='row')
    j = 0
    new_f = open(conf.tags_path, 'w')
    tag_frequency_dict = dict()
    initial_tag_set = conf.required_tags()
    for event, row in context:
        if event == 'end' and row.tag == 'row':
            post_id = row.get('Id')
            print post_id
            post_type = row.get('PostTypeId')
            if post_type == '1':
                tags = row.get('Tags')
                for tag in initial_tag_set:
                    tag_str = '<' + tag + '>'
                    if tag_str in tags:
                        real_tags = tags.split('>')[:-1]
                        for t in real_tags:
                            try:
                                tag_frequency_dict[t[1:]] += 1
                            except KeyError:
                                tag_frequency_dict[t[1:]] = 1
                        j += 1
                        break
        row.clear()
        while row.getprevious() is not None:
            del row.getparent()[0]
    del context
    sorted_dict = sorted(tag_frequency_dict.items(), key=lambda x:x[1], reverse=True)
    serialize.dump_obj('tags_dict3', tag_frequency_dict)
    new_f.write(str(sorted_dict))
    new_f.close()
    print j


def get_all_questions(topic):
    context = etree.iterparse(path, events=('end',), tag='row')
    j = 0
    questions = []
    required_tags = conf.required_tags
    for event, row in context:
        
        if event == 'end' and row.tag == 'row':
            post_id = row.get('Id')
            print post_id
            post_type = row.get('PostTypeId')
            if post_type == '1':
                tags = row.get('Tags')
                for tag in required_tags:
                    tag_str = '<' + tag + '>'
                    if tag_str in tags:
                        j += 1
                        questions.append(int(post_id))
                        if j % 10000 == 0:
                            questions_path = os.path.join(conf.questions_dir(topic),
                                                          conf.question_dump_name + '-' + str(j/10000))
                            serialize.dump_obj(questions_path, questions)
                            questions = list()
                        break

        row.clear()
        while row.getprevious() is not None:
            del row.getparent()[0]
    del context
    if len(questions) > 0:
        questions_path = os.path.join(conf.questions_dir(topic),
                                       conf.question_dump_name + '-' + str(j/10000 + 1))
        serialize.dump_obj(questions_path, questions)
    print j


def get_all_questions_from_files(topic):
    questions_dir = conf.questions_dir(topic)
    filename_list = os.listdir(questions_dir)
    assert (len(filename_list) > 0)
    questions = list()
    for name in filename_list:
        path = os.path.join(questions_dir, name)
        questions += serialize.load_dump(path)
    return questions


def get_all_answers(topic):
    questions_set = set(get_all_questions_from_files(topic))
    context = etree.iterparse(path, events=('end',), tag='row')
    j = 0
    answers = []
    for event, row in context:
        if event == 'end' and row.tag == 'row':
            post_id = row.get('Id')
            print post_id
            post_type = row.get('PostTypeId')
            if post_type == '2':
                parent_id = int(row.get('ParentId'))
                if parent_id in questions_set:
                    j += 1
                    answers.append(int(post_id))
                    if j % 10000 == 0:
                        answers_path = os.path.join(conf.answers_dir(topic),
                                                    conf.answer_dump_name + '-' + str(j/10000))
                        serialize.dump_obj(answers_path, answers)
                        answers = list()

        row.clear()
        while row.getprevious() is not None:
            del row.getparent()[0]
    del context
    if len(answers) > 0:
        answers_path = os.path.join(conf.answers_dir(topic),
                                    conf.answer_dump_name + '-' + str(j/10000 + 1))
        serialize.dump_obj(answers_path, answers)
    print j


def get_all_answers_from_files(topic):
    answers_dir = conf.answers_dir(topic)
    filename_list = os.listdir(answers_dir)
    assert(len(filename_list) > 0)
    answers = list()
    for name in filename_list:
        path = os.path.join(answers_dir, name)
        answers += serialize.load_dump(path)
    return answers


def store_question_to_db(topic):
    questions_set = set(get_all_questions_from_files(topic))
    context = etree.iterparse(path, events=('end',), tag='row')
    question_posts = list()
    for event, row in context:
        if event == 'end' and row.tag == 'row':
            post_id = int(row.get('Id'))
            print post_id
            if post_id in questions_set:
                qs = question.Question(row)
                question_posts.append(qs.to_dict())
                if len(question_posts) % 10000 == 0:
                    print 'start store db'
                    pdb = posts.PostDB('question', topic)
                    pdb.insert(question_posts)
                    question_posts = list()
        row.clear()
        while row.getprevious() is not None:
            del row.getparent()[0]
    del context
    if len(question_posts) > 0:
        pdb = posts.PostDB('question', topic)
        pdb.insert(question_posts)


def store_answer_to_db(topic):
    answers_set = set(get_all_answers_from_files(topic))
    context = etree.iterparse(path, events=('end',), tag='row')
    answer_posts = list()
    for event, row in context:
        if event == 'end' and row.tag == 'row':
            post_id = int(row.get('Id'))
            print post_id
            if post_id in answers_set:
                ans = answer.Answer(row)
                answer_posts.append(ans.to_dict())
                if len(answer_posts) % 10000 == 0:
                    print 'start store db'
                    pdb = posts.PostDB('answer', topic)
                    pdb.insert(answer_posts)
                    answer_posts = list()
        row.clear()
        while row.getprevious() is not None:
            del row.getparent()[0]
    del context
    if len(answer_posts) > 0:
        pdb = posts.PostDB(topic, 'answer')
        pdb.insert(answer_posts)

if __name__ == '__main__':
    get_all_questions('android')
    get_all_answers('android')
    # store_question_to_db('android')
    # store_answer_to_db('android')



