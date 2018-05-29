import datetime
from django.db import models

from Registration.models import Subject, Faculty, Branch, Student


class CollegeYear(models.Model):
    year = models.CharField(max_length=20)
    number = models.IntegerField(default=0, null=True)
    no_of_semester = models.IntegerField(null=True)

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
        return self.branch.branch + ' ' + str(self.year.year)


# Will be known as division
class Division(models.Model):
    year_branch = models.ForeignKey(YearBranch, on_delete=models.CASCADE, null=True)
    division = models.CharField(max_length=1)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.year_branch) + ' ' + self.division


class Semester(models.Model):
    semester = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.semester)

    # def is_current(self):
    #     if self.start_date <= datetime.date.today() <= self.end_date:
    #         return True
    #     else:
    #         return False


# class StudentSemester(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
#     is_active = models.BooleanField(default=True)

class YearSemester(models.Model):
    year_branch = models.ForeignKey(YearBranch, on_delete=models.CASCADE, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    lecture_start_date = models.DateField(null=True, blank=True)
    lecture_end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    number_of_electives_groups = models.IntegerField(default=0)

    def __str__(self):
        return str(self.year_branch) + " " + str(self.semester)


class Batch(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    batch_name = models.CharField(max_length=10)

    def __str__(self):
        return self.division.year_branch.year.year + ' ' + self.division.division + " " + self.batch_name


class ElectiveGroup(models.Model):
    year_branch = models.ForeignKey(YearBranch, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    group = models.CharField(max_length=20, null=True)

    def __str__(self):
        return str(self.year_branch) + " " + str(self.semester) + " " + str(self.group)


class BranchSubject(models.Model):
    # branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    # year = models.ForeignKey(CollegeYear, on_delete=models.CASCADE)
    year_branch = models.ForeignKey(YearBranch, on_delete=models.CASCADE, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, null=True)
    group = models.ForeignKey(ElectiveGroup, on_delete=models.CASCADE, null=True)
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
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.faculty.user.first_name + self.subject.name + self.division.division + " " + self.faculty.initials


class StudentDetail(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True)
    # batch = models.CharField(max_length=10)
    roll_number = models.PositiveIntegerField(null=True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    has_registered_subject = models.BooleanField(default=False)

    def __str__(self):
        return str(self.batch.division) + " " + str(self.student.first_name) + " " + str(self.roll_number)


class StudentSubject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.student) + " " + str(self.subject)


# Abhi ye  do class rakhe hai for storing schedules of subject registration
class Schedulable(models.Model):
    name = models.CharField(max_length=500)
    created_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    def event_active(self, name):
        if self.name == name:
            today = datetime.date.today()
            if self.end_date and self.created_date != None:
                if self.end_date > today > self.created_date:
                    return True
        return False

class Schedule(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    event = models.ForeignKey(Schedulable, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
