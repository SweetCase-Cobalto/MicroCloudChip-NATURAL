import {Route} from 'react-router-dom';

// Path
import LoginPage from './page/LoginPage';

const App = () => {
    
    return (
        <div>
            <Route exact path='/' component={LoginPage} />
        </div>
    );
}
export default App;