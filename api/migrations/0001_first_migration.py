# Generated by Django 3.1 on 2020-08-24 11:16

import api.state_machine
import api.validators
from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_score', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000)])),
                ('max_score', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000)])),
                ('terms', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('percentage', models.DecimalField(decimal_places=3, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0'))])),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('cpf', models.CharField(max_length=11, validators=[api.validators.validate_cpf])),
                ('birthdate', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6, validators=[api.validators.validate_amount])),
                ('score', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000)])),
                ('commitment', models.DecimalField(decimal_places=2, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01')), django.core.validators.MaxValueValidator(Decimal('0.99'))])),
                ('terms', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('income', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('1'))])),
                ('refused_policy', models.CharField(choices=[('age', 'age'), ('score', 'score'), ('commitment', 'commitment')], default=None, max_length=30, null=True)),
                ('result', models.CharField(choices=[('approved', 'approved'), ('refused', 'refused')], default=None, max_length=30, null=True)),
                ('state', models.CharField(choices=[('processing_age', 'processing_age'), ('processing_score', 'processing_score'), ('processing_commitment', 'processing_commitment'), ('approved', 'approved'), ('refused', 'refused')], default='processing_age', max_length=30)),
                ('status', models.CharField(choices=[('processing', 'processing'), ('completed', 'completed')], default='processing', max_length=30)),
            ],
            bases=(models.Model, api.state_machine.LoanStateMachine),
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('loan', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, primary_key=True, related_name='proposal', serialize=False, to='api.loan')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6, validators=[api.validators.validate_amount])),
                ('terms', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('age', 'age'), ('score', 'score'), ('commitment', 'commitment')], max_length=30)),
                ('failed', models.BooleanField(default=False)),
                ('response', models.TextField()),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='policies', to='api.loan')),
            ],
        ),
    ]
