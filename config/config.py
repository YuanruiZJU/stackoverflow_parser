import simplejson
import os


class Config:
    def __init__(self):
        config_content = file('config.json', 'r').read()
        config = simplejson.loads(config_content)
        self.root_path = config['root-path']
        self.posts_file_path = os.path.join(config['root-path'], config['file-name'])
        self.question_dump_name = config['question-dump-name']
        self.answer_dump_name = config['answer-dump-name']
        self.__db_name_prefix = config['db-name-prefix']
        assert(os.path.exists(self.posts_file_path))
        self.__initial_path = config['required_tags_path']
        self.__questions_dir = config['questions-dir']
        self.__answers_dir = config['answers-dir']
        self.__cache_required_tags = None

    def questions_dir(self, topic):
        topic_path = os.path.join(self.root_path, topic)
        dir_path = os.path.join(topic_path, self.__questions_dir)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return dir_path

    def answers_dir(self, topic):
        topic_path = os.path.join(self.root_path, topic)
        dir_path = os.path.join(topic_path, self.__answers_dir)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return dir_path

    def db_name(self, topic):
        if topic == 'java':
            return self.__db_name_prefix
        else:
            return self.__db_name_prefix + '_' + topic

    @property
    def required_tags(self):
        if self.__cache_required_tags is not None:
            return self.__cache_required_tags
        else:
            f = open(self.__initial_path, 'r')
            tags_str = f.read()
            tags = tags_str.split('\n')
            tag_list = list()
            for t in tags:
                t = t.lstrip().rstrip()
                t.replace('\r', '')
                tag_list.append(t)
            self.__cache_required_tags = tag_list
        return self.__cache_required_tags
