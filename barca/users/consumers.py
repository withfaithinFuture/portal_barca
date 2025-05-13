import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import LikeDislike


class LikeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get("user")

        if isinstance(self.user, AnonymousUser):
            await self.close(code=4001) 
            return

        self.content_type = self.scope['url_route']['kwargs']['content_type']
        self.content_id = self.scope['url_route']['kwargs']['content_id']
        self.room_group_name = f'likes_{self.content_type}_{self.content_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        await self.send_initial_data()

    async def send_initial_data(self):
        likes, dislikes, user_vote = await self.get_votes_data()
        await self.send(text_data=json.dumps({
            'type': 'like_data',
            'likes': likes,
            'dislikes': dislikes,
            'user_vote': user_vote
        }))

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            if data.get('type') == 'like_action':
                vote = int(data['vote'])
                await self.handle_vote(vote)

                await self.send_update_to_group()

        except Exception as e:
            print(f"Error processing vote: {e}")

    async def send_update_to_group(self):
        likes, dislikes, user_vote = await self.get_votes_data()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_like_data',
                'likes': likes,
                'dislikes': dislikes,
                'user_vote': user_vote
            }
        )

    async def send_like_data(self, event):
        """Обработчик для групповых рассылок"""
        await self.send(text_data=json.dumps({
            'type': 'like_update',
            'likes': event['likes'],
            'dislikes': event['dislikes'],
            'user_vote': event['user_vote']
        }))

    @database_sync_to_async
    def get_votes_data(self):
        likes = LikeDislike.objects.filter(
            content_type=self.content_type,
            content_id=self.content_id,
            vote=1
        ).count()

        dislikes = LikeDislike.objects.filter(
            content_type=self.content_type,
            content_id=self.content_id,
            vote=-1
        ).count()

        user_vote = 0
        if not isinstance(self.user, AnonymousUser):
            try:
                user_vote = LikeDislike.objects.get(
                    user=self.user,
                    content_type=self.content_type,
                    content_id=self.content_id
                ).vote
            except LikeDislike.DoesNotExist:
                pass

        return likes, dislikes, user_vote

    @database_sync_to_async
    def handle_vote(self, vote):
        if not isinstance(self.user, AnonymousUser):
            LikeDislike.objects.update_or_create(
                user=self.user,
                content_type=self.content_type,
                content_id=self.content_id,
                defaults={'vote': vote}
            )
