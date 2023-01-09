import csv
import random

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from core.models import VLE

output_path_folder = settings.BASE_DIR / 'output_data'


class Command(BaseCommand):

    def handle(self, *args, **options):
        output_file = output_path_folder / 'oulad_actions.csv'

        with open(output_file, 'w') as logs_file:
            all_data = []
            material_actions = VLE.objects.all().distinct().values_list('activity', flat=True)

            log_writer = csv.DictWriter(logs_file, fieldnames=['action', 'verb'])

            log_writer.writeheader()

            # Other actions
            for action in material_actions:
                line_data = {
                    'action': action,
                    'verb': ''
                }

                all_data.append(line_data)

            log_writer.writerows(all_data)

        self.stdout.write(self.style.SUCCESS('Successfully written actions from OULAD'))
        self.stdout.write(self.style.SUCCESS(f'New file saved at: {output_file}'))
