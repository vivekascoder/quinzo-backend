from django.db import models


class Paper(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Question(models.Model):
    OPTIONS = (
        ('option_a', 'option_a'), ('option_b', 'option_b'), ('option_c', 'option_c'), ('option_d', 'option_d')
    )
    title = models.CharField(max_length=100, unique=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')
    marks = models.PositiveIntegerField(default=1)
    option_a = models.CharField(max_length=100)    
    option_b = models.CharField(max_length=100)
    option_c = models.CharField(max_length=100)
    option_d = models.CharField(max_length=100)    
    answer = models.CharField(choices=OPTIONS, max_length=10)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-date',)
    

    def __str__(self):
        return self.title
