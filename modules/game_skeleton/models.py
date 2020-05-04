from django.db import models


class HeroClass(models.Model):
    name = models.CharField(max_length=500)
    parent = models.OneToOneField(
        'HeroClass', on_delete=models.SET_NULL, null=True, blank=True
    )
    capacity = models.FloatField(
        help_text='How many experience points should be collected '
                  'to finish the hero class.'
    )
    image = models.ImageField(upload_to='hero_class/', null=True, blank=True)
    is_draft = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Hero classes'


class Gift(models.Model):
    hero_class = models.ForeignKey(
        'HeroClass', on_delete=models.SET_NULL, related_name='gifts',
        null=True,
    )

    name = models.CharField(max_length=500)
    image = models.ImageField(upload_to='gifts/', null=True, blank=True)
    remain = models.FloatField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=4)

    is_group_wide = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Cristal(models.Model):
    name = models.CharField(max_length=500)
    image = models.ImageField(upload_to='cristal/', null=True, blank=True)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()
    cristal = models.OneToOneField(
        'Cristal', on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name


class Rule(models.Model):
    name = models.CharField(max_length=500)
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Gradation(models.Model):
    name = models.CharField(max_length=500)
    money = models.DecimalField(max_digits=10, decimal_places=4, default=0.0)
    experience = models.FloatField()
    rule = models.ForeignKey(
        'Rule', on_delete=models.CASCADE, related_name='gradations'
    )

    def __str__(self):
        return self.name


class Penalty(models.Model):
    name = models.CharField(max_length=500)
    experience = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Penalties'
