import csv
import random
from django.shortcuts import render
from .models import question, subject


def upload_questions(request):
     print("view called")  # Debugging line to check if the view is being accessed
     if request.method == 'POST':
          
          file = request.FILES['file']
          if not file:
                 return render(request, 'paper/upload.html', {'msg': 'No file uploaded.'})
          decoded_file = file.read().decode('latin-1').splitlines()   
          reader = csv.DictReader(decoded_file)


          for row in reader:
                 print("Row data:", row)  # Debugging line to check the content of each row
                 sub = subject.objects.get_or_create(name=row['subject'])
                   
                 question.objects.create(
                        text=row['question_text'],
                        marks=row['marks'],
                        subject=sub[0]
                    )
          return render(request, 'paper/upload.html',{'msg':'Questions uploaded successfully!'})
     return render(request, 'paper/upload.html')
                 
def select_semester(request):
    return render(request, 'paper/select_semester.html')


def select_subject(request):
        if request.method == 'POST':
            semester = request.POST.get('semester')
            subjects = subject.objects.filter(semester=semester)
            return render(request, 'paper/select_subject.html', {'subjects': subjects, 'semester': semester})
        
        return render(request, 'paper/select_semester.html')




def generate_paper(request):
    if request.method == 'POST':

        subject_id = request.POST.get('subject')
        if not subject_id:
            return render(request, 'paper/select_subject.html')

        selected_subject = subject.objects.get(id=subject_id)

        short_questions = list(question.objects.filter(subject=selected_subject, marks='5'))
        long_questions = list(question.objects.filter(subject=selected_subject, marks='10'))

        num_short = request.POST.get('num_short')
        num_long = request.POST.get('num_long')

        num_short = int(num_short) if num_short and num_short.isdigit() else 5
        num_long = int(num_long) if num_long and num_long.isdigit() else 5

        selected_short = random.sample(short_questions, min(len(short_questions), num_short))
        selected_long = random.sample(long_questions, min(len(long_questions), num_long))

        return render(request, 'paper/paper.html', {
            'subject': selected_subject,
            'short_questions': selected_short,
            'long_questions': selected_long
        })

    return render(request, 'paper/select_subject.html')
 