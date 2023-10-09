"""Module for page rendering."""
import json
from django.http import HttpResponseRedirect
#from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from ilmoweb.models import User, Courses, Labs, LabGroups, SignUp
from ilmoweb.forms import NewLabForm
from ilmoweb.logic import labs, signup, labgroups


def home_page_view(request):    # pylint: disable=unused-argument
    """
        Homepage view.

    """
    return render(request, 'home.html')

def database_test_view(request):
    """
        Database test view.
    """
    test_data = User.objects.all()    # pylint: disable=no-member

    return render(request, 'database_test.html', {"users":test_data})

def created_labs(request):
    """
        View for all created labs.
    """
    courses = Courses.objects.all()    # pylint: disable=no-member
    course_id = request.POST.get("course_id")

    if request.user.is_staff is not True:
        return redirect("/open_labs")

    courses = Courses.objects.all()
     
    return render(request, "created_labs.html", {"courses":courses})

def create_lab(request):
    """
        View for creating a new lab.
    """
    if request.method == "POST":
        form = NewLabForm(request.POST)
        course_id = request.POST.get("course_id")

        if form.is_valid():
            content = form.cleaned_data

        labs.create_new_lab(content, course_id)

        return created_labs(request)

    course_id = request.GET.get("course_id")
    form = NewLabForm

    return render(request, "create_lab.html", {"form": form, "course_id": course_id})

def open_labs(request):     # pylint: disable=unused-argument
    """
        View for labs that are open
    """
    courses =  Courses.objects.all()    # pylint: disable=no-member
    course_labs =  Labs.objects.all()    # pylint: disable=no-member
    lab_groups =  LabGroups.objects.all()    # pylint: disable=no-member

    return render(request, 'open_labs.html', {"courses":courses, "labs":course_labs,
                                              "lab_groups":lab_groups})

def delete_lab(request, course_id):
    """
        Delete lab from database.
    """    
    lab = Labs.objects.get(pk=course_id)
    lab.deleted=1
    lab.save()
    courses = Courses.objects.all()

    return render(request, "created_labs.html", {"lab":lab, "courses":courses})

def confirm(request):
    """
        request for confirming a labgroup
    """
    if request.method == "POST":
        group_id = json.loads(request.body)
        labgroups.confirm(group_id)

    return HttpResponseRedirect("/open_labs")