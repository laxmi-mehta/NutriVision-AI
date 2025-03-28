# Create your views here.
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage, default_storage
from django.conf import settings
import tensorflow as tf
import numpy as np
import os
import cv2
from tensorflow.keras.preprocessing import image
import google.generativeai as genai
from pyzbar.pyzbar import decode
import requests
from django.http import HttpResponse
#from .models import FeedBack
from django.shortcuts import render, redirect 
#from models import Post, Comment
#from .models import Barcode  
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserLoginForm, AdminLoginForm
from .models import AdminProfile, UserProfile
from pymongo import MongoClient  # Import MongoDB Client
from django.contrib.auth import logout

# Connect to MongoDB
client = MongoClient("conection string")  # Change if using different DB
db = client["your db name"]  # Replace with your actual database name
users_collection  = db["profiles_adminprofile"]  # Collection where admin data is stored


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'media')
# Configure Gemini API
genai.configure(api_key="gemini api")
model = genai.GenerativeModel("gemini-1.5-flash")

# Load your model (update with correct path)
model_path = 'profiles\model_v1_inceptionV3.h5'
tensorflow_model = tf.keras.models.load_model(model_path)

class_labels = ['burger', 'butter_naan', 'chai', 'chapati', 'chole_bhature', 'dal_makhani', 'dhokla',
                'fried_rice', 'idli', 'jalebi', 'kaathi_rolls', 'kadai_paneer', 'kulfi', 'masala_dosa',
                'momos', 'paani_puri', 'pakode', 'pav_bhaji', 'pizza', 'samosa', 'apple']


from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth import login
from django.contrib.auth import get_backends
from django.contrib.auth.backends import ModelBackend
from bson.objectid import ObjectId
from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage
import logging
from django.contrib.auth.decorators import login_required
from .models import Post
from django.conf import settings
from profiles.forms import PostForm

logger = logging.getLogger(__name__)
# Custom backend class to set backend attribute for authentication
class CustomBackend(ModelBackend):
    pass


# def hom(request):
#     return render(request, 'hom.html', {'user': request.user})
from django.shortcuts import render
from profiles.models import UserProfile, UploadedImage  # Import your models
from django.core.exceptions import ObjectDoesNotExist


def dashboard(request):
    # Fetch the UserProfile associated with the current user
    profiles = UserProfile.objects.filter(user_id=request.user.id)

    if profiles.exists():
        profile = profiles.latest('_id')  # Use '_id' for MongoDB primary key
    else:
        # Handle the case where no profile exists
        profile = None

    return render(request, 'dashboard.html', {'profile': profile})


# views.py
from bson import ObjectId  # For MongoDB ObjectId
from django.shortcuts import render, redirect
from .models import UserProfile
from django.contrib.auth.decorators import login_required

def input_user_details(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        activity_level = request.POST.get('activity_level')
        allergy_level = request.POST.get('allergy_level')

        # Check if user already has a profile
        profile, created = UserProfile.objects.get_or_create(user_id=request.user.id)

        # Update the profile with the submitted data
        profile.first_name = first_name
        profile.age = age
        profile.gender = gender
        profile.weight = weight
        profile.height = height
        profile.activity_level = activity_level
        profile.allergy_level = allergy_level
        profile.save()

        return redirect('dashboard')  # Replace with your success URL

    return render(request, 'input_user_details.html')



def create_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES.get('image')
        image_url = None

        if image:
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            image_url = fs.url(filename)

        post = Post(title=title, content=content, image_url=image_url)
        post.save()
        return redirect('community_forum')

    return render(request, 'create_post.html')

# Delete post view
def delete_post(request, post_id):
    print("Post ID received:", post_id)  # Debugging output
    
    post = get_object_or_404(Post,  _id=ObjectId(post_id))
    post.delete()
    return redirect('community_forum')

# Update post view
def update_post(request, post_id):
    post = get_object_or_404(Post,_id=ObjectId(post_id))
    if request.method == 'POST':
        post.title = request.POST['title']
        post.content = request.POST['content']
        if 'image' in request.FILES:
            post.image_url = request.FILES['image']  # Ensure you handle file saving properly
        post.save()
        return redirect('community_forum')
    return render(request, 'update_post.html', {'post': post})


def community_forum(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'community_forum.html', context)

from django.contrib.auth import logout
from django.contrib.auth import get_user_model

User = get_user_model()
def user_logout(request):
    if request.method == 'POST':
        user = request.user  # Get the logged-in user

        if user.is_authenticated:  # Ensure user is logged in
            # Delete user data from MongoDB
            User.objects.filter(id=user.id).delete()
            messages.success(request, "Your account and data have been deleted successfully.")
        
        logout(request)  # Log out the user
        request.session.flush() 
        return redirect('login')  # Redirect to login page

    return render(request, 'logout.html')  # Render the confirmation page

# Registration view
def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        contact_number = request.POST.get('contact_number')
        
        

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'register.html')

        user = CustomUser.objects.create_user(
            email=email,
            username=username,
            password=password,
            contact_number=contact_number
        )
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('login')

    return render(request, 'register.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from .forms import LoginForm 

User = get_user_model()  # Fetch the user model dynamically
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Debugging output
        logger.debug(f"Attempting to authenticate user with email: {email}")

        try:
            # Check if the user is registered
            registered_user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            logger.error(f"User with email {email} not found.")
            messages.error(request, 'User does not exist. Please register first.')
            return render(request, 'login.html')

        # Authenticate the registered user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            logger.debug(f"Authentication successful for email: {email}")
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")  # Add welcome message
            return redirect('dashboard')  # Redirect to dashboard  # Redirect to home if login successful
            if user.is_superuser:
                return redirect('admin_page')  # Redirect to admin dashboard
            else:
                return redirect('dashboard')
        else:
            logger.error(f"Authentication failed for email: {email}")
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login.html')


def homePage(request):
    return render(request,'index.html', {'user': request.user})

def aboutUs(request):
    return render(request,'about_us.html')
def recipeSuggestion(request):
    return render(request,'recipe_suggestion.html')
def newsSection(request):
    return render(request,'news_section.html')

def stepsStart(request): 
    return render(request,'steps_start.html')

def chatbot(request):
    return render(request,'chatbot.html')
# def upload(request):
#     return render(request,'nutrition/upload.html')
def result(request):
    return render(request,'nutrition/result.html')
def findhotel(request):
    return render(request,'findhotel.html')


def extract_barcode_from_image(image_path):
    image = cv2.imread(image_path)
    barcodes = decode(image)
    if barcodes:
        return barcodes[0].data.decode("utf-8")
    return None

def get_nutrition_info_from_barcode(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)
    if response.status_code == 200 and response.json().get("status") == 1:
        product = response.json()["product"]
        nutriments = product.get("nutriments", {})
        return {
            "product_name": product.get("product_name", "N/A"),
            "brand": product.get("brands", "N/A"),
            "energy": nutriments.get("energy-kcal_100g", "N/A"),
            "proteins": nutriments.get("proteins_100g", "N/A"),
            "carbohydrates": nutriments.get("carbohydrates_100g", "N/A"),
            "sugars": nutriments.get("sugars_100g", "N/A"),
            "fats": nutriments.get("fat_100g", "N/A"),
            "salt": nutriments.get("salt_100g", "N/A"),
        }
    return None

def scan_barcode(request):
    nutrition_info = None
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]
        fs = FileSystemStorage(location=MEDIA_ROOT)
        image_path = fs.save(image.name, image)
        image_full_path = os.path.join(MEDIA_ROOT, image_path)

        # Extract barcode and fetch nutrition info
        barcode = extract_barcode_from_image(image_full_path)
        if barcode:
            nutrition_info = get_nutrition_info_from_barcode(barcode)
        else:
            nutrition_info = {"error": "No barcode detected"}

        # Save image for dashboard
        dashboard_path = os.path.join(MEDIA_ROOT, "dashboard", image.name)
        os.makedirs(os.path.dirname(dashboard_path), exist_ok=True)
        fs.save(dashboard_path, image)

    return render(request, "scan_barcode.html", {"nutrition_info": nutrition_info})

