# -*- coding: UTF-8 -*-

# Copyright (c) 2012-2015 Jose Antonio Chavarría
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Author: Jose Antonio Chavarría <jachavar@gmail.com>

__author__ = 'Jose Antonio Chavarría'
__license__ = 'GPLv3'

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, UserManager


class AdministrativeManager(models.Manager):
    def get_queryset(self):
        return super(AdministrativeManager, self).get_queryset().filter(
            staff_type='A'
        )


class DoctorManager(models.Manager):
    def get_queryset(self):
        return super(DoctorManager, self).get_queryset().filter(
            staff_type='D'
        )


@python_2_unicode_compatible
class Staff(AbstractUser):
    STAFF_CHOICES = (
        ('A', _('Administrative')),
        ('D', _('Doctor')),
    )

    collegiate_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_('collegiate number')
    )
    tin = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_('taxpayer Identification Number (TIN)')
    )

    last_name_optional = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name=_('last name optional')
    )

    address = models.TextField(blank=True, null=True, verbose_name=_('address'))
    phone_contact = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('phone contact')
    )

    staff_type = models.CharField(
        max_length=1,
        choices=STAFF_CHOICES,
        default='A',
        verbose_name=_('staff type')
    )

    objects = UserManager()
    doctors = DoctorManager()
    administratives = AdministrativeManager()

    def clean(self):
        super(Staff, self).clean()
        if self.staff_type == 'D' and not self.collegiate_number:
            raise ValidationError(_('Collegiate number is required for doctor'))

    def __str__(self):
        return '%s %s %s' % (
            self.first_name,
            self.last_name,
            self.last_name_optional
        )

    class Meta:
        app_label = 'medical'
        db_table = 'staff'
