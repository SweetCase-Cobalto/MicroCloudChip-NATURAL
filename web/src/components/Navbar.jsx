import styled from "styled-components"

import NavIcon from "../asset/img/nav-icon.svg"

import 'bootstrap/dist/css/bootstrap.min.css';

const Navbar = () => {
    return (
        <Layout>
            <img src={NavIcon} width="30px" height="30px" style={{ margin: "10px" }} alt="navbar icon" />
            <TextItemLayer>Storage</TextItemLayer>
            <TextItemLayer>Shared</TextItemLayer>
            <TextItemLayer>Accounts</TextItemLayer>
            <TextItemLayer>Settings</TextItemLayer>
            <TextItemLayer style={{ float: "right" }}>Logout</TextItemLayer>
        </Layout>
    );
}
export default Navbar;
const Layout = styled.div`
    background-color: #137813;
    color: white;
    width: 100%;
    height: 50px;
    display: flex;
`
const TextItemLayer = styled.div`
    margin-left: 40px;
    margin: 10px 0px 10px 40px;
    font-size: 1.3em;
    font-family: "Gothic A1";
    font-weight: medium;
`