"""A video class."""

from typing import Sequence


class Video:
    """A class used to represent a Video."""

    def __init__(self, video_title: str, video_id: str, video_tags: Sequence[str]):
        """Video constructor."""
        self._title = video_title
        self._video_id = video_id

        # Turn the tags into a tuple here so it's unmodifiable,
        # in case the caller changes the 'video_tags' they passed to us
        self._tags = tuple(video_tags)
        self._flag = None

    @property
    def title(self) -> str:
        """Returns the title of a video."""
        return self._title

    @property
    def video_id(self) -> str:
        """Returns the video id of a video."""
        return self._video_id

    @property
    def tags(self) -> Sequence[str]:
        """Returns the list of tags of a video."""
        return self._tags


    def print_info(self):
        info = f"{self._title} ({self._video_id}) [{' '.join(self._tags)}]"
        if self._flag:
            info += f" - FLAGGED (reason: {self._flag})"

        return info

    def __lt__(self, other):
        return self.title < other.title

    def __gt__(self, other):
       return self.title > other.title

    def __le__(self, other):
       return self.title <= other.title

    def __ge__(self, other):
       return self.title >= other.title

    def __eq__(self, other):
       return self.title == other.title

    def __ne__(self, other):
       return self.title != other.title

