import styled from "styled-components"
import { Link } from "react-router-dom";
import { connect } from "react-redux";
import { userLogout } from "../reducers/ConnectedUserReducer";

import NavIcon from "../asset/img/nav-icon.svg"

import 'bootstrap/dist/css/bootstrap.min.css';

const Navbar = (props) => {

    const logoutEvent = () => {
        props.userLogout();
        window.location.assign("/");
    }

    let displaySetting = props.isAdmin ? "block" : "none";

    return (
        <Layout>
            <img src={NavIcon} width="30px" height="30px" style={{ margin: "10px" }} alt="navbar icon" />
            <TextItemLayer><Link to="/storage/root" style={{ color: "white"}}>Storage</Link></TextItemLayer>
            <TextItemLayer><Link to="/accounts" style={{ color: "white", display: displaySetting }}>Accounts</Link></TextItemLayer>
            <TextItemLayer><Link to="/settings" style={{ color: "white", display: displaySetting }}>Settings</Link></TextItemLayer>
            <TextItemLayer style={{ float: "right", cursor: "pointer", color: "white" }} onClick={logoutEvent}>Logout</TextItemLayer>
        </Layout>
    );
}
const mapStateToProps = (state) => {
    return state.ConnectedUserReducer;
}
export default connect(mapStateToProps, {userLogout})(Navbar);

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