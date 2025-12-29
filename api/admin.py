from django.contrib import admin
from .models import ChainBlock, ChainTransaction, NGOLogin, CorporateLogin, AdminLogin, FieldOfficerLogin, IsroAdminLogin


@admin.register(ChainBlock)
class ChainBlockAdmin(admin.ModelAdmin):
	list_display = ("index", "hash", "previous_hash", "timestamp")
	readonly_fields = ("index", "hash", "previous_hash", "nonce", "timestamp", "raw")


@admin.register(ChainTransaction)
class ChainTransactionAdmin(admin.ModelAdmin):
	list_display = ("kind", "amount", "sender", "recipient", "project_id")
	readonly_fields = ("kind", "amount", "sender", "recipient", "project_id", "meta", "block")


@admin.register(NGOLogin)
class NGOLoginAdmin(admin.ModelAdmin):
	list_display = ("email",)


@admin.register(CorporateLogin)
class CorporateLoginAdmin(admin.ModelAdmin):
	list_display = ("email",)


@admin.register(AdminLogin)
class AdminLoginAdmin(admin.ModelAdmin):
	list_display = ("email",)


@admin.register(FieldOfficerLogin)
class FieldOfficerLoginAdmin(admin.ModelAdmin):
	list_display = ("email",)


@admin.register(IsroAdminLogin)
class IsroAdminLoginAdmin(admin.ModelAdmin):
	list_display = ("email",)
