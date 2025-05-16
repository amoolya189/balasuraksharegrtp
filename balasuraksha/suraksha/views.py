from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from .models import IncidentReport, CustomUser
from .forms import ReportForm

# Home and Static Pages
def index(request):
    return render(request, 'suraksha/index.html')

def home(request):
    return render(request, 'suraksha/home.html')

def logocover(request):
    return render(request, 'suraksha/logocover.html')

def help_line(request):
    return render(request, 'suraksha/help_line.html')

def map_view(request):
    return render(request, 'suraksha/map.html')

def support(request):
    return render(request, 'suraksha/support.html')

def general_discussion(request):
    return render(request, 'suraksha/general-discussion.html')

def video_tutorials(request):
    return render(request, 'suraksha/video.html')

# Story Pages
def story_view(request): return render(request, 'suraksha/story.html')
def story_view1(request): return render(request, 'suraksha/story1.html')
def story_view2(request): return render(request, 'suraksha/story2.html')
def story_view3(request): return render(request, 'suraksha/story3.html')
def story_view4(request): return render(request, 'suraksha/story4.html')
def story_view5(request): return render(request, 'suraksha/story5.html')
def story_view6(request): return render(request, 'suraksha/story6.html')
def story_view7(request): return render(request, 'suraksha/story7.html')
def story_view8(request): return render(request, 'suraksha/story8.html')
def story_view9(request): return render(request, 'suraksha/story9.html')
def story_view10(request): return render(request, 'suraksha/story10.html')

# Authentication
def login_register_view(request):
    if request.method == "POST":
        # Login
        if "login" in request.POST:
            username = request.POST.get("login-username")
            password = request.POST.get("login-password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")

        # Registration
        elif "register" in request.POST:
            username = request.POST.get("register-username")
            email = request.POST.get("register-email")
            password1 = request.POST.get("register-password1")
            password2 = request.POST.get("register-password2")
            role = request.POST.get("register-role")

            if password1 != password2:
                messages.error(request, "Passwords do not match.")
            elif User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                messages.success(request, "Registration successful. You can now log in.")

    return render(request, "suraksha/login.html")

def logout_view(request):
    logout(request)
    return redirect('logocover')

# Incident Reporting
def report_incident(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')
    else:
        form = ReportForm()
    return render(request, 'suraksha/report_incident.html', {'form': form})

def user_dashboard(request):
    reports = IncidentReport.objects.all()
    return render(request, 'suraksha/user_dashboard.html', {'reports': reports})

@csrf_exempt
def send_report(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        relationship = request.POST.get('relationship')
        victim_name = request.POST.get('victimName')
        location = request.POST.get('location')
        description = request.POST.get('description')
        proof_file = request.FILES.get('proofFiles[]')

        IncidentReport.objects.create(
            name=name,
            email=email,
            relationship=relationship,
            victim_name=victim_name,
            location=location,
            description=description,
            proof_files=proof_file
        )

        return JsonResponse({'message': 'Report submitted successfully!'})
    return JsonResponse({'error': 'Invalid method'}, status=400)

# Email Notification to Parents
def report_issue(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            victim_email = request.user.email  # From logged-in user
            parent_email = form.cleaned_data['parent_email']
            message = form.cleaned_data['message']

            subject = "A Message Regarding Your Child"
            body = f"This message was submitted by {victim_email}:\n\n{message}"

            try:
                send_mail(
                    subject,
                    body,
                    settings.EMAIL_HOST_USER,
                    [parent_email],
                    fail_silently=False,
                )
                return render(request, 'suraksha/report_success.html', {'parent_email': parent_email})
            except Exception as e:
                return render(request, 'suraksha/report_issue.html', {
                    'form': form,
                    'error': f"Failed to send email: {str(e)}"
                })
    else:
        form = ReportForm()

    return render(request, 'suraksha/report_issue.html', {'form': form})

 