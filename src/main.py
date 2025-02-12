from settings import *
import menutools
import canvas
import pygame

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Drawing App')
clock = pygame.time.Clock()

canvas = canvas.Canvas(screen)

menu = menutools.Menu(screen, menutools.instruments_list)

is_onscreen = False
while True:
    xm, ym = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_focused():
            xm, ym = pygame.mouse.get_pos()

            # choose instrument
            menu.choose_instrument(xm, ym)

            # drawing
            if xm > 100 and xm < size[0] and ym > 0 and ym < size[1]:
                is_onscreen = True

            # eraser
            if menu.get_choosed == 'erase':
                handle_pos_eraser = menutools.eraser.slider._calculate_handle_position()
                #(self.x, handle_pos), self.handle_radius
                if xm > menutools.eraser.slider.x - menutools.eraser.slider.handle_radius \
                    and xm < menutools.eraser.slider.x + menutools.eraser.slider.handle_radius \
                        and ym > handle_pos_eraser - menutools.eraser.slider.handle_radius \
                            and ym < handle_pos_eraser + menutools.eraser.slider.handle_radius:
                    menutools.eraser.slider.is_dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            is_onscreen = False
            menutools.eraser.slider.is_dragging = False
            menutools.pen.positions = []

    # canvas
    screen.fill('white')

    #canvas.canvas_np = np.ones((*canvas_size, 3), dtype=np.uint8) * 255
    #cv2.circle(canvas.canvas_np, (300, 400), 100, (0, 0, 0), 1)
    #canvas.canvas = pygame.surfarray.make_surface(canvas.canvas_np)

    #start = time.time()
    #menutools.fill.fill(canvas, (300, 400))
    #end = time.time()
    #print('filled in: ', str(end-start))
    #times.append(end-start)

    canvas.draw(50, 0)

    # menu
    menu.draw(0, 0)
    menu.mouse_on_instrument(xm, ym)
    menutools.eraser.slider.calc()

    # drawing
    if is_onscreen:
        if menu.get_choosed == 'pen':
            if not menutools.pen.positions:
                menutools.pen.add_start_point(xm-50, ym)
            menutools.pen.add(xm-50, ym)
            menutools.pen.draw_pen(canvas)
        elif menu.get_choosed == 'fill':
            #plt.imshow(canvas.canvas_np)
            #plt.title('before')
            #plt.show()

            #print(f'Filled in: {menutools.fill.fill(canvas, (ym, xm-50))}')
            menutools.fill.fill(canvas, (ym, xm-50))

            #plt.imshow(canvas.canvas_np)
            #plt.title('after')
            #plt.show()
        elif menu.get_choosed == 'erase':
            menutools.eraser.erase(canvas, (xm-50, ym))

    if xm > 100 and xm < size[0] and ym > 0 and ym < size[1]:
        if menu.get_choosed == 'pen':
            pygame.draw.circle(screen, (0, 0, 0), (xm, ym), 5, 5)
        elif menu.get_choosed == 'erase':
            menutools.eraser.erase_field(screen, (xm, ym))

    pygame.display.flip()
    clock.tick(fps)