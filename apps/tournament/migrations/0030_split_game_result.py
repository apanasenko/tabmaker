# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection


def migrate_results(apps, schema_editor):
    cursor = connection.cursor()
    cursor.execute('''
BEGIN;
CREATE TABLE "tournament_playoffresult" (
	"gameresult_ptr_id" integer NOT NULL PRIMARY KEY,
	"og" boolean NOT NULL,
	"oo" boolean NOT NULL,
	"cg" boolean NOT NULL,
	"co" boolean NOT NULL
);

CREATE TABLE "tournament_qualificationresult" (
	"gameresult_ptr_id" integer NOT NULL PRIMARY KEY,
	"og" integer NOT NULL,
	"oo" integer NOT NULL,
	"cg" integer NOT NULL,
	"co" integer NOT NULL,
	"pm" integer NOT NULL,
	"pm_exist" boolean NOT NULL,
	"dpm" integer NOT NULL,
	"dpm_exist" boolean NOT NULL,
	"lo" integer NOT NULL,
	"lo_exist" boolean NOT NULL,
	"dlo" integer NOT NULL,
	"dlo_exist" boolean NOT NULL,
	"mg" integer NOT NULL,
	"mg_exist" boolean NOT NULL,
	"gw" integer NOT NULL,
	"gw_exist" boolean NOT NULL,
	"mo" integer NOT NULL,
	"mo_exist" boolean NOT NULL,
	"ow" integer NOT NULL,
	"ow_exist" boolean NOT NULL
);

INSERT INTO tournament_qualificationresult (gameresult_ptr_id, og, oo, cg, co, pm, pm_exist, dpm, dpm_exist, lo, lo_exist, dlo, dlo_exist, mg, mg_exist, gw, gw_exist, mo, mo_exist, ow, ow_exist)
SELECT id, og, oo, cg, co, pm, pm_exist, dpm, dpm_exist, lo, lo_exist, dlo, dlo_exist, mg, mg_exist, gw, gw_exist, mo, mo_exist, ow, ow_exist FROM tournament_gameresult;


ALTER TABLE "tournament_playoffresult" ADD CONSTRAINT "gameresult_ptr_id_4ee7f04aa4c494a1_fk_tournament_gameresult_id" FOREIGN KEY ("gameresult_ptr_id") REFERENCES "tournament_gameresult" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "tournament_qualificationresult" ADD CONSTRAINT "gameresult_ptr_id_25aaa8c683af6a60_fk_tournament_gameresult_id" FOREIGN KEY ("gameresult_ptr_id") REFERENCES "tournament_gameresult" ("id") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "tournament_gameresult" DROP COLUMN "cg" CASCADE;
ALTER TABLE "tournament_gameresult" DROP COLUMN "co" CASCADE;
ALTER TABLE "tournament_gameresult" DROP COLUMN "dlo" CASCADE;
ALTER TABLE "tournament_gameresult" DROP COLUMN "dlo_exist" CASCADE;
ALTER TABLE "tournament_gameresult" DROP COLUMN "dpm" CASCADE;
ALTER TABLE "tournament_gameresult" DROP COLUMN "dpm_exist" CASCADE;
ALTER TABLE "tournament_gameresult" DROP COLUMN "gw" CASCADE;
ALTER TABLE "tournament_gameresult" DROP COLUMN "gw_exist" CASCADE;
ALTER TABLE "tournament_gameresult" DROP COLUMN "lo" CASCADE;
ALTER TABLE "tournament_gameresult" DROP COLUMN "lo_exist" CASCADE;
ALTER TABLE "tournament_gameresult" DROP COLUMN "mg" CASCADE;
ALTER TABLE "tournament_gameresult" DROP COLUMN "mg_exist" CASCADE;
ALTER TABLE "tournament_gameresult" DROP COLUMN "mo" CASCADE;
ALTER TABLE "tournament_gameresult" DROP COLUMN "mo_exist" CASCADE;
ALTER TABLE "tournament_gameresult" DROP COLUMN "og" CASCADE;
ALTER TABLE "tournament_gameresult" DROP COLUMN "oo" CASCADE;
ALTER TABLE "tournament_gameresult" DROP COLUMN "ow" CASCADE;
ALTER TABLE "tournament_gameresult" DROP COLUMN "ow_exist" CASCADE;
ALTER TABLE "tournament_gameresult" DROP COLUMN "pm" CASCADE;
ALTER TABLE "tournament_gameresult" DROP COLUMN "pm_exist" CASCADE;

COMMIT;
        ''')


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0029_move_sequence'),
    ]

    operations = [

        migrations.RunPython(migrate_results),

    ]
