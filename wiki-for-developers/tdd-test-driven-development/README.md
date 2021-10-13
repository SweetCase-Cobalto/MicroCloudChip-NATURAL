---
description: 얘는 기능 하나 하나를 구현하려면  테스트를 거쳐야 해요
---

# Code Test

## 개요

Microcloudchip 초기 버전의 개발 실패 원인은 해당 프레임워크 지식의 부족도 있었지만 가장 큰 문제는 잦은 버그와 실수였습니다. 하지만 버그와 실수는  TDD(Test Driven Development)를 도입하면 상당수의 실수를 예방할 수 있습니다.

실제 이 프로젝트에서도 TDD를 도입하고 있으며 그 결과 초기 버전 보다 어플리케이션 안정화 속도가 더 빨라졌습니다.

## 기술 스택

TDD 도입에 사용되는 기술 스택 또는 Python Module은 다음과 같습니다.

* Python Module
  * DJango Unittest (django.test)
* CI/CD
  * CircleCI
  * Codecov

