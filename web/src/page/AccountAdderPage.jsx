import styled from "styled-components";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import AccountUpdaterForm from "../components/formComponents/AccountUpdaterForm";
import { Helmet } from "react-helmet";

import '../asset/font/font.css'
import { connect } from "react-redux";
import { useState } from "react";
import { syncUserInfo } from "../reducers/ConnectedUserReducer";

const AccountAdderPage = (props) => {

    const [isConnected, setIsConnected] = useState(false);
    // 유저 서버 연결 시도
    if(!isConnected) {
        props.syncUserInfo(props.id, props.token);
        setIsConnected(true);
        return (<div>
            Loading
        </div>)
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


    return (
        <div>
            <Helmet>
                <title>Add New Account</title>
            </Helmet>
            <Navbar />
            <Layer>
            <h3 style={{ fontWeight: "bold" }}>계정 추가</h3>
                <AccountUpdaterForm actionType="add" target="other" />
            </Layer>
            <Footer />
        </div>
    );
}
const mapStateToProps = (state) => {
    return state.ConnectedUserReducer;
}
export default connect(mapStateToProps, {syncUserInfo})(AccountAdderPage);
const Layer = styled.div`
    margin: 100px 350px 0px 350px;
    border: 1px solid #128D12;
    padding: 20px;
    font-family: 'Gothic A1';
    font-size: 1.1em;
`