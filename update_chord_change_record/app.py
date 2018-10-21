from datetime import datetime

from pynamodb.exceptions import UpdateError
from pynamodb.models import Model
from pynamodb.attributes import (
    NumberAttribute, UnicodeAttribute, UTCDateTimeAttribute)


class ChordChangeRecord(Model):
    class Meta:
        region = 'eu-central-1'
        table_name = 'chord_change_record'

    chord_change = UnicodeAttribute(hash_key=True)

    count = NumberAttribute(default=0)
    first_attempt_at = UTCDateTimeAttribute()
    last_attempt_at = UTCDateTimeAttribute(null=True)
    last_record_at = UTCDateTimeAttribute(null=True)


def lambda_handler(event, context):
    for record in event['Records']:
        if record['eventName'] != 'INSERT':
            continue

        update_chord_change_record(
            record['dynamodb']['Keys']['chord_change']['S'],
            int(record['dynamodb']['NewImage']['count']['N'])
        )


def update_chord_change_record(chord_change: str, count: int):
    now = datetime.utcnow()

    try:
        record = ChordChangeRecord.get(chord_change)
    except ChordChangeRecord.DoesNotExist:
        record = ChordChangeRecord(
            chord_change=chord_change, first_attempt_at=now)
        record.save()

    record.update(actions=[ChordChangeRecord.last_attempt_at.set(now)])

    try:
        record.update(
            actions=[
                ChordChangeRecord.count.set(count),
                ChordChangeRecord.last_record_at.set(now)
            ],
            condition=(ChordChangeRecord.count < count)
        )
    except UpdateError:
        pass
