from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from datetime import datetime
# for writing json to file
import json

# Create your views here.

def home(request):
    #return render(request, 'auth-signin.html')
    return render(request, 'dash1.html')


def dashboard(request):
    # Load token from session
    token = request.session.get('authToken', None)
    
    if token:
        # Use the token for subsequent requests
        headers = {
            'Authorization': f'Token {token}'
        }

        caturl = "http://localhost:8085/finapi/category/"
        tagexpurl = 'http://localhost:8085/finapi/actexpfilter/?grpby=cat_tags'    # last 6 months
        nameexpurl = 'http://localhost:8085/finapi/actexpfilter/?grpby=cat_name'    # last 6 months
        catexpurl = 'http://localhost:8085/finapi/categoryexpfilter/'
        
        try:
            cat_response = requests.get(caturl, headers = headers) # pass TOKEN as header
            gbar_response = requests.get(tagexpurl)
            garea_response = requests.get(nameexpurl)
            gdonut_response = requests.get(catexpurl)

            if cat_response.status_code == 200 and gdonut_response.status_code == 200 and gbar_response.status_code == 200  and garea_response.status_code == 200 :
                cat_data = cat_response.json()
                bar_data = gbar_response.json()
                area_data = garea_response.json()
                donut_data = gdonut_response.json()

                # print(area_data)

                # print(donut_data)

                #print(data)
                # get username from session to display 
                au_uname = request.session.get('active_uname', None)
                return render(request, 'dashboard.html', {'au_uname': au_uname, 'categories': cat_data, 'tag_exp_monthwise' : bar_data, 'cname_exp_monthwise' : area_data, 'tot_cat_exp_data': donut_data})
                
            else:
                messages.warning(request, "Failed to retrieve data from the API.")
        except Exception as ex:
            print(ex)
            messages.warning(request, "An error occurred while fetching data.")
        
        return render(request, 'dashboard.html')

    # Session missing
    else:
        messages.warning(request, "You need to login to access this functionality.")
        return redirect('login-user')

#------------------------------------
#        Add new activity 
#------------------------------------
def activity_add(request):
    # Load token from session
    token = request.session.get('authToken', None)

    if token:
        # Use the token for subsequent requests
        headers = {
            'Authorization': f'Token {token}'
        }

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
                response = requests.post(url, json=payload, headers = headers) # pass TOKEN as header
                if response.status_code == 201:
                    data = response.json()
                    messages.success(request, f"Activity added successfully ")  # with ID: {data['ac_id']}
                else:
                    messages.warning(request, "Failed to add activity.")
            except Exception as ex:
                print(ex)
                messages.warning(request, "An error occurred during the save process.")
            return redirect('add-activity') # render through redirect to lead the categories by API CAlls
        
        else:
            # Fetch categories for the dropdown
            try:
                categories_url = 'http://localhost:8085/finapi/category/'
                categories_response = requests.get(categories_url, headers = headers) # pass TOKEN as header
                if categories_response.status_code == 200:
                    categories = categories_response.json()
                else:
                    categories = []
                    messages.warning(request, "Failed to retrieve categories.")
            except Exception as ex:
                print(ex)
                categories = []
                messages.warning(request, "An error occurred while fetching categories.")
            # get username before render
            au_uname = request.session.get('active_uname', None)

            return render(request, 'activity-add.html', {'au_uname': au_uname, 'categories': categories})
    
    # Session missing
    else:
        messages.warning(request, "You need to login to access this functionality.")
        return redirect('login-user')

#----------------------------------------------------------------
#                   get list of activities
#----------------------------------------------------------------

def getactdata(request):
    # Load token from session
    token = request.session.get('authToken', None)

    """ Option 2: from a filefrom file
    with open('token.json', 'r') as file:
        data = json.load(file)
        token = data['token']
    """

    if token:
        # Use the token for subsequent requests
        headers = {
            'Authorization': f'Token {token}'
        }

        url = 'http://localhost:8085/finapi/activity/'
        
        try:
            response = requests.get(url, headers = headers) # pass TOKEN as header
            
            if response.status_code == 200:
                # convert the response to JSON
                data = response.json()
                
                au_uname = request.session.get('active_uname', None)  # Get username for display
                return render(request, 'activities.html', {'acdata': data, 'au_uname': au_uname})
            
            else:
                messages.warning(request, "Failed to retrieve data from the API.")
        
        except Exception as ex:
            print(ex)
            messages.warning(request, "An error occurred while fetching data.")
            return redirect('dashboard')
    
    # Session missing
    else:
        messages.warning(request, "You are not authorized to access this page. Please login")
        return redirect('login-user')

#----------------------------------------------------------------
#                   EDit an Activity
#----------------------------------------------------------------
def edit_activity(request, ac_id):
    # Load token from session
    token = request.session.get('authToken', None)

    if token:
        # Use the token for subsequent requests
        headers = {
            'Authorization': f'Token {token}'
        }

        url = f'http://localhost:8085/finapi/activity/{ac_id}/'
        categories_url = 'http://localhost:8085/finapi/category/'

        if request.method == "POST":    # UPDATE activity
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
                response = requests.put(url, json=payload, headers = headers) # pass Token with headers
                
                if response.status_code == 200:
                    # data = response.json()   # returns a dictionary object with all the details of newly added object including Primary Key & auto updated values
                    messages.success(request, "Activity updated successfully.")
                
                else:
                    messages.warning(request, "Failed to update activity.")
            except Exception as ex:
                print(ex)
                messages.warning(request, "An error occurred during the update process, check logs for details.")
            
            return redirect('get-act')
        
        else:   # Fetch data to load in form

            try:
                activity_response = requests.get(url, headers = headers)    # pass token as header
                categories_response = requests.get(categories_url, headers = headers)

                if activity_response.status_code == 200 and categories_response.status_code == 200:
                    # convert the response to JSON
                    activity_data = activity_response.json()
                    categories = categories_response.json()

                    # get username before render
                    au_uname = request.session.get('active_uname', None)

                    return render(request, 'activity_edit.html', {'activity_data': activity_data, 'categories': categories, 'au_uname': au_uname})
                else:
                    messages.warning(request, "Failed to retrieve activity or categories.")
            except Exception as ex:
                print(ex)
                messages.warning(request, "An error occurred while fetching data, please check log.")

        return redirect('get-act')
    else:
        messages.warning(request, "You are not authorized to access this page. Please login")
        return redirect('login-user')

#----------------------------------------------------------------
#                   DELETE Activity
#----------------------------------------------------------------
def del_activity(request, ac_id):
    # Load token from session
    token = request.session.get('authToken', None)

    if token:
        # Use the token for subsequent requests
        headers = {
            'Authorization': f'Token {token}'
        }

        url = f'http://127.0.0.1:8085/finapi/activity/{ac_id}/'

        try:
            response = requests.delete(url, headers = headers)  
        
            if response.status_code == 204:
                messages.success(request, "Activity deleted successfully.")
            else:
                messages.warning(request, "Failed to delete activity. Remote server did not respond properly.")
        except Exception as ex:
            print(ex)
            messages.warning(request, "An error occurred during the delete process. Check logs for details.")

        return redirect('get-act')
    
    # Session missing
    else:
        messages.warning(request, "You are not authorized to access this page. Please login")
        return redirect('login-user')

#----------------------------------------------------------------
#                   Add new category (POST)
#----------------------------------------------------------------
def save_cat(request):

    # Load token from session
    token = request.session.get('authToken', None)
    
    if token:
        # Use the token for subsequent requests
        headers = {
            'Authorization': f'Token {token}'
        }

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
                response = requests.post(url, json=payload, headers = headers) # pass TOKEN as header
                if response.status_code == 201:
                    data = response.json()
                    messages.success(request, "Category details stored successfully")

                else:
                    messages.warning(request, "Failed to save data.")
            except Exception as ex:
                print(ex)
                messages.warning(request, "An error occurred during the save process.")
        # get username before render
        au_uname = request.session.get('active_uname', None)

        return render(request, 'category_add.html', {'au_uname': au_uname})
    
    # Session missing
    else:
        messages.warning(request, "You need to login to access this functionality.")
        return redirect('login-user')

#----------------------------------------------------------------
#       get category list
#----------------------------------------------------------------
def get_catlist(request):
    # Load token from session
    token = request.session.get('authToken', None)

    if token:
        # Use the token for subsequent requests
        headers = {
            'Authorization': f'Token {token}'
        }

        url = 'http://localhost:8085/finapi/category/'
        
        try:
            response = requests.get(url, headers = headers) # pass TOKEN as header

            if response.status_code == 200:
                # convert the response to JSON
                data = response.json()
                
                au_uname = request.session.get('active_uname', None)  # Get username for display
                return render(request, 'category.html', {'categorydata': data , 'au_uname': au_uname})
            
            else:
                messages.warning(request, "Failed to retrieve data from the API.")
        
        except Exception as ex:
            print(ex)
            messages.warning(request, "An error occurred while fetching data.")
            return redirect('/trackmyexp/dash') #***********
    
    # Session missing
    else:
        messages.warning(request, "You are not authorized to access this page. Please login")
        return redirect('login-user')

# ---------------------------------------------------
#       EDIT category
# ---------------------------------------------------
def edit_cat(request, cat_id):

    # Load token from session
    token = request.session.get('authToken', None)

    if token:
        # Use the token for subsequent requests
        headers = {
            'Authorization': f'Token {token}'
        }

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

            try:
                response = requests.put(url, json = payload, headers = headers) # pass Token with headers

                if response.status_code == 200:   # response 200
                    data = response.json()   # returns a dictionary object with all the details of newly added object including Primary Key & auto updated values
                    messages.success(request, "Details updated successfully with Name: " + str(data["cat_name"]) + ", Budget: " + str(data["budget"]))
                    
                else:
                    messages.warning(request, "Failed to update activity.")
            except Exception as ex:
                print(ex)
                messages.warning(request, "An error occurred during the update process, check logs for details.")
            

            return redirect('/trackmyexp/getcategorylist')  # redirect to view all

        else:  # * * * * * * * get details of the selected company by API Call  * * * * * * * 
            try:
                response = requests.get(url, headers = headers)  #.json()
                if response.status_code == 200:
                    data = response.json()

                    # get username before render
                    au_uname = request.session.get('active_uname', None)
                    return render(request, 'category_edit.html', {'categorydata' : data, 'au_uname': au_uname})
                else:
                    messages.warning(request, "Failed to retrieve category details.")
            except Exception as ex:
                print(ex)
                messages.warning(request, "An error occurred while fetching data, please check log.")
        
#----------------------------------------------------------------
#                   DELETE Category
#----------------------------------------------------------------
def del_cat(request, cat_id):
    # Load token from session
    token = request.session.get('authToken', None)

    if token:
        # Use the token for subsequent requests
        headers = {
            'Authorization': f'Token {token}'
        }
    
        url = 'http://127.0.0.1:8085/finapi/category/' + str(cat_id) + '/'

        try:
            response = requests.delete(url, headers = headers)  
        
            if response.status_code == 204:
                messages.success(request, "Details deleted successfully")
            else:
                messages.warning(request, "Failed to delete resource..remote server did not respond properly")
        except Exception as ex:
            print(ex)
            messages.warning(request, "Some error occured during delete, check logs for details")

        return redirect('/trackmyexp/getcategorylist')
    
    # Session missing
    else:
        messages.warning(request, "You are not authorized to access this page. Please login")
        return redirect('login-user')

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


# ==============================================================================
#                       USER AUTHENTICATION
# ==============================================================================

def registeruser(request):
    regurl = "http://localhost:8085/authapi/register/"

    if request.method == "POST":
        uname = request.POST.get('txtUname')
        upass = request.POST.get('txtUpass')
        uemail = request.POST.get('txtEmail')
        
        payload = {
            'username': uname, 
            'password': upass,
            'email' : uemail
        }

        try:
            response = requests.post(regurl, json = payload)  # response contains login token

            if response.status_code == 201:
                
                # Extract the token from the response
                # token =  response.json().get('token')  ORRR

                # data = response.json()
                # token = data['token']

                # Save token to a file
                # with open('token.json', 'w') as file:
                #     json.dump({'token': token}, file)

                #set a msg
                messages.success(request, "User registration successfull")
                # redirect to login page
                return redirect('login-user')
            else:
                messages.warning(request, "Failed to save data.")
        except Exception as ex:
            print(ex)
            messages.warning(request, "An error occurred during the save process.")

    return render(request, 'auth-signup.html')

# ============ LOGIN ================
# @csrf_exempt  ??????

def loginuser(request):
    loginurl = 'http://localhost:8085/authapi/login/'
    if request.method == "POST":
        uname = request.POST.get('txtUname')
        upass = request.POST.get('txtUpass')
        
        credentials = {
            'username': uname, 
            'password': upass
        }

        try:
            response = requests.post(loginurl, json = credentials)  # response contains login token

            if response.status_code == 200:
                
                # Extract the token from the response
                # token =  response.json().get('token')
                data = response.json()
                token = data['token']

                # Save the token for future API calls -
                # Option 1: in session
                request.session['authToken'] = token
                request.session['active_uname'] = data['act_uname']
                

                """ # Option 2: in a file
                with open('token.json', 'w') as file:
                    json.dump({'token': token}, file)
                """

                #set a msg
                messages.success(request, "Login successfull")
                # redirect to dashboard
                return redirect('dashboard')
            else:
                messages.warning(request, "Incorrect credential, please try again.")
        except Exception as ex:
            print(ex)
            messages.warning(request, "An error occurred during login. Please try again")

    # render login page
    return render(request, 'auth-signin.html')


# ============== LOGOUT =================
def logoutuser(request):

    # Load token 
    # Option 1: from session
    token = request.session.get('authToken', None)

    """ Option 2: from a filefrom file
    with open('token.json', 'r') as file:
        data = json.load(file)
        token = data['token']
    """

    if token:
        # Use the token for subsequent requests
        headers = {
            'Authorization': f'Token {token}'
        }

        logouturl = 'http://localhost:8085/authapi/logout/'
        
        try:
            response = requests.post(logouturl, headers = headers)  # response contains login token

            if response.status_code == 200:
                
                # Extract the logout msg from the response
                rmsg = response.json().get('message')

                # Clear token & username from SESSION
                try:
                    del request.session['authToken']
                    del request.session['active_uname']
                except KeyError:
                    pass

                #set a msg
                messages.success(request, rmsg)
                # redirect to login page
                # xxxx return render(request, 'auth-signin.html')  xxxx not directly render...form submission for login does not redirecthere
                return redirect('login-user')
                
            else:
                messages.warning(request, "Opration failed.") 
                # redirect to dash
        except Exception as ex:
            print(ex)
            messages.warning(request, "An error occurred during logout.")
    else:
        messages.warning(request, "User not authenticated. Please login")
        return redirect('login-user')
    
    return redirect('dashboard')

    




