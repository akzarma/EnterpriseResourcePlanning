from django.db import models

from Registration.models import Subject, Faculty, Branch, Student


class CollegeYear(models.Model):
    year = models.CharField(max_length=20)
    number = models.IntegerField(default=0)

    def __str__(self):
        return self.year


class Semester(models.Model):
    semester = models.PositiveIntegerField()

    def __str__(self):
        return str(self.semester)


class Shift(models.Model):
    shift = models.PositiveIntegerField()

    def __str__(self):
        return str(self.shift)


# Will be known as division
class CollegeExtraDetail(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    year = models.ForeignKey(CollegeYear, on_delete=models.CASCADE)
    division = models.CharField(max_length=1)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)

    def __str__(self):
        return self.branch.branch + ' ' + str(self.year) + ' ' + self.division


class Batch(models.Model):
    division = models.ForeignKey(CollegeExtraDetail, on_delete=models.CASCADE)
    batch_name = models.CharField(max_length=10)
    starting_roll_number = models.PositiveIntegerField()
    ending_roll_number = models.PositiveIntegerField()

    def __str__(self):
        return self.batch_name


class BranchSubject(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    year = models.ForeignKey(CollegeYear, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)  # Should not be null=Trus
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.branch.branch + self.subject.name


class FacultySubject(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    division = models.ForeignKey(CollegeExtraDetail, on_delete=models.CASCADE)

    def __str__(self):
        return self.faculty.user.first_name + self.subject.name + self.division.division + " " + self.faculty.initials


class StudentDivision(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    division = models.ForeignKey(CollegeExtraDetail, on_delete=models.CASCADE)

    def __str__(self):
        return self.division.division + " " + self.student.first_name


class StudentSubject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
