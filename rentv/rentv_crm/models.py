from django.db import models

# Manager model
class Manager(models.Model):
    name = models.CharField(max_length=255)
    created_date = models.DateTimeField('Дата создания')
    last_login_date = models.DateTimeField('Последний вход')
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(verbose_name='Администратор?');
    
    def __str__(self):
        return self.name
    def get_absolute_path(self):
        return "/manager/%i" % self.id

# Status model
class Status(models.Model):
    title = models.CharField(verbose_name='Название статуса', max_length=255)
    description = models.TextField(max_length=1000, verbose_name='Описание статуса')
    
    def __str__(self):
        return self.title
    def get_absolute_path(self):
        return "/status/%i" % self.id

# Client model
class Client(models.Model):
    title = models.TextField(verbose_name='Название клиента', max_length=500)
    contact_person = models.CharField(max_length=255, verbose_name='Контактное лицо')
    contact_phone = models.CharField(max_length=255, verbose_name='Контактный телефон')
    contact_email = models.CharField(max_length=255, verbose_name='Контактный email')
    description = models.TextField(max_length=2000, verbose_name='Описание клиента')
    manager = models.ForeignKey(Manager, verbose_name='Курирующий менеджер')
    status = models.ForeignKey(Status, verbose_name='Статус клиента')
    
    def __str__(self):
        return self.title
    
    def get_absolute_path(self):
        return "/site/%i" % self.id 
    
# StatusChange model
class StatusChangeAction(models.Model):
    manager = models.ForeignKey(Manager, related_name='+')
    client = models.ForeignKey(Client, related_name='+')
    old_status = models.ForeignKey(Status, related_name='+')
    new_status = models.ForeignKey(Status, related_name='+')
    change_date = models.DateTimeField('Дата установки статуса')
    comment = models.TextField(max_length=3000)
    
    def __str__(self):
        return '{0} -> {1}'.format(self.old_status, self.new_status)
    
    def get_absolute_path(self):
        return "/status_changes/%i" % self.id 
    
    

    