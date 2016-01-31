#warnings
import itertools

W_NO_IMAGE = "This podcast has no image."
W_NO_AUTHOR = "The author is not specified in this podcast feed."
W_NO_DESCRIPTION = "There's no description for this podcast in the feed"
W_NO_CATEGORIES = "The feed of this podcast doesn't specify the categor(y/ies) it is in."
W_NO_EXPLICIT = "This podcast's feed doesn't say whether it contains explicit content or not."
W_NO_LANGUAGE = "The feed for this podcast does not specify the language."
W_NO_GUID = "Episode \"%s\" has no GUID."
W_NO_DURATION = "The duration of the episode \"%s\" is not (correctly) specified in the podcast feed"
W_NO_EPISODE_AUTHOR = "The episode \"%s\"'s author is not specified in the podcast feed."
W_DUPLICATE_GUID = "There are multiple episodes in this feed with guid \"%s\"."


class Podcast(object):
    """The podcast class represents a podcast."""

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
            episode.validate(self.warnings)

        keyfunc = lambda ep: ep.guid
        for guid, episodes in itertools.groupby(sorted(self.episodes, key=keyfunc), key=keyfunc):
            if len(list(episodes)) > 1:
                self.warnings.append(W_DUPLICATE_GUID % guid)



class Episode(object):
    """The Episode class represents a podcast episode. I"""
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

    def validate(self, warnings):
        if not self.guid:
            warnings.append(W_NO_GUID % self.title)
        if not self.duration or self.duration == 0:
            warnings.append(W_NO_DURATION % self.title)
        if not self.author:
            warnings.append(W_NO_EPISODE_AUTHOR % self.title)

        self.guid = self.guid or self.link


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