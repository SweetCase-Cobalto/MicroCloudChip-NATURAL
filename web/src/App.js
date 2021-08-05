import {Route} from 'react-router-dom';

// Path
import LoginPage from './page/LoginPage';
import SettingsPage from './page/SettingsPage';
import StoragePage from './page/StoragePage';
import AccountsPage from './page/AccountsPage';

const App = () => {
    
    return (
        <div>
            <Route exact path='/' component={LoginPage} />
            <Route exact path='/settings' component={SettingsPage} />
            <Route path="/storage/" component={StoragePage} />
            <Route exact path="/accounts" component={AccountsPage} />
        </div>
    );
}
export default App;