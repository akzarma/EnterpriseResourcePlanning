from django.db import models
from Registration.models import Faculty, ElectiveSubject
from General.models import BranchSubject, Batch, Division, ElectiveDivision

# from Attendance.models import Division
from Registration.models import Faculty, Subject, Branch


# Create your models here.
# from Registration.models import Branch


class Time(models.Model):
    starting_time = models.IntegerField()
    ending_time = models.IntegerField()

    def __str__(self):
        start = str(self.starting_time)
        start = start[:len(start) - 2] + ':' + start[len(start) - 2:]
        end = str(self.ending_time)
        end = end[:len(end) - 2] + ':' + end[len(end) - 2:]
        return start + '-' + end

    def format_for_json(self):
        start_string = str(self.starting_time)
        start_len = start_string.__len__()

        end_string = str(self.ending_time)
        end_len = end_string.__len__()
        if start_len < 4:
            start_string = '0' + start_string
        if end_len < 4:
            end_string = '0' + end_string
        return start_string + '-' + end_string


class Room(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    lab = models.BooleanField(default=False)
    capacity = models.PositiveIntegerField(default=28)
    number_of_rows = models.PositiveIntegerField(default=4)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.branch) + str(self.room_number)


class Timetable(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    time = models.ForeignKey(Time, on_delete=models.CASCADE)
    day = models.CharField(max_length=10)
    branch_subject = models.ForeignKey(BranchSubject, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, null=True, on_delete=models.CASCADE)
    is_practical = models.BooleanField(default=False)
    batch = models.ForeignKey(Batch, null=True, on_delete=models.CASCADE)
    elective_division = models.ForeignKey(ElectiveDivision, on_delete=models.CASCADE, null=True)
    elective_subject = models.ForeignKey(ElectiveSubject, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.room.room_number + str(
            self.time.starting_time) + self.day + self.branch_subject.subject.name + str(self.faculty)


class DateTimetable(models.Model):
    date = models.DateField()
    original = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='original')
    not_available = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_substituted = models.BooleanField(default=False)
    substitute = models.ForeignKey(Timetable, related_name='substitute', null=True, on_delete=models.CASCADE)
