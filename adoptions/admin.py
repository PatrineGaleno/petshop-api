from django.contrib import admin
from .models import Species, Pet, Adoption


admin.site.register(Species)
admin.site.register(Pet)

@admin.register(Adoption)
class AdoptionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    
    def get_readonly_fields(self, request, obj = ...):
        if obj and obj.status == 'P':
            return ['pet', 'customer', 'solicitation_date']        
        return ['pet', 'customer', 'solicitation_date', 'status']
    
    def save_model(self, request, obj, form, change):
        if not change:
            return super().save_model(request, obj, form, change)
        
        old_adoption = Adoption.objects.filter(id=obj.id).first()
            
        if old_adoption is None:
            return super().save_model(request, obj, form, change)

        if old_adoption.status == 'A':
            obj.status = 'A'
            return super().save_model(request, obj, form, change)

        if old_adoption.status == 'R':
            obj.status = 'R'
            return super().save_model(request, obj, form, change)
            
        if old_adoption.status == 'P' and obj.status == 'A':
            obj.pet.status = 'C'
            obj.pet.save()
            return super().save_model(request, obj, form, change)

        return super().save_model(request, obj, form, change)
