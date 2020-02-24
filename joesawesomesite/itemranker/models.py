from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class RankLists(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    list_name = models.CharField('Listname', max_length=100)

    class Meta:
        abstract = True


class PersonalList(RankLists):
    list_id = models.AutoField(primary_key=True)
    list_json = models.TextField("Rank List")

    def __str__(self):
        return f'{self.list_name} by {self.user.username}'


class MasterList(RankLists):
    list_id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.list_name


class MasterItem(models.Model):
    master_list = models.ForeignKey(MasterList, on_delete=models.CASCADE)
    item_name = models.CharField('Item Name', max_length=35)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.item_name} from {self.master_list.list_name}'

    def add_vote(self):
        self.votes += 1
