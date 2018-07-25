import datetime

from django.core.exceptions import ValidationError
from django.db import models

from Internship.models import Internship
from Registration.models import Subject, Faculty, Branch, Student, ElectiveSubject


class CollegeYear(models.Model):
    year = models.CharField(max_length=20)
    number = models.IntegerField(default=0, null=True)
    no_of_semester = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.year


class YearBranch(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    year = models.ForeignKey(CollegeYear, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.branch.branch + ' ' + str(self.year.year)


class Shift(models.Model):
    shift = models.PositiveIntegerField()
    year_branch = models.ForeignKey(YearBranch, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.year_branch.branch.branch + '-' + self.year_branch.year.year + '-' + str(self.shift)


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

    # number_of_elective_groups = models.IntegerField(default=0)

    def __str__(self):
        return str(self.year_branch) + " " + str(self.semester)

    def save(self, *args, **kwargs):
        models.Model.save(self, *args, **kwargs)
        branch_obj = Branch.objects.get(branch=self.year_branch.branch)
        year_obj = CollegeYear.objects.get(year=self.year_branch.year)
        # YearSemester.objects.get_or_create(semester=self.semester, year_branch=self.year_branch)

        year_branch_obj = YearBranch.objects.get(branch=branch_obj, year=year_obj, is_active=True)

        # for i in range(self.number_of_elective_groups):
        #     ElectiveGroup.objects.create(year_branch=year_branch_obj, semester=self.semester,
        #                                  group=chr(i + 65))
        year_branch_obj = YearBranch.objects.get(year=year_obj, branch=branch_obj, is_active=True)
        # year_sem_obj = YearSemester.objects.get(year_branch=year_branch_obj, semester=self.semester, is_active=True)
        # year_sem_obj.start_date = self.start_date
        # year_sem_obj.end_date = self.end_date
        # year_sem_obj.lecture_start_date = self.lecture_start_date
        # year_sem_obj.lecture_end_date = self.lecture_end_date
        # year_sem_obj.number_of_electives_groups = self.number_of_elective_groups
        # year_sem_obj.save()


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
    # type = models.CharField(max_length=20, null=True)
    # group = models.ForeignKey(ElectiveGroup, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)  # Should not be null=True
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.year_branch) + " " + self.subject.name

    def save(self, *args, **kwargs):
        models.Model.save(self, *args, **kwargs)


class ElectiveDivision(models.Model):
    elective_subject = models.ForeignKey(ElectiveSubject, on_delete=models.CASCADE)
    division = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.division) + " " + str(self.elective_subject)


class FacultySubject(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True, blank=True)

    elective_subject = models.ForeignKey(ElectiveSubject, on_delete=models.CASCADE, null=True, blank=True)
    elective_division = models.ForeignKey(ElectiveDivision, on_delete=models.CASCADE, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.faculty.user.first_name + self.subject.name + " " + self.faculty.initials


class StudentDetail(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True)
    # batch = models.CharField(max_length=10)
    roll_number = models.PositiveIntegerField(null=True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    has_registered_subject = models.BooleanField(default=False)
    last_subject_registration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.batch.division) + " " + str(self.student.first_name) + " " + str(self.roll_number)


class ElectiveBatch(models.Model):
    division = models.ForeignKey(ElectiveDivision, on_delete=models.CASCADE)
    batch_name = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.batch_name)


class StudentSubject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    elective_division = models.ForeignKey(ElectiveDivision, on_delete=models.CASCADE, null=True, default=None,
                                          blank=True)
    elective_batch = models.ForeignKey(ElectiveBatch, null=True, on_delete=models.CASCADE)
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


class Schedule(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    event = models.ForeignKey(Schedulable, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def event_active(self, name, date):
        if self.event.name == name:
            if self.end_date and self.start_date != None:
                if self.end_date > date > self.start_date:
                    return True
        return False


class StudentInternship(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    work_from_home = models.BooleanField(default=False)
    application_date = models.DateField()
    remarks = models.CharField(max_length=300, null=True, blank=True)
    is_reviewed = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.student) + ' ' + str(self.internship)
