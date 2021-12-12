// Main Reducer
import { persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';
import { combineReducers } from 'redux';
import { TokenReducer } from './TokenReducer';


// Redux Local Storage
const persistConfig = {
    key: "root",
    storage,
    whitelist: ["TokenReducer"]
}

const rootReducer = combineReducers({
    TokenReducer
});
export default persistReducer(persistConfig, rootReducer);
