// Main Reducer
import { persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';
import { combineReducers } from 'redux';
import { UserInfoReducer } from './UserInfoReducer';


// Redux Local Storage
const persistConfig = {
    key: "root",
    storage,
    whitelist: ["UserInfoReducer"]
}

const rootReducer = combineReducers({
    UserInfoReducer
});
export default persistReducer(persistConfig, rootReducer);
