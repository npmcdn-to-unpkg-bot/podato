import { createReducer } from "redux-act";
import Immutable from "immutable";
import {setPlaying, setPosition, setDuration, setEpisode} from "../actions/playback-actions";

export default playbackReducer = createReducer({
    [setEpisode]: (state, payload) => state.set("episode", payload),
    [setDuration]: (state, payload) => state.set("duration", payload),
    [setPlaying]: (state, payload) => state.set("playing", payload),
    [setPosition]: (state, payload) => state.set("position", payload)
}, Immutable.Map({
    episode: null,
    position: 0,
    duration: 0,
    playing: false
}));
