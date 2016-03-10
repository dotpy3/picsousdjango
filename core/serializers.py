from rest_framework import serializers
from core import models as core_models


class BugReportSerializer(serializers.Serializer):
	class Meta:
		model = core_models.BugReport


class PeriodeTVASerializer(serializers.Serializer):
	
	class Meta:
		model = core_models.PeriodeTVA


class LoginInputSerializer(serializers.Serializer):
	ticket = serializers.CharField()
	service = serializers.CharField()
