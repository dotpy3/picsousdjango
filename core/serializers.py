# -*- coding: utf-8 -*-

from rest_framework import serializers
from core import models as core_models


class BugReportSerializer(serializers.ModelSerializer):
	# Serializer du bug report
	class Meta:
		model = core_models.BugReport


class PeriodeTVASerializer(serializers.ModelSerializer):
	# Serializer de la periode de TVA
	class Meta:
		model = core_models.PeriodeTVA


class UserRightSerializer(serializers.ModelSerializer):
	# Serializer des droits utilisateurs
	class Meta:
		model = core_models.UserRight


class LoginInputSerializer(serializers.Serializer):
	# Serializer d'input de la requête de login.
	ticket = serializers.CharField()
	service = serializers.CharField()
