# 마지막 불빛

크리스마스 밤, 조난당한 겨울 산에서 민가의 불빛을 향해 스키로 내려가는 브라우저 러너 게임입니다. 중간고사 바이브 코딩 과제로 제작합니다.

> 현재 기획 단계이며, 아직 실행할 수 있는 빌드는 없습니다.

## 1. 제작한 것 소개

비행기 사고로 고도가 높은 산에 조난당한 주인공이 잔해로 스키를 만들어 마을까지 내려갑니다. 어두운 숲길에서 나무와 돌을 피하고 코인을 모으며 달리고, 약 1분 10초 뒤 민가에 도착하면 끝납니다.

- 실행 방법: [GitHub Pages에서 플레이](https://aa8543aa.github.io/last-light/) 또는 `index.html`을 브라우저로 열기 (인터넷 연결 필요)
- 조작법: `A`/`D` 또는 `←`/`→`로 좌우 이동, `Space` 점프, 마우스를 움직여 주변 보기 (커서를 위로 올리면 하늘)
- 에셋 출처: 하늘은 [Milky Way at Chajnantor](https://commons.wikimedia.org/wiki/File:Milky_Way_at_Chajnantor_(uhd_9428_panorama_eq).jpg) (Y. Beletsky (LCO)/ESO, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0)), 산은 [Kanchenjungha-Panorama](https://commons.wikimedia.org/wiki/File:Kanchenjungha-Panorama.jpg) (Sujay25, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0))를 사용함. 하늘은 위쪽만 잘라 별을 지웠고, 산은 하늘을 지우고 밤 색으로 보정함. 눈 지면은 [Poly Haven Snow 02](https://polyhaven.com/a/snow_02) (Rob Tuytel, CC0). 나무는 [Poly Haven Fir Tree 01](https://polyhaven.com/a/fir_tree_01), [Fir Sapling Medium](https://polyhaven.com/a/fir_sapling_medium) (Rob Tuytel, Rico Cilliers, CC0)에 눈과 달빛을 입혀 이미지로 제작함. 바위는 코드로 생성함

## 2. PRD

### 목표

- 브라우저에서 설치 없이 실행되는 약 1분 10초 분량의 러너 게임을 만든다.
- 눈 덮인 밤 숲을 실시간 렌더링으로 최대한 사실적으로 표현한다.
- 일반 노트북에서도 플레이할 수 있는 성능을 유지한다.

### 게임 흐름

| 단계 | 내용 |
| --- | --- |
| 1. 사고 | 기내에서 폭발이 일어나 추락하고, 눈에 파묻혔다가 빠져나온다. |
| 2. 발견 | 주변을 둘러보다 먼 곳에서 흐릿한 민가 불빛을 발견한다. |
| 3. 제작 | 판자, 비행기 잔해, 나뭇가지를 주워 스키를 만드는 장면이 자동으로 재생된다. |
| 4. 활강 | 불빛을 향해 자동으로 내려가며 장애물을 피하거나 파괴한다. |
| 5. 도착 | 민가에 도착하면 최종 점수와 함께 끝난다. |

### 핵심 기능

| 우선순위 | 기능 | 설명 |
| --- | --- | --- |
| 필수 | 이동 | 전진은 자동이고 플레이어는 좌우 이동과 점프를 할 수 있다. 점프는 스테미나를 쓴다. |
| 필수 | 인트로 | 스키 착용까지 입력 없는 고정 애니메이션으로 진행하고, 그 뒤 조작을 시작한다. |
| 필수 | 장애물 | 나무와 돌을 무작위로 배치하되 지나갈 길을 항상 남긴다. |
| 필수 | 충돌과 체력 | 장애물에 부딪히면 체력이 줄고, 0이 되면 게임 오버 후 재시작한다. |
| 필수 | HUD | 체력, 민가까지 남은 거리, 시간, 코인, 점수, 스테미나, 조작법을 표시한다. |
| 필수 | 점수 | 코인과 생존 시간으로 점수를 얻는다. |
| 필수 | 진행도 | 3km를 달리면 민가가 나타나고, 불빛이 점점 가까워진다. |
| 필수 | 배경 | 상고대가 덮인 밤 숲, 쌓인 눈, 달빛, 안개, 내리는 눈 |
| 선택 | 연출 | 크리스마스 장식, 바람 소리와 스키 소리, 카메라 흔들림 |
| 선택 | 그래픽 옵션 | 저사양 기기를 위한 품질 단계 |

### 범위에서 제외

- 멀티플레이
- 복잡한 제작 화면과 인벤토리
- 무기와 장애물 파괴
- 나무와 돌 이외의 장애물
- 적과 싸우는 전투 (곰과 늑대는 피하기만 함)

### 기술 스택

- 렌더링: Babylon.js
- 구조: 빌드 없이 HTML 파일과 CDN 스크립트만 사용
- 에셋: 라이선스를 확인한 무료 에셋 (예: Poly Haven의 CC0 텍스처, 모델)과 코드로 생성한 나무
- 배포: GitHub Pages에 HTML을 그대로 올림

### 사실감 전략

사진의 상고대 나무는 가는 가지가 많아 그대로 재현하면 성능 부담이 큽니다. 어둠과 안개로 먼 나무의 디테일을 줄이고, 플레이어 주변에 품질을 집중합니다.

### 완료 기준

- 배포된 URL에서 사고 장면부터 민가 도착까지 플레이할 수 있다.
- 시드를 바꿔 코스를 생성해도 지나갈 길이 항상 존재한다.
- 한 판의 길이가 약 1분 10초다.
- 일반 노트북 기준 평균 30 FPS 이상을 유지한다.
- 사용한 에셋의 출처와 라이선스를 README에 기록한다.

## 3. Todo 리스트

### 현재 계획

- [x] 저장소 생성 및 PRD 작성
- [x] 새 기획으로 PRD와 Todo 수정
- [x] 배경 렌더 테스트 작성 ([concept/index.html](concept/index.html))
- [x] HUD 디자인
- [x] 렌더 테스트 개선 (민가 불빛, 상고대, 성능)
- [x] 프로젝트 전용 스킬 작성
- [x] 게임용 index.html 구성
- [x] GitHub Pages 배포
- [x] 끝없이 이어지는 코스 생성 구현
- [x] 좌우 이동과 스키 카메라 구현
- [x] 울타리를 바위와 나무 경계로 교체
- [x] 시야 밖 렌더링 제외, 바람과 눈, 스키 팔 동작
- [x] 스테미나, 부스트, 점프 구현
- [x] 지나갈 길을 보장하는 장애물과 점프, 부스트 전용 구간 구현
- [x] 곰과 늑대 출현, 점프 회피 구현
- [x] 충돌, 체력, 게임 오버, 재시작 구현
- [x] 코인, 시간 점수 구현과 HUD 연결
- [x] 플레이어 몸 구현 (팔, 다리, 스키)
- [x] 비행기, 폭발, 추락 인트로 구현
- [x] 눈 속 탈출, 민가 발견, 스키 제작 인트로 구현
- [ ] 민가 도착 엔딩 구현
- [x] 민가를 언덕 지형 위의 집과 창문 불빛으로 교체
- [x] 코스 3km, 기본 속도 43m/s, 스테미나는 점프 전용으로 변경
- [x] 급경사 위 추락 지점과 자동 활강 인트로로 변경
- [x] 사용한 스킬과 활용 방식을 README에 기록
- [x] 민가가 약 3km 밖으로 보이도록 변경
- [x] 숲을 스캔 모델로 만든 이미지 카드로 교체
- [ ] 사운드와 크리스마스 연출 추가
- [x] 1차 최적화 (전후 수치는 변경 내역 참고)
- [ ] 게임 완성 후 최종 성능 측정
- [ ] 플레이 테스트 후 난이도 조정
- [ ] README 마무리

### 변경 내역

처음 계획과 달라진 부분을 작업 중에 기록합니다. 처음 계획은 [첫 커밋](https://github.com/aa8543aa/last-light/commit/3547514)에서 볼 수 있습니다.

| 날짜 | 구분 | 처음 계획 | 변경 후 | 이유 |
| --- | --- | --- | --- | --- |
| 2026-10-30 | 수정 | Three.js 사용 | Babylon.js 사용 | 충돌, 후처리 등 게임 기능이 내장되어 있어 구현에 유리함 |
| 2026-10-30 | 수정 | 실내 아레나 1인칭 슈팅 | 겨울 산 스키 러너 | 조난 스토리와 크리스마스 배경으로 기획을 구체화함 |
| 2026-10-30 | 삭제 | 사격, 재장전, 적 AI, 웨이브 | 없음 | 러너 게임에 필요하지 않음 |
| 2026-10-30 | 추가 | 없음 | 코스 생성, 장애물, 도끼, 코인, 도입부, 엔딩 | 새 게임 방식에 필요함 |
| 2026-10-30 | 추가 | 없음 | 배경 렌더 테스트 | 사실적인 배경이 가능한지 구현 전에 확인하기 위함 |
| 2026-10-30 | 삭제 | Havok 물리 | 없음 | 좌우 이동과 단순 충돌만 있어 물리 엔진이 필요하지 않음 |
| 2026-10-30 | 수정 | Vite, TypeScript 빌드 | HTML과 CDN만 사용 | 받아서 바로 열 수 있고 GitHub Pages에 그대로 올릴 수 있어야 함 |
| 2026-10-30 | 수정 | 충돌 시 즉시 게임 오버 | 체력 감소 후 0이면 게임 오버 | HUD에 체력을 표시하기로 함 |
| 2026-10-30 | 추가 | 없음 | HUD 디자인 | 플레이 정보를 구현 전에 확정하기 위함 |
| 2026-10-30 | 수정 | 상고대를 튜브로 표현 | 작은 삼각형 결정으로 표현 | 렌더 테스트에서 약 26 FPS(135만 버텍스)가 60 FPS(156만 버텍스)로 개선됨. 먼 나무 그림자 제외, 나무 수 감소, SSAO와 안티앨리어싱 샘플 감소를 함께 적용 |
| 2026-10-30 | 수정 | 폭이 좁은 숲길(울타리 간격 5.8m) | 울타리 간격 8.4m | 이동 테스트에서 좌우로 움직일 공간이 부족할 것으로 판단함 |
| 2026-10-30 | 수정 | 검은 화면에서 눈을 뜨며 시작 | 기내에서 시작해 폭발, 추락, 눈 속 탈출 후 민가 발견 | 도입부를 더 극적으로 만들기로 함 |
| 2026-10-30 | 수정 | 재료를 직접 주움 | 스키 착용까지 입력 없는 고정 애니메이션 | 조작은 스키 착용 후에만 시작하기로 함 |
| 2026-10-30 | 추가 | 없음 | 1인칭 플레이어 몸 | 비행기와 스키 장면에서 내 몸이 보여야 함 |
| 2026-10-30 | 추가 | 없음 | 히말라야 파노라마 사진, 3D 산맥, 구름층을 겹친 추락 배경 | 외딴 오지의 느낌과 입체감을 주기 위함 |
| 2026-10-30 | 삭제 | 인트로 자막 | 없음 | 말 없이 장면으로 서사를 전달하기로 함 |
| 2026-10-30 | 수정 | 지상 근처까지 추락 | 상공에서 의식을 잃고 눈 속에서 깨어남 | 약 10km 상공에서 튕겨 나가는 전개로 바꿈 |
| 2026-10-30 | 수정 | 스키를 만들어 착용 | 판자, 금속판, 끈, 나뭇가지로 엉성하게 만든 스키와 지팡이 | 잔해로 급조한 느낌을 살리기 위함 |
| 2026-10-30 | 추가 | 없음 | 무릎 위 선물, 옆자리 승객, 잔해에서 다시 줍는 선물 | 자막 없이 약간의 서사를 전달하기 위함 |
| 2026-10-30 | 수정 | 추락하며 주변을 보여 줌 | 창밖으로 깊은 설산을 보여 주고, 폭발 직후 바로 의식을 잃음 | 오지라는 정보를 창밖에서 전달하고 전개를 간결하게 함 |
| 2026-10-30 | 수정 | 위키미디어 파노라마 사진과 3D 산맥 | 지형을 계산해 렌더링한 밤 계곡, 창밖 설산 이미지 | 플레이 테스트에서 산이 사실적이지 않았고, 참고 이미지 같은 구도와 하늘이 필요함 |
| 2026-10-30 | 수정 | 울타리로 막은 곧은 길 | 폭이 변하는 길을 바위, 나무, 덤불로 자연스럽게 제한 | 울타리가 인위적으로 보임 |
| 2026-10-30 | 수정 | 시속 약 43km(12m/s), 3.6km | 시속 약 65km(18m/s), 5.4km, 맞바람에 스치는 눈과 시야 변화 | 플레이 시간은 약 5분으로 두고 속도감을 높임 |
| 2026-10-30 | 추가 | 없음 | 달리는 동안 뒤와 옆 시야 밖 나무, 바위 제외 | 보이지 않는 부분의 렌더링 부하를 줄임 |
| 2026-10-30 | 추가 | 좌우 이동만 가능 | 스테미나, 부스트, 점프 | 조작의 재미를 높이고 전용 구간을 만들기 위함 |
| 2026-10-30 | 추가 | 나무와 돌 장애물 | 점프로 넘는 통나무, 부스트하며 점프해야 넘는 크레바스 | 스테미나 기능을 꼭 쓰게 하는 구간이 필요함 |
| 2026-10-30 | 추가 | 적과 전투 없음 | 간혹 달려드는 곰과 늑대, 타이밍 점프로 회피하면 사라짐 | 긴장감을 더하기 위함. 싸우지 않고 피하기만 함 |
| 2026-10-30 | 수정 | 코드로 렌더링한 하늘과 산 | 실제 은하수와 설산 사진으로 만든 돔과 산 띠 | 실물과 비교되는 품질을 얻기 위함. 렌더링 스크립트는 삭제함 |
| 2026-10-30 | 수정 | 입체 나무 전체 렌더링 | 먼 나무는 이미지 카드로 대체, SSAO 제거, 그림자 축소, 자동 해상도 조절 | 프레임당 정점 약 1억 1,400만 개에서 약 700만 개로 감소, 36 FPS에서 60 FPS로 개선 |
| 2026-10-30 | 추가 | 없음 | 마우스 시점 | 달리면서 하늘과 주변을 볼 수 있게 함 |
| 2026-10-30 | 수정 | 스테미나 소모 26/초, 재생 11/초, 점프 18 | 소모 13/초, 재생 26/초, 점프 10 | 플레이 테스트에서 스테미나가 부족했음 |
| 2026-10-30 | 수정 | 곰과 늑대가 뛰어올라 덮침 | 뛰지 않고 위치만 따라오며, 점프 중이면 지나감 | 플레이 테스트에서 늑대를 피할 수 없었음 |
| 2026-10-30 | 수정 | 곰과 늑대가 플레이어를 따라옴 | 길 위 한 곳에 서 있어 옆으로 피하거나 뛰어넘음 | 재테스트에서도 피할 수 없었음 |
| 2026-10-30 | 수정 | 게임 제목 불빛을 향해 | 마지막 불빛 | 제목 변경 요청 |
| 2026-10-30 | 수정 | 저장소와 주소 realistic-combat-web | last-light | 게임 내용과 맞지 않는 이름을 바꿈 |
| 2026-10-30 | 수정 | 평지에 그린 검은 크레바스 | 지형을 약 70m 깎은 낭떠러지, 빠지면 추락 장면 후 건너편에서 재개 | 빈 공간이 사실적이지 않았음 |
| 2026-10-30 | 수정 | 코드로 만든 눈 지면과 빠르게 스치는 눈 | 실제 눈 촬영 재질과 천천히 내리는 큰 눈송이 추가 | 눈이 내리는 느낌이 약하고 지면이 평평해 보임 |
| 2026-10-30 | 추가 | 상고대 활엽수만 있는 숲 | 눈 쌓인 가문비나무를 섞은 숲 | 겨울 산의 실제 숲 구성에 가깝게 함 |
| 2026-10-30 | 수정 | 18m/s, 5.4km, 틈 19m | 27m/s, 8.1km, 틈 24m, 장애물 간격 1.5배 | 플레이 테스트에서 속도가 답답함. 약 5분 길이와 부스트 필수 구간은 유지 |
| 2026-10-30 | 수정 | 사진 속 별을 그대로 사용 | 사진은 은하수의 빛과 먼지만 쓰고, 별은 셰이더로 화면 픽셀 단위 렌더링 | 사진 해상도의 한계로 별이 점처럼 보임 |
| 2026-10-30 | 삭제 | 도끼 파밍과 장애물 파괴 | 없음 | 점프와 부스트로 충분하다고 판단해 범위에서 제외 |
| 2026-10-30 | 수정 | 굵고 많은 별, 사진 속 별의 얼룩, 블룸 | 1~2픽셀의 선명한 별, 원본 사진에서 별을 지워 먼지 띠까지 선명한 은하수, 블룸 제거 | 하늘이 정신없고 저해상도처럼 보임 |
| 2026-10-30 | 수정 | 잠깐 둘러본 뒤 작은 불빛을 봄 | 흐린 시야에서 정신을 차리고 둘러보다 불빛을 발견해 시선이 확대됨 | 플레이 테스트에서 발견 연출이 보이지 않았음 |
| 2026-10-30 | 수정 | 많은 눈 입자 | 입자 수와 크기를 절반 수준으로 정리 | 화면이 정신없음 |
| 2026-10-30 | 수정 | 클릭 후 포인터 잠금 시점 | 커서 위치를 따라가는 시점 | 수정 중 시점 코드가 지워져 동작하지 않았고, 잠금은 환경에 따라 막힘 |
| 2026-10-30 | 수정 | 카메라를 따라다니는 불빛 이미지 | 언덕 지형 위의 집과 창문 불빛, 도착 지점에도 마을 배치 | 플레이 테스트에서 불빛이 허공에 떠 보임 |
| 2026-10-30 | 수정 | 27m/s, 8.1km, 약 5분, Shift 부스트 | 43m/s 상시, 3km, 약 1분 10초, 부스트 키 삭제, 스테미나는 점프에만 사용 | 플레이 테스트에서 코스가 너무 길고 속도가 답답함 |
| 2026-10-30 | 수정 | 게임 시작 위치에서 깨어남 | 약 50m 위 급경사의 턱에서 민가를 내려다보고, 자동으로 활강한 뒤 원래 위치에서 조작 시작 | 내려다보는 발견 연출이 더 자연스러움 |
| 2026-10-30 | 수정 | 약 380m 앞 언덕의 민가 | 약 3km 거리로 보이는 먼 능선 위의 민가, 첫 낭떠러지는 620m 지점으로 이동 | 플레이 테스트에서 민가가 너무 가까움. 코스 길이와 맞춤 |
| 2026-10-30 | 수정 | 코드로 만든 입체 나무와 덤불, 가문비나무 | CC0 스캔 전나무로 미리 만든 이미지 카드, 입체 나무 제거 | 정점을 줄이면서 사실감을 높이기 위함 |
| 2026-10-30 | 추가 | 스키를 묶으면 바로 조작 시작 | 미끄러지다 뒤돌아보면 늑대 무리가 쫓아오는 장면 후 조작 시작 | 도입부의 긴장감을 높이기 위함 |
| 2026-10-30 | 추가 | 없음 | 체력 30을 회복하는 키트 | 장애물과 동물로 줄어든 체력을 회복하기 위함 |
| 2026-10-30 | 수정 | 하늘과 산 이미지 3840px | 원본에서 하늘은 시점 범위 8192px, 산은 7680px로 다시 제작 | 플레이 테스트에서 해상도가 낮게 보임. 파일 크기는 커짐 |
| 2026-10-30 | 추가 | 인트로 건너뛰기 없음 | Enter로 건너뛰기 | 반복 플레이와 테스트를 위함 |
| 2026-10-30 | 수정 | 낮은 렌더 해상도, FXAA, 그레인, 강한 블룸 | 화면 배율 반영, MSAA 4배, 그레인 제거, 약한 블룸, 해상도 자동 저하 최소화 | 플레이 테스트에서 화면이 흐리게 보임 |
| 2026-10-30 | 수정 | 성능 측정과 최적화 | 게임 완성 후 최적화하고 전후 수치를 기록 | 렌더 테스트가 약 26 FPS로 목표 30 FPS에 못 미침 |

## 4. 스킬

이번 프로젝트에서 사용한 스킬은 두 가지입니다.

### run (기존 스킬)

**고른 이유:** 이 과제는 브라우저에서 실제로 실행되어야 합니다. `run`은 테스트 코드가 아니라 앱을 직접 띄우고 조작한 뒤 화면을 보고 판단하게 하는 스킬이라, 렌더링 문제가 많은 이 게임의 검증에 맞습니다.

**쓰인 방식:** 급경사 추락 지점과 자동 활강 인트로를 검증할 때 Claude Code의 Skill 도구로 호출했습니다. 스킬의 절차대로 프로젝트 전용 실행 스킬이 있는지 먼저 찾았고, 없어서 브라우저 방식을 따랐습니다. 다만 스킬의 예시 도구인 `chromium-cli` 대신 앱 내 브라우저에서 게임을 조작하고 스크린샷을 확인했습니다.

**찾아낸 문제:** 활강과 조작 시작은 정상이었지만, 높은 곳에서 민가가 보이지 않았습니다. 스크린샷을 보고 하늘 바닥판이 계곡을 가리는 것을 찾아 고쳤습니다. 코드만 읽어서는 놓쳤을 문제입니다.

**SKILL.md 내용:** (Claude Code 내장 스킬)

````markdown
**Running means launching the actual app and interacting with it** -
not the test suite, not an `import` of an internal function and a
`console.log`. The app as a user (human or programmatic) would meet
it: the CLI at its command, the server at its socket, the GUI at its
window.

## First: does a project skill already cover this?

A project skill that launches this app is the repo's verified path -
its author already cold-started from a Linux container and committed
what worked: the exact `apt-get` line, the env vars, the patches, the
driver. Use it instead of rediscovering.

```bash
d=$PWD; while :; do
  grep -Hm1 '^description:' "$d"/.claude/skills/*/SKILL.md 2>/dev/null
  [ -e "$d/.git" ] || [ "$d" = / ] && break
  d=$(dirname "$d")
done
```

- **One describes launching/driving this app** -> read that SKILL.md
  and follow it verbatim. Don't paraphrase; don't skip the patches.
- **Mega-repo, several plausible, no clear match** -> ask the user
  which unit to run.
- **Stale** (fails on mechanics unrelated to your task) -> tell the
  user; offer to refresh it via `/run-skill-generator`.
- **Nothing about running** -> fall back to the patterns below.

## Otherwise: match the shape, use the pattern

Pick the row closest to your project. Each example walks through
launch + first interaction; ignore any trailing "write the skill"
section - you're using the recipe, not authoring one.

| Project type | Handle | Example |
|---|---|---|
| CLI tool | direct invocation, exit code, stdin/stdout | [examples/cli.md](examples/cli.md) |
| Web server / API | background launch + `curl` smoke | [examples/server.md](examples/server.md) |
| TUI / interactive terminal | tmux `send-keys` / `capture-pane` | [examples/tui.md](examples/tui.md) |
| Electron / desktop GUI | Playwright `_electron` REPL under xvfb | [examples/electron.md](examples/electron.md) |
| Browser-driven | dev server + `chromium-cli` script | [examples/playwright.md](examples/playwright.md) |
| Library / SDK | import-and-call smoke script at the package boundary | [examples/library.md](examples/library.md) |

If nothing fits, start from the closest match and adapt. For a web
app, [examples/playwright.md](examples/playwright.md) - drive it with
`chromium-cli`, no custom driver needed. For a desktop app,
[examples/electron.md](examples/electron.md) - it has the `_electron`
REPL driver skeleton and the tmux wrapping.

## Drive it, don't just launch it

Launching with no interaction proves the entrypoint resolves. That's
not running the app - it's typechecking with extra steps. Drive it to
a point where a user would see something:

- CLI -> type a representative command, check the exit code and output.
- Server -> hit the route the diff touches with `curl`, read the body.
- TUI -> `send-keys` a navigation, `capture-pane` the result.
- GUI -> click the button, screenshot the window. **Look at the
  screenshot.** A blank frame is a failure to launch.

If the fallback pattern didn't work out of the box - you had to
install packages, set env vars, patch config, or write a driver -
recommend `/run-skill-generator` in your report so that work gets
captured as a project skill. If it just worked, don't.
````

### midterm-todo-cycle (직접 제작)

**만든 이유:** 작업 도중 push가 한 번도 안 된 상태로 진행된 적이 있었습니다. 과제는 Todo 작업 중 일정한 간격의 push와 변경 내역 기록을 요구하므로, 매 항목마다 따를 절차를 문서로 고정했습니다.

**쓰인 방식:** 이 스킬은 작업 중에 만들어서 해당 세션의 스킬 목록에 등록되지 않았고, 호출을 시도했을 때도 인식되지 않았습니다. 그래서 자동으로 실행한 것이 아니라, 절차 문서로 참고해 Todo 항목마다 직접 따랐습니다. 그럼에도 여러 작업을 한 커밋에 묶은 적이 있어, 사용자의 지적을 받고 이후 작업 단위로 나눴습니다.

**SKILL.md 내용:** ([원본](.claude/skills/midterm-todo-cycle/SKILL.md))

````markdown
---
name: midterm-todo-cycle
description: last-light 저장소에서 Todo 항목을 하나 진행할 때 사용한다. 과제 조건을 먼저 확인하고, 브라우저 검증, README 기록, 커밋과 push까지 한 항목 단위로 끝낸다.
---

# 중간고사 Todo 작업 주기

Todo 항목 하나를 아래 순서로 끝낸 뒤 다음 항목으로 넘어간다.

## 1. 과제 조건 확인

- 저장소는 Public이고 코드는 GitHub에 있어야 한다.
- 다 만든 뒤 한 번에 push하지 않고, Todo 작업 중 일정한 간격으로 push한다.
- 커밋 메시지에는 커밋 내용을 적는다.
- 프로젝트는 브라우저에서 실행되어야 한다.
- README에는 소개, PRD와 Todo, Todo 변경 내역, 스킬, 느낀점과 결론이 있어야 한다.

## 2. 구현

- 빌드 도구 없이 HTML 파일과 CDN 스크립트만 사용한다.
- PRD에 없는 기능을 추가하거나 계획을 바꾸면 변경 내역에 남긴다.

## 3. 검증

- 브라우저에서 실제로 열어 콘솔 오류, 화면, 조작을 확인한다.
- 성능에 영향을 주는 작업은 FPS와 버텍스 수를 전후로 잰다.
- 확인하지 못한 것은 완료로 적지 않는다.

## 4. README 기록

- 끝난 Todo 항목을 체크한다.
- 처음 계획과 달라졌다면 날짜, 구분, 처음 계획, 변경 후, 이유를 변경 내역에 적는다.

## 5. 커밋과 push

- 코드와 README 변경을 항목 단위로 함께 커밋한다.
- 메시지 첫 줄에 무엇을 했는지, 본문에 왜 또는 어떻게 했는지 적는다.
- 바로 push하고 원격에 올라갔는지 확인한다.
````

## 5. 느낀점, 결론

프로젝트 완료 후 작성합니다.
