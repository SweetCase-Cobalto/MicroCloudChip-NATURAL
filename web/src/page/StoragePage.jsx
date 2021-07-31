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

    // Storages (MB 단위)
    let capacityStorage = 100
    let usedStroage = 15


    // example file list
    let allRootArr = window.location.pathname.split('/').slice(2);

    return (
        <div>
            <Helmet>
                <title>Storage</title>
            </Helmet>
            <Navbar />
            <Layout>
                <AccountStatus 
                    accountName="admin"
                    accountEmail="seokbong60@gmail.com"
                    accountType="admin"

                    capacityStorage={capacityStorage}
                    usedStorage={usedStroage}

                    userImgLink={usrIcon}
                />
                <FileListComponent 
                    allRootArr={allRootArr}
                />
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