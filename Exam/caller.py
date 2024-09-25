import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

from main_app.models import Astronaut, Mission, Spacecraft
from django.db.models import Count, Sum, Q, Avg


def get_astronauts(search_string=None):
    if search_string is None:
        return ""

    astronauts = Astronaut.objects.filter(
        Q(name__icontains=search_string) | Q(phone_number__icontains=search_string)
    ).order_by('name')

    if not astronauts:
        return ""

    result = []
    for astronaut in astronauts:
        status = 'Active' if astronaut.is_active else 'Inactive'
        result.append(f"Astronaut: {astronaut.name}, phone number: {astronaut.phone_number}, status: {status}")

    return "\n".join(result)


def get_top_astronaut():
    top_astronaut = Astronaut.objects.annotate(
        mission_count=Count('mission')
    ).order_by('-mission_count', 'phone_number').first()

    if top_astronaut and top_astronaut.mission_count > 0:
        return f"Top Astronaut: {top_astronaut.name} with {top_astronaut.mission_count} missions."
    return "No data."


def get_top_commander():
    top_commander = Astronaut.objects.annotate(
        command_count=Count('commanded_missions')
    ).order_by('-command_count', 'phone_number').first()

    if top_commander and top_commander.command_count > 0:
        return f"Top Commander: {top_commander.name} with {top_commander.command_count} commanded missions."
    return "No data."


def get_last_completed_mission():
    last_completed_mission = Mission.objects.filter(status='Completed').order_by('-launch_date').first()

    if last_completed_mission:
        astronauts = last_completed_mission.astronauts.order_by('name')
        astronaut_names = ", ".join([astronaut.name for astronaut in astronauts])
        commander_name = last_completed_mission.commander.name if last_completed_mission.commander else "TBA"
        total_spacewalks = astronauts.aggregate(total_spacewalks=Sum('spacewalks'))['total_spacewalks'] or 0
        return f"The last completed mission is: {last_completed_mission.name}. Commander: {commander_name}. Astronauts: {astronaut_names}. Spacecraft: {last_completed_mission.spacecraft.name}. Total spacewalks: {total_spacewalks}."
    return "No data."


def get_most_used_spacecraft():
    spacecrafts_with_mission_count = Spacecraft.objects.annotate(
        mission_count=Count('mission')
    ).order_by('-mission_count', 'name')

    if spacecrafts_with_mission_count.exists():
        most_used_spacecraft = spacecrafts_with_mission_count.first()
        unique_astronauts = Astronaut.objects.filter(
            mission__spacecraft=most_used_spacecraft
        ).distinct().count()
        return f"The most used spacecraft is: {most_used_spacecraft.name}, manufactured by {most_used_spacecraft.manufacturer}, used in {most_used_spacecraft.mission_count} missions, astronauts on missions: {unique_astronauts}."
    return "No data."


def decrease_spacecrafts_weight():
    planned_spacecrafts = Spacecraft.objects.filter(
        mission__status='Planned', weight__gte=200.0
    ).distinct()

    affected_spacecrafts = planned_spacecrafts.count()

    if affected_spacecrafts > 0:
        for spacecraft in planned_spacecrafts:
            spacecraft.weight -= 200.0
            spacecraft.save()

        avg_weight = Spacecraft.objects.aggregate(avg_weight=Avg('weight'))['avg_weight']
        return f"The weight of {affected_spacecrafts} spacecrafts has been decreased. The new average weight of all spacecrafts is {avg_weight:.1f}kg"
    return "No changes in weight."


