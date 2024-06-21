from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from datetime import datetime

# Create your views here.

def home(request):
    #return render(request, 'auth-signin.html')
    return render(request, 'dashboard.html')


def dashboard(request):
    caturl = "http://localhost:8085/finapi/category/"
    tagexpurl = 'http://localhost:8085/finapi/actexpfilter/?grpby=cat_tags'    # last 6 months
    nameexpurl = 'http://localhost:8085/finapi/actexpfilter/?grpby=cat_name'    # last 6 months
    catexpurl = 'http://localhost:8085/finapi/categoryexpfilter/'
    
    try:
        cat_response = requests.get(caturl)
        gbar_response = requests.get(tagexpurl)
        garea_response = requests.get(nameexpurl)
        gdonut_response = requests.get(catexpurl)

        if cat_response.status_code == 200 and gdonut_response.status_code == 200 and gbar_response.status_code == 200  and garea_response.status_code == 200 :
            cat_data = cat_response.json()
            bar_data = gbar_response.json()
            area_data = garea_response.json()
            donut_data = gdonut_response.json()

            #print(data)
            return render(request, 'dashboard.html', {'categories': cat_data, 'tag_exp_monthwise' : bar_data, 'cname_exp_monthwise' : area_data, 'tot_cat_exp_data': donut_data})
        else:
            messages.warning(request, "Failed to retrieve data from the API.")
    except Exception as ex:
        print(ex)
        messages.warning(request, "An error occurred while fetching data.")
    
    return render(request, 'dashboard.html')

