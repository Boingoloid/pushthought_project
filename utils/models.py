from django.db import models


class CounterMixin(models.Model):
    counter = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def increase(self):
        self.counter += 1
        self.save()
        return True

    def save_recount(self):
        count = self.recount()
        self.counter = count
        self.save()
        return count

    def recount(self):
        count = self.counter_model.count()
        return count