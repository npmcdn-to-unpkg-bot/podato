import PlaybackManager from "../playback-manager.js";
import {createAction, assignAll} from "redux-act";

import store from '../store.js';

export const setEpisode = createAction("Sets the currently playing episode")
export const setPlaying = createAction("Sets whether the player is currently playing media, or stopped/paused");
export const setPosition = createAction("Sets the playback position in seconds");
export const setDuration = createAction("Sets the duration of the currently playing media.")
assignAll([setEpisode, setPlaying, setPosition, setDuration], store);

export function playEpisode(episode){
    setEpisode(episode);
    setPlaying(true);
    PlaybackManager.setEpisode(episode);
    PlaybackManager.play();
}

export function pause(){
    setPlaying(false);
    PlaybackManager.pause();
}

export function resume(){
    setPlaying(true);
    PlaybackManager.play();
}

export function seek(secs){
    setPosition(secs);
    PlaybackManager.seek(secs)
}


PlaybackManager.on("time", (playback) => {
    setPosition(playback.getCurrentTime());
    setDuration(playback.getDuration());
});

