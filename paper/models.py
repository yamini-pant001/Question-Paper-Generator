from django.db import models


# here we are defining two models, subject and question. The subject model has a name field, while the question model has a foreign key to the subject model, a text field for the question text, and a marks field that uses choices to specify the type of question (5 marks or 10 marks). We also have __str__ methods to return a string representation of each model instance.
class subject(models.Model):
    name = models.CharField(max_length=100)      #name of the subject
    semester = models.IntegerField(default=1)            #semester 

    def __str__(self):
        return self.name
    
class question(models.Model):           #question type can be either 5 marks or 10 marks, we are using choices to specify the options for the marks field. The subject field is a foreign key to the subject model, which allows us to associate each question with a specific subject.
    question_type=(
        ('5','5 marks'),
        ('10','10 marks'),
    )
    subject = models.ForeignKey(subject, on_delete=models.CASCADE)      #foreign key to the subject model
    text = models.TextField()                               #text of the question
    marks=models.CharField(max_length=2,choices=question_type)      #marks for the question, either 5 or 10

    def __str__(self):
        return self.text        #it returns the text of the question when we print a question object.