"""Generic tests."""
import datetime

from django.test import TestCase
from django.db.utils import DataError
from django.db.utils import IntegrityError
from django.utils import timezone

from .models.image import Image
from .models.post import Post
from .models.tag import Tag


def create_tag(name, color=None):
    """Shortcut creation tags."""
    if color:
        return Tag.objects.create(
            name=name,
            color=color,
        )
    else:
        return Tag.objects.create(
            name=name,
        )


def create_image(name, image=None):
    """Shortcut creation images."""
    return Image.objects.create(
        name=name,
        image=image,
    )


def create_post(title, content=None, pub_date=None):
    """Shortcut creation images."""
    if content and pub_date:
        return Post.objects.create(
            title=title,
            content=content,
            pub_date=pub_date,
        )
    elif content and not pub_date:
        return Post.objects.create(
            title=title,
            content=content,
        )
    elif not content and pub_date:
        return Post.objects.create(
            title=title,
            pub_date=pub_date,
        )
    else:
        return Post.objects.create(
            title=title,
        )


def get_assert_attrs(exception, sql_ex=''):
    """Get a attrs for an assert with first, second and msg attrs.

    Returns a tuple (first, second, msg) for an assert with this attrs
    """
    ex_dict = {
        'not-null': 'violates not-null constraint',
        'unique': 'violates unique constraint',
    }

    def get_ex_fields():
        """Return constraint and detail of exception."""
        ex_args = exception.args[0].split('\n')
        if len(ex_args) < 2:
            ex_args.append('')
        return ex_args[0], ex_args[1]

    constraint, detail = get_ex_fields()

    return (
        (ex_dict.get(sql_ex) and ex_dict.get(sql_ex) in constraint) or False,
        (
            "Exception not expected. Validation expected '{ex_expected}' "
            "constraint, but raise '{ex}'".format(
                ex_expected=sql_ex,
                ex=constraint,
            )
        ),
    )


class TagModelTests(TestCase):
    """Test for Tag model."""

    def test_name_unique(self):
        """Name should be unique."""
        name = 'Same name'
        try:
            for i in range(2):
                create_tag(name)
        except IntegrityError as e:
            val, msg = get_assert_attrs(e, 'unique')
            self.assertTrue(val, msg)
        else:
            self.assertEqual(
                i,
                2,
                msg="It shouldn't be possible to assign the same name."
            )

    def test_name_not_null(self):
        """Name must be mandatory."""
        name = 'can be create this tag'
        was_created = create_tag(name)
        self.assertEqual(
            was_created.name,
            name,
            msg='This tag should be created.'
        )

        try:
            wrong_tag = create_tag(None)
            self.assertIs(
                wrong_tag.name,
                None,
                msg='Exception was spected. Name should have been null.',
            )
        except IntegrityError as e:
            val, msg = get_assert_attrs(e, 'not-null')
            self.assertTrue(val, msg)

    def test_color_default(self):
        """Default color must be expected."""
        expected = '#3F7C82'
        self.assertFalse(
            Tag('a tag').color != expected,
            msg='Default color not expected (Expected: {hex}).'.format(
                hex=expected
            )
        )

    def test_color_was_tiny(self):
        """Code color must be seven characters."""
        color = '#12345'
        tiny = create_tag(
            'tiny color tag',
            color
        )
        self.assertFalse(
            tiny.check_color_format(),
            "Hexadecimal '{hex}' color is wrong because is very "
            "short.".format(hex=color),
        )

    def test_color_was_big(self):
        """Code color must be seven characters."""
        color = '#1234567'
        try:
            create_tag(
                'big color tag',
                color
            )
            self.assertFalse(
                True,
                "Hexadecimal '{hex}' color shouldn't possible create it "
                "because is very long.".format(hex=color),
            )
        except DataError as e:
            pass

    def test_color_was_correctly(self):
        """Code color must be hexadecimal code and seven chars lenght."""
        color = '#ABCDEF'
        hexa = create_tag(
            'hexa color tag',
            color
        )
        self.assertTrue(
            hexa.check_color_format(),
            "Hexadecimal '{hex}' color is not hexadecimal.".format(hex=color),
        )

    def test_color_was_hexadecimal(self):
        """Code color must be hexadecimal code and seven chars lenght."""
        color = '#X1F4A6'
        tag = create_tag(
            'wrong color',
            color
        )
        self.assertFalse(
            tag.check_color_format(),
            "Hexadecimal '{hex}' format isn't correctly".format(hex=color),
        )


