import {Routes, Route} from 'react-router-dom';
import LoginPage from './page/LoginPage';
import StoragePage from './page/StoragePage';

const App = () => {
    return (
        <div>
            <Routes>
                <Route exact path='/' element={<LoginPage />} />
                <Route path = '/storage/' element={<StoragePage />} />
            </Routes>
        </div>
    );
}
export default App;