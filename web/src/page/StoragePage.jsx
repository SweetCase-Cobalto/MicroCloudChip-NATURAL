import React from 'react';
import URL from '../asset/config.json';

import MicrocloudchipNavbar from "../components/Navbar";
import LeftMenuBar from "../components/LeftMenuBar";
import StorageLayout from "../components/storage/StorageLayout";
import {connect} from 'react-redux';

import { resetTokenReducer } from '../reducers/TokenReducer';
import { ResponsiveQuery } from '../variables/responsive';
import { useMediaQuery } from 'react-responsive';
import { getUserInformation } from '../connection/user';

import { useState } from 'react';
import { ViewErrorCodes } from '../variables/errors';



const StoragePage = (props) => {

    const [userInfo, setUserInfo] = useState(null);
    const isPC = useMediaQuery(ResponsiveQuery.PC);

    const checkIsLogined = async () => {
        // 로그인이 되어있는 지 확인

        // check token
        if(props.loginStatus.token == null) {
            // 로그인 자체를 하지 않은 경우
            window.location.href = "/";
            return;
        }

        // 유저 데이터를 갖고옴으로써 토큰이 유효한지 확인
        let data = await getUserInformation(URL.URL, props.loginStatus.token, props.loginStatus.id);
        if(data.err == ViewErrorCodes.SUCCESS) {
            setUserInfo(data.data);
        } else {
            // Failed
            alert(data.msg);
            props.resetTokenReducer();
        }

    }

    if(userInfo == null)
        checkIsLogined();
    
    if(userInfo == null) {
        return <div>
            <h1>Loading</h1>
        </div>
    } else {
        return (
            <div>
                <MicrocloudchipNavbar userInfo={userInfo} />
                <div style={{ display: "flex" }}>
                    {isPC && <LeftMenuBar />}
                    <StorageLayout />
                </div>
            </div>
        );
    }
}

const mapStateToProps = (state) => (
    {loginStatus: state.TokenReducer }
)
// export default StoragePage;
export default connect(mapStateToProps, { resetTokenReducer })(StoragePage);