import urllib
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from waitress import profile
from .models import Announcement, County, OfficerTask, SubCounty, Ward, Crop, CropAdvice, FarmActivity, FarmingTip, Profile, FarmerQuestion, MarketPrice, Question,WebsiteFeedback
from django.http import JsonResponse
import json
import requests
from .decorators import farmer_required, officer_required
API_KEY ="d62393fc065ed8c96510c54ba30d8518"  # Replace

# Home Page

def home(request):

    tips = FarmingTip.objects.all().order_by("-created_at")[:4]

    return render(request, "home.html", {"tips": tips})

# ================= FARMER LOGIN =================

def farmerlogin(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("farmerdashboard")

        else:

            messages.error(request, "Invalid username or password.")

    return render(request, "farmerlogin.html")


# ================= OFFICER LOGIN =================

def officerlogin(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("officerdashboard")

        else:

            messages.error(request, "Invalid username or password.")

    return render(request, "officerlogin.html")


#=================== FARMER REGISTER =================
def farmerregister(request):

    counties = County.objects.all()

    if request.method == "POST":

        fullname = request.POST["fullname"]
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        county_id = request.POST.get("county")
        sub_county_id = request.POST.get("sub_county")
        ward_id = request.POST.get("ward")
        phone_number = request.POST.get("phone_number")
        farming_activity = request.POST.get("farming_activity")
        bio = request.POST.get("bio")
        photo = request.FILES.get("photo")

        if password != confirm_password:

            messages.error(request, "Passwords do not match.")

        elif User.objects.filter(username=username).exists():

            messages.error(request, "Username already exists.")

        else:

            user = User.objects.create_user(
                first_name=fullname,
                username=username,
                password=password
            )

            Profile.objects.create(
    user=user,
    role="Farmer",

    phone_number=phone_number,

    county_id=county_id,
    sub_county_id=sub_county_id,
    ward_id=ward_id,

    farming_activity=farming_activity,

    bio=bio,

    photo=photo
)

            messages.success(request, "Registration successful.")

            return redirect("farmerlogin")

    return render(
        request,
        "farmerregister.html",
        {
            "counties": counties
        }
    )
#=================== OFFICER REGISTER =================
def officerregister(request):
    counties = County.objects.all()

    if request.method == "POST":

        fullname = request.POST["fullname"]
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        phone_number = request.POST.get("phone_number")
        county_id = request.POST.get("county")
        specialization = request.POST.get("specialization")
        photo = request.FILES.get("photo")

        if password != confirm_password:

            messages.error(request, "Passwords do not match.")

        elif User.objects.filter(username=username).exists():

            messages.error(request, "Username already exists.")

        else:

            user = User.objects.create_user(
                first_name=fullname,
                username=username,
                password=password
            )

            Profile.objects.create(
    user=user,
    role="Officer",

    phone_number=phone_number,

    county_id=county_id,

    specialization=specialization,

    photo=photo
)

            messages.success(request, "Registration successful.")

            return redirect("officerlogin")

    return render(
        request,
        "officerregister.html",
        {
            "counties": counties
        }
    )
    



# ================= FARMER DASHBOARD =================
@login_required
@farmer_required
def farmerdashboard(request):
    print("Logged in user:", request.user.username)
    print("Full name:", request.user.first_name)

    profile = Profile.objects.get(user=request.user)

    return render(request, "farmer_dashboard.html", {"profile": profile})


# ================= OFFICER DASHBOARD =================
@login_required
@officer_required

def officerdashboard(request):
    profile = Profile.objects.get(user=request.user)

    return render(request, "officer_dashboard.html", {"profile": profile})

#================== FARMER PROFILE =================
@login_required
@farmer_required
def farmerprofile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={"role": "Farmer"}
    )

    return render(
        request,
        "farmerprofile.html",
        {
            "profile": profile
        }
    )
#=================== EDIT FARMER PROFILE =================
@login_required
@farmer_required
def edit_profile(request):

    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":

        # User model fields
        request.user.first_name = request.POST.get("first_name")
        request.user.last_name = request.POST.get("last_name")
        request.user.username = request.POST.get("username")
        request.user.save()

        # Profile model fields
        profile.phone_number = request.POST.get("phone_number")
        profile.farming_activity = request.POST.get("farming_activity")
        profile.bio = request.POST.get("bio")

        # Location
        profile.county_id = request.POST.get("county")
        #=========profile.sub_county_id = request.POST.get("sub_county")=====
        #=======profile.ward_id = request.POST.get("ward") ========

        # Photo
        if request.FILES.get("photo"):
            profile.photo = request.FILES.get("photo")

        profile.save()

        return redirect("farmerprofile")

    return render(
        request,
        "edit_profile.html",
        {
            "profile": profile,
            "counties": County.objects.all()
        }
    )

#=================== OFFICER PROFILE =================
@login_required
@officer_required

def officer_profile(request):

    profile = Profile.objects.get(user=request.user)

    return render(
        request,
        "officer_profile.html",
        {"profile": profile}
    )

#================ OFFICER EDIT PROFILE =================

@login_required
@officer_required
def edit_officer_profile(request):

    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":

        # Update User model
        request.user.first_name = request.POST.get("first_name")
        request.user.username = request.POST.get("username")
        request.user.save()


        # Update Profile model
        profile.phone_number = request.POST.get("phone_number")

        profile.specialization = request.POST.get("specialization")

        profile.bio = request.POST.get("bio")


        # Update location
        profile.county_id = request.POST.get("county")
        profile.sub_county_id = request.POST.get("sub_county")
        profile.ward_id = request.POST.get("ward")


        # Update photo
        if request.FILES.get("photo"):
            profile.photo = request.FILES.get("photo")


        profile.save()


        return redirect("officer_profile")


    return render(
        request,
        "edit_officer_profile.html",
        {
            "profile": profile,
            "counties": County.objects.all()
        }
    )



#================= FARMER QUESTION =================
### old code for askquestion and myquestions views ###
@login_required
@farmer_required
def askquestion(request):

    if request.method == "POST":

        title = request.POST["title"]
        category = request.POST["category"]
        description = request.POST["description"]

        FarmerQuestion.objects.create(
            farmer=request.user,
            title=title,
            category=category,
            description=description
        )

        return redirect("myquestions")

    return render(request, "askquestion.html")

### old system ###
@login_required
@farmer_required
def myquestions(request):

    questions = Question.objects.filter(
        farmer=request.user
    ).order_by("-created_at")

    return render(
        request,
        "myquestions.html",
        {
            "questions": questions
        }
    )

#================== officer views on announcements =================
@login_required
@officer_required

def postannouncement(request):

    if request.method == "POST":

        title = request.POST["title"]

        message = request.POST["message"]

        Announcement.objects.create(

            title=title,

            message=message,

            posted_by=request.user

        )

        return redirect("viewannouncements")

    return render(request, "postannouncement.html")

#================== farmer views on announcements =================
@login_required
@farmer_required
def viewannouncements(request):

    announcements = Announcement.objects.all().order_by("-created_at")

    return render(

        request,

        "viewannouncements.html",

        {

            "announcements": announcements

        }

    )

#================== market prices =================
@login_required
@farmer_required
def marketprices(request):

    prices = MarketPrice.objects.all().order_by("product_name")

    return render(
        request,
        "marketprices.html",
        {"prices": prices}
    )

#================== Officer Market Prices View =================
@login_required
@officer_required
def officermarketprices(request):

    prices = MarketPrice.objects.all()

    return render(
        request,
        "officer_marketprices.html",
        {
            "prices": prices
        }
    )
#================== Officer add market price =================

@login_required
@officer_required

def add_marketprice(request):

    if request.method == "POST":

        product_name = request.POST["product_name"]
        product_type = request.POST["product_type"]
        county = request.POST["county"]
        price = request.POST["price"]
        unit = request.POST["unit"]

        MarketPrice.objects.create(

            product_name=product_name,
            product_type=product_type,
            county=county,
            price=price,
            unit=unit

        )

        return redirect("officermarketprices")

    return render(request, "add_marketprice.html")

#================== edit market price ===========

@login_required
@officer_required
def edit_marketprice(request, id):

    price = MarketPrice.objects.get(id=id)

    if request.method == "POST":

        price.product_name = request.POST["product_name"]
        price.product_type = request.POST["product_type"]
        price.county = request.POST["county"]
        price.price = request.POST["price"]
        price.unit = request.POST["unit"]

        price.save()

        return redirect("officermarketprices")

    return render(
        request,
        "edit_marketprice.html",
        {"price": price}
    )
#================== delete market price ===========
@login_required
@officer_required
def delete_marketprice(request, id):

    price = MarketPrice.objects.get(id=id)
    price.delete()

    return redirect("officermarketprices")

#================== ask an officer ==================
@login_required
@farmer_required


def ask_officer(request):

    print("===== ask_officer called =====")
    print("Method:", request.method)

    if request.method == "POST":

        print("POST received")

        question = request.POST.get("question")
        image = request.FILES.get("image")

        print("Question:", question)
        print("Image:", image)
        print("User:", request.user)

        Question.objects.create(
            farmer=request.user,
            question=question,
            image=image
        )

        print("Saved successfully!")

        return redirect("myquestions")

    return render(request, "askquestion.html")
#================== officer view  farmer's questions =================

@login_required
@officer_required
def officer_questions(request):

    questions = Question.objects.all().order_by( "is_answered","-created_at")
    print(questions)

    return render(
        request,
        "officer_questions.html",
        {"questions": questions}
    )


#================== officer answers question ==================

#============def answer_question(request, id):

    question = Question.objects.get(id=id)

    if request.method == "POST":

        question.answer = request.POST.get("answer")
        question.answered_by = request.user
        question.is_answered = True
        question.save()

        return redirect("officer_questions")

    return render(
        request,
        "answer_question.html",
        {
            "question": question
        }
    ) 

#================== officer answers question ==================
@login_required
@officer_required
def answer_question(request, id):
    question = Question.objects.get(id=id)

    if request.method == "POST":
        answer_text = request.POST.get("answer")

        question.answer = answer_text
        question.is_answered = True
        question.answered_by = request.user
        question.save()

        return redirect("officer_questions")

    return render(request, "answer_question.html", {"question": question})

#================== farmer record ==========
@login_required
@farmer_required
def farm_records(request):

    records = FarmActivity.objects.filter(farmer=request.user).order_by("-date")

    return render(request, "farm_records.html", {"records": records})

#=================== add farm record ==========
@login_required
@farmer_required
def add_activity(request):

    if request.method == "POST":

        FarmActivity.objects.create(
            farmer=request.user,
            crop_name=request.POST.get("crop_name"),
            activity_type=request.POST.get("activity_type"),
            date=request.POST.get("date"),
            quantity=request.POST.get("quantity"),
            notes=request.POST.get("notes"),
        )

        return redirect("farm_records")

    return render(request, "add_activity.html")

#=================== edit farm record ==========
@login_required
@farmer_required
def edit_farm_activity(request, id):

    activity = FarmActivity.objects.get(
        id=id,
        farmer=request.user
    )


    if request.method == "POST":

        activity.crop_name = request.POST.get("crop_name")

        activity.activity_type = request.POST.get("activity_type")

        activity.date = request.POST.get("date")

        activity.quantity = request.POST.get("quantity")

        activity.notes = request.POST.get("notes")

        activity.save()


        return redirect("farm_records")


    return render(
        request,
        "edit_farm_activity.html",
        {
            "activity": activity
        }
    )
#=================== delete farm record ==========
@login_required
@farmer_required
def delete_farm_activity(request, id):

    activity = FarmActivity.objects.get(
        id=id,
        farmer=request.user
    )


    if request.method == "POST":

        activity.delete()

        return redirect("farm_records")


    return render(
        request,
        "delete_farm_activity.html",
        {
            "activity": activity
        }
    )

#=================== crop advice from farmers ==========
@login_required
@officer_required
def add_crop_advice(request):

    if request.method == "POST":

        CropAdvice.objects.create(
            category=request.POST.get("category"),
            farm_item=request.POST.get("farm_item"),
            advice=request.POST.get("advice"),
            source="OFFICER"
        )

        return redirect("officerdashboard")

    return render(request, "add_crop_advice.html")
#=================== farmers view advice ==========
@login_required
@farmer_required
def my_crop_advice(request):

    advice = CropAdvice.objects.all().order_by("-created_at")

    return render(request, "my_crop_advice.html", {"advice": advice})

# ================= Manage Crop Advice =================

@login_required
@officer_required
def manage_crop_advice(request):

    advice = CropAdvice.objects.all().order_by("-created_at")

    return render(
        request,
        "manage_crop_advice.html",
        {
            "advice": advice
        }
    )

# ================= Edit Crop Advice =================

@login_required
@officer_required
def edit_crop_advice(request, id):

    advice = CropAdvice.objects.get(id=id)

    if request.method == "POST":

        advice.category = request.POST.get("category")
        advice.farm_item = request.POST.get("farm_item")
        advice.advice = request.POST.get("advice")

        advice.save()

        return redirect("manage_crop_advice")

    return render(
        request,
        "edit_crop_advice.html",
        {
            "advice": advice
        }
    )

# ================= Delete Crop Advice =================

@login_required
@officer_required
def delete_crop_advice(request, id):

    advice = CropAdvice.objects.get(id=id)

    if request.method == "POST":

        advice.delete()

        return redirect("manage_crop_advice")

    return render(
        request,
        "delete_crop_advice.html",
        {
            "advice": advice
        }
    )
#=================== farming tips =================


def farming_tips(request):

    tips = FarmingTip.objects.all().order_by("-created_at")

    return render(request, "farming_tips.html", {"tips": tips})
#=================== add farming tip =================
@login_required
@officer_required
def add_farming_tip(request):

    if request.method == "POST":

        FarmingTip.objects.create(
            title=request.POST.get("title"),
            category=request.POST.get("category"),
            content=request.POST.get("content"),
            image=request.FILES.get("image"),
            video=request.FILES.get("video"),
        )

        return redirect("farming_tips")

    return render(request, "add_farming_tip.html")

#=================== manage farming tips =================
@login_required
@officer_required
def manage_farming_tips(request):

    tips = FarmingTip.objects.all().order_by("-created_at")

    return render(
        request,
        "manage_farming_tips.html",
        {
            "tips": tips
        }
    )
#================== edit views =======
@login_required
@officer_required
def edit_farming_tip(request, id):

    tip = FarmingTip.objects.get(id=id)

    if request.method == "POST":

        tip.title = request.POST.get("title")
        tip.category = request.POST.get("category")
        tip.content = request.POST.get("content")

        if request.FILES.get("image"):
            tip.image = request.FILES.get("image")

        if request.FILES.get("video"):
            tip.video = request.FILES.get("video")

        tip.save()

        return redirect("manage_farming_tips")

    return render(
        request,
        "edit_farming_tip.html",
        {
            "tip": tip
        }
    )

#================== delete views =======
@login_required
@officer_required
def delete_farming_tip(request, id):

    tip = FarmingTip.objects.get(id=id)

    if request.method == "POST":

        tip.delete()

        return redirect("manage_farming_tips")

    return render(
        request,
        "delete_farming_tip.html",
        {
            "tip": tip
        }
    )

#=================== registered farmers view =================

@login_required
@officer_required
def registered_farmers(request):

    farmers = Profile.objects.filter(role="Farmer").select_related("user")

    return render(
        request,
        "registered_farmers.html",
        {
            "farmers": farmers
        }
    )

#=================== weather record views =================
@login_required
@farmer_required
def weather_dashboard(request):

    profile = Profile.objects.get(user=request.user)

    if not profile.latitude or not profile.longitude:
        return render(
            request,
            "weather_dashboard.html",
            {
                "profile": profile,
                "error": "Please allow location access to view your local weather."
            }
        )

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={profile.latitude}"
        f"&lon={profile.longitude}"
        f"&appid={API_KEY}"
        f"&units=metric"
    )

    response = requests.get(url)
    weather = response.json()
    weather = response.json()

    if response.status_code != 200:
          return render(
        request,
        "weather_dashboard.html",
        {
            "profile": profile,
            "error": weather.get("message", "Unable to fetch weather."),
        },
    )


    temperature = weather["main"]["temp"]
    humidity = weather["main"]["humidity"]
    wind = weather["wind"]["speed"]
    description = weather["weather"][0]["description"]

    icon = weather["weather"][0]["icon"]
    icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"

    location = weather["name"]

    # Create advice list
    advice = []

    # Rain
    if "rain" in description.lower():
        advice.append("🌧️ Rain is expected. Delay pesticide spraying.")
        advice.append("🌱 Good soil moisture for planting.")

    # High temperature
    if temperature >= 30:
        advice.append("☀️ High temperatures detected. Increase irrigation.")
        advice.append("🐄 Ensure livestock have plenty of drinking water.")

    elif 18 <= temperature < 30:
        advice.append("🌿 Good weather for most farming activities.")

    else:
        advice.append("🥶 Cool temperatures. Monitor sensitive crops.")

    # Strong winds
    if wind >= 8:
        advice.append("💨 Strong winds detected. Avoid spraying chemicals.")

    # High humidity
    if humidity >= 80:
        advice.append("🍄 High humidity may increase fungal diseases.")

    if not advice:
        advice.append("✅ Weather conditions are suitable for normal farm activities.")

    return render(
        request,
        "weather_dashboard.html",
        {
            "profile": profile,
            "location": location,
            "temperature": temperature,
            "humidity": humidity,
            "wind": wind,
            "description": description,
            "icon_url": icon_url,
            "advice": advice,
        }
    )
    

#================== views for json locations ==========
from django.http import JsonResponse

def load_subcounties(request):

    county_id = request.GET.get("county")

    sub_counties = SubCounty.objects.filter(
        county_id=county_id
    ).order_by("name")

    data = list(
        sub_counties.values("id", "name")
    )

    return JsonResponse(data, safe=False)


def load_wards(request):

    sub_county_id = request.GET.get("sub_county")

    wards = Ward.objects.filter(
        sub_county_id=sub_county_id
    ).order_by("name")

    data = list(
        wards.values("id", "name")
    )

    return JsonResponse(data, safe=False)


#=================== views for json locationson weather things==========
@login_required

def save_location(request):
    if request.method == "POST":
        data = json.loads(request.body)

        profile = request.user.profile
        profile.latitude = data.get("latitude")
        profile.longitude = data.get("longitude")
        profile.save()

        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error"})

#=================== WEBSITE FEEDBACK =================

@login_required
def website_feedback(request):

    if request.method == "POST":

        WebsiteFeedback.objects.create(

            user=request.user,

            role=request.user.profile.role,

            rating=request.POST.get("rating"),

            category=request.POST.get("category"),

            message=request.POST.get("message")

        )

        messages.success(
            request,
            "Thank you for helping improve Urimi Digital."
        )

        return redirect("website_feedback")

    return render(
        request,
        "website_feedback.html"
    )
