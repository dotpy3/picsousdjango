from rest_framework import serializers
from core import models as core_models


class BugReportSerializer(serializers.Serializer):
	class Meta:
		model = core_models.BugReport


class PeriodeTVASerializer(serializers.Serializer):
	debut = serializers.DateField()
	fin = serializers.DateField()
	state = serializers.CharField()
	class Meta:
		model = core_models.PeriodeTVA
		fields = ('debut', 'fin', 'state')


class LoginInputSerializer(serializers.Serializer):
	ticket = serializers.CharField()
	service = serializers.CharField()
