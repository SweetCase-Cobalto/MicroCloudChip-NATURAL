import { combineReducers } from "redux";
import { persistReducer } from "redux-persist";
import storage from "redux-persist/lib/storage";

import { DirListReducer } from "./DirListReducer";
import { ConnectedUserReducer } from "./ConnectedUserReducer";
import { UserListReducer } from "./UserListReducer";
import { SelectedAccountReducer } from "./SelectedAccountReducer";
import { SelectedDirReducer } from "./SelectedDirReducer";

// Redux Local Storage [Setting]
const persistConfig = {
    key: "root",
    storage,
    whitelist: ["ConnectedUserReducer"]
}

const rootReducer = combineReducers({
    DirListReducer, 
    ConnectedUserReducer, 
    UserListReducer,
    SelectedAccountReducer,
    SelectedDirReducer
});

export default persistReducer(persistConfig, rootReducer);