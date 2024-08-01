# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Category(models.Model):
    categoryid = models.AutoField(db_column='categoryID', primary_key=True)  # Field name made lowercase.
    categoryname = models.TextField()

    class Meta:
        managed = False
        db_table = 'Category'


class Colleges(models.Model):
    collegeid = models.AutoField(db_column='collegeID', primary_key=True)  # Field name made lowercase.
    collegename = models.TextField(db_column='collegeName')  # Field name made lowercase.
    project985 = models.BooleanField()
    project211 = models.BooleanField()
    top = models.BooleanField()
    provinceid = models.ForeignKey('Provinces', models.DO_NOTHING, db_column='provinceID_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Colleges'


class Firstlevel(models.Model):
    firstlevelid = models.AutoField(db_column='firstlevelID', primary_key=True)  # Field name made lowercase.
    firstlevelname = models.TextField(db_column='firstlevelName')  # Field name made lowercase.
    subjectid = models.IntegerField(db_column='subjectID')  # Field name made lowercase.
    subjectname = models.TextField(db_column='subjectName')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Firstlevel'


class Majors(models.Model):
    majorname = models.TextField(db_column='majorName')  # Field name made lowercase.
    year = models.IntegerField()
    minscore = models.IntegerField(db_column='minScore')  # Field name made lowercase.
    avgscore = models.IntegerField(db_column='avgScore', blank=True, null=True)  # Field name made lowercase.
    maxscore = models.IntegerField(db_column='maxScore', blank=True, null=True)  # Field name made lowercase.
    firstlevelids = models.TextField(db_column='firstlevelIDs', blank=True, null=True)  # Field name made lowercase.
    categoryid = models.ForeignKey(Category, models.DO_NOTHING, db_column='categoryID_id', blank=True, null=True)  # Field name made lowercase.
    collegeid = models.ForeignKey(Colleges, models.DO_NOTHING, db_column='collegeID_id', blank=True, null=True)  # Field name made lowercase.
    provinceid = models.ForeignKey('Provinces', models.DO_NOTHING, db_column='provinceID_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Majors'


class Provinces(models.Model):
    provinceid = models.AutoField(db_column='provinceID', primary_key=True)  # Field name made lowercase.
    provincename = models.TextField(db_column='provinceName')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Provinces'


class Rankings(models.Model):
    year = models.IntegerField()
    score = models.IntegerField()
    rank = models.IntegerField()
    categoryid = models.ForeignKey(Category, models.DO_NOTHING, db_column='categoryID_id', blank=True, null=True)  # Field name made lowercase.
    provinceid = models.ForeignKey(Provinces, models.DO_NOTHING, db_column='provinceID_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Rankings'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Bestcity(models.Model):
    city_id = models.AutoField(primary_key=True, blank=True)
    city = models.TextField(blank=True, null=True)
    city_score = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bestCity'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Total2020(models.Model):
    total_id = models.AutoField(primary_key=True, blank=True)
    total_majorname = models.TextField(db_column='total_majorName', blank=True, null=True)  # Field name made lowercase.
    total_year = models.IntegerField(blank=True, null=True)
    total_minscore = models.IntegerField(db_column='total_minScore', blank=True, null=True)  # Field name made lowercase.
    total_categoryid_id = models.IntegerField(db_column='total_categoryID_id', blank=True, null=True)  # Field name made lowercase.
    total_collegeid_id = models.IntegerField(db_column='total_collegeID_id', blank=True, null=True)  # Field name made lowercase.
    total_c1 = models.TextField(blank=True, null=True)
    total_c2 = models.TextField(blank=True, null=True)
    total_college_loc = models.TextField(blank=True, null=True)
    total_provinceloc = models.TextField(db_column='total_provinceLoc', blank=True, null=True)  # Field name made lowercase.
    total_cityloc_field = models.TextField(db_column='total_cityLoc\n', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    total_adcode = models.IntegerField(blank=True, null=True)
    total_cityscore_field = models.TextField(db_column='total_cityScore\n', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'. This field type is a guess.
    total_c2code = models.TextField(blank=True, null=True)  # This field type is a guess.
    total_majorscore_field = models.TextField(db_column='total_majorScore\n', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'. This field type is a guess.
    total_preranking = models.IntegerField(db_column='total_preRanking', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'total2020'


class Total2020Init(models.Model):
    total_id = models.AutoField(primary_key=True, blank=True)
    total_majorname = models.TextField(db_column='total_majorName', blank=True, null=True)  # Field name made lowercase.
    total_year = models.IntegerField(blank=True, null=True)
    total_minscore = models.IntegerField(db_column='total_minScore', blank=True, null=True)  # Field name made lowercase.
    total_categoryid_id = models.IntegerField(db_column='total_categoryID_id', blank=True, null=True)  # Field name made lowercase.
    total_collegeid_id = models.IntegerField(db_column='total_collegeID_id', blank=True, null=True)  # Field name made lowercase.
    total_c1 = models.TextField(blank=True, null=True)
    total_c2 = models.TextField(blank=True, null=True)
    total_college_loca = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'total2020_init'