#------------------------------------
#        Add new activity 
#------------------------------------
def activity_add(request):
    url = 'http://localhost:8085/finapi/activity/'
    
    if request.method == "POST":
        ac_name = request.POST.get('txtActName')
        ac_desc = request.POST.get('txtAcDesc')
        expense = float( request.POST.get('txtExpense'))
        a_cat = request.POST.get('ddlCat')      # URL to category
        a_date = request.POST.get('txtActDate')

        # Step 1: Parse the date string to a datetime object
        date_obj = datetime.strptime(a_date, '%d/%m/%Y')
        # Step 2: Format the datetime object to 'YYYY-MM-DD' format
        formatted_date = date_obj.strftime('%Y-%m-%d')

        payload = {
            'ac_name': ac_name,
            'ac_desc': ac_desc,
            'expense': expense,
            'a_cat': a_cat,
            'a_date': formatted_date
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 201:
                data = response.json()
                messages.success(request, f"Activity added successfully ")  # with ID: {data['ac_id']}
            else:
                messages.warning(request, "Failed to add activity.")
        except Exception as ex:
            print(ex)
            messages.warning(request, "An error occurred during the save process.")
        return redirect('add-activity')
    
    else:
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

#----------------------------------------------------------------
#                   get list of activities
#----------------------------------------------------------------

def getactdata(request):
    url = 'http://localhost:8085/finapi/activity/'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            #print(data)
            return render(request, 'activities.html', {'acdata': data})
        else:
            messages.warning(request, "Failed to retrieve data from the API.")
    except Exception as ex:
        print(ex)
        messages.warning(request, "An error occurred while fetching data.")
    return render(request, 'index.html')

#----------------------------------------------------------------
#                   EDit an Activity
#----------------------------------------------------------------
def edit_activity(request, ac_id):
    url = f'http://localhost:8085/finapi/activity/{ac_id}/'
    categories_url = 'http://localhost:8085/finapi/category/'

    if request.method == "POST":
        ac_name = request.POST.get('txtActName')
        ac_desc = request.POST.get('txtAcDesc')
        expense = request.POST.get('txtExpense')
        a_cat = request.POST.get('ddlCat')
        a_date = request.POST.get('txtActDate')

        # Parse the date string to a datetime object
        date_obj = datetime.strptime(a_date, '%d/%m/%Y')
        # Format the datetime object to 'YYYY-MM-DD' format
        formatted_date = date_obj.strftime('%Y-%m-%d')

        payload = {
            'ac_name': ac_name,
            'ac_desc': ac_desc,
            'expense': expense,
            'a_cat': a_cat,
            'a_date': formatted_date
        }
        try:
            response = requests.put(url, json=payload)
            if response.status_code == 200:
                messages.success(request, "Activity updated successfully.")
                return redirect('get-act')
            else:
                messages.warning(request, "Failed to update activity.")
        except Exception as ex:
            print(ex)
            messages.warning(request, "An error occurred during the update process.")

    try:
        activity_response = requests.get(url)
        categories_response = requests.get(categories_url)
        if activity_response.status_code == 200 and categories_response.status_code == 200:
            activity_data = activity_response.json()
            categories = categories_response.json()
            return render(request, 'activity_edit.html', {'activity_data': activity_data, 'categories': categories})
        else:
            messages.warning(request, "Failed to retrieve activity or categories.")
    except Exception as ex:
        print(ex)
        messages.warning(request, "An error occurred while fetching data.")

    return redirect('get-act')

#----------------------------------------------------------------
#                   DELTE Activity
#----------------------------------------------------------------
def del_activity(request, ac_id):
    url = f'http://127.0.0.1:8085/finapi/activity/{ac_id}/'

    try:
        response = requests.delete(url)
    
        if response.status_code == 204:
            messages.success(request, "Activity deleted successfully.")
        else:
            messages.warning(request, "Failed to delete activity. Remote server did not respond properly.")
    except Exception as ex:
        print(ex)
        messages.warning(request, "An error occurred during the delete process. Check logs for details.")

    return redirect('get-act')

#----------------------------------------------------------------
#                   Add new category (POST)
#----------------------------------------------------------------
def save_cat(request):
    url = 'http://localhost:8085/finapi/category/'
    if request.method == "POST":
        cname = request.POST.get('txtName')
        bplan = request.POST.get('txtBudget')
        cattag = request.POST.get('ddlTag')
        
        payload = {
            'cat_name': cname, 
            'budget': bplan,
            'cat_tags' : cattag
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

#----------------------------------------------------------------
#       get category list
#----------------------------------------------------------------
def get_catlist(request):
    url = 'http://localhost:8085/finapi/category/'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            #print(data)
            return render(request, 'category.html', {'categorydata': data})
        else:
            messages.warning(request, "Failed to retrieve data from the API.")
    except Exception as ex:
        print(ex)
        messages.warning(request, "An error occurred while fetching data.")
    return redirect('/trackmyexp/dash') #***********

# ---------------------------------------------------
#       EDIT category
# ---------------------------------------------------
def edit_cat(request, cat_id):
    url = 'http://127.0.0.1:8085/finapi/category/' + str(cat_id) + '/'  # must teminate with /

    if request.method == "POST":
        # get data from form
        cname = request.POST.get('txtName')
        bplan = request.POST.get('txtBudget')        
        cattag = request.POST.get('ddlTag')
        
        payload = {
            'cat_name': cname, 
            'budget': bplan,
            'cat_tags' : cattag
        }

        response = requests.put(url, json = payload)  # send as JSON

        if response.status_code == 200:   # response 200
            data = response.json()   # returns a dictionary object with all the details of newly added object including Primary Key & auto updated values
            #print(data)
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

#-------------------------------------------------------
#   Get all activities by a selected category 
#=------------------------------------------------------
def get_act_by_cat(request, cat_id):
    url = 'http://localhost:8085/finapi/category/' + str(cat_id) + '/activity/'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # print(data)
            return render(request, 'activities.html', {'acdata': data})
        else:
            messages.warning(request, "Failed to retrieve data from the API.")
    except Exception as ex:
        print(ex)
        messages.warning(request, "An error occurred while fetching data.")
    
    return redirect('get-catlist')


#=============== REPORTS =====================
def detailed_report(request):
    url = 'http://localhost:8085/finapi/activityfilter/'

    if request.method == "POST":
        # get data from form
        fromDate = request.POST.get('txtFromDate')
        toDate = request.POST.get('txtToDate')

        url = url + '?start_date=' + fromDate + '&end_date=' + toDate

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                #print(data)
                return render(request, 'reports/detailed_report.html', {'acdata': data})
            else:
                messages.warning(request, "Failed to retrieve data from the API.")
        except Exception as ex:
            print(ex)
            messages.warning(request, "An error occurred while fetching data. Please check logs.")
        
    return render(request, 'reports/detailed_report.html')



