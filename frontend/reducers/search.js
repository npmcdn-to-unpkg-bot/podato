import { createReducer } from "redux-act";
import Immutable from "immutable";
import {searchProgress, searchComplete} from "../actions/search-actions";

export default playbackReducer = createReducer({
    [searchProgress]: (state, payload) => state.merge({loading: true, results: []}),
    [searchComplete]: (state, payload) => state.merge({loading: false, results: payload})
}, Immutable.Map({
    loading: false,
    results: []
}));
