
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book_detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('authors/<int:id>',views.AuthorDetailView, name ='author_detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.AllBorrowedBooks.as_view(), name='books-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

    
urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]

urlpatterns += {
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='update-book'),
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name = 'book-delete'),
}
urlpatterns += {
    path('booksInstance/', views.BookInstances.as_view(), name='books-instances'),
    path('bookInstance/<slug:slug>', views.BookInstanceDetail.as_view(), name='detail-book-instance'),
    path('bookInstance/<slug:slug>/delete', views.BookInstanceDelete.as_view(), name='bookinstance-delete'),

}