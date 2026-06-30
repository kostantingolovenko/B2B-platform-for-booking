from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField()
    website = models.URLField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Office(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='offices')
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    open_time = models.TimeField()
    close_time = models.TimeField()
    phone = models.CharField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_organization(self):
        return self.organization

    def __str__(self):
        return self.address

class Room(models.Model):
    office = models.ForeignKey(Office, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=255)
    floor = models.IntegerField()

    class RoomType(models.TextChoices):
        MEETING_ROOM = 'meeting', 'Meeting Room'
        OPEN_SPACE = 'open', 'Open Space'
        PRIVATE_OFFICE = 'private', 'Private Office'
    room_type = models.CharField(max_length=20, choices=RoomType.choices, default=RoomType.OPEN_SPACE)

    capacity = models.IntegerField()
    has_projector = models.BooleanField(default=False)
    has_whiteboard = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_organization(self):
        return self.office.organization

    def __str__(self):
        return self.name

class Desk(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='desks')
    number = models.CharField(max_length=50)
    is_adjustable = models.BooleanField(default=False)
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_organization(self):
        return self.room.office.organization

    def __str__(self):
        return self.number