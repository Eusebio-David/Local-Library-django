from django.contrib import admin
from .models import Book, Author, BookInstance, Language, Genre

# Register your models here.
class BoooksInstanceInline(admin.TabularInline):
    model = BookInstance

    #Especifica la cantidad de formularios adicionales
    #Si no hay objeto muestra dos de lo contrario 0
    def get_extra(self, request, obj=None, **kwargs):
        extra = 2
        if obj:
            return extra -2
        return extra

class BookInline(admin.TabularInline):
    model = Book
     #Especifica la cantidad de formularios adicionales
    #Si no hay objeto muestra dos de lo contrario 0
    def get_extra(self, request, obj=None, **kwargs):
        extra = 2
        if obj:
            return extra -2
        return extra

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name', 'date_of_birth', 'date_of_death')
    inlines = [BookInline]
    fields = ['first_name', 'last_name', ('date_of_birth',
                                        'date_of_death')]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

    inlines = [BoooksInstanceInline]

  

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    list_display = ('book','status','due_back','id')
    fieldsets = (
        (None,{
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        })
    )

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass

