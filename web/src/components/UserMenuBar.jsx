import React from 'react';
import styled from 'styled-components';
import { Image } from 'react-bootstrap';
import { Colors } from '../variables/color';
import DefaultUserImage from '../asset/img/user-icon.svg';
import { convertRawVolumeToString } from '../variables/volume';

import { Link } from 'react-router-dom';

// redux
import { connect } from 'react-redux';
import { resetTokenReducer } from '../reducers/TokenReducer';

const UserMenuBar = (props) => {

    const logoutEvent = () => {
        props.resetTokenReducer();
        window.location.href = "/";
    }
    
    let volumeUsageGage = (props.userInfo.usedVolume / props.userInfo.maximumVolume) * 100;

    return (
        <Layout>
            <center><h5>Signed as <strong>{props.userInfo.userName}</strong></h5></center>
            <center><h6>{props.userInfo.isAdmin ? "admin" : "client"}</h6></center>
            <center><Image src={DefaultUserImage} width="100px" style={{ marginTop: "20px" }} roundedCircle /></center>
            <center><div style={{ marginTop: "20px", marginBottom: "20px", width: "80%", height: "1px", backgroundColor: "gray" }} /></center>

            <center>
                <table style={{ width: "80%" }}>
                    <tbody>
                        <tr><Item><Link to="/settings" style={{ textDecorationLine: "none" }}><ItemInLink>Settings</ItemInLink></Link></Item></tr>
                        <tr><Item onClick={logoutEvent}>Logout</Item></tr>
                    </tbody>
                </table>
            </center>
            <center><div style={{ marginTop: "20px", marginBottom: "20px", width: "80%", height: "1px", backgroundColor: "gray" }} /></center>
            <UsageLayer>
                <p style={{ fontSize: "0.8em" }}>{convertRawVolumeToString(props.userInfo.usedVolume)}/{convertRawVolumeToString(props.userInfo.maximumVolume)}</p>
                <div style={{display: "flex", marginTop: "-10px"}}>
                    <UsageLine style={{width: `${volumeUsageGage}%`}} />
                    <NoneUsageLine style={{width: `${100 - volumeUsageGage}%`}} />
                </div>
            </UsageLayer>
        </Layout>
    )
}
// 리덕스 돌리기용
const mapStateToProps = (state) => (
    {loginStatus: state.TokenReducer }
)
export default connect(mapStateToProps, {resetTokenReducer})(UserMenuBar);
const Layout = styled.div`
    width: 100%;
    padding: 30px 5px 10px 5px;
`
const Item = styled.td`
    padding: 5px 10px 5px 10px;
    cursor: pointer;
    &:hover {
        color: white;
        background: ${Colors.ACCESS_COLOR}
    }
`
const ItemInLink = styled.div`
    color: black;
    &:hover {
        color: white;
        background: ${Colors.ACCESS_COLOR}
    }

`
const UsageLayer = styled.div`
    padding: 5px 10px 5px 25px;
`
const UsageLine = styled.div`
    height: 4px;
    background-color: ${Colors.ACCESS_COLOR}
`
const NoneUsageLine = styled.div`
    height: 4px;
    background-color: ${Colors.UNABLE_COLOR}
`
