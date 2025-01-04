import pygame
import sys
import os
import math
from aircapitan.sim.planesim import PlaneSim


class AirPlaneGame:

    def __init__(self, sim: PlaneSim):

        self.sim = sim
        pygame.init()
        self.clock = pygame.time.Clock()

        game_root = os.path.dirname(os.path.realpath(__file__))
        assets_root = os.path.join(game_root, 'assets')

        self.surface = pygame.display.set_mode((640, 480), pygame.RESIZABLE)

        pygame.display.set_caption("Air Capitan")
        self.rock_texture = pygame.image.load(os.path.join(
            assets_root, 'rock.jpeg')).convert()

        self.plane_image = pygame.image.load(os.path.join(
            assets_root, 'plane.png')).convert()

        self.roll_indicator_image = pygame.image.load(os.path.join(
            assets_root, 'roll_indicator_inner.png')).convert()

        self.roll_indicator_outter = pygame.image.load(os.path.join(
            assets_root, 'roll_indicator_outter.png')).convert()

        self.info_text_font = pygame.font.SysFont('consolas', 12)
        self.height_to_width = 1.0

    def screen_width_m(self):
        min_screen_width_m = 150
        max_screen_width_m = 500

        min_ground_speed_mps = 5
        max_ground_speed_mps = 40

        ground_speed_mps = self.sim.airspeed_mps
        if ground_speed_mps < min_ground_speed_mps:
            return min_screen_width_m

        if ground_speed_mps > max_ground_speed_mps:
            return max_screen_width_m

        speed_range = max_ground_speed_mps - min_ground_speed_mps
        screen_range = max_screen_width_m - min_screen_width_m

        speed_fraction = (ground_speed_mps -
                          min_ground_speed_mps) / speed_range

        return speed_fraction * screen_range + min_screen_width_m

    def screen_height_m(self):
        return self.screen_width_m() * self.height_to_width

    def plane_relative_location_on_screen(self):
        return (0.25, 0.75)

    def plane_location_on_screen(self):
        rel_loc = self.plane_relative_location_on_screen()
        loc_x_pix = int(rel_loc[0] * self.surface.get_width())
        loc_y_pix = int(rel_loc[1] * self.surface.get_height())
        return (loc_x_pix, loc_y_pix)

    def get_screen_rect_m(self):
        width_m = self.screen_width_m()
        height_m = self.screen_height_m()

        relative_plane_x, relative_plane_y = self.plane_relative_location_on_screen()

        plane_m_offset_bottom = (1.0 - relative_plane_y) * height_m
        plane_m_offset_left = (relative_plane_x) * width_m

        screen_start_x_m = self.sim.position_m - plane_m_offset_left
        screen_start_y_m = self.sim.altitude_m - plane_m_offset_bottom

        return (screen_start_x_m, screen_start_y_m, width_m, height_m)

    def draw_horizontal_lines_at_altitudes(self, alts, width=1, color=(128, 128, 128)):
        screen_x_m, screen_y_m, screen_w_m, screen_h_m = self.get_screen_rect_m()
        for alt in alts:
            fy = (alt - screen_y_m) / (screen_h_m)
            y = int((1.0 - fy) * self.surface.get_height())
            pygame.draw.line(self.surface, color, (0, y),
                             (self.surface.get_width(), y), width=width)

    def draw_vertical_lines_at_positions(self, list_of_pos, width=1, color=(128, 128, 128)):
        screen_x_m, screen_y_m, screen_w_m, screen_h_m = self.get_screen_rect_m()
        for pos_m in list_of_pos:
            fx = (pos_m - screen_x_m) / (screen_w_m)
            x = int(fx * self.surface.get_width())
            pygame.draw.line(self.surface, color, (x, 0),
                             (x, self.surface.get_height()), width=width)

    def draw_grid(self, step, width, color):
        screen_x_m, screen_y_m, screen_w_m, screen_h_m = self.get_screen_rect_m()
        pos_i_m = math.floor((screen_x_m - step) / step) * step
        alt_i_m = math.floor((screen_y_m - step) / step) * step

        vertical_lines_pos_m = []
        while pos_i_m <= (screen_x_m + screen_w_m):
            vertical_lines_pos_m.append(pos_i_m)
            pos_i_m += step

        horizontal_lines_alt_m = []
        while alt_i_m < (screen_y_m + screen_w_m):
            horizontal_lines_alt_m.append(alt_i_m)
            alt_i_m += step

        self.draw_vertical_lines_at_positions(
            vertical_lines_pos_m, width, color)
        self.draw_horizontal_lines_at_altitudes(
            horizontal_lines_alt_m, width, color)

    def draw_background(self):
        screen_x_m, screen_y_m, screen_w_m, screen_h_m = self.get_screen_rect_m()

        self.draw_grid(step=50, width=1, color=(200, 200, 200))
        self.draw_grid(step=1000, width=2, color=(120, 120, 120))

        fy = (0 - screen_y_m) / (screen_h_m)
        y = int((1.0 - fy) * self.surface.get_height())

        pygame.draw.rect(self.surface, (100, 100, 100), (0, y,
                         self.surface.get_width(), self.surface.get_height()))

    def draw_roll_indicator(self):

        roll = math.degrees(self.sim.plane_roll_rad)
        rotated_image_center = (
            0, 0
        )

        rotated_sprite = pygame.transform.rotozoom(
            self.roll_indicator_outter, roll, 1.0)

        rotated_image_rect = rotated_sprite.get_rect(
            center=rotated_image_center)

        self.surface.blit(rotated_sprite, rotated_image_rect.move(
            self.surface.get_width() -
            self.roll_indicator_outter.get_width(
            ) / 2 - 10, self.roll_indicator_outter.get_height() / 2 + 10

        ))

    def draw_plane(self):
        fraction_length = self.sim.length_m / self.screen_width_m()

        # img_h_to_w = self.plane_image.get_height() / self.plane_image.get_width()

        # new_width_pix = int(fraction_length * self.surface.get_width())
        # new_height_pix = int(new_width_pix * img_h_to_w)

        # zoom_as_fraction_of_original_size = new_width_pix / self.plane_image.get_width()

        # picture = pygame.transform.scale(
        #    self.plane_image, (new_with_pix, new_height_pix))

        # self.surface.blit(picture, self.plane_location_on_screen())

        pitch = math.degrees(self.sim.plane_pitch_rad)

        rotated_image_center = (
            0, 0
        )
        rotated_sprite = pygame.transform.rotozoom(
            self.plane_image, pitch, 1.0)

        rotated_image_rect = rotated_sprite.get_rect(
            center=rotated_image_center)

        self.surface.blit(rotated_sprite, rotated_image_rect.move(
            self.plane_location_on_screen()))

    def draw_stats(self):
        def fmt_float(v, uom):
            return "%2.2f %s" % (v, uom)

        content = [
            ('fdm time', fmt_float(self.sim.fdm_time_s, 's')),
            ('game time', fmt_float(self.sim.sim_time_s, 's')),
            ('altitude', fmt_float(self.sim.altitude_m, 'm')),
            ('position', fmt_float(self.sim.position_m, 'm')),
            ('vertical speed', fmt_float(self.sim.vertical_speed_mps, 'm/s')),
            ('ground speed', fmt_float(self.sim.ground_speed_mps, 'm/s')),
            ('air speed', fmt_float(self.sim.airspeed_mps, 'm/s')),
            None,
            ('plane roll ', fmt_float(math.degrees(self.sim.plane_roll_rad), 'deg')),
            ('plane pitch ', fmt_float(math.degrees(self.sim.plane_pitch_rad), 'deg')),
            ('plane heading ', fmt_float(math.degrees(
                self.sim.plane_heading_rad), 'deg')),

            None,
            ('Engine RPMs', fmt_float(self.sim.engine_rpm, 'rpm')),
            None,
            ('cmd thrust level', fmt_float(self.sim.cmd_thrust_level, '%')),
            ('cmd elevator', fmt_float(self.sim.cmd_elevator, '')),
            ('cmd rudder', fmt_float(self.sim.cmd_rudder, '')),
            ('cmd aileron', fmt_float(self.sim.cmd_aileron, '')),
            None,
        ]

        y_offset = 10
        x_offset = 10

        for itm in content:
            if itm is None:
                img = self.info_text_font.render(
                    f'---', 1, (0, 0, 255))
            else:
                label, value = itm
                img = self.info_text_font.render(
                    f'{label}: {value}', 1, (0, 0, 255))
            self.surface.blit(img, (x_offset, y_offset))
            y_offset += img.get_size()[1]

    def run(self):

        FPS = 60
        while True:

            dt = self.clock.tick(FPS)/1000
            self.sim.propagate(dt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.VIDEORESIZE:

                    self.surface = pygame.display.set_mode((event.w, event.h),
                                                           pygame.RESIZABLE)

                keys = pygame.key.get_pressed()
                if keys[pygame.K_EQUALS]:

                    self.sim.set_cmd_thrust(self.sim.get_cmd_thrust() + 0.05)

                if keys[pygame.K_MINUS]:

                    self.sim.set_cmd_thrust(self.sim.get_cmd_thrust() - 0.05)

                rudder = 0.0
                if keys[pygame.K_COMMA]:
                    rudder = -1.0

                if keys[pygame.K_PERIOD]:
                    rudder = 1.0

                self.sim.set_cmd_rudder(rudder)

                aileron = 0.0
                if keys[pygame.K_LEFT]:
                    aileron = 1.0

                if keys[pygame.K_RIGHT]:
                    aileron = -1.0

                self.sim.set_cmd_aileron(aileron)

                elevator = 0.0
                if keys[pygame.K_UP]:
                    elevator = 1.0

                if keys[pygame.K_DOWN]:
                    elevator = -1.0

                self.sim.set_cmd_elevator(elevator)

                if keys[pygame.K_q]:
                    if self.sim.flap_deflection_rad < math.radians(50):
                        self.sim.flap_deflection_rad += 0.08
                if keys[pygame.K_a]:
                    if self.sim.flap_deflection_rad > 0:
                        self.sim.flap_deflection_rad -= 0.08

            self.surface.fill((255, 255, 255))

            self.draw_background()
            self.draw_roll_indicator()
            self.draw_plane()
            self.draw_stats()
            pygame.display.flip()


if __name__ == '__main__':
    sim = PlaneSim()
    game = AirPlaneGame(sim)
    game.run()
