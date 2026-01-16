from django.core.management.base import BaseCommand
from django.conf import settings
from MovieChatBot.models import Movie, Review
import requests

class Command(BaseCommand):
    help = 'TMDB에서 인기 영화와 줄거리(요약)를 수집합니다.'

    def handle(self, *args, **kwargs):
        api_key = getattr(settings, 'TMDB_API_KEY', None)
        if not api_key:
            self.stdout.write(self.style.ERROR("API 키가 없습니다."))
            return

        # [수정됨] TMDB가 한국어로 응답하므로, 키 값을 한글로 변경했습니다.
        GENRE_MAP = {
            '액션': 'ACTION',
            '로맨스': 'ROMANCE',
            '멜로': 'ROMANCE', # TMDB가 가끔 멜로라고 줄 수도 있음
            '코미디': 'COMEDY',
            '스릴러': 'THRILLER',
            '드라마': 'DRAMA',
            'SF': 'SF',
            '공상과학': 'SF'
        }

        # 1. 영화 목록 가져오기
        list_url = 'https://api.themoviedb.org/3/movie/popular'
        params = {'api_key': api_key, 'language': 'ko-KR', 'page': 1}
        
        try:
            response = requests.get(list_url, params=params)
            movie_list = response.json().get('results', [])
        except Exception:
            return

        self.stdout.write(f"{len(movie_list)}개의 영화와 요약을 저장합니다...")

        for item in movie_list:
            movie_id = item['id']
            
            # 2. 상세 정보 조회
            detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
            detail_params = {'api_key': api_key, 'language': 'ko-KR', 'append_to_response': 'credits'}
            
            res = requests.get(detail_url, params=detail_params)
            if res.status_code != 200: continue
            info = res.json()

            # 데이터 가공
            release_year = int(info['release_date'][:4]) if info.get('release_date') else None
            
            # [수정됨] 장르 매핑 로직
            tmdb_genres = info.get('genres', [])
            genre_code = None
            if tmdb_genres:
                first_genre_name = tmdb_genres[0]['name'] # 이제 여기서 '액션'이 나옵니다.
                genre_code = GENRE_MAP.get(first_genre_name) 
                # 만약 매핑 안 된 장르(예: 애니메이션)라면 그냥 None으로 둠

            crew = info.get('credits', {}).get('crew', [])
            director = next((p['name'] for p in crew if p['job'] == 'Director'), "정보 없음")
            
            cast = info.get('credits', {}).get('cast', [])
            actors = ", ".join([p['name'] for p in cast[:3]])
            
            tmdb_score = info.get('vote_average', 0.0)

            # 3. 영화 저장
            movie, created = Movie.objects.update_or_create(
                tmdb_id=info['id'],
                defaults={
                    'title': info['title'],
                    'poster_path': info['poster_path'],
                    'release_year': release_year,
                    'genre': genre_code, # 수정된 장르 코드 저장
                    'running_time': info.get('runtime'),
                    'director': director,
                    'actors': actors,
                    'tmdb_average': tmdb_score,
                }
            )

            # 4. 줄거리(Overview) 저장 로직
            overview = info.get('overview', '')
            if overview:
                rating = round(tmdb_score / 2)
                if rating < 1: rating = 1
                if rating > 5: rating = 5

                if not Review.objects.filter(movie=movie, is_tmdb=True).exists():
                    Review.objects.create(
                        movie=movie,
                        rating=rating,
                        content=overview,
                        is_tmdb=True
                    )
                    
        self.stdout.write(self.style.SUCCESS("완료!"))