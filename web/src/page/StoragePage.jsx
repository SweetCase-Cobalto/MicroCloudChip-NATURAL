import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import {Helmet} from 'react-helmet'
import styled from 'styled-components';

import MyAccountStatusComponent from '../components/accountComponent/MyAccountStatusComponent';
import FileStatusComponent from '../components/storageComponent/FileStatusComponent';
import FileListComponent from '../components/storageComponent/FileListComponent';

import 'bootstrap/dist/css/bootstrap.min.css';

const StoragePage = (props) => {

    return (
        <div>
            <Helmet>
                <title>Storage</title>
            </Helmet>
            <Navbar />
            <Layout>
                <MyAccountStatusComponent history={props.history} />
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