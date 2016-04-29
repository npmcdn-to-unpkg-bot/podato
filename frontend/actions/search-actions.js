import utils from "../utils";
import { createAction, assignAll } from "redux-act";

import store from '../store.js';

export const searchProgress = createAction("Indicates that a search is in progress");
export const searchComplete = createAction("Indicates that a search is complete, and results have been returned.");

assignAll([searchProgress, searchComplete], store);

export function search(query){
    searchProgress();
    return new Promise(() => {
        utils.fetchJSONP("https://itunes.apple.com/search",  {
            term: query,
            media: "podcast"
        }).then((result) => {
            searchComplete(result.results);
        });
    });
}
