from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage

from forms import NoteForm
from .utils import get_mongo


def home(request, page=2):
    db = get_mongo()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, "quotes/index.html", context={"quotes": quotes_on_page})


def quote(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:home')
        else:
            return render(request, 'quotes/quote.html', {'form': form})

    return render(request, 'quotes/quote.html', {'form': NoteForm()})
