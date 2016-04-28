import { combineReducers } from "redux-immutable";
import playbackReducer from "./playback.js";
import searchReducer from "./search.js";

export default rootReducer = combineReducers({
    playback: playbackReducer,
    search: searchReducer
})