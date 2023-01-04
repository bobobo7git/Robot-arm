import pygame
import numpy as np
import time

# 게임 윈도우 크기
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

# 색 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SILVER = (192, 192, 192)



def Rmat(deg):
    radian = np.deg2rad(deg)

    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array([[c, -s, 0],[s, c, 0], [0, 0, 1]])
    return R

def Tmat(a,b):
    H = np.eye(3)
    H[0,2] = a
    H[1,2] = b
    return H

class Arm:
    def __init__(self):
        self.width = 200
        self.height = 40
        self.deg = 0
        self.d = 0
        self.color = SILVER

        self.Lcor = np.array([self.height/2, self.height/2, 1])
        self.Rcor = np.array([self.width - self.height/2, self.height/2, 1])
        self.poly = np.array([[0, 0, 1],[self.width, 0, 1],
         [self.width, self.height, 1], [0, self.height, 1]])
        
        self.poly = self.poly.T
        
    def update(self,m = None):
        
        if m != None:
            self.corp = m.H @ m.Rcor
            self.H = Tmat(self.corp[0],self.corp[1]) @ Rmat(self.deg) @ Tmat(-self.Lcor[0],-self.Lcor[1])
            self.pp = m.H @ self.poly
        if m is None:
            self.H = Tmat(200,400) @ Tmat(self.Lcor[0],self.Lcor[1]) @ Rmat(self.deg) @ Tmat(-self.Lcor[0],-self.Lcor[1])
            self.corp = self.H @ self.Lcor
            self.pp = self.H @ self.poly
        self.deg -= self.d
        
        self.q = self.pp[0:2, :].T

        

    def draw(self,screen):
        
        pygame.draw.polygon(screen, self.color, self.q, 0)
        pygame.draw.polygon(screen, BLACK, self.q, 3)
        pygame.draw.circle(screen,BLACK, self.corp[:2], 5)

class Grip:
    def __init__(self):
        self.width = 60
        self.height = 10
        self.deg = 0
        self.color = BLACK
        self.poly  = np.array([[0, 0, 1],[self.width, 0, 1],
         [self.width, self.height, 1], [0, self.height, 1]])
        self.poly2 = np.array([[0,0,1],[10,0,1],[10,40,1],[0,40,1]])
        self.poly3 = np.array([[0,0,1],[30,0,1],[30,10,1],[0,10,1]])
        self.poly4 = np.array([[0,0,1],[30,0,1],[30,10,1],[0,10,1]])
        
    
    def update(self, arm,deg):
        self.deg = deg
        self.H =  Tmat(arm.corp[0],arm.corp[1]) @ Rmat(self.deg) @Tmat(-self.height/2, -self.height/2)
        self.H2 =  self.H @ Tmat(self.width,-arm.height/2 + 5)
        self.H3 =  self.H @ Tmat(self.width,-arm.height/2 + 5)
        self.H4 =  self.H3 @ Tmat(0,+arm.height - 5)
        self.pp = self.H @ self.poly.T 
        self.pp2 = self.H2 @ self.poly2.T
        self.pp3 = self.H3 @ self.poly3.T
        self.pp4 = self.H4 @ self.poly4.T
        self.q = self.pp[0:2].T
        self.q2 = self.pp2[0:2].T
        self.q3 = self.pp3[0:2].T
        self.q4 = self.pp4[0:2].T
        #print(arm.deg, self.deg)

    def draw(self,screen):
        pygame.draw.polygon(screen, self.color, self.q, 0)
        pygame.draw.polygon(screen, self.color, self.q2, 0)
        pygame.draw.polygon(screen, self.color, self.q3, 0)
        pygame.draw.polygon(screen, self.color, self.q4, 0)
        


# Pygame 초기화
pygame.init()

# 윈도우 제목
pygame.display.set_caption("Robot arms")

# 윈도우 생성
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 게임 화면 업데이트 속도
clock = pygame.time.Clock()


font = pygame.font.SysFont('FixedSys', 40, True, False)
# 게임 종료 전까지 반복
done = False


arm_base = Arm()
arm_base.d = 0
arm_base.deg = -90
arm_base.H = Tmat(200,300) @ Tmat(arm_base.Lcor[0],arm_base.Lcor[1]) @ Rmat(arm_base.deg) @ Tmat(-arm_base.Lcor[0],-arm_base.Lcor[1])

armList = []
armList.append(arm_base)
for i in range(4):
    armList.append(Arm())

grip = Grip()

autoMode = False
timer = [0,0,0,0]

msg = "Auto Mode : Off"


# 게임 반복 구간
while not done:
    # 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN and autoMode == False:
            if event.key == pygame.K_q:
                armList[0].d = 1
            if event.key == pygame.K_a:
                armList[0].d = -1
            if event.key == pygame.K_w:
                armList[1].d = 1
            if event.key == pygame.K_s:
                armList[1].d = -1
            if event.key == pygame.K_e:
                armList[2].d = 1
            if event.key == pygame.K_d:
                armList[2].d = -1
            if event.key == pygame.K_r:
                armList[3].d = 1
            if event.key == pygame.K_f:
                armList[3].d = -1
            if event.key == pygame.K_SPACE:
                autoMode = True
        elif event.type == pygame.KEYDOWN and autoMode:
            if event.key == pygame.K_SPACE:
                autoMode = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_q or event.key == pygame.K_a:
                armList[0].d = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                armList[1].d = 0
            if event.key == pygame.K_e or event.key == pygame.K_d:
                armList[2].d = 0
            if event.key == pygame.K_r or event.key == pygame.K_f:
                armList[3].d = 0
            
    # 게임 로직 구간

    # 화면 삭제 구간

    # 윈도우 화면 채우기
    screen.fill(WHITE)

    arm_base.update()
    arm_base.draw(screen)
 
    for i in range(1, len(armList)):
        armList[i].update(armList[i-1])
        armList[i].draw(screen)

    
    
    grip.update(armList[len(armList)-1],armList[len(armList)-2].deg)
    grip.draw(screen)

    armList[1].color = 90,90,90
    armList[2].color = 120,120,120
    armList[3].color = 150,150,150

    if autoMode:
        for i in range(4):
            timer[i] += 1
        if(timer[0] < 60):
            armList[0].deg += 1
        if(timer[0] > 60):
            armList[0].deg = armList[0].deg
        if(timer[0] > 240):
            timer[0] = 0
        if(timer[1] > 180):
            armList[1].deg += -0.5
        if(timer[1] > 240):
            armList[1].deg = armList[1].deg
            timer[1] = 0
        if(timer[2] > 240):
            armList[2].deg += 1
        if(timer[2] > 360):
            armList[2].deg = armList[2].deg
            timer[2] = 0
        if(timer[3] > 120):
            armList[3].deg += 3
        if(timer[3] > 130):
            armList[3].deg -= 3
        if(timer[3] > 270):
            armList[3].deg -= 3
        if(timer[3] > 300):
            armList[3].deg = armList[3].deg
            timer[3] = 0

    if autoMode == False:
        for i in range(4):
            timer[i] = 0

    print(timer[3])
    
    
    text1 = font.render("Press q,w,e,r to make the joints up", True, BLACK)
    text2 = font.render("Press a,s,d,f to make them down", True, BLACK)
    text3 = font.render("Press space to toggle auto mode", True, BLACK)
    text4 = font.render(msg, True, BLUE)

    # 화면에 텍스트 표시
    
    screen.blit(text1,[10,10])
    screen.blit(text2,[10,50])
    screen.blit(text3,[10,90])
    if(autoMode):
        msg = "Auto Mode : On"
        text4 = font.render(msg, True, BLUE)
    else:
        msg = "Auto Mode : Off"
        text4 = font.render(msg, True, RED)
    screen.blit(text4,[WINDOW_WIDTH - text4.get_width() - 10,10])
    
    # 화면 업데이트
    pygame.display.flip()

    # 초당 60 프레임으로 업데이트
    clock.tick(60)

# 게임 종료
pygame.quit()