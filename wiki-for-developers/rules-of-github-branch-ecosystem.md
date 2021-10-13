---
description: Github Branch 사용 규칙
---

# Rules Of Git Branch Ecosystem

![](<../.gitbook/assets/git-ecosystem (2).png>)

## Branch 종류

Microcloudchip-NATURAL에셔의 Branch는 크게 3 종류로 나뉩니다.

### master

Minor 이상 버전 단위의 branch로 기능을 추가하는데 사용됩니다. 목표치 의 기능이 완료되면 해당 버전에 맞는 `0.?.x` Branch를 생성합니다.

### 0.?.x

v0.?의 patch 버전 단위의 branch로 어플리케이션 내 버그 잡는 데 사용하는 Branch입니다. 해당 patch 버전의 목표치에 맞는 버그를 수정했으면 `0.?.?-product` branch를 수정하고 패치 내용을 차기 마이너 버전에 적용하기 위해 master가 해당 branch를 merge합니다.

### 0.?.?-product

**0.?.?-product**: `0.?.x` branch에서 목표치의 구현이 완성되었을 경우, deploy 및 Install Test를 하기 위해 `0.?.x` 로부터 분리된 Branch 입니다. Install Test가 완료되었으면 `0.?.?` 버전을 Release 합니다. 

