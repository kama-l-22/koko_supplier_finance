# Generated by Django 4.1.3 on 2023-01-30 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KOKO_bank_app', '0002_rename_invoice_request_approved_invoice_invoice_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='approved_invoice',
            name='Loan_id',
        ),
    ]