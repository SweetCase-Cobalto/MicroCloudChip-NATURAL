import styled from 'styled-components';
import LoginForm from '../components/LoginForm';

const LoginPage = (props) => {

    return (
        <Layout>
            <center>
                <LoginLayout>
                    <LoginForm />
                </LoginLayout>
            </center>
        </Layout>
    );
}

const Layout = styled.div`
    height: 70vh;
`
const LoginLayout = styled.div`
    margin-top: 200px;
`

export default LoginPage;