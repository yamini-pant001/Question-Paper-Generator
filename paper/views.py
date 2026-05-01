import random
from urllib import request
from django.shortcuts import render
from .models import question, subject

def generate_paper(request):
    subjects = subject.objects.all()

    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        selected_subject = subject.objects.get(id=subject_id)

        # Filter questions
        short_questions = list(question.objects.filter(subject=selected_subject, marks='5'))
        long_questions = list(question.objects.filter(subject=selected_subject, marks='10'))

        # Random selection (safe)
        num_short = int(request.POST.get('num_short'))
        num_long = int(request.POST.get('num_long'))
        selected_short = random.sample(short_questions, min(len(short_questions), num_short))
        selected_long = random.sample(long_questions, min(len(long_questions), num_long))

        return render(request, 'paper/paper.html', {
            'subject': selected_subject,
            'short_questions': selected_short,
            'long_questions': selected_long
        })

    return render(request, 'paper/select_subject.html', {'subjects': subjects})
 