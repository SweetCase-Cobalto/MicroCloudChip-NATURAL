import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import {Helmet} from 'react-helmet'
import styled from 'styled-components';

import AccountStatus from '../components/accountComponent/AccountStatus';
import FileStatusComponent from '../components/storageComponent/FileStatusComponent';
import FileListComponent from '../components/storageComponent/FileListComponent';

import usrIcon from '../asset/img/icons/user-icon.svg';

import 'bootstrap/dist/css/bootstrap.min.css';

const StoragePage = (props, {history}) => {

    return (
        <div>
            <Helmet>
                <title>Storage</title>
            </Helmet>
            <Navbar />
            <Layout>
                <AccountStatus />
                <FileListComponent />
                <FileStatusComponent />
            </Layout>
            <Footer />
        </div>
    );
}
const Layout = styled.div`
    display: flex;
    margin-top: 150px;
`
export default StoragePage;