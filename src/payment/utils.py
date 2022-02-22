import random

from django.db import connection


def identifier_builder() -> str:
    with connection.cursor() as cur:
        cur.execute('''SELECT last_value FROM payments_id_seq;''')
        row = cur.fetchone()
    seq_id = str(row[0] + 1)
    random_suffix = random.randint(10, 99)
    return 'CBP' + seq_id.rjust(8, '0') + str(random_suffix)
