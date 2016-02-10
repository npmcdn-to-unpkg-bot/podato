from django.shortcuts import render

def graphiql(request):
    return render(request, "graphiql.html")