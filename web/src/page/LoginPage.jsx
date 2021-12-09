import styled from 'styled-components';
import { Colors } from '../variables/color';

import LoginForm from '../components/LoginForm';

const LoginPage = (props) => {

    return (
        <div>
            <center>
                <Layout>
                    <LoginForm />
                </Layout>
            </center>
        </div>
    );
}

const Layout = styled.div`
    width: 500px;
`

export default LoginPage;