class ImageModelTests(TestCase):
    """Test for Image model."""

    def test_name_unique(self):
        """Name should be unique."""
        name = 'Same name'
        try:
            for i in range(2):
                create_image(name)
        except IntegrityError as e:
            val, msg = get_assert_attrs(e, 'unique')
            self.assertTrue(val, msg)
        else:
            self.assertEqual(
                i,
                2,
                msg="It shouldn't be possible to assign the same name."
            )

    def test_name_not_null(self):
        """Name must be mandatory."""
        name = 'can be create'
        was_created = create_image(name)
        self.assertEqual(
            was_created.name,
            name,
            msg='This image should be created.'
        )

        try:
            wrong_image = create_image(None)
            self.assertIs(
                wrong_image.name,
                None,
                msg='Exception was spected. Name should have been null.',
            )
        except IntegrityError as e:
            val, msg = get_assert_attrs(e, 'not-null')
            self.assertTrue(val, msg)


class PostModelTests(TestCase):
    """Test for Post model."""

    def test_title_unique(self):
        """Title should be unique."""
        title = 'Same title'
        try:
            for i in range(2):
                create_post(title)
        except IntegrityError as e:
            val, msg = get_assert_attrs(e, 'unique')
            self.assertTrue(e)
        else:
            self.assertEqual(
                i,
                2,
                msg="It shouldn't be possible to assign the same title."
            )

    def test_title_not_null(self):
        """Title must be mandatory."""
        title = 'can be create this post'
        was_created = create_post(title)
        self.assertEqual(
            was_created.title,
            title,
            msg='This post should be created.'
        )

        try:
            wrong_post = create_post(None)
            self.assertIs(
                wrong_post.title,
                None,
                msg='Exception was spected. Title should have been null.',
            )
        except IntegrityError as e:
            val, msg = get_assert_attrs(e, 'not-null')
            self.assertTrue(val, msg)

    def test_title_length(self):
        """Name must be 200 chars or less."""
        title = '0123456789'*20 + 'X'
        try:
            wrong_length = create_post(title)
            self.assertFalse(
                True,
                "Title '{title}' shouldn't possible create it "
                "because is very large".format(
                    title=wrong_length
                ),
            )
        except DataError as e:
            pass

    def test_pub_date_default_is_today(self):
        """Deafult value for pub_date should be today."""
        today = timezone.now()
        tformat = '%d%m%Y'
        future_question = create_post('a title')
        self.assertIs(
            future_question.pub_date.strftime(tformat) ==
            today.strftime(tformat), True
        )

    def test_pub_date_default_is_not_today(self):
        """Deafult value for pub_date should be today."""
        today = timezone.now() + datetime.timedelta(days=1)
        tformat = '%d%m%Y'
        future_question = create_post('a title')
        self.assertIs(
            future_question.pub_date.strftime(tformat) ==
            today.strftime(tformat), False
        )

    def test_was_published_with_future_question(self):
        """was_published() returns False for posts at the future."""
        time = timezone.now() + datetime.timedelta(days=1)
        future_question = create_post('On the future', pub_date=time)
        self.assertIs(future_question.was_published(), False)

    def test_was_published_with_recent_question(self):
        """was_published() returns True for posts at today or on past."""
        time = timezone.now() - datetime.timedelta(
            hours=23,
            minutes=59,
            seconds=59
        )
        recent_question = create_post('On the past', pub_date=time)
        self.assertIs(recent_question.was_published(), True)
