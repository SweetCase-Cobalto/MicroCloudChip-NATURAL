import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { Helmet } from 'react-helmet';
import styled from 'styled-components';
import { connect } from "react-redux";
import { useState } from 'react';

import MyAccountStatusComponent from '../components/accountComponent/MyAccountStatusComponent';
import AccountListComponent from '../components/accountComponent/AccountListComponent';
import AccountStatusComponent from '../components/accountComponent/AccountStatusComponent';

import { syncUserInfo } from '../reducers/ConnectedUserReducer';

import 'bootstrap/dist/css/bootstrap.min.css';

const AccountsPage = (props) => {

    const [isConnected, setIsConnected] = useState(false);

    if(!isConnected) {
        props.syncUserInfo(props.id, props.token);
        setIsConnected(true);
        return <div>
            Loading
        </div>
    }
    if(isConnected && props.id == "") {
        alert("세션이 만료되었습니다.");
        window.location.href = "/";
    }

    if(isConnected && props.id != "" && !props.isAdmin) {
        return (<div>
            <h4>접근 권한이 없습니다.</h4>
        </div>)
    }

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
const mapStateToProps = (state) => {
    return state.ConnectedUserReducer;
}
export default connect(mapStateToProps, {syncUserInfo})(AccountsPage);
const Layout = styled.div`
    display: flex;
    margin-top: 150px;
`