from django.shortcuts import render, redirect
from django.contrib import messages
import requests

# Create your views here.

def home(request):
    #return render(request, 'auth-signin.html')
    return render(request, 'dashboard.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def activity_add(request):
    url = 'http://localhost:8085/finapi/activity/'
    
    if request.method == "POST":
        ac_name = request.POST.get('txtActName')
        ac_desc = request.POST.get('txtAcDesc')
        expense = float( request.POST.get('txtExpense'))
        a_cat = request.POST.get('ddlCat')
        a_date = request.POST.get('txtActDate')
        payload = {
            'ac_name': ac_name,
            'ac_desc': ac_desc,
            'expense': expense,
            'a_cat': a_cat,
            'a_date': a_date
        }
        print(payload)
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 201:
                data = response.json()
                messages.success(request, f"Activity added successfully with ID: {data['ac_id']}")
            else:
                messages.warning(request, "Failed to add activity.")
        except Exception as ex:
            print(ex)
            messages.warning(request, "An error occurred during the save process.")
        return redirect('add-activity')

    # Fetch categories for the dropdown
    try:
        categories_url = 'http://localhost:8085/finapi/category/'
        categories_response = requests.get(categories_url)
        if categories_response.status_code == 200:
            categories = categories_response.json()
        else:
            categories = []
            messages.warning(request, "Failed to retrieve categories.")
    except Exception as ex:
        print(ex)
        categories = []
        messages.warning(request, "An error occurred while fetching categories.")

    return render(request, 'activity-add.html', {'categories': categories})


# ------------ get list of activities -------------------
def getactdata(request):
    url = 'http://localhost:8085/finapi/activity/'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(data)
            return render(request, 'activities.html', {'acdata': data})
        else:
            messages.warning(request, "Failed to retrieve data from the API.")
    except Exception as ex:
        print(ex)
        messages.warning(request, "An error occurred while fetching data.")
    return render(request, 'index.html')


def save_cat(request):
    url = 'http://localhost:8085/finapi/category/'
    if request.method == "POST":
        cname = request.POST.get('txtName')
        bplan = request.POST.get('txtBudget')

        payload = {
            'cat_name': cname, 
            'budget': bplan
            }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 201:
                data = response.json()
                messages.success(request, f"Details stored successfully with ID: {data['cat_id']} and Name: {data['cat_name']}")
            else:
                messages.warning(request, "Failed to save data.")
        except Exception as ex:
            print(ex)
            messages.warning(request, "An error occurred during the save process.")
    return render(request, 'category_add.html')


def get_catlist(request):
    url = 'http://localhost:8085/finapi/category/'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(data)
            return render(request, 'category.html', {'categorydata': data})
        else:
            messages.warning(request, "Failed to retrieve data from the API.")
    except Exception as ex:
        print(ex)
        messages.warning(request, "An error occurred while fetching data.")
    return render(request, 'dashboard.html') #***********

def edit_cat(request, cat_id):
    url = 'http://127.0.0.1:8085/finapi/category/' + str(cat_id) + '/'  # must teminate with /

    if request.method == "POST":
        
        # get data from form
        cname = request.POST.get('txtName')
        bplan = request.POST.get('txtBudget')
        
        # cstatus = request.POST.get('rating') checkbox handling later
       

        payload = {
            'cat_name': cname,
            'budget': bplan
            
        }

        response = requests.put(url, json = payload)  # send as JSON

        if response.status_code == 200:   # response 200
            data = response.json()   # returns a dictionary object with all the details of newly added object including Primary Key & auto updated values
            print(data)
            # return data
            messages.success(request, "Details updated successfully with Name: " + str(data["cat_name"]) + ", Budget: " + str(data["budget"]))
            
        else:
            messages.warning(request, "Some error occured during update, check logs for details")
            #return None

        return redirect('/trackmyexp/getcategorylist')  # redirect to view all

    else:  # * * * * * * * get details of the selected company by API Call  * * * * * * * 

        response = requests.get(url) #.json()
        if response.status_code == 200:
            data = response.json()
            return render(request, 'category_edit.html', {'categorydata' : data})
        

        # --------------- DELETE (One)----------------------
def del_cat(request, cat_id):
    url = 'http://127.0.0.1:8085/finapi/category/' + str(cat_id) + '/'

    try:
        response = requests.delete(url)
    
        if response.status_code == 204:
            messages.success(request, "Details deleted successfully")
        else:
            messages.warning(request, "Failed to delete resource..remote server did not respond properly")
    except Exception as ex:
        print(ex)
        messages.warning(request, "Some error occured during delete, check logs for details")

    return redirect('/trackmyexp/getcategorylist')



