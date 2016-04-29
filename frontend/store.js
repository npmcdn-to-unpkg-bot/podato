import { createStore } from "redux";
import rootReducer from "./reducers/index.js";
import Immutable from "immutable"

export default createStore(rootReducer, Immutable.Map());
