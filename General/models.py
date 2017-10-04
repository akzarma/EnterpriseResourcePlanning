from django.db import models

from Registration.models import Subject, Faculty, Branch, Student


class CollegeYear(models.Model):
    year = models.CharField(max_length=20)

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


class CollegeExtraDetail(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    year = models.ForeignKey(CollegeYear, on_delete=models.CASCADE)
    division = models.CharField(max_length=1)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)

    def __str__(self):
        return self.branch.branch + ' ' + str(self.year) + ' ' + self.division + str(self.shift)


class BranchSubject(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    year = models.ForeignKey(CollegeYear, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.branch.branch + self.subject.name


class FacultySubject(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    division = models.ForeignKey(CollegeExtraDetail, on_delete=models.CASCADE)

    def __str__(self):
        return self.faculty.user.first_name + self.subject.name + self.division.division


class StudentDivision(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    division = models.ForeignKey(CollegeExtraDetail, on_delete=models.CASCADE)


class StudentSubject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)