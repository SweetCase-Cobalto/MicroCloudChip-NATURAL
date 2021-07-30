import styled from "styled-components";
import Navbar from "../components/Navbar";
import {Image, Form, Button} from "react-bootstrap";
import Footer from "../components/Footer";
import AccountUpdaterForm from "../components/formComponents/AccountUpdaterForm";

import '../asset/font/font.css'

const SettingsPage = () => {

    return (
        <div>
            <Navbar />
            <Layer>
                <h3 style={{ fontWeight: "bold" }}>관리자 계정</h3>
                <AccountUpdaterForm target="admin" />
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