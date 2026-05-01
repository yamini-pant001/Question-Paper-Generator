from django.db import models

# Create your models here.

# here we are defining two models, subject and question. The subject model has a name field, while the question model has a foreign key to the subject model, a text field for the question text, and a marks field that uses choices to specify the type of question (5 marks or 10 marks). We also have __str__ methods to return a string representation of each model instance.
class subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class question(models.Model):
    question_type=(
        ('5','5 marks'),
        ('10','10 marks'),
    )
    subject = models.ForeignKey(subject, on_delete=models.CASCADE)
    text = models.TextField()
    marks=models.CharField(max_length=2,choices=question_type)

    def __str__(self):
        return self.text