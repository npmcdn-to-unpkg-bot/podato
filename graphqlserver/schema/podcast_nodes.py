from graphene.contrib.django.types import DjangoNode
from graphene.contrib.django.filter import DjangoFilterConnectionField
from graphene import relay, ObjectType
import graphene

from podcasts.models import Podcast, Episode
from podcasts.services import get_podcast_by_url

class PodcastNode(DjangoNode):
    class Meta:
        model = Podcast
        filter_fields = ['title', 'author', 'url', 'tags']
        filter_order_by = ['author']
        only_fields = ("url", "link", "title", "description", "copyright", "author", "episodes", "image", "tags",
                       "last_fetched", "")


class EpisodeNode(DjangoNode):
    class Meta:
        model = Episode
        only_fields = ['podcast', 'link', 'title', 'subtitle', 'description', 'content', 'explicit', 'author',
                         'summary', 'enclosure_type', 'enclosure_url', 'duration', 'image', 'published']
        filter_fields = ['published', 'podcast', 'explicit', 'author']
        filter_order_by = ['podcast', 'published', 'author', 'duration']


class PodcastQuery(ObjectType):
    podcast = relay.NodeField(PodcastNode)
    episode = relay.NodeField(EpisodeNode)
    all_podcasts = DjangoFilterConnectionField(PodcastNode)
    all_episodes = DjangoFilterConnectionField(EpisodeNode)
    podcast_by_url = graphene.Field(PodcastNode, url=graphene.String())

    def resolve_podcast_by_url(self, args, info):
        return PodcastNode(get_podcast_by_url(args.get("url")))

    class Meta:
        abstract = True
