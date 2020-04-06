# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TAddress(models.Model):
    consignee = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_address'


class TBookClassification(models.Model):
    level = models.IntegerField(blank=True, null=True)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    category_title = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_book_classification'


class TBooks(models.Model):
    category = models.ForeignKey(TBookClassification, models.DO_NOTHING, blank=True, null=True)
    book_name = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    publishing_time = models.DateTimeField(blank=True, null=True)
    commentnum = models.IntegerField(blank=True, null=True)
    dang_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    edition = models.IntegerField(blank=True, null=True)
    pages = models.IntegerField(blank=True, null=True)
    words = models.IntegerField(blank=True, null=True)
    printing_time = models.DateTimeField(blank=True, null=True)
    book_size = models.CharField(max_length=255, blank=True, null=True)
    paper_type = models.CharField(max_length=255, blank=True, null=True)
    impression = models.IntegerField(db_column='Impression', blank=True, null=True)  # Field name made lowercase.
    packaging_type = models.CharField(max_length=255, blank=True, null=True)
    is_set = models.IntegerField(blank=True, null=True)
    isbn = models.CharField(db_column='ISBN', max_length=255, blank=True, null=True)  # Field name made lowercase.
    advertise = models.CharField(max_length=255, blank=True, null=True)
    recommend = models.TextField(blank=True, null=True)
    content_recommendation = models.TextField(blank=True, null=True)
    about_author = models.TextField(blank=True, null=True)
    catalogue = models.TextField(blank=True, null=True)
    media_reviews = models.TextField(blank=True, null=True)
    read_online = models.TextField(blank=True, null=True)
    picture_one = models.CharField(max_length=255, blank=True, null=True)
    picture_two = models.CharField(max_length=255, blank=True, null=True)
    picture_three = models.CharField(max_length=255, blank=True, null=True)
    picture_four = models.CharField(max_length=255, blank=True, null=True)
    picture_five = models.CharField(max_length=255, blank=True, null=True)
    add_time = models.DateTimeField(blank=True, null=True)
    sales = models.IntegerField(blank=True, null=True)

    def discount(self):
        return '%.2f' %(self.dang_price / self.price *10)

    class Meta:
        managed = False
        db_table = 't_books'


class TOrder(models.Model):
    id = models.IntegerField(primary_key=True)
    order_number = models.CharField(max_length=255, blank=True, null=True)
    generated_time = models.DateTimeField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    address = models.ForeignKey(TAddress, models.DO_NOTHING, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_order'


class TOrderDetail(models.Model):
    id = models.IntegerField(primary_key=True)
    book = models.ForeignKey(TBooks, models.DO_NOTHING, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    books_number = models.IntegerField(blank=True, null=True)
    order = models.ForeignKey(TOrder, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_order_detail'


class TShoppingCart(models.Model):
    quantity = models.IntegerField(blank=True, null=True)
    book = models.ForeignKey(TBooks, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_shopping_cart'


class TUser(models.Model):
    username = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_user'
