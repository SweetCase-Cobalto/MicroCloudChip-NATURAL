import { connect } from "react-redux";
import styled from "styled-components";
import { Button } from "react-bootstrap";

import { updateUserList } from "../../reducers/UserListReducer";
import AccountItemInList from "./AccountItemInList";
import { Link } from "react-router-dom";

const AccountListComponent = (props) => {
    /*
        계정 리스트
    */

    if(props.userList === undefined) {
        /*
            처음 접속을 할 경우 유저 데이터를 갖고와야 하므로
            updateUserList 함수를 사용해 서버로부터 데이터를 갖고 온다.
        */
        props.updateUserList();
        return (
            // TODO: 로딩 페이지 구현 필요
            <Layout>
                <h1>Loading</h1>
            </Layout>
        )
    } else {
        
        const UserItems = props.userList.map((user) => {
            /*
                서버로부터 받은 계정 데이터를 이용해
                계정 컴포넌트 리스트 생성

                이 때 들어가는 데이터
                username: 계정 닉네임
                staticId: 게정 아이디: 닉네임이 변경되도 다른 데이터가 변경되지 말아야 한다
                imgLink: 계정 이미지 링크
            */
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
                    <Link to="/accounts/account-adder">
                        <Button variant="success" style={{ width: "200px", marginBottom: "20px"}}>생성</Button>
                    </Link>
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