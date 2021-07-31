import {Route} from 'react-router-dom';

// Path
import LoginPage from './page/LoginPage';
import SettingsPage from './page/SettingsPage';
import StoragePage from './page/StoragePage';

const App = () => {
    
    return (
        <div>
            <Route exact path='/' component={LoginPage} />
            <Route exact path='/settings' component={SettingsPage} />
            <Route path="/storage/" component={StoragePage} />
        </div>
    );
}
export default App;