def get_nutritional_info_from_gemini(food_name):
    prompt = f"""
    Provide nutritional information for {food_name} in this format:
    - Calories: <number>
    - Protein: <number>g
    - Carbohydrates: <number>g
    - Fiber: <number>g
    - Sugar: <number>g
    - Fat: <number>g
    - Vitamin C: <percentage> of daily value
    - Potassium: <percentage> of daily value
    - Suitable for: <diet types>
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        return {"error": str(e)}

def preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

def infer(img_tensor):
    return tensorflow_model.predict(img_tensor)

def upload(request):
    if request.method == 'POST' and request.FILES['image']:
        uploaded_file = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        uploaded_file_url = fs.url(filename)

        # Process the uploaded image
        img_path = f'.{uploaded_file_url}'  # Full file path for the image
        img_tensor = preprocess_image(img_path)
        predictions = infer(img_tensor)

        logits = predictions[0]
        confidence = np.max(logits) * 100
        predicted_class = np.argmax(logits)

        food_name = class_labels[predicted_class] if confidence >= 60 else "Unrecognized Food"
        nutritional_info = get_nutritional_info_from_gemini(food_name)

        # Save image for dashboard
        dashboard_path = os.path.join(MEDIA_ROOT, "dashboard", uploaded_file.name)
        os.makedirs(os.path.dirname(dashboard_path), exist_ok=True)
        fs.save(dashboard_path, uploaded_file)

        context = {
            'food_name': food_name,
            'confidence': confidence,
            'nutritional_info': nutritional_info,
            'image_url': uploaded_file_url
        }

        return render(request, 'nutrition/result.html', context)

    return render(request, 'nutrition/upload.html')


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from profiles.models import UploadedImage  # Import your image model
from .models import UserProfile

@login_required
def admin_page(request):
    if not request.user.is_superuser:
        return redirect('dashboard')  # Restrict non-admin users
    
    users = User.objects.all()  # Get all users
    posts = Post.objects.all()  # Get all posts, if necessary

    return render(request, 'admin_page.html', {
        'users': users,
        'posts': posts
    })

def admin_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        # Check if admin exists in MongoDB
        admin = admin_collection.find_one({"email": email, "password": password})

        if admin:
            request.session["admin_logged_in"] = True  # Store admin session
            return redirect("admin_dashboard")  # Redirect to admin dashboard
        else:
            messages.error(request, "Invalid admin credentials.")  # Error message

    return render(request, "admin_login.html")  # Show login form

def admin_dashboard(request):
    if not request.session.get("admin_logged_in"):
        return redirect("admin_login")

    admin_email = request.session.get("admin_email")  # Fetch admin email from session

    # Fetch all registered users from MongoDB
    users = list(users_collection.find({}, {"_id": 1, "email": 1, "first_name": 1, "last_name": 1}))

    return render(request, "admin_dashboard.html", {"admin_email": admin_email, "users": users})

def admin_logout(request):
    logout(request)
    request.session.flush()  # Clear admin session
    return redirect("admin_login")  # Redirect to admin login page

def delete_user(request, user_id):
    if not request.session.get("admin_logged_in"):
        return redirect("admin_login")

    users_collection.delete_one({"_id": user_id})
    messages.success(request, "User deleted successfully.")
    return redirect("admin_dashboard")