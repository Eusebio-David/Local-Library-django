import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from catalog.models import BookInstance, Book
from django.forms import ModelForm

"""
    este formulario fue de prueba
"""
class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        #cheaquea que la fecha no este en pasado 
        if data < datetime.date.today():
            raise ValidationError(_('Invalidate data - renewal in past'))
        
        # comprueba si la fecha enta entre los intervalos de 4 semanas 

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalidate date - renewal more than 4 weeks ahead'))

        # si los datos son correctos devolvemos la fecha 

        return data 
    
    
class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
       data = self.cleaned_data['due_back']

       # Check if a date is not in the past.
       if data < datetime.date.today():
           raise ValidationError(_('Invalid date - renewal in past'))

       # Check if a date is in the allowed range (+4 weeks from today).
       if data > datetime.date.today() + datetime.timedelta(weeks=4):
           raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

       # Remember to always return the cleaned data.
       return data

    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _('Renewal date')}
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}

class BookModelEditForm(ModelForm):


    class meta:
        model = Book
        fields = ['title','author', 'summary', 'isbn', 'genre', 'language']
        

