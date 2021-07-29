import {Route} from 'react-router-dom';

// Path
import LoginPage from './page/LoginPage';
import SettingsPage from './page/SettingsPage';

const App = () => {
    
    return (
        <div>
            <Route exact path='/' component={LoginPage} />
            <Route exact path='/settings' component={SettingsPage} />
        </div>
    );
}
export default App;