#=================== OFFICER DAILY PLANNER =================
@login_required
@officer_required
def officer_tasks(request):

    tasks = OfficerTask.objects.filter(
        officer=request.user
    ).order_by("completed", "due_date")

    return render(
        request,
        "officer_tasks.html",
        {
            "tasks": tasks
        }
    )
#=================== OFFICER ADD TASK =================
@login_required
@officer_required
def add_officer_task(request):

    if request.method == "POST":

        OfficerTask.objects.create(

            officer=request.user,

            title=request.POST.get("title"),

            description=request.POST.get("description"),

            due_date=request.POST.get("due_date")

        )

        return redirect("officer_tasks")

    return render(
        request,
        "add_officer_task.html"
    )

#=================== EDIT OFFICER TASK =================

@login_required
@officer_required
def edit_officer_task(request, id):

    task = OfficerTask.objects.get(
        id=id,
        officer=request.user
    )

    if request.method == "POST":

        task.title = request.POST.get("title")

        task.description = request.POST.get("description")

        task.due_date = request.POST.get("due_date")

        task.save()

        return redirect("officer_tasks")

    return render(
        request,
        "edit_officer_task.html",
        {
            "task": task
        }
    )

#=================== DELETE OFFICER TASK =================
#=================== DELETE OFFICER TASK =================

@login_required
@officer_required
def delete_officer_task(request, id):

    task = OfficerTask.objects.get(
        id=id,
        officer=request.user
    )

    if request.method == "POST":

        task.delete()

        return redirect("officer_tasks")

    return render(
        request,
        "delete_officer_task.html",
        {
            "task": task
        }
    )

#=================== COMPLETE OFFICER TASK =================

@login_required
@officer_required
def complete_officer_task(request, id):

    task = OfficerTask.objects.get(
        id=id,
        officer=request.user
    )

    if request.method == "POST":

        task.completed = True
        task.save()

        return redirect("officer_tasks")

    return render(
        request,
        "complete_officer_task.html",
        {
            "task": task
        }
    )
# ================= LOGOUT =================

def logout_view(request):

    logout(request)

    return redirect("home")
