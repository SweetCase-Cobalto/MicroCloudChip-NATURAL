""" search.py
검색 및 분석 관련 메소드(툴)
"""


class StorageNameSearchNode:
    """파일/디렉토리 문자열 매칭 돌릴 때
    사용하는 오토마타 노드
    """

    def __init__(self):
        self.next_dict = {}

    def connect_node(self, condition: str, next_node):
        self.next_dict[condition] = next_node

    def goto_next(self, condition: str):
        # 다음 노드로 이동
        if condition in self.next_dict:
            return self.next_dict[condition]
        elif "*" in self.next_dict:
            return self.next_dict["*"]
        else:
            # 해당돠는 문자가 없으면 문자열에 맞지 않으므로
            return None

    def has_all_match_value(self):
        # * 존재 여부
        return True if "*" in self.next_dict else False

    def is_matched(self, char):
        return True if char in self.next_dict else False


class StorageNameSearcher:
    """
        스토리지 이름 매칭 클래스
        전부 소문자로 초기화 한 다음 돌린다.
    """
    node_head: StorageNameSearchNode

    def __init__(self, regex: str):
        self.node_head = StorageNameSearchNode()

        cur = self.node_head
        for char in regex:
            if char == "*":
                # 모든 문자 허용
                if "*" not in cur.next_dict:
                    cur.connect_node("*", cur)
            else:
                # 일반 문자
                next_node = StorageNameSearchNode()
                cur.connect_node(char.lower(), next_node)
                cur = next_node

    def __call__(self, target_str: str) -> bool:
        # 문자열 탐색

        # 문자열이 비어있으면 False
        if not target_str:
            return False

        node_stack = []

        # 소문자 처리
        target_str = target_str.lower()

        cur: StorageNameSearchNode = self.node_head
        for i in range(len(target_str)):
            if cur.has_all_match_value():
                if cur.is_matched(target_str[i]):
                    # *가 존재하고 동시에 알파벳도 매칭이 되는 경우
                    # 현재 위치를 stack에 집어넣고 다음 노드로 이동한다
                    next_cur = cur.goto_next(target_str[i])
                    node_stack.append(cur)
                    cur = next_cur
                else:
                    cur = cur.goto_next(target_str[i])
            else:
                # * 가 없는 경우
                if cur.is_matched(target_str[i]):
                    cur = cur.goto_next(target_str[i])
                else:
                    # 매칭이 안되는 경우
                    # 스택에서 노드를 꺼내는데 없으면 아예 매칭이 안된 상태이므로 False
                    if not node_stack:
                        return False
                    else:
                        cur = node_stack.pop()

        # 노드가 맨 끝까지 가야 True, 아니면 False
        connecters = list(cur.next_dict.keys())
        if not connecters or (len(connecters) == 1 and connecters[0] == "*"):
            return True
        else:
            return False
