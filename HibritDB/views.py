from django.shortcuts import render

def index(request):
    return render(request, 'index.html') #templateddeki index.html cekiyo

def header(request):
    return render(request, 'header.html')

def slider(request):
    return render(request, 'slider.html')

def content(request):
    return render(request, 'content.html')

def footer(request):
    return render(request, 'footer.html')
