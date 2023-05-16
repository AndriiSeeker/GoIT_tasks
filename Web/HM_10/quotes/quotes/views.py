from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse

from .models import Author, Quote, Tag
from .forms import QuoteForm, AuthorForm, TagForm
from .utils.scraper import start_parse


def main(request):
    quotes = Quote.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    top_ten_tags = Quote.objects.values('tags__name').annotate(quote_count=Count('id')).order_by('-quote_count')[:10]

    return render(request, "quotes/index.html", context={'quotes': page_obj, "top_ten_tags": top_ten_tags})


def author_about(request, _id):
    author = Author.objects.get(pk=_id)
    return render(request, 'quotes/author.html', context={'author': author})


def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()
            return redirect(to="quotes:home")
        else:
            return render(request, "quotes/add_quote.html", context={'form': QuoteForm(), "message": "Form not valid"})
    return render(request, "quotes/add_quote.html", context={'form': QuoteForm()})


def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            new_quote = form.save()
            return redirect(to="quotes:home")
        else:
            return render(request, "quotes/add_author.html",
                          context={'form': AuthorForm(), "message": "Form not valid"})
    return render(request, "quotes/add_author.html", context={'form': AuthorForm()})


def add_tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            new_quote = form.save()
            return redirect(to="quotes:home")
        else:
            return render(request, "quotes/add_tag.html", context={'form': TagForm(), "message": "Form not valid"})
    return render(request, "quotes/add_tag.html", context={'form': TagForm()})


def find_by_tag(request, _id):
    per_page = 5
    if isinstance(_id, int):
        quotes = Quote.objects.filter(tags=_id).all()
    elif isinstance(_id, str):
        _id = Tag.objects.filter(name=_id).first()
        quotes = Quote.objects.filter(tags=_id.id).all()

    top_ten_tags = Quote.objects.values('tags__name').annotate(quote_count=Count('id')).order_by('-quote_count')[:10]

    paginator = Paginator(list(quotes), per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "quotes/index.html", context={'quotes': page_obj, "top_ten_tags": top_ten_tags})


def search_form(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            quotes = Quote.objects.filter(
                Q(quote__contains=query)
            )
            return render(request, "quotes/searchbar.html", context={'quotes': quotes})
        else:
            return render(request, "quotes/searchbar.html", {})


def parser(request):
    quotes = start_parse()
    return HttpResponse(render(request, "quotes/parser.html", context={"json_quotes": quotes}))

