from django.db.models.signals import post_save,pre_save,m2m_changed,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from tasks.models import Task

#django signals Task create korar por notification save
# @receiver(post_save,sender=Task)
# def notify_task_creation(sender,instance,created,**kwargs):
#     print('Sender',sender)
#     print("Instance",instance)
#     print(kwargs)
#     print(created)
#     if created:
#         instance.is_completed = True
#         instance.save()

# Task save korar age notification send
# @receiver(pre_save,sender=Task)
# def notify_task_creation(sender,instance,**kwargs):
#     print('Sender',sender)
#     print("Instance",instance)
#     print(kwargs)
#     instance.is_completed = True
#     instance.save()


@receiver(m2m_changed,sender=Task.assigned_to.through)
def notify_task_creation(sender,instance,action,**kwargs):
    if action == 'post_add':
            assigned_emails=[emp.email for emp in instance.assigned_to.all()]
            send_mail(
                "New Task Assigned",
                f"You have been assigned to the task:{instance.title}",
                "alamincse16th@gmail.com",
                assigned_emails,
                
            )

@receiver(post_delete,sender=Task)
def delete_associate_details(sender,instance,**kwargs):
    if instance.details:
        print(instance)
        instance.details.delete()
        print("Delete Successfully")