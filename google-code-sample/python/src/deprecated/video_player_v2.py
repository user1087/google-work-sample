"""A video player class."""

from .video_library import VideoLibrary
from .playlist import Playlist
import random
import pickle
import json
import os


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._current_video = None
        self._pause = False
        self._pl_dir = "./playlists" # Directory to save playlist

        if not os.path.exists(self._pl_dir):
            os.mkdir(self._pl_dir)

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        all_videos = self._video_library.get_all_videos()
        all_videos.sort()
        print("Here's a list of all available videos:")
        [print(f"  {video.title} ({video.video_id}) [{' '.join(video.tags)}]") 
         for video in all_videos]

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)

        if video:
            if self._current_video:
                self.stop_video()

            print(f"Playing video: {video.title}")
            self._current_video = video
            self._pause = False
        else:
            print("Cannot play video: Video does not exist")

    def stop_video(self):
        """Stops the current video."""

        if self._current_video:
            print(f"Stopping video: {self._current_video.title}")
            self._current_video = None
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""

        all_videos = self._video_library.get_all_videos()
        list_id = random.randint(0,len(all_videos)-1)
        self.play_video(all_videos[list_id].video_id)

    def pause_video(self):
        """Pauses the current video."""

        if not self._current_video: # Nothing playing
            print("Cannot pause video: No video is currently playing")
        elif self._pause: 
            print(f"Video already paused: {self._current_video.title}")
        else:
            print(f"Pausing video: {self._current_video.title}")
            self._pause = True

    def continue_video(self):
        """Resumes playing the current video."""

        if self._pause:
            print(f"Continuing video: {self._current_video.title}")
            self._pause = False
        elif not self._current_video:
            print("Cannot continue video: No video is currently playing")
        else :
            print("Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""

        if self._current_video:
            video = self._current_video
            print(f"Currently playing: {video.title} ({video.video_id}) [{' '.join(video.tags)}]", end="")

            if self._pause:
                print(" - PAUSED")
            else:
                print("") # Go to next line
        else:
            print("No video is currently playing")

# PART 2 ######################################################################
    def save_playlist(self, playlist):
        with open(f"{self._pl_dir}/{playlist._name.lower()}", "wb") as f:
            pickle.dump(playlist, f)

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        
        if os.path.exists(f"{self._pl_dir}/{playlist_name.lower()}"):
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            playlist = Playlist(playlist_name)
            self.save_playlist(playlist)

            print(f"Successfully created new playlist: {playlist_name}")

    def load_playlist(self, playlist_name):
        """Loads a playlist with a given name.

        Args:
            playlist_name: The playlist name.

        Returns:
            A Playlist object
        """
        if not os.path.exists(f"{self._pl_dir}/{playlist_name.lower()}"):
            return None
        else:
            with open(f"{self._pl_dir}/{playlist_name.lower()}", "rb") as f:
                return pickle.load(f)

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """

        playlist = self.load_playlist(playlist_name)

        if playlist:
            video = self._video_library.get_video(video_id)
            if video:
                if video_id in playlist._videos:
                    print(f"Cannot add video to {playlist_name}: Video already added")

                else:
                    playlist._videos.append(video_id)
                    self.save_playlist(playlist)

                    print(f"Added video to {playlist_name}: {video.title}")

            else:
                print(f"Cannot add video to {playlist_name}: Video does not exist")

        else:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")

    def show_all_playlists(self):
        """Display all playlists."""

        playlists = []
        for playlist_name in os.listdir(self._pl_dir):
            playlists.append(self.load_playlist(playlist_name))
        
        if len(playlists) == 0:
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            playlists.sort()
            [print(f"  {playlist._name}") for playlist in playlists]

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        playlist = self.load_playlist(playlist_name)
        if playlist:
            print(f"Showing playlist: {playlist_name}")
            if len(playlist._videos) == 0:
                print("  No videos here yet")
            else:
                videos =[
                    self._video_library.get_video(video_id) 
                    for video_id in playlist._videos]

                [print(f"  {video.title} ({video.video_id}) [{' '.join(video.tags)}]")
                 for video in videos]
        else:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlist = self.load_playlist(playlist_name)
        if playlist:
            if video_id in playlist._videos:
                playlist._videos = [video for video in playlist._videos 
                                    if video != video_id]
                self.save_playlist(playlist)
                title = self._video_library.get_video(video_id)._title
                print(f"Removed video from {playlist_name}: {title}")
            else:
                print(f"Cannot remove video from {playlist_name}: Video does not exist")
        else:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self.load_playlist(playlist_name)
        if playlist:
            playlist._videos = []
            self.save_playlist(playlist)
            print(f"Successfully removed all videos from {playlist_name}")

        else:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self.load_playlist(playlist_name)
        if playlist:
            os.remove(f"{self._pl_dir}/{playlist._name.lower()}")
            print(f"Deleted playlist: {playlist_name}")

        else:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")

###############################################################################

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        print("search_videos needs implementation")

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        print("search_videos_tag needs implementation")

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        print("flag_video needs implementation")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")
