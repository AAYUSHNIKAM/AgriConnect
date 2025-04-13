from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, BlogForm
from .models import Blog, FarmAnalysis, Cart, Product
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from twilio.rest import Client
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import base64
from django.utils.timezone import now
from datetime import datetime

# from .forms import MarketForm


def index(request):
    return render(request, 'agri_app/index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Use 'password1' instead of 'password'
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'agri_app/register.html', {'form': form})


from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']  # Use 'username' instead of 'email'
        password = request.POST['password']
        # Authenticate using username and password
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')  # Redirect to home
        else:
            return render(request, 'agri_app/login.html', {'error': 'Invalid username or password'})
    return render(request, 'agri_app/login.html')



@login_required
def home(request):
    return render(request, 'agri_app/home.html', {'user': request.user})

@login_required
def blogs(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blogs')
    else:
        form = BlogForm()
    user_blogs = Blog.objects.filter(author=request.user)
    return render(request, 'agri_app/blogs.html', {'form': form, 'blogs': user_blogs})

def user_logout(request):
    logout(request)
    return redirect('index')


@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    
    # Check if the logged-in user is the author of the blog
    if blog.author == request.user:
        blog.delete()  # Delete the blog post
        return redirect('blogs')  # Redirect to the blogs list after deletion
    else:
        # If the user is not the author, you can show an error or redirect to the home page
        return redirect('home')
    


# View to display the list of produ

def shop(request):
    # Static list of products
    products = [
        {'name': 'Organic Wheat', 'price': 20, 'description': 'Freshly harvested organic wheat.', 'image': 'wheat.jpg'},
        {'name': 'Fresh Milk', 'price': 15, 'description': 'Milk from local farms.', 'image': 'milk.jpg'},
        {'name': 'Rice', 'price': 25, 'description': 'High-quality rice from the farm.', 'image': 'rice.jpg'},
        {'name': 'Organic Tomatoes', 'price': 10, 'description': 'Home-grown organic tomatoes.', 'image': 'tomatoes.jpg'},
    ]
    return render(request, 'agri_app/shop.html', {'products': products})


# Admin view to add a new product


# Temporary storage for products (can be replaced with a database model)
class Product:
    def __init__(self, product_name, quantity, phone_no):
        self.product_name = product_name
        self.quantity = quantity
        self.phone_no = phone_no

# Temporary list to store products
products = []

def market(request):
    if request.method == 'POST':
        product_name = request.POST['product_name']
        quantity = request.POST['quantity']
        phone_no = request.POST['phone_no']
        
        # Create a new product object and add it to the list
        new_product = Product(product_name, quantity, phone_no)
        products.append(new_product)
    
    return render(request, 'agri_app/market.html', {'products': products})




# ALERTS

def alert_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        message = request.POST.get('message')
        
        if phone_number and message:
            # Send SMS
            send_sms(phone_number, message)
            messages.success(request, 'Alert sent successfully!')
        else:
            messages.error(request, 'Please fill in all fields.')
        
    return render(request, 'agri_app/alert.html')

def send_sms(to_number, message_body):
    account_sid = 'ACf4dfce08d63703abe7bb3bf6e6799eb3'
    auth_token = '4df68031d0563d3944052cbe35f776ad'
    client = Client(account_sid, auth_token)
    
    # Ensure 'to_number' is in E.164 format
    if not to_number.startswith('+'):
        to_number = f"+91{to_number}"  # Assuming India (+91) as default country code
    
    message = client.messages.create(
        body=message_body,
        from_='+16084047720',
        to=to_number
    )
    return message.sid





def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            send_mail(subject, full_message, 'your_email@example.com', ['recipient@example.com'])
            messages.success(request, "Your query has been sent successfully.")
        except Exception as e:
            messages.error(request, "There was an error sending your query. Please try again later.")

    return render(request, "agri_app/contact.html")




# analyze



def analyze(request):
    if request.method == 'POST':
        date = request.POST.get('date', now().date())
        income = float(request.POST.get('income', 0))
        expenses = float(request.POST.get('expenses', 0))
        harvested_quantity = float(request.POST.get('harvested_quantity', 0))

        FarmAnalysis.objects.create(
            date=date,
            income=income,
            expenses=expenses,
            harvested_quantity=harvested_quantity,
        )
        return redirect('analyze') 

    
    all_analyses = FarmAnalysis.objects.all().order_by('-date')
    latest_analysis = all_analyses.first()

    profit_or_loss = "Profit" if latest_analysis.income - latest_analysis.expenses >= 0 else "Loss"


    profit_loss_value = latest_analysis.income - latest_analysis.expenses
    profit_or_loss_label = "Profit" if profit_loss_value >= 0 else "Loss"

    labels = ['Income', 'Expenses', 'Harvested Quantity', profit_or_loss_label]
    sizes = [latest_analysis.income, latest_analysis.expenses, latest_analysis.harvested_quantity, abs(profit_loss_value)]
    colors = ['#ff6347', '#32cd32', '#1e90ff', '#ffd700']  
    explode = (0.05, 0.03, 0.03, 0.05)  

    
    fig, ax = plt.subplots()
    ax.pie(
        sizes,
        explode=explode,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        shadow=True,
        startangle=140
    )
    ax.axis('equal') 

    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    
    return render(request, 'agri_app/analyze.html', {
        'all_analyses': all_analyses,
        'latest_analysis': latest_analysis,
        'profit_or_loss': profit_or_loss,
        'profit_loss_value': profit_loss_value,
        'chart_data': chart_data,
    })

def delete_analysis(request, id):  
    analysis = get_object_or_404(FarmAnalysis, id=id)
    analysis.delete()
    return redirect('analyze')  