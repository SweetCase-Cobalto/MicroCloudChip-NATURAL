import MicrocloudchipNavbar from "../components/Navbar";
import LeftMenuBar from "../components/LeftMenuBar";

import { ResponsiveQuery } from '../variables/responsive';
import { useMediaQuery } from 'react-responsive';
import AccountSettingLayout from "../components/AccountSetting/AccountSettingLayout";

const AccountPage = () => {

    const isPC = useMediaQuery(ResponsiveQuery.PC);

    return (
        <div>
            <MicrocloudchipNavbar />
            <div style={{ display: "flex" }}>
                {isPC && <LeftMenuBar />}
                <AccountSettingLayout />
            </div>
        </div>
    )
}
export default AccountPage;