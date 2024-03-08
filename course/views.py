from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Avg, Max, Min, Count
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.core.paginator import Paginator
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django_filters.views import FilterView
from django.db.models import Q
from django.http import HttpResponse
from accounts.models import User, Student
from core.models import Session, Semester
from course.models import TakenCourse
from accounts.decorators import lecturer_required, student_required
from .forms import (
    ProgramForm,
    CourseAddForm,
    CourseAllocationForm,
    EditCourseAllocationForm,
    UploadFormFile,
    UploadFormVideo,
    CourseAddFeedback
)
from .filters import ProgramFilter, CourseAllocationFilter
from .models import Program, Course, CourseAllocation, Upload, UploadVideo,Course_feedback


@method_decorator([login_required(login_url='login')], name="dispatch")
class ProgramFilterView(FilterView):
    filterset_class = ProgramFilter
    template_name = "course/program_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Programs"
        return context

#####################################################################################################
# Admin can only create,edit and delete programs
#####################################################################################################
@login_required(login_url='login')
@lecturer_required
def program_add(request):
    if request.method == "POST":
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, request.POST.get("title") + " program has been created."
            )
            return redirect("programs")
        else:
            messages.error(request, "Correct the error(S) below.")
    else:
        form = ProgramForm()

    return render(
        request,
        "course/program_add.html",
        {
            "title": "Add Program",
            "form": form,
        },
    )


@login_required(login_url='login')
def program_detail(request, pk):
    program = Program.objects.get(pk=pk)
    courses = Course.objects.filter(program_id=pk).order_by("-year")
    credits = Course.objects.aggregate(Sum("credit"))

    paginator = Paginator(courses, 10)
    page = request.GET.get("page")

    courses = paginator.get_page(page)
    

    return render(
        request,
        "course/program_single.html",
        {
            "title": program.title,
            "program": program,
            "courses": courses,
            "credits": credits,
        },
    )


@login_required(login_url='login')
@lecturer_required
def program_edit(request, pk):
    program = Program.objects.get(pk=pk)

    if request.method == "POST":
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            messages.success(
                request, str(request.POST.get("title")) + " program has been updated."
            )
            return redirect("programs")
    else:
        form = ProgramForm(instance=program)

    return render(
        request,
        "course/program_add.html",
        {"title": "Edit Program", "form": form},
    )


@login_required(login_url='login')
@lecturer_required
def program_delete(request, pk):
    program = Program.objects.get(pk=pk)
    title = program.title
    program.delete()
    messages.success(request, "Program " + title + " has been deleted.")

    return redirect("programs")


# ########################################################


# ########################################################
# Course views
# Lecturer and admins can create program courses
# ########################################################
@login_required(login_url='login')
def course_single(request, slug):
    course = Course.objects.get(slug=slug)
    files = Upload.objects.filter(course__slug=slug)
    videos = UploadVideo.objects.filter(course__slug=slug)

    

    lecturers = CourseAllocation.objects.filter(courses__pk=course.id).first()
    all_lecturers=CourseAllocation.objects.filter(courses__pk=course.id)

  

    return render(
        request,
        "course/course_single.html",
        {
            "title": course.title,
            "course": course,
            "files": files,
            "videos": videos,
            "lecturers": lecturers,
            "all_lecturers":all_lecturers,
            "media_url": settings.MEDIA_ROOT,
        },
    )


