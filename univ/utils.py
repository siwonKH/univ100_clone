from univ.models import University


def search_university(query):
    return University.objects.filter(name__istartswith=query)

