from django.shortcuts import render_to_response,render
from django.http import HttpResponseRedirect, HttpResponse
from books.models import Book
from django.core.mail import send_mail
from forms import ContactForm
from django.template.context_processors import csrf
def search(request):
	errors = []
	if 'q' in request.GET:
		q = request.GET['q']
		if not q:
			errors.append('Enter a search term')
		elif len(q)>20:
			errors.append('Please enter at most 20 characters')
		else:
			books = Book.objects.filter(title__icontains=q)
			return render_to_response('search_results.html',
			{'books':books, 'query':q})
	return render_to_response('search_form.html', {'errors':errors})

def contact(request):
	errors = []
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			send_mail(
				cd['subject'],
				cd['message'],
				cd.get('email', 'noreply@example.com'),
				['siteowner@example.com'],
				)
			return HttpResponseRedirect('/contact/thanks/')
	else:
		form = ContactForm(
			initial={'subject': 'I love your site!'})
	return render(request, 'contact_form.html', {'form': form}) #solve csrf problem, do not use render_response
