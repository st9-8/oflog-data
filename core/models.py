from django.db import models


class Course(models.Model):
    """
        File contains the list of all available modules and their presentations.
    """
    code_module = models.CharField(max_length=45)
    code_presentation = models.CharField(max_length=45)
    start_date = models.DateTimeField(auto_now_add=True)

    @property
    def name(self):
        return f'CS{self.code_module}-{self.code_presentation}'

    def __str__(self):
        return self.name


class StudentInfo(models.Model):
    """
        This file contains demographic information about the students together with their results.
        File contains the following columns
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students')
    id_student = models.BigIntegerField(unique=True, primary_key=True)
    gender = models.CharField(max_length=3)
    region = models.CharField(max_length=45)
    imd_brand = models.CharField(max_length=16)
    highest_education = models.CharField(max_length=45)
    age_band = models.CharField(max_length=16)
    num_of_prev_attempts = models.IntegerField()
    studied_credits = models.IntegerField()
    disability = models.CharField(max_length=3)
    final_result = models.CharField(max_length=45)

    @property
    def name(self):
        return f'{"Male" if self.gender == "M" else "Female"}#{self.id_student}'

    def __str__(self):
        return self.name


class StudentRegistration(models.Model):
    """
        This file contains information about the time when the student registered for the module presentation.
        For students who unregistered the date of unregistration is also recorded
    """
    student = models.ForeignKey(StudentInfo, on_delete=models.CASCADE, related_name='registrations')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='registrations')
    date_registration = models.DateTimeField(auto_now=True)
    date_unregistration = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.student}'


class VLE(models.Model):
    id_site = models.BigIntegerField(unique=True, primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    activity = models.CharField(max_length=45)
    week_from = models.IntegerField(null=True)
    week_to = models.IntegerField(null=True)

    def __str__(self):
        return f'Material #{self.id_site}'


class Assessment(models.Model):
    """
        This file contains information about assessments in module-presentations.
        Usually, every presentation has a number of assessments followed by the final exam
    """

    id_assessment = models.BigIntegerField(unique=True, primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assessments')
    assessment_type = models.CharField(max_length=45)
    date = models.DateTimeField(null=True, blank=True,
                                help_text="information about the final submission date of the assessment calculated as "
                                          "the number of days since the start of the module-presentation. The starting "
                                          "date of the presentation has number 0 (zero). weight - weight of the "
                                          "assessment in %. Typically, Exams are treated separately and have the weight"
                                          "100%; the sum of all other assessments is 100%.")

    def __str__(self):
        return f'Assessment #{self.id_assessment}'


class StudentAssessment(models.Model):
    """
        This file contains the results of students’ assessments.
        If the student does not submit the assessment, no result is recorded
    """

    student = models.ForeignKey(StudentInfo, on_delete=models.CASCADE, related_name='assessments')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='students')
    date_submitted = models.DateTimeField(blank=True, null=True,
                                          help_text='the date of student submission, measured as the number of days '
                                                    'since the start of the module presentation.')
    is_banked = models.BooleanField()
    score = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'{self.student} submitted {self.assessment}'


class StudentVle(models.Model):
    """
        The studentVle.csv file contains information about each student’s interactions with the materials in the VLE
    """

    material = models.ForeignKey(VLE, on_delete=models.CASCADE, related_name='students_vle')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students_vle')
    student = models.ForeignKey(StudentInfo, on_delete=models.CASCADE, related_name='student_vle')
    date = models.DateTimeField(null=True, blank=True,
                               help_text="the date of student’s interaction with the material measured as the number "
                                         "of days since the start of the module-presentation.")
    sum_click = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.student} interated with material {self.material}'