@login_required(login_url='login')
@lecturer_required
def course_add(request, pk):
    users = User.objects.all()
    if request.method == "POST":
        form = CourseAddForm(request.POST)
        course_name = request.POST.get("title")
        course_code = request.POST.get("code")
        get_semester=request.POST.get('semester')
        if form.is_valid():
            
            form.save()
            
            get_session_name = request.POST.get('session')
            filter_session=Session.objects.filter(session=get_session_name,is_current_session=True)
            if filter_session.exists():
            
                get_session_model=Session.objects.get(session=get_session_name,is_current_session=True)
                semester_create,get=Semester.objects.get_or_create(semester=request.POST.get('semester'),is_current_semester=True,session=get_session_model)

                get_course_model = Course.objects.get(title=course_name, code=course_code)
                course_allocate_user = CourseAllocation(lecturer=request.user, session=get_session_model)
                course_allocate_user.save()
                course_allocate_user.courses.add(get_course_model)
            else:
                new_session=Session.objects.create(session=get_session_name,is_current_session=True)
                semester_create,grab=Semester.objects.get_or_create(semester=request.POST.get('semester'),is_current_semester=True,session=new_session)
                get_course_model = Course.objects.get(title=course_name, code=course_code)
                
                course_allocate_user = CourseAllocation(lecturer=request.user, session=new_session)
                course_allocate_user.save()
                course_allocate_user.courses.add(get_course_model)
            
                
            
            messages.success(
                request, (course_name + "(" + course_code + ")" + " has been created.")
            )
            
            return redirect("program_detail", pk=request.POST.get("program"))
        else:
            messages.error(request, "Correct the error(s) below.")
    else:
        form = CourseAddForm(initial={"program": Program.objects.get(pk=pk)})

    return render(
        request,
        "course/course_add.html",
        {
            "title": "Add Course",
            "form": form,
            "program": pk,
            "users": users,
        },
    )





#####################################################################################################
# Students can leave feedbacks to courses but only the lecturer that can delete them
#####################################################################################################
@login_required(login_url='login')
def course_feedback(request, pk):
    if request.method == "POST":
        form = CourseAddFeedback(request.POST)
        get_course=Course.objects.get(id=pk)
        course_slug=get_course.slug
        if form.is_valid():
            save_feedback=form.save(commit=False)
            save_feedback.user=request.user
            save_feedback.course=get_course
            save_feedback.save()
            messages.success(
                request, ("Your feedback has been saved.")
            )
            return redirect("course_detail", slug=course_slug)
        else:
            messages.error(request, "Correct the error(s) below.")
    else:
        form = CourseAddFeedback()

    return render(
        request,
        "course/course_feedback.html",
        {
            "title": "Course Feedback",
            "form": form,
        },
    )
@login_required(login_url='login')
@lecturer_required
def check_feedbacks(request,id):
    get_course=Course.objects.get(id=id)
    feed_response=Course_feedback.objects.filter(course=get_course)
    context = {
        'feedback': feed_response  # Corrected from '{'feedback', feed_response}' to '{'feedback': feed_response}'
    }
    return render(request,'course/course_feedback_list.html',context)


@login_required(login_url='login')
@lecturer_required
def delete_feedbacks(request,id):
    get_feedback=Course_feedback.objects.get(pk=id)
    get_feedback.delete()
    messages.success(request,'Feedback deleted')
    return redirect('check_feedbacks',id=get_feedback.course.pk)





