from django.core.management.base import BaseCommand
from YunHui.models import Data

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        try:
            d = Data(id=1, success=0)
            d.save()
        except Exception as e:
            print(e)
        print("初始化成功")
