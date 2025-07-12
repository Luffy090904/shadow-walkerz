from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Answer, Notification, Tag
from .forms import QuestionForm, AnswerForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from .models import Tag


def home(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'forum/index.html', {'questions': questions})

@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()

            # Parse and attach custom tags
            tag_string = form.cleaned_data.get('tags', '')
            tag_names = [tag.strip() for tag in tag_string.split(',') if tag.strip()]
            for tag_name in tag_names:
                tag_obj, created = Tag.objects.get_or_create(name=tag_name)
                question.tags.add(tag_obj)

            return redirect('home')
    else:
        form = QuestionForm()

    return render(request, 'forum/ask_question.html', {'form': form})

def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = question.answers.all().order_by('-created_at')

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()

            # Create a simple notification
            if question.user != request.user:
                Notification.objects.create(
                    user=question.user,
                    message=f"{request.user.username} answered your question."
                )

            return redirect('question_detail', pk=question.pk)
    else:
        form = AnswerForm()

    return render(request, 'forum/question_detail.html', {
        'question': question,
        'answers': answers,
        'form': form
    })

def signup(request):
    print("Reached signup view")
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'forum/signup.html', {'form': form})


@login_required
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if question.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this question.")

    if request.method == "POST":
        question.delete()
        return redirect('home')

    return render(request, 'forum/confirm_delete.html', {'question': question})