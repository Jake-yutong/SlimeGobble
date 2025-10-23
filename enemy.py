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
        # 初始随机方向，让敌人开始就游荡
        self.direction = random.choice(['front', 'back', 'left', 'right'])
        self.moving = True  # 开始就处于移动状态
        
        # 动画相关
        self.sprites = {}
        self.animations = {}
        self.current_frame = 0
        self.animation_speed = 0.15
        self.animation_counter = 0
        
        # AI相关
        self.direction_change_timer = random.randint(0, 30)  # 随机初始计时器，让敌人不同步
        self.direction_change_interval = 60  # 每60帧切换一次方向
        self.chase_update_timer = random.randint(0, 10)  # 随机初始计时器
        self.chase_update_interval = 20 if ai_mode == 'chase' else 10  # chase模式每20帧更新一次路径，fast_chase每10帧
        
        # 加载敌人资产
        self.load_assets()
        
        # 碰撞检测用的矩形
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
    
    def load_assets(self):
        """加载敌人的精灵图（只需PNG，不需要JSON动画）"""
        # 文件名映射: front=下, back=上, left=左, right=右
        direction_files = {
            'front': 'Chaser front',  # 下
            'back': 'Chaser back',    # 上
            'left': 'Chaser left',    # 左
            'right': 'Chaser right'   # 右
        }
        
        print(f"\n=== 加载敌人贴图 ===")
        print(f"资产路径: {ASSETS_PATH}")
        
        for direction, filename in direction_files.items():
            # 只加载PNG图像（不需要JSON）
            sprite_path = os.path.join(ASSETS_PATH, f'{filename}.png')
            
            try:
                # 加载精灵图
                sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
                self.sprites[direction] = sprite_sheet
                # 创建简单的静态"动画"（只有一帧）
                self.animations[direction] = {'frames': []}
                print(f"  ✓ 成功加载: {filename}.png")
            except Exception as e:
                print(f"  ✗ 无法加载 {filename}.png: {e}")
                # 如果加载失败，创建红色方块占位符
                self.sprites[direction] = pygame.Surface((TILE_SIZE, TILE_SIZE))
                self.sprites[direction].fill(RED)
                self.animations[direction] = {'frames': []}
        
        print(f"===================\n")
    
    def get_current_sprite(self):
        """获取当前帧的精灵图像（静态图片，不需要动画）"""
        sprite = self.sprites.get(self.direction)
        if sprite:
            # 直接缩放到TILE_SIZE并返回
            return pygame.transform.scale(sprite, (TILE_SIZE, TILE_SIZE))
        else:
            # 如果没有加载成功，返回红色方块
            surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            surf.fill(RED)
            return surf
        
        return pygame.transform.scale(frame_surface, (TILE_SIZE, TILE_SIZE))
    
    def update_animation(self):
        """更新动画帧（敌人使用静态图片，此方法保留但不需要复杂逻辑）"""
        # 敌人使用静态PNG图片，不需要帧动画
        pass
    
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
        """追踪玩家AI（有思考延迟，远距离游荡）"""
        # 计算到玩家的距离
        dx = player.x - self.x
        dy = player.y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        
        # 设置追踪距离阈值（以像素为单位）
        chase_distance = TILE_SIZE * 8  # 8格以内才开始追踪
        
        # 如果玩家距离太远，使用游荡模式
        if distance > chase_distance:
            self.move_random(level_map)
            return
        
        # 更新追踪计时器
        self.chase_update_timer += 1
        
        # 只在特定帧数更新追踪方向（不是每帧都追）
        if self.chase_update_timer >= self.chase_update_interval:
            self.chase_update_timer = 0
            
            # 选择优先移动方向（曼哈顿距离）
            if abs(dx) > abs(dy):
                # 优先水平移动
                if dx > 0:
                    self.target_direction = 'right'
                else:
                    self.target_direction = 'left'
            else:
                # 优先垂直移动
                if dy > 0:
                    self.target_direction = 'front'
                else:
                    self.target_direction = 'back'
        
        # 使用目标方向（如果还没设置，先设置）
        if not hasattr(self, 'target_direction'):
            self.target_direction = self.direction
        
        self.direction = self.target_direction
        
        # 计算移动
        test_x, test_y = self.x, self.y
        if self.direction == 'right':
            test_x = self.x + self.speed
        elif self.direction == 'left':
            test_x = self.x - self.speed
        elif self.direction == 'front':
            test_y = self.y + self.speed
        elif self.direction == 'back':
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
            # 如果被挡，尝试转向（简单处理，随机选个其他方向）
            self.moving = False
            # 重新计算路径
            self.chase_update_timer = self.chase_update_interval
    
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
        """重置到出生点（重置后继续游荡）"""
        self.x = self.spawn_x * TILE_SIZE
        self.y = self.spawn_y * TILE_SIZE
        self.rect.x = self.x
        self.rect.y = self.y
        # 随机新的方向，继续游荡
        self.direction = random.choice(['front', 'back', 'left', 'right'])
        self.moving = True
        self.current_frame = 0
        self.direction_change_timer = random.randint(0, 30)
    
    def check_collision_with_player(self, player):
        """检查是否与玩家碰撞"""
        return self.rect.colliderect(player.rect)
