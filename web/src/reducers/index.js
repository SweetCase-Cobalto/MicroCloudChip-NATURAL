import { combineReducers } from "redux";
import { persistReducer } from "redux-persist";
import storage from "redux-persist/lib/storage";

import { DirListReducer } from "./DirListReducer";
import { ConnectedUserReducer } from "./ConnectedUserReducer";

// Redux Local Storage [Setting]
const persistConfig = {
    key: "root",
    storage,
    whitelist: ["ConnectedUserReducer"]
}

const rootReducer = combineReducers({
    DirListReducer, ConnectedUserReducer
});

export default persistReducer(persistConfig, rootReducer);