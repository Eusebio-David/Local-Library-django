from django.core.management.base import BaseCommand
from catalog.models import BookInstance
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Generar slugs para instancias de libros existentes'

    """
    handle(self, *args, **kwargs): Este es el método principal que se ejecutará cuando llames al comando. Dentro de este método, se busca cada instancia de BookInstance en la base de datos.
    """
    def handle(self, *args, **kwargs):
        # Obtener todas las instancias de BookInstance
        instances = BookInstance.objects.all()
        for instance in instances:
            # Verificar si el campo slug está vacío
            if not instance.slug:
                # Generar un slug basado en el campo 'imprint' u otro campo relevante
                instance.slug = slugify(instance.book.title)
                # Guardar la instancia actualizada
                instance.save()

        # Imprimir un mensaje de éxito al terminar
        self.stdout.write(self.style.SUCCESS('Slugs generados correctamente.'))