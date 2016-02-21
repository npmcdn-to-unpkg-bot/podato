from graphene.contrib.django.types import DjangoNode
from graphene.contrib.django.filter import DjangoFilterConnectionField
from graphene import relay, ObjectType
import graphene

from podcasts.models import Podcast, Episode
from podcasts.services import get_podcast_by_url, subscribe_user_by_urls, is_user_subscribed, unsubscribe_user_from_podcast
from graphqlserver.schema.user_nodes import UserNode


class PodcastNode(DjangoNode):
    class Meta:
        model = Podcast
        filter_fields = ['title', 'author', 'url', 'tags']
        filter_order_by = ['author']
        only_fields = ("url", "link", "title", "description", "copyright", "author", "episodes", "image", "tags",
                       "last_fetched", "subscribers", "user_is_subscribed")

    user_is_subscribed = graphene.BooleanField(description="Whether the current user is subscribed to this podcast")

    def resolve_user_is_subscribed(self, args, info):
        if not info.request_context.user.is_authenticated():
            return None
        return is_user_subscribed(info.request_context.user, self.instance)


class EpisodeNode(DjangoNode):
    class Meta:
        model = Episode
        only_fields = ['podcast', 'link', 'title', 'subtitle', 'description', 'content', 'explicit', 'author',
                         'summary', 'enclosure_type', 'enclosure_url', 'duration', 'image', 'published']
        filter_fields = ['published', 'podcast', 'explicit', 'author']
        filter_order_by = ['podcast', 'published', 'author', 'duration']


class Subscribe(relay.ClientIDMutation):

    class Input:
        feed_urls = graphene.List(graphene.String())

    user = graphene.Field(UserNode)
    success = graphene.List(graphene.String())

    @classmethod
    def mutate_and_get_payload(cls, input, info):
        if not info.request_context.user.is_authenticated():
            raise Exception("You need to be logged in to subscribe to podcasts.")

        urls = input["feed_urls"]
        result_dict = subscribe_user_by_urls(info.request_context.user, urls)
        for i in xrange(len(urls)):
            urls[i] = result_dict[urls[i]]

        return Subscribe(user=UserNode(info.request_context.user), success=urls)


class Unsubscribe(relay.ClientIDMutation):
    """Unsubscribe the current user from the podcast associated with the given podcast_url."""

    class Input:
        podcast_url = graphene.StringField()

    user = graphene.Field(UserNode)
    podcast = graphene.Field(PodcastNode)
    success = graphene.BooleanField()

    @classmethod
    def mutate_and_get_payload(cls, input, info):
        user = info.request_context.user
        if not user.is_authenticated():
            raise Exception("You need to be logged in to unsubscribe from podcasts.")

        podcast = get_podcast_by_url(input["podcast_url"])
        result = unsubscribe_user_from_podcast(user, podcast)

        return Unsubscribe(user=user, podcast=podcast, success=result)


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


class PodcastMutations(ObjectType):
    subscribe = graphene.Field(Subscribe)
    unsubscribe = graphene.Field(Unsubscribe)
    class Meta:
        abstract = True