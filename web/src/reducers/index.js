import { combineReducers } from "redux";
import { DirListReducer } from "./DirListReducer";
import { ConnectedUserReducer } from "./ConnectedUserReducer";

export const rootReducer = combineReducers({
    DirListReducer, ConnectedUserReducer
});