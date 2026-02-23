# utils.py
from django.core.paginator import Paginator

def paginate_queryset(request, queryset, per_page=10):
    """
    যে কোনো queryset কে paginate করার function
    - request: Django request object
    - queryset: যে queryset paginate করতে চান
    - per_page: page এ কতটা item দেখাবেন (default 10)
    Returns: page_obj (paginated page object)
    """
    try:
        per_page = int(request.GET.get('per_page', per_page))
    except ValueError:
        per_page = per_page
    
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj