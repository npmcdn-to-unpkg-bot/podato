import { createStore } from "redux";
import rootReducer from "./reducers/index.js";
import Immutable from "immutable"

export default store = createStore(rootReducer, Immutable.Map());
