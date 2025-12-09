from __future__ import annotations
import pygame as pg
from enum import Enum
from typing import Callable, Optional, Tuple

from utils import *
from enclosure import *
from config import *


class ShopTab(Enum):
    """
    enum for different shop tabs available in the game
    enclosures - for building animal pens
    props - for decorative items and structures
    animals - for purchasing animals
    """
    ENCLOSURES = 0
    PROPS = 1
    ANIMALS = 2


class PlacementMode(Enum):
    """
    enum for different placement modes in the game
    controls what the player is currently doing with the mouse
    """
    NONE = 0  # default mode, no placement active
    ENCLOSURE = 1  # placing an enclosure
    PROP = 2  # placing a decorative prop
    ANIMAL = 3  # placing an animal in an enclosure
    BULLDOZER = 4  # destruction mode for removing items


class Button:
    """
    generic reusable button class with optional image support
    handles hover states, click events, and secondary text labels
    """
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 text: str = "", 
                 callback: Optional[Callable] = None,
                 image: Optional[pg.Surface] = None,
                 hover_image: Optional[pg.Surface] = None,
                 active_image: Optional[pg.Surface] = None,
                 font: Optional[pg.font.Font] = None,
                 text_color: Tuple[int, int, int] = (255, 255, 255),
                 bg_color: Optional[Tuple[int, int, int]] = None,
                 hover_color: Optional[Tuple[int, int, int]] = None,
                 active_color: Optional[Tuple[int, int, int]] = None,
                 visible: bool = True,
                 enabled: bool = True):
        """
        creates a generic button with customizable appearance and behavior
        
        args:
            x, y: button position on screen
            width, height: button dimensions
            text: text to display on button
            callback: function to call when button is clicked
            image: background image for button (optional)
            hover_image: image when mouse hovers over (optional)
            active_image: image when button is active (optional)
            font: font for text rendering
            text_color: color of the text
            bg_color: background color if no image provided
            hover_color: color when hovering
            active_color: color when button is active
            visible: whether button is visible initially
            enabled: whether button is enabled initially
        """
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.image = image
        self.hover_image = hover_image
        self.active_image = active_image
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color or (100, 100, 100)
        self.hover_color = hover_color or (150, 150, 150)
        self.active_color = active_color
        self.is_hovered = False
        self.is_active = False
        self.visible = visible
        self.enabled = enabled
        
        # secondary texts for displaying prices, etc
        self.secondary_texts = []
    
    def set_position(self, x: int, y: int):
        """change the button position"""
        self.rect.x = x
        self.rect.y = y
    
    def add_secondary_text(self, text: str, color: Tuple[int, int, int], offset_y: int = 0):
        """add a secondary text below the main text"""
        self.secondary_texts.append((text, color, offset_y))
    
    def clear_secondary_texts(self):
        """clear all secondary texts"""
        self.secondary_texts = []
    
    def handle_event(self, event) -> bool:
        """
        handle events for this button
        
        returns:
            true if button was clicked, false otherwise
        """
        if not self.visible or not self.enabled:
            return False
        
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()
                return True
        
        return False
    
    def update(self, mouse_pos: Tuple[int, int]):
        """update button state (hover, etc)"""
        if not self.visible:
            return
        
        self.is_hovered = self.rect.collidepoint(mouse_pos) and self.enabled
    
    def draw(self, screen: pg.Surface):
        """draw the button on screen"""
        if not self.visible:
            return
        
        # choose appropriate image based on state
        current_image = None
        if self.is_active and self.active_image:
            current_image = self.active_image
        elif self.is_hovered and self.hover_image:
            current_image = self.hover_image
        elif self.image:
            current_image = self.image
        
        # draw image or background
        if current_image:
            screen.blit(current_image, self.rect.topleft)
        else:
            # draw colored background
            if self.is_active and self.active_color:
                color = self.active_color
            elif self.is_hovered:
                color = self.hover_color
            else:
                color = self.bg_color
            
            pg.draw.rect(screen, color, self.rect)
            pg.draw.rect(screen, (255, 255, 255), self.rect, 2)
        
        # draw main text
        if self.text and self.font:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery - (len(self.secondary_texts) * 10)))
            screen.blit(text_surface, text_rect)
        
        # draw secondary texts
        for i, (sec_text, sec_color, offset_y) in enumerate(self.secondary_texts):
            if self.font:
                # adapt font size if text is too long
                sec_surface = self.font.render(sec_text, True, sec_color)
                
                # if text exceeds button width, use smaller font
                if sec_surface.get_width() > self.rect.width - 10:
                    # create smaller font (reduce by 20%)
                    smaller_font = pg.font.Font(self.font.get_fontpath() if hasattr(self.font, 'get_fontpath') else None, 
                                                int(self.font.get_height() * 0.6))
                    sec_surface = smaller_font.render(sec_text, True, sec_color)
                
                sec_rect = sec_surface.get_rect(center=(self.rect.centerx, self.rect.centery + 20 + (i * 15) + offset_y))
                screen.blit(sec_surface, sec_rect)


class ShopItem:
    """generic class for shop items in the store interface"""
    
    def __init__(self, x: int, y: int, width: int, height: int,
                 name: str, price: int, 
                 on_click: Optional[Callable] = None,
                 can_afford: bool = True,
                 info_text: str = ""):
        """
        create a shop item
        
        args:
            x, y: item position
            width, height: item dimensions
            name: item name
            price: item price
            on_click: function called on click
            can_afford: whether player can afford this item
            info_text: additional information text
        """
        self.rect = pg.Rect(x, y, width, height)
        self.name = name
        self.price = price
        self.on_click = on_click
        self.can_afford = can_afford
        self.info_text = info_text
    
    def handle_event(self, event) -> bool:
        """handle click on the item"""
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.can_afford:
                if self.on_click:
                    self.on_click()
                return True
        return False
    
    def draw(self, screen: pg.Surface, name_font: pg.font.Font, info_font: pg.font.Font):
        """draw the shop item"""
        # semi-transparent background
        item_surface = pg.Surface((self.rect.width, self.rect.height))
        item_surface.set_alpha(180)
        color = (80, 150, 80) if self.can_afford else (150, 80, 80)
        item_surface.fill(color)
        screen.blit(item_surface, self.rect.topleft)
        pg.draw.rect(screen, (200, 200, 150), self.rect, 2)
        
        # name
        name_text = name_font.render(self.name, True, (255, 255, 230))
        screen.blit(name_text, (self.rect.left + 15, self.rect.top + 8))
        
        # price
        price_text = name_font.render(f"${self.price}", True, (255, 215, 100))
        screen.blit(price_text, (self.rect.right - price_text.get_width() - 15, self.rect.top + 8))
        
        # info
        if self.info_text:
            info_surface = info_font.render(self.info_text, True, (230, 230, 200))
            screen.blit(info_surface, (self.rect.left + 15, self.rect.top + 35))


