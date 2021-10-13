---
description: URL 관련 파일
---

# Production / Debug Mode

## 개요

Microcloudchip은 서버가 따로 존재하는 것이 아니라, 직접 사용자가 서버를 구축해서 어플리케이션을 운영해야 합니다. 그렇기 때문에 Web Server(Nginx, Apache...)을 지원하지 않고 브라우저에서도 지원을 해야 하기 때문에 정적 파일과 백엔드 프레임워크가 같은 서버 또는 컨테이너 내에 존재해야 합니다(Full Stack Application)

그런데 해당 프로젝트는 Frontend를 JQuery가 아닌 ReactJS를 사용합니다. ReactJS 특성상 개발을 할 때는 프론트 엔드 따로 Node를 실행해서 디버깅을 해야 하기 때문에 디버깅 할 때의  코드의 일부분이 달라야 합니다. 이 페이지에서느 개발 할 때의 코드와 배포 할 때의 코드의 차이점 또는 일반 프로젝트와 의 차이점을 다룹니다.

