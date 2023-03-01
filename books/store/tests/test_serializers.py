from django.contrib.auth.models import User
from django.db.models import Count, Case, When, F
from rest_framework.test import APITestCase

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BookSerializerTestCase(APITestCase):
    def test_ok(self):
        user1 = User.objects.create(username='user1', first_name='Ivan', last_name='Petrov')
        user2 = User.objects.create(username='user2', first_name='Ivan', last_name='Sidorov')
        user3 = User.objects.create(username='user3', first_name='Ivan', last_name='Ivanov')

        book_1 = Book.objects.create(name='Test book 1', price=25, author_name='Author 1',
                                     discount='3.00', owner=user1)
        book_2 = Book.objects.create(name='Test book 2', price=55, author_name='Author 2',
                                     discount='2.00')

        UserBookRelation.objects.create(user=user1, book=book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=user3, book=book_1, like=True, rate=4)

        UserBookRelation.objects.create(user=user1, book=book_2, like=True, rate=3)
        UserBookRelation.objects.create(user=user2, book=book_2, like=True, rate=4)
        UserBookRelation.objects.create(user=user3, book=book_2, like=False)

        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            price_discount=F('price') - F('discount'),
            owner_name=F('owner__username')
        ).prefetch_related('readers').order_by('id')
        data = BooksSerializer(books, many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test book 1',
                'price': '25.00',
                'author_name': 'Author 1',
                'annotated_likes': 3,
                'rating': '4.67',
                'discount': '3.00',
                'price_discount': '22.00',
                'owner_name': 'user1',
                'readers': [
                    {
                        "first_name": "Ivan",
                        "last_name": "Petrov"
                    },
                    {
                        "first_name": "Ivan",
                        "last_name": "Sidorov"
                    },
                    {
                        "first_name": "Ivan",
                        "last_name": "Ivanov"
                    },
                ]
            },
            {
                'id': book_2.id,
                'name': 'Test book 2',
                'price': '55.00',
                'author_name': 'Author 2',
                'annotated_likes': 2,
                'rating': '3.50',
                'discount': '2.00',
                'price_discount': '53.00',
                'owner_name': None,
                'readers': [
                    {
                        "first_name": "Ivan",
                        "last_name": "Petrov"
                    },
                    {
                        "first_name": "Ivan",
                        "last_name": "Sidorov"
                    },
                    {
                        "first_name": "Ivan",
                        "last_name": "Ivanov"
                    },
                ]
            }
        ]
        self.assertEqual(expected_data, data)
