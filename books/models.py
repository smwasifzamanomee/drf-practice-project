from django.db import models
import uuid
from django.utils.text import slugify

# Create your models here.

class MyModelName(models.Model):
    my_field_name = models.CharField(max_length=100, help_text='Enter field documentation')
    
    class Meta: 
        ordering = ['-my_field_name']
        
    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        return self.my_field_name

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')
    
    class Meta:
        verbose_name_plural = 'genr'
    
    def __str__(self):
        return self.name

class Book(models.Model):
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, help_text='Enter the title of the book')
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.title
    
    def get_reverse_url(self):
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    
    #  auto generate slug field
    slug = models.SlugField(max_length=250, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.book)
        super(BookInstance, self).save(*args, **kwargs)

    
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )
    
    class Meta:
        ordering = ['due_back']
    
    def __str__(self):
        return f'{self.id} ({self.book.title})'
    

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

class Language(models.Model):
    name = models.CharField(max_length=200, help_text='Enter the book\'s natural language (e.g. English, French, Japanese etc.)')
    
    def __str__(self):
        return self.name
