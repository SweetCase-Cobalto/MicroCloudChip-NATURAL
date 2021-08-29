import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import {Helmet} from 'react-helmet'
import styled from 'styled-components';

import axios from 'axios';

import MyAccountStatusComponent from '../components/accountComponent/MyAccountStatusComponent';
import FileStatusComponent from '../components/storageComponent/FileStatusComponent';
import FileListComponent from '../components/storageComponent/FileListComponent';

import 'bootstrap/dist/css/bootstrap.min.css';

const StoragePage = () => {

    // 서버로부터 데이터 요청


    return (
        <div>
            <Helmet>
                <title>Storage</title>
            </Helmet>
            <Navbar />
            <Layout>
                <MyAccountStatusComponent />
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