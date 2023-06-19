import pygame
import random

pygame.init() #초기화(반드시 필요)

#화면 크기 설정
screen_width=480
screen_height=640 #가로세로 크기
screen=pygame.display.set_mode((screen_width,screen_height))

#화면 타이틀 설정
pygame.display.set_caption('운석 피하기') #게임 이름

#FPS
clock=pygame.time.Clock()


#sprite(캐릭터) 불러오기
character=pygame.image.load('C:\pygame_discovery\운석 피하기\character.png')
character_size=character.get_rect().size #이미지의 크기를 구해옴
character_width=character_size[0] #캐릭터의 가로 크기
character_height=character_size[1] #캐릭터의 세로 크기
character_x_pos=screen_width/2-character_width/2 #화면 가로의 절반 크기에 해당하는 곳에 위치
character_y_pos=screen_height-character_height #화면 세로 크기 가장 아래에 해당하는 곳에 위치

#이동할 좌표
to_x=0

#이동 속도
character_speed=0.5

#적 캐릭터 생성 횟수
enemy_count=random.randint(1,3)
item_count=random.randint(1,3)

#적 캐릭터(enemy)
for e in range(enemy_count):
    enemy=pygame.image.load('C:\pygame_discovery\운석 피하기\enemy.png')
    enemy_size=enemy.get_rect().size #이미지의 크기를 구해옴
    enemy_width=enemy_size[0] #적의 가로 크기
    enemy_height=enemy_size[1] #적의 세로 크기
    enemy_x_pos=random.randint(0,screen_width-enemy_width)
    enemy_y_pos=0
    enemy_speed=10
    
#점수 캐릭터(item)
for _ in range(item_count):
    item=pygame.image.load('C:\pygame_discovery\운석 피하기\item.png')
    item_size=item.get_rect().size #이미지의 크기를 구해옴
    item_width=item_size[0] #적의 가로 크기
    item_height=item_size[1] #적의 세로 크기
    item_x_pos=random.randint(0,screen_width-item_width)
    item_y_pos=0
    item_speed=7

#폰트 정의
game_font=pygame.font.Font(None,40) #폰트 객체 생성(폰트, 크기)
end_font=pygame.font.Font(None,70)

#점수 정의
num=0

#목숨 개수 정의
remainHeart=3

#목숨 개수 텍스트 색깔 정의
c=255

#이벤트 루프
running=True #게임이 진행중인가?
while running:
    dt=clock.tick(70) #게임화면의 초당 프레임 수를 설정
    for event in pygame.event.get(): #어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: #창이 닫히는 이벤트가 발생하였는가?
            running=False #게임이 진행중이 아님.
    
        if event.type==pygame.KEYDOWN: #키가 눌러졌는지 확인
            if event.key==pygame.K_LEFT: #캐릭터를 왼쪽으로
                to_x -= character_speed
            elif event.key==pygame.K_RIGHT: #캐릭터를 오른쪽으로
                to_x += character_speed

        if event.type == pygame.KEYUP: #방향키를 떼면 멈춤
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x=0
    
    screen.fill((0,0,50)) #배경화면 채우기

    #게임 캐릭터 위치 정의
    character_x_pos += to_x*dt


    #가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos=0
    elif character_x_pos > screen_width-character_width:
        character_x_pos=screen_width-character_width

   
    
    enemy_y_pos+=enemy_speed #적이 점점 내려옴
    item_y_pos+=item_speed

   
    #적 세로 경계값 처리+바닥에 도착하면 다시 위로 올려보내기
    if enemy_y_pos>screen_height-enemy_height:
        enemy_y_pos=0
        enemy_x_pos=random.randint(0,screen_width-enemy_width)
        num+=1
        
    if item_y_pos>screen_height-item_height:
        item_y_pos=0
        item_x_pos=random.randint(0,screen_width-item_width)


        
    #충돌 처리를 위한 rect정보 업데이트
    character_rect=character.get_rect()
    character_rect.left=character_x_pos
    character_rect.top=character_y_pos

    enemy_rect=enemy.get_rect()
    enemy_rect.left=enemy_x_pos
    enemy_rect.top=enemy_y_pos

    item_rect=enemy.get_rect()
    item_rect.left=item_x_pos
    item_rect.top=item_y_pos

    

    #충돌 체크
    if character_rect.colliderect(enemy_rect):
        enemy_y_pos=0
        remainHeart-=1
        c-=70
    
    if character_rect.colliderect(item_rect):
        item_y_pos=0
        num+=3
    
        
        

    #세 번째 맞았을 때 게임종료
    if remainHeart==0:
        end_message='Game Over'
        running=False



    remainHeart_num=game_font.render(f'Heart: {str(remainHeart)}', True, (255,c,c))
    text_num=game_font.render(f'Score: {str(num)}', True, (255,255,255))
    # 출력할 글자, True, 글자 색상

   
    screen.blit(character,(character_x_pos,character_y_pos)) #캐릭터 그리기
    screen.blit(enemy,(enemy_x_pos,enemy_y_pos)) #적 캐릭터(enemy) 그리기
    screen.blit(item,(item_x_pos,item_y_pos))
    screen.blit(text_num,(10,10)) #피한 개수(nums) 그리기
    screen.blit(remainHeart_num,(365,10))
    
    
    pygame.display.update() #게임 화면을 다시 그리기!(필수)



#게임오버 메세지 출력
message=end_font.render(end_message, True, (255,0,0))
screen.blit(message,(107,200))
pygame.display.update()

#잠시 대기
pygame.time.delay(2000) #1초 정도 대기(ms)



#pygame 종료
pygame.quit()

#추가할 것
#충돌했을 때 게임오버 텍스트 화면에 띄우기(완료)
#충돌 세번했을 때 게임오버 되게 하기(완료)
#추가로 하트 개수 줄어들때마다 글자 점점 빨간색으로 보이게 함.(완료)
