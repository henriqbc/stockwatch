from django.shortcuts import render

def stocks_list(request):
    return render(request, 'stocks/stocks_list.html')
