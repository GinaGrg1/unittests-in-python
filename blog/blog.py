from post import Post


class Blog:
    def __init__(self, title, author):
        self.author = author
        self.title = title
        self.posts = []

    def __repr__(self):
        return '{} by {} ({} post{})'.format(self.title,
                                             self.author,
                                             len(self.posts),
                                             's' if len(self.posts) > 1 else '')

    def create_post(self, title, content):
        self.posts.append(Post(title, content))

    def json(self):
        return {
            'title': self.title,
            'author': self.author,
            'posts': [post.json() for post in self.posts]
        }


"""
b = Blog('Test', 'Test Author')
b.create_post(b.title, 'Hello World!')

print(b.json())
{'title': 'Test', 'author': 'Test Author', 'posts': [{'title': 'Test', 'content': 'Hello World!'}]}
"""
