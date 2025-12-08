from __future__ import annotations
import pygame as pg
import os
from enum import Enum
from typing import Callable, Optional, Tuple

class MenuOption(Enum):
    """
    enumeration for menu options that the user can select
    provides three main choices for navigation
    """
    NEW_GAME = 1
    INFO = 2
    QUIT = 3


class MenuButton:
    """
    interactive button class for the main menu
    handles rendering, hover effects, and click events
    each button can have different images for normal and hover states
    """
    
    def __init__(self, x: int, y: int, width: int, height: int,
                 callback: Optional[Callable] = None,
                 image: Optional[pg.Surface] = None,
                 hover_image: Optional[pg.Surface] = None):
        """
        initialize a new menu button with position and size
        callback function is executed when the button is clicked
        """
        self.rect = pg.Rect(x, y, width, height)
        self.callback = callback
        self.image = image
        self.hover_image = hover_image
        self.is_hovered = False
    
    def set_position(self, x: int, y: int):
        """update the button position on screen"""
        self.rect.x = x
        self.rect.y = y
    
    def handle_event(self, event) -> bool:
        """
        process mouse events for this button
        returns true if button was clicked
        """
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()
                return True
        return False
    
    def update(self, mouse_pos: Tuple[int, int]):
        """check if mouse is hovering over the button"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def draw(self, screen: pg.Surface):
        """render the button with appropriate image based on hover state"""
        current_image = self.hover_image if self.is_hovered else self.image
        if current_image:
            screen.blit(current_image, self.rect.topleft)


class Menu:
    """
    main menu class that handles the game's start screen
    manages parallax background layers, title animation, and menu buttons
    implements mouse-based parallax effect for visual depth
    """
    
    def __init__(self, screen: pg.Surface, font: pg.font.Font) -> None:
        """
        initialize the menu with screen and font
        loads all visual assets including parallax layers and buttons
        """
        self.screen = screen
        self.font = font
        
        # menu state variables
        self.running = True
        self.selected_option = None
        self.show_info = False
        
        # load background parallax layers (11 layers total)
        self.background_layers = []
        self.load_background_layers()
        
        # load title parallax layers (5 layers total)
        self.title_layers = []
        self.load_title_layers()
        
        # initialize menu buttons
        self.load_buttons()
        
        # load info screen image
        self.info_image = pg.image.load("media/hud/backgrounds/info.png").convert_alpha()
        
        # mouse position offsets for parallax effect
        self.mouse_offset_x = 0
        self.mouse_offset_y = 0
        
        # create close button for info page
        close_btn_img = pg.image.load("media/hud/buttons/close_2.png").convert_alpha()
        close_btn_hover = pg.image.load("media/hud/buttons/close_2_hover.png").convert_alpha()
        close_btn_img = pg.transform.scale(close_btn_img, (60, 60))
        close_btn_hover = pg.transform.scale(close_btn_hover, (60, 60))
        
        self.close_info_button = MenuButton(
            0, 0, 60, 60,  # position will be updated later
            callback=self.close_info,
            image=close_btn_img,
            hover_image=close_btn_hover
        )
        
    def load_background_layers(self):
        """
        load all 11 parallax background layers
        layers are ordered from closest to farthest (01_ground to 11_background)
        each layer gets a different parallax factor for depth effect
        """
        background_files = [
            "01_ground.png",
            "02_trees and bushes.png", 
            "03_distant_trees.png",
            "04_bushes.png",
            "05_hill1.png",
            "06_hill2.png",
            "07_huge_clouds.png",
            "08_clouds.png",
            "09_distant_clouds1.png",
            "10_distant_clouds.png",
            "11_background.png"
        ]
        
        for i, filename in enumerate(background_files):
            path = os.path.join("media/parallax/background", filename)
            img = pg.image.load(path).convert_alpha()
            
            # calculate zoom needed to avoid visible edges
            # add 20% margin for parallax movement
            screen_width, screen_height = self.screen.get_size()
            img_width, img_height = img.get_size()
            
            # compute zoom factor to cover entire screen with margin
            zoom_factor = max(
                (screen_width * 1.2) / img_width,
                (screen_height * 1.2) / img_height
            )
            
            new_width = int(img_width * zoom_factor)
            new_height = int(img_height * zoom_factor)
            
            scaled_img = pg.transform.scale(img, (new_width, new_height))
            
            # last layer (11_background.png) remains fixed
            is_fixed = (i == len(background_files) - 1)
            
            # files are ordered from CLOSEST to FARTHEST
            # 01 (ground) = index 0 = closest = moves FASTEST
            # 11 (background) = index 10 = farthest = FIXED
            # higher index means farther away, so slower movement
            if not is_fixed:
                # index 0 (01_ground.png) → 0.10
                # index 1 (02_trees.png) → 0.09
                # index 9 (10_distant_clouds.png) → 0.01
                parallax_factor = 0.10 - (i * 0.01)
            else:
                parallax_factor = 0.0
            
            self.background_layers.append({
                'image': scaled_img,
                'parallax_factor': parallax_factor,
                'is_fixed': is_fixed
            })
    
    def load_title_layers(self):
        """
        load the 5 parallax layers for the title screen
        different parallax speeds create depth illusion
        03_fix_title remains static while others move subtly
        """
        title_files = [
            "01_title.png",
            "02_title.png",
            "03_fix_title.png",
            "05_title.png",
            "06_title.png"
        ]
        
        # different parallax factors for each layer (fairly slow)
        # 01_title = closest = 0.03
        # 02_title = 0.025
        # 03_fix_title = fixed = 0.0
        # 05_title = 0.015
        # 06_title = farthest = 0.01
        parallax_factors = [0.03, 0.025, 0.0, 0.015, 0.01]
        
        for i, filename in enumerate(title_files):
            path = os.path.join("media/parallax/title", filename)
            img = pg.image.load(path).convert_alpha()
            
            # 03_fix_title.png stays fixed
            is_fixed = (filename == "03_fix_title.png")
            
            # use specific factor for this layer
            parallax_factor = parallax_factors[i]
            
            self.title_layers.append({
                'image': img,
                'parallax_factor': parallax_factor,
                'is_fixed': is_fixed
            })
    
    def load_buttons(self):
        """
        initialize all menu buttons with their images
        all buttons are square shaped for consistent look
        play button is larger than info and quit buttons
        """
        # load button images
        play_img = pg.image.load("media/hud/buttons/play.png").convert_alpha()
        play_hover = pg.image.load("media/hud/buttons/play_hover.png").convert_alpha()
        info_img = pg.image.load("media/hud/buttons/info.png").convert_alpha()
        info_hover = pg.image.load("media/hud/buttons/info_hover.png").convert_alpha()
        quit_img = pg.image.load("media/hud/buttons/quit.png").convert_alpha()
        quit_hover = pg.image.load("media/hud/buttons/quit_hover.png").convert_alpha()
        
        # resize buttons - ALL SQUARE like shop and bulldozer
        # play: larger size (140x140)
        play_img = pg.transform.scale(play_img, (140, 140))
        play_hover = pg.transform.scale(play_hover, (140, 140))
        
        # info and quit: same size as shop/bulldozer (110x110)
        info_img = pg.transform.scale(info_img, (110, 110))
        info_hover = pg.transform.scale(info_hover, (110, 110))
        quit_img = pg.transform.scale(quit_img, (110, 110))
        quit_hover = pg.transform.scale(quit_hover, (110, 110))
        
        # button positions (will be updated in update_button_positions)
        screen_width, screen_height = self.screen.get_size()
        center_x = screen_width // 2
        center_y = screen_height * 2 // 3  # position in lower third
        
        # play button (center) - 140x140
        self.play_button = MenuButton(
            center_x - 70, center_y - 70, 140, 140,
            callback=self.start_game,
            image=play_img,
            hover_image=play_hover
        )
        
        # info button (right of play) - 110x110
        self.info_button = MenuButton(
            center_x + 90, center_y - 55, 110, 110,
            callback=self.open_info,
            image=info_img,
            hover_image=info_hover
        )
        
        # quit button (left of play) - 110x110
        self.quit_button = MenuButton(
            center_x - 200, center_y - 55, 110, 110,
            callback=self.quit_game,
            image=quit_img,
            hover_image=quit_hover
        )
        
        self.buttons = [self.play_button, self.info_button, self.quit_button]
    
    def update_button_positions(self):
        """
        recalculate button positions based on current screen size
        ensures proper centering when window is resized
        """
        screen_width, screen_height = self.screen.get_size()
        center_x = screen_width // 2
        center_y = screen_height * 2 // 3
        
        # reposition SQUARE buttons
        # play: 140x140 in center
        self.play_button.set_position(center_x - 70, center_y - 70)
        # info: 110x110 to the right of play
        self.info_button.set_position(center_x + 90, center_y - 55)
        # quit: 110x110 to the left of play
        self.quit_button.set_position(center_x - 200, center_y - 55)
        
        # update close button for info screen
        if self.show_info:
            # calculate size and position of info image
            screen_width, screen_height = self.screen.get_size()
            info_scale = min(screen_width * 0.8 / self.info_image.get_width(),
                           screen_height * 0.8 / self.info_image.get_height())
            info_width = int(self.info_image.get_width() * info_scale)
            info_height = int(self.info_image.get_height() * info_scale)
            info_x = (screen_width - info_width) // 2
            info_y = (screen_height - info_height) // 2
            
            # position close button at top right of info image, lowered by 50px
            self.close_info_button.set_position(info_x + info_width - 80, info_y + 70)
    
    def start_game(self):
        """trigger new game start"""
        self.selected_option = MenuOption.NEW_GAME
        self.running = False
    
    def open_info(self):
        """display the information page"""
        self.show_info = True
        self.update_button_positions()
    
    def close_info(self):
        """hide the information page"""
        self.show_info = False
    
    def quit_game(self):
        """exit the game"""
        self.selected_option = MenuOption.QUIT
        self.running = False
    
    def update(self):
        """
        update menu state each frame
        recalculates parallax offsets based on mouse position
        updates button hover states
        """
        # update button positions if window size changed
        self.update_button_positions()
        
        # calculate parallax offset based on mouse position
        mouse_x, mouse_y = pg.mouse.get_pos()
        screen_width, screen_height = self.screen.get_size()
        
        # calculate normalized offset (-1 to 1)
        norm_x = (mouse_x / screen_width) - 0.5
        norm_y = (mouse_y / screen_height) - 0.5
        
        # limit movement to avoid seeing edges
        max_offset = 50  # maximum pixels of offset
        self.mouse_offset_x = norm_x * max_offset
        self.mouse_offset_y = norm_y * max_offset
        
        # update buttons
        if self.show_info:
            self.close_info_button.update(pg.mouse.get_pos())
        else:
            for button in self.buttons:
                button.update(pg.mouse.get_pos())
    
    def handle_event(self, event):
        """
        process input events from user
        handles button clicks and keyboard shortcuts
        """
        if self.show_info:
            # in info mode, only close button is active
            if self.close_info_button.handle_event(event):
                return True
            # close with escape or right click
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.close_info()
                return True
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                self.close_info()
                return True
        else:
            # handle clicks on menu buttons
            for button in self.buttons:
                if button.handle_event(event):
                    return True
        
        return False
    
    def draw(self):
        """
        render the complete menu scene
        draws parallax layers in reverse order (far to near)
        displays info screen or menu buttons depending on state
        """
        screen_width, screen_height = self.screen.get_size()
        
        # draw background parallax layers in REVERSE ORDER
        # files are named 01→11 (near→far)
        # but we display 11→01 (far→near) so near layers are on top
        for layer in reversed(self.background_layers):
            img = layer['image']
            offset_x = -self.mouse_offset_x * layer['parallax_factor'] * 10
            offset_y = -self.mouse_offset_y * layer['parallax_factor'] * 10
            
            # CENTER vertically to avoid seeing edges
            img_width, img_height = img.get_size()
            x = (screen_width - img_width) // 2 + offset_x
            y = (screen_height - img_height) // 2 + offset_y
            
            self.screen.blit(img, (x, y))
        
        # if displaying info page, dont draw title and buttons
        if self.show_info:
            # semi-transparent overlay
            overlay = pg.Surface((screen_width, screen_height))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            # display info image centered and scaled
            info_scale = min(screen_width * 0.8 / self.info_image.get_width(),
                           screen_height * 0.8 / self.info_image.get_height())
            info_width = int(self.info_image.get_width() * info_scale)
            info_height = int(self.info_image.get_height() * info_scale)
            info_scaled = pg.transform.scale(self.info_image, (info_width, info_height))
            info_x = (screen_width - info_width) // 2
            info_y = (screen_height - info_height) // 2
            
            self.screen.blit(info_scaled, (info_x, info_y))
            
            # draw close button
            self.close_info_button.draw(self.screen)
        else:
            # draw title parallax layers in REVERSE ORDER
            # so near layers (01, 02) are on top of far layers (05, 06)
            for layer in reversed(self.title_layers):
                img = layer['image']
                offset_x = -self.mouse_offset_x * layer['parallax_factor'] * 10
                offset_y = -self.mouse_offset_y * layer['parallax_factor'] * 10
                
                # center title at top of screen
                img_width, img_height = img.get_size()
                x = (screen_width - img_width) // 2 + offset_x
                y = screen_height // 8 + offset_y  # position in upper area of screen
                
                self.screen.blit(img, (x, y))
            
            # draw buttons
            for button in self.buttons:
                button.draw(self.screen)
    
    def run(self) -> MenuOption:
        """
        execute the main menu loop
        returns the selected menu option when user makes a choice
        handles window resizing and reloads background layers accordingly
        """
        clock = pg.time.Clock()
        
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.selected_option = MenuOption.QUIT
                    self.running = False
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    if not self.show_info:
                        self.selected_option = MenuOption.QUIT
                        self.running = False
                elif event.type == pg.VIDEORESIZE:
                    # reload layers with new size
                    self.screen = pg.display.get_surface()
                    self.background_layers.clear()
                    self.load_background_layers()
                
                self.handle_event(event)
            
            self.update()
            self.draw()
            pg.display.flip()
            clock.tick(60)
        
        return self.selected_option if self.selected_option else MenuOption.QUIT
