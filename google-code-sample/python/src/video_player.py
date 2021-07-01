"""A video player class."""

from .video_library import VideoLibrary
from .playlist import Playlist
import random
import re

from src import video_library

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._current_video = None
        self._pause = False
        self._playlists = {}


    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")


    def show_all_videos(self):
        """Returns all videos."""
        all_videos = self._video_library.get_all_videos()
        all_videos.sort()
        print("Here's a list of all available videos:")
        [print(f"  {video.print_info()}") for video in all_videos]


    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)

        if video:
            if not video._flag:
                if self._current_video:
                    self.stop_video()

                print(f"Playing video: {video.title}")
                self._current_video = video
                self._pause = False
            else:
                print(f"Cannot play video: Video is currently flagged (reason: {video._flag})")

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

        videos = self._video_library.get_all_videos()
        videos = [video for video in videos if not video._flag]

        if len(videos) > 0:
            list_id = random.randint(0,len(videos)-1)
            self.play_video(videos[list_id].video_id)
        else:
            print("No videos available")


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
    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        
        if playlist_name.lower() in list(self._playlists.keys()):
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            playlist = Playlist(playlist_name)
            self._playlists[playlist_name.lower()] = playlist
            print(f"Successfully created new playlist: {playlist_name}")


    def load_playlist(self, playlist_name):
        """Loads a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        Returns:
            A Playlist object or None
        """
        try:
            return self._playlists[playlist_name.lower()]
        except:
            return None


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
                if not video._flag:
                    if not video_id in playlist._videos:
                        playlist._videos.append(video_id)
                        print(f"Added video to {playlist_name}: {video.title}")                        

                    else:
                        print(f"Cannot add video to {playlist_name}: Video already added")
                else:
                    print(f"Cannot add video to my_playlist: Video is currently flagged (reason: {video._flag})")
            else:
                print(f"Cannot add video to {playlist_name}: Video does not exist")
        else:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")


    def show_all_playlists(self):
        """Display all playlists."""

        if len(self._playlists) == 0:
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            keys = list(self._playlists.keys())
            keys.sort()
            [print(f"  {self._playlists[key]._name}") for key in keys]


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

                [print(f"  {video.print_info()}") for video in videos]
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
                title = self._video_library.get_video(video_id)._title
                print(f"Removed video from {playlist_name}: {title}")
            elif video_id not in self._video_library.get_all_video_ids():
                print(f"Cannot remove video from {playlist_name}: Video does not exist")
            else:
                print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
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
            print(f"Successfully removed all videos from {playlist_name}")

        else:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")


    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        try:
            del self._playlists[playlist_name.lower()]
            print(f"Deleted playlist: {playlist_name}")
        except:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")

# PART 3 #######################################################################

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        videos = self._video_library.get_all_videos()
        videos = [video for video in videos if not video._flag]

        regex = re.compile(f".*{search_term}.*", re.I)
        videos = [video for video in videos if regex.search(video._title)]

        if len(videos) > 0:
            videos.sort()
            print(f"Here are the results for {search_term}:")
            for i in range(len(videos)):
                print(f"{i+1}) {videos[i].print_info()}")
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")

            answer = input("YT> ")
            try:
                answer = int(answer)
                if answer in range(1,len(videos)+1):
                    self.play_video(videos[answer-1]._video_id)
            except:
                pass

        else:
            print(f"No search results for {search_term}")
        

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        videos = self._video_library.get_all_videos()
        videos = [video for video in videos if not video._flag]

        regex = re.compile(f"{video_tag}$", re.I)
        videos = [
            video for video in videos 
            if any([regex.match(tag) for tag in video._tags])]

        if len(videos) > 0:
            print(f"Here are the results for {video_tag}:")
            for i in range(len(videos)):
                print(f"{i+1}) {videos[i].print_info()}")
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")

            answer = input("YT> ")
            try:
                answer = int(answer)
                if answer in range(1,len(videos)+1):
                    self.play_video(videos[answer-1]._video_id)
            except:
                pass

        else:
            print(f"No search results for {video_tag}")
            
# PART 4 #######################################################################

    def flag_video(self, video_id, flag_reason="Not supplied"):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video = self._video_library.get_video(video_id)
        if video:
            if not video._flag:
                video._flag = flag_reason
                if self._current_video and self._current_video._video_id== video._video_id:
                    self.stop_video()
                print(f"Successfully flagged video: {video._title} (reason: {video._flag})")
            else:
                print("Cannot flag video: Video is already flagged")
        else:
            print("Cannot flag video: Video does not exist")


    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video = self._video_library.get_video(video_id)
        if video:
            if video._flag:
                video._flag = None
                print(f"Successfully removed flag from video: {video._title}")
            else:
                print("Cannot remove flag from video: Video is not flagged")
        else:
            print("Cannot remove flag from video: Video does not exist")
