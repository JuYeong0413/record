from django.contrib import admin
from .models import Music

# Register your models here.
# admin.ModelAdmin 상속을 통해 커스터마이징, 장식자(decorator) 형태로 등록
@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):

    # 목록 내에서 링크로 지정할 필드 목록
    # 옵션을 지정하지 않으면 첫 번째에 위치하는 필드만 링크가 가능함
    list_diaply_links = (
        'title',
    )

    # 사용자가 입력하는 검색어를 찾을 필드
    search_fields = (
        'title',
        'singer',
    )

    # 필터 옵션을 제공할 필드 목록
    list_filter = (
    )

    # Admin 사이트에 보여질 필드 목록
    list_display = (
        'title',
        'genre',
        'singer',
        'writer',
        'created_at',
        'updated_at',
    )