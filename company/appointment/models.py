from django.db import models
from django.contrib.auth.models import AbstractUser

class Masters(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, blank=True)
    telephone = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.name}'


class PriceList(models.Model):
    title = models.CharField(max_length=50)
    price = models.FloatField()
    work_time = models.TimeField()

    def __str__(self):
        return f'{self.title}'


class Appointment(models.Model):
    master = models.ForeignKey(Masters, on_delete=models.PROTECT)
    time = models.DateTimeField()
    status_appointment = (
        ('B', 'Забронировано'),
        ('F', 'Свободно'),
        ('P', 'В процессе'),
        ('W', 'Выполнено'),
    )
    status = models.CharField(max_length=1, choices=status_appointment)
    comment = models.TextField(blank=True)
    price_list = models.ForeignKey(PriceList, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f'{self.master} and {self.time}'


class Client(AbstractUser):
    telephone_number = models.CharField(max_length=12)
    mail = models.EmailField()
    discount = models.IntegerField(null=True, blank=True)
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name="Прошел активацию?")
    send_messages = models.BooleanField(default=True, verbose_name="Оповещения о записи")

    class Meta(AbstractUser.Meta):
        pass

    def __str__(self):
        return f'{self.username}'


class Basket(models.Model):
    client = models.OneToOneField(Client, on_delete=models.PROTECT)
    appointment = models.ManyToManyField(Appointment)




