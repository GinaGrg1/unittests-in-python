from unittest import TestCase
from unittest.mock import patch

import app
from blog import Blog
from post import Post


class AppTest(TestCase):
    def setUp(self) -> None:
        """
        This builtin function always runs before each tests.
        """
        blog = Blog('Test', 'Test Author')  # this will call the __repr__ function
        app.blogs = {'Test': blog}

    def test_menu_calls_create_blog(self):
        with patch('builtins.input') as mocked_input:
            with patch('app.ask_create_blog') as mocked_ask_create_blog:
                mocked_input.side_effect = ('c', 'q')  # ask_create_blog is not called so we dont need to patch the inputs from there.
                app.menu()

                mocked_ask_create_blog.assert_called()

    def test_menu_prints_prompt(self):
        # Without the return_value here, it will constantly look for inputs.
        with patch('builtins.input', return_value='q') as mocked_input:
            app.menu()

            mocked_input.assert_called_with(app.MENU_PROMPT)

    def test_menu_calls_print_blogs(self):
        with patch('app.print_blogs') as mocked_print_blogs:
            # Whenever input() is called it returns a variable q.
            with patch('builtins.input', return_value='q'):  # mocking input() so that it doesn't do anything.
                app.menu()
                mocked_print_blogs.assert_called()

    def test_print_blogs(self):
        with patch('builtins.print') as mocked_print:  # this mocked_print is going to replace the print in app.py
            app.print_blogs()
            mocked_print.assert_called_with('- Test by Test Author (0 post)')

    def test_ask_create_blog(self):
        with patch('builtins.input') as mocked_input:
            # side_effect will turn the 1st value, the 1st time it is called & 2nd value the 2nd time
            mocked_input.side_effect = ('Test', 'Test Author')
            app.ask_create_blog()

            # Testing the value of key 'Test' is not None
            self.assertIsNotNone(app.blogs.get('Test'))

    def test_ask_read_blog(self):
        """
        When the input() is called in app.py, it is going to return the value 'Test'
        def ask_read_blog():
            title = input('Enter the blog title you want to read: ')  --> title = 'Test'
            print_posts(blogs[title])                                 --> print_posts(blogs['Test'])

        """
        with patch('builtins.input', return_value='Test'):
            with patch('app.print_posts') as mocked_print_posts:
                app.ask_read_blog()

                mocked_print_posts.assert_called_with(app.blogs['Test'])

    def test_print_posts(self):
        """
        Testing to see if the print_post() is called. We call print_posts() since it calls this function.

        """
        blog = app.blogs['Test']
        blog.create_post('Test Post', 'Test Content')

        with patch('app.print_post') as mocked_print_post:
            app.print_posts(blog)

            mocked_print_post.assert_called_with(blog.posts[0])

    def test_print_post(self):
        post = Post('Post title', 'Post content')
        expected_print = '''
--- Post title ---

Post content

'''
        with patch('builtins.print') as mocked_print:
            app.print_post(post)

            mocked_print.assert_called_with(expected_print)

    def test_ask_create_post(self):
        with patch('builtins.input') as mocked_input:
            mocked_input.side_effect = ('Test', 'Test Title', 'Test Content')

            app.ask_create_post()  # call the function. This has 3 input()s

            self.assertEqual(app.blogs['Test'].posts[0].title, 'Test Title')
            self.assertEqual(app.blogs['Test'].posts[0].content, 'Test Content')









