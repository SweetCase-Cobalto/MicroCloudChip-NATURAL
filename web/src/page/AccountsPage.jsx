import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { Helmet } from 'react-helmet';
import styled from 'styled-components';

import MyAccountStatusComponent from '../components/accountComponent/MyAccountStatusComponent';
import AccountListComponent from '../components/accountComponent/AccountListComponent';
import AccountStatusComponent from '../components/accountComponent/AccountStatusComponent';
import 'bootstrap/dist/css/bootstrap.min.css';

const AccountsPage = () => {
    return(
        <div>
            <Helmet>
                <title>Accounts</title>
            </Helmet>
            <Navbar />
            <Layout>
                <MyAccountStatusComponent />
                <AccountListComponent />
                <AccountStatusComponent />
            </Layout>
            <Footer />
        </div>
    );
}
export default AccountsPage;
const Layout = styled.div`
    display: flex;
    margin-top: 150px;
`