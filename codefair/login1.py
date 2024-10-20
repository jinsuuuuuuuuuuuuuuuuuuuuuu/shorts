from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle

# 인증 관련 정보
SCOPES = ['https://www.googleapis.com/auth/takeout.readonly']
creds = None

# token.pickle 파일에 저장된 기존 자격 증명 로드
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

# 자격 증명이 없거나 만료된 경우 새로 인증
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

    # 자격 증명 저장
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

# 자격 증명을 사용하여 API 호출
from googleapiclient.discovery import build
service = build('takeout', 'v1', credentials=creds)

# API 요청 코드 추가
