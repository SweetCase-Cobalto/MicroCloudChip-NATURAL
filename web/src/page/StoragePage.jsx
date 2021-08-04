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

    // File List Example
    const testFileListCase = [
        {
            "filename": "file1.txt",
            "modify-date": "2021-01-01 4:13am",
            "isDir": false,
            "file-type": "text",
            "size-str": "1KB"
        },
        {
            "filename": "mymusic.mp3",
            "modify-date": "2021-01-01 4:13am",
            "file-type": "audio",
            "size-str": "3MB",
            "isDir": false,
        },
        {
            "filename": "mydir",
            "modify-date": "2021-01-01 4:13am",
            "file-type": "none",
            "size-str": "11",
            "isDir": true,
        }
    ]
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
                    fileListData={testFileListCase}
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