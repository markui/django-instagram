"""
post앱을 생성
class Post(models.Model):
  photo = models.어떤필드를 써야할까요
  생성일시 기록

class PostComment(models.Model):
  photo = 자신의 Photo와 MTO로 연결
  생성일시 기록
"""

"""
member 앱을 생성
1. templates/member/signup.html
    input 2개를 구현
    name은 각각 username, password

2. views.py에
def signup(request):
    request.POST로 전달된 username, password값을 이용해
    새 유저를 생성(create_user()메서드를 사용
    그리고 만든 유저의 username과 password를 HttpResponse로 리턴
    
3. 사용하는 URL은
    /member/signup/
"""


