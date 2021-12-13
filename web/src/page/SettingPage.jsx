import React from 'react';
import ClientSettingPage from "./ClientSettingPage";
import AdminSettingPage from "./AdminSettingPage";

import { useState } from 'react';
import { connect } from 'react-redux';
import { resetTokenReducer } from '../reducers/TokenReducer';
import { getUserInformation } from '../connection/user';
import { ViewErrorCodes } from '../variables/errors';

import URL from '../asset/config.json';

const SettingPage = (props) => {

    const [userInfo, setUserInfo] = useState(null);

    const checkIsLogined = async () => {
        //로그인이 되어있는 지 확인

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
            alert(data.err);
            props.resetTokenReducer();
        }
    }

    if(userInfo == null) {
        checkIsLogined();
        return (
            <div><h1>Loading</h1></div>
        )
    }
    else {
        return (<div>
            {userInfo.isAdmin && <AdminSettingPage userInfo={userInfo} />}
            {(!userInfo.isAdmin) && <ClientSettingPage userInfo={userInfo} />}
        </div>)
    }
}
const mapStateToProps = (state) => (
    {loginStatus: state.TokenReducer }
)
export default connect(mapStateToProps, {resetTokenReducer})(SettingPage);