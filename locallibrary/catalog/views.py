from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Book,Author, BookInstance, Genre
from django.views.generic import ListView, DetailView
# Create your views here

def index(request):
    """Views function for home page of sitie"""

    #Genera la cantidad de objetos, tanto de libros como de instancias. 
    num_books = Book.objects.all().count()
    num_instance = BookInstance.objects.all().count()

    # Libros disponibles filtrando por (status = 'a')
    num_instance_available = BookInstance.objects.filter(status__exact='a').count()

    # the 'all()' is implied by default
    num_auathors = Author.objects.count()

    #the 'all()' Genre
    num_genres = Genre.objects.all().count()
    #books that contain a specific word
    book_specific_word = Book.objects.filter(title__icontains = 'e').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instance,
        'num_instance_available': num_instance_available,
        'num_authors': num_auathors,
        'num_genres': num_genres,
        'book_specific_word': book_specific_word,
    }

    #Renderizamos el template HTML intex.html con la data que esta dentro de la variable 'context' 
    return render(request, 'catalog/index.html', context=context)

class BookListView(ListView):

    model = Book
    paginate_by = 3
    #context_object_name = 'book_list'   # your own name for the list as a template variable
    #queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    template_name = 'catalog/book_list.html'  # Specify your own template name/location
    
    #Anulacion de metodos basados en clases
    #Por ejemplo, podemos anular el get_queryset()método para cambiar la lista de registros devueltos. Esto es más flexible que simplemente configurar el querysetatributo como hicimos en el fragmento de código anterior (aunque no hay ningún beneficio real en este caso):
    """
    def get_queryset(self):
        return Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    """
    #También podemos anular la función get_context_data()para pasar variables de contexto adicionales a la plantilla (por ejemplo, la lista de libros se pasa de manera predeterminada). El fragmento a continuación muestra cómo agregar una variable denominada " some_data" al contexto (que luego estaría disponible como una variable de plantilla).
    

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context
    

class BookDetailView(DetailView):
    model = Book
    

class AuthorListView(ListView):
    model = Author

def AuthorDetailView(request, id:int):
    author = get_object_or_404(Author, id=id)
    template_name = 'catalog/author_detail.html'
    books = Book.objects.filter(author=author)
    context = {'author':author, 'books':books}
   
    return render(request, template_name, context=context)