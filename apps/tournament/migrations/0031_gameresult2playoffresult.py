# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection


def migrate_results(apps, schema_editor):
    cursor = connection.cursor()
    cursor.execute('''
BEGIN;

INSERT INTO tournament_playoffresult (gameresult_ptr_id, og, oo, cg, co)
SELECT
  gameresult_ptr_id,
  CASE WHEN og < 3 THEN TRUE  ELSE FALSE END AS og,
  CASE WHEN oo < 3 THEN TRUE  ELSE FALSE END AS oo,
  CASE WHEN cg < 3 THEN TRUE  ELSE FALSE END AS cg,
  CASE WHEN co < 3 THEN TRUE  ELSE FALSE END AS co
FROM tournament_qualificationresult q
INNER JOIN tournament_gameresult r ON q.gameresult_ptr_id = r.id
INNER JOIN tournament_game g ON g.id = r.game_id
INNER JOIN tournament_room room ON room.game_id = g.id
INNER JOIN tournament_round round ON room.round_id = round.id
WHERE round.is_playoff = TRUE;

DELETE FROM tournament_qualificationresult q
WHERE q.gameresult_ptr_id IN (
    SELECT
      q1.gameresult_ptr_id
    FROM tournament_qualificationresult q1
    INNER JOIN tournament_gameresult r ON q1.gameresult_ptr_id = r.id
    INNER JOIN tournament_game g ON g.id = r.game_id
    INNER JOIN tournament_room room ON room.game_id = g.id
    INNER JOIN tournament_round round ON room.round_id = round.id
    WHERE round.is_playoff = TRUE
);

COMMIT;''')


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0030_split_game_result'),
    ]

    operations = [

        migrations.RunPython(migrate_results),

    ]
