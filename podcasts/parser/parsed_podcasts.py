import itertools
from django.db import transaction

from podcasts.models import Podcast, Episode, Category


#warning constants
W_NO_IMAGE = "W_NO_IMAGES"
W_NO_AUTHOR = "W_NO_AUTHOR"
W_NO_DESCRIPTION = "W_NO_DESCRIPTION"
W_NO_CATEGORIES = "W_NO_CATEGORIES"
W_NO_EXPLICIT = "W_NO_EXPLICIT"
W_NO_LANGUAGE = "W_NO_LANGUAGE"
W_NO_GUID = "W_NO_GUID"
W_NO_DURATION = "W_NO_DURATION"
W_NO_EPISODE_AUTHOR = "W_NO_EPISODE_AUTHOR"
W_DUPLICATE_GUID = "W_DUPLICATE_GUID"


def get_warning_message(warning, episode=None):
    """Get the warning message for e given warning constant. If the warning is about a specific episode, pass it in."""
    messages = {
        W_NO_IMAGE: "This podcast has no image.",
        W_NO_AUTHOR: "The author is not specified in this podcast feed.",
        W_NO_DESCRIPTION: "There's no description for this podcast in the feed",
        W_NO_CATEGORIES: "The feed of this podcast doesn't specify the categor(y/ies) it is in.",
        W_NO_EXPLICIT: "This podcast's feed doesn't say whether it contains explicit content or not.",
        W_NO_LANGUAGE: "The feed for this podcast does not specify the language.",
        W_NO_GUID: "Episode \"%s\" has no GUID.",
        W_NO_DURATION: "The duration of the episode \"%s\" is not (correctly) specified in the podcast feed",
        W_NO_EPISODE_AUTHOR: "The episode \"%s\"'s author is not specified in the podcast feed.",
        W_DUPLICATE_GUID: "There are multiple episodes in this feed with guid \"%s\"."
    }

    if warning in {W_NO_GUID, W_NO_DURATION, W_NO_EPISODE_AUTHOR}:
        return messages[warning] % episode.title
    elif warning == W_DUPLICATE_GUID:
        return messages[warning] % episode.guid
    return messages[warning]


class ParsedPodcast(object):
    """The ParsedPodcast class represents the result of parsing a podcast feed.

    This class exists to distinguish between the podcast's data as represented by the feed, and the data we store in the
    database. In the database, data is often structured and/or represented differently.
    """

    def __init__(self, url=None, link=None, title=None, description=None, author=None, image=None, copyright=None,
                 tags=None, language=None, last_fetched=None, categories=None, owner=None, episodes=None,
                 explicit=None):
        self.url = url
        self.link = link
        self.title = title
        self.description = description
        self.author = author
        self.image = image
        self.tags = tags or []
        self.categories = categories or []
        self.language = language
        self.last_fetched = last_fetched
        self.owner = owner
        self.episodes = episodes or []
        self.copyright = copyright
        self.explicit = explicit

        self.warnings = []


    def validate(self):
        """Validates the data stored in the feed. This populates this.warnings"""
        if self.image is None:
            self.warnings.append(W_NO_IMAGE)
        if self.author is None:
            self.warnings.append(W_NO_AUTHOR)
        if self.description is None:
            self.warnings.append(W_NO_DESCRIPTION)
        if self.categories is None or len(self.categories) == 0:
            self.warnings.append(W_NO_CATEGORIES)
        if self.explicit is None:
            self.warnings.append(W_NO_EXPLICIT)
        if self.language is None:
            self.warnings.append(W_NO_LANGUAGE)

        for episode in self.episodes:
            episode.validate()

        keyfunc = lambda ep: ep.guid
        for guid, episodes in itertools.groupby(sorted(self.episodes, key=keyfunc), key=keyfunc):
            episodes_with_guid = list(episodes)
            if len(episodes_with_guid) > 1:
                episodes_with_guid[0].warnings.append(W_DUPLICATE_GUID)
                for ep in episodes_with_guid[1:]:
                    self.episodes.remove(ep)

        if self.explicit == "clean":
            self.explicit = "c"
        if self.explicit == "yes":
            self.explicit = "e"
        self.explicit = "u"

    @transaction.atomic
    def save_to_db(self):
        """Store the podcast and all its related models in the database."""
        podcast_obj, created = Podcast.objects.update_or_create(url=self.url, defaults={
            "link": self.link,
            "title": self.title,
            "description": self.description,
            "author": self.author,
            "image": self.image,
            "tags": self.tags,
            "language": self.language,
            "last_fetched": self.last_fetched,
            "owner_name": self.owner.name,
            "owner_email": self.owner.email,
            "copyright": self.copyright,
            "explicit": self.explicit,
            "warnings": self.warnings
        })

        if not created:
            podcast_obj.episodes.clear()

        episode_objs = [ep.save_to_db(podcast_obj) for ep in self.episodes]
        podcast_obj.episodes = episode_objs

        category_objs = []
        for category in self.categories:
            parent = None
            for name in category:
                category, _ = Category.objects.get_or_create(name=name, parent_name=parent, defaults={"visible": False})
                category_objs.append(category)
                parent = name

        podcast_obj.categories.set(category_objs, clear=True)
        return podcast_obj


class ParsedEpisode(object):
    """The ParsedEpisode class represents a podcast episode as parsed from a podcast feed."""
    def __init__(self, guid=None, link=None, title=None, subtitle=None, summary=None, description=None, content=None, image=None, author=None, duration=None,
                 published=None, explicit=None, enclosure=None):
        self.guid = guid
        self.link = link
        self.title = title
        self.subtitle = subtitle
        self.summary = summary
        self.description = description
        self.content = content
        self.image = image
        self.author = author
        self.duration = duration
        self.published = published
        self.explicit = explicit
        self.enclosure = enclosure
        self.warnings = []

    def validate(self):
        if not self.guid:
            self.warnings.append(W_NO_GUID)
        if not self.duration or self.duration == 0:
            self.warnings.append(W_NO_DURATION)
        if not self.author:
            self.warnings.append(W_NO_EPISODE_AUTHOR)

        if self.explicit == "clean":
            self.explicit = "c"
        if self.explicit == "yes":
            self.explicit = "e"
        self.explicit = "u"

        self.guid = self.guid or self.link

    def save_to_db(self, podcast):
        """Converts this ParsedEpisode object to an Episode object to be stored in the db.

        You probably don't want to call this directly, but rather call save_to_db on the podcast. That methods ensures
        that all a podcast's episodes are correctly saved to the database."""
        episode_obj, _ = Episode.objects.update_or_create(guid=self.guid, defaults={
            "podcast": podcast,
            "link": self.link,
            "title": self.title,
            "subtitle": self.subtitle,
            "summary": self.summary,
            "description": self.description,
            "content": self.content,
            "image": self.image,
            "author": self.author,
            "duration": self.duration,
            "published": self.published,
            "explicit": self.explicit,
            "enclosure_url": self.enclosure.url,
            "enclosure_type": self.enclosure.type,
            "warnings": self.warnings
        })

        return episode_obj


class Person(object):
    """Person represents a person, as given in a podcast feed."""
    def __init__(self, name, email):
        self.name = name
        self.email = email


class Enclosure(object):
    """The Closure class represents an enclosure in a podcast feed."""
    def __init__(self, url, type=None, length=None):
        self.url = url
        self.type = type
        self.length = length