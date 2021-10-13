---
description: 어플리케이션의 테스트 코드가 돌아가는 방식을 설명해요
---

# Test Process

## 개요

해당 프로젝트가 어떻게 테스트를 진행하는지 설명합니다. 테스트 진행 방식은 크게 두 가지로 나뉘어서 설명할 수 있는 데 Layer 별로 단계적으로 테스트를 진행하는 **Layer Test**와 테스트 코드를 최대한 모듈화 해서 효율적인 테스트를 진행하는 **Modular Test**로 설명할 수 있습니다.

테스트 코드는 해당 [링크](https://github.com/SweetCase-Cobalto/microcloudchip-natural/tree/master/app/server/app/tests)에서 보실 수 있습니다.

## Layer Test

### 설명

앞서 [**System Information & Structure**](https://app.gitbook.com/@seokbong60/s/microcloudchip-natural/\~/drafts/-Ml9\_veCn3PxriKdolUm/v/v0.0.x/wiki-for-developers/system-information-and-structure)** 에서 **서술했듯이**, 시스템은 크게 **3가지 Layer(Data/Data Builder, Manager, API)로 작동합니다. 각 Layer 마다 맡은 역할이 다르기 때문에 Layer 단계별로 테스트를 진행합니다.

### Data/Data Builder Layer

Layer중에 가장 low한 단계에 존재하는 Layer 입니다. 데이터를 수동으로 조작하거나 생성/삭제합니다. 그렇기 때문에 데이터의 CRUD Test 및 Data Validation, 즉 데이터가 일련의 작업 후에 올바른 형태로 있는지 직접 검사하는 테스트를 거칩니다. 데이터 조작을 직접 해야 하기 때문에 Manager Layer에서 1\~2라인에 해결할 코드를 몇 십 라인을 작성해야 하는 상황이 옵니다. 그렇기 때문에 작업 Routine Method를 따로 작성해서 활용합니다.

어플리케이션이 패치를 거듭할 수록 다뤄야 할 데이터 유형들은 점점 많아지기 때문에 test code를 최대한 나눠서 작성합니다.

### Manager Layer

중간 단계에 위치해 있는 Layer로 API Layer로부터 받은 request를 토대로 Data/Data Builder Layer를 조작해 데이터를 관리하는 중요한 위치에 있습니다.  Data/ Data Builder Layer의 테스트 검증 내용은 비슷하나 Manager Layer는 Data/Data Builder Layer Test에서 작성한 작업 루틴 Process를 Manager의 멤버 함수에 배치해서 작업을 하기 때문에 Manager 자체가 올바르게 기능을 작동하고 있는지 검토를 한다는 점에서 차이가 있습니다.

즉, Data/Data Builder Layer처럼 데이터 조작을 직접 구현할 필요가 없기 때문에 Routine Method 또한 직접 만들 필요가 없습니다.

### API Layer

최상위 단계에 있는 Layer입니다. 이미 데이터 작업 및 관리 검증은 하위 2개의 계층에서 해결했기 때문에 API를 요청했을 때 올바른 ErrorCode가 전송되는 지 테스트만 합니다. 가끔씩 작업이 끝날 때마다 데이터 확인을 하는 데, 확인하는 방법 마저 직접 확인하는 것이 아닌 API Method를 사용합니다

## Modular Test

다량의 테스트 케이스가 요구 될 경우 모든 케이스들을 Python Code안에 다 집어넣으면 코드 길이가 상당이 길어지고 보기가 불편할 수 있습니다. 이를 방지하기 위해서 해당 프로젝트는 Test Case를 JSON파일에 저장하고 테스트 실행 시 JSON 파일의 Test Case를 불러와서 진행하는 방식으로 테스트를 운용합니다.

그러나 JSON파일을 직접 읽는 루틴 Ctrl+C, Ctrl+V를할 순 없기에 해당 프로젝트는 Test Solution Class를 직접 구현해서 테스트를 운용합니다. 자세한 내용은 아래 페이지에서 보실 수 있습니다.

{% content-ref url="testflow-module.md" %}
[testflow-module.md](testflow-module.md)
{% endcontent-ref %}

