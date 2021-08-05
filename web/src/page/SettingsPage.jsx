import styled from "styled-components";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import AccountUpdaterForm from "../components/formComponents/AccountUpdaterForm";
import { Helmet } from "react-helmet";

import '../asset/font/font.css'

const SettingsPage = () => {

    return (
        <div>
            <Helmet>
                <title>Settings</title>
            </Helmet>
            <Navbar />
            <Layer>
                <h3 style={{ fontWeight: "bold" }}>관리자 계정</h3>
                <AccountUpdaterForm actionType="modify" />
            </Layer>
            <Footer />
        </div>
    );
}

const Layer = styled.div`
    margin: 100px 350px 0px 350px;
    border: 1px solid #128D12;
    padding: 20px;
    font-family: 'Gothic A1';
    font-size: 1.1em;
`

export default SettingsPage;