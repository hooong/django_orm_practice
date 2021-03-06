from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import F, Q
from .models import *


# N+1 문제
def user_list(request):
    # N+1이 발생하는 쿼리셋
    # users = User.objects.all()

    # N+1은 select_related(), prefetch_related()라는 메서드로 Eager Loading하여 방지할 수 있다.
    # select_related() : 정방향 참조 필드
    # prefetch_related() : 역방향 참조 필드
    users = User.objects.select_related('userinfo')

    for user in users:
        user.userinfo

    return render(request, 'index.html')


# F() => python 메모리에 저장을 하지 않고 쿼리문을 만들어 DB 자체에서 연산을 수행.
def age_for_f(request):
    userinfo_hong = Userinfo.objects.get(first_name='hong')

    # not used F()
    #userinfo_hong.age += 1

    # use F()
    userinfo_hong.age = F('age') + 1
    userinfo_hong.save()

    # F() 사용시 주의점 => 모델 필드에 할당된 F() 객체는 저장 후에도 유지된다.
    # userinfo_hong.age = F('age') + 1
    # userinfo_hong.save()
    #
    # userinfo_hong.first_name = 'hooong'
    # userinfo_hong.save()    # 'hong'을 가지고 있던 userinfo는 age가 2만큼 증가하게 된다.

    return render(request, 'index.html')


# Q() => Where절에 or 또는 AND를 추가할때 사용할 수 있는 함수
def q_function(request):

    userinfo_with_25_or_21 = Userinfo.objects.filter(
                                                Q(age=21) | Q(age=25))
    # SELECT * FROM "orm_test_userinfo"
    # WHERE ("orm_test_userinfo"."age" = 21 OR "orm_test_userinfo"."age" = 25) LIMIT 21;
    print(userinfo_with_25_or_21)

    q = Q()
    q.add(Q(age=20), q.OR)
    q.add(Q(first_name='a'), q.AND)     # 두번째 인자값은 해당 조건문 앞으로 붙는다.
    userinfo_a = Userinfo.objects.filter(q)
    # SELECT * FROM "orm_test_userinfo"
    # WHERE ("orm_test_userinfo"."age" = 20 AND "orm_test_userinfo"."first_name" = 'a') LIMIT 21;
    print(userinfo_a)

    return render(request, 'index.html')
