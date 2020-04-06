from home.models import TBooks


class Car:
    def __init__(self):
        self.book_items = []  # 用来存储书  容器

    def add_book(self, book_id, number=1):
        book = self.get_book(book_id)
        if book:
            book.book_number += number
            book.total_price = book.book_number * book.book_price
        else:
            book = Book(book_id, number)
            self.book_items.append(book)

    def del_book(self, book_id):
        book = self.get_book(book_id)
        if book:
            self.book_items.remove(book)

    def reduce_book(self, book_id, number=1):
        book = self.get_book(book_id)
        if book:
            book.book_number -= number
            book.total_price = book.book_number * book.book_price

    def get_book(self, book_id):
        for book in self.book_items:
            if book_id == book.book_id:
                return book

    def add_shopping_car(self, book_id, number):
        """
        将购物车中的商品添加到用户的购物车中
        :param book_id: 获取书籍id
        :param user_id: 获取用户id
        :return:
        """
        book = Book(book_id, number)
        self.book_items.append(book)


class Book:
    def __init__(self, book_id, number):
        book = TBooks.objects.filter(id=book_id)[0]
        self.book_id = book.id
        self.book_name = book.book_name
        self.book_price = book.dang_price
        self.book_picture = book.picture_one
        self.book_number = number
        self.total_price = self.book_price * self.book_number
        self.publisher = book.publisher
