import React from 'react';
import ClientSettingPage from "./ClientSettingPage";
import AdminSettingPage from "./AdminSettingPage";

import { useState } from 'react';
import { connect } from 'react-redux';
import { resetUserInfoReducer, updateUserInfoReducer } from '../reducers/UserInfoReducer';

import { getUserInformation } from '../connection/user';
import { ViewErrorCodes } from '../variables/errors';

import URL from '../asset/config.json';

const SettingPage = (props) => {

    const [oldToken, _] = useState(props.loginStatus.token); // 서버 연결 확인(토큰 갱신)

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
            // token update
            props.updateUserInfoReducer(
                data.data.staticId, data.data.newToken, data.data.email,
                data.data.isAdmin, data.data.userName, data.data.volumeType,
                data.data.maximumVolume, data.data.usedVolume
            )
        } else {
            // Failed
            alert(data.msg);
            props.resetUserInfoReducer();
            window.location.href = "/";
        }

    }

    if(oldToken == props.loginStatus.token) {
        checkIsLogined();
        return (
            <div><h1>Loading</h1></div>
        )
    }
    else {
        return (<div>
            {props.loginStatus.isAdmin && <AdminSettingPage />}
            {(!props.loginStatus.isAdmin) && <ClientSettingPage />}
        </div>)
    }
}
const mapStateToProps = (state) => (
    {loginStatus: state.UserInfoReducer }
)
export default connect(mapStateToProps, {updateUserInfoReducer, resetUserInfoReducer})(SettingPage);