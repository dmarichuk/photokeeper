from django.apps import AppConfig

class AlbumsConfig(AppConfig):
    name = 'albums'
    
    def ready(self):
        from actstream import registry
        from users.models import User, Follow
        registry.register(User, Follow, self.get_model('Album'), self.get_model('Photo'), self.get_model('Comment'))
