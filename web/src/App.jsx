import {Routes, Route, BrowserRouter} from 'react-router-dom';
import LoginPage from './page/LoginPage';

const App = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route exact path='/' element={<LoginPage />} />
            </Routes>
        </BrowserRouter>
    );
}
export default App;