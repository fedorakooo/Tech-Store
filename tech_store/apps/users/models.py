from django.db import models


class Users(models.Model):
    id = models.UUIDField(primary_key=True)
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    phone_number = models.CharField(unique=True, max_length=20)
    email = models.CharField(unique=True, max_length=255)
    hashed_password = models.CharField(max_length=255)
    role = models.TextField()
    is_active = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "users"


class Customers(models.Model):
    id = models.UUIDField(primary_key=True)
    user = models.OneToOneField("Users", models.DO_NOTHING)
    date_of_birth = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "customers"
