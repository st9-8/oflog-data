from django.core.management.base import BaseCommand, CommandError
from core.utils import *


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--count', default=10000, type=int)

    def handle(self, *args, **options):
        try:
            load_courses(count=options['count'])
            load_student_infos(count=options['count'])
            load_vle(count=options['count'])
            load_student_registrations(count=options['count'])
            load_assessments(count=options['count'])
            load_student_assessments(count=options['count'])
            load_student_vle(count=options['count'])
        except Exception as e:
            import traceback
            traceback.print_exc()

            raise CommandError(str(e))

        self.stdout.write(self.style.SUCCESS('Successfully load logs data'))
