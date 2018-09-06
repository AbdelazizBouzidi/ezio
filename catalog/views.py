from django.shortcuts import render
from catalog.models import Book, Author, Genre,UserProfile
from django.views.generic import TemplateView
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,update_session_auth_hash
from django.shortcuts import redirect
from catalog.forms import SignUpForm,EditProfileForm
from catalog.forms import Search,SearchAuthor,UserProfileForm,SearchSubject
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django.core.paginator import Paginator

class SearchViewBook(TemplateView):
    tempalte_name='catalog/Search_Result.html'
    def get(self, request):
         num_books = Book.objects.all()
         form = Search()
         context = {
         'book': num_books,
         'form': form,
         }
         return render(request, self.tempalte_name, context=context)
    def post(self, request):
        form = Search(request.POST)
        if form.is_valid():
            word=form.cleaned_data["What_are_you_looking_for"]
            num_books = Book.objects.filter(genre__icontains=word)
        args={'form': form, 'word': word,'book': num_books,'userr': UserProfile,}
        return render(request,self.tempalte_name,args)
def index(request):
    """View function for home page of site."""


    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_books': num_books,
        'num_authors': num_authors,
        'num_visits': num_visits,
        'userr': UserProfile,

    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
class BookSubjectView(TemplateView):
    tempalte_name='catalog/book_subject.html'
    def get(self, request):
         num_books = Genre.objects.all()
         form = SearchSubject()
         context = {
         'books': num_books,
         'form': form,
         }
         return render(request, self.tempalte_name, context=context)
    def post(self, request):
        form = SearchSubject(request.POST)
        if form.is_valid():
            word=form.cleaned_data["Enter_the_subject_name"]
            genree = Genre.objects.filter(name__icontains=word)
            num_books = Book.objects.all()
            paginator = Paginator(num_books,12)
            page = request.GET.get('page')
            num_books = paginator.get_page(page)
        args={'form': form, 'word': word,'book': num_books,'genree':genree}
        return render(request,self.tempalte_name,args)
class BookListView(generic.ListView):
    model = Book
    tempalte_name='catalog/book_list.html'
    def get(self, request):
         num_books = Book.objects.all()
         paginator = Paginator(num_books,12)
         page = request.GET.get('page')
         num_books = paginator.get_page(page)
         form = Search()
         context = {
         'book': num_books,
         'form': form,
         }
         return render(request, self.tempalte_name, context=context)
    def post(self, request):
        form = Search(request.POST)
        if form.is_valid():
            word=form.cleaned_data["Enter_a_book_name"]
            num_books = Book.objects.filter(title__icontains=word)
            paginator = Paginator(num_books,12)
            page = request.GET.get('page')
            num_books = paginator.get_page(page)
        args={'form': form, 'word': word,'book': num_books,}
        return render(request,self.tempalte_name,args)
    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['userr'] = UserProfile
        return context
class BookDetailView(generic.DetailView):
    model = Book
    def book_detail_view(request, primary_key):
       book = get_object_or_404(Book, pk=primary_key)
       author= get_object_or_404(Author, pk=primary_key)
       return render(request, 'catalog/book_detail.html', context={'book': book,'author': author,'userr': UserProfile,})
                                                                   
class AuthorListView(generic.ListView):
    model = Author
    paginate_by =1
    tempalte_name='catalog/author_list.html'
    def get(self, request):
         num_books = Author.objects.all()
         form = SearchAuthor()
         paginator = Paginator(num_books,12)
         page = request.GET.get('page')
         num_books = paginator.get_page(page)
         context = {
         'author': num_books,
         'form': form,
         'userr': UserProfile,
         }
         return render(request, self.tempalte_name, context=context)
    def post(self, request):
        form = SearchAuthor(request.POST)
        if form.is_valid():
            first=form.cleaned_data["Enter_an_author_name"]
            num_books = Author.objects.filter(full_name__icontains=first)
            paginator = Paginator(num_books,12)
            page = request.GET.get('page')
            num_books = paginator.get_page(page)
        args={'form': form,'author': num_books}
        return render(request,self.tempalte_name,args)
    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        context['userr'] = UserProfile
        return context
class AuthorDetailView(generic.DetailView):
    model=Author
    tempalte_name='catalog/author_detail.html'
    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        context['book_list'] = Book.objects.all()
        return context
    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        context['book_list'] = Book.objects.all()
        return context
    def author_detail_view(request, primary_key):
       author = get_object_or_404(Author, pk=primary_key)
       args = {'author': author,'userr': UserProfile}
       return render(request, template_name,args)
class signup(TemplateView):
    tempalte_name='catalog/SignUp.html'
    def get(self, request):
         form = SignUpForm()
         context = {
             "form":form,
         }
         return render(request, self.tempalte_name, context=context)
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
         form.save()
         usern=form.cleaned_data["username"]
         emai =form.cleaned_data["email"]
         passs=form.cleaned_data["password1"]
         ava=form.cleaned_data["gender"]
         user = User.objects.create_user(usern, emai, passs)
         user.first_name =form.cleaned_data["first_name"]
         user.last_name = form.cleaned_data["last_name"]
         user.userprofile.gender = ava
         user.save()
        args={'form': form}
        return redirect("/accounts/login")
def profile(request):
    return render(request,'catalog/profile.html',{})
def profile_edit(request):
    tempalte_name='catalog/profile_edit.html'
    if request.method == 'POST':
        form=EditProfileForm(request.POST,instance=request.user)
        if form.is_valid:
           form.save()
           return redirect('/profile')
    else:
        form=EditProfileForm(instance=request.user)
        args={'form':form  }
        return render(request,tempalte_name,args)
def change_password(request):
    tempalte_name='catalog/change_password.html'
    if request.method=="POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
           form.save()
           update_session_auth_hash(request, form.user)
           return redirect('/profile')
        else:
           return redirect('/profile/edit/change-password')

    else:
        form=PasswordChangeForm(user=request.user)
        args={'form':form,
              'book':Book}

        return render(request,tempalte_name,args)
