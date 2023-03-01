from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from store.logic import set_rating
from store.models import Book, UserBookRelation


class SetRatingTestCase(APITestCase):
    def setUp(self):
        user1 = User.objects.create(username='user1', first_name='Ivan', last_name='Petrov')
        user2 = User.objects.create(username='user2', first_name='Ivan', last_name='Sidorov')
        user3 = User.objects.create(username='user3', first_name='Ivan', last_name='Ivanov')

        self.book_1 = Book.objects.create(name='Test book 1', price=25, author_name='Author 1',
                                          discount='3.00', owner=user1)

        UserBookRelation.objects.create(user=user1, book=self.book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=self.book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=user3, book=self.book_1, like=True, rate=4)

    def test_ok(self):
        set_rating(self.book_1)
        self.book_1.refresh_from_db()
        self.assertEqual('4.67', str(self.book_1.rating))
