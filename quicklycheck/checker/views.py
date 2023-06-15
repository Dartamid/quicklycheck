from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect, get_object_or_404
from .models import Class, Student, Test, Pattern, Blank
from io import BytesIO

# Create your views here.
from .forms import ClassForm, StudentForm, TestForm, PatternForm
from .utils import checker


def index(request):
    return render(request, 'index.html')


@login_required()
def list_classes(request):
    user = request.user
    classes = Class.objects.filter(teacher=user)
    context = {
        'classes': classes,
    }
    return render(
        request,
        'list_classes.html',
        context
    )


@login_required()
def add_class(request):
    view_template = 'add_class.html'
    form = ClassForm()
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            grade = Class(teacher=request.user, number=data['number'], letter=data['letter'])
            grade.save()
            return redirect('myclasses')
        context = {
            'form': form,
        }
    return render(
        request,
        view_template,
        context
    )


@login_required()
def class_detail(request, class_pk):
    grade = get_object_or_404(Class, pk=class_pk)
    template_view = 'class_detail.html'
    context = {
        'class': grade
    }
    return render(
        request,
        template_view,
        context
    )


@login_required()
def add_student(request, class_pk):
    view_template = 'add_student.html'
    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            grade = get_object_or_404(Class, pk=class_pk)
            student = Student(name=data['name'], teacher=request.user, grade=grade)
            student.save()
            return redirect('class_detail', class_pk)
    context = {
        'form': form,
        'class_pk': class_pk,
    }
    return render(
        request,
        view_template,
        context
    )


@login_required()
def add_test(request, class_pk):
    view_template = 'add_test.html'
    form = TestForm()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            grade = get_object_or_404(Class, pk=class_pk)
            student = Test(name=data['name'], teacher=request.user, grade=grade)
            student.save()
            return redirect('class_detail', class_pk)
    context = {
        'form': form,
        'class_pk': class_pk,
    }
    return render(
        request,
        view_template,
        context
    )


@login_required()
def add_pattern(request, test_pk):
    view_template = 'add_pattern.html'
    form = PatternForm()
    if request.method == 'POST':
        form = PatternForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            test = get_object_or_404(Test, pk=test_pk)
            pattern = Pattern(num=data['num'], pattern=data['pattern'], test=test)
            pattern.save()
            return redirect('class_detail', test_pk)
    context = {
        'form': form,
        'test_pk': test_pk,
    }
    return render(
        request,
        view_template,
        context
    )


@login_required()
def test_detail(request, test_pk):
    test = get_object_or_404(Test, pk=test_pk)
    template_view = 'test_detail.html'
    context = {
        'test': test
    }
    return render(
        request,
        template_view,
        context
    )


@login_required()
def add_blanks(request, test_pk):
    view_template = 'add_blanks.html'
    test = get_object_or_404(Test, pk=test_pk)
    student = get_object_or_404(Student, pk=1)
    if request.method == "POST":
        images = request.FILES.getlist('images')
        for image in images:
            results, image = checker(image.temporary_file_path())
            bytes_io = BytesIO()
            image.save(bytes_io, format='JPEG')
            file = InMemoryUploadedFile(
                bytes_io, None, 'image.jpg', 'image/jpeg',
                bytes_io.getbuffer().nbytes, None
            )
            blank = Blank.objects.create(
                test=test,
                author=test.grade.students.all()[int(results['blank_id'])-1],
                var=int(results['var']),
                id_blank=results['blank_id'],
                answers=','.join(results['answers'].values()),
                image=file
            )
        return redirect('myclasses')
    context = {
        'test_pk': test_pk,
    }
    return render(
        request,
        view_template,
        context
    )


@login_required()
def blank_detail(request, blank_pk):
    template_view = 'blank_detail.html'
    blank = get_object_or_404(Blank, pk=blank_pk)
    pattern = blank.test.patterns.filter(num=blank.var)[0]
    answers = blank.answers.split(',')
    pattern = pattern.pattern.split(',')
    print(answers, pattern)
    result = []
    count = 0
    for i in range(len(pattern)):
        if pattern[i] == answers[i]:
            result += [f'{pattern[i]} - {answers[i]}']
            count += 1
        else:
            result += [f'{pattern[i]} - {answers[i]}']

    context = {
        'blank': blank,
        'result': result,
        'count': len(pattern),
        'score': count,
        'proc': int(count / len(pattern) * 100)
    }
    return render(
        request,
        template_view,
        context
    )


def delete_class(request, class_pk):
    Class.objects.filter(pk=class_pk).delete()
    return redirect('myclasses')


def download(request):
    return render(request, 'download.html')
