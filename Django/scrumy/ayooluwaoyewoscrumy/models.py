from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms


# Create your models here.
class GoalStatus(models.Model):
    status_name = models.CharField(max_length=200)
    def __str__(self):
        return self.status_name

class ScrumyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    def __str__(self):
        return self.nickname

    class Meta:
        ordering = ['nickname']


class ScrumyGoals(models.Model):
    visible = models.BooleanField(default=True)
    goal_name = models.CharField(max_length=200)
    goal_id = models.AutoField(primary_key=True)
    created_by = models.CharField(max_length=200)
    moved_by =  models.CharField(max_length=200)
    owner = models.CharField(max_length=200)
    goal_status = models.ForeignKey(GoalStatus, on_delete=models.PROTECT)
    user = models.ForeignKey(ScrumyUser, on_delete=models.CASCADE)
    def __str__(self):
        return self.goal_name

    class Meta:
        ordering = ['-goal_id']
    
        
class ScrumyHistory(models.Model):
    moved_by =  models.CharField(max_length=200)
    created_by = models.CharField(max_length=200)
    moved_from = models.CharField(max_length=200)
    moved_to = models.CharField(max_length=200)
    time_of_action = models.TimeField('time of action')
    goal = models.ForeignKey(ScrumyGoals, on_delete=models.CASCADE)
    def __str__(self):
        return self.moved_by


class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

class CreateGoalForm(ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_name', 'user']

class AddGoalForm(ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_name', 'goal_status']

class WeekOnlyAddGoalForm(ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_name']
class MoveGoalForm(ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_status']

class DevMoveGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[:3]])

    class Meta:
        model = GoalStatus
        fields = ['goal_status']


class AdminPersonalChangeGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[:3]])
    class Meta:
        model = GoalStatus
        fields = ['goal_status']
class OwnerChangeGoalForm(ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_status']
class AdminOthersChangeGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[1:3]])
    class Meta:
        model = GoalStatus
        fields = ['goal_status']

class QADoneChangeGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[:4]])
    class Meta:
        model = GoalStatus
        fields = ['goal_status']
class QAPersonalChangeGoalForm(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset[:4]])
    class Meta:
        model = GoalStatus
        fields = ['goal_status']
class QAVerifyChangegoal(forms.ModelForm):
    queryset = GoalStatus.objects.all()
    goal_status = forms.ChoiceField(choices=[(choice.pk, choice) for choice in queryset.order_by('-id')[:2][::-1]])

    class Meta:
        model = GoalStatus
        fields = ['goal_status']
class QAChangeGoalForm(ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_status', 'user']
