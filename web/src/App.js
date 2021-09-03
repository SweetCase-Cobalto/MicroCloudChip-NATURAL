import {Route, Switch} from 'react-router-dom';

// Path
import LoginPage from './page/LoginPage';
import SettingsPage from './page/SettingsPage';
import StoragePage from './page/StoragePage';
import AccountsPage from './page/AccountsPage';
import AccountAdderPage from './page/AccountAdderPage';
import AccountModifyPage from './page/AccountModifyPage';

const App = () => {
    
    return (
        <div>
            <Switch>
                <Route exact path='/' component={LoginPage} />
                <Route exact path='/settings' component={SettingsPage} />
                <Route path="/storage/" component={StoragePage} />
                <Route exact path="/accounts" component={AccountsPage} />
                <Route exact path="/accounts/account-adder" component={AccountAdderPage} />
                <Route exact path="/accounts/modify/:staticId" component={AccountModifyPage} />
            </Switch>
        </div>
    );
}
export default App;