from ayooluwaoyewoscrumy.models import GoalStatus, ScrumyGoals, ScrumyHistory
from django.contrib.auth.models import User, Group, Permission
from .models import ScrumyGoals, GoalStatus, ScrumyUser
from .models import SignUpForm, CreateGoalForm, AddGoalForm, WeekOnlyAddGoalForm,OwnerChangeGoalForm, QAVerifyChangegoal, DevMoveGoalForm, AdminPersonalChangeGoalForm,AdminOthersChangeGoalForm, QADoneChangeGoalForm, QAPersonalChangeGoalForm
from django.contrib.contenttypes.models import ContentType
from django.template import loader
from django.conf import settings
from django.shortcuts import redirect
from django.core import serializers
from .serializers import ScrumGoalSerializer, ScrumUserSerializer
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
import json
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
# Create your views here.

content_type_scrumygoals = ContentType.objects.get_for_model(ScrumyGoals)
content_type_goalstatus = ContentType.objects.get_for_model(GoalStatus)

developergroup = Group.objects.get(name='Developer')
admingroup = Group.objects.get(name='Admin')
qualityassurancegroup = Group.objects.get(name='Quality Assurance')
ownergroup = Group.objects.get(name='Owner')
verifygoal = GoalStatus.objects.get(status_name="Verify Goal")
dailygoal = GoalStatus.objects.get(status_name="Daily Goal")
donegoal = GoalStatus.objects.get(status_name="Done Goal")
weeklygoal = GoalStatus.objects.get(status_name="Weekly Goal")







def index(request):
    form = SignUpForm()
    if request.method == 'GET':
        return render(request, 'ayooluwaoyewoscrumy/index.html', {'form': form})
    elif request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            formdata = request.POST.copy()
            username = formdata.get('username')
            form.save()
            devgroupuser = Group.objects.get(name='Developer')
            user = User.objects.get(username=username)
            devgroupuser.user_set.add(user)
            successful = 'Your account has been created successfully'
            context = {'success': successful}
            return render(request, 'ayooluwaoyewoscrumy/successful.html', context)
    else:
        form = SignUpForm()
        return HttpResponseRedirect(reverse('ayooluwaoyewoscrumyindex:index'))


def scrumygoals(request):
    response = ScrumyGoals.objects.all()
    return HttpResponse(response)


def specificgoal(request):
    response = ScrumyGoals.objects.filter(goal_name='Learn Django')
    return HttpResponse(response)



def move_goals(request, goal_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    current_user = request.user
    usr_grp = request.user.groups.all()[0]
    # goals = get_object_or_404(ScrumyGoals, pk=goal_id)
    try:
        goal = ScrumyGoals.objects.get(pk=goal_id)
    except ObjectDoesNotExist:
        notexist = 'A record with that goal id does not exist'
        context = {'not_exist': notexist}
        return render(request, 'ayooluwaoyewoscrumy/exception.html', context)

    if usr_grp == Group.objects.get(name='Developer'): 
        if current_user == goal.user:
            form = DevMoveGoalForm()

            if request.method == 'GET':
                return render(request, 'ayooluwaoyewoscrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current_user, 'group': usr_grp})

            if request.method == 'POST':
                form = DevMoveGoalForm(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    selected = form.cleaned_data['goal_status']
                    get_status = selected_status.status_name
                    choice = GoalStatus.objects.get(id=int(selected))
                    goal.goal_status = choice
                    goal.save()
                    return HttpResponseRedirect(reverse('ayooluwaoyewoscrumy:homepage'))

            else:
                form = DevMoveGoalForm()
                return render(request, 'ayooluwaoyewoscrumy/movegoal.html',
                          {'form': form, 'goal': goal, 'current_user': current_user,  'group': usr_grp})

        if current_user != goal.user:
            notexist = 'A Developer Cannot move other users goals'
            context = {'not_exist': notexist}
            return render(request, 'ayooluwaoyewoscrumy/exception.html', context)

    if usr_grp == Group.objects.get(name='Admin'):
        if current_user == goal.user:
            form = AdminPersonalChangeGoalForm()

            if request.method == 'GET':
                return render(request, 'ayooluwaoyewoscrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current_user, 'group': usr_grp})
            if request.method == 'POST':
                form = AdminPersonalChangeGoalForm(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    selected = form.cleaned_data['goal_status']
                    get_status = selected_status.status_name
                    choice = GoalStatus.objects.get(id=int(selected))
                    goal.goal_status = choice
                    goal.save()
                    return HttpResponseRedirect(reverse('ayooluwaoyewoscrumy:homepage'))
            else:
                form = AdminPersonalChangeGoalForm()
                return render(request, 'ayooluwaoyewoscrumy/movegoal.html',
                          {'form': form, 'goal': goal, 'current_user': current_user,  'group': usr_grp})
     
        if current_user != goal.user and goal.goal_status == dailygoal or goal.goal_status == verifygoal:
            form = AdminOthersChangeGoalForm()

            if request.method == 'GET':
                return render(request, 'ayooluwaoyewoscrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current_user, 'group': usr_grp})
            if request.method == 'POST':
                form = AdminOthersChangeGoalForm(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    selected = form.cleaned_data['goal_status']
                    get_status = selected_status.status_name
                    choice = GoalStatus.objects.get(id=int(selected))
                    goal.goal_status = choice
                    goal.save()
                    return HttpResponseRedirect(reverse('ayooluwaoyewoscrumy:homepage'))
            else:
                form = AdminOthersChangeGoalForm()
                return render(request, 'ayooluwaoyewoscrumy/movegoal.html',
                          {'form': form, 'goal': goal, 'current_user': current_user,  'group': usr_grp})
    
        if current_user != goal.user and goal.goal_status != dailygoal or goal.goal_status != verifygoal:
            notexist = 'Admin Can Only Move other users goals back and forth from Daily Column to Verify Column'
            context = {'not_exist': notexist}
            return render(request, 'ayooluwaoyewoscrumy/exception.html', context)

    if usr_grp == Group.objects.get(name='Owner'):
        form = OwnerChangeGoalForm()

        if request.method == 'GET':
            return render(request, 'ayooluwaoyewoscrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current_user, 'group': usr_grp})
        if request.method == 'POST':
                form = OwnerChangeGoalForm(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    get_status = selected_status.goal_status
                    goal.goal_status = get_status
                    goal.save()
                    return HttpResponseRedirect(reverse('ayooluwaoyewoscrumy:homepage'))
        else:
            form = OwnerChangeGoalForm()
            return render(request, 'ayooluwaoyewoscrumy/movegoal.html',
                          {'form': form, 'goal': goal, 'current_user': current_user,  'group': usr_grp})
    
    
    if usr_grp == Group.objects.get(name='Quality Assurance'):
        if goal.goal_status == verifygoal:
            form = QAVerifyChangegoal()

            if request.method == 'GET':
                return render(request, 'ayooluwaoyewoscrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current_user, 'group': usr_grp})
            if request.method == 'POST':
                form = QAVerifyChangegoal(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    selected = form.cleaned_data['goal_status']
                    get_status = selected_status.status_name
                    choice = GoalStatus.objects.get(id=int(selected))
                    goal.goal_status = choice
                    goal.save()
                    return HttpResponseRedirect(reverse('ayooluwaoyewoscrumy:homepage'))
            else:
                form = QAVerifyChangegoal()
                return render(request, 'ayooluwaoyewoscrumy/movegoal.html',
                              {'form': form, 'goal': goal, 'currentuser': current_user, 'group': usr_grp})

        if goal.goal_status == donegoal:
            form = QADoneChangeGoalForm()
            if request.method == 'GET':
                return render(request, 'ayooluwaoyewoscrumy/movegoal.html', {'form': form, 'goal': goal, 'currentuser': current_user, 'group': usr_grp})
            if request.method == 'POST':
                form = QADoneChangeGoalForm(request.POST)
                if form.is_valid():
                    selected_status = form.save(commit=False)
                    selected = form.cleaned_data['goal_status']
                    get_status = selected_status.status_name
                    choice = GoalStatus.objects.get(id=int(selected))
                    goal.goal_status = choice
                    goal.save()
                    return HttpResponseRedirect(reverse('ayooluwaoyewoscrumy:homepage'))

            else:
                form = QADoneChangeGoalForm()
                return render(request, 'ayooluwaoyewoscrumy/movegoal.html',
                              {'form': form, 'goal': goal, 'currentuser': current_user, 'group': usr_grp})
        if goal.goal_status != verifygoal or goal.goal_status != donegoal and current_user != goal.user:
            notexist = 'Quality assurance Can Only Move other users goals from Verify Column to Done Column, and from Done Column to other columns'
            context = {'not_exist': notexist}
            return render(request, 'ayooluwaoyewoscrumy/exception.html', context)



def add_goal(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    form = CreateGoalForm()
    if request.method == 'GET':
        return render(request, 'ayooluwaoyewoscrumy/addgoal.html', {'form': form})
    elif request.method == 'POST':
        form = CreateGoalForm(request.POST)
        post = form.save(commit=False)
        goal_id = randint(1000, 9999)
        status_name = GoalStatus(id=1)
        post.created_by = "Louis"
        post.moved_by = "Louis"
        post.owner = "Louis"
        post.goal_id = goal_id
        post.goal_status = status_name
        post.save()
    else:
        form = CreateGoalForm()
    return HttpResponseRedirect(reverse('ayooluwaoyewoscrumy:addgoal'))


def home(request):
    scrumygoal = ScrumyGoals.objects.filter(goal_name='Keep Learning Django')
    output = ', '.join([eachgoal.goal_name for eachgoal in scrumygoal])
    return HttpResponse(output)


def homepage(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = User.objects.all()
    current_user = request.user
    group = current_user.groups.values_list('name', flat=True)[0]
    weeklygoal = GoalStatus.objects.get(status_name="Weekly Goal")
    wg = weeklygoal.scrumygoals_set.all()
    dailygoal = GoalStatus.objects.get(status_name="Daily Goal")
    dg = dailygoal.scrumygoals_set.all()
    verifygoal = GoalStatus.objects.get(status_name="Verify Goal")
    vg = verifygoal.scrumygoals_set.all()
    donegoal = GoalStatus.objects.get(status_name="Done Goal")
    gd = donegoal.scrumygoals_set.all()

    if current_user.is_authenticated:
        if group == 'Developer' or group == 'Owner' or group == 'Quality Assurance':
            form = WeekOnlyAddGoalForm()
            context = {'user': user, 'weeklygoal': wg, 'dailygoal': dg, 'verifygoal': vg,
                       'donegoal': gd, 'form': form, 'currentuser': current_user.username, 'group': group}
            if request.method == 'GET':
                return render(request, 'ayooluwaoyewoscrumy/home.html', context)
            if request.method == 'POST':
                form = WeekOnlyAddGoalForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    goal_id = randint(1000, 9999)
                    post.moved_by = current_user.first_name
                    post.owner = current_user.first_name
                    post.goal_id = goal_id
                    post.goal_status = weeklygoal
                    post.user = current_user
                    post.save()

            else:
                form = WeekOnlyAddGoalForm()
            return HttpResponseRedirect(reverse('ayooluwaoyewoscrumy:homepage'))
        if group == 'Admin':
            context = {'user': user, 'weeklygoal': wg, 'dailygoal': dg, 'verifygoal': vg,
                       'donegoal': gd, 'currentuser': current_user.username, 'group': group}
            if request.method == 'GET':
                return render(request, 'ayooluwaoyewoscrumy/home.html', context)
            
               




#Using serializers and views in django rest framework    

class ScrumUserViewSet(viewsets.ModelViewSet):
    queryset = ScrumyUser.objects.all()
    serializer_class = ScrumUserSerializer

    def create(self, request):
        password = request.data['password']
        confirmpassword = request.data['confirmpassword']
        role = request.data['role']
        fullname = request.data['fullname']
        username = request.data['username']

        if password == '' and role == '' and fullname == '' and username == '':
            return JsonResponse({'message': 'Error: All fields are required.'})
        if password != confirmpassword:
            return JsonResponse({'message': 'Error: Password Do not match.'})
        user, created = User.objects.get_or_create(username = request.data['username'])
        if created:
            user.set_password(password)
            group = Group.objects.get(name = request.data['role'])
            group.user_set.add(user)
            user.save()
            scrum_user = ScrumyUser(user=user, nickname=request.data['fullname'])
            scrum_user.save()
            return JsonResponse({'message': 'User Created Successfully'})
        else:
            return JsonResponse({'message': 'Error: Username Already Exists.'})



def filtered_users():
    users = ScrumUserSerializer(ScrumyUser.objects.all(), many=True).data

    for user in users:
        user['scrumygoals_set'] = [x for x in user['scrumygoals_set']
         if x['visible'] == True]
    return users

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     def create(self, request):
#         username = request.data['username']
#         password = request.data['password']

#         login_user = authenticate(request, username=username, password=password)
#         if login_user is not None:
#             return JsonResponse({'exit': 0, 'message': 'Welcome to your Scrum Board', 'role': login_user.groups.all()[0].name, 'data': filtered_users()})
#         else: 
#             return JsonResponse({'exit': 1, 'message': 'Error: Invalid Credentials'})



class ScrumGoalViewSet(viewsets.ModelViewSet):
    queryset = ScrumyGoals.objects.all()
    serializer_class = ScrumGoalSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    def create(self, request):
            goal_name = request.data['goal_name']
            group_name = request.user.groups.all()[0].name 
            status_name = GoalStatus(id=1)
            if group_name == 'Admin':
                status_name = GoalStatus(id=2)
                 
            elif group_name == 'Quality Assurance':
                status_name = GoalStatus(id=3)
                
            goal = ScrumyGoals(user=request.user.scrumyuser, goal_name = goal_name, goal_status = status_name)
            goal.save()
            return JsonResponse({ 'message': 'Goal Added', 'data': filtered_users()})
        
    
    def patch(self, request):
            goals_id = request.data['goal_id']
            to_id = request.data['to_id']
            print(to_id)

            if to_id == 4:
                if request.user.groups.all()[0].name == 'Developer':
                    if request.user != ScrumyGoals.objects.get(goal_id=goals_id).user.user:
                        return JsonResponse({ 'message': 'Permission Denied: Unauthorized Deletion of Goal.', 'data': filtered_users()})
                
                del_goal = ScrumyGoals.objects.get(goal_id = goals_id)
                del_goal.visible = False
                del_goal.save()
                return JsonResponse({'message': 'Goal Removed Successfully', 'data': filtered_users()})
            else:
                goal_item = ScrumyGoals.objects.get(goal_id=goals_id)
                print(goal_item)
                group = request.user.groups.all()[0].name
                print(group)
                from_allowed = []
                to_allowed = []

                if group == 'Developer':

                    if request.user != goal_item.user.user:
                        return JsonResponse({'message': 'Permission Denied: Unauthorized Deletion of Goal.', 'data': filtered_users()})

                if group == 'Owner':
                    from_allowed = [1,2,3,4]
                    to_allowed = [0,1,2,3]
                
                elif  group == 'Admin':
                    from_allowed = [2,3]
                    to_allowed = [1,2]


                elif  group == 'Developer':
                    from_allowed = [1,2]
                    to_allowed = [0,1]
                
                if (goal_item.goal_status_id in from_allowed) and (to_id in to_allowed):
                    # choice = GoalStatus.objects.get(id=to_id)
                    if to_id >= 0:
                        goal_item.goal_status_id = to_id  + 1
                    
                    



                elif group == 'Quality Assurance' and goal_item.goal_status_id == 3 and to_id == 0:
                    goal_item.goal_status_id = to_id + 1

                else: 
                    return JsonResponse({ 'message': 'Permission Denied: Unauthorized Movement of Goal.', 'data': filtered_users()})   

                goal_item.save()  
                return JsonResponse({ 'message': 'Goal Moved Successfully', 'data': filtered_users()})   

       

    def put(self, request):
        if request.data['mode'] == 0:
            from_id = request.data['from_id']
            to_id = request.data['to_id']
            if request.user.groups.all()[0].name == 'Developer' or request.user.groups.all()[0].name == 'Quality Assurance':
                return JsonResponse({'message': 'Permission Denied: Unauthorized Reassignment of Goal.', 'data': filtered_users()})   
        
            goal = ScrumyGoals.objects.get(goal_id=from_id)
            author = None
            if to_id[0] == 'u':
                author = ScrumyUser.objects.get(id =  to_id[1:])
            else:
                author = ScrumyGoals.objects.get(goal_id=to_id).user
            goal.user = author
            goal.save()
            return JsonResponse({'message': 'Goal Reassigned Successfully.', 'data': filtered_users()})
        else:
            goal = ScrumyGoals.objects.get(goal_id = request.data['goal_id'])
            if request.user.groups.all()[0].name != 'Owner' or request.user != goal.user.user:
                return JsonResponse({'message': 'Permission Denied: Unauthorized Goal Name Change', 'data': filtered_users()})
            
            goal.goal_name = request.data['new_name']
            print(goal);
            goal.save()
            return JsonResponse({'message': 'Goal Name Changed Successfully.', 'data': filtered_users()})


def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'role': user.groups.all()[0].name,
            'message': 'Welcome!',
            'data': filtered_users()
        }