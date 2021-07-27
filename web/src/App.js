import {Route} from 'react-router-dom';

// Path
import LoginPage from './page/LoginPage';
import FirstSettingSetAdminPage from './page/firstSetting/FirstSettingSetAdminPage';
import FirstSettingSetDatabasePage from './page/firstSetting/FirstSettingSetDatabasePage';

const App = () => {
    
    return (
        <div>
            <Route exact path='/' component={LoginPage} />

            <Route exact path="/firstsetting/setadmin" component={FirstSettingSetAdminPage} />
            <Route exact path="/firstsetting/setdatabase" component={FirstSettingSetDatabasePage} />
        </div>
    );
}
export default App;