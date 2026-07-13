import json
import os

from django.core.management.base import BaseCommand
from users.models import County, SubCounty, Ward


class Command(BaseCommand):

    help = "Load Kenya locations"


    def handle(self, *args, **kwargs):

        file_path = os.path.join(
            "users",
            "data",
            "kenya_locations.json"
        )


        with open(file_path, "r") as file:
            locations = json.load(file)


        for county_name, sub_counties in locations.items():

            county, created = County.objects.get_or_create(
                name=county_name
            )


            for sub_name, wards in sub_counties.items():

                sub_county, created = SubCounty.objects.get_or_create(
                    county=county,
                    name=sub_name
                )


                for ward_name in wards:

                    Ward.objects.get_or_create(
                        sub_county=sub_county,
                        name=ward_name
                    )


        self.stdout.write(
            self.style.SUCCESS(
                "Locations loaded successfully!"
            )
        )