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
    for record in event['Records']:
        update_chord_change_record(
            record['dynamodb']['Keys']['chord_change']['S'],
            record['dynamodb']['NewImage']['count']['N']
       )


def update_chord_change_record(chord_change: str, count: int):
    try:
        record = ChordChangeRecord.get(chord_change)
    except ChordChangeRecord.DoesNotExist:
        record = ChordChangeRecord(chord_change=chord_change)
        record.save()

    try:
        record.update(
            actions=[ChordChangeRecord.count.set(count)],
            condition=(ChordChangeRecord.count < count)
        )
    except UpdateError:
        pass
