from django.db import models

class Report(models.Model):
    date = models.DateField(verbose_name=u'Date')
    restaurant = models.CharField(max_length=20, verbose_name=u'Restaurant')
    planned_hours = models.IntegerField(verbose_name=u'Planned_Hours')
    actual_hours = models.IntegerField(verbose_name=u'Actual_Hours')
    budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Budget')
    sells = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=u'Sells')

    class Meta:
        verbose_name_plural = "Reports"
        db_table = 'report'

    def __str__(self):
        return self.restaurant

