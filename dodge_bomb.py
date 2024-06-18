import os
import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1300, 800
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = {
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5, 0),
    }


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect，または，爆弾Rect
    戻り値：真理値タプル（横方向，縦方向）
    画面内ならTrue　画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def kk_change(yoko, tate):
    katamuki = 0
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), katamuki, 2.0)
    if(yoko, tate) == (0, -5):
        katamuki = -90
        kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), katamuki, 2.0)
        kk_img = pg.transform.flip(kk_img, True, False)

    elif(yoko, tate) == (+5, -5):
        kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 2.0)
        kk_img = pg.transform.flip(kk_img, True, False)

    elif(yoko, tate) == (+5, 0):
        kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
        kk_img = pg.transform.flip(kk_img, True, False)
            
    elif(yoko, tate) == (+5, +5):
        kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 2.0)
        kk_img = pg.transform.flip(kk_img, True, False)

    elif(yoko,tate) == (0, +5):
        kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 90, 2.0)
        kk_img = pg.transform.flip(kk_img, True, False)
    
    elif(yoko, tate) == (-5, +5):
        kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 2.0)

    elif(yoko, tate) == (-5, 0):
        kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)

    elif(yoko, tate) == (-5, -5):
        kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 2.0)
    return kk_img


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")   
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    clock = pg.time.Clock()
    tmr = 0


    #爆弾の描画
    bb_img = pg.Surface((20, 20))
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()  # 爆弾Rect
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):  # 衝突判定
            return  # ゲームオーバー
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
                kk_img = kk_change(sum_mv[0], sum_mv[1])
                

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        bb_rct.move_ip(vx, vy)  #爆弾の動き
        screen.blit(bb_img, bb_rct)  #爆弾の動き
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
