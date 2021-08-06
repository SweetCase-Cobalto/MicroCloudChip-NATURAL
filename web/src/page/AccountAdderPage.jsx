import styled from "styled-components";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import AccountUpdaterForm from "../components/formComponents/AccountUpdaterForm";
import { Helmet } from "react-helmet";

import '../asset/font/font.css'

const AccountAdderPage = () => {
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
export default AccountAdderPage;

const Layer = styled.div`
    margin: 100px 350px 0px 350px;
    border: 1px solid #128D12;
    padding: 20px;
    font-family: 'Gothic A1';
    font-size: 1.1em;
`