#####################################################################################################
# Lecturers and admin can edit and delete their courses
#####################################################################################################
@login_required(login_url='login')
@lecturer_required
def course_edit(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.method == "POST":
        form = CourseAddForm(request.POST, instance=course)
        course_name = request.POST.get("title")
        course_code = request.POST.get("code")
        if form.is_valid():
            form.save()
            messages.success(
                request, (course_name + "(" + course_code + ")" + " has been updated.")
            )
            return redirect("program_detail", pk=request.POST.get("program"))
        else:
            messages.error(request, "Correct the error(s) below.")
    else:
        form = CourseAddForm(instance=course)

    return render(
        request,
        "course/course_add.html",
        {
            "title": "Edit Course",
            # 'form': form, 'program': pk, 'course': pk
            "form": form,
        },
    )


@login_required(login_url='login')
@lecturer_required
def course_delete(request, slug):
    course = Course.objects.get(slug=slug)
    # course_name = course.title
    course.delete()
    messages.success(request, "Course " + course.title + " has been deleted.")

    return redirect("program_detail", pk=course.program.pk)





# ########################################################
# Lecturers who create a specific course gets the course allocated to them and admin can also allocate course to othe lecturers
# ########################################################
@method_decorator([login_required(login_url='login')], name="dispatch")
class CourseAllocationFormView(CreateView):
    form_class = CourseAllocationForm
    template_name = "course/course_allocation_form.html"

    def get_form_kwargs(self):
        kwargs = super(CourseAllocationFormView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        lecturer = form.cleaned_data["lecturer"]
        selected_courses = form.cleaned_data["courses"]
        courses = ()
        for course in selected_courses:
            courses += (course.pk,)

        try:
            a = CourseAllocation.objects.get(lecturer=lecturer)
        except:
            a = CourseAllocation.objects.create(lecturer=lecturer)
        for i in range(0, selected_courses.count()):
            a.courses.add(courses[i])
            a.save()
        return redirect("course_allocation_view")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Assign Course"
        return context


@method_decorator([login_required(login_url='login')], name="dispatch")
class CourseAllocationFilterView(FilterView):
    filterset_class = CourseAllocationFilter
    template_name = "course/course_allocation_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Course Allocations"
        return context


@login_required(login_url='login')
@lecturer_required
def edit_allocated_course(request, pk):
    allocated = get_object_or_404(CourseAllocation, pk=pk)
    if request.method == "POST":
        form = EditCourseAllocationForm(request.POST, instance=allocated)
        if form.is_valid():
            form.save()
            messages.success(request, "course assigned has been updated.")
            return redirect("course_allocation_view")
    else:
        form = EditCourseAllocationForm(instance=allocated)

    return render(
        request,
        "course/course_allocation_form.html",
        {"title": "Edit Course Allocated", "form": form, "allocated": pk},
    )

#####################################################################################################
# Admin and lecturers can remove other lecturers from a course...
# Note:Only the lecturer that created the course and the admin
# that can add and delete other lecturers
#####################################################################################################
@login_required(login_url='login')
@lecturer_required
def deallocate_course(request, pk):
    course = CourseAllocation.objects.get(pk=pk)
    course.delete()
    messages.success(request, "successfully deallocate!")
    return redirect("course_allocation_view")


# ########################################################


# ########################################################
# File Upload views
# ########################################################
@login_required(login_url='login')
@lecturer_required
def handle_file_upload(request, slug):
    course = Course.objects.get(slug=slug)
    if request.method == "POST":
        form = UploadFormFile(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.course = course
            obj.save()

            messages.success(
                request, (request.POST.get("title") + " has been uploaded.")
            )
            return redirect("course_detail", slug=slug)
    else:
        form = UploadFormFile()
    return render(
        request,
        "upload/upload_file_form.html",
        {"title": "File Upload", "form": form, "course": course},
    )


@login_required(login_url='login')
@lecturer_required
def handle_file_edit(request, slug, file_id):
    course = Course.objects.get(slug=slug)
    instance = Upload.objects.get(pk=file_id)
    if request.method == "POST":
        form = UploadFormFile(request.POST, request.FILES, instance=instance)
        # file_name = request.POST.get('name')
        if form.is_valid():
            form.save()
            messages.success(
                request, (request.POST.get("title") + " has been updated.")
            )
            return redirect("course_detail", slug=slug)
    else:
        form = UploadFormFile(instance=instance)

    return render(
        request,
        "upload/upload_file_form.html",
        {"title": instance.title, "form": form, "course": course},
    )


def handle_file_delete(request, slug, file_id):
    file = Upload.objects.get(pk=file_id)
    # file_name = file.name
    file.delete()

    messages.success(request, (file.title + " has been deleted."))
    return redirect("course_detail", slug=slug)


# ########################################################
# Video Upload views
# ########################################################
@login_required(login_url='login')
@lecturer_required
def handle_video_upload(request, slug):
    course = Course.objects.get(slug=slug)
    if request.method == "POST":
        form = UploadFormVideo(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.course = course
            obj.save()

            messages.success(
                request, (request.POST.get("title") + " has been uploaded.")
            )
            return redirect("course_detail", slug=slug)
    else:
        form = UploadFormVideo()
    return render(
        request,
        "upload/upload_video_form.html",
        {"title": "Video Upload", "form": form, "course": course},
    )


@login_required(login_url='login')
# @lecturer_required
def handle_video_single(request, slug, video_slug):
    course = get_object_or_404(Course, slug=slug)
    video = get_object_or_404(UploadVideo, slug=video_slug)
    return render(request, "upload/video_single.html", {"video": video})


@login_required(login_url='login')
@lecturer_required
def handle_video_edit(request, slug, video_slug):
    course = Course.objects.get(slug=slug)
    instance = UploadVideo.objects.get(slug=video_slug)
    if request.method == "POST":
        form = UploadFormVideo(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(
                request, (request.POST.get("title") + " has been updated.")
            )
            return redirect("course_detail", slug=slug)
    else:
        form = UploadFormVideo(instance=instance)

    return render(
        request,
        "upload/upload_video_form.html",
        {"title": instance.title, "form": form, "course": course},
    )


def handle_video_delete(request, slug, video_slug):
    video = get_object_or_404(UploadVideo, slug=video_slug)
    # video = UploadVideo.objects.get(slug=video_slug)
    video.delete()

    messages.success(request, (video.title + " has been deleted."))
    return redirect("course_detail", slug=slug)



# ########################################################
#Students Course Registration
# ########################################################
@login_required(login_url='login')
@student_required
def course_registration(request):
    if request.method == "POST":
        student = Student.objects.get(student__pk=request.user.id)
        ids = ()
        data = request.POST.copy()
        data.pop("csrfmiddlewaretoken", None)  # remove csrf_token
        for key in data.keys():
            ids = ids + (str(key),)
        for s in range(0, len(ids)):
            course = Course.objects.get(pk=ids[s])
            obj = TakenCourse.objects.create(student=student, course=course)
            obj.save()
        messages.success(request, "Courses registered successfully!")
        return redirect("course_registration")
    else:
        current_semester = Semester.objects.filter(is_current_semester=True).first()
        if not current_semester:
            messages.error(request, "No active semester found.")
            return render(request, "course/course_registration.html")

        # student = Student.objects.get(student__pk=request.user.id)
        student = get_object_or_404(Student, student__id=request.user.id)
        taken_courses = TakenCourse.objects.filter(student__student__id=request.user.id)
        t = ()
        for i in taken_courses:
            t += (i.course.pk,)

        courses = (
            Course.objects.filter(
                program__pk=student.program.id,
                level=student.level,
                semester=current_semester,
            )
            .exclude(id__in=t)
            .order_by("year")
        )
        all_courses = Course.objects.filter(
            level=student.level, program__pk=student.program.id
        )

        no_course_is_registered = False  # Check if no course is registered
        all_courses_are_registered = False

        registered_courses = Course.objects.filter(level=student.level).filter(id__in=t)
        if (
            registered_courses.count() == 0
        ):  # Check if number of registered courses is 0
            no_course_is_registered = True

        if registered_courses.count() == all_courses.count():
            all_courses_are_registered = True

        total_first_semester_credit = 0
        total_sec_semester_credit = 0
        total_registered_credit = 0
        for i in courses:
            if i.semester == "First":
                total_first_semester_credit += int(i.credit)
            if i.semester == "Second":
                total_sec_semester_credit += int(i.credit)
        for i in registered_courses:
            total_registered_credit += int(i.credit)
        context = {
            "is_calender_on": True,
            "all_courses_are_registered": all_courses_are_registered,
            "no_course_is_registered": no_course_is_registered,
            "current_semester": current_semester,
            "courses": courses,
            "total_first_semester_credit": total_first_semester_credit,
            "total_sec_semester_credit": total_sec_semester_credit,
            "registered_courses": registered_courses,
            "total_registered_credit": total_registered_credit,
            "student": student,
        }
        return render(request, "course/course_registration.html", context)

#####################################################################################################
# Students can drop specific courses
#####################################################################################################
@login_required(login_url='login')
@student_required
def course_drop(request):
    if request.method == "POST":
        student = Student.objects.get(student__pk=request.user.id)
        ids = ()
        data = request.POST.copy()
        data.pop("csrfmiddlewaretoken", None)  # remove csrf_token
        for key in data.keys():
            ids = ids + (str(key),)
        for s in range(0, len(ids)):
            course = Course.objects.get(pk=ids[s])
            obj = TakenCourse.objects.get(student=student, course=course)
            obj.delete()
        messages.success(request, "Successfully Dropped!")
        return redirect("course_registration")




#####################################################################################################
# Students can see courses they enroll to,while lecturers can see the courses they created
#####################################################################################################
@login_required(login_url='login')
def user_course_list(request):
    if request.user.is_lecturer:
        courses = Course.objects.filter(allocated_course__lecturer__pk=request.user.id).order_by('-pk')
        all_courses=Course.objects.all().order_by('-pk')

        return render(request, "course/user_course_list.html", {"courses": courses,"all_courses":all_courses})

    elif request.user.is_student:
        student = Student.objects.get(student__pk=request.user.pk)
        taken_courses = TakenCourse.objects.filter(
            student__student__id=student.student.pk
        )
        courses = Course.objects.filter(level=student.level).filter(
            program__pk=student.program.pk
        )
        all_courses=Course.objects.all().order_by('-pk')

        return render(
            request,
            "course/user_course_list.html",
            {"student": student, "taken_courses": taken_courses,"courses": courses,"all_courses":all_courses},
        )

    else:
        return render(request, "course/user_course_list.html")
    


#################################################################################################################
# Lecturer can see students that enroll in his/her course
#####################################################################################################
def lecturer_course_list(request,course_id):
    if request.user.is_lecturer:
        get_lecturer_courses = CourseAllocation.objects.filter(lecturer=request.user)
        students = []

        for course_allocation in get_lecturer_courses:
            course_taken_by_student = TakenCourse.objects.filter(course__in=course_allocation.courses.all())
            course_id=course_allocation.pk
            students.extend(course_taken_by_student)
        return render(request, 'course/student_course_list.html', {'students': students,'lecturers':get_lecturer_courses,'course_id':course_id})

#################################################################################################################
# Lecturer can remove student from specfic courses
#####################################################################################################
def remove_student(request, username, course_id):
    course = get_object_or_404(Course, id=course_id)

    get_lecturer_course = get_object_or_404(CourseAllocation, courses=course)


    user = get_object_or_404(User, username=username)

    student = get_object_or_404(Student, student=user)

    get_student = get_object_or_404(TakenCourse, course=course, student=student)
    get_student.delete()

    messages.success(request, f'You removed {username} from this course')
    return redirect('enrolled_student',course_id=course_id)



#################################################################################################################
# Lecturer can add student to specfic courses
#####################################################################################################
def add_student(request, course_id):
    if request.method == 'POST':
        username = request.POST.get('username')

        # Get the CourseAllocation object based on the course_id
        course_allocation = get_object_or_404(CourseAllocation, pk=course_id)

        # Get the courses associated with the CourseAllocation
        courses = course_allocation.courses.all()

        # Get the Student object based on the username
        student = get_object_or_404(Student, student__username=username)

        # Check if the student is already enrolled in any of the courses
        if TakenCourse.objects.filter(course__in=courses, student=student).exists():
            messages.warning(request, f'{username} is already enrolled in one of these courses.')
            return redirect('enrolled_student', course_id=course_id)
        
        # Add the student to each course
        for course in courses:
            TakenCourse.objects.create(course=course, student=student)
        
        messages.success(request, f'{username} successfully added to the courses.')
        return redirect('enrolled_student', course_id=course_id)
    else:
        return HttpResponse('Not a POST method')
