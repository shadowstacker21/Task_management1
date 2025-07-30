from django.apps import AppConfig


class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'
    
    #signals pathanor jonno ready korte hobe
    def ready(self):
        import tasks.signals
