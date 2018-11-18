from django.db import models


class ModelManager(models.Manager):
    def get_queryset(self):
        return super(ModelManager, self).get_queryset().filter(isValid=1)


# 数据字典模型
class DataDic(models.Model):
    dataDicName = models.CharField(max_length=50, db_column='data_dic_name')
    dataDicValue = models.CharField(max_length=50, db_column='data_dic_value')
    isValid = models.IntegerField(db_column='is_valid')
    createDate = models.DateTimeField(db_column='create_date', auto_now_add=True)
    updateDate = models.DateTimeField(db_column='update_date', auto_now_add=True)

    objects = ModelManager()

    class Meta:
        db_table = 't_datadic'
