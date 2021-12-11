import {Routes, Route} from 'react-router-dom';
import LoginPage from './page/LoginPage';
import StoragePage from './page/StoragePage';
import AccountPage from './page/AccountPage';

const App = () => {
    return (
        <div>
            <Routes>
                <Route exact path='/' element={<LoginPage />} />
                <Route exact path='/account' element={<AccountPage />} />
                <Route path = '/storage/' element={<StoragePage />} />
            </Routes>
        </div>
    );
}
export default App;