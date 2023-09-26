import pygame

pygame.init()
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
dark_green = (21, 71, 52)

gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Cubic Bezier Curve with Matrices")
clock = pygame.time.Clock()

def plot(x, y, w, h, c):
    pygame.draw.rect(gameDisplay, c, [x, y, w, h])

def calculate_curve(t, P0, P1):
    (1-t)(P0[0] + t*P1[1]) + t((1-t)*P0[0] + t*P1[1])

def game_loop():
    gameExit = False

    scale = 10
    scale_change = 0
    
    #sextic coords
    x = [-1, 3, 4, 6, 8, 10, 13, 20]
    y = [-1, 3, 0, 4, -2, 0,  5,  0]
    
    m = [[ -1,    7,  -21,   35,  -35,  21, -7, 1], 
         [  7,  -42,  105, -140,  105, -42,  7, 0],
         [-21,  105, -210,  210, -105,  21,  0, 0], 
         [ 35, -140,  210, -140,   35,   0,  0, 0],
         [-35,  105, -105,   35,    0,   0,  0, 0],
         [ 21,  -42,   21,    0,    0,   0,  0, 0],
         [ -7,    7,    0,    0,    0,   0,  0, 0],
         [  1,    0,    0,    0,    0,   0,  0, 0]]
   
    row = 8
    col = 8

    tm = [1, 1, 1, 1, 1, 1, 1, 1]

    x0_change = 0
    x2_change = 0
    x3_change = 0
    x4_change = 0
    x6_change = 0
    y1_change = 0
    y3_change = 0
    y4_change = 0
    

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    scale_change = 1
                elif event.key == pygame.K_DOWN:
                    scale_change = -1
                elif event.key == pygame.K_a:
                    y1_change = 1
                elif event.key == pygame.K_s:
                    y1_change = -1
                elif event.key == pygame.K_z:
                    y3_change = 1
                elif event.key == pygame.K_x:
                    y3_change = -1
                elif event.key == pygame.K_c:
                    y4_change = -1
                elif event.key == pygame.K_v:
                    y4_change = 1
                elif event.key == pygame.K_q:
                    x0_change = -1
                elif event.key == pygame.K_w:
                    x0_change = 1
                elif event.key == pygame.K_t:
                    x2_change = 1
                elif event.key == pygame.K_y:
                    x2_change = -1
                elif event.key == pygame.K_e:
                    x3_change = -1
                elif event.key == pygame.K_r:
                    x3_change = 1
                elif event.key == pygame.K_f:
                    x4_change = -1
                elif event.key == pygame.K_g:
                    x4_change = 1
                elif event.key == pygame.K_h:
                    x6_change = -1
                elif event.key == pygame.K_j:
                    x6_change = 1
                

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    scale_change = 0
                elif event.key == pygame.K_a or event.key == pygame.K_s:
                    y1_change = 0
                elif event.key == pygame.K_z or event.key == pygame.K_x:
                    y3_change = 0
                elif event.key == pygame.K_q or event.key == pygame.K_w:
                    x0_change = 0
                elif event.key == pygame.K_e or event.key == pygame.K_r:
                    x3_change = 0
                elif event.key == pygame.K_t or event.key == pygame.K_y:
                    x2_change = 0
                elif event.key == pygame.K_f or event.key == pygame.K_g:
                    x4_change = 0
                elif event.key == pygame.K_c or event.key == pygame.K_v:
                    y4_change = 0
                elif event.key == pygame.K_h or event.key == pygame.K_j:
                     x6_change = 0
                

        gameDisplay.fill(white)

        plot(0, 300, 800, 1, red)
        plot(400, 0, 1, 600, blue)

        # limit scale to be at least 10
        if scale + scale_change > 10:
            scale = scale + scale_change

        # determine number of ticks to draw on each axis
        # larger scale -> smaller number of ticks
        x_ticks = int(400 / scale + 1)
        y_ticks = int(300 / scale + 1)

        # plot x-ticks and y-ticks
        for i in range(y_ticks):
            plot(399, 299 - i * scale, 3, 3, dark_green)
        for i in range(y_ticks):
            plot(399, 299 + i * scale, 3, 3, dark_green)
        for i in range(x_ticks):
            plot(399 + i * scale, 299, 3, 3, dark_green)
        for i in range(x_ticks):
            plot(399 - i * scale, 299, 3, 3, dark_green)
        
        # change in control points position
        x[0] += x0_change * 0.1
        x[2] += x2_change * 0.1
        x[3] += x3_change * 0.1
        x[4] += x4_change * 0.1
        x[6] += x6_change * 0.1
        y[1] += y1_change * 0.1
        y[3] += y3_change * 0.1
        y[4] += y4_change * 0.1
        
        xm = [0, 0, 0, 0, 0, 0, 0, 0]
        ym = [0, 0, 0, 0, 0, 0, 0, 0]
        
        for i in range(row):
            for j in range(col):
                xm[i] += x[j] * m[j][i]
                ym[i] += y[j] * m[j][i]
        
        t = 0
        t_end = 1
        
        # compute and plot bounding polygon - Q0, Q1, Q2, Q3, C0, C1, D0, E0
        while t <= t_end:
            for i in range(col-1):
                X = (1-t) * x[i] + t * x[i+1]
                Y = (1-t) * y[i] + t * y[i+1]
                plot(X*scale+399, 299-Y*scale, 3, 3, green)
            
         
            for i in range(6,-1,-1):
                tm[i] = tm[i+1] * t

            X = 0
            Y = 0
            # compute second part: computed->
            # ([P0 P1 P2 P3 P4 P5 P6 P7] * coefficients matrix) * [t7 t6 t5 t4 t3 t2 t 1]
            for i in range(col):
                X += xm[i] * tm[i]
                Y += ym[i] * tm[i]
            plot(X*scale+399, 299-Y*scale, 3, 3, red)

            t += 0.005

        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
