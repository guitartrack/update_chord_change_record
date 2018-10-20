from pynamodb.exceptions import UpdateError
from pynamodb.models import Model
from pynamodb.attributes import NumberAttribute, UnicodeAttribute


class ChordChangeRecord(Model):
    class Meta:
        region = 'eu-central-1'
        table_name = 'chord_change_record'

    chord_change = UnicodeAttribute(hash_key=True)
    count = NumberAttribute(default=0)


def lambda_handler(event, context):
    return True
