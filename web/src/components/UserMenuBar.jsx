import React from 'react';
import styled from 'styled-components';
import { Image } from 'react-bootstrap';
import { Colors } from '../variables/color';

import DefaultUserImage from '../asset/img/user-icon.svg';

const UserMenuBar = (props) => {

    return (
        <Layout>
            <center><h5>Signed as <strong>User1</strong></h5></center>
            <center><h6>client</h6></center>
            <center><Image src={DefaultUserImage} width="100px" style={{ marginTop: "20px" }} roundedCircle /></center>
            <center><div style={{ marginTop: "20px", marginBottom: "20px", width: "80%", height: "1px", backgroundColor: "gray" }} /></center>

            <center>
                <table style={{ width: "80%" }}>
                    <tbody>
                        <tr><Item>Settings</Item></tr>
                        <tr><Item>Logout</Item></tr>
                    </tbody>
                </table>
            </center>
            <center><div style={{ marginTop: "20px", marginBottom: "20px", width: "80%", height: "1px", backgroundColor: "gray" }} /></center>
            <UsageLayer>
                <p style={{ fontSize: "0.8em" }}>133KB/5GB</p>
                <div style={{display: "flex", marginTop: "-10px"}}>
                    <UsageLine style={{width: "20%"}} />
                    <NoneUsageLine style={{width: "80%"}} />
                </div>
            </UsageLayer>
        </Layout>
    )
}

const Layout = styled.div`
    width: 100%;
    padding: 30px 5px 10px 5px;
`
const Item = styled.td`
    padding: 5px 10px 5px 10px;
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

export default UserMenuBar;