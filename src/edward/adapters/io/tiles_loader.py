
import local_data
import pygame, csv, os
import json

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.parse_sprite(image)
        #print (x,y)
        # Manual load in: self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class TileMap():
    def __init__(self, filename, spritesheet):
        self.tile_size = 16
        self.start_x, self.start_y = 0, 0
        self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def draw_map(self, surface):
        surface.blit(self.map_surface, (0 ,0))

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def change_me(self ,x ,y):  # a tjh test
        print ('my data' ,local_data.mapx)
        print('mycell' ,local_data.mapx[y][x])

        local_data.mapx[y][x] = 1


    def read_csv(self, filename):
        map = []

        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        # local_data.mapx=map
        # print(local_data.mapx) # which is in form list of lists
        #print ('map in read-csv' ,map)
        return map

    def load_tiles(self, filename):
        tiles = []
        map = self.read_csv(filename)
        local_data.mapx = map # hughes addition

        x, y = 0, 0
        # for row in map:
        for row in local_data.mapx: # hughes mod
            x = 0
            for tile in row:
                if tile == '0':
                    self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
                elif tile == '1':
                    tiles.append(Tile('beach.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '2':
                    tiles.append(Tile('rocks.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '3':
                    tiles.append(Tile('calm.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '4':
                    tiles.append(Tile('land.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '5':
                    tiles.append(Tile('northsouth.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '6':
                    tiles.append(Tile('gulf.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '7':
                    tiles.append(Tile('eastwest.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '8':
                    tiles.append(Tile('westeast.png', x * self.tile_size, y * self.tile_size, self.spritesheet))



                    # Move to next tile in current row
                x += 1

            # Move to next row
            y += 1
            # Store the size of the tile map
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        #print('self tile size' ,self.tile_size)
        #print('map in load_tiles', map)
        # print(tiles)
        return tiles

    def load_tiles_mod(self):
        tiles = []
        # map = self.read_csv(filename)
        # local_data.mapx = map  # hughes addition

        x, y = 0, 0
        # for row in local data:
        for row in local_data.mapx:  # hughes mod
            x = 0
            for tile in row:
                if tile == '0':
                    pass
                    # self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
                elif tile == '1':
                    tiles.append('beach.png')
                elif tile == '2':
                    tiles.append('beach.png')
                    # Move to next tile in current row
                x += 1

            # Move to next row
            y += 1
            # Store the size of the tile map
        # self.map_w, self.map_h = x * self.tile_size, y * self.tile_size

        return tiles

    def write_csv(self):
        with open('output.csv', 'w', newline='') as csvfile:
            # Create a CSV writer object
            writer = csv.writer(csvfile)

            # Write the data
            writer.writerows(local_data.mapx)

        return

###########from spritesheet

class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.meta_data = self.filename.replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()



    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        #sprite.set_colorkey((0,0,0))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet,(0, 0),(x, y, w, h))
        return sprite

    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_sprite(x, y, w, h)
        return image




