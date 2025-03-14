# Reversible Watermarking for Secure Image Protection

## 📌 Project Overview
본 애플리케이션은 이미지의 품질을 손상시키지 않으면서 텍스트 워터마크를 안전하게 삽입하고 제거할 수 있는 도구입니다. 암호화 및 복호화 과정을 통해 원본 이미지와 워터마크를 복구할 수 있으며, **군사 및 의료 분야**와 같은 보안이 중요한 환경에서 활용할 수 있습니다.

## 🎯 주요 기능
- **워터마크 삽입**: 사용자가 입력한 텍스트를 이미지에 삽입
- **워터마크 제거**: 올바른 키를 입력하면 삽입된 워터마크 복구
- **전체 이미지 복구**: 내장된 텍스트를 모두 추출하고 원본 이미지를 손실 없이 재구성합니다.
- **성능 평가**: PSNR, BER 등의 지표를 사용하여 이미지 품질 분석
- **사용자 친화적인 인터페이스**: 간편한 암호화, 임베딩, 추출 및 복호화가 가능합니다.

## 🛠️ 기술스택
- **Programming Language**: Python
- **Libraries**: OpenCV, NumPy, PyCryptodome, Tkinter (for UI)
- **Image Format**: .tiff (ensuring high-quality preservation)


## 🚀 실행 방법
### 1️⃣ 환경 설정
1. 애플리케이션을 실행하기 위해 필요한 라이브러리를 설치합니다.
pip install -r requirements.txt
2. 프로그램 실행
UI branch로 이동 후 python main.py
3. 이미지 포맷
본 애플리케이션은 .tiff 형식의 이미지를 지원합니다. 다른 형식의 이미지는 .tiff로 변환 후 사용해야 합니다.

### 사용 방법
1. 워터마크 삽입
#### <img width="529" alt="Screenshot 2025-03-11 at 2 06 54 PM" src="https://github.com/user-attachments/assets/a76f6022-49dd-4ed3-87ff-e3d10693dbc8" />
- 이미지 불러오기: Open Image 버튼을 눌러 .tiff 이미지를 선택
- 워터마킹 알고리즘 선택: 드롭다운 메뉴에서 알고리즘 선택
- 워터마크 텍스트 입력: 워터마크로 삽입할 텍스트 입력
- 데이터 히딩 키 입력: 숫자로 된 데이터 히딩 키 입력 (예: 1234)
- 암호화 키 입력: 16바이트 길이의 암호화 키 입력
- 삽입 실행: Submit 버튼을 눌러 워터마크 삽입
- 결과 확인: 삽입된 워터마크 이미지가 embedded_image.tiff로 저장
#### <img width="528" alt="Screenshot 2025-03-11 at 2 02 30 PM" src="https://github.com/user-attachments/assets/143c584f-977b-4013-a6a2-1d59294a49cd" />

2. 워터마크 복구 및 제거
- 암호화된 이미지 불러오기
Decryption 탭에서 .tiff 이미지를 선택
- 암호화 키 입력
삽입 시 사용한 16바이트 암호화 키 입력
- 키가 다를 경우 복호화 실패: “Decryption key is incorrect. The extracted message is invalid.”
- 데이터 히딩 키 및 블록 크기 입력
원래 사용한 값과 동일해야 정확한 워터마크 복구 가능
- 복호화 실행
Decrypt 버튼 클릭 후 원본 이미지 및 텍스트 확인
#### <img width="214" alt="Screenshot 2025-03-11 at 2 02 59 PM" src="https://github.com/user-attachments/assets/5b7dfe4b-4de5-4885-9bf9-75253b56946e" />
#### <img width="449" alt="Screenshot 2025-03-11 at 2 03 56 PM" src="https://github.com/user-attachments/assets/44e253d0-eacc-45dd-a3dd-093f09ff3528" />

3. 성능 평가
워터마크 제거 후 Calculate Statistics 버튼을 눌러 PSNR, BER 등의 성능 지표를 확인할 수 있습니다.
#### <img width="366" alt="Screenshot 2025-03-11 at 2 04 09 PM" src="https://github.com/user-attachments/assets/958377db-2bdd-486e-a187-c85a2aa50097" />


주의: 여러 블록 크기에서 반복 계산이 수행되므로 최대 15초가 소요될 수 있습니다.

## 시스템 요구 사항
Python 3.7 이상
OpenCV, NumPy, PyCryptodome 등의 라이브러리 사용

### 3️⃣ Workflow
- **1단계**: AES-CTR을 사용하여 이미지를 암호화합니다.
- **2단계**: 암호화된 이미지에 텍스트 워터마크를 삽입합니다.
- **3단계**: 워터마크된 이미지에서 워터마크를 추출합니다.
- **4단계**: 이미지를 원래 형태로 다시 해독합니다.

## 📊 Performance Metrics
이 프로젝트는 워터마킹의 결과:
- **PSNR(피크 신호 대 잡음비)**: 복구된 이미지의 품질을 측정합니다.
- **BER (비트 오류율)**: 추출된 워터마크의 정확도를 결정합니다.
  
## 👥 Team Contributions
- **김예찬**: UI 구현, 시각화 및 암호화 알고리즘 개발.
- **Chen Hao**: 데이터 추출 및 복호화 구현.
- **Manan**: UI 디자인 및 통합.
- **Iwyn**: 워터마크 임베딩 알고리즘 구현.

## 📌 Applications
- **의료 영상**: 의료 스캔에 환자 정보를 안전하게 삽입합니다.
- **군사 통신**: 민감한 데이터를 안전하게 내장하고 복구할 수 있도록 보장합니다.
- **저작권 보호**: 디지털 미디어에서 지적 재산권 보호.

## 📢 Future Improvements
- **더 높은 용량과 견고성**을 위한 워터마킹 알고리즘 최적화.
- **다양한 이미지 형식(JPEG, PNG 등)**에 대한 지원 구현**.
- UI/UX를 향상시켜 **더 나은 사용자 상호작용과 경험**을 제공합니다.
