import datetime
from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Book,Author, BookInstance, Genre
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm, RenewBookModelForm
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author
from django.contrib import messages

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
    
    #Number of visitis to this view, as countend inthe session variable
    num_visits = request.session.get('num_visits', 0)
    num_visits+=1
    request.session['num_visits'] = num_visits
    context = {
        'num_books': num_books,
        'num_instances': num_instance,
        'num_instance_available': num_instance_available,
        'num_authors': num_auathors,
        'num_genres': num_genres,
        'book_specific_word': book_specific_word,
        'num_visits': num_visits
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

class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    """Usamos de generic la clase basada en vista ListView para mostrar los libros que estan en prestamo de un usuario"""

    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower = self.request.user).filter(status__exact = 'o').order_by('due_back')
        )

class AllBorrowedBooks(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'catalog/book_borrowed.html'

    def get_queryset(self):
        return (
            BookInstance.objects.all().order_by('due_back')
        )

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
   
    #si la request es POST, porcesa los datos del formulario 
    if request.method == 'POST':
        
        #crea una isntancia del formulario y la rellena con los datos
        form = RenewBookModelForm(request.POST)
        

        #verificamos si la info es valida 
        if form.is_valid():
            #procesar los datos en form.cleaned_data según sea necesario (aquí sólo los escribimos en el campo due_back del modelo)
            
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()

            #redirecciona a una nueva URL
            return HttpResponseRedirect(reverse('books-borrowed'))
    else:
        # si la request es GET, u otro metodo crea un formulario por default
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form =  RenewBookModelForm(initial={'due_back': proposed_renewal_date})
            

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)





class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/11/2023'}
    permission_required = 'catalog.add_author'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
    permission_required = 'catalog.change_author'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("author-delete", kwargs={"pk": self.object.pk})
            )

#clases para editar, eliminar y crear una instancia de libro
class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.change_book'
    
    
    def form_valid(self, form):
        messages.success(self.request, 'successfully updated book')
        return super().form_valid(form)
    
class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn','genre', 'language']
    permission_required = 'catalog.add_book'

    def form_valid(self, form):
        messages.success(self.request, 'successfully create book')
        return super().form_valid(form)


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.delete_book'

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request,  'successfully delete book')
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("book-delete", kwargs={"pk": self.object.pk})
            )


#creamos vistas para las copias de los libros
class BookInstances(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'catalog/book_instances.html'

    def get_queryset(self):
        return (
            BookInstance.objects.all().order_by('status')
        )



class BookInstanceDetail(PermissionRequiredMixin, DetailView):
    model = BookInstance
    # Indicamos que se busca el objeto usando el slug
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'catalog/bookinstance_detail.html'
    permission_required = 'catalog.can_mark_returned'

class BookInstanceDelete(PermissionRequiredMixin, DeleteView):
    model = BookInstance
    success_url = reverse_lazy('books')
    permission_required = 'catalog.delete_instance'

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request,  'successfully delete instance book')
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("bookInstance-delete", kwargs={"slug": self.object.slug})
            )