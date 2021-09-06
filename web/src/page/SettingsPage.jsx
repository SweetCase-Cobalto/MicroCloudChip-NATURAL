import styled from "styled-components";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import AccountUpdaterForm from "../components/formComponents/AccountUpdaterForm";
import { Helmet } from "react-helmet";

import '../asset/font/font.css'
import { connect } from "react-redux";

const SettingsPage = (props) => {
    // 계정에 따라 다름

    if(props.isAdmin) {
        // 관리자 전용
        return (
            <div>
                <Helmet>
                    <title>Settings</title>
                </Helmet>
                <Navbar />
                <Layer>
                    <h3 style={{ fontWeight: "bold" }}>관리자 계정</h3>
                    <AccountUpdaterForm actionType="modify" target="my" />
                </Layer>
                <Footer />
            </div>
        );
    } else {
        // 일반 계정 커스템
        return (
            <div>
                <Helmet>
                    <title>Settings</title>
                </Helmet>
                <Navbar />
                <Layer>
                    <h3 style={{ fontWeight: "bold" }}>내 계정</h3>
                    <AccountUpdaterForm actionType="modify" target="my" />
                </Layer>
                <Footer />
            </div>
        )
    }
}

const Layer = styled.div`
    margin: 100px 350px 0px 350px;
    border: 1px solid #128D12;
    padding: 20px;
    font-family: 'Gothic A1';
    font-size: 1.1em;
`
const mapStateToProps = (state) => {
    return state.ConnectedUserReducer;
}
export default connect(mapStateToProps)(SettingsPage);