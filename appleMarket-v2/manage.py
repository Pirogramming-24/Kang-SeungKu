#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
if os.name == 'nt':
    # 폴더가 없으면 생성
    target_cache_dir = 'C:/paddle_cache'
    if not os.path.exists(target_cache_dir):
        try:
            os.makedirs(target_cache_dir)
        except:
            pass
            
    # 환경 변수 강제 설정 (Paddle이 '강승구'를 못 보게 함)
    os.environ['USERPROFILE'] = target_cache_dir
    os.environ['HOME'] = target_cache_dir
    os.environ['PADDLE_HOME'] = target_cache_dir
        
def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
