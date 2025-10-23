"""
SlimeGobble - Player 类
管理玩家角色的所有功能：移动、动画、碰撞检测等
"""

import pygame
import json
import os
from config import *


class Player:
    """玩家类 - 控制可爱的史莱姆 Mumu"""
    
    def __init__(self, x, y):
        """
        初始化玩家
        Args:
            x: 玩家在地图上的x坐标（网格坐标）
            y: 玩家在地图上的y坐标（网格坐标）
        """
        self.grid_x = x
        self.grid_y = y
        self.x = x * TILE_SIZE  # 实际像素坐标
        self.y = y * TILE_SIZE
        self.speed = PLAYER_SPEED
        self.direction = 'front'  # 当前朝向：front, back, left, right
        self.moving = False  # 是否正在移动
        
        # 动画相关
        self.sprites = {}  # 存储四个方向的精灵图
        self.animations = {}  # 存储四个方向的动画数据
        self.current_frame = 0  # 当前动画帧
        self.animation_speed = 0.15  # 动画播放速度
        self.animation_counter = 0  # 动画计数器
        
        # 加载玩家资产
        self.load_assets()
        
        # 碰撞检测用的矩形
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
        
    def load_assets(self):
        """加载玩家的精灵图和动画数据"""
        directions = ['front', 'back', 'left', 'right']
        
        for direction in directions:
            # 加载PNG图像
            sprite_path = os.path.join(ASSETS_PATH, f'slime {direction}.png')
            json_path = os.path.join(ASSETS_PATH, f'slime {direction}.json')
            
            try:
                # 加载精灵图
                sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
                self.sprites[direction] = sprite_sheet
                
                # 加载动画JSON数据
                with open(json_path, 'r') as f:
                    self.animations[direction] = json.load(f)
                    
                print(f"成功加载玩家资产: slime {direction}")
            except Exception as e:
                print(f"警告：无法加载玩家资产 {direction}: {e}")
                # 如果加载失败，创建一个占位符表面
                self.sprites[direction] = pygame.Surface((TILE_SIZE, TILE_SIZE))
                self.sprites[direction].fill(GREEN)
                self.animations[direction] = {'frames': [{'frame': {'x': 0, 'y': 0, 'w': TILE_SIZE, 'h': TILE_SIZE}}]}
    
    def get_current_sprite(self):
        """
        获取当前帧的精灵图像
        Returns:
            pygame.Surface: 当前帧的图像
        """
        # 获取当前方向的动画数据
        anim_data = self.animations.get(self.direction, {})
        frames_data = anim_data.get('frames', [])
        
        if not frames_data:
            # 如果没有动画数据，返回整个精灵图
            sprite = self.sprites.get(self.direction)
            if sprite:
                return pygame.transform.scale(sprite, (TILE_SIZE, TILE_SIZE))
            else:
                # 返回占位符
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                surf.fill(GREEN)
                return surf
        
        # 兼容frames是字典或列表的情况
        if isinstance(frames_data, dict):
            # frames是字典: {"frame_0": {...}, "frame_1": {...}}
            frames_list = list(frames_data.values())
        elif isinstance(frames_data, list):
            # frames是列表: [{...}, {...}]
            frames_list = frames_data
        else:
            # 未知格式，返回整个精灵图
            sprite = self.sprites.get(self.direction)
            if sprite:
                return pygame.transform.scale(sprite, (TILE_SIZE, TILE_SIZE))
            else:
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                surf.fill(GREEN)
                return surf
        
        if not frames_list:
            # 空列表，返回整个精灵图
            sprite = self.sprites.get(self.direction)
            if sprite:
                return pygame.transform.scale(sprite, (TILE_SIZE, TILE_SIZE))
            else:
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                surf.fill(GREEN)
                return surf
        
        # 确保帧索引在范围内
        frame_index = int(self.current_frame) % len(frames_list)
        
        # 获取帧数据
        frame_item = frames_list[frame_index]
        if isinstance(frame_item, dict):
            # 格式1: {'frame': {'x': ..., 'y': ..., 'w': ..., 'h': ...}}
            frame_data = frame_item.get('frame', frame_item)
        else:
            # 格式2: 直接是frame数据
            frame_data = frame_item
        
        # 确保frame_data有必要的字段
        if not isinstance(frame_data, dict) or 'x' not in frame_data:
            # 无效格式，返回整个精灵图
            sprite = self.sprites.get(self.direction)
            if sprite:
                return pygame.transform.scale(sprite, (TILE_SIZE, TILE_SIZE))
            else:
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                surf.fill(GREEN)
                return surf
        
        # 从精灵图中提取当前帧
        sprite_sheet = self.sprites[self.direction]
        frame_rect = pygame.Rect(
            frame_data['x'],
            frame_data['y'],
            frame_data['w'],
            frame_data['h']
        )
        
        # 创建当前帧的表面
        frame_surface = pygame.Surface((frame_data['w'], frame_data['h']), pygame.SRCALPHA)
        frame_surface.blit(sprite_sheet, (0, 0), frame_rect)
        
        # 缩放到瓦片大小
        return pygame.transform.scale(frame_surface, (TILE_SIZE, TILE_SIZE))
    
    def update_animation(self):
        """更新动画帧"""
        if self.moving:
            anim_data = self.animations.get(self.direction, {})
            frames = anim_data.get('frames', [])
            
            if frames:
                self.animation_counter += self.animation_speed
                if self.animation_counter >= 1:
                    self.animation_counter = 0
                    self.current_frame = (self.current_frame + 1) % len(frames)
        else:
            # 不移动时重置到第一帧
            self.current_frame = 0
            self.animation_counter = 0
    
    def move(self, dx, dy, level_map):
        """
        移动玩家（优化转弯流畅度）
        Args:
            dx: x方向的移动增量（-1, 0, 1）
            dy: y方向的移动增量（-1, 0, 1）
            level_map: 当前关卡的地图数据
        """
        # 更新朝向
        if dx > 0:
            self.direction = 'right'
        elif dx < 0:
            self.direction = 'left'
        elif dy > 0:
            self.direction = 'front'
        elif dy < 0:
            self.direction = 'back'
        
        # 转弯自动对齐功能（让转弯更丝滑）
        alignment_threshold = 6  # 对齐阈值（像素）
        
        # 如果从水平方向转向垂直方向
        if dy != 0 and dx == 0:
            # 计算当前位置相对于网格中心的偏移
            grid_center_x = (self.x // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2
            offset_x = self.x + TILE_SIZE // 2 - grid_center_x
            
            # 如果偏移不大，自动对齐到中心
            if abs(offset_x) <= alignment_threshold:
                self.x = grid_center_x - TILE_SIZE // 2
                self.rect.x = self.x
        
        # 如果从垂直方向转向水平方向
        if dx != 0 and dy == 0:
            # 计算当前位置相对于网格中心的偏移
            grid_center_y = (self.y // TILE_SIZE) * TILE_SIZE + TILE_SIZE // 2
            offset_y = self.y + TILE_SIZE // 2 - grid_center_y
            
            # 如果偏移不大，自动对齐到中心
            if abs(offset_y) <= alignment_threshold:
                self.y = grid_center_y - TILE_SIZE // 2
                self.rect.y = self.y
        
        # 计算新位置
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # 分别检测x和y方向的碰撞（滑墙效果）
        moved = False
        
        # 先尝试只在x方向移动
        if dx != 0:
            test_rect = pygame.Rect(new_x, self.y, TILE_SIZE, TILE_SIZE)
            if not self.check_collision(test_rect, level_map):
                self.x = new_x
                self.rect.x = self.x
                moved = True
        
        # 再尝试只在y方向移动
        if dy != 0:
            test_rect = pygame.Rect(self.x, new_y, TILE_SIZE, TILE_SIZE)
            if not self.check_collision(test_rect, level_map):
                self.y = new_y
                self.rect.y = self.y
                moved = True
        
        self.moving = moved
    
    def check_collision(self, rect, level_map):
        """
        检查给定矩形是否与墙壁碰撞
        Args:
            rect: 要检查的矩形
            level_map: 当前关卡的地图数据
        Returns:
            bool: 如果发生碰撞返回True，否则返回False
        """
        # 缩小碰撞箱，减少卡墙问题
        margin = 2  # 2像素的容错边距
        test_rect = pygame.Rect(
            rect.left + margin,
            rect.top + margin,
            rect.width - margin * 2,
            rect.height - margin * 2
        )
        
        # 获取矩形四个角对应的网格坐标
        corners = [
            (test_rect.left, test_rect.top),
            (test_rect.right - 1, test_rect.top),
            (test_rect.left, test_rect.bottom - 1),
            (test_rect.right - 1, test_rect.bottom - 1)
        ]
        
        for corner_x, corner_y in corners:
            # 转换为网格坐标
            grid_x = corner_x // TILE_SIZE
            grid_y = corner_y // TILE_SIZE
            
            # 检查是否越界
            if grid_y < 0 or grid_y >= len(level_map) or grid_x < 0 or grid_x >= len(level_map[0]):
                return True
            
            # 检查是否是墙壁
            if level_map[grid_y][grid_x] == WALL:
                return True
        
        return False
    
    def update(self, keys, level_map):
        """
        更新玩家状态
        Args:
            keys: pygame.key.get_pressed() 返回的按键状态
            level_map: 当前关卡的地图数据
        """
        dx, dy = 0, 0
        
        # 检测WASD按键
        if keys[pygame.K_w]:
            dy = -1
        elif keys[pygame.K_s]:
            dy = 1
        elif keys[pygame.K_a]:
            dx = -1
        elif keys[pygame.K_d]:
            dx = 1
        
        # 如果有按键按下，移动玩家
        if dx != 0 or dy != 0:
            self.move(dx, dy, level_map)
        else:
            self.moving = False
        
        # 更新动画
        self.update_animation()
    
    def draw(self, screen, camera_offset=(0, 0)):
        """
        绘制玩家
        Args:
            screen: pygame显示表面
            camera_offset: 相机偏移量（用于滚动）
        """
        sprite = self.get_current_sprite()
        screen.blit(sprite, (self.x + camera_offset[0], self.y + camera_offset[1]))
    
    def reset_position(self, x, y):
        """
        重置玩家位置（例如碰到敌人后）
        Args:
            x: 网格x坐标
            y: 网格y坐标
        """
        self.grid_x = x
        self.grid_y = y
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.rect.x = self.x
        self.rect.y = self.y
        self.direction = 'front'
        self.moving = False
        self.current_frame = 0
