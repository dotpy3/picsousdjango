from rest_framework import serializers
from core import models as core_models


class BugReportSerializer(serializers.ModelSerializer):
	class Meta:
		model = core_models.BugReport


class PeriodeTVASerializer(serializers.ModelSerializer):
	
	class Meta:
		model = core_models.PeriodeTVA


class LoginInputSerializer(serializers.Serializer):
	ticket = serializers.CharField()
	service = serializers.CharField()
