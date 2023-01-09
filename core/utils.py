import csv
import random
from datetime import timedelta

from core.models import *

course_path = '/home/st9_8/Documents/Memoire/Conference Paper/data/anonymisedData/courses.csv'
student_infos_path = '/home/st9_8/Documents/Memoire/Conference Paper/data/anonymisedData/studentInfo.csv'
vle_path = '/home/st9_8/Documents/Memoire/Conference Paper/data/anonymisedData/vle.csv'
assessment_path = '/home/st9_8/Documents/Memoire/Conference Paper/data/anonymisedData/assessments.csv'
student_registration_path = '/home/st9_8/Documents/Memoire/Conference Paper/data/anonymisedData/studentRegistration.csv'
student_assessment_path = '/home/st9_8/Documents/Memoire/Conference Paper/data/anonymisedData/studentAssessment.csv'
student_vle_path = '/home/st9_8/Documents/Memoire/Conference Paper/data/anonymisedData/studentVle.csv'

import time


def load_courses(count=10000):
    with open(course_path, 'r') as course_file:
        csv_reader = csv.DictReader(course_file)

        counter = 1
        index = 1
        print('Loading courses: ')

        for row in csv_reader:
            if counter == count:
                break

            # time.sleep(0.5)
            print('.' * (index + 1), end='\r')
            if index == 20:
                index = 1
                print(' ' * 21, end='\r')
            else:
                index += 1

            Course.objects.update_or_create(
                code_module=row['code_module'],
                code_presentation=row['code_presentation']
            )
            counter += 1

        print()


def load_student_infos(count=10000):
    with open(student_infos_path, 'r') as student_infos_file:
        csv_reader = csv.DictReader(student_infos_file)

        counter = 1
        index = 1
        print('Loading student infos: ')

        for row in csv_reader:
            if counter == count:
                break

            # time.sleep(0.5)
            print('.' * (index + 1), end='\r')
            if index == 20:
                index = 1
                print(' ' * 21, end='\r')
            else:
                index += 1

            course = Course.objects.get(
                code_module=row['code_module'], code_presentation=row['code_presentation'])

            try:
                StudentInfo.objects.update_or_create(
                    course=course,
                    id_student=int(row['id_student']),
                    gender=row['gender'],
                    region=row['region'],
                    highest_education=row['highest_education'],
                    imd_brand=row['imd_band'],
                    age_band=row['age_band'],
                    num_of_prev_attempts=int(row['num_of_prev_attempts']),
                    studied_credits=int(row['studied_credits']),
                    disability=row['disability'],
                    final_result=row['final_result']
                )
            except Exception:
                pass

            counter += 1

        print()


def load_vle(count=10000):
    with open(vle_path, 'r') as vle_file:
        csv_reader = csv.DictReader(vle_file)

        counter = 1
        index = 1
        print('Loading vle: ')

        for row in csv_reader:
            if counter == count:
                break

            # time.sleep(0.5)
            print('.' * (index + 1), end='\r')
            if index == 20:
                index = 1
                print(' ' * 21, end='\r')
            else:
                index += 1

            course = Course.objects.get(
                code_module=row['code_module'], code_presentation=row['code_presentation'])

            vle, _ = VLE.objects.update_or_create(
                id_site=int(row['id_site']),
                course=course,
                activity=row['activity_type'],
            )

            if row['week_from']:
                vle.week_from = int(row['week_from'])
            if row['week_to']:
                vle.week_to = int(row['week_to'])

            vle.save()

            counter += 1

        print()


def load_assessments(count=10000):
    with open(assessment_path, 'r') as assessment_file:
        csv_reader = csv.DictReader(assessment_file)

        counter = 1
        index = 1
        print('Loading assessments: ')

        for row in csv_reader:
            if counter == count:
                break

            # time.sleep(0.5)
            print('.' * (index + 1), end='\r')
            if index == 20:
                index = 1
                print(' ' * 21, end='\r')
            else:
                index += 1

            course = Course.objects.get(
                code_module=row['code_module'], code_presentation=row['code_presentation'])

            assessment, _ = Assessment.objects.update_or_create(
                course=course,
                id_assessment=int(row['id_assessment']),
                assessment_type=row['assessment_type']
            )

            if row['date']:
                assessment.date = course.start_date + timedelta(days=int(row['date']))

            assessment.save()

            counter += 1


def load_student_registrations(count=10000):
    with open(student_registration_path, 'r') as student_registration_file:
        csv_reader = csv.DictReader(student_registration_file)

        counter = 1
        index = 1
        print('Loading student registrations: ')

        for row in csv_reader:
            if counter == count:
                break

            # time.sleep(0.5)
            print('.' * (index + 1), end='\r')
            if index == 20:
                index = 1
                print(' ' * 21, end='\r')
            else:
                index += 1

            course = Course.objects.get(
                code_module=row['code_module'], code_presentation=row['code_presentation'])

            try:
                student = StudentInfo.objects.get(id_student=int(row['id_student']))

                StudentRegistration.objects.update_or_create(
                    course=course,
                    student=student,
                    date_registration=course.start_date + timedelta(days=random.randint(1, 31)),
                    # Complete data, because it's empty in row['date_registration']
                    # date_unregistration=row['date_unregistration']
                )
            except StudentInfo.DoesNotExist:
                pass

            counter += 1

        print()


def load_student_assessments(count=10000):
    with open(student_assessment_path, 'r') as student_assessment_file:
        csv_reader = csv.DictReader(student_assessment_file)

        counter = 1
        index = 1
        print('Loading students assessments: ')
        for row in csv_reader:
            if counter == count:
                break

            # time.sleep(0.5)
            print('.' * (index + 1), end='\r')
            if index == 20:
                index = 1
                print(' ' * 21, end='\r')
            else:
                index += 1

            student = StudentInfo.objects.get(id_student=int(row['id_student']))
            assessment = Assessment.objects.get(id_assessment=int(row['id_assessment']))

            student_assessment, _ = StudentAssessment.objects.update_or_create(
                student=student,
                assessment=assessment,
                is_banked=eval(row['is_banked'])
            )

            if row['date_submitted']:
                student_assessment.date_submitted = assessment.course.start_date + timedelta(
                    days=int(row['date_submitted']))

            if row['score']:
                student_assessment.score = float(row['score'])

            student_assessment.save()

            counter += 1

        print()


def load_student_vle(count=10000):
    with open(student_vle_path, 'r') as student_vle_file:
        csv_reader = csv.DictReader(student_vle_file)

        counter = 1
        index = 1
        print('Loading students vle: ')

        for row in csv_reader:
            if counter == count:
                break

            # time.sleep(0.5)
            print('.' * (index + 1), end='\r')
            if index == 20:
                index = 1
                print(' ' * 21, end='\r')
            else:
                index += 1

            course = Course.objects.get(code_module=row['code_module'], code_presentation=row['code_presentation'])
            student = StudentInfo.objects.get(id_student=int(row['id_student']))
            material = VLE.objects.get(id_site=int(row['id_site']))

            student_vle, _ = StudentVle.objects.update_or_create(
                material=material,
                course=course,
                student=student,
                sum_click=int(row['sum_click'])
            )

            if row['date']:
                student_vle.date = course.start_date + timedelta(days=int(row['date']))

            student_vle.save()

            counter += 1

        print()
