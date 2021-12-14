from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    # false => present in hostel
    # true  => absent  in hostel
    flag = models.BooleanField(default=False) 
    # rollnumber = ""

    def __str__(self):
        return f"{self.user}, {self.flag}"

class Registerbook(models.Model):
    exit_time = models.DateTimeField()
    enter_time = models.DateTimeField()
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    reason = models.CharField(max_length=150, default="")

    def __str__(self):
        return f"{self.exit_time}, {self.enter_time}"
