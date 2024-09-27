from django.db import models
from django.urls import reverse
"""
    Se utiliza UniqueContraint para definir restricciones a nivel de base de datos
    en uno o mas campos de un modelo.
    Asegura que los valores de esos campos sean unicos en la tabla

    ¿Qué hace? - si aplicas UniqueConstraint a un solo campo, aseguras que no haya dos registros iguales en la tabla. Si lo aplicas a varios campos, se asegura que la combinacion de esos campos sea única

    Ejemplo: Tenemos un modelo Persona y quieres asegurarte de que no haya dos personas con el mismo correo electrónico
    

        class Persona(models.Model):
            nombre = models.CharField(max_length=100)
            email = models.EmailField()

        class Meta:
            constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email')
            ]
    ¿Por qué es útil? 
    Para la integridad de los datos: preveniendo duplicados
    Para la Lógico de negocio
"""
from django.db.models import UniqueConstraint 
"""
    En Django, el término "functions" generalmente se refiere a las funciones de base de datos que puedes usar en consultas para realizar operaciones específicas sobre los datos.
    -¿Qué son las funciones de base de datos en Django?-
    Las funciones de base de datos en Django son clases que representan funciones SQL que se pueden utilizar dentro de las consultas ORM. Están disponibles en django.db.models.functions y puedes usarlas para realizar cálculos y transformaciones de datos en la base de datos sin tener que traer los datos a Python.
    
    ¿Por qué usar funciones de base de datos?
    Eficiencia: Al realizar operaciones directamente en la base de datos, reduces la cantidad de datos que necesitas traer a tu aplicación y procesar en Python.

    Poder: Puedes realizar operaciones complejas en consultas de base de datos que, de otro modo, requerirían múltiples pasos en Python.

    Flexibilidad: Te permiten realizar operaciones y transformaciones dinámicas sobre los datos en tiempo de consulta, haciendo tu código más limpio y manejable.
"""
from django.db.models.functions import Lower
import uuid
from django.conf import settings
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Genre(models.Model):
    #Representamos el genero de un libro
    name = models.CharField(max_length=200, unique=True, help_text="Enter a book genre (e.g. Science Fiction, French Poetry, etc.)")
    

    def __str__(self):
        #String para representar el modelo del objecto
        return self.name
    
    def get_absolute_url(self):
        #Retorna la url para acceder a un género en particular
        return reverse("genre_detail", args=[str(self.id)])
    
    class Meta:
        constraints =[
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_unique',
                violation_error_message = 'Genre already exists (case insensitive match)'
            ),
        ]
class Language(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text="Enter the book's natural language (e.g. English, French, Spanish, etc.)")
    
    def get_absolute_url(self):
        return reverse("language_detail", args=[str(self.id)])
    
    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message=" Language already exists (case insensitive math)"
            ),
        ]
    

class Book(models.Model):
    #Representamos el modelo de un libro 
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)
    #Usamos una foreignKey porque el libro solo puede tener un autor, pero el autor puede tener varios libros

    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
    
    #Se usa ManyToManyField porque los géneros pueden contener muchos libros, los libros pueden cubrir muchos géneros 

    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['title', 'author']
    
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.id)])
    
      
    def display_genre(self):
        """
        Crea un string para el género. Esto es requerido para mostrar el genero en el panel de administracion de django. 
        """
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    """
        short_description se utiliza para cambiar el nombre de un método o campo calculado en el panel de administración de Django.
        Hace que los nombres sean más legibles y fáciles de entender para los administradores del sitio.
    """
    display_genre.short_description = "Genre"
    
class BookInstance(models.Model):
    """
        El modelo representa una copia de un libro (i.e.) puede ser prestado de la libreria
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique Id for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    #Fecha (en la que se espera que el libro esté disponible después de haber sido prestado o en mantenimiento).
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )   

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m',
                              help_text="Book availability")
    
    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f'{self.id}({self.book.title})'
    
    def is_overdue(self):
        """Determinamos si el libro esta vencido en cuanto a la fecha de devolucion y la actual """
        return bool(self.due_back and date.today()>self.due_back)
    
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author_detail', args=[str(self.id)])
    
    def __str__(self):
        return f'{self.last_name}, {self.first_name}'