import datetime
from django.db import models

from Registration.models import Subject, Faculty, Branch, Student


class CollegeYear(models.Model):
    year = models.CharField(max_length=20)
    number = models.IntegerField(default=0)

    def __str__(self):
        return self.year


class Shift(models.Model):
    shift = models.PositiveIntegerField()

    def __str__(self):
        return str(self.shift)


class YearBranch(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    year = models.ForeignKey(CollegeYear, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.branch.branch + ' ' + str(self.year)


# Will be known as division
class Division(models.Model):
    year_branch = models.ForeignKey(YearBranch, on_delete=models.CASCADE, null=True)
    division = models.CharField(max_length=1)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.year_branch) + ' ' + self.division


class Semester(models.Model):
    semester = models.PositiveIntegerField()
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    is_active = models.BooleanField(default=True)

    # lectures_start_date = models.DateTimeField()
    # lectures_end_date = models.DateTimeField()

    def __str__(self):
        return str(self.semester)

    # def is_current(self):
    #     if self.start_date <= datetime.date.today() <= self.end_date:
    #         return True
    #     else:
    #         return False


class Batch(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    batch_name = models.CharField(max_length=10)

    def __str__(self):
        return self.division.year_branch.year.year + ' ' + self.division.division + " " + self.batch_name


class BranchSubject(models.Model):
    # branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    # year = models.ForeignKey(CollegeYear, on_delete=models.CASCADE)
    year_branch = models.ForeignKey(YearBranch, on_delete=models.CASCADE, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    group = models.CharField(max_length=20, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)  # Should not be null=True
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.year_branch) + " " + self.subject.name


class FacultySubject(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)

    def __str__(self):
        return self.faculty.user.first_name + self.subject.name + self.division.division + " " + self.faculty.initials


class StudentDetail(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    # batch = models.CharField(max_length=10)
    roll_number = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.batch.division) + " " + str(self.student.first_name) + " " + str(self.roll_number)


class StudentSubject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


# Abhi ye  do class rakhe hai for storing schedules of subject registration
class Schedulable(models.Model):
    name = models.CharField(max_length=500)
    created_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    event = models.ForeignKey(Schedulable, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
