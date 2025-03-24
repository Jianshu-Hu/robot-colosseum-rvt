from typing import List

import numpy as np
from pyrep.objects.proximity_sensor import ProximitySensor
from pyrep.objects.shape import Shape
from rlbench.backend.conditions import DetectedCondition, NothingGrasped
from rlbench.backend.task import Task
from rlbench.const import colors
import random
from colosseum.rlbench.extensions.spawn_boundary import SpawnBoundaryExt


class StackFourCups(Task):
    def init_task(self) -> None:
        success_sensor = ProximitySensor("success")
        self.cup1 = Shape("cup1")
        self.cup2 = Shape("cup2")
        self.cup3 = Shape("cup3")
        self.cup4 = Shape("cup4")
        self.cup1_visual = Shape("cup1_visual")
        self.cup2_visual = Shape("cup2_visual")
        self.cup3_visaul = Shape("cup3_visual")
        self.cup4_visaul = Shape("cup4_visual")

        self.register_graspable_objects([self.cup1, self.cup2, self.cup3, self.cup4])
        self.register_success_conditions(
            [
                DetectedCondition(self.cup1, success_sensor),
                DetectedCondition(self.cup3, success_sensor),
                DetectedCondition(self.cup4, success_sensor),
                NothingGrasped(self.robot.gripper),
            ]
        )
        self.boundary = SpawnBoundaryExt([Shape('boundary')])

    def init_episode(self, index: int) -> List[str]:
        self.variation_index = index
        index = np.random.choice(len(colors))
        target_color_name, target_rgb = colors[index]

        random_idx = np.random.choice(len(colors))
        while random_idx == index:
            random_idx = np.random.choice(len(colors))
        other1_color_name, other1_rgb = colors[random_idx]

        random_idx = np.random.choice(len(colors))
        while random_idx == index:
            random_idx = np.random.choice(len(colors))
        other2_color_name, other2_rgb = colors[random_idx]

        random_idx = np.random.choice(len(colors))
        while random_idx == index:
            random_idx = np.random.choice(len(colors))
        other3_color_name, other3_rgb = colors[random_idx]

        self.cup2_visual.set_color(target_rgb)
        self.cup1_visual.set_color(other1_rgb)
        self.cup3_visaul.set_color(other2_rgb)
        self.cup4_visaul.set_color(other3_rgb)

        # switch position of cups
        pos_cups = [self.cup1.get_position(), self.cup2.get_position(), self.cup3.get_position(), self.cup4.get_position()]

        cup_ind_list = [0, 1, 2, 3]
        random.shuffle(cup_ind_list)

        self.boundary.clear()
        self.cup1.set_position(pos_cups[cup_ind_list[0]])
        self.cup2.set_position(pos_cups[cup_ind_list[1]])
        self.cup3.set_position(pos_cups[cup_ind_list[2]])
        self.cup4.set_position(pos_cups[cup_ind_list[3]])

        return [
            f'stack the {other1_color_name} cup and the {other2_color_name} cup and the {other3_color_name} cup '
            f'on top of the {target_color_name} cup',
            "stack the other cups on top of the %s cup" % target_color_name,
            "place three of the cups onto the odd cup out",
            "put the remaining three cups on top of the %s cup"
            % target_color_name,
            "pick up and set the cups down into the %s cup" % target_color_name,
            "create a stack of cups with the %s cup as its base"
            % target_color_name,
            "keeping the %s cup on the table, stack the other three onto it"
            % target_color_name,
        ]

    def variation_count(self) -> int:
        return len(colors)
