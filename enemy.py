"""
SlimeGobble - Enemy 类
管理敌人角色的所有功能：AI、移动、动画等
"""

import pygame
import json
import os
import random
from config import *


class Enemy:
    """敌人类 - 追逐玩家的Chaser"""
    
    def __init__(self, x, y, ai_mode='random', speed=ENEMY_SPEED_LEVEL1):
        """
        初始化敌人
        Args:
            x: 敌人在地图上的x坐标（网格坐标）
            y: 敌人在地图上的y坐标（网格坐标）
            ai_mode: AI模式 ('random', 'chase', 'fast_chase')
            speed: 移动速度
        """
        self.grid_x = x
        self.grid_y = y
        self.x = x * TILE_SIZE  # 实际像素坐标
        self.y = y * TILE_SIZE
        self.spawn_x = x  # 记录出生点
        self.spawn_y = y
        self.speed = speed
        self.ai_mode = ai_mode
        self.direction = 'front'  # 当前朝向
        self.moving = False
        
        # 动画相关
        self.sprites = {}
        self.animations = {}
        self.current_frame = 0
        self.animation_speed = 0.15
        self.animation_counter = 0
        
        # AI相关
        self.direction_change_timer = 0  # 随机AI的方向切换计时器
        self.direction_change_interval = 60  # 每60帧切换一次方向
        
        # 加载敌人资产
        self.load_assets()
        
        # 碰撞检测用的矩形
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
    
    def load_assets(self):
        """加载敌人的精灵图和动画数据"""
        directions = ['front', 'back', 'left', 'right']
        
        for direction in directions:
            # 加载PNG图像
            sprite_path = os.path.join(ASSETS_PATH, f'Chaser {direction}.png')
            json_path = os.path.join(ASSETS_PATH, f'Chaser {direction}.json')
            
            try:
                # 加载精灵图
                sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
                self.sprites[direction] = sprite_sheet
                
                # 加载动画JSON数据
                with open(json_path, 'r') as f:
                    self.animations[direction] = json.load(f)
                    
                print(f"成功加载敌人资产: Chaser {direction}")
            except Exception as e:
                print(f"警告：无法加载敌人资产 {direction}: {e}")
                # 如果加载失败，创建一个占位符表面（红色方块）
                self.sprites[direction] = pygame.Surface((TILE_SIZE, TILE_SIZE))
                self.sprites[direction].fill(RED)
                self.animations[direction] = {'frames': []}
    
    def get_current_sprite(self):
        """获取当前帧的精灵图像"""
        # 与Player类相同的逻辑
        anim_data = self.animations.get(self.direction, {})
        frames_data = anim_data.get('frames', [])
        
        if not frames_data:
            sprite = self.sprites.get(self.direction)
            if sprite:
                return pygame.transform.scale(sprite, (TILE_SIZE, TILE_SIZE))
            else:
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                surf.fill(RED)
                return surf
        
        # 兼容frames是字典或列表
        if isinstance(frames_data, dict):
            frames_list = list(frames_data.values())
        elif isinstance(frames_data, list):
            frames_list = frames_data
        else:
            sprite = self.sprites.get(self.direction)
            if sprite:
                return pygame.transform.scale(sprite, (TILE_SIZE, TILE_SIZE))
            else:
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                surf.fill(RED)
                return surf
        
        if not frames_list:
            sprite = self.sprites.get(self.direction)
            if sprite:
                return pygame.transform.scale(sprite, (TILE_SIZE, TILE_SIZE))
            else:
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                surf.fill(RED)
                return surf
        
        frame_index = int(self.current_frame) % len(frames_list)
        frame_item = frames_list[frame_index]
        
        if isinstance(frame_item, dict):
            frame_data = frame_item.get('frame', frame_item)
        else:
            frame_data = frame_item
        
        if not isinstance(frame_data, dict) or 'x' not in frame_data:
            sprite = self.sprites.get(self.direction)
            if sprite:
                return pygame.transform.scale(sprite, (TILE_SIZE, TILE_SIZE))
            else:
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                surf.fill(RED)
                return surf
        
        sprite_sheet = self.sprites[self.direction]
        frame_rect = pygame.Rect(
            frame_data['x'],
            frame_data['y'],
            frame_data['w'],
            frame_data['h']
        )
        
        frame_surface = pygame.Surface((frame_data['w'], frame_data['h']), pygame.SRCALPHA)
        frame_surface.blit(sprite_sheet, (0, 0), frame_rect)
        
        return pygame.transform.scale(frame_surface, (TILE_SIZE, TILE_SIZE))
    
    def update_animation(self):
        """更新动画帧"""
        if self.moving:
            anim_data = self.animations.get(self.direction, {})
            frames_data = anim_data.get('frames', [])
            
            if isinstance(frames_data, dict):
                frames = list(frames_data.values())
            else:
                frames = frames_data
            
            if frames:
                self.animation_counter += self.animation_speed
                if self.animation_counter >= 1:
                    self.animation_counter = 0
                    self.current_frame = (self.current_frame + 1) % len(frames)
        else:
            self.current_frame = 0
            self.animation_counter = 0
    
    def check_collision(self, rect, level_map):
        """检查碰撞"""
        corners = [
            (rect.left, rect.top),
            (rect.right - 1, rect.top),
            (rect.left, rect.bottom - 1),
            (rect.right - 1, rect.bottom - 1)
        ]
        
        for corner_x, corner_y in corners:
            grid_x = corner_x // TILE_SIZE
            grid_y = corner_y // TILE_SIZE
            
            if grid_y < 0 or grid_y >= len(level_map) or grid_x < 0 or grid_x >= len(level_map[0]):
                return True
            
            if level_map[grid_y][grid_x] == WALL:
                return True
        
        return False
    
    def move_random(self, level_map):
        """随机移动AI"""
        self.direction_change_timer += 1
        
        # 每隔一段时间随机改变方向
        if self.direction_change_timer >= self.direction_change_interval:
            self.direction_change_timer = 0
            directions = [(-1, 0, 'left'), (1, 0, 'right'), (0, -1, 'back'), (0, 1, 'front')]
            random.shuffle(directions)
            
            # 尝试每个方向，找到第一个可行的
            for dx, dy, dir_name in directions:
                test_rect = pygame.Rect(
                    self.x + dx * self.speed,
                    self.y + dy * self.speed,
                    TILE_SIZE, TILE_SIZE
                )
                if not self.check_collision(test_rect, level_map):
                    self.direction = dir_name
                    break
        
        # 按当前方向移动
        dx, dy = 0, 0
        if self.direction == 'left':
            dx = -1
        elif self.direction == 'right':
            dx = 1
        elif self.direction == 'back':
            dy = -1
        elif self.direction == 'front':
            dy = 1
        
        # 分别尝试x和y方向
        moved = False
        if dx != 0:
            test_rect = pygame.Rect(self.x + dx * self.speed, self.y, TILE_SIZE, TILE_SIZE)
            if not self.check_collision(test_rect, level_map):
                self.x += dx * self.speed
                self.rect.x = self.x
                moved = True
            else:
                # 碰墙了，立即换方向
                self.direction_change_timer = self.direction_change_interval
        
        if dy != 0:
            test_rect = pygame.Rect(self.x, self.y + dy * self.speed, TILE_SIZE, TILE_SIZE)
            if not self.check_collision(test_rect, level_map):
                self.y += dy * self.speed
                self.rect.y = self.y
                moved = True
            else:
                # 碰墙了，立即换方向
                self.direction_change_timer = self.direction_change_interval
        
        self.moving = moved
    
    def move_chase(self, player, level_map):
        """追踪玩家AI"""
        # 计算到玩家的方向
        dx = player.x - self.x
        dy = player.y - self.y
        
        # 选择优先移动方向（曼哈顿距离）
        if abs(dx) > abs(dy):
            # 优先水平移动
            if dx > 0:
                self.direction = 'right'
                test_x = self.x + self.speed
                test_y = self.y
            else:
                self.direction = 'left'
                test_x = self.x - self.speed
                test_y = self.y
        else:
            # 优先垂直移动
            if dy > 0:
                self.direction = 'front'
                test_x = self.x
                test_y = self.y + self.speed
            else:
                self.direction = 'back'
                test_x = self.x
                test_y = self.y - self.speed
        
        # 尝试移动
        test_rect = pygame.Rect(test_x, test_y, TILE_SIZE, TILE_SIZE)
        if not self.check_collision(test_rect, level_map):
            self.x = test_x
            self.y = test_y
            self.rect.x = self.x
            self.rect.y = self.y
            self.moving = True
        else:
            # 如果主方向被挡，尝试另一个方向
            if abs(dx) > abs(dy):
                # 尝试垂直移动
                if dy > 0:
                    self.direction = 'front'
                    test_y = self.y + self.speed
                else:
                    self.direction = 'back'
                    test_y = self.y - self.speed
                test_x = self.x
            else:
                # 尝试水平移动
                if dx > 0:
                    self.direction = 'right'
                    test_x = self.x + self.speed
                else:
                    self.direction = 'left'
                    test_x = self.x - self.speed
                test_y = self.y
            
            test_rect = pygame.Rect(test_x, test_y, TILE_SIZE, TILE_SIZE)
            if not self.check_collision(test_rect, level_map):
                self.x = test_x
                self.y = test_y
                self.rect.x = self.x
                self.rect.y = self.y
                self.moving = True
            else:
                self.moving = False
    
    def update(self, player, level_map):
        """更新敌人状态"""
        if self.ai_mode == 'random':
            self.move_random(level_map)
        elif self.ai_mode in ['chase', 'fast_chase']:
            self.move_chase(player, level_map)
        
        # 更新动画
        self.update_animation()
    
    def draw(self, screen):
        """绘制敌人"""
        sprite = self.get_current_sprite()
        screen.blit(sprite, (self.x, self.y))
    
    def reset_position(self):
        """重置到出生点"""
        self.x = self.spawn_x * TILE_SIZE
        self.y = self.spawn_y * TILE_SIZE
        self.rect.x = self.x
        self.rect.y = self.y
        self.direction = 'front'
        self.moving = False
        self.current_frame = 0
        self.direction_change_timer = 0
    
    def check_collision_with_player(self, player):
        """检查是否与玩家碰撞"""
        return self.rect.colliderect(player.rect)
