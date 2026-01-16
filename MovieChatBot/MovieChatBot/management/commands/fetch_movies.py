from django.core.management.base import BaseCommand
from django.conf import settings
from MovieChatBot.models import Movie
import requests

class Command(BaseCommand):
    help = 'TMDB에서 인기 영화의 상세 정보를 수집합니다.'

    def handle(self, *args, **kwargs):
        # settings.py에서 가져온 키 사용
        api_key = getattr(settings, 'TMDB_API_KEY', None)
        
        if not api_key:
            self.stdout.write(self.style.ERROR("API 키가 없습니다. .env 파일과 settings.py를 확인해주세요."))
            return

        # 장르 매핑 (TMDB 영어 장르 -> 형님 모델의 한글 코드)
        GENRE_MAP = {
            'Action': 'ACTION',
            'Romance': 'ROMANCE',
            'Comedy': 'COMEDY',
            'Thriller': 'THRILLER',
            'Drama': 'DRAMA',
            'Science Fiction': 'SF'
        }

        # 1. 인기 영화 목록 가져오기 (1페이지)
        list_url = 'https://api.themoviedb.org/3/movie/popular'
        params = {'api_key': api_key, 'language': 'ko-KR', 'page': 1}
        
        try:
            response = requests.get(list_url, params=params)
            response.raise_for_status()
            movie_list = response.json().get('results', [])
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"API 호출 실패: {e}"))
            return

        self.stdout.write(f"{len(movie_list)}개의 영화 정보를 상세 조회 및 저장합니다...")

        count = 0
        for item in movie_list:
            movie_id = item['id']
            
            # 2. 상세 정보 조회
            detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
            detail_params = {
                'api_key': api_key, 
                'language': 'ko-KR',
                'append_to_response': 'credits'
            }
            
            detail_res = requests.get(detail_url, params=detail_params)
            if detail_res.status_code != 200:
                continue
                
            info = detail_res.json()

            # 3. 데이터 가공
            release_date = info.get('release_date', '')
            release_year = int(release_date[:4]) if release_date else None

            tmdb_genres = info.get('genres', [])
            genre_code = None
            if tmdb_genres:
                first_genre_name = tmdb_genres[0]['name']
                genre_code = GENRE_MAP.get(first_genre_name) 

            crew_list = info.get('credits', {}).get('crew', [])
            director = next((p['name'] for p in crew_list if p['job'] == 'Director'), "정보 없음")
            
            cast_list = info.get('credits', {}).get('cast', [])
            actors = ", ".join([p['name'] for p in cast_list[:3]])

            # 4. DB 저장
            Movie.objects.update_or_create(
                tmdb_id=info['id'],
                defaults={
                    'title': info['title'],
                    'poster_path': info['poster_path'],
                    'release_year': release_year,
                    'genre': genre_code,
                    'running_time': info.get('runtime'),
                    'director': director,
                    'actors': actors,
                    'tmdb_average': info.get('vote_average', 0.0),
                }
            )
            count += 1
            self.stdout.write(f"[{count}] {info['title']} 저장 완료")

        self.stdout.write(self.style.SUCCESS("데이터 수집 완료!"))