from django.contrib.auth.models import User
from django.db import models


#=================== location ==========

class County(models.Model):
    name = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class SubCounty(models.Model):
    county = models.ForeignKey(
        County,
        on_delete=models.CASCADE,
        related_name="subcounties"
    )

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ward(models.Model):
    sub_county = models.ForeignKey(
        SubCounty,
        on_delete=models.CASCADE,
        related_name="wards"
    )

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



#=========== profile =========

class Profile(models.Model):

    ROLE_CHOICES = (
        ('Farmer','Farmer'),
        ('Officer','Officer'),
    )

    FARM_TYPES = (
        ('Crop Farming', 'Crop Farming'),
        ('Livestock Farming', 'Livestock Farming'),
        ('Mixed Farming', 'Mixed Farming'),
    )


    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True
    )


    county = models.ForeignKey(
        County,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    sub_county = models.ForeignKey(
        SubCounty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    ward = models.ForeignKey(
        Ward,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )


    farming_activity = models.CharField(
        max_length=30,
        choices=FARM_TYPES,
        blank=True
    )


    photo = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True
    )
    
    specialization = models.CharField(
    max_length=100,
    blank=True
)
    



    def __str__(self):
        return self.user.username

#=================== ask an officer ==========
    

class FarmerQuestion(models.Model):

    CATEGORY_CHOICES = (
        ('Crops', 'Crops'),
        ('Livestock', 'Livestock'),
        ('Soil', 'Soil'),
        ('Irrigation', 'Irrigation'),
        ('Other', 'Other'),
    )

    farmer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    description = models.TextField()

    answer = models.TextField(
        blank=True
    )
    

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title
    

#================== announcement ==========

class Announcement(models.Model):

    title = models.CharField(max_length=200)

    message = models.TextField()

    posted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title
    
#================== market prices ==========
class MarketPrice(models.Model):

    PRODUCT_TYPES = (
        ('Crop', 'Crop'),
        ('Livestock', 'Livestock'),
    )

    product_name = models.CharField(max_length=100)

    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPES
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    unit = models.CharField(
        max_length=50,
        default="per Kg"
    )

    county = models.CharField(
        max_length=100
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.product_name
    

#================= ask an officer ==========
class Question(models.Model):

    farmer = models.ForeignKey(User, on_delete=models.CASCADE)

    question = models.TextField()

    image = models.ImageField(upload_to="questions/", blank=True, null=True)

    answer = models.TextField(blank=True, null=True)

    answered_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="answered_questions"
    )

    is_answered = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
    
#=================== crop models(rec) =================
class Crop(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    variety = models.CharField(max_length=100, blank=True)

    planting_date = models.DateField()

    expected_growth_months = models.PositiveIntegerField(default=4)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.variety}) - Planted on {self.planting_date}"

#=================== farm activity models(rec) =================
class FarmActivity(models.Model):

    ACTIVITY_TYPES = [
        ("PLANTING", "Planting"),
        ("SPRAYING", "Spraying"),
        ("FERTILIZER", "Fertilizer"),
        ("HARVEST", "Harvest"),
        ("FEEDING", "Feeding"),
        ("MILK", "Milk Production"),
        ("VACCINATION", "Vaccination"),
        ("DEWORMING", "Deworming"),
    ]

    farmer = models.ForeignKey(User, on_delete=models.CASCADE)

    
    crop_name = models.CharField(max_length=100)

    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)

    date = models.DateField()

    quantity = models.FloatField(null=True, blank=True)  # e.g. milk liters, fertilizer kg

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.activity_type} - {self.crop_name} on {self.date}"

#=================== agriculture report  =================
class AgricultureReport(models.Model):

    REPORT_TYPES = [
        ("CROP", "Crop Report"),
        ("LIVESTOCK", "Livestock Report"),
    ]

    title = models.CharField(max_length=200)

    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

#=================== crop advice =================
class CropAdvice(models.Model):

    category = models.CharField(
        max_length=20,
        choices=[
            ("CROP", "Crop"),
            ("LIVESTOCK", "Livestock"),
        ],
        default="CROP"
    )

    farm_item = models.CharField(max_length=100)

    advice = models.TextField()

    source = models.CharField(
        max_length=20,
        choices=[
            ("OFFICER", "Officer"),
            ("SYSTEM", "System Generated"),
            ("REPORT", "From Report"),
            ("TIP", "From Tip"),
        ],
        default="OFFICER"
    )

    target_group = models.CharField(
        max_length=20,
        choices=[
            ("ALL", "All Farmers"),
            ("CROPS", "Crop Farmers"),
            ("LIVESTOCK", "Livestock Farmers"),
        ],
        default="ALL"
    )

    related_report = models.ForeignKey(
        "users.AgricultureReport",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} Advice for {self.farm_item}"

#======================= my farming tips ==========================
class FarmingTip(models.Model):

    CATEGORY_CHOICES = [
        ("CROPS", "Crops"),
        ("LIVESTOCK", "Livestock"),
        ("IRRIGATION", "Irrigation"),
        ("GENERAL", "General"),
    ]

    title = models.CharField(max_length=200)

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    content = models.TextField()

    image = models.ImageField(upload_to="tips/images/", blank=True, null=True)

    video = models.FileField(upload_to="tips/videos/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
#======================= weather record ==========================

class WeatherRecord(models.Model):

    county = models.ForeignKey(
        County,
        on_delete=models.CASCADE
    )

    temperature = models.FloatField()

    humidity = models.IntegerField()

    rain_probability = models.IntegerField()

    wind_speed = models.FloatField()

    weather_description = models.CharField(
        max_length=100
    )

    advice = models.TextField()

    updated_at = models.DateTimeField(
        auto_now=True
    )

#=================== WEBSITE FEEDBACK =================

class WebsiteFeedback(models.Model):

    CATEGORY_CHOICES = (
        ("General", "General"),
        ("Bug Report", "Bug Report"),
        ("Suggestion", "Suggestion"),
        ("Feature Request", "Feature Request"),
        ("Compliment", "Compliment"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20
    )

    rating = models.IntegerField()

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.category}"
    
#=================== OFFICER DAILY PLANNER =================

class OfficerTask(models.Model):

    officer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    due_date = models.DateField()

    completed = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title