class HUD:
    """
    main hud class that manages all user interface elements
    handles shop, buttons, placement modes, and visual feedback
    """
    def __init__(self, game) -> None:
        self.game = game
        
        # load custom font
        font_path = "media/hud/font/soupofjustice.ttf"
        self.font = pg.font.Font(font_path, 36)
        self.small_font = pg.font.Font(font_path, 24)
        self.medium_font = pg.font.Font(font_path, 30)
        
        # load hud images
        self.shop_bg_img = pg.image.load("media/hud/backgrounds/shop.png").convert_alpha()
        btn_img_original = pg.image.load("media/hud/buttons/btn.png").convert_alpha()
        btn_hover_original = pg.image.load("media/hud/buttons/btn_hover.png").convert_alpha()
        btn_active_original = pg.image.load("media/hud/buttons/btn_activated.png").convert_alpha()
        
        # load new shop and bulldozer button images (text already included)
        shop_btn_img_original = pg.image.load("media/hud/buttons/shop.png").convert_alpha()
        shop_btn_hover_original = pg.image.load("media/hud/buttons/shop_hover.png").convert_alpha()
        shop_btn_active_original = pg.image.load("media/hud/buttons/shop_activated.png").convert_alpha()
        
        bulldozer_btn_img_original = pg.image.load("media/hud/buttons/buldozer.png").convert_alpha()
        bulldozer_btn_hover_original = pg.image.load("media/hud/buttons/buldozer_hover.png").convert_alpha()
        bulldozer_btn_active_original = pg.image.load("media/hud/buttons/buldozer_activated.png").convert_alpha()
        
        # load pause menu button images
        play_btn_img_original = pg.image.load("media/hud/buttons/play.png").convert_alpha()
        play_btn_hover_original = pg.image.load("media/hud/buttons/play_hover.png").convert_alpha()
        quit_btn_img_original = pg.image.load("media/hud/buttons/quit.png").convert_alpha()
        quit_btn_hover_original = pg.image.load("media/hud/buttons/quit_hover.png").convert_alpha()
        
        # load pause menu background
        self.pause_bg_img = pg.image.load("media/hud/backgrounds/pause.png").convert_alpha()
        
        # scale shop and bulldozer buttons to 110x110 (increased from 90)
        shop_btn_img = pg.transform.scale(shop_btn_img_original, (110, 110))
        shop_btn_hover = pg.transform.scale(shop_btn_hover_original, (110, 110))
        shop_btn_active = pg.transform.scale(shop_btn_active_original, (110, 110))
        
        bulldozer_btn_img = pg.transform.scale(bulldozer_btn_img_original, (110, 110))
        bulldozer_btn_hover = pg.transform.scale(bulldozer_btn_hover_original, (110, 110))
        bulldozer_btn_active = pg.transform.scale(bulldozer_btn_active_original, (110, 110))
        
        # scale pause menu buttons - squares like shop and bulldozer (110x110)
        play_btn_img = pg.transform.scale(play_btn_img_original, (110, 110))
        play_btn_hover = pg.transform.scale(play_btn_hover_original, (110, 110))
        quit_btn_img = pg.transform.scale(quit_btn_img_original, (110, 110))
        quit_btn_hover = pg.transform.scale(quit_btn_hover_original, (110, 110))
        
        # scale pause menu background (same scale as shop: 60%)
        original_pause_width, original_pause_height = self.pause_bg_img.get_size()
        pause_scale_factor = 0.6
        self.pause_width = int(original_pause_width * pause_scale_factor)
        self.pause_height = int(original_pause_height * pause_scale_factor)
        self.pause_bg_img = pg.transform.scale(self.pause_bg_img, (self.pause_width, self.pause_height))
        
        # load close button images with hover state
        close_img_original = pg.image.load("media/hud/buttons/close_2.png").convert_alpha()
        close_hover_original = pg.image.load("media/hud/buttons/close_2_hover.png").convert_alpha()
        minus_img_original = pg.image.load("media/hud/buttons/minus.png").convert_alpha()
        plus_img_original = pg.image.load("media/hud/buttons/plus.png").convert_alpha()
        
        # load mode screen images
        self.construction_mode_img_original = pg.image.load("media/hud/screen/construction_mode.png").convert_alpha()
        self.placement_mode_img_original = pg.image.load("media/hud/screen/placement_mode.png").convert_alpha()
        self.destruction_mode_img_original = pg.image.load("media/hud/screen/destruction_mode.png").convert_alpha()
        
        # resize mode screens (80% of screen width max)
        screen_width, screen_height = self.game.current_res
        mode_scale = min(screen_width * 0.8 / 1536, 1.0)  # 1536 is the original width
        mode_width = int(1536 * mode_scale)
        mode_height = int(331 * mode_scale)
        self.construction_mode_img = pg.transform.scale(self.construction_mode_img_original, (mode_width, mode_height))
        self.placement_mode_img = pg.transform.scale(self.placement_mode_img_original, (mode_width, mode_height))
        self.destruction_mode_img = pg.transform.scale(self.destruction_mode_img_original, (mode_width, mode_height))
        
        # shop dimensions based on image (increased from 50% to 60%)
        original_width, original_height = self.shop_bg_img.get_size()
        scale_factor = 0.6  # increased from 0.5
        self.shop_width = int(original_width * scale_factor)
        self.shop_height = int(original_height * scale_factor)
        self.shop_bg_img = pg.transform.scale(self.shop_bg_img, (self.shop_width, self.shop_height))
        
        # get prop and animal images from renderer (no need to load separately)
        # renderer already loads them in game.renderer
        
        # load enclosure image (use one of the custom enclosures)
        try:
            self.enclosure_image = pg.image.load("media/custom_enclosures/0.png").convert_alpha()
        except:
            self.enclosure_image = None
        
        # resize button images
        btn_img = pg.transform.scale(btn_img_original, (180, 60))
        btn_hover = pg.transform.scale(btn_hover_original, (180, 60))
        btn_active = pg.transform.scale(btn_active_original, (180, 60))
        close_img = pg.transform.scale(close_img_original, (60, 60))
        close_hover = pg.transform.scale(close_hover_original, (60, 60))
        small_button_size = 50
        minus_img = pg.transform.scale(minus_img_original, (small_button_size, small_button_size))
        plus_img = pg.transform.scale(plus_img_original, (small_button_size, small_button_size))
        
        # shop state
        self.shop_open = False
        self.current_tab = ShopTab.ENCLOSURES
        
        # placement mode
        self.placement_mode = PlacementMode.NONE
        self.selected_item = None
        self.enclosure_width = 3
        self.enclosure_height = 3
        self.hover_pos = None
        self.can_place = False
        
        # create generic buttons
        self.buttons = []
        
        # get screen dimensions for positioning
        screen_width, screen_height = self.game.current_res
        
        # shop button (using new shop button images with text already in them)
        # 110x110 - top right corner
        self.shop_button = Button(
            screen_width - 120, 10, 110, 110,  # top right corner
            text="",  # no text needed, it's in the image
            callback=self.toggle_shop,
            image=shop_btn_img,
            hover_image=shop_btn_hover,
            active_image=shop_btn_active,
            font=self.medium_font
        )
        self.buttons.append(self.shop_button)
        
        # bulldozer button (using new bulldozer button images with text already in them)
        # bottom right corner
        self.bulldozer_button = Button(
            screen_width - 120, screen_height - 120, 110, 110,  # bottom right corner
            text="",  # no text needed for main text, it's in the image
            callback=self.toggle_bulldozer,
            image=bulldozer_btn_img,
            hover_image=bulldozer_btn_hover,
            active_image=bulldozer_btn_active,
            font=self.small_font
        )
        # we'll update the price display dynamically - centered
        self.bulldozer_button.add_secondary_text(f"${BULLDOZER_BASE_COST}", (255, 215, 0), 10)  # y_offset=10 (lowered by 25)
        self.buttons.append(self.bulldozer_button)
        
        # speed buttons - bottom left, same line as zoom
        self.speed_minus_button = Button(
            10, screen_height - 60, small_button_size, small_button_size,
            callback=self.decrease_speed,
            image=minus_img
        )
        self.buttons.append(self.speed_minus_button)
        
        self.speed_plus_button = Button(
            70, screen_height - 60, small_button_size, small_button_size,
            callback=self.increase_speed,
            image=plus_img
        )
        self.buttons.append(self.speed_plus_button)
        
        # zoom buttons - bottom left, next to speed selector (shifted 50px right)
        # inverted: - to zoom out (increase), + to zoom in (decrease)
        self.zoom_minus_button = Button(
            330, screen_height - 60, small_button_size, small_button_size,
            callback=self.increase_zoom,  # - zooms out (increases tile_size)
            image=minus_img
        )
        self.buttons.append(self.zoom_minus_button)
        
        self.zoom_plus_button = Button(
            390, screen_height - 60, small_button_size, small_button_size,
            callback=self.decrease_zoom,  # + zooms in (decreases tile_size)
            image=plus_img
        )
        self.buttons.append(self.zoom_plus_button)
        
        # button to exit construction mode (cross, initially hidden)
        # position will be updated in update_shop_rects
        # lowered by 30px (from -40 to -10) and shifted 150px left (from -50 to -200)
        exit_btn_x = self.game.current_res[0] - 200 if hasattr(self.game, 'current_res') else 1200
        self.exit_mode_button = Button(
            exit_btn_x, -10, 60, 120,  # descended by 30px and moved left by 150px
            callback=self.exit_placement_mode,
            image=close_img,
            hover_image=close_hover,
            visible=False  # hidden by default
        )
        self.buttons.append(self.exit_mode_button)
        
        # images for shop buttons
        self.minus_img = minus_img
        self.plus_img = plus_img
        self.close_img = close_img
        self.close_hover = close_hover
        self.tab_btn_img = btn_img_original
        
        # store button images for shop items
        self.shop_item_btn_img = btn_img
        self.shop_item_btn_hover = btn_hover
        self.shop_item_btn_active = btn_active
        
        # initialize buttons and rectangles that will be created dynamicaly
        self.shop_close_button = None
        self.pause_play_button = None
        self.pause_quit_button = None
        self.pause_rect = None
        
        # rectangles will be calculated dynamically
        self.update_shop_rects()
        
        # buttons to adjust enclosure size
        self.enclosure_width_minus_rect = None
        self.enclosure_width_plus_rect = None
        self.enclosure_height_minus_rect = None
        self.enclosure_height_plus_rect = None
        
        # track hovered shop item
        self.hovered_shop_item_rect = None
        
        # track hovered tab
        self.hovered_tab = None
        
        # placement error message
        self.placement_error = ""
        
        # pause menu state
        self.pause_menu_open = False
        
        # store pause button images for later use
        self.play_btn_img = play_btn_img
        self.play_btn_hover = play_btn_hover
        self.quit_btn_img = quit_btn_img
        self.quit_btn_hover = quit_btn_hover
        
        # scroll system for shop
        self.scroll_offset = 0  # current scroll position (0 = top)
        self.max_visible_items = 4  # maximum items visible at once in shop
        self.virtual_total_slots = 50  # virtual slots for smooth scrolling
        self.scroll_dragging = False  # is user dragging the scrollbar
        self.scroll_drag_start_y = 0  # y position where drag started
        self.scroll_drag_start_offset = 0  # scroll offset when drag started
        
        # load scrollbar images
        scroll_bg_original = pg.image.load("media/hud/scrollbar/scroll_background.png").convert_alpha()
        scroll_cursor_original = pg.image.load("media/hud/scrollbar/scroll_cursor.png").convert_alpha()
        
        # scale scrollbar images - cursor is square (30x30)
        self.scroll_bg_img = pg.transform.scale(scroll_bg_original, (30, 400))
        self.scroll_cursor_img = pg.transform.scale(scroll_cursor_original, (30, 30))
        
        # scrollbar position (will be set in update_shop_rects)
        self.scroll_bar_rect = None
        self.scroll_cursor_rect = None
        
        # initialize pause menu rectangles
        self.update_pause_menu_rects()
    
    # button callbacks
    def toggle_shop(self):
        """open/close the shop"""
        self.shop_open = not self.shop_open
        if self.shop_open:
            self.placement_mode = PlacementMode.NONE
            self.bulldozer_button.is_active = False
            self.exit_mode_button.visible = False
        self.shop_button.is_active = self.shop_open
    
    def close_shop(self):
        """close the shop"""
        self.shop_open = False
        self.placement_mode = PlacementMode.NONE
        self.shop_button.is_active = False
    
    def toggle_bulldozer(self):
        """enable/disable bulldozer mode"""
        if self.placement_mode == PlacementMode.BULLDOZER:
            self.placement_mode = PlacementMode.NONE
            self.bulldozer_button.is_active = False
            self.exit_mode_button.visible = False
        else:
            self.placement_mode = PlacementMode.BULLDOZER
            self.shop_open = False
            self.shop_button.is_active = False
            self.bulldozer_button.is_active = True
            self.exit_mode_button.visible = True
    
    def exit_placement_mode(self):
        """exit placement/construction mode"""
        self.placement_mode = PlacementMode.NONE
        self.selected_item = None
        self.bulldozer_button.is_active = False
        self.exit_mode_button.visible = False
    
    def toggle_pause(self):
        """toggle pause menu"""
        self.pause_menu_open = not self.pause_menu_open
        if self.pause_menu_open:
            # close shop and exit placement mode
            self.shop_open = False
            self.shop_button.is_active = False
            self.placement_mode = PlacementMode.NONE
            self.bulldozer_button.is_active = False
            self.exit_mode_button.visible = False
    
    def resume_game(self):
        """resume game from pause"""
        self.pause_menu_open = False
    
    def quit_to_menu(self):
        """quit to main menu"""
        self.pause_menu_open = False
        self.game.return_to_menu()
    
    def get_total_items_for_tab(self):
        """get the total number of items for the current tab"""
        if self.current_tab == ShopTab.PROPS:
            return len(PROP_PRICES)
        elif self.current_tab == ShopTab.ANIMALS:
            return len(ANIMAL_PRICES)
        else:
            return 0  # enclosures tab doesn't have scrollable items
    
    def get_effective_scroll_range(self):
        """get the effective scroll range (uses virtual slots if items < 50)"""
        total_items = self.get_total_items_for_tab()
        if total_items == 0:
            return 0
        # if less than 50 items, use 50 virtual slots for smooth scrolling
        if total_items < self.virtual_total_slots:
            return self.virtual_total_slots - self.max_visible_items
        else:
            return total_items - self.max_visible_items
    
    def decrease_speed(self):
        """decrease player speed"""
        if self.game.player.speed <= 1:
            self.game.player.speed = 8
        else:
            self.game.player.speed -= 1
    
    def increase_speed(self):
        """increase player speed"""
        if self.game.player.speed >= 8:
            self.game.player.speed = 1
        else:
            self.game.player.speed += 1
    
    def decrease_zoom(self):
        """decrease zoom (increase tile_size) - powers of 2 (base 64=x1)"""
        # x0.25 (16), x0.5 (32), x1 (64), x2 (128), x4 (256)
        if self.game.tile_size >= 256:
            self.game.tile_size = 16
        elif self.game.tile_size >= 128:
            self.game.tile_size = 256
        elif self.game.tile_size >= 64:
            self.game.tile_size = 128
        elif self.game.tile_size >= 32:
            self.game.tile_size = 64
        else:
            self.game.tile_size = 32
        # reload renderer textures with new size
        self.game.renderer.load_tiles()
        self.game.renderer.load_props()
        self.game.renderer.load_enclosures()
        self.game.renderer.load_animals()
    
    def increase_zoom(self):
        """increase zoom (decrease tile_size) - powers of 2 (base 64=x1)"""
        # x0.25 (16), x0.5 (32), x1 (64), x2 (128), x4 (256)
        if self.game.tile_size <= 16:
            self.game.tile_size = 256
        elif self.game.tile_size <= 32:
            self.game.tile_size = 16
        elif self.game.tile_size <= 64:
            self.game.tile_size = 32
        elif self.game.tile_size <= 128:
            self.game.tile_size = 64
        else:
            self.game.tile_size = 128
        # reload renderer textures with new size
        self.game.renderer.load_tiles()
        self.game.renderer.load_props()
        self.game.renderer.load_enclosures()
        self.game.renderer.load_animals()
    
    def get_zoom_label(self):
        """return zoom label in format x0.25, x0.5, x1, x2, x4 (base=64 is x1)"""
        if self.game.tile_size <= 16:
            return "x0.25"
        elif self.game.tile_size <= 32:
            return "x0.5"
        elif self.game.tile_size <= 64:
            return "x1"
        elif self.game.tile_size <= 128:
            return "x2"
        else:
            return "x4"

    def handle_resize(self):
        """update all button positions when window is resized"""
        screen_width, screen_height = self.game.current_res
        small_button_size = 50
        
        # shop button - top right
        self.shop_button.set_position(screen_width - 120, 10)
        
        # bulldozer button - bottom right
        self.bulldozer_button.set_position(screen_width - 120, screen_height - 120)
        
        # speed buttons - bottom left
        self.speed_minus_button.set_position(10, screen_height - 60)
        self.speed_plus_button.set_position(70, screen_height - 60)
        
        # zoom buttons - bottom left, offset
        self.zoom_minus_button.set_position(330, screen_height - 60)
        self.zoom_plus_button.set_position(390, screen_height - 60)
        
        # resize construction mode images
        self.resize_mode_images()
        
        # reload renderer textures with new size
        self.game.renderer.load_tiles()
        self.game.renderer.load_props()
        self.game.renderer.load_enclosures()
        self.game.renderer.load_animals()
        
        # update shop rectangles and pause menu
        self.update_shop_rects()
        self.update_pause_menu_rects()
    
    def resize_mode_images(self):
        """resize construction mode images based on screen size"""
        screen_width, screen_height = self.game.current_res
        mode_scale = min(screen_width * 0.8 / 1536, 1.0)  # 1536 is the original width
        mode_width = int(1536 * mode_scale)
        mode_height = int(331 * mode_scale)
        self.construction_mode_img = pg.transform.scale(self.construction_mode_img_original, (mode_width, mode_height))
        self.placement_mode_img = pg.transform.scale(self.placement_mode_img_original, (mode_width, mode_height))
        self.destruction_mode_img = pg.transform.scale(self.destruction_mode_img_original, (mode_width, mode_height))

    def update_shop_rects(self):
        """update shop rectangles based on screen size"""
        screen_width, screen_height = self.game.current_res
        
        # update position and size of exit mode button
        # lowered by 30px (from -40 to -10) and shifted 150px left (from -50 to -200)
        if hasattr(self, 'exit_mode_button'):
            self.exit_mode_button.rect.width = 60
            self.exit_mode_button.rect.height = 120  # increased from 60
            self.exit_mode_button.set_position(screen_width - 200, -10)  # descended by 30px and moved left by 150px
        
        # center the shop
        shop_x = (screen_width - self.shop_width) // 2
        shop_y = (screen_height - self.shop_height) // 2
        
        self.shop_rect = pg.Rect(shop_x, shop_y, self.shop_width, self.shop_height)
        
        # tab buttons (relative to shop position)
        tab_y = shop_y + 190  # changed from 90 to 190 (moved down 100px)
        tab_width = 180
        tab_height = 50
        tab_spacing = 20
        total_tabs_width = 3 * tab_width + 2 * tab_spacing
        start_x = shop_x + (self.shop_width - total_tabs_width) // 2
        
        self.tab_buttons = {
            ShopTab.ENCLOSURES: pg.Rect(start_x, tab_y, tab_width, tab_height),
            ShopTab.PROPS: pg.Rect(start_x + tab_width + tab_spacing, tab_y, tab_width, tab_height),
            ShopTab.ANIMALS: pg.Rect(start_x + 2 * (tab_width + tab_spacing), tab_y, tab_width, tab_height)
        }
        
        # close button (top right) - moved down 100px
        close_size = 60
        self.close_button_rect = pg.Rect(shop_x + self.shop_width - close_size - 20, shop_y + 120, close_size, close_size)  # changed from shop_y + 20
        
        # create or update shop close button
        if self.shop_close_button is None:
            self.shop_close_button = Button(
                shop_x + self.shop_width - close_size - 20, shop_y + 120, close_size, close_size,
                callback=self.close_shop,
                image=self.close_img,
                hover_image=self.close_hover
            )
        else:
            self.shop_close_button.set_position(shop_x + self.shop_width - close_size - 20, shop_y + 120)
        
        # buttons to adjust enclosure size (in enclosures tab)
        content_y = shop_y + 280  # changed from 180 to 280
        button_size = 50
        
        # calculate centered positions for size selectors
        selector_width = self.shop_width - 230  # match item width (reduced by 60px)
        selector_start_x = shop_x + 115  # match item x position (increased by 30px)
        
        # each selector group (minus, value, plus) is about 140px wide
        selector_group_width = button_size + 140 + button_size  # minus + space + plus
        
        # width selector centered in left half
        width_center_x = selector_start_x + (selector_width // 4)
        width_minus_x = width_center_x - (selector_group_width // 2)
        
        # height selector centered in right half  
        height_center_x = selector_start_x + (3 * selector_width // 4)
        height_minus_x = height_center_x - (selector_group_width // 2)
        
        # width buttons (x) - centered
        self.enclosure_width_minus_rect = pg.Rect(width_minus_x, content_y + 100, button_size, button_size)
        self.enclosure_width_plus_rect = pg.Rect(width_minus_x + 140, content_y + 100, button_size, button_size)
        
        # height buttons (y) - centered
        self.enclosure_height_minus_rect = pg.Rect(height_minus_x, content_y + 100, button_size, button_size)
        self.enclosure_height_plus_rect = pg.Rect(height_minus_x + 140, content_y + 100, button_size, button_size)
        
        # initialize scrollbar position (will be drawn dynamically based on content)
        scrollbar_x = shop_x + self.shop_width - 112  # moved 3px right from -115
        scrollbar_y = content_y
        self.scroll_bar_rect = pg.Rect(scrollbar_x, scrollbar_y, 30, 400)
        self.scroll_cursor_rect = pg.Rect(scrollbar_x - 1, scrollbar_y, 30, 30)  # cursor 1px left (was -3, now -1 = 2px right)

    def update_pause_menu_rects(self):
        """update pause menu rectangles based on screen size"""
        screen_width, screen_height = self.game.current_res
        
        # center the pause menu
        pause_x = (screen_width - self.pause_width) // 2
        pause_y = (screen_height - self.pause_height) // 2
        
        self.pause_rect = pg.Rect(pause_x, pause_y, self.pause_width, self.pause_height)
        
        # square play and quit buttons (110x110) like shop and bulldozer
        button_size = 110
        button_spacing = 40
        
        # button positions (centered in pause menu and lowered by 70px + 150px = 220px total)
        total_button_width = 2 * button_size + button_spacing
        buttons_start_x = pause_x + (self.pause_width - total_button_width) // 2
        buttons_y = pause_y + (self.pause_height - button_size) // 2 + 220  # lowered by 220px total
        
        # play button - square (110x110)
        if self.pause_play_button is None:
            self.pause_play_button = Button(
                buttons_start_x, buttons_y, button_size, button_size,
                callback=self.resume_game,
                image=self.play_btn_img,
                hover_image=self.play_btn_hover
            )
        else:
            self.pause_play_button.set_position(buttons_start_x, buttons_y)
        
        # quit button - square (110x110)
        if self.pause_quit_button is None:
            self.pause_quit_button = Button(
                buttons_start_x + button_size + button_spacing, buttons_y, button_size, button_size,
                callback=self.quit_to_menu,
                image=self.quit_btn_img,
                hover_image=self.quit_btn_hover
            )
        else:
            self.pause_quit_button.set_position(buttons_start_x + button_size + button_spacing, buttons_y)

    def handle_event(self, event):
        """handle mouse and keyboard events for the hud"""
        # if pause menu is open, only pause menu buttons are active
        if self.pause_menu_open:
            if self.pause_play_button and self.pause_play_button.handle_event(event):
                return
            if self.pause_quit_button and self.pause_quit_button.handle_event(event):
                return
            return  # block all other events during pause
        
        # handle generic buttons first
        for button in self.buttons:
            if button.handle_event(event):
                return  # a button was clicked, stop processing
        
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            
            # if shop is open
            if self.shop_open:
                # click on close button
                if self.shop_close_button and self.shop_close_button.handle_event(event):
                    return
                
                # click on tabs
                for tab, rect in self.tab_buttons.items():
                    if rect.collidepoint(mouse_pos):
                        self.current_tab = tab
                        self.scroll_offset = 0  # reset scroll when changing tabs
                        return
                
                # click on scrollbar cursor (for drag & drop)
                if self.scroll_cursor_rect and self.scroll_cursor_rect.collidepoint(mouse_pos):
                    if self.current_tab in [ShopTab.PROPS, ShopTab.ANIMALS]:
                        self.scroll_dragging = True
                        self.scroll_drag_start_y = mouse_pos[1]
                        self.scroll_drag_start_offset = self.scroll_offset
                        return
                
                # click on enclosure size buttons (enclosures tab)
                if self.current_tab == ShopTab.ENCLOSURES:
                    if self.enclosure_width_minus_rect.collidepoint(mouse_pos):
                        self.enclosure_width = max(3, self.enclosure_width - 1)
                        return
                    elif self.enclosure_width_plus_rect.collidepoint(mouse_pos):
                        self.enclosure_width = min(15, self.enclosure_width + 1)
                        return
                    elif self.enclosure_height_minus_rect.collidepoint(mouse_pos):
                        self.enclosure_height = max(3, self.enclosure_height - 1)
                        return
                    elif self.enclosure_height_plus_rect.collidepoint(mouse_pos):
                        self.enclosure_height = min(15, self.enclosure_height + 1)
                        return
                
                # click on shop items
                self.handle_shop_click(mouse_pos)
            
            # placement mode active - place object
            elif self.placement_mode != PlacementMode.NONE:
                if self.placement_mode == PlacementMode.BULLDOZER:
                    # bulldozer mode - remove object
                    self.bulldoze_item()
                elif self.can_place and self.hover_pos:
                    self.place_item()
        
        # cancel placement with right click
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            if self.placement_mode != PlacementMode.NONE:
                self.exit_placement_mode()
        
        # mouse button up - stop scrollbar dragging
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.scroll_dragging = False
        
        # mouse motion - handle scrollbar dragging
        elif event.type == pg.MOUSEMOTION:
            if self.scroll_dragging and self.scroll_bar_rect:
                # calculate scroll offset based on cursor position
                mouse_y = event.pos[1]
                delta_y = mouse_y - self.scroll_drag_start_y
                
                # calculate how much scrollbar area is available
                scrollable_height = self.scroll_bar_rect.height - self.scroll_cursor_img.get_height()
                
                # get effective scroll range (uses virtual slots)
                max_scroll = max(0, self.get_effective_scroll_range())
                
                # convert pixel delta to scroll offset
                if scrollable_height > 0 and max_scroll > 0:
                    scroll_per_pixel = max_scroll / scrollable_height
                    new_offset = self.scroll_drag_start_offset + (delta_y * scroll_per_pixel)
                    self.scroll_offset = max(0, min(max_scroll, new_offset))
        
        # mouse wheel - scroll items in shop
        elif event.type == pg.MOUSEWHEEL:
            if self.shop_open and self.current_tab in [ShopTab.PROPS, ShopTab.ANIMALS]:
                # scroll in shop (uses virtual slots for smooth scrolling)
                max_scroll = max(0, self.get_effective_scroll_range())
                self.scroll_offset = max(0, min(max_scroll, self.scroll_offset - event.y))
            elif self.placement_mode == PlacementMode.ENCLOSURE:
                # change enclosure size with mouse wheel
                if pg.key.get_mods() & pg.KMOD_SHIFT:
                    self.enclosure_height = max(3, min(10, self.enclosure_height + event.y))
                else:
                    self.enclosure_width = max(3, min(10, self.enclosure_width + event.y))

    def handle_shop_click(self, mouse_pos):
        """handle clicks in the shop"""
        # shop content area (relative to shop_rect) - must match draw_shop_content
        content_y = self.shop_rect.y + 280  # changed from 180 to 280 (moved down 100px)
        item_height = 70  # increased from 45
        item_spacing = 15  # reduced from 20
        
        if self.current_tab == ShopTab.ENCLOSURES:
            # select an enclosure to place
            enclosure_rect = pg.Rect(self.shop_rect.x + 115, content_y, self.shop_width - 230, item_height)  # reduced width by 60px
            if enclosure_rect.collidepoint(mouse_pos):
                price = self.calculate_enclosure_price()
                if self.game.money >= price:
                    self.placement_mode = PlacementMode.ENCLOSURE
                    self.shop_open = False
                    self.shop_button.is_active = False
                    self.exit_mode_button.visible = True
        
        elif self.current_tab == ShopTab.PROPS:
            # props list with scroll
            y_offset = content_y
            
            # calculate actual start index using virtual scrolling (same as draw_shop_content)
            total_items = len(PROP_PRICES)
            if total_items < self.virtual_total_slots:
                max_virtual_scroll = self.virtual_total_slots - self.max_visible_items
                if max_virtual_scroll > 0:
                    scroll_ratio = min(1.0, self.scroll_offset / max_virtual_scroll)
                    actual_start_index = scroll_ratio * (self.virtual_total_slots - self.max_visible_items)
                else:
                    actual_start_index = 0
            else:
                actual_start_index = self.scroll_offset
            
            items_drawn = 0
            for i, (prop_name, data) in enumerate(PROP_PRICES.items()):
                # skip items before scroll offset
                if i < int(actual_start_index):
                    continue
                # stop after max visible items
                if items_drawn >= self.max_visible_items:
                    break
                
                # calculate position for this visible item
                item_y = y_offset + items_drawn * (item_height + item_spacing)
                
                prop_rect = pg.Rect(self.shop_rect.x + 115, item_y, self.shop_width - 230, item_height)
                if prop_rect.collidepoint(mouse_pos):
                    if self.game.money >= data["price"]:
                        self.placement_mode = PlacementMode.PROP
                        self.selected_item = prop_name
                        self.shop_open = False
                        self.shop_button.is_active = False
                        self.exit_mode_button.visible = True
                        return
                
                items_drawn += 1
        
        elif self.current_tab == ShopTab.ANIMALS:
            # animals list with scroll
            y_offset = content_y
            
            # calculate actual start index using virtual scrolling (same as draw_shop_content)
            total_items = len(ANIMAL_PRICES)
            if total_items < self.virtual_total_slots:
                max_virtual_scroll = self.virtual_total_slots - self.max_visible_items
                if max_virtual_scroll > 0:
                    scroll_ratio = min(1.0, self.scroll_offset / max_virtual_scroll)
                    actual_start_index = scroll_ratio * (self.virtual_total_slots - self.max_visible_items)
                else:
                    actual_start_index = 0
            else:
                actual_start_index = self.scroll_offset
            
            items_drawn = 0
            for i, (animal_name, data) in enumerate(ANIMAL_PRICES.items()):
                # skip items before scroll offset
                if i < int(actual_start_index):
                    continue
                # stop after max visible items
                if items_drawn >= self.max_visible_items:
                    break
                
                # calculate position for this visible item
                item_y = y_offset + items_drawn * (item_height + item_spacing)
                
                animal_rect = pg.Rect(self.shop_rect.x + 115, item_y, self.shop_width - 230, item_height)
                if animal_rect.collidepoint(mouse_pos):
                    if self.game.money >= data["price"]:
                        self.placement_mode = PlacementMode.ANIMAL
                        self.selected_item = animal_name
                        self.shop_open = False
                        self.shop_button.is_active = False
                        self.exit_mode_button.visible = True
                        return
                
                items_drawn += 1

    def update(self):
        """update hud state"""
        # update shop rectangles if window was resized
        self.update_shop_rects()
        self.update_pause_menu_rects()
        
        # if pause menu is open, only update pause menu buttons
        if self.pause_menu_open:
            mouse_pos = pg.mouse.get_pos()
            if self.pause_play_button:
                self.pause_play_button.update(mouse_pos)
            if self.pause_quit_button:
                self.pause_quit_button.update(mouse_pos)
            return  # dont update rest of hud while paused
        
        # update buttons (hover, etc)
        mouse_pos = pg.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)
        
        # update bulldozer button price display dynamically
        bulldozer_cost = self.calculate_bulldozer_cost()
        self.bulldozer_button.clear_secondary_texts()
        self.bulldozer_button.add_secondary_text(f"${bulldozer_cost}", (255, 215, 0), 10)  # lowered by 25 total
        
        # update shop close button if shop is open
        if self.shop_open and self.shop_close_button:
            self.shop_close_button.update(mouse_pos)
        
        # track hovered shop item
        self.hovered_shop_item_rect = None
        self.hovered_tab = None
        if self.shop_open:
            self.update_shop_item_hover(mouse_pos)
            self.update_tab_hover(mouse_pos)
        
        if self.placement_mode != PlacementMode.NONE:
            # get mouse position in world coordinates
            world_x = mouse_pos[0] + self.game.camera.x
            world_y = mouse_pos[1] + self.game.camera.y
            tile_x = int(world_x // self.game.tile_size)
            tile_y = int(world_y // self.game.tile_size)
            
            self.hover_pos = (tile_x, tile_y)
            
            # check if we can place the object
            if self.placement_mode == PlacementMode.ENCLOSURE:
                self.can_place = self.check_enclosure_placement(tile_x, tile_y)
            elif self.placement_mode == PlacementMode.PROP:
                self.can_place = self.check_prop_placement(tile_x, tile_y)
            elif self.placement_mode == PlacementMode.ANIMAL:
                self.can_place = self.check_animal_placement(tile_x, tile_y)
            elif self.placement_mode == PlacementMode.BULLDOZER:
                self.can_place = self.check_bulldozer_target(tile_x, tile_y)

    def update_shop_item_hover(self, mouse_pos):
        """update which shop item is being hovered"""
        content_y = self.shop_rect.y + 280  # changed from 180 to 280
        item_height = 70  # increased from 45
        item_spacing = 15
        
        if self.current_tab == ShopTab.ENCLOSURES:
            enclosure_rect = pg.Rect(self.shop_rect.x + 115, content_y, self.shop_width - 230, item_height)  # reduced width by 60px
            if enclosure_rect.collidepoint(mouse_pos):
                self.hovered_shop_item_rect = enclosure_rect
        
        elif self.current_tab == ShopTab.PROPS:
            y_offset = content_y
            for prop_name, data in PROP_PRICES.items():
                prop_rect = pg.Rect(self.shop_rect.x + 115, y_offset, self.shop_width - 230, item_height)  # reduced width by 60px
                if prop_rect.collidepoint(mouse_pos):
                    self.hovered_shop_item_rect = prop_rect
                    break
                y_offset += item_height + item_spacing
        
        elif self.current_tab == ShopTab.ANIMALS:
            y_offset = content_y
            for animal_name, data in ANIMAL_PRICES.items():
                animal_rect = pg.Rect(self.shop_rect.x + 115, y_offset, self.shop_width - 230, item_height)  # reduced width by 60px
                if animal_rect.collidepoint(mouse_pos):
                    self.hovered_shop_item_rect = animal_rect
                    break
                y_offset += item_height + item_spacing

    def update_tab_hover(self, mouse_pos):
        """update which tab is being hovered"""
        self.hovered_tab = None
        for tab, rect in self.tab_buttons.items():
            if rect.collidepoint(mouse_pos):
                self.hovered_tab = tab
                break

    def check_enclosure_placement(self, x, y):
        """check if we can place an enclosure at this position"""
        # verify that all tiles are free (no prop and no existing enclosure)
        for i in range(self.enclosure_width):
            for j in range(self.enclosure_height):
                tile = self.game.map.get_tile(x + i, y + j)
                if not tile:
                    self.placement_error = "Out of bounds"
                    return False
                if tile.prop:
                    self.placement_error = "Area occupied by prop"
                    return False
                if tile.is_enclosure:
                    self.placement_error = "Area occupied by enclosure"
                    return False
        self.placement_error = ""
        return True

    def check_prop_placement(self, x, y):
        """check if we can place a prop at this position"""
        if not self.selected_item:
            self.placement_error = "No item selected"
            return False
        
        size = PROPS_SIZES.get(self.selected_item, (1, 1))
        for i in range(int(size[0])):
            for j in range(int(size[1])):
                tile = self.game.map.get_tile(x + i, y + j)
                if not tile:
                    self.placement_error = "Out of bounds"
                    return False
                # cant place on existing prop or enclosure
                if tile.prop:
                    self.placement_error = "Area occupied by prop"
                    return False
                if tile.is_enclosure:
                    self.placement_error = "Area occupied by enclosure"
                    return False
        self.placement_error = ""
        return True

    def check_animal_placement(self, x, y):
        """check if we can place an animal at this position (in an enclosure)"""
        tile = self.game.map.get_tile(x, y)
        if not tile:
            self.placement_error = "Out of bounds"
            return False
        if not tile.is_enclosure:
            self.placement_error = "Not an enclosure"
            return False
        if not tile.prop:
            self.placement_error = "No enclosure found"
            return False
        
        # enclosure is directly in tile.prop
        enclosure = tile.prop
        # check if enclosure isnt full
        if len(enclosure.animals) >= enclosure.max_animals:
            self.placement_error = "Enclosure is full"
            return False
        
        self.placement_error = ""
        return True
    
    def check_bulldozer_target(self, x, y):
        """check if there's something to destroy at this position"""
        tile = self.game.map.get_tile(x, y)
        if not tile:
            self.placement_error = "Out of bounds"
            return False
        if not tile.prop:
            self.placement_error = "Nothing to destroy"
            return False
        
        # we can destroy if we have enough money
        bulldozer_cost = self.calculate_bulldozer_cost()
        if self.game.money < bulldozer_cost:
            self.placement_error = f"Not enough money (${bulldozer_cost} needed)"
            return False
        
        self.placement_error = ""
        return True

    def place_item(self):
        """place the selected object"""
        if not self.hover_pos:
            return
        
        x, y = self.hover_pos
        
        if self.placement_mode == PlacementMode.ENCLOSURE:
            price = self.calculate_enclosure_price()
            if self.game.money >= price:
                self.game.map.create_enclosure(x, y, self.enclosure_width, self.enclosure_height)
                self.game.money -= price
                self.exit_placement_mode()  # use function to properly clean up
        
        elif self.placement_mode == PlacementMode.PROP and self.selected_item:
            price = PROP_PRICES[self.selected_item]['price']
            if self.game.money >= price:
                self.game.map.create_prop(self.selected_item, x, y)
                self.game.money -= price
                self.exit_placement_mode()  # use function to properly clean up
        
        elif self.placement_mode == PlacementMode.ANIMAL and self.selected_item:
            price = ANIMAL_PRICES[self.selected_item]["price"]
            if self.game.money >= price:
                # enclosure is directly in tile.prop
                tile = self.game.map.get_tile(x, y)
                if tile and tile.is_enclosure and tile.prop:
                    enclosure = tile.prop
                    animal = Animal(self.selected_item, x + 0.5, y + 0.5)
                    enclosure.add_animal(animal)
                    self.game.money -= price
                    self.exit_placement_mode()  # use function to properly clean up

    def bulldoze_item(self):
        """destroy a prop or enclosure"""
        if not self.hover_pos:
            return
        
        x, y = self.hover_pos
        tile = self.game.map.get_tile(x, y)
        
        if not tile or not tile.prop:
            return
        
        # check we have enough money
        bulldozer_cost = self.calculate_bulldozer_cost()
        if self.game.money < bulldozer_cost:
            return
        
        prop = tile.prop
        
        # if its an enclosure
        if prop.is_enclosure:
            # remove all animals from the enclosure
            if hasattr(prop, 'animals'):
                prop.animals.clear()
            
            # delete all enclosure tiles
            for i in range(prop.width):
                for j in range(prop.height):
                    t = self.game.map.get_tile(prop.x + i, prop.y + j)
                    if t:
                        t.prop = None
                        t.is_enclosure = False
                        t.enclosure_type = None
                        t.main_prop_tile = False
            
            # remove from enclosure list
            if prop in self.game.map.enclosures:
                self.game.map.enclosures.remove(prop)
        else:
            # if its a normal prop
            self.game.map.remove_prop(prop)
        
        # deduct cost
        bulldozer_cost = self.calculate_bulldozer_cost()
        self.game.money -= bulldozer_cost

    def calculate_bulldozer_cost(self):
        """calculate bulldozer cost based on income per second"""
        if hasattr(self.game, 'income_per_second') and self.game.income_per_second > 0:
            return max(BULLDOZER_BASE_COST, int(min(self.game.income_per_second * 30, BULLDOZER_MAX_COST)))
        return BULLDOZER_BASE_COST

    def calculate_enclosure_price(self):
        """calculate enclosure price based on its size"""
        return ENCLOSURE_BASE_PRICE + (self.enclosure_width * self.enclosure_height * ENCLOSURE_COST_PER_TILE)

    def draw(self):
        """draw the hud"""
        screen_width, screen_height = self.game.current_res
        
        # if pause menu is open, only display pause menu
        if self.pause_menu_open:
            self.draw_pause_menu()
            return
        
        # display money in top left
        money_text = self.font.render(f"${int(self.game.money)}", True, (255, 215, 0))
        self.game.screen.blit(money_text, (10, 10))
        
        # display income per second in top left
        if hasattr(self.game, 'income_per_second'):
            income_text = self.small_font.render(f"+${self.game.income_per_second:.1f}/s", True, (100, 255, 100))
            self.game.screen.blit(income_text, (10, 50))
        
        # draw all generic buttons (except exit_mode_button which will be drawn after)
        for button in self.buttons:
            if button != self.exit_mode_button:
                button.draw(self.game.screen)
        
        # display current speed - next to buttons in bottom left
        speed_text = self.small_font.render(f"Camera Speed: {self.game.player.speed}", True, (255, 255, 255))
        self.game.screen.blit(speed_text, (130, screen_height - 45))
        
        # display current zoom - next to buttons in bottom left
        zoom_label = self.get_zoom_label()
        zoom_text = self.small_font.render(f"Zoom: {zoom_label}", True, (255, 255, 255))
        self.game.screen.blit(zoom_text, (450, screen_height - 45))
        
        # display mode screen if in placement mode
        if self.placement_mode != PlacementMode.NONE and not self.shop_open:
            self.draw_mode_screen()
        
        # draw exit_mode button after mode sprites so its on top
        if hasattr(self, 'exit_mode_button'):
            self.exit_mode_button.draw(self.game.screen)
        
        # draw shop if open
        if self.shop_open:
            self.draw_shop()
        
        # draw placement hover
        if self.placement_mode != PlacementMode.NONE and self.hover_pos:
            self.draw_placement_hover()
            
            # display error message if placement is not valid
            if not self.can_place and self.placement_error:
                screen_width = self.game.current_res[0]
                error_text = self.medium_font.render(self.placement_error, True, (255, 50, 50))
                error_rect = error_text.get_rect(center=(screen_width // 2, 70))  # moved down from 50 to 70
                
                # no background, just transparent red text
                self.game.screen.blit(error_text, error_rect)
    
    def draw_mode_screen(self):
        """draw screen corresponding to current mode"""
        screen_width, screen_height = self.game.current_res
        
        # choose appropriate image
        mode_img = None
        if self.placement_mode == PlacementMode.ENCLOSURE or self.placement_mode == PlacementMode.PROP:
            mode_img = self.construction_mode_img
        elif self.placement_mode == PlacementMode.ANIMAL:
            mode_img = self.placement_mode_img
        elif self.placement_mode == PlacementMode.BULLDOZER:
            mode_img = self.destruction_mode_img
        
        if mode_img:
            # center image at top of screen
            img_width = mode_img.get_width()
            x = (screen_width - img_width) // 2
            y = 0
            self.game.screen.blit(mode_img, (x, y))

    def draw_shop(self):
        """draw the shop window"""
        # shop background with image (no border)
        self.game.screen.blit(self.shop_bg_img, self.shop_rect.topleft)
        
        # close button with hover
        if self.shop_close_button:
            self.shop_close_button.draw(self.game.screen)
        
        # tabs with button images
        for tab, rect in self.tab_buttons.items():
            # choose the appropriate button image based on state
            if tab == self.current_tab:
                # active state - use activated image
                tab_img = pg.transform.scale(self.shop_item_btn_active, (rect.width, rect.height))
            elif tab == self.hovered_tab:
                # hover state - use hover image
                tab_img = pg.transform.scale(self.shop_item_btn_hover, (rect.width, rect.height))
            else:
                # normal state - use normal image
                tab_img = pg.transform.scale(self.shop_item_btn_img, (rect.width, rect.height))
            
            self.game.screen.blit(tab_img, rect.topleft)
            
            tab_names = {
                ShopTab.ENCLOSURES: "ENCLOS",  # translated from "ENCLOS"
                ShopTab.PROPS: "PROPS",
                ShopTab.ANIMALS: "ANIMALS"  # translated from "ANIMAUX"
            }
            tab_text = self.medium_font.render(tab_names[tab], True, (255, 255, 255))
            text_rect = tab_text.get_rect(center=rect.center)
            self.game.screen.blit(tab_text, text_rect)
        
        # tab content
        self.draw_shop_content()

    def draw_shop_content(self):
        """draw current tab content"""
        content_y = self.shop_rect.y + 280  # changed from 180 to 280 (moved down 100px)
        item_height = 70  # increased from 45
        item_spacing = 15  # reduced from 20
        
        if self.current_tab == ShopTab.ENCLOSURES:
            # enclosures
            price = self.calculate_enclosure_price()
            item_rect = pg.Rect(self.shop_rect.x + 115, content_y, self.shop_width - 230, item_height)  # reduced width by 60px
            
            # draw solid color background
            item_surface = pg.Surface((item_rect.width, item_rect.height))
            item_surface.set_alpha(180)
            color = (80, 150, 80) if self.game.money >= price else (150, 80, 80)
            item_surface.fill(color)
            self.game.screen.blit(item_surface, item_rect.topleft)
            pg.draw.rect(self.game.screen, (200, 200, 150), item_rect, 2)
            
            # draw enclosure image preview
            image_size = 60  # increased from 40
            if self.enclosure_image:
                enc_img = pg.transform.scale(self.enclosure_image, (image_size, image_size))
                self.game.screen.blit(enc_img, (item_rect.left + 5, item_rect.top + (item_height - image_size) // 2))
            
            # text (offset to make room for image)
            text_offset = image_size + 15
            name_text = self.medium_font.render(f"Enclosure {self.enclosure_width}x{self.enclosure_height}", True, (255, 255, 230))
            price_text = self.medium_font.render(f"${price}", True, (255, 215, 100))
            info_text = self.small_font.render("Click to buy and place", True, (230, 230, 200))
            
            self.game.screen.blit(name_text, (item_rect.left + text_offset, item_rect.top + 10))
            self.game.screen.blit(price_text, (item_rect.right - price_text.get_width() - 15, item_rect.top + 10))
            self.game.screen.blit(info_text, (item_rect.left + text_offset, item_rect.top + 40))  # more spacing  # adjusted from 35
            
            # size controls
            controls_y = content_y + 100  # moved down from 80
            
            # calculate center position for the entire size selector
            selector_width = self.shop_width - 230  # match item width (reduced by 60px)
            selector_start_x = self.shop_rect.x + 115  # match item x position (increased by 30px)
            
            # width (x) - label on the left, shifted 100px right
            width_label = self.medium_font.render("Width:", True, (0, 0, 0))  # changed to black
            width_label_x = self.enclosure_width_minus_rect.left - width_label.get_width() - 10 + 100
            self.game.screen.blit(width_label, (width_label_x, controls_y - 30))
            
            # button - with image
            self.game.screen.blit(self.minus_img, self.enclosure_width_minus_rect.topleft)
            
            # value
            width_value = self.font.render(f"{self.enclosure_width}", True, (0, 0, 0))  # changed to black
            width_value_x = (self.enclosure_width_minus_rect.right + self.enclosure_width_plus_rect.left) // 2
            width_value_rect = width_value.get_rect(center=(width_value_x, self.enclosure_width_minus_rect.centery))
            self.game.screen.blit(width_value, width_value_rect)
            
            # button + with image
            self.game.screen.blit(self.plus_img, self.enclosure_width_plus_rect.topleft)
            
            # height (y) - label on the left, shifted 100px right
            height_label = self.medium_font.render("Height:", True, (0, 0, 0))  # changed to black
            height_label_x = self.enclosure_height_minus_rect.left - height_label.get_width() - 10 + 100
            self.game.screen.blit(height_label, (height_label_x, controls_y - 30))
            
            # button - with image
            self.game.screen.blit(self.minus_img, self.enclosure_height_minus_rect.topleft)
            
            # value
            height_value = self.font.render(f"{self.enclosure_height}", True, (0, 0, 0))  # changed to black
            height_value_x = (self.enclosure_height_minus_rect.right + self.enclosure_height_plus_rect.left) // 2
            height_value_rect = height_value.get_rect(center=(height_value_x, self.enclosure_height_minus_rect.centery))
            self.game.screen.blit(height_value, height_value_rect)
            
            # button + with image
            self.game.screen.blit(self.plus_img, self.enclosure_height_plus_rect.topleft)
        
        elif self.current_tab == ShopTab.PROPS:
            y_offset = content_y
            
            # calculate actual start index using virtual scrolling
            total_items = len(PROP_PRICES)
            if total_items < self.virtual_total_slots:
                # use virtual slots for smooth scrolling with empty space at bottom
                # map scroll_offset (0 to 46 for 50 slots) to allow scrolling past items
                max_virtual_scroll = self.virtual_total_slots - self.max_visible_items  # 46 for 50 slots
                if max_virtual_scroll > 0:
                    # normalize scroll position (0.0 to 1.0)
                    scroll_ratio = min(1.0, self.scroll_offset / max_virtual_scroll)
                    # allow scrolling to show empty space - go beyond total_items
                    # with 8 items and 50 virtual slots, we can scroll much further
                    actual_start_index = scroll_ratio * (self.virtual_total_slots - self.max_visible_items)
                else:
                    actual_start_index = 0
            else:
                actual_start_index = self.scroll_offset
            
            # draw only visible items based on scroll
            items_drawn = 0
            for i, (prop_name, data) in enumerate(PROP_PRICES.items()):
                # skip items before scroll offset (using float comparison for smooth scroll)
                if i < int(actual_start_index):
                    continue
                # stop rendering after max visible items or if we've drawn enough
                if items_drawn >= self.max_visible_items:
                    break
                
                # calculate position for this visible item
                item_y = y_offset + items_drawn * (item_height + item_spacing)
                
                item_rect = pg.Rect(self.shop_rect.x + 115, item_y, self.shop_width - 230, item_height)
                
                price = data["price"]
                income = data["income"]
                
                # draw solid color background
                item_surface = pg.Surface((item_rect.width, item_rect.height))
                item_surface.set_alpha(180)
                color = (80, 150, 80) if self.game.money >= price else (150, 80, 80)
                item_surface.fill(color)
                self.game.screen.blit(item_surface, item_rect.topleft)
                pg.draw.rect(self.game.screen, (200, 200, 150), item_rect, 2)
                
                # draw prop image preview
                image_size = 60  # increased from 40
                prop_img = self.game.renderer.get_prop_texture(prop_name)
                if prop_img:
                    prop_img_scaled = pg.transform.scale(prop_img, (image_size, image_size))
                    self.game.screen.blit(prop_img_scaled, (item_rect.left + 5, item_rect.top + (item_height - image_size) // 2))
                
                # text (offset to make room for image)
                text_offset = image_size + 15
                name_text = self.medium_font.render(prop_name.capitalize(), True, (255, 255, 230))
                price_text = self.medium_font.render(f"${price}", True, (255, 215, 100))
                size = PROPS_SIZES.get(prop_name, (1, 1))
                income_text = self.small_font.render(f"+${income}/s | Size: {int(size[0])}x{int(size[1])}", True, (230, 230, 200))
                
                self.game.screen.blit(name_text, (item_rect.left + text_offset, item_rect.top + 10))
                self.game.screen.blit(price_text, (item_rect.right - price_text.get_width() - 15, item_rect.top + 10))
                self.game.screen.blit(income_text, (item_rect.left + text_offset, item_rect.top + 40))  # shows income + size
                
                items_drawn += 1
            
            # draw scrollbar
            self.draw_scrollbar()
        
        elif self.current_tab == ShopTab.ANIMALS:
            y_offset = content_y
            
            # calculate actual start index using virtual scrolling
            total_items = len(ANIMAL_PRICES)
            if total_items < self.virtual_total_slots:
                # use virtual slots for smooth scrolling with empty space at bottom
                # map scroll_offset (0 to 46 for 50 slots) to allow scrolling past items
                max_virtual_scroll = self.virtual_total_slots - self.max_visible_items  # 46 for 50 slots
                if max_virtual_scroll > 0:
                    # normalize scroll position (0.0 to 1.0)
                    scroll_ratio = min(1.0, self.scroll_offset / max_virtual_scroll)
                    # allow scrolling to show empty space - go beyond total_items
                    # with 8 items and 50 virtual slots, we can scroll much further
                    actual_start_index = scroll_ratio * (self.virtual_total_slots - self.max_visible_items)
                else:
                    actual_start_index = 0
            else:
                actual_start_index = self.scroll_offset
            
            # draw only visible items based on scroll
            items_drawn = 0
            for i, (animal_name, data) in enumerate(ANIMAL_PRICES.items()):
                # skip items before scroll offset (using float comparison for smooth scroll)
                if i < int(actual_start_index):
                    continue
                # stop rendering after max visible items or if we've drawn enough
                if items_drawn >= self.max_visible_items:
                    break
                
                # calculate position for this visible item
                item_y = y_offset + items_drawn * (item_height + item_spacing)
                
                item_rect = pg.Rect(self.shop_rect.x + 115, item_y, self.shop_width - 230, item_height)
                
                # draw solid color background
                item_surface = pg.Surface((item_rect.width, item_rect.height))
                item_surface.set_alpha(180)
                color = (80, 150, 80) if self.game.money >= data['price'] else (150, 80, 80)
                item_surface.fill(color)
                self.game.screen.blit(item_surface, item_rect.topleft)
                pg.draw.rect(self.game.screen, (200, 200, 150), item_rect, 2)
                
                # draw animal image preview
                image_size = 60  # increased from 40
                # get first frame of idle south animation from renderer
                animal_img = self.game.renderer.get_animal_frame(animal_name, 'idle', Direction.SOUTH, 0)
                if animal_img:
                    animal_img_scaled = pg.transform.scale(animal_img, (image_size, image_size))
                    self.game.screen.blit(animal_img_scaled, (item_rect.left + 5, item_rect.top + (item_height - image_size) // 2))
                
                # text (offset to make room for image)
                text_offset = image_size + 15
                name_text = self.medium_font.render(animal_name.capitalize(), True, (255, 255, 230))
                price_text = self.medium_font.render(f"${data['price']}", True, (255, 215, 100))
                income_text = self.small_font.render(f"Income: +${data['income']}/s", True, (150, 255, 150))
                
                self.game.screen.blit(name_text, (item_rect.left + text_offset, item_rect.top + 10))
                self.game.screen.blit(price_text, (item_rect.right - price_text.get_width() - 15, item_rect.top + 10))
                self.game.screen.blit(income_text, (item_rect.left + text_offset, item_rect.top + 40))  # more spacing  # adjusted from 35
                
                items_drawn += 1
            
            # draw scrollbar
            self.draw_scrollbar()
    
    def draw_scrollbar(self):
        """draw the scrollbar for props and animals tabs"""
        if self.current_tab not in [ShopTab.PROPS, ShopTab.ANIMALS]:
            return
        
        total_items = self.get_total_items_for_tab()
        
        # always show scrollbar if using virtual slots (even if items <= max_visible)
        # this ensures smooth scrolling even with few items
        effective_range = self.get_effective_scroll_range()
        if effective_range <= 0:
            return  # no scrolling needed
        
        # position scrollbar on the right side of shop content (moved 3px right from -115)
        content_y = self.shop_rect.y + 280
        scrollbar_x = self.shop_rect.x + self.shop_width - 112  # moved 3px right from -115
        scrollbar_y = content_y
        
        # calculate scrollbar height based on visible area
        item_height = 70
        item_spacing = 15
        visible_area_height = self.max_visible_items * (item_height + item_spacing) - item_spacing
        scrollbar_height = min(400, visible_area_height)
        
        # draw scrollbar background
        scroll_bg = pg.transform.scale(self.scroll_bg_img, (30, scrollbar_height))
        self.game.screen.blit(scroll_bg, (scrollbar_x, scrollbar_y))
        self.scroll_bar_rect = pg.Rect(scrollbar_x, scrollbar_y, 30, scrollbar_height)
        
        # calculate cursor position using effective scroll range (virtual slots)
        max_scroll = effective_range
        if max_scroll > 0:
            scroll_ratio = self.scroll_offset / max_scroll
            cursor_height = self.scroll_cursor_img.get_height()
            max_cursor_y = scrollbar_height - cursor_height
            cursor_y = scrollbar_y + int(scroll_ratio * max_cursor_y)
        else:
            cursor_y = scrollbar_y
        
        # draw scrollbar cursor (square, 1px left = 2px more to right from original -3)
        cursor_x = scrollbar_x - 1
        self.game.screen.blit(self.scroll_cursor_img, (cursor_x, cursor_y))
        self.scroll_cursor_rect = pg.Rect(cursor_x, cursor_y, 30, self.scroll_cursor_img.get_height())

    def draw_placement_hover(self):
        """draw placement preview"""
        if not self.hover_pos:
            return
        
        x, y = self.hover_pos
        
        if self.placement_mode == PlacementMode.BULLDOZER:
            # for bulldozer, show area to destroy
            tile = self.game.map.get_tile(x, y)
            if tile and tile.prop:
                prop = tile.prop
                color = (255, 100, 0, 120) if self.can_place else (255, 0, 0, 120)
                
                if prop.is_enclosure:
                    # highlight entire enclosure
                    for i in range(prop.width):
                        for j in range(prop.height):
                            world_x = (prop.x + i) * self.game.tile_size
                            world_y = (prop.y + j) * self.game.tile_size
                            screen_x, screen_y = self.game.camera.apply((world_x, world_y))
                            
                            hover_surface = pg.Surface((self.game.tile_size, self.game.tile_size))
                            hover_surface.set_alpha(color[3])
                            hover_surface.fill(color[:3])
                            self.game.screen.blit(hover_surface, (screen_x, screen_y))
                            pg.draw.rect(self.game.screen, color[:3], 
                                       (screen_x, screen_y, self.game.tile_size, self.game.tile_size), 2)
                else:
                    # highlight the prop
                    size = PROPS_SIZES.get(prop.name, (1, 1))
                    for i in range(int(size[0])):
                        for j in range(int(size[1])):
                            world_x = (prop.x + i) * self.game.tile_size
                            world_y = (prop.y + j) * self.game.tile_size
                            screen_x, screen_y = self.game.camera.apply((world_x, world_y))
                            
                            hover_surface = pg.Surface((self.game.tile_size, self.game.tile_size))
                            hover_surface.set_alpha(color[3])
                            hover_surface.fill(color[:3])
                            self.game.screen.blit(hover_surface, (screen_x, screen_y))
                            pg.draw.rect(self.game.screen, color[:3], 
                                       (screen_x, screen_y, self.game.tile_size, self.game.tile_size), 2)
            return
        
        color = (0, 255, 0, 100) if self.can_place else (255, 0, 0, 100)
        
        if self.placement_mode == PlacementMode.ENCLOSURE:
            width, height = self.enclosure_width, self.enclosure_height
        elif self.placement_mode == PlacementMode.PROP and self.selected_item:
            width, height = PROPS_SIZES.get(self.selected_item, (1, 1))
        else:
            width, height = 1, 1
        
        # draw highlighted tiles
        for i in range(int(width)):
            for j in range(int(height)):
                world_x = (x + i) * self.game.tile_size
                world_y = (y + j) * self.game.tile_size
                screen_x, screen_y = self.game.camera.apply((world_x, world_y))
                
                # semi-transparent surface
                hover_surface = pg.Surface((self.game.tile_size, self.game.tile_size))
                hover_surface.set_alpha(color[3])
                hover_surface.fill(color[:3])
                self.game.screen.blit(hover_surface, (screen_x, screen_y))
                
                # border
                pg.draw.rect(self.game.screen, color[:3], 
                           (screen_x, screen_y, self.game.tile_size, self.game.tile_size), 2)
    
    def draw_pause_menu(self):
        """draw pause menu"""
        # semi-transparent background to darken screen
        overlay = pg.Surface(self.game.current_res)
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.game.screen.blit(overlay, (0, 0))
        
        # pause menu background with image
        self.game.screen.blit(self.pause_bg_img, self.pause_rect.topleft)
        
        # draw pause menu buttons
        if self.pause_play_button:
            self.pause_play_button.draw(self.game.screen)
        if self.pause_quit_button:
            self.pause_quit_button.draw(self.game.screen)