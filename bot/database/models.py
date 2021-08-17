from tortoise import fields
from tortoise.models import Model


class Quotes(Model):
    id = fields.auto_increment(auto_increment=True, pk=True)
    user = fields.CharField(max_length=255)
    quote = fields.CharField(max_length=2000)

    def __str__(self):
        return self.name
