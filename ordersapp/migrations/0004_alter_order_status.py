# Generated by Django 3.2.7 on 2021-11-13 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordersapp', '0003_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('FM', 'формируется'), ('STP', 'отправлен на обработку'), ('PD', 'оплачено'), ('PRD', 'обрабатывается'), ('RDY', 'готов к выдаче'), ('CNC', 'отмена заказа')], default='FM', max_length=3, verbose_name='статус'),
        ),
    ]
