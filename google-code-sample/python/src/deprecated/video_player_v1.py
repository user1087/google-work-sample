"""A video player class."""

from .video_library import VideoLibrary
import random
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
        [print(f"{video.title} ({video.video_id}) [{' '.join(video.tags)}]") 
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
            print(f"Stopping Video: {self._current_video.title}")
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
            print(f"{video.title} ({video.video_id}) [{' '.join(video.tags)}]", end="")

            if self._pause:
                print(" - PAUSED")
            else:
                print("") # Go to next line
        else:
            print("No video is currently playing")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        
        if os.path.exists(f"{self._pl_dir}/{playlist_name.lower()}.json"):
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            playlist = {
                "name": playlist_name,
                "videos": []
            }
            with open(f"{self._pl_dir}/{playlist_name.lower()}.json", "w", encoding="utf-8") as f:
                json.dump(playlist, f, indent=4, ensure_ascii=False)

            print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        if not os.path.exists(f"{self._pl_dir}/{playlist_name.lower()}.json"):
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")

        else:
            video = self._video_library.get_video(video_id)

            if video:
                with open(f"{self._pl_dir}/{playlist_name.lower()}.json") as f:
                    playlist = json.load(f)

                if video_id in playlist["videos"]:
                    print(f"Cannot add video to {playlist_name}: Video already added")
                else:
                    playlist["videos"].append(video_id)
                    with open(f"{self._pl_dir}/{playlist_name.lower()}.json", "w", encoding="utf-8") as f:
                        json.dump(playlist, f, indent=4, ensure_ascii=False)

                    print(f"Added video to {playlist_name}: {video.title}")

            else:
                print(f"Cannot add video to {playlist_name}: Video does not exist")

###############################################################################

    def show_all_playlists(self):
        """Display all playlists."""

        for playlist

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        print("show_playlist needs implementation")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        print("remove_from_playlist needs implementation")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        print("clears_playlist needs implementation")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        print("deletes_playlist needs implementation")

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
