from rest_framework import serializers
from . import models

class ReportSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Report
        fields = '__all__'