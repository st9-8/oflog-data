import csv
import random

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from core.models import StudentVle
from core.models import StudentAssessment
from core.models import StudentRegistration

output_path_folder = settings.BASE_DIR / 'output_data'


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--registration_count', default=1000, type=int)
        parser.add_argument('--other_count', default=5000, type=int)
        parser.add_argument('--assessment_count', default=5000, type=int)

    def handle(self, *args, **options):
        output_file = output_path_folder / 'oulad_logs.csv'

        with open(output_file, 'w') as logs_file:
            all_data = []
            registrations = StudentRegistration.objects.order_by('?')[:options['registration_count']]
            material_actions = StudentVle.objects.order_by('?')[:options['other_count']]
            assessments = StudentAssessment.objects.order_by('?')[:options['assessment_count']]

            log_writer = csv.DictWriter(logs_file, fieldnames=['course', 'datetime', 'action', 'information', 'anoname',
                                                               'ip_address'])

            log_writer.writeheader()
            # Registration actions
            for registration in registrations:
                line_data = {
                    'course': registration.course.name,
                    'datetime': registration.date_registration.strftime('%Y %B %d %H:%M'),
                    'action': 'registration',
                    'information': '',
                    'anoname': registration.student.name,
                    'ip_address': 'X.Y.Z'
                }

                all_data.append(line_data)

            # Other actions
            for student_material in material_actions:
                line_data = {
                    'course': student_material.course.name,
                    'datetime': student_material.date.strftime('%Y %B %d %H:%M'),
                    'action': student_material.material.activity,
                    'information': '',
                    'anoname': student_material.student.name,
                    'ip_address': 'X.Y.Z'
                }

                all_data.append(line_data)

            # Assessment actions
            for student_assessment in assessments:
                line_data = {
                    'course': student_assessment.assessment.course.name,
                    'datetime': student_assessment.date_submitted.strftime('%Y %B %d %H:%M'),
                    'action': 'assessment',
                    'information': student_assessment.assessment.assessment_type,
                    'anoname': student_assessment.student.name,
                    'ip_address': 'X.Y.Z'
                }

                all_data.append(line_data)

            random.shuffle(all_data)

            log_writer.writerows(all_data)

        self.stdout.write(self.style.SUCCESS('Successfully written logs data from OULAD'))
        self.stdout.write(self.style.SUCCESS(f'New file saved at: {output_file}'))
