import ClientSettingPage from "./ClientSettingPage";
import AdminSettingPage from "./AdminSettingPage";
import React from 'react';

const SettingPage = (props) => {

    // 어드민인지 확인
    const isAdmin = true;

    return (<div>
        {isAdmin && <AdminSettingPage />}
        {(!isAdmin) && <ClientSettingPage />}
    </div>)
}

export default SettingPage;