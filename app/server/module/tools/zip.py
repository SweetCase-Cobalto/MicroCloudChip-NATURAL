import zipfile

import zipfile
import os
import stat


def zip_multiple(__src_list: list[str], __dst: str) -> bool:
    """디렉토리 저장
        __src_list: 압축 대상 파일들
        __dst: 추출 파일 루트
    """

    ziped_file: zipfile.ZipFile = zipfile.ZipFile(__dst, 'w', zipfile.ZIP_DEFLATED)

    for src_object in __src_list:

        try:
            # 파일 및 디렉토리가 존재하는 지 확인
            src_stat: os.stat_result = os.stat(src_object)
        except FileNotFoundError:
            # 파일을 못찾는 경우, 에러를 호출하지 않고 그냥 넘김
            continue
        else:
            if stat.S_ISREG(src_stat.st_mode):
                # 파일인 경우
                save_root: str = os.path.join(__dst, src_object.split(os.sep)[-1])
                ziped_file.write(src_object, save_root)
            elif stat.S_ISDIR(src_stat.st_mode):
                # 디렉토리인 경우
                # src_object가 root가 된다.
                src_only_name = src_object.split(os.sep)[-1]
                for root, dirs, files in os.walk(src_object):
                    # 파일 저장
                    for f_root in files:
                        target_root: str = os.path.join(root, f_root)
                        save_root: str = \
                            os.path.join(
                                __dst,
                                src_only_name,
                                os.path.join(root, f_root)[len(src_object):]
                            )
                        ziped_file.write(target_root, save_root)

    ziped_file.close()
    return True
