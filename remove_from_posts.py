from db.mongodb.posts import PostDB
import re


formal_code_str_l1 = [r'<pre.*?>\s*?\n*?<code>(.*?\n)*?.*?</code>[\s\n]*</pre>',
                      r'<pre.*?>\s*?\n*?<code>(.*?\n)*?.*?</pre>[\s\n]*</code>',
                      r'<code>\s*?\n*?<pre.*?>(.*?\n)*?.*?</pre>[\s\n]*</code>',
                      r'<code>\s*?\n*?<pre.*?>(.*?\n)*?.*?</code>[\s\n]*</pre>']

formal_code_pattern_l2 = re.compile(r'<pre.*?>(.*?\n)*?.*</pre>', re.IGNORECASE)
formal_img_pattern = re.compile(r'<img.*?src=.*?>', re.IGNORECASE)

informal_code_strs = [
    # r'package\s*\S+;'
    # r'import\s*\S+;',
    # r'(public|private|protected)\s+(abstract\s+)?class.*{',
    # r'\n\s*(public|private|protected)\s+(static\s+|abstract\s+)?\S+\s+\S+(.*).*{',
    # r'\n\s*(if|for|while)\s*(.*)\s*\n*{.*}',
    # r'(<p>|\n)catch\s*\n?\s*{',
    # r'(<p>|\n)try\s?\n?{',
    # r'(<p>|\n).*?=.*?;(</p>|\n)',
    # r'(<p>|\n)\s*(\S+\.)*\S+(.*);(</p>|\n)'
]

formal_code_patterns = list()
for reg_str in formal_code_str_l1:
    formal_code_patterns.append(re.compile(reg_str, re.IGNORECASE))

re_code_patterns = list()
for reg_str in informal_code_strs:
    re_code_patterns.append(re.compile(reg_str))


def contain_code(body):
    for rep in formal_code_patterns:
        if rep.search(body) is not None:
            return True

    for rep in re_code_patterns:
        if rep.search(body) is not None:
            return True
    return False


def contain_img(body):
    if formal_img_pattern.search(body) is not None:
        return True
    return False


def contain_informal_code(body):
    for rep in re_code_patterns:
        if rep.search(body) is not None:
            return True
    return False


def remove_code_from_body(body):
    removed_body = body
    for rep in formal_code_patterns:
        removed_body = rep.sub('', removed_body)
    return removed_body


def remove_code_l2_from_body(body):
    return formal_code_pattern_l2.sub('', body)


def remove_code_by_informal_patterns(body):
    pass


def remove_img_from_body(body):
    return formal_img_pattern.sub('', body)


def analyze_posts_body(post_type):
    db_api = PostDB(post_type, 'java')
    ids = db_api.get_all_ids()
    print 'all ids got'
    print len(ids)
    slice_start = 0
    i = 0
    posts_num = len(ids)
    while slice_start < posts_num:
        print i
        slice_end = slice_start + 10000
        if slice_end > posts_num:
            slice_end = posts_num
        slice_ids = ids[slice_start:slice_end]
        db_api = PostDB(post_type, 'java')
        posts = db_api.get_posts_from_ids(slice_ids)

        db_obj_lists = list()

        for p in posts:
            body = p['body']
            removed_body = remove_code_from_body(body)
            removed_body = remove_code_l2_from_body(removed_body)
            removed_body = remove_img_from_body(removed_body)
            new_p = p
            new_p['body'] = removed_body
            db_obj_lists.append(new_p)

        db_api2 = PostDB(post_type)
        db_api2.insert(db_obj_lists)
        slice_start = slice_end
        i += 1


if __name__ == '__main__':
    analyze_posts_body('answer')
    analyze_posts_body('question')
