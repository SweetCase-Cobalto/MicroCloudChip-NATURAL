import { connect } from "react-redux";
import styled from "styled-components";
import { Button } from "react-bootstrap";

import { updateUserList } from "../../reducers/UserListReducer";
import AccountItemInList from "./AccountItemInList";

const AccountListComponent = (props) => {


    if(props.userList === undefined) {
        props.updateUserList();
        return (
            <Layout>
                <h1>Loading</h1>
            </Layout>
        )
    } else {
        
        const UserItems = props.userList.map((user) => {
            return <AccountItemInList 
                        key={user['user_static_id']}
                        username={user.username}
                        staticId={user['user_static_id']}
                        imgLink={user.userImgLink}
                    />
        })

        return (
            <Layout>
                <div>
                    <Button variant="success" style={{ width: "200px", marginBottom: "20px"}}>생성</Button>
                    <div style={{ width: "100%", height: "1px", backgroundColor: "gray", marginBottom: "20px" }} />
                    <UsersLayer>
                        {UserItems}
                    </UsersLayer>
                </div>
            </Layout>
        );
    }
};
const mapStateToProps = (state) => {
    return state.UserListReducer;
};
export default connect(mapStateToProps, {updateUserList})(AccountListComponent);
const Layout = styled.div`
    line-height: 0.4em;

    font-family: "Gothic A1";
    width: 65%;

    border: 1.2px solid #1DB21D;
    box-shadow: 2px 2px 3px gray;

    padding: 30px;
`;
const UsersLayer = styled.div`
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    row-gap: 70